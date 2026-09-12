// AN Paint JNI integration, 2026-09-12. AGPL-3.0-or-later.
// libwebp: Google and contributors, BSD-3-Clause.
#include <jni.h>
#include <android/bitmap.h>
#include <webp/encode.h>
#include <unistd.h>
#include <algorithm>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <new>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
struct Budget {
    size_t limit = 0, used = 0;
    bool exhausted = false;
};
thread_local Budget* activeBudget = nullptr;
struct alignas(std::max_align_t) Allocation {
    size_t size;
    Budget* owner;
};
struct BudgetScope {
    Budget* previous;
    explicit BudgetScope(Budget& budget) : previous(activeBudget) { activeBudget = &budget; }
    ~BudgetScope() { activeBudget = previous; }
};
void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}
void fail(JNIEnv* env, bool memory, const char* message) {
    if (!env->ExceptionCheck())
        env->ThrowNew(env->FindClass(memory ? "java/lang/OutOfMemoryError" : "java/io/IOException"), message);
}
struct Utf {
    JNIEnv* env;
    jstring string;
    const char* text;
    Utf(JNIEnv* e, jstring s) : env(e), string(s), text(e->GetStringUTFChars(s, nullptr)) {
        if (!text) throw std::bad_alloc();
    }
    ~Utf() { env->ReleaseStringUTFChars(string, text); }
};
struct Pixels {
    JNIEnv* env;
    jobject image;
    AndroidBitmapInfo info{};
    void* data = nullptr;
    Pixels(JNIEnv* e, jobject bitmap) : env(e), image(bitmap) {
        require(AndroidBitmap_getInfo(env, image, &info) == ANDROID_BITMAP_RESULT_SUCCESS &&
                info.format == ANDROID_BITMAP_FORMAT_RGBA_8888, "WebP needs an ARGB_8888 bitmap.");
        require(info.width > 0 && info.height > 0 && info.width <= WEBP_MAX_DIMENSION &&
                info.height <= WEBP_MAX_DIMENSION, "WebP supports dimensions up to 16383 pixels per side.");
        require(info.stride >= uint64_t(info.width) * 4 && info.stride <= INT_MAX,
                "Invalid WebP bitmap row stride.");
    }
    void lock() {
        if (AndroidBitmap_lockPixels(env, image, &data) != ANDROID_BITMAP_RESULT_SUCCESS)
            throw std::bad_alloc();
        require(data != nullptr, "Cannot read WebP source pixels.");
    }
    ~Pixels() { if (data) AndroidBitmap_unlockPixels(env, image); }
};
struct Picture {
    WebPPicture value{};
    Picture() { require(WebPPictureInit(&value), "Cannot initialise WebP encoder."); }
    ~Picture() { WebPPictureFree(&value); }
};
struct Output {
    FILE* file = nullptr;
    std::string temporary;
    bool failed = false;
    explicit Output(const char* destination) {
        std::string pattern = std::string(destination) + ".XXXXXX";
        std::vector<char> name(pattern.begin(), pattern.end());
        name.push_back('\0');
        const int fd = mkstemp(name.data());
        require(fd >= 0, "Cannot create WebP output file.");
        file = fdopen(fd, "wb");
        if (!file) { close(fd); unlink(name.data()); throw std::runtime_error("Cannot write WebP output file."); }
        temporary = name.data();
    }
    ~Output() {
        if (file) fclose(file);
        if (!temporary.empty()) unlink(temporary.c_str());
    }
    static int write(const uint8_t* data, size_t size, const WebPPicture* picture) {
        auto& output = *static_cast<Output*>(picture->custom_ptr);
        if (output.failed || fwrite(data, 1, size, output.file) != size) {
            output.failed = true;
            return 0;
        }
        return 1;
    }
    void commit(const char* destination) {
        require(!failed && fflush(file) == 0, "Cannot finish writing WebP output.");
        const int result = fclose(file);
        file = nullptr;
        require(result == 0, "Cannot close WebP output.");
        require(rename(temporary.c_str(), destination) == 0, "Cannot replace WebP output.");
        temporary.clear();
    }
};
}

// CMake redirects allocations in the pinned static codec to these functions.
// The bridge itself uses libc normally. WEBP_USE_THREAD=OFF ensures allocation
// and release happen under the calling encode's thread-local budget.
extern "C" void* AnPaintWebpMalloc(size_t size) {
    Budget* owner = activeBudget;
    if (size > SIZE_MAX - sizeof(Allocation)) {
        if (owner) owner->exhausted = true;
        return nullptr;
    }
    const size_t total = size + sizeof(Allocation);
    if (owner && (total > owner->limit || owner->used > owner->limit - total)) {
        owner->exhausted = true;
        return nullptr;
    }
    auto* allocation = static_cast<Allocation*>(std::malloc(total));
    if (!allocation) {
        if (owner) owner->exhausted = true;
        return nullptr;
    }
    allocation->size = total;
    allocation->owner = owner;
    if (owner) owner->used += total;
    return allocation + 1;
}
extern "C" void AnPaintWebpFree(void* pointer) {
    if (!pointer) return;
    auto* allocation = static_cast<Allocation*>(pointer) - 1;
    if (allocation->owner) allocation->owner->used -= allocation->size;
    std::free(allocation);
}
extern "C" void* AnPaintWebpCalloc(size_t count, size_t size) {
    if (size && count > SIZE_MAX / size) {
        if (activeBudget) activeBudget->exhausted = true;
        return nullptr;
    }
    void* pointer = AnPaintWebpMalloc(count * size);
    if (pointer) std::memset(pointer, 0, count * size);
    return pointer;
}
extern "C" void* AnPaintWebpRealloc(void* pointer, size_t size) {
    if (!pointer) return AnPaintWebpMalloc(size);
    if (!size) { AnPaintWebpFree(pointer); return nullptr; }
    auto* allocation = static_cast<Allocation*>(pointer) - 1;
    // Allocate before releasing the old block: the transient peak is charged.
    void* replacement = AnPaintWebpMalloc(size);
    if (replacement) {
        std::memcpy(replacement, pointer, std::min(size, allocation->size - sizeof(Allocation)));
        AnPaintWebpFree(pointer);
    }
    return replacement;
}

extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_WebpCodec_00024Native_encode(
        JNIEnv* env, jobject, jobject bitmap, jstring path, jint quality, jboolean lossless, jlong maxBytes) {
    Budget budget;
    try {
        Utf name(env, path);
        Pixels pixels(env, bitmap);
        const uint64_t sourceBytes = uint64_t(pixels.info.stride) * pixels.info.height;
        const uint64_t count = uint64_t(pixels.info.width) * pixels.info.height;
        // Reserve bridge/file bookkeeping; codec allocations are additionally
        // capped at runtime. This estimate rejects infeasible exports early.
        const uint64_t reserve = 1024 * 1024;
        const uint64_t minimum = sourceBytes + reserve + count * (lossless ? 24 : 12);
        if (maxBytes <= 0 || uint64_t(maxBytes) < minimum) throw std::bad_alloc();
        budget.limit = static_cast<size_t>(std::min<uint64_t>(uint64_t(maxBytes) - sourceBytes - reserve, SIZE_MAX / 2));
        BudgetScope scope(budget);
        pixels.lock();
        // AN Paint documents are opaque. Refuse accidental transparent inputs
        // instead of saving premultiplied dark colours or an alpha channel.
        for (uint32_t y = 0; y < pixels.info.height; ++y) {
            const auto* row = static_cast<const uint8_t*>(pixels.data) + size_t(y) * pixels.info.stride;
            for (uint32_t x = 0; x < pixels.info.width; ++x)
                require(row[size_t(x) * 4 + 3] == 255, "WebP export requires an opaque document.");
        }
        WebPConfig config{};
        require(WebPConfigInit(&config), "Cannot initialise WebP settings.");
        config.lossless = lossless ? 1 : 0;
        config.quality = lossless ? 75.0f : float(std::max(1, std::min(100, int(quality))));
        config.method = 4;
        config.near_lossless = 100;
        config.exact = 1;
        config.thread_level = 0;
        config.low_memory = 1;
        require(WebPValidateConfig(&config), "Invalid WebP encoder settings.");
        Picture picture;
        picture.value.width = static_cast<int>(pixels.info.width);
        picture.value.height = static_cast<int>(pixels.info.height);
        picture.value.use_argb = lossless ? 1 : 0;
        if (!WebPPictureImportRGBX(&picture.value, static_cast<const uint8_t*>(pixels.data), int(pixels.info.stride)))
            throw std::bad_alloc();
        Output output(name.text);
        picture.value.writer = Output::write;
        picture.value.custom_ptr = &output;
        if (!WebPEncode(&config, &picture.value)) {
            if (budget.exhausted || picture.value.error_code == VP8_ENC_ERROR_OUT_OF_MEMORY ||
                    picture.value.error_code == VP8_ENC_ERROR_BITSTREAM_OUT_OF_MEMORY) throw std::bad_alloc();
            throw std::runtime_error(output.failed ? "Cannot write WebP image." : "Cannot encode WebP image.");
        }
        output.commit(name.text);
    } catch (const std::bad_alloc&) {
        fail(env, true, "Not enough memory to encode WebP.");
    } catch (const std::exception& error) {
        fail(env, budget.exhausted, error.what());
    }
}
