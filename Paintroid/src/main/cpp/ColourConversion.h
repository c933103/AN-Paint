// AN Paint, 2026. AGPL-3.0-or-later.
// Uses the bundled skcms and JPEG XL colour-management implementations;
// their original BSD licences are included in JXL_NOTICES.txt.
#pragma once
#include <skcms.h>
#include "lib/jxl/cms/tone_mapping.h"
#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <stdexcept>

namespace anpaint::colour {
constexpr float kSdrWhiteNits = 203.0f;
constexpr size_t kMaximumIccBytes = 4 * 1024 * 1024;
inline float bounded(float value) { return std::isfinite(value) ? std::clamp(value, 0.0f, 1.0f) : 0.0f; }
inline uint8_t byte(float value) { return static_cast<uint8_t>(std::lround(bounded(value) * 255.0f)); }

// Convert into linear sRGB before quantization. HDR uses the pinned libjxl
// Rec.2408 luminance mapping, then its hue-preserving gamut mapping. Alpha is
// linear coverage and is never gamma-corrected or included in tone mapping.
class Transform {
 public:
    explicit Transform(const skcms_ICCProfile& profile, int transfer = 0, float sourcePeak = 203.0f)
        : source_(profile), linear_(*skcms_sRGB_profile()), transfer_(transfer), peak_(sourcePeak) {
        skcms_SetTransferFunction(&linear_, skcms_Identity_TransferFunction());
        if (source_.has_CICP && (source_.CICP.transfer_characteristics == 16 || source_.CICP.transfer_characteristics == 18)) {
            transfer_ = source_.CICP.transfer_characteristics;
            source_.has_CICP = false;
            // HDR CICP supplies the transfer; the ICC matrix still supplies
            // primaries and white-point adaptation. Do not apply an A2B table
            // as well as the explicit HDR transfer.
            if (!source_.has_toXYZD50) throw std::runtime_error("HDR ICC profile needs an RGB primary matrix");
            source_.has_A2B = false;
        }
        if (transfer_ == 16 || transfer_ == 18 || (transfer_ == 8 && sourcePeak > 255.0f)) {
            source_.has_A2B = false;
            skcms_SetTransferFunction(&source_, skcms_Identity_TransferFunction());
            peak_ = std::clamp(sourcePeak, kSdrWhiteNits, 10000.0f);
            mapper_ = std::make_unique<jxl::Rec2408ToneMapperBase>(
                jxl::Range{0.0f, peak_}, jxl::Range{0.0f, kSdrWhiteNits}, jxl::Vector3{0.2126f, 0.7152f, 0.0722f});
        }
    }
    static skcms_ICCProfile parse(const void* bytes, size_t length) {
        skcms_ICCProfile profile;
        if (!length || length > kMaximumIccBytes || !skcms_Parse(bytes, length, &profile))
            throw std::runtime_error("Invalid or unsupported embedded ICC colour profile");
        if (profile.data_color_space != skcms_Signature_RGB && profile.data_color_space != skcms_Signature_Gray)
            throw std::runtime_error("Embedded colour profile does not describe decoded RGB/gray pixels");
        return profile;
    }
    // Input/output RGBA are unassociated; input colour samples retain native
    // precision until this operation. The result is sRGB with unassociated alpha.
    void convert(float* rgba, size_t count) const {
        if (mapper_) {
            for (size_t i = 0; i < count; ++i) {
                auto* p = rgba + i * 4;
                if (transfer_ == 16) {
                    constexpr float m1 = 2610.0f / 16384.0f, m2 = 2523.0f / 32.0f;
                    for (int c = 0; c < 3; ++c) {
                        const float n = std::pow(bounded(p[c]), 1.0f / m2);
                        p[c] = 10000.0f / kSdrWhiteNits * std::pow(std::max(n - 3424.0f / 4096.0f, 0.0f) /
                            (2413.0f / 128.0f - 2392.0f / 128.0f * n), 1.0f / m1);
                    }
                } else if (transfer_ == 18) {
                    for (int c = 0; c < 3; ++c) {
                        const float n = bounded(p[c]);
                        p[c] = n <= 0.5f ? n * n / 3.0f : (std::exp((n - 0.55991073f) / 0.17883277f) + 0.28466892f) / 12.0f;
                    }
                } else {
                    for (int c = 0; c < 3; ++c) p[c] *= peak_ / kSdrWhiteNits;
                }
            }
        }
        if (!skcms_Transform(rgba, skcms_PixelFormat_RGBA_ffff, skcms_AlphaFormat_Unpremul, &source_,
                            rgba, skcms_PixelFormat_RGBA_ffff, skcms_AlphaFormat_Unpremul, &linear_, count))
            throw std::runtime_error("Embedded colour profile cannot be converted to sRGB");
        for (size_t i = 0; i < count; ++i) {
            auto* p = rgba + i * 4;
            jxl::Color rgb{p[0], p[1], p[2]};
            for (int c = 0; c < 3; ++c) if (!std::isfinite(rgb[c])) rgb[c] = 0;
            if (mapper_) {
                if (transfer_ == 18) {
                    // BT.2100 reference-display OOTF (1,000 cd/m2, gamma 1.2).
                    // Compute Y after primary conversion, so HLG tagged with
                    // Display-P3 or other primaries does not use BT.2020 weights.
                    const float luminance = std::max(0.0f, 0.2126f*rgb[0] + 0.7152f*rgb[1] + 0.0722f*rgb[2]);
                    const float scale = (1000.0f / kSdrWhiteNits) * std::pow(luminance, 0.2f);
                    for (int c = 0; c < 3; ++c) rgb[c] *= scale;
                }
                for (int c = 0; c < 3; ++c) rgb[c] *= kSdrWhiteNits / peak_;
                mapper_->ToneMap(rgb);
            }
            jxl::GamutMapScalar(rgb, jxl::Vector3{0.2126f, 0.7152f, 0.0722f});
            for (int c = 0; c < 3; ++c) {
                const float v = bounded(rgb[c]);
                p[c] = v <= 0.0031308f ? 12.92f * v : 1.055f * std::pow(v, 1.0f/2.4f) - 0.055f;
            }
            p[3] = bounded(p[3]);
        }
    }
 private:
    skcms_ICCProfile source_, linear_;
    int transfer_;
    float peak_;
    std::unique_ptr<jxl::Rec2408ToneMapperBase> mapper_;
};
}
