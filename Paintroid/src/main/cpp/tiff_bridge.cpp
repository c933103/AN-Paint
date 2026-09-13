// AN Paint TIFF integration, 2026. AGPL-3.0-or-later.
// The pinned libtiff/libjpeg-turbo sources retain their original licences.
// See TIFF_NOTICES.txt. This bridge does not implement a TIFF parser.
#include <jni.h>
#include <android/bitmap.h>
#include <tiffio.h>
#include <sys/stat.h>
#include <unistd.h>
#include <algorithm>
#include <array>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <new>
#include <stdexcept>
#include <string>
#include <vector>
#include "ColourConversion.h"
#include "TiffSrgbProfile.h"

namespace {
constexpr uint64_t kReserve = 32ULL * 1024 * 1024;
constexpr uint64_t kMaximumPixels = 1000000000ULL;
constexpr uint32_t kMaximumBlocks = 1000000;
constexpr uint32_t kMaximumPages = 4096; // Also set as libtiff's TIFF_MAX_DIR_COUNT.
struct Budget { size_t limit = 0, used = 0; bool exhausted = false; };
thread_local Budget* activeBudget = nullptr;
struct alignas(std::max_align_t) Allocation { size_t size; Budget* owner; };
struct BudgetScope {
    Budget* previous;
    explicit BudgetScope(Budget& budget) : previous(activeBudget) { activeBudget = &budget; }
    ~BudgetScope() { activeBudget = previous; }
};
void require(bool condition, const char* message) { if (!condition) throw std::runtime_error(message); }
void fail(JNIEnv* env, bool memory, const char* message) {
    if (!env->ExceptionCheck()) env->ThrowNew(env->FindClass(memory ? "java/lang/OutOfMemoryError" : "java/io/IOException"), message);
}
uint64_t multiply(uint64_t a, uint64_t b) {
    if (b && a > uint64_t(INT64_MAX) / b) throw std::bad_alloc();
    return a * b;
}
uint64_t add(uint64_t a, uint64_t b) {
    if (a > uint64_t(INT64_MAX) - b) throw std::bad_alloc();
    return a + b;
}
struct Utf {
    JNIEnv* env; jstring value; const char* text;
    Utf(JNIEnv* e, jstring v) : env(e), value(v), text(e->GetStringUTFChars(v, nullptr)) { if (!text) throw std::bad_alloc(); }
    ~Utf() { env->ReleaseStringUTFChars(value, text); }
};
struct Pixels {
    JNIEnv* env; jobject image; AndroidBitmapInfo info{}; void* data = nullptr;
    Pixels(JNIEnv* e, jobject bitmap) : env(e), image(bitmap) {
        require(AndroidBitmap_getInfo(env, image, &info) == ANDROID_BITMAP_RESULT_SUCCESS &&
                info.format == ANDROID_BITMAP_FORMAT_RGBA_8888, "TIFF needs an ARGB_8888 bitmap");
        require(info.width && info.height && info.width <= INT_MAX && info.height <= INT_MAX &&
                info.stride >= uint64_t(info.width) * 4, "Invalid TIFF bitmap dimensions or stride");
    }
    void lock() {
        if (AndroidBitmap_lockPixels(env, image, &data) != ANDROID_BITMAP_RESULT_SUCCESS) throw std::bad_alloc();
        require(data != nullptr, "Cannot access TIFF bitmap pixels");
    }
    ~Pixels() { if (data) AndroidBitmap_unlockPixels(env, image); }
};
struct Errors {
    bool failed = false;
    bool strictDirectoryWarnings = false;
    char message[512]{};
    static int error(TIFF*, void* opaque, const char*, const char* format, va_list args) {
        auto& state = *static_cast<Errors*>(opaque);
        if (!state.failed) vsnprintf(state.message, sizeof(state.message), format, args);
        state.failed = true;
        return 1;
    }
    static int warning(TIFF* tif, void* opaque, const char* module, const char* format, va_list args) {
        // libtiff deliberately truncates a cyclic directory chain with a
        // warning. A page selector must reject that damaged chain instead of
        // presenting the truncated count as the document's actual page count.
        auto& state = *static_cast<Errors*>(opaque);
        return state.strictDirectoryWarnings ? error(tif,opaque,module,format,args) : 1;
    }
    void check(bool ok, const char* fallback) const {
        if (!ok || failed) throw std::runtime_error(message[0] ? message : fallback);
    }
};
using Tiff = std::unique_ptr<TIFF, decltype(&TIFFClose)>;
using Options = std::unique_ptr<TIFFOpenOptions, decltype(&TIFFOpenOptionsFree)>;
Options options(Errors& errors, Budget& budget) {
    Options opts(TIFFOpenOptionsAlloc(), TIFFOpenOptionsFree);
    if (!opts) throw std::bad_alloc();
    const auto cap = static_cast<tmsize_t>(std::min<size_t>(budget.limit, PTRDIFF_MAX));
    TIFFOpenOptionsSetMaxSingleMemAlloc(opts.get(), cap);
    TIFFOpenOptionsSetMaxCumulatedMemAlloc(opts.get(), cap);
    TIFFOpenOptionsSetErrorHandlerExtR(opts.get(), Errors::error, &errors);
    TIFFOpenOptionsSetWarningHandlerExtR(opts.get(), Errors::warning, &errors);
    return opts;
}
Tiff input(const char* path, Errors& errors, Budget& budget) {
    auto opts = options(errors, budget);
    // 'm' disables mmap so an input cannot escape memory accounting. 'B'
    // explicitly requests MSB-first decoded packed samples; 16-bit values are
    // still automatically converted to host byte order by libtiff.
    Tiff tif(TIFFOpenExt(path, "rmB", opts.get()), TIFFClose);
    errors.check(tif != nullptr, "Cannot open TIFF image");
    return tif;
}
uint32_t pageCount(TIFF* tif, Errors& errors) {
    // libtiff walks only main-IFD offsets here, without decoding pages or
    // interpreting unrelated colour models. Its bounded offset maps detect
    // repeated offsets/cycles and the compiled 4096-directory limit.
    errors.strictDirectoryWarnings = true;
    const auto count = TIFFNumberOfDirectories(tif);
    errors.strictDirectoryWarnings = false;
    errors.check(count > 0, "Invalid TIFF page directory chain");
    require(count <= kMaximumPages, "TIFF contains more than 4096 pages");
    return count;
}
void selectPage(TIFF* tif, Errors& errors, jint pageIndex) {
    require(pageIndex >= 0 && uint32_t(pageIndex) < kMaximumPages, "TIFF page index is outside the supported range");
    const auto count = pageCount(tif, errors);
    require(uint32_t(pageIndex) < count, "TIFF page index is outside this document");
    if (pageIndex != 0) errors.check(TIFFSetDirectory(tif, uint32_t(pageIndex)) == 1, "Cannot read selected TIFF page");
}
struct Rect { int64_t left, top, right, bottom; };
struct Point { int64_t x, y; };
struct Info {
    uint32_t width = 0, height = 0, blockWidth = 0, blockHeight = 0, blocks = 0;
    uint16_t bits = 0, samples = 0, photo = 0, planar = 0, orientation = 1, compression = 0;
    uint16_t baseSamples = 0, planes = 1;
    bool tiled = false, associated = false, alpha = false, jpegRgb = false;
    uint64_t rowBytes = 0, blockBytes = 0, workingBytes = 0;
    const uint16_t *red = nullptr, *green = nullptr, *blue = nullptr;
    uint32_t iccSize = 0;
    const void* icc = nullptr;
    uint32_t displayWidth() const { return orientation >= 5 ? height : width; }
    uint32_t displayHeight() const { return orientation >= 5 ? width : height; }
    Point display(int64_t x, int64_t y) const {
        switch (orientation) {
            case 2: return {width-1-x,y};
            case 3: return {width-1-x,height-1-y};
            case 4: return {x,height-1-y};
            case 5: return {y,x};
            case 6: return {height-1-y,x};
            case 7: return {height-1-y,width-1-x};
            case 8: return {y,width-1-x};
            default: return {x,y};
        }
    }
    Point source(int64_t x, int64_t y) const {
        switch (orientation) {
            case 2: return {width-1-x,y};
            case 3: return {width-1-x,height-1-y};
            case 4: return {x,height-1-y};
            case 5: return {y,x};
            case 6: return {y,height-1-x};
            case 7: return {width-1-y,height-1-x};
            case 8: return {width-1-y,x};
            default: return {x,y};
        }
    }
    Rect mapped(Rect r, bool toDisplay) const {
        const auto a = toDisplay ? display(r.left,r.top) : source(r.left,r.top);
        const auto b = toDisplay ? display(r.right-1,r.bottom-1) : source(r.right-1,r.bottom-1);
        return {std::min(a.x,b.x),std::min(a.y,b.y),std::max(a.x,b.x)+1,std::max(a.y,b.y)+1};
    }
};
Info inspect(TIFF* tif, Errors& errors) {
    Info i;
    require(TIFFGetField(tif, TIFFTAG_IMAGEWIDTH, &i.width) && TIFFGetField(tif, TIFFTAG_IMAGELENGTH, &i.height) &&
            i.width && i.height && i.width <= INT_MAX && i.height <= INT_MAX,
            "Invalid TIFF image dimensions");
    require(uint64_t(i.width) * i.height <= kMaximumPixels, "TIFF exceeds the supported one-billion-pixel input limit");
    TIFFGetFieldDefaulted(tif, TIFFTAG_BITSPERSAMPLE, &i.bits);
    TIFFGetFieldDefaulted(tif, TIFFTAG_SAMPLESPERPIXEL, &i.samples);
    TIFFGetFieldDefaulted(tif, TIFFTAG_PLANARCONFIG, &i.planar);
    TIFFGetFieldDefaulted(tif, TIFFTAG_ORIENTATION, &i.orientation);
    TIFFGetFieldDefaulted(tif, TIFFTAG_COMPRESSION, &i.compression);
    uint16_t sampleFormat = SAMPLEFORMAT_UINT;
    TIFFGetFieldDefaulted(tif, TIFFTAG_SAMPLEFORMAT, &sampleFormat);
    require(sampleFormat == SAMPLEFORMAT_UINT, "TIFF floating-point, signed and logarithmic samples are not supported");
    require(i.orientation >= 1 && i.orientation <= 8, "Unsupported TIFF orientation");
    require(i.planar == PLANARCONFIG_CONTIG || i.planar == PLANARCONFIG_SEPARATE, "Unsupported TIFF planar configuration");
    require(TIFFGetField(tif, TIFFTAG_PHOTOMETRIC, &i.photo), "TIFF has no photometric interpretation");
    switch (i.compression) {
        case COMPRESSION_NONE: case COMPRESSION_CCITTRLE: case COMPRESSION_CCITTFAX3:
        case COMPRESSION_CCITTFAX4: case COMPRESSION_LZW: case COMPRESSION_JPEG:
        case COMPRESSION_DEFLATE: case COMPRESSION_ADOBE_DEFLATE: case COMPRESSION_PACKBITS: break;
        default: throw std::runtime_error("Unsupported TIFF compression (use None, LZW, Deflate, PackBits, CCITT or modern JPEG)");
    }
    require(TIFFIsCODECConfigured(i.compression), "This TIFF compression is unavailable");
    if (i.photo == PHOTOMETRIC_YCBCR) {
        require(i.compression == COMPRESSION_JPEG && i.bits == 8 && i.samples == 3 && i.planar == PLANARCONFIG_CONTIG,
                "TIFF YCbCr requires 8-bit contiguous JPEG compression");
        require(TIFFSetField(tif, TIFFTAG_JPEGCOLORMODE, JPEGCOLORMODE_RGB), "Cannot convert TIFF JPEG samples to RGB");
        i.jpegRgb = true;
    }
    const bool gray = i.photo == PHOTOMETRIC_MINISBLACK || i.photo == PHOTOMETRIC_MINISWHITE;
    const bool rgb = i.photo == PHOTOMETRIC_RGB || i.jpegRgb;
    const bool palette = i.photo == PHOTOMETRIC_PALETTE;
    require(gray || rgb || palette, "TIFF CMYK, Lab, logarithmic and other non-RGB colour models are not supported");
    require((rgb && (i.bits == 8 || i.bits == 16)) || (!rgb &&
            (i.bits == 1 || i.bits == 2 || i.bits == 4 || i.bits == 8 || i.bits == 16)), "Unsupported TIFF sample precision");
    require(i.compression != COMPRESSION_JPEG || i.bits == 8, "Only 8-bit JPEG-compressed TIFF is supported");
    if (i.compression == COMPRESSION_CCITTRLE || i.compression == COMPRESSION_CCITTFAX3 || i.compression == COMPRESSION_CCITTFAX4)
        require(gray && i.bits == 1 && i.samples == 1, "CCITT TIFF must contain bilevel grayscale samples");
    i.baseSamples = rgb ? 3 : 1;
    uint16_t extraCount = 0;
    uint16_t* extras = nullptr;
    TIFFGetFieldDefaulted(tif, TIFFTAG_EXTRASAMPLES, &extraCount, &extras);
    require(i.samples == i.baseSamples + extraCount && extraCount <= 1 && (!palette || !extraCount),
            "TIFF has unsupported or unspecified extra colour channels");
    if (extraCount) {
        require(extras && (extras[0] == EXTRASAMPLE_ASSOCALPHA || extras[0] == EXTRASAMPLE_UNASSALPHA),
                "TIFF extra sample must explicitly describe alpha coverage");
        i.alpha = true;
        i.associated = extras[0] == EXTRASAMPLE_ASSOCALPHA;
    }
    if (palette) require(TIFFGetField(tif, TIFFTAG_COLORMAP, &i.red, &i.green, &i.blue) && i.red && i.green && i.blue,
                         "TIFF palette is missing or malformed");
    if (TIFFGetField(tif, TIFFTAG_ICCPROFILE, &i.iccSize, &i.icc)) {
        const auto profile = anpaint::colour::Transform::parse(i.icc, i.iccSize);
        require(profile.data_color_space == (gray ? skcms_Signature_Gray : skcms_Signature_RGB),
                "TIFF ICC profile does not match its decoded colour samples");
    } else {
        uint16_t *a = nullptr, *b = nullptr, *c = nullptr;
        float* chromaticity = nullptr;
        require(!TIFFGetField(tif, TIFFTAG_TRANSFERFUNCTION, &a, &b, &c) &&
                !TIFFGetField(tif, TIFFTAG_WHITEPOINT, &chromaticity) &&
                !TIFFGetField(tif, TIFFTAG_PRIMARYCHROMATICITIES, &chromaticity),
                "TIFF colour calibration without an ICC profile is not supported; convert or embed its ICC profile first");
    }
    i.tiled = TIFFIsTiled(tif);
    if (i.tiled) {
        require(TIFFGetField(tif, TIFFTAG_TILEWIDTH, &i.blockWidth) && TIFFGetField(tif, TIFFTAG_TILELENGTH, &i.blockHeight),
                "TIFF tile dimensions are missing");
        i.rowBytes = TIFFTileRowSize64(tif);
        i.blockBytes = TIFFTileSize64(tif);
        i.blocks = TIFFNumberOfTiles(tif);
    } else {
        i.blockWidth = i.width;
        TIFFGetFieldDefaulted(tif, TIFFTAG_ROWSPERSTRIP, &i.blockHeight);
        i.blockHeight = std::min(i.height, i.blockHeight);
        i.rowBytes = TIFFScanlineSize64(tif);
        i.blockBytes = TIFFStripSize64(tif);
        i.blocks = TIFFNumberOfStrips(tif);
    }
    require(i.blockWidth && i.blockHeight && i.rowBytes && i.blockBytes && i.blocks && i.blocks <= kMaximumBlocks,
            "Invalid TIFF layout or more than one million strips/tiles");
    i.planes = i.planar == PLANARCONFIG_SEPARATE ? i.samples : 1;
    const uint64_t expectedRow = (multiply(multiply(i.blockWidth, i.planar == PLANARCONFIG_CONTIG ? i.samples : 1), i.bits) + 7) / 8;
    require(i.rowBytes == expectedRow && i.blockBytes >= multiply(i.rowBytes, i.blockHeight), "Unsupported TIFF decoded sample layout");
    struct stat st{};
    require(fstat(TIFFFileno(tif), &st) == 0 && st.st_size > 0, "Cannot inspect TIFF input length");
    uint64_t rawMaximum = 0;
    for (uint32_t block = 0; block < i.blocks; ++block) {
        int badOffset = 0, badCount = 0;
        const auto offset = TIFFGetStrileOffsetWithErr(tif, block, &badOffset);
        const auto count = TIFFGetStrileByteCountWithErr(tif, block, &badCount);
        require(!badOffset && !badCount && count && offset <= uint64_t(st.st_size) && count <= uint64_t(st.st_size) - offset,
                "TIFF strip/tile is missing or truncated");
        rawMaximum = std::max(rawMaximum, count);
    }
    // The estimator includes source blocks even for a small target. Runtime
    // accounting additionally caps every libtiff, zlib and libjpeg allocation.
    i.workingBytes = add(kReserve, add(multiply(i.blockBytes, i.planes),
        add(multiply(rawMaximum, 2), multiply(multiply(i.blockWidth,i.blockHeight), i.compression == COMPRESSION_JPEG ? 16 : 4))));
    errors.check(true, "Cannot read TIFF metadata");
    return i;
}
}

// libtiff, zlib's TIFF callbacks, and the pinned JPEG library all use this
// per-call allocator. The libraries run synchronously on the calling thread.
extern "C" void* AnPaintTiffMalloc(size_t size) {
    auto* owner = activeBudget;
    if (size > SIZE_MAX - sizeof(Allocation)) { if (owner) owner->exhausted = true; return nullptr; }
    const size_t total = size + sizeof(Allocation);
    if (owner && (total > owner->limit || owner->used > owner->limit - total)) { owner->exhausted = true; return nullptr; }
    auto* allocation = static_cast<Allocation*>(std::malloc(total));
    if (!allocation) { if (owner) owner->exhausted = true; return nullptr; }
    allocation->size = total; allocation->owner = owner;
    if (owner) owner->used += total;
    return allocation + 1;
}
extern "C" void AnPaintTiffFree(void* pointer) {
    if (!pointer) return;
    auto* allocation = static_cast<Allocation*>(pointer)-1;
    if (allocation->owner) allocation->owner->used -= allocation->size;
    std::free(allocation);
}
extern "C" void* AnPaintTiffCalloc(size_t count, size_t size) {
    if (size && count > SIZE_MAX / size) { if (activeBudget) activeBudget->exhausted = true; return nullptr; }
    void* pointer = AnPaintTiffMalloc(count*size);
    if (pointer) std::memset(pointer,0,count*size);
    return pointer;
}
extern "C" void* AnPaintTiffRealloc(void* pointer, size_t size) {
    if (!pointer) return AnPaintTiffMalloc(size);
    if (!size) { AnPaintTiffFree(pointer); return nullptr; }
    const auto* allocation = static_cast<Allocation*>(pointer)-1;
    void* replacement = AnPaintTiffMalloc(size);
    if (replacement) {
        std::memcpy(replacement,pointer,std::min(size,allocation->size-sizeof(Allocation)));
        AnPaintTiffFree(pointer);
    }
    return replacement;
}

namespace {
struct Buffer {
    uint8_t* data = nullptr;
    explicit Buffer(uint64_t size) {
        if (size > SIZE_MAX) throw std::bad_alloc();
        data = static_cast<uint8_t*>(AnPaintTiffMalloc(static_cast<size_t>(size)));
        if (!data) throw std::bad_alloc();
    }
    ~Buffer() { AnPaintTiffFree(data); }
};
uint16_t sample(const Info& i, const uint8_t* block, uint32_t x, uint32_t y, uint16_t channel) {
    const uint64_t plane = i.planes == 1 ? 0 : channel;
    const uint64_t index = i.planes == 1 ? uint64_t(x)*i.samples+channel : x;
    const auto* row = block + plane*i.blockBytes + uint64_t(y)*i.rowBytes;
    if (i.bits == 16) { uint16_t value; std::memcpy(&value,row+index*2,2); return value; }
    if (i.bits == 8) return row[index];
    const auto bit = index*i.bits;
    return (row[bit/8] >> (8-i.bits-bit%8)) & ((1U<<i.bits)-1);
}
void color(const Info& i, const uint8_t* block, uint32_t x, uint32_t y, float* rgba) {
    const float maximum = float((1U<<i.bits)-1);
    if (i.photo == PHOTOMETRIC_PALETTE) {
        const auto index = sample(i,block,x,y,0);
        rgba[0]=i.red[index]/65535.0f; rgba[1]=i.green[index]/65535.0f; rgba[2]=i.blue[index]/65535.0f;
    } else if (i.baseSamples == 3) {
        for (int c=0;c<3;++c) rgba[c]=sample(i,block,x,y,c)/maximum;
    } else {
        float gray = sample(i,block,x,y,0)/maximum;
        if (i.photo == PHOTOMETRIC_MINISWHITE) gray=1-gray;
        rgba[0]=rgba[1]=rgba[2]=gray;
    }
    rgba[3]=i.alpha ? sample(i,block,x,y,i.baseSamples)/maximum : 1.0f;
    if (i.associated) for (int c=0;c<3;++c) rgba[c]=rgba[3]>0 ? rgba[c]/rgba[3] : 0;
}
int64_t ceilingRatio(int64_t a, int64_t b, int64_t c) { return (a*b+c-1)/c; }
void render(const Info& i, const uint8_t* block, uint32_t originX, uint32_t originY,
            Rect crop, Pixels& target, const anpaint::colour::Transform* transform) {
    const Rect source{originX,originY,static_cast<int64_t>(std::min<uint64_t>(uint64_t(originX)+i.blockWidth,i.width)),
                                   static_cast<int64_t>(std::min<uint64_t>(uint64_t(originY)+i.blockHeight,i.height))};
    const auto displayed=i.mapped(source,true);
    const auto left=std::max(displayed.left,crop.left), top=std::max(displayed.top,crop.top);
    const auto right=std::min(displayed.right,crop.right), bottom=std::min(displayed.bottom,crop.bottom);
    if (left>=right || top>=bottom) return;
    const auto cropWidth=crop.right-crop.left, cropHeight=crop.bottom-crop.top;
    const auto x0=ceilingRatio(left-crop.left,target.info.width,cropWidth);
    const auto x1=ceilingRatio(right-crop.left,target.info.width,cropWidth);
    const auto y0=ceilingRatio(top-crop.top,target.info.height,cropHeight);
    const auto y1=ceilingRatio(bottom-crop.top,target.info.height,cropHeight);
    std::array<float,256*4> colors{};
    for (int64_t y=y0;y<y1;++y) for (int64_t x=x0;x<x1;) {
        const auto count=static_cast<size_t>(std::min<int64_t>(256,x1-x));
        for (size_t c=0;c<count;++c) {
            const auto p=i.source(crop.left+(x+c)*cropWidth/target.info.width,
                                  crop.top+y*cropHeight/target.info.height);
            require(p.x>=source.left && p.x<source.right && p.y>=source.top && p.y<source.bottom,
                    "TIFF crop mapping exceeds its source block");
            color(i,block,uint32_t(p.x-originX),uint32_t(p.y-originY),colors.data()+c*4);
        }
        if (transform) transform->convert(colors.data(),count);
        for (size_t c=0;c<count;++c) {
            const auto* rgba=colors.data()+c*4;
            auto* pixel=static_cast<uint8_t*>(target.data)+uint64_t(y)*target.info.stride+(x+c)*4;
            pixel[3]=anpaint::colour::byte(rgba[3]);
            for (int channel=0;channel<3;++channel) pixel[channel]=anpaint::colour::byte(rgba[channel]*rgba[3]);
        }
        x+=count;
    }
}
struct Output {
    std::string temporary;
    Tiff tif{nullptr,TIFFClose};
    Output(const char* destination, Errors& errors, Budget& budget) {
        std::string pattern=std::string(destination)+".XXXXXX";
        std::vector<char> name(pattern.begin(),pattern.end()); name.push_back('\0');
        const int fd=mkstemp(name.data());
        require(fd>=0,"Cannot create TIFF output file");
        try {
            temporary=name.data();
            auto opts=options(errors,budget);
            tif.reset(TIFFFdOpenExt(fd,name.data(),"wl",opts.get()));
            errors.check(tif!=nullptr,"Cannot open TIFF output file");
        } catch (...) {
            if (!tif) close(fd);
            tif.reset(); unlink(name.data()); temporary.clear();
            throw;
        }
    }
    ~Output() { tif.reset(); if (!temporary.empty()) unlink(temporary.c_str()); }
    void commit(const char* destination, Errors& errors) {
        errors.check(TIFFWriteDirectory(tif.get())==1,"Cannot write TIFF image directory");
        errors.check(TIFFFlush(tif.get())==1,"Cannot finish TIFF output");
        tif.reset();
        errors.check(true,"Cannot close TIFF output");
        require(rename(temporary.c_str(),destination)==0,"Cannot replace TIFF output file");
        temporary.clear();
    }
};
}

extern "C" JNIEXPORT jlongArray JNICALL
Java_org_catrobat_paintroid_classic_TiffCodec_00024Native_info(JNIEnv* env,jobject,jstring path,jint pageIndex) {
    Budget budget{static_cast<size_t>(kReserve)};
    try {
        BudgetScope scope(budget); Utf name(env,path); Errors errors;
        auto tif=input(name.text,errors,budget); selectPage(tif.get(),errors,pageIndex);
        const auto i=inspect(tif.get(),errors);
        const jlong values[]={i.displayWidth(),i.displayHeight(),static_cast<jlong>(i.workingBytes)};
        auto result=env->NewLongArray(3);
        if (result) env->SetLongArrayRegion(result,0,3,values);
        return result;
    } catch (const std::bad_alloc&) { fail(env,true,"Not enough memory to inspect TIFF"); }
      catch (const std::exception& error) { fail(env,budget.exhausted,error.what()); }
    return nullptr;
}

extern "C" JNIEXPORT jint JNICALL
Java_org_catrobat_paintroid_classic_TiffCodec_00024Native_pageCount(JNIEnv* env,jobject,jstring path) {
    Budget budget{static_cast<size_t>(kReserve)};
    try {
        BudgetScope scope(budget); Utf name(env,path); Errors errors;
        auto tif=input(name.text,errors,budget);
        return static_cast<jint>(pageCount(tif.get(),errors));
    } catch (const std::bad_alloc&) { fail(env,true,"Not enough memory to inspect TIFF pages"); }
      catch (const std::exception& error) { fail(env,budget.exhausted,error.what()); }
    return 0;
}

extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_TiffCodec_00024Native_decode(
        JNIEnv* env,jobject,jstring path,jobject bitmap,jint left,jint top,jint right,jint bottom,jlong maxBytes,jint pageIndex) {
    Budget budget;
    try {
        Utf name(env,path); Pixels target(env,bitmap);
        const auto outputBytes=multiply(target.info.stride,target.info.height);
        if (maxBytes<=0 || uint64_t(maxBytes)<add(outputBytes,kReserve)) throw std::bad_alloc();
        budget.limit=static_cast<size_t>(std::min<uint64_t>(uint64_t(maxBytes)-outputBytes-1024*1024,SIZE_MAX/2));
        BudgetScope scope(budget); Errors errors;
        auto tif=input(name.text,errors,budget); selectPage(tif.get(),errors,pageIndex);
        const auto i=inspect(tif.get(),errors);
        if (add(i.workingBytes,outputBytes)>uint64_t(maxBytes)) throw std::bad_alloc();
        Rect crop{left,top,right<0 ? i.displayWidth() : right,bottom<0 ? i.displayHeight() : bottom};
        require(crop.left>=0 && crop.top>=0 && crop.left<crop.right && crop.top<crop.bottom &&
                crop.right<=i.displayWidth() && crop.bottom<=i.displayHeight(),"TIFF crop must stay inside the image");
        std::unique_ptr<anpaint::colour::Transform> transform;
        if (i.icc) transform=std::make_unique<anpaint::colour::Transform>(anpaint::colour::Transform::parse(i.icc,i.iccSize));
        Buffer block(multiply(i.blockBytes,i.planes));
        target.lock();
        const auto bounds=i.mapped(crop,false);
        const auto startX=uint32_t(bounds.left)/i.blockWidth*i.blockWidth;
        const auto startY=uint32_t(bounds.top)/i.blockHeight*i.blockHeight;
        for (uint64_t y=startY;y<uint64_t(bounds.bottom);y+=i.blockHeight)
            for (uint64_t x=startX;x<uint64_t(bounds.right);x+=i.blockWidth) {
                const auto expected=i.tiled ? i.blockBytes : i.rowBytes*std::min<uint64_t>(i.blockHeight,i.height-y);
                require(expected<=PTRDIFF_MAX,"TIFF decoded strip/tile exceeds addressable memory");
                for (uint16_t plane=0;plane<i.planes;++plane) {
                    const uint32_t index=i.tiled ? TIFFComputeTile(tif.get(),uint32_t(x),uint32_t(y),0,plane)
                                                 : TIFFComputeStrip(tif.get(),uint32_t(y),plane);
                    const auto count=i.tiled ? TIFFReadEncodedTile(tif.get(),index,block.data+plane*i.blockBytes,tmsize_t(expected))
                                             : TIFFReadEncodedStrip(tif.get(),index,block.data+plane*i.blockBytes,tmsize_t(expected));
                    errors.check(count>=0 && uint64_t(count)==expected,"Cannot decode complete TIFF strip/tile");
                }
                render(i,block.data,uint32_t(x),uint32_t(y),crop,target,transform.get());
            }
    } catch (const std::bad_alloc&) { fail(env,true,"Not enough memory to decode TIFF"); }
      catch (const std::exception& error) { fail(env,budget.exhausted,error.what()); }
}

extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_TiffCodec_00024Native_encode(
        JNIEnv* env,jobject,jobject bitmap,jstring path,jboolean compressed,jlong maxBytes) {
    Budget budget;
    try {
        Utf name(env,path); Pixels source(env,bitmap);
        const auto sourceBytes=multiply(source.info.stride,source.info.height);
        const auto rowBytes=multiply(source.info.width,3);
        // Keep classic TIFF's offsets below 4 GiB, including worst-case Deflate
        // growth, per-strip tables and profile/directory overhead.
        const auto payload=multiply(rowBytes,source.info.height);
        require(payload<0xF0000000ULL,"TIFF export exceeds the classic TIFF size limit");
        const auto minimum=add(sourceBytes,add(kReserve,multiply(rowBytes,4)));
        if (maxBytes<=0 || uint64_t(maxBytes)<minimum) throw std::bad_alloc();
        budget.limit=static_cast<size_t>(std::min<uint64_t>(uint64_t(maxBytes)-sourceBytes-1024*1024,SIZE_MAX/2));
        BudgetScope scope(budget); Errors errors;
        Output output(name.text,errors,budget); auto* tif=output.tif.get();
        const uint32_t rows=static_cast<uint32_t>(std::max<uint64_t>(1,std::min<uint64_t>(source.info.height,65536/rowBytes)));
        require((uint64_t(source.info.height)+rows-1)/rows<=kMaximumBlocks,"TIFF export needs too many strips");
        require(TIFFSetField(tif,TIFFTAG_IMAGEWIDTH,source.info.width) && TIFFSetField(tif,TIFFTAG_IMAGELENGTH,source.info.height) &&
                TIFFSetField(tif,TIFFTAG_SAMPLESPERPIXEL,3) && TIFFSetField(tif,TIFFTAG_BITSPERSAMPLE,8) &&
                TIFFSetField(tif,TIFFTAG_SAMPLEFORMAT,SAMPLEFORMAT_UINT) && TIFFSetField(tif,TIFFTAG_PHOTOMETRIC,PHOTOMETRIC_RGB) &&
                TIFFSetField(tif,TIFFTAG_PLANARCONFIG,PLANARCONFIG_CONTIG) && TIFFSetField(tif,TIFFTAG_ORIENTATION,ORIENTATION_TOPLEFT) &&
                TIFFSetField(tif,TIFFTAG_ROWSPERSTRIP,rows) &&
                TIFFSetField(tif,TIFFTAG_COMPRESSION,compressed ? COMPRESSION_ADOBE_DEFLATE : COMPRESSION_NONE) &&
                TIFFSetField(tif,TIFFTAG_ICCPROFILE,static_cast<uint32_t>(sizeof(kTiffSrgbProfile)),kTiffSrgbProfile) &&
                TIFFSetField(tif,TIFFTAG_SOFTWARE,"AN Paint"),"Cannot configure TIFF export");
        if (compressed) require(TIFFSetField(tif,TIFFTAG_PREDICTOR,PREDICTOR_HORIZONTAL) &&
                                TIFFSetField(tif,TIFFTAG_ZIPQUALITY,6),"Cannot configure lossless TIFF compression");
        Buffer row(rowBytes); source.lock();
        for (uint32_t y=0;y<source.info.height;++y) {
            const auto* pixels=static_cast<const uint8_t*>(source.data)+uint64_t(y)*source.info.stride;
            for (uint32_t x=0;x<source.info.width;++x) {
                require(pixels[uint64_t(x)*4+3]==255,"TIFF export requires an opaque document");
                std::memcpy(row.data+uint64_t(x)*3,pixels+uint64_t(x)*4,3);
            }
            errors.check(TIFFWriteScanline(tif,row.data,y,0)==1,"Cannot encode TIFF scanline");
        }
        output.commit(name.text,errors);
    } catch (const std::bad_alloc&) { fail(env,true,"Not enough memory to encode TIFF"); }
      catch (const std::exception& error) { fail(env,budget.exhausted,error.what()); }
}
