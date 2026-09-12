// AN Paint JNI integration, 2026-09-10. AGPL-3.0-or-later.
// JPEG XL library: JPEG XL Project Authors, BSD-3-Clause.
#include <jni.h>
#include <android/bitmap.h>
#include <jxl/decode.h>
#include <jxl/encode.h>
#include <jxl/color_encoding.h>
#include <jxl/cms.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <algorithm>
#include <array>
#include <atomic>
#include <climits>
#include <cerrno>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>
#include "ColourConversion.h"

namespace {
struct Budget {
    size_t limit; std::atomic<size_t> used{0}; bool exhausted=false;
    struct alignas(std::max_align_t) Header {size_t size;};
    static void* alloc(void* opaque,size_t size) {
        auto& b=*static_cast<Budget*>(opaque);
        const size_t total=size+sizeof(Header);
        if(total<size || total>b.limit || b.used.load()>b.limit-total) {b.exhausted=true;return nullptr;}
        auto* h=static_cast<Header*>(std::malloc(total));
        if(!h) {b.exhausted=true;return nullptr;}
        h->size=total;b.used+=total;return h+1;
    }
    static void free(void* opaque,void* ptr) {
        if(!ptr)return;auto* h=static_cast<Header*>(ptr)-1;
        static_cast<Budget*>(opaque)->used-=h->size;std::free(h);
    }
    JxlMemoryManager manager() {return {this,alloc,free};}
};
struct Utf {
    JNIEnv* env;jstring str;const char* text;
    Utf(JNIEnv* e,jstring s):env(e),str(s),text(e->GetStringUTFChars(s,nullptr)) {if(!text)throw std::bad_alloc();}
    ~Utf(){env->ReleaseStringUTFChars(str,text);}
};
struct Mapping {
    void* bytes=MAP_FAILED;size_t size=0;
    explicit Mapping(const char* path) {
        int fd=open(path,O_RDONLY);if(fd<0)throw std::runtime_error("Cannot read JPEG XL file.");
        struct stat st{};
        if(fstat(fd,&st)!=0 || st.st_size<2 || static_cast<uint64_t>(st.st_size)>SIZE_MAX) {close(fd);throw std::runtime_error("Invalid JPEG XL file size.");}
        size=static_cast<size_t>(st.st_size);bytes=mmap(nullptr,size,PROT_READ,MAP_PRIVATE,fd,0);close(fd);
        if(bytes==MAP_FAILED)throw std::bad_alloc();
    }
    ~Mapping(){if(bytes!=MAP_FAILED)munmap(bytes,size);}
};
struct Pixels {
    JNIEnv* env;jobject image;AndroidBitmapInfo info{};void* data=nullptr;
    Pixels(JNIEnv* e,jobject bitmap):env(e),image(bitmap) {
        if(AndroidBitmap_getInfo(env,image,&info)!=ANDROID_BITMAP_RESULT_SUCCESS || info.format!=ANDROID_BITMAP_FORMAT_RGBA_8888)
            throw std::runtime_error("JPEG XL needs an ARGB_8888 bitmap.");
        if(AndroidBitmap_lockPixels(env,image,&data)!=ANDROID_BITMAP_RESULT_SUCCESS)throw std::bad_alloc();
    }
    ~Pixels(){if(data)AndroidBitmap_unlockPixels(env,image);}
};
using Decoder=std::unique_ptr<JxlDecoder,decltype(&JxlDecoderDestroy)>;
using Encoder=std::unique_ptr<JxlEncoder,decltype(&JxlEncoderDestroy)>;
void require(bool condition,const char* message) {if(!condition)throw std::runtime_error(message);}
void fail(JNIEnv* env,bool memory,const char* message) {
    if(!env->ExceptionCheck())env->ThrowNew(env->FindClass(memory?"java/lang/OutOfMemoryError":"java/io/IOException"),message);
}
size_t limit(jlong requested,uint64_t outputBytes) {
    if(requested<0 || static_cast<uint64_t>(requested)<=outputBytes+1024*1024)throw std::bad_alloc();
    return static_cast<size_t>(std::min<uint64_t>(static_cast<uint64_t>(requested)-outputBytes,SIZE_MAX/2));
}
struct Output {
    Pixels* pixels;uint64_t width,height,left,top;
    std::unique_ptr<anpaint::colour::Transform> colour;
    bool failed=false;
};
struct Input {
    Pixels* pixels;Budget* budget;
    static void format(void*,JxlPixelFormat* out) {*out={3,JXL_TYPE_UINT8,JXL_NATIVE_ENDIAN,0};}
    static const void* read(void* opaque,size_t x,size_t y,size_t width,size_t height,size_t* stride) {
        auto& input=*static_cast<Input*>(opaque);auto& p=*input.pixels;
        // Check actual bitmap bounds, not the nominal 2048-pixel tile size.
        // Some libjxl paths request a larger rectangle; rejecting that valid
        // request made images such as 2057 x 17 fail before encoding.
        if(width==0 || height==0 || x>p.info.width || y>p.info.height || width>p.info.width-x || height>p.info.height-y)return nullptr;
        if(width>SIZE_MAX/3 || height>SIZE_MAX/(width*3)) {input.budget->exhausted=true;return nullptr;}
        *stride=width*3;
        auto* rgb=static_cast<uint8_t*>(Budget::alloc(input.budget,*stride*height));
        if(!rgb)return nullptr;
        for(size_t row=0;row<height;row++) {
            const auto* source=static_cast<const uint8_t*>(p.data)+(y+row)*p.info.stride+x*4;
            auto* target=rgb+row*(*stride);
            for(size_t col=0;col<width;col++) for(int channel=0;channel<3;channel++)target[col*3+channel]=source[col*4+channel];
        }
        return rgb;
    }
    static void release(void* opaque,const void* ptr) {Budget::free(static_cast<Input*>(opaque)->budget,const_cast<void*>(ptr));}
};
struct FileOutput {
    FILE* file;bool failed=false;uint64_t position=0;
    std::array<uint8_t,65536> buffer{};
    static void* get(void* opaque,size_t* size) {
        auto& out=*static_cast<FileOutput*>(opaque);
        *size=out.failed?0:out.buffer.size();
        return out.failed?nullptr:out.buffer.data();
    }
    static void release(void* opaque,size_t written) {
        auto& out=*static_cast<FileOutput*>(opaque);
        if(written>out.buffer.size() || out.position>INT64_MAX-written) {out.failed=true;return;}
        size_t done=0;
        while(!out.failed && done<written) {
            // pwrite64 is available on the minimum Android API; fseeko64 is not.
            const ssize_t count=pwrite64(fileno(out.file),out.buffer.data()+done,written-done,static_cast<off64_t>(out.position+done));
            if(count<0 && errno==EINTR)continue;
            if(count<=0) {out.failed=true;break;}
            done+=static_cast<size_t>(count);
        }
        out.position+=done;
    }
    static void seek(void* opaque,uint64_t position) {
        auto& out=*static_cast<FileOutput*>(opaque);
        if(position>INT64_MAX)out.failed=true;
        else out.position=position;
    }
    static void finalized(void*,uint64_t) {} // The seekable file already owns these bytes.
    JxlEncoderOutputProcessor processor() {return {this,get,release,seek,finalized};}
};
void outputBytePixels(void* opaque,size_t x,size_t y,size_t count,const void* data) {
    auto& o=*static_cast<Output*>(opaque);auto& p=*o.pixels;
    const auto* input=static_cast<const uint8_t*>(data);
    if(y<o.top || y>=o.top+o.height)return;
    const uint64_t begin=std::max<uint64_t>(x,o.left);
    const uint64_t end=std::min<uint64_t>(uint64_t(x)+count,o.left+o.width);
    if(begin>=end)return;
    const uint64_t left=((begin-o.left)*p.info.width+o.width-1)/o.width;
    const uint64_t right=std::min<uint64_t>(((end-o.left)*p.info.width+o.width-1)/o.width,p.info.width);
    const uint64_t top=((uint64_t(y)-o.top)*p.info.height+o.height-1)/o.height;
    const uint64_t bottom=std::min<uint64_t>(((uint64_t(y)+1-o.top)*p.info.height+o.height-1)/o.height,p.info.height);
    for(uint64_t dy=top;dy<bottom;dy++) for(uint64_t dx=left;dx<right;dx++) {
        const auto* src=input+4*(dx*o.width/p.info.width+o.left-x);
        auto* dest=static_cast<uint8_t*>(p.data)+dy*p.info.stride+dx*4;
        // Android's software bitmap stores premultiplied RGBA. The main editor
        // later composites this temporary import against its opaque background.
        dest[3]=src[3];for(int c=0;c<3;c++)dest[c]=static_cast<uint8_t>((src[c]*src[3]+127)/255);
    }
}
void outputPixels(void* opaque,size_t x,size_t y,size_t count,const void* data) {
    auto& out=*static_cast<Output*>(opaque);
    if(out.failed || y<out.top || y>=out.top+out.height)return;
    if(!out.colour) {outputBytePixels(opaque,x,y,count,data);return;}
    // Bounded streaming colour conversion, including reduced/cropped imports:
    // never allocate a full-resolution float RGBA image beside the bitmap.
    constexpr size_t chunk=256;
    std::array<float,4*chunk> floats;
    std::array<uint8_t,4*chunk> bytes;
    try {
        for(size_t offset=0;offset<count;offset+=chunk) {
            const size_t n=std::min(chunk,count-offset);
            if(x+offset+n<=out.left || x+offset>=out.left+out.width)continue;
            std::copy_n(static_cast<const float*>(data)+4*offset,4*n,floats.data());
            out.colour->convert(floats.data(),n);
            for(size_t p=0;p<4*n;p++)bytes[p]=anpaint::colour::byte(floats[p]);
            outputBytePixels(opaque,x+offset,y,n,bytes.data());
        }
    } catch(...) {out.failed=true;} // Never unwind through the codec callback.
}
skcms_ICCProfile profileForEncoding(const JxlColorEncoding& colour) {
    if(colour.color_space==JXL_COLOR_SPACE_GRAY)return *skcms_sRGB_profile();
    skcms_ICCProfile profile;skcms_Init(&profile);
    profile.data_color_space=skcms_Signature_RGB;
    require(skcms_PrimariesToXYZD50(
        colour.primaries_red_xy[0],colour.primaries_red_xy[1],
        colour.primaries_green_xy[0],colour.primaries_green_xy[1],
        colour.primaries_blue_xy[0],colour.primaries_blue_xy[1],
        colour.white_point_xy[0],colour.white_point_xy[1],&profile.toXYZD50),
        "Invalid JPEG XL HDR colour primaries.");
    profile.has_toXYZD50=true;
    skcms_SetTransferFunction(&profile,skcms_Identity_TransferFunction());
    return profile;
}
}

extern "C" JNIEXPORT jintArray JNICALL
Java_org_catrobat_paintroid_classic_JxlCodec_00024Native_info(JNIEnv* env,jobject,jstring path) {
    Budget budget{32*1024*1024};
    try {
        Utf name(env,path);Mapping file(name.text);auto manager=budget.manager();Decoder dec(JxlDecoderCreate(&manager),JxlDecoderDestroy);
        if(!dec)throw std::bad_alloc();
        require(JxlDecoderSubscribeEvents(dec.get(),JXL_DEC_BASIC_INFO)==JXL_DEC_SUCCESS,"Cannot inspect JPEG XL.");
        JxlDecoderSetInput(dec.get(),static_cast<const uint8_t*>(file.bytes),file.size);JxlDecoderCloseInput(dec.get());
        require(JxlDecoderProcessInput(dec.get())==JXL_DEC_BASIC_INFO,"Invalid JPEG XL header.");
        JxlBasicInfo info{};require(JxlDecoderGetBasicInfo(dec.get(),&info)==JXL_DEC_SUCCESS,"Invalid JPEG XL dimensions.");
        require(info.xsize>0 && info.ysize>0 && info.xsize<=INT_MAX && info.ysize<=INT_MAX,"JPEG XL dimensions exceed supported coordinates.");
        jint values[4]={static_cast<jint>(info.xsize),static_cast<jint>(info.ysize),
                       static_cast<jint>(info.bits_per_sample),static_cast<jint>(info.alpha_bits)};
        jintArray out=env->NewIntArray(4);if(out)env->SetIntArrayRegion(out,0,4,values);return out;
    } catch(const std::bad_alloc&) {fail(env,true,"Not enough memory to inspect JPEG XL.");}
      catch(const std::exception& e) {fail(env,budget.exhausted,e.what());}
    return nullptr;
}

extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_JxlCodec_00024Native_decode(JNIEnv* env,jobject,jstring path,jobject bitmap,jint left,jint top,jint right,jint bottom,jlong maxBytes) {
    Budget budget{0};
    try {
        Utf name(env,path);Mapping file(name.text);Pixels pixels(env,bitmap);budget.limit=limit(maxBytes,static_cast<uint64_t>(pixels.info.stride)*pixels.info.height);
        auto manager=budget.manager();Decoder dec(JxlDecoderCreate(&manager),JxlDecoderDestroy);if(!dec)throw std::bad_alloc();
        require(JxlDecoderSetCms(dec.get(),*JxlGetDefaultCms())==JXL_DEC_SUCCESS,"Cannot initialize JPEG XL colour management.");
        require(JxlDecoderSubscribeEvents(dec.get(),JXL_DEC_BASIC_INFO|JXL_DEC_COLOR_ENCODING|JXL_DEC_FULL_IMAGE)==JXL_DEC_SUCCESS,"Cannot start JPEG XL decoder.");
        require(JxlDecoderSetUnpremultiplyAlpha(dec.get(),JXL_TRUE)==JXL_DEC_SUCCESS,"Cannot prepare JPEG XL alpha conversion.");
        JxlDecoderSetInput(dec.get(),static_cast<const uint8_t*>(file.bytes),file.size);JxlDecoderCloseInput(dec.get());
        Output out{&pixels,0,0,0,0};JxlPixelFormat format{4,JXL_TYPE_UINT8,JXL_NATIVE_ENDIAN,0};
        float sourcePeak=1000.f;
        std::vector<uint8_t> sourceIcc; // Remains alive while skcms references it.
        for(;;) {
            const auto status=JxlDecoderProcessInput(dec.get());
            if(status==JXL_DEC_BASIC_INFO) {
                JxlBasicInfo info{};require(JxlDecoderGetBasicInfo(dec.get(),&info)==JXL_DEC_SUCCESS,"Invalid JPEG XL dimensions.");
                sourcePeak=info.intensity_target;
                require(info.xsize>0 && info.ysize>0 && info.xsize<=INT_MAX && info.ysize<=INT_MAX,"JPEG XL dimensions exceed supported coordinates.");
                if(right<0)right=info.xsize;if(bottom<0)bottom=info.ysize;
                require(left>=0 && top>=0 && right>left && bottom>top && uint32_t(right)<=info.xsize && uint32_t(bottom)<=info.ysize,"The JPEG XL crop must stay inside the image.");
                out.width=right-left;out.height=bottom-top;out.left=left;out.top=top;
            } else if(status==JXL_DEC_COLOR_ENCODING) {
                JxlColorEncoding original{};
                const bool structured=JxlDecoderGetColorAsEncodedProfile(dec.get(),JXL_COLOR_PROFILE_TARGET_ORIGINAL,&original)==JXL_DEC_SUCCESS;
                const bool hdr=structured && (original.transfer_function==JXL_TRANSFER_FUNCTION_PQ || original.transfer_function==JXL_TRANSFER_FUNCTION_HLG ||
                    (original.transfer_function==JXL_TRANSFER_FUNCTION_LINEAR && sourcePeak>255.f));
                if(hdr) {
                    // libjxl 0.12's built-in tone-mapping stage uses the
                    // destination transfer on non-XYB source pixels. Request
                    // the original encoding and convert float samples ourselves
                    // so both lossless and XYB inputs follow the same path.
                    require(JxlDecoderSetPreferredColorProfile(dec.get(),&original)==JXL_DEC_SUCCESS,"Cannot decode JPEG XL HDR source colours.");
                    out.colour=std::make_unique<anpaint::colour::Transform>(profileForEncoding(original),original.transfer_function,sourcePeak);
                } else if(!structured) {
                    size_t size=0;
                    require(JxlDecoderGetICCProfileSize(dec.get(),JXL_COLOR_PROFILE_TARGET_ORIGINAL,&size)==JXL_DEC_SUCCESS && size>0 && size<=anpaint::colour::kMaximumIccBytes,"Unsupported JPEG XL colour profile.");
                    if(size>budget.limit || budget.used.load()>budget.limit-size)throw std::bad_alloc();
                    budget.limit-=size;sourceIcc.resize(size);
                    require(JxlDecoderGetColorAsICCProfile(dec.get(),JXL_COLOR_PROFILE_TARGET_ORIGINAL,sourceIcc.data(),sourceIcc.size())==JXL_DEC_SUCCESS,"Cannot read JPEG XL colour profile.");
                    skcms_ICCProfile profile{};
                    const bool parsed=skcms_Parse(sourceIcc.data(),sourceIcc.size(),&profile);
                    if(parsed && profile.has_CICP && (profile.CICP.transfer_characteristics==16 || profile.CICP.transfer_characteristics==18 ||
                        (profile.CICP.transfer_characteristics==8 && sourcePeak>255.f))) {
                        require(JxlDecoderSetOutputColorProfile(dec.get(),nullptr,sourceIcc.data(),sourceIcc.size())==JXL_DEC_SUCCESS,"Cannot decode JPEG XL HDR ICC colours.");
                        out.colour=std::make_unique<anpaint::colour::Transform>(profile,profile.CICP.transfer_characteristics,sourcePeak);
                    }
                }
                if(out.colour)format.data_type=JXL_TYPE_FLOAT;
                else {
                    JxlColorEncoding color;JxlColorEncodingSetToSRGB(&color,JXL_FALSE);
                    require(JxlDecoderSetPreferredColorProfile(dec.get(),&color)==JXL_DEC_SUCCESS,"Cannot convert JPEG XL colours to sRGB.");
                }
            } else if(status==JXL_DEC_NEED_IMAGE_OUT_BUFFER) {
                require(out.width>0 && JxlDecoderSetImageOutCallback(dec.get(),&format,outputPixels,&out)==JXL_DEC_SUCCESS,"Cannot prepare JPEG XL output.");
            } else if(status==JXL_DEC_FULL_IMAGE) {
                require(!out.failed,"Cannot convert JPEG XL HDR pixels to sRGB.");
                return; // First composited frame of an animated input.
            }
            else throw std::runtime_error("JPEG XL decoding failed or the file is incomplete.");
        }
    } catch(const std::bad_alloc&) {fail(env,true,"Not enough memory to decode JPEG XL.");}
      catch(const std::exception& e) {fail(env,budget.exhausted,e.what());}
}

extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_JxlCodec_00024Native_encode(JNIEnv* env,jobject,jobject bitmap,jstring path,jint quality,jboolean lossless,jlong maxBytes) {
    Budget budget{0};
    try {
        Utf name(env,path);Pixels pixels(env,bitmap);budget.limit=limit(maxBytes,static_cast<uint64_t>(pixels.info.stride)*pixels.info.height);
        std::unique_ptr<FILE,decltype(&fclose)> file(fopen(name.text,"wb"),fclose);require(file!=nullptr,"Cannot write JPEG XL file.");
        // Keep the callbacks and file alive until the encoder is destroyed.
        FileOutput output{file.get()};Input input{&pixels,&budget};
        auto manager=budget.manager();Encoder enc(JxlEncoderCreate(&manager),JxlEncoderDestroy);if(!enc)throw std::bad_alloc();
        require(JxlEncoderSetOutputProcessor(enc.get(),output.processor())==JXL_ENC_SUCCESS,"Cannot prepare JPEG XL output.");
        JxlBasicInfo info;JxlEncoderInitBasicInfo(&info);info.xsize=pixels.info.width;info.ysize=pixels.info.height;info.bits_per_sample=8;info.num_color_channels=3;info.alpha_bits=0;info.uses_original_profile=lossless?JXL_TRUE:JXL_FALSE;
        require(JxlEncoderSetBasicInfo(enc.get(),&info)==JXL_ENC_SUCCESS,"Cannot set JPEG XL dimensions.");
        JxlColorEncoding color;JxlColorEncodingSetToSRGB(&color,JXL_FALSE);
        require(JxlEncoderSetColorEncoding(enc.get(),&color)==JXL_ENC_SUCCESS,"Cannot set JPEG XL colour profile.");
        auto* settings=JxlEncoderFrameSettingsCreate(enc.get(),nullptr);
        if(!settings)throw std::bad_alloc();
        require(JxlEncoderSetFrameLossless(settings,lossless?JXL_TRUE:JXL_FALSE)==JXL_ENC_SUCCESS,"Cannot set JPEG XL lossless mode.");
        require(JxlEncoderSetFrameDistance(settings,lossless?0.f:JxlEncoderDistanceFromQuality(quality))==JXL_ENC_SUCCESS,"Cannot set JPEG XL quality.");
        require(JxlEncoderFrameSettingsSetOption(settings,JXL_ENC_FRAME_SETTING_EFFORT,3)==JXL_ENC_SUCCESS,"Cannot set JPEG XL effort.");
        // Input AND output must use streaming callbacks. With ProcessOutput,
        // libjxl 0.12.0 CopyBuffers() requests the whole input rectangle and
        // creates another full RGB copy before encoding instead of using tiles.
        // RGB chunks omit the document's unused alpha channel.
        JxlChunkedFrameInputSource chunks{};
        chunks.opaque=&input;chunks.get_color_channels_pixel_format=Input::format;
        chunks.get_color_channel_data_at=Input::read;chunks.release_buffer=Input::release;
        const auto status=JxlEncoderAddChunkedFrame(settings,JXL_TRUE,chunks);
        require(!output.failed,"JPEG XL output could not be written.");
        require(status==JXL_ENC_SUCCESS,"Cannot encode JPEG XL pixels.");
        JxlEncoderCloseInput(enc.get());
        require(JxlEncoderFlushInput(enc.get())==JXL_ENC_SUCCESS,"JPEG XL encoding failed.");
        require(!output.failed,"JPEG XL output could not be written.");
        require(fflush(file.get())==0,"JPEG XL output could not be flushed.");
    } catch(const std::bad_alloc&) {fail(env,true,"Not enough memory to encode JPEG XL.");}
      catch(const std::exception& e) {fail(env,budget.exhausted,e.what());}
}
