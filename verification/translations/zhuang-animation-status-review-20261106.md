# Zhuang unknown-animation warning and complete animation-family review

Date: 2026-11-06 UTC. Base `46a9b46a174009b2facad98a057f86061cf30369`, tree `07e17c10d1cb0d1d7d1376ad3b9d66fff59bc463`.

## P0 hold resolved

Added missing P0 `formats22_animation_unknown` in canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 315 preceding resource nodes, attributes and prefix bytes remain unchanged.

The new warning first identifies excessive file complexity, then asks explicitly whether it contains at least two pictures/frames and states that AN Paint cannot determine that. It then explains still-image-only opening and still saved output. A standalone question removes the previously unresolved scope of a question marker after a negated ascertainment predicate. It is neither an assertion of multiple frames nor merely an unknown exact count. It does not classify the source as static, require visible movement between frames, promise preservation of animation, claim a save already succeeded, or say the source file changes.

Independent full-value review accepted this revision unchanged. Semantic/scope confidence is moderately high; full-sentence naturalness remains moderate. The question-and-response form is somewhat conversational but makes the uncertainty explicit. Picture/frame and still-image wording remain descriptive compositions, not claims of standardized technical terminology or native-speaker certification. This replaces the specific unresolved construction recorded in the earlier lower-bound report; it does not restore withdrawn historical blanket approvals.

## Existing six-entry review cohort

All six existing full values were independently reviewed against current consumers and retained:
- `formats22_animation_title`: descriptive animated-image label, used only after at least two frames are established.
- `formats22_open_still`: neutral still-image opening command and unknown-status title.
- `formats22_animation_message`: format, contained-picture count, still-image editing and still saved output. Its string count accepts either an exact count or the complete lower-bound fragment.
- `formats22_animation_still`: imports only the first picture; saved output is still. Its quoted Save command matches current `Rom`.
- `formats22_animation_poster`: imports the separate PNG image instead of this animation, not a general prohibition on opening animation. “Default” is conveyed by the selected separate image's role. Saved output remains still; the Save command matches `Rom`.
- `formats22_at_least_frames`: genuine minimum count; the containing sentence supplies its classifier and noun, without duplication.

These seven values comprise this bounded review. No other translated resource or fallback receives review credit. Whole-language and all-translated-string release review remain incomplete.

## Sources and actual branch behavior

[Dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports `labcab` complex (L.htm 2/49), `ceiqnoix` at least (C.htm 32/78), sentence-final `lwi` (L.htm 48/49), and `rox` know (R.htm 18/33). The OCR warns of incomplete proofreading. [A published translation discussion](https://www.guangximinzubao.cn/szbzw/html/2018-06/20/content_26157.htm) supplies the picture classifier and a `rox ndaej` construction; the article is also a caution against mechanical word-for-word substitution. [Modern prose](https://www.guangximinzubao.cn/zw/l/393949.html) supports `ndawde` as containment/member reference. These pages were directly retrieved by both checks. The independent review additionally checked [official ordinal and inability constructions](https://www.guangximinzubao.cn/sy/gg/383691.html). Components support the authored sentence but do not attest it verbatim.

`AnimationMetadata` performs a bounded container scan. At its work limit, zero or one proven frame means multiple-frame status is unknown; it does not mean static. Proven counts of at least two remain exact or lower-bound counts as appropriate. Malformed/unsupported/single-frame completed scans may instead return null and proceed to ordinary decoding. The scanner is not an image validator and does not decode pixels.

`AnimationInfo` forwards all result fields. `ImportSelection.showAnimation` selects the new warning only when `frameCount < 2`, with the neutral Open still image title. It does not append the known-count message or poster/first-frame suffix to that branch. The known branch formats the exact/lower-bound count and selects its separate-PNG or first-frame suffix. Continue selects index zero; negative action and cancellation dispose of the staged input. No scanner, decoder, dialog or saving logic changes.

## Verification

- Fresh review head reconciled with the previous verified publication. Develop remained `412aab0c604060fb66fbd2edc6bb05572d10b56d`; separate Navajo work remains untouched. All 1,589 base files matched Git blob contents and executable modes.
- One unique missing scalar added with unchanged `%1$s`, source attributes and escaping. Literal, numeric, newline and old-value preservation checks pass. All 171 offered catalogues and the priority manifest pass structural validation. XML blob `1e5f0b590d4c92748129c3de92905f22865d36e0`, 31,538 UTF-8 bytes.
- 61 localization host tests passed in 5.740 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- 11 production Java scanner tests passed in 2.589 seconds via `test_animation_metadata`: exact GIF/APNG/WebP counts, separate PNG poster, decoy markers, malformed/truncated containers, bounded scans with zero/one/proven-multiple frames and large sparse chunks. This is actual scanner execution, not Android decoding.
- 46 host Java formatting/composition cases passed across English and Zhuang: static family values, unknown-status format arguments including percent/Unicode/empty/null robustness values, lower-bound integers and exact/lower-bound message composition. Extreme formatting inputs are not claims about actual scanner outputs.
- Temporary token-aware checks verified all eight resource bindings, unknown versus known branch boundaries, title and suffix selection, continue/cancel ownership, unchanged field forwarding and current quoted Save labels. `git diff --check` passed.

Zhuang has 316 typed resources: P0 75/94, P1 158/249, P2 80/305, P3 3/71. Global missing counts over 171 offered options are 156/1,333/30,049/7,478 for P0–P3; 46 options have complete presence. Presence is not fluency, full-review acceptance or release readiness.

Android SDK/Kotlin compiler are unavailable here. Android build/AAPT, actual localized dialog/layout/accessibility, image decoding and saved-output animation behavior were not executed. No merge or release is claimed. Only canonical XML and this report change; temporary wording mirrors/tests are not published. The conditional P0/P1 completion and all-translated-string review release plan remains in force.
