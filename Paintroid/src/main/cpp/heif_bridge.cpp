// AN Paint, 2026. AGPL-3.0-or-later. Codec notices: HEIF_AVIF_NOTICES.txt.
#include <jni.h>
#include <android/bitmap.h>
#include <libheif/heif.h>
#include <algorithm>
#include <climits>
#include <cstdint>
#include <cstring>
#include <memory>
#include <mutex>
#include <stdexcept>
#include <string>
#include <vector>
#include <array>
#include "ColourConversion.h"

namespace {
constexpr uint64_t kReserve = 32ULL * 1024 * 1024;
constexpr uint32_t kEncodeTile = 1024;
// The libraries have global codec setup; serialization also makes the working
// memory estimate independent of two callers importing/exporting at once.
std::mutex codecMutex;
struct Utf {
    JNIEnv* env; jstring value; const char* text;
    Utf(JNIEnv* e, jstring v) : env(e), value(v), text(e->GetStringUTFChars(v, nullptr)) { if (!text) throw std::bad_alloc(); }
    ~Utf() { env->ReleaseStringUTFChars(value, text); }
};
struct Pixels {
    JNIEnv* env; jobject bitmap; AndroidBitmapInfo info{}; void* data = nullptr;
    Pixels(JNIEnv* e, jobject b, bool allowWide = false) : env(e), bitmap(b) {
        if (AndroidBitmap_getInfo(env, bitmap, &info) != ANDROID_BITMAP_RESULT_SUCCESS || (info.format != ANDROID_BITMAP_FORMAT_RGBA_8888 && !(allowWide && info.format == ANDROID_BITMAP_FORMAT_RGBA_F16)))
            throw std::runtime_error("HEIC/AVIF requires an ARGB_8888 bitmap");
        if (AndroidBitmap_lockPixels(env, bitmap, &data) != ANDROID_BITMAP_RESULT_SUCCESS) throw std::bad_alloc();
    }
    ~Pixels() { if (data) AndroidBitmap_unlockPixels(env, bitmap); }
};
using Context = std::unique_ptr<heif_context, decltype(&heif_context_free)>;
using Handle = std::unique_ptr<heif_image_handle, decltype(&heif_image_handle_release)>;
using Image = std::unique_ptr<heif_image, decltype(&heif_image_release)>;
using Encoder = std::unique_ptr<heif_encoder, decltype(&heif_encoder_release)>;
using DecodeOptions = std::unique_ptr<heif_decoding_options, decltype(&heif_decoding_options_free)>;
using EncodeOptions = std::unique_ptr<heif_encoding_options, decltype(&heif_encoding_options_free)>;
using Profile = std::unique_ptr<heif_color_profile_nclx, decltype(&heif_nclx_color_profile_free)>;
void check(heif_error e) {
    if (e.code == heif_error_Memory_allocation_error) throw std::bad_alloc();
    if (e.code != heif_error_Ok) throw std::runtime_error(e.message ? e.message : "HEIC/AVIF codec error");
}
void require(bool condition, const char* message) { if (!condition) throw std::runtime_error(message); }
void fail(JNIEnv* env, bool memory, const char* message) {
    if (!env->ExceptionCheck()) env->ThrowNew(env->FindClass(memory ? "java/lang/OutOfMemoryError" : "java/io/IOException"), message);
}
Context context(uint64_t budget) {
    Context result(heif_context_alloc(), heif_context_free);
    if (!result) throw std::bad_alloc();
    auto* limits = heif_context_get_security_limits(result.get());
    limits->max_total_memory = budget;
    limits->max_memory_block_size = budget;
    // Metadata inspection must be able to describe an oversized image before
    // asking the user what to do. Pixel allocation is checked separately below.
    limits->max_image_size_pixels = static_cast<uint64_t>(INT_MAX) * INT_MAX;
    heif_context_set_max_decoding_threads(result.get(), 0);
    return result;
}
Handle primary(heif_context* ctx, const char* path) {
    check(heif_context_read_from_file(ctx, path, nullptr));
    heif_image_handle* raw = nullptr;
    check(heif_context_get_primary_image_handle(ctx, &raw));
    Handle image(raw, heif_image_handle_release);
    require(image && heif_image_handle_get_width(image.get()) > 0 && heif_image_handle_get_height(image.get()) > 0,
            "Invalid HEIC/AVIF image dimensions");
    return image;
}
heif_image_tiling tiling(heif_image_handle* handle) {
    heif_image_tiling tiles{};
    tiles.version = 1;
    auto err = heif_image_handle_get_image_tiling(handle, 1, &tiles);
    if (err.code != heif_error_Ok || !tiles.num_columns || !tiles.num_rows || !tiles.tile_width || !tiles.tile_height) {
        tiles = {};
        tiles.version = 1; tiles.num_columns = tiles.num_rows = 1;
        tiles.tile_width = tiles.image_width = heif_image_handle_get_width(handle);
        tiles.tile_height = tiles.image_height = heif_image_handle_get_height(handle);
    }
    require(tiles.tile_width <= INT_MAX && tiles.tile_height <= INT_MAX, "HEIC/AVIF tile dimensions exceed supported coordinates");
    return tiles;
}
void budgetCheck(jlong requested, uint64_t pixels, uint64_t bitmapBytes, uint64_t bytesPerPixel) {
    if (requested < 0 || pixels > (UINT64_MAX - bitmapBytes - kReserve) / bytesPerPixel ||
        pixels * bytesPerPixel + bitmapBytes + kReserve > static_cast<uint64_t>(requested)) throw std::bad_alloc();
}
skcms_ICCProfile cicpProfile(int primaries, int transfer) {
    // ITU-T H.273 primary/white chromaticities, in R/G/B/white order.
    // The libheif setter validates the enum but does not fill its decoded xy
    // fields, so construct these primary matrices explicitly.
    std::array<float,8> xy;
    switch (primaries) {
        case 1: case 2: xy={.640f,.330f,.300f,.600f,.150f,.060f,.3127f,.3290f};break;
        case 4: xy={.670f,.330f,.210f,.710f,.140f,.080f,.310f,.316f};break;
        case 5: xy={.640f,.330f,.290f,.600f,.150f,.060f,.3127f,.3290f};break;
        case 6: case 7: xy={.630f,.340f,.310f,.595f,.155f,.070f,.3127f,.3290f};break;
        case 8: xy={.681f,.319f,.243f,.692f,.145f,.049f,.310f,.316f};break;
        case 9: xy={.708f,.292f,.170f,.797f,.131f,.046f,.3127f,.3290f};break;
        case 10: break; // XYZ, equal-energy white, rather than RGB primaries.
        case 11: xy={.680f,.320f,.265f,.690f,.150f,.060f,.314f,.351f};break;
        case 12: xy={.680f,.320f,.265f,.690f,.150f,.060f,.3127f,.3290f};break;
        case 22: xy={.630f,.340f,.295f,.605f,.155f,.077f,.3127f,.3290f};break;
        default: throw std::runtime_error("Unsupported image colour primaries");
    }
    skcms_Matrix3x3 matrix;
    require(primaries == 10 ? skcms_AdaptToXYZD50(1.0f/3,1.0f/3,&matrix) :
        skcms_PrimariesToXYZD50(xy[0],xy[1],xy[2],xy[3],xy[4],xy[5],xy[6],xy[7],&matrix),
        "Unsupported image colour primaries");
    skcms_ICCProfile profile; skcms_Init(&profile); skcms_SetXYZD50(&profile, &matrix);
    skcms_TransferFunction curve = *skcms_sRGB_TransferFunction();
    switch (transfer) {
        case 1: case 6: case 14: case 15:
            curve = {1.0f/0.45f, 1.0f/1.09929682680944f, 0.09929682680944f/1.09929682680944f,
                     1.0f/4.5f, 4.5f*0.018053968510807f, 0, 0}; break;
        case 2: case 13: break;
        case 4: curve = {2.2f,1,0,0,0,0,0}; break;
        case 5: curve = {2.8f,1,0,0,0,0,0}; break;
        case 7: curve = {1.0f/0.45f,1.0f/1.1115f,0.1115f/1.1115f,1.0f/4.0f,0.0912f,0,0}; break;
        case 8: case 16: case 18: curve = *skcms_Identity_TransferFunction(); break;
        case 17: curve = {2.6f,std::pow(52.37f/48.0f,1.0f/2.6f),0,0,0,0,0}; break;
        default: throw std::runtime_error("Unsupported image transfer characteristic");
    }
    skcms_SetTransferFunction(&profile, &curve);
    return profile;
}
float sourcePeak(heif_image_handle* handle, int transfer) {
    heif_content_light_level cll{};
    if (heif_image_handle_get_content_light_level(handle, &cll) && cll.max_content_light_level > 203)
        return std::min(10000.0f, static_cast<float>(cll.max_content_light_level));
    heif_mastering_display_colour_volume mastering{};
    if (heif_image_handle_get_mastering_display_colour_volume(handle, &mastering) && mastering.max_display_mastering_luminance > 2030000)
        return std::min(10000.0f, mastering.max_display_mastering_luminance / 10000.0f);
    return transfer == 18 ? 1000.0f : transfer == 16 ? 10000.0f : anpaint::colour::kSdrWhiteNits;
}
void storePixel(const float* source, uint8_t* target) {
    target[3] = anpaint::colour::byte(source[3]);
    for (int c = 0; c < 3; ++c) target[c] = anpaint::colour::byte(source[c] * source[3]);
}
// Copy destination pixels covered by this transformed source tile. Native
// 10/12-bit samples stay at their original precision through RGB conversion,
// profile conversion and HDR tone mapping; only the final sRGB result is 8-bit.
void copyTile(Pixels& output, heif_image* tile, heif_image_handle* handle, const std::vector<uint8_t>& icc,
              int64_t originX, int64_t originY, int64_t left, int64_t top, int64_t right, int64_t bottom) {
    const int64_t tileWidth = heif_image_get_width(tile, heif_channel_interleaved);
    const int64_t tileHeight = heif_image_get_height(tile, heif_channel_interleaved);
    require(tileWidth > 0 && tileHeight > 0, "Decoded HEIC/AVIF tile has no pixels");
    const int64_t sx0 = std::max(left, originX), sy0 = std::max(top, originY);
    const int64_t sx1 = std::min(right, originX + tileWidth), sy1 = std::min(bottom, originY + tileHeight);
    if (sx0 >= sx1 || sy0 >= sy1) return;
    const uint64_t width = right - left, height = bottom - top;
    const uint64_t x0 = ((sx0 - left) * output.info.width + width - 1) / width;
    const uint64_t x1 = std::min<uint64_t>(((sx1 - left) * output.info.width + width - 1) / width, output.info.width);
    const uint64_t y0 = ((sy0 - top) * output.info.height + height - 1) / height;
    const uint64_t y1 = std::min<uint64_t>(((sy1 - top) * output.info.height + height - 1) / height, output.info.height);
    const bool high = heif_image_get_chroma_format(tile) == heif_chroma_interleaved_RRGGBBAA_LE;
    const int depth = heif_image_get_bits_per_pixel_range(tile, heif_channel_interleaved);
    require(depth >= 8 && depth <= 16, "Unsupported HEIC/AVIF RGB sample depth");
    const size_t pixelBytes = high ? 8 : 4;
    const float maximum = static_cast<float>((1u << depth) - 1);
    size_t stride = 0;
    const uint8_t* data = heif_image_get_plane_readonly2(tile, heif_channel_interleaved, &stride);
    require(data && stride >= static_cast<uint64_t>(tileWidth) * pixelBytes, "Invalid HEIC/AVIF pixel layout");
    const bool associated = heif_image_is_premultiplied_alpha(tile) || heif_image_handle_is_premultiplied_alpha(handle);
    heif_color_profile_nclx* raw = nullptr;
    auto nclxError = heif_image_handle_get_nclx_color_profile(handle, &raw);
    // The container is authoritative. Some libheif RGB conversion steps retain
    // source samples but attach a default transfer to their output image.
    // Only use decoded bitstream metadata when no container profile exists.
    if (nclxError.code != heif_error_Ok) nclxError = heif_image_get_nclx_color_profile(tile, &raw);
    Profile nclx(raw, heif_nclx_color_profile_free);
    int transfer = nclxError.code == heif_error_Ok && nclx ? nclx->transfer_characteristics : 13;
    if (icc.empty() && !high && depth == 8 && nclx &&
        nclx->color_primaries == heif_color_primaries_ITU_R_BT_709_5 &&
        transfer == heif_transfer_characteristic_IEC_61966_2_1) {
        // These decoded samples already are 8-bit sRGB. A second matrix/TRC
        // round trip can move a low channel by one byte through floating-point
        // approximation and gamut mapping, breaking exact lossless AVIF import.
        // Retain the samples, applying only Android's required alpha association.
        for (uint64_t y = y0; y < y1; ++y) {
            const uint64_t sourceY = y * height / output.info.height + top - originY;
            for (uint64_t x = x0; x < x1; ++x) {
                const uint64_t sourceX = x * width / output.info.width + left - originX;
                const auto* source = data + sourceY * stride + sourceX * 4;
                auto* target = static_cast<uint8_t*>(output.data) + y * output.info.stride + x * 4;
                target[3] = source[3];
                for (int c = 0; c < 3; ++c) target[c] = associated ? source[c] :
                    static_cast<uint8_t>((source[c] * source[3] + 127) / 255);
            }
        }
        return;
    }
    auto profile = icc.empty() ? cicpProfile(nclx ? nclx->color_primaries : 1, transfer) : anpaint::colour::Transform::parse(icc.data(), icc.size());
    if (!icc.empty()) transfer = profile.has_CICP ? profile.CICP.transfer_characteristics : 0;
    anpaint::colour::Transform transform(profile, transfer, sourcePeak(handle, transfer));
    std::array<float, 256*4> buffer{};
    for (uint64_t y = y0; y < y1; ++y) {
        const uint64_t sourceY = y * height / output.info.height + top - originY;
        for (uint64_t x = x0; x < x1;) {
            const size_t count = std::min<uint64_t>(256, x1-x);
            for (size_t i = 0; i < count; ++i) {
                const uint64_t sourceX = (x+i) * width / output.info.width + left - originX;
                const auto* pixel = data + sourceY*stride + sourceX*pixelBytes;
                auto* p = buffer.data()+i*4;
                for (int c = 0; c < 4; ++c) p[c] = high ? (pixel[c*2] | (pixel[c*2+1] << 8)) / maximum : pixel[c]/255.0f;
                if (associated) for (int c = 0; c < 3; ++c) p[c] = p[3] > 0 ? p[c]/p[3] : 0;
            }
            transform.convert(buffer.data(), count);
            for (size_t i = 0; i < count; ++i)
                storePixel(buffer.data()+i*4, static_cast<uint8_t*>(output.data)+y*output.info.stride+(x+i)*4);
            x += count;
        }
    }
}
void convertBitmap(Pixels& input, Pixels& output, const anpaint::colour::Transform& transform) {
        const bool half = input.info.format == ANDROID_BITMAP_FORMAT_RGBA_F16;
        const size_t pixelBytes = half ? 8 : 4;
        const auto format = half ? skcms_PixelFormat_RGBA_hhhh : skcms_PixelFormat_RGBA_8888;
        const auto alpha = (input.info.flags & ANDROID_BITMAP_FLAGS_ALPHA_MASK) == ANDROID_BITMAP_FLAGS_ALPHA_UNPREMUL
            ? skcms_AlphaFormat_Unpremul : skcms_AlphaFormat_PremulAsEncoded;
        std::array<float, 256*4> buffer;
        for (uint32_t y = 0; y < input.info.height; ++y) for (uint32_t x = 0; x < input.info.width;) {
            const size_t count = std::min<uint32_t>(256, input.info.width-x);
            const auto* source = static_cast<uint8_t*>(input.data)+y*input.info.stride+x*pixelBytes;
            require(skcms_Transform(source, format, alpha, nullptr, buffer.data(), skcms_PixelFormat_RGBA_ffff,
                                   skcms_AlphaFormat_Unpremul, nullptr, count), "Cannot read decoded bitmap colour samples");
            transform.convert(buffer.data(), count);
            for (size_t i = 0; i < count; ++i)
                storePixel(buffer.data()+i*4, static_cast<uint8_t*>(output.data)+y*output.info.stride+(x+i)*4);
            x += count;
        }
}
Image encodeTile(Pixels& bitmap, uint32_t left, uint32_t top, uint32_t width, uint32_t height,
                 bool identity, const heif_color_profile_nclx* profile) {
    heif_image* raw = nullptr;
    check(heif_image_create(width, height, identity ? heif_colorspace_YCbCr : heif_colorspace_RGB,
                           identity ? heif_chroma_444 : heif_chroma_interleaved_RGB, &raw));
    Image image(raw, heif_image_release);
    check(heif_image_set_nclx_color_profile(image.get(), profile));
    const heif_channel channels[] = {heif_channel_Y, heif_channel_Cb, heif_channel_Cr};
    uint8_t* planes[3]{}; size_t strides[3]{};
    if (identity) {
        for (int i = 0; i < 3; ++i) {
            check(heif_image_add_plane(image.get(), channels[i], width, height, 8));
            planes[i] = heif_image_get_plane2(image.get(), channels[i], &strides[i]);
        }
    } else {
        check(heif_image_add_plane(image.get(), heif_channel_interleaved, width, height, 8));
        planes[0] = heif_image_get_plane2(image.get(), heif_channel_interleaved, &strides[0]);
    }
    for (uint32_t y = 0; y < height; ++y) {
        const uint32_t sy = std::min(top + y, bitmap.info.height - 1);
        for (uint32_t x = 0; x < width; ++x) {
            const uint32_t sx = std::min(left + x, bitmap.info.width - 1);
            const auto* source = static_cast<const uint8_t*>(bitmap.data) + static_cast<size_t>(sy) * bitmap.info.stride + sx * 4;
            // Document is opaque. Reject a caller error rather than labelling
            // premultiplied transparent values as a successful RGB export.
            require(source[3] == 255, "Flatten transparent pixels before HEIC/AVIF export");
            if (identity) {
                planes[0][y * strides[0] + x] = source[1]; // Y = G
                planes[1][y * strides[1] + x] = source[2]; // Cb = B
                planes[2][y * strides[2] + x] = source[0]; // Cr = R
            } else {
                auto* target = planes[0] + y * strides[0] + x * 3;
                std::memcpy(target, source, 3);
            }
        }
    }
    return image;
}
}

extern "C" JNIEXPORT jintArray JNICALL
Java_org_catrobat_paintroid_classic_HeifCodec_00024Native_info(JNIEnv* env, jobject, jstring path) {
    try {
        std::lock_guard<std::mutex> lock(codecMutex);
        Utf file(env, path); auto ctx = context(kReserve); auto image = primary(ctx.get(), file.text); auto tiles = tiling(image.get());
        jint values[] = {heif_image_handle_get_width(image.get()), heif_image_handle_get_height(image.get()),
                         static_cast<jint>(tiles.tile_width), static_cast<jint>(tiles.tile_height)};
        auto result = env->NewIntArray(4);
        if (result) env->SetIntArrayRegion(result, 0, 4, values);
        return result;
    } catch (const std::bad_alloc&) { fail(env, true, "Not enough memory to inspect HEIC/AVIF"); }
      catch (const std::exception& e) { fail(env, false, e.what()); }
    return nullptr;
}

extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_HeifCodec_00024Native_decode(JNIEnv* env, jobject, jstring path, jobject bitmap,
                                                             jint left, jint top, jint right, jint bottom, jlong maxBytes) {
    try {
        std::lock_guard<std::mutex> lock(codecMutex);
        Utf file(env, path); Pixels output(env, bitmap);
        const uint64_t outputBytes = static_cast<uint64_t>(output.info.stride) * output.info.height;
        budgetCheck(maxBytes, 0, outputBytes, 32);
        auto ctx = context(static_cast<uint64_t>(maxBytes) - outputBytes);
        auto handle = primary(ctx.get(), file.text); auto tiles = tiling(handle.get());
        budgetCheck(maxBytes, static_cast<uint64_t>(tiles.tile_width) * tiles.tile_height, outputBytes, 32);
        int width = heif_image_handle_get_width(handle.get()), height = heif_image_handle_get_height(handle.get());
        if (right < 0) right = width;
        if (bottom < 0) bottom = height;
        require(left >= 0 && top >= 0 && right > left && bottom > top && right <= width && bottom <= height,
                "HEIC/AVIF crop must stay inside the image");
        DecodeOptions options(heif_decoding_options_alloc(), heif_decoding_options_free);
        if (!options) throw std::bad_alloc();
        options->ignore_transformations = 0;
        options->convert_hdr_to_8bit = 0;
        options->output_image_nclx_profile_passthrough = 1;
        options->num_codec_threads = 1;
        // Preserve source transfer/primaries and alpha until explicit colour management.
        const bool high = std::max(heif_image_handle_get_luma_bits_per_pixel(handle.get()),
                                   heif_image_handle_get_chroma_bits_per_pixel(handle.get())) > 8;
        const auto chroma = high ? heif_chroma_interleaved_RRGGBBAA_LE : heif_chroma_interleaved_RGBA;
        const auto iccSize = heif_image_handle_get_raw_color_profile_size(handle.get());
        require(iccSize <= anpaint::colour::kMaximumIccBytes, "Embedded ICC profile exceeds the supported size");
        std::vector<uint8_t> icc(iccSize);
        if (iccSize) check(heif_image_handle_get_raw_color_profile(handle.get(), icc.data()));
        if (tiles.num_columns == 1 && tiles.num_rows == 1) {
            heif_image* raw = nullptr;
            check(heif_decode_image(handle.get(), &raw, heif_colorspace_RGB, chroma, options.get()));
            Image decoded(raw, heif_image_release);
            copyTile(output, decoded.get(), handle.get(), icc, 0, 0, left, top, right, bottom);
        } else {
            const uint32_t firstX = (static_cast<uint64_t>(left) + tiles.left_offset) / tiles.tile_width;
            const uint32_t firstY = (static_cast<uint64_t>(top) + tiles.top_offset) / tiles.tile_height;
            const uint32_t lastX = std::min<uint64_t>((static_cast<uint64_t>(right - 1) + tiles.left_offset) / tiles.tile_width, tiles.num_columns - 1);
            const uint32_t lastY = std::min<uint64_t>((static_cast<uint64_t>(bottom - 1) + tiles.top_offset) / tiles.tile_height, tiles.num_rows - 1);
            for (uint32_t y = firstY; y <= lastY; ++y) for (uint32_t x = firstX; x <= lastX; ++x) {
                heif_image* raw = nullptr;
                check(heif_image_handle_decode_image_tile(handle.get(), &raw, heif_colorspace_RGB, chroma, options.get(), x, y));
                Image decoded(raw, heif_image_release);
                copyTile(output, decoded.get(), handle.get(), icc, static_cast<int64_t>(x) * tiles.tile_width - tiles.left_offset,
                         static_cast<int64_t>(y) * tiles.tile_height - tiles.top_offset, left, top, right, bottom);
            }
        }
    } catch (const std::bad_alloc&) { fail(env, true, "Not enough memory to decode HEIC/AVIF at this size"); }
      catch (const std::exception& e) { fail(env, false, e.what()); }
}

extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_HeifCodec_00024Native_encode(JNIEnv* env, jobject, jobject bitmap, jstring path,
                                                             jstring format, jint quality, jboolean lossless, jlong maxBytes) {
    try {
        std::lock_guard<std::mutex> lock(codecMutex);
        Utf file(env, path), type(env, format); Pixels input(env, bitmap);
        const bool avif = std::strcmp(type.text, "avif") == 0;
        require(avif || std::strcmp(type.text, "heic") == 0, "Unknown HEIF output format");
        require(!lossless || avif, "HEIC export uses adjustable quality");
        const uint64_t inputBytes = static_cast<uint64_t>(input.info.stride) * input.info.height;
        const bool gridOutput = input.info.width > kEncodeTile || input.info.height > kEncodeTile;
        const uint32_t tileWidth = std::max(gridOutput ? 64u : 1u, std::min(input.info.width, kEncodeTile));
        const uint32_t tileHeight = std::max(gridOutput ? 64u : 1u, std::min(input.info.height, kEncodeTile));
        budgetCheck(maxBytes, static_cast<uint64_t>(tileWidth) * tileHeight, inputBytes, 64);
        auto ctx = context(static_cast<uint64_t>(maxBytes) - inputBytes);
        heif_encoder* rawEncoder = nullptr;
        check(heif_context_get_encoder_for_format(ctx.get(), avif ? heif_compression_AV1 : heif_compression_HEVC, &rawEncoder));
        Encoder encoder(rawEncoder, heif_encoder_release);
        check(heif_encoder_set_lossy_quality(encoder.get(), quality));
        check(heif_encoder_set_lossless(encoder.get(), lossless));
        if (avif) {
            check(heif_encoder_set_parameter_integer(encoder.get(), "threads", 1));
            check(heif_encoder_set_parameter_integer(encoder.get(), "speed", 8));
            check(heif_encoder_set_parameter_string(encoder.get(), "chroma", lossless ? "444" : "420"));
            check(heif_encoder_set_parameter_string(encoder.get(), "tune", "ssim"));
        }
        Profile profile(heif_nclx_color_profile_alloc(), heif_nclx_color_profile_free);
        EncodeOptions options(heif_encoding_options_alloc(), heif_encoding_options_free);
        if (!profile || !options) throw std::bad_alloc();
        profile->color_primaries = heif_color_primaries_ITU_R_BT_709_5;
        profile->transfer_characteristics = heif_transfer_characteristic_IEC_61966_2_1;
        profile->matrix_coefficients = lossless ? heif_matrix_coefficients_RGB_GBR : heif_matrix_coefficients_ITU_R_BT_601_6;
        profile->full_range_flag = 1;
        options->save_alpha_channel = 0;
        options->output_nclx_profile = profile.get();
        if (input.info.width <= kEncodeTile && input.info.height <= kEncodeTile) {
            auto tile = encodeTile(input, 0, 0, tileWidth, tileHeight, lossless, profile.get());
            check(heif_context_encode_image(ctx.get(), tile.get(), encoder.get(), options.get(), nullptr));
        } else {
            const uint32_t columns = (input.info.width + kEncodeTile - 1) / kEncodeTile;
            const uint32_t rows = (input.info.height + kEncodeTile - 1) / kEncodeTile;
            heif_image_handle* rawGrid = nullptr;
            check(heif_context_add_grid_image(ctx.get(), input.info.width, input.info.height, columns, rows, options.get(), &rawGrid));
            Handle grid(rawGrid, heif_image_handle_release);
            for (uint32_t y = 0; y < rows; ++y) for (uint32_t x = 0; x < columns; ++x) {
                auto tile = encodeTile(input, x * kEncodeTile, y * kEncodeTile, tileWidth, tileHeight, lossless, profile.get());
                check(heif_context_add_image_tile(ctx.get(), grid.get(), x, y, tile.get(), encoder.get()));
            }
            check(heif_context_set_primary_image(ctx.get(), grid.get()));
        }
        check(heif_context_write_to_file(ctx.get(), file.text));
    } catch (const std::bad_alloc&) { fail(env, true, "Not enough memory to encode HEIC/AVIF at this size"); }
      catch (const std::exception& e) { fail(env, false, e.what()); }
}


extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_HeifCodec_00024Native_convertColour(
        JNIEnv* env, jobject, jobject bitmap, jobject target, jbyteArray rawIcc, jint primaries, jint transfer) {
    try {
        std::lock_guard<std::mutex> lock(codecMutex);
        Pixels input(env, bitmap, true), output(env, target);
        require(input.info.width == output.info.width && input.info.height == output.info.height,
                "Colour conversion bitmap dimensions differ");
        std::vector<uint8_t> icc;
        skcms_ICCProfile profile;
        if (rawIcc) {
            const auto size = env->GetArrayLength(rawIcc);
            require(size > 0 && static_cast<size_t>(size) <= anpaint::colour::kMaximumIccBytes, "Embedded ICC profile exceeds the supported size");
            icc.resize(size); env->GetByteArrayRegion(rawIcc, 0, size, reinterpret_cast<jbyte*>(icc.data()));
            if (env->ExceptionCheck()) return;
            profile = anpaint::colour::Transform::parse(icc.data(), icc.size());
            transfer = profile.has_CICP ? profile.CICP.transfer_characteristics : 0;
        } else profile = cicpProfile(primaries, transfer);
        anpaint::colour::Transform transform(profile, transfer, transfer == 18 ? 1000.0f : transfer == 16 ? 10000.0f : anpaint::colour::kSdrWhiteNits);
        convertBitmap(input, output, transform);
    } catch (const std::bad_alloc&) { fail(env, true, "Not enough memory to convert image colour profile"); }
      catch (const std::exception& e) { fail(env, false, e.what()); }
}


extern "C" JNIEXPORT void JNICALL
Java_org_catrobat_paintroid_classic_HeifCodec_00024Native_convertPngColour(
        JNIEnv* env, jobject, jobject bitmap, jobject target, jfloat gamma, jfloatArray chromaticities) {
    try {
        std::lock_guard<std::mutex> lock(codecMutex);
        Pixels input(env, bitmap, true), output(env, target);
        require(input.info.width == output.info.width && input.info.height == output.info.height,
                "Colour conversion bitmap dimensions differ");
        auto profile = *skcms_sRGB_profile();
        if (chromaticities) {
            require(env->GetArrayLength(chromaticities) == 8, "PNG chromaticities must contain eight values");
            float xy[8]; env->GetFloatArrayRegion(chromaticities, 0, 8, xy);
            if (env->ExceptionCheck()) return;
            for (float value : xy) require(std::isfinite(value) && value >= 0 && value <= 1, "Invalid PNG chromaticity");
            skcms_Matrix3x3 matrix;
            require(skcms_PrimariesToXYZD50(xy[2],xy[3],xy[4],xy[5],xy[6],xy[7],xy[0],xy[1],&matrix),
                    "Unsupported PNG chromaticities");
            skcms_SetXYZD50(&profile,&matrix);
        }
        if (gamma != 0) {
            require(std::isfinite(gamma) && gamma > 0.01f && gamma <= 10.0f, "Unsupported PNG gamma value");
            skcms_TransferFunction curve{1.0f/gamma,1,0,0,0,0,0};
            skcms_SetTransferFunction(&profile,&curve);
        }
        anpaint::colour::Transform transform(profile);
        convertBitmap(input,output,transform);
    } catch (const std::bad_alloc&) { fail(env, true, "Not enough memory to convert PNG colours"); }
      catch (const std::exception& e) { fail(env, false, e.what()); }
}
