# Early migration review

This is a current behavior/contract review. It does not demand permanent source snapshots or reconstruction of historical endpoints. The exact 04 runtime review is separately frozen at `../anpaint-pr55-natural-relayout-artifact-review-20261012/DELIVERY-FILES.json`.

## Findings sent to writer

1. Current font mapping validation accepted a required supplementary codepoint mapped to glyph65535 in a740-glyph font. Retained coverage saw the same codepoint set. Require all mappings in bounds, not just seven protected glyphs.
2. Declared zero-length format4 cmap was parsed beyond its subtable. Bound format4/12 lengths/counts/offsets and Unicode/glyph ranges before expansion.
3. Removing source licence text, or consistently removing all OFL permissions/conditions across all copies, passed current and retained disclosure checks. Complete normalized canonical licence inputs are meaningful product fixtures; historic source-file reconstruction is unnecessary.
4. Removing the HTTP message contract and all SVG contracts in memory left all9 initial wording tests green. Explicit current family/key/nonempty-locale validation is needed. `probe_wording_coverage.py` and its log preserve this finding; no source/fixture file was mutated by the probe.
5. Retained phase tests still froze app/library method totals. Use current SDK-eligible disjoint set union, explicit eligibility omissions, operational deadlines and a new-method positive control.
6. Initial whole-glyph/mark native controls exercised only the component-loss guard. Add a focused opaque-sample clip with the component surviving to prove the independent opaque-loss guard actually rejects its intended defect.

The writer accepted these issues. Early static inspection confirms fixes for4/5/6 are being incorporated; font fixes are pending. Final focused tests, final source scope and compilation/native execution remain separately required before those fixes can be called verified.

## Sound retained design

Parsed default+59 wording, intentional81 fallback choices, Android formatting/duplicate-key/Unicode controls, Hungarian label/legal literals, Help provider/caption constraints, TIFF current literal expectations and actual Kotlin resource/flow/lifecycle tests are retained. Removing full XML/source hashes and inverse adapters is appropriate. Historical tests of failed evidence files are removable where the generic malformed/duplicate/phase/transport controls remain.

The raster-policy change preserves every original alpha/ARGB diagnostic and independent complete reference, plus all72 earlier native mutations. Hard positive checks reject empty/unsafe reference allocations, missing complete ink components and completely missing opaque reference samples. Other differences remain review-required. Components are not glyph segmentation; partial loss still needs explicit review. No production geometry, text, font, shader or tolerance change is supported by this review.

The new focused native controls use a separate TextView and actual Canvas clips, with unchanged full reference and complete text/accessibility. Their live execution is still unrun locally. The reference component scan is bounded by the existing allocation cap; its queue cannot exceed the counted nonzero reference samples.
