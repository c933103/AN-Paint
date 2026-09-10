// AN Paint JNI integration, 2026-09-10. AGPL-3.0-or-later.
// JPEG XL library: JPEG XL Project Authors, BSD-3-Clause.
#include <jni.h>
#include <android/bitmap.h>
#include <jxl/decode.h>
#include <jxl/encode.h>
#include <jxl/color_encoding.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <algorithm>
#include <atomic>
#include <climits>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <stdexcept>
#include <string>

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
struct Output {Pixels* pixels;uint64_t width,height;};
void outputPixels(void* opaque,size_t x,size_t y,size_t count,const void* data) {
    auto& o=*static_cast<Output*>(opaque);auto& p=*o.pixels;
    const auto* input=static_cast<const uint8_t*>(data);
    const uint64_t left=(uint64_t(x)*p.info.width+o.width-1)/o.width;
    const uint64_t right=std::min<uint64_t>(((uint64_t(x)+count)*p.info.width+o.width-1)/o.width,p.info.width);
    const uint64_t top=(uint64_t(y)*p.info.height+o.height-1)/o.height;
    const uint64_t bottom=std::min<uint64_t>(((uint64_t(y)+1)*p.info.height+o.height-1)/o.height,p.info.height);
    for(uint64_t dy=top;dy<bottom;dy++) for(uint64_t dx=left;dx<right;dx++) {
        const auto* src=input+4*(dx*o.width/p.info.width-x);
        auto* dest=static_cast<uint8_t*>(p.data)+dy*p.info.stride+dx*4;
        // Android's software bitmap stores premultiplied RGBA. The main editor
        // later composites this temporary import against its opaque background.
        dest[3]=src[3];for(int c=0;c<3;c++)dest[c]=static_cast<uint8_t>((src[c]*src[3]+127)/255);
    }
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
        jint values[2]={static_cast<jint>(info.xsize),static_cast<jint>(info.ysize)};
        jintArray out=env->NewIntArray(2);if(out)env->SetIntArrayRegion(out,0,2,values);return out;
    } catch(const std::bad_alloc&) {fail(env,true,"Not enough memory to inspect JPEG XL.");}
      catch(const std::exception& e) {fail(env,budget.exhausted,e.what());}
    return nullptr;
}

extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_JxlCodec_00024Native_decode(JNIEnv* env,jobject,jstring path,jobject bitmap,jlong maxBytes) {
    Budget budget{0};
    try {
        Utf name(env,path);Mapping file(name.text);Pixels pixels(env,bitmap);budget.limit=limit(maxBytes,static_cast<uint64_t>(pixels.info.stride)*pixels.info.height);
        auto manager=budget.manager();Decoder dec(JxlDecoderCreate(&manager),JxlDecoderDestroy);if(!dec)throw std::bad_alloc();
        require(JxlDecoderSubscribeEvents(dec.get(),JXL_DEC_BASIC_INFO|JXL_DEC_COLOR_ENCODING|JXL_DEC_FULL_IMAGE)==JXL_DEC_SUCCESS,"Cannot start JPEG XL decoder.");
        JxlDecoderSetUnpremultiplyAlpha(dec.get(),JXL_TRUE);
        JxlDecoderSetInput(dec.get(),static_cast<const uint8_t*>(file.bytes),file.size);JxlDecoderCloseInput(dec.get());
        Output out{&pixels,0,0};JxlPixelFormat format{4,JXL_TYPE_UINT8,JXL_NATIVE_ENDIAN,0};
        for(;;) {
            const auto status=JxlDecoderProcessInput(dec.get());
            if(status==JXL_DEC_BASIC_INFO) {
                JxlBasicInfo info{};require(JxlDecoderGetBasicInfo(dec.get(),&info)==JXL_DEC_SUCCESS,"Invalid JPEG XL dimensions.");
                require(info.xsize>0 && info.ysize>0 && info.xsize<=INT_MAX && info.ysize<=INT_MAX,"JPEG XL dimensions exceed supported coordinates.");out.width=info.xsize;out.height=info.ysize;
            } else if(status==JXL_DEC_COLOR_ENCODING) {
                JxlColorEncoding color;JxlColorEncodingSetToSRGB(&color,JXL_FALSE);
                require(JxlDecoderSetPreferredColorProfile(dec.get(),&color)==JXL_DEC_SUCCESS,"Cannot convert JPEG XL colours to sRGB.");
            } else if(status==JXL_DEC_NEED_IMAGE_OUT_BUFFER) {
                require(out.width>0 && JxlDecoderSetImageOutCallback(dec.get(),&format,outputPixels,&out)==JXL_DEC_SUCCESS,"Cannot prepare JPEG XL output.");
            } else if(status==JXL_DEC_FULL_IMAGE) return; // First composited frame of an animated input.
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
        auto manager=budget.manager();Encoder enc(JxlEncoderCreate(&manager),JxlEncoderDestroy);if(!enc)throw std::bad_alloc();
        JxlBasicInfo info;JxlEncoderInitBasicInfo(&info);info.xsize=pixels.info.width;info.ysize=pixels.info.height;info.bits_per_sample=8;info.num_color_channels=3;info.alpha_bits=0;info.uses_original_profile=lossless?JXL_TRUE:JXL_FALSE;
        require(JxlEncoderSetBasicInfo(enc.get(),&info)==JXL_ENC_SUCCESS,"Cannot set JPEG XL dimensions.");
        JxlColorEncoding color;JxlColorEncodingSetToSRGB(&color,JXL_FALSE);
        require(JxlEncoderSetColorEncoding(enc.get(),&color)==JXL_ENC_SUCCESS,"Cannot set JPEG XL colour profile.");
        auto* settings=JxlEncoderFrameSettingsCreate(enc.get(),nullptr);
        require(JxlEncoderSetFrameLossless(settings,lossless?JXL_TRUE:JXL_FALSE)==JXL_ENC_SUCCESS,"Cannot set JPEG XL lossless mode.");
        require(JxlEncoderSetFrameDistance(settings,lossless?0.f:JxlEncoderDistanceFromQuality(quality))==JXL_ENC_SUCCESS,"Cannot set JPEG XL quality.");
        require(JxlEncoderFrameSettingsSetOption(settings,JXL_ENC_FRAME_SETTING_EFFORT,3)==JXL_ENC_SUCCESS,"Cannot set JPEG XL effort.");
        JxlPixelFormat format{4,JXL_TYPE_UINT8,JXL_NATIVE_ENDIAN,pixels.info.stride};
        require(JxlEncoderAddImageFrame(settings,&format,pixels.data,static_cast<size_t>(pixels.info.stride)*pixels.info.height)==JXL_ENC_SUCCESS,"Cannot encode JPEG XL pixels.");
        JxlEncoderCloseInput(enc.get());
        std::unique_ptr<FILE,decltype(&fclose)> file(fopen(name.text,"wb"),fclose);require(file!=nullptr,"Cannot write JPEG XL file.");
        uint8_t buffer[65536];
        for(;;) {
            uint8_t* next=buffer;size_t remaining=sizeof(buffer);
            auto status=JxlEncoderProcessOutput(enc.get(),&next,&remaining);size_t count=sizeof(buffer)-remaining;
            require(fwrite(buffer,1,count,file.get())==count,"JPEG XL output could not be written.");
            if(status==JXL_ENC_SUCCESS)break;
            require(status==JXL_ENC_NEED_MORE_OUTPUT,"JPEG XL encoding failed.");
        }
        require(fflush(file.get())==0,"JPEG XL output could not be flushed.");
    } catch(const std::bad_alloc&) {fail(env,true,"Not enough memory to encode JPEG XL.");}
      catch(const std::exception& e) {fail(env,budget.exhausted,e.what());}
}
