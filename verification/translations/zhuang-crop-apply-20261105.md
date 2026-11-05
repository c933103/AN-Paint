# Zhuang apply controls and crop failure notice

Base: `9628731f3b06afd0eaf7932739506b2fd20673ba` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 strings for Apply, Apply crop and the crop-submission fallback error. All 153 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent language and consumer review accepted the two action labels and revised the failure sentence's word order. The crop is now the grammatical topic/underlying object, followed by the verb and negative potential construction. [Sybesma's postverbal-ndaej study](https://www.researchgate.net/publication/300848712_6_Zhuang_A_Tai_language_with_some_Sinitic_characteristics_Postverbal_%27can%27_in_Zhuang_Cantonese_Vietnamese_and_Lao), section 3.3.2, examples 27–28, directly supports that order and `yungh mbouj ndaej`; section 3.3.4 reinforces verb adjacency. The notice expresses that this crop cannot be applied in the failure context, without turning it into a prohibition or claiming permanent impossibility.

The [terminology commission's ninth list](https://www.guangximinzubao.cn/szbzw/html/2025-09/03/content_54472.htm), entry 103, supports `yungh` in digital-technology application. [Published discussion of rhetorical methods](https://www.guangximinzubao.cn/zw/l/393949.html) also uses it for applying abstract methods. These support the use/apply sense, not an exact software button attestation.

[Sio and Sybesma's nominal-phrase study](https://www.academia.edu/214062/The_Nominal_Phrase_in_Northern_Zhuang_A_descriptive_study_2008_), section 3.3.1, supports classifier-plus-verb nominalization. Its examples name entities such as food and clothing, not this exact abstract crop. Applying that construction to a selected crop remains editorial. The cutting and edge vocabulary has primary support in the [10 September 2025 translation page](https://www.guangximinzubao.cn/szbzw/html/2025-09/10/content_54492.htm) and [16 October 2024 prose](https://www.guangximinzubao.cn/szbzw/html/2024-10/16/content_51700.htm).

Confidence is moderate-high for the generic action and moderate for the crop compositions. No complete new phrase is claimed as independently attested software terminology. Technical idiomaticity remains uncertain; native-speaker certification is not claimed.

## Consumer and targeted checks

- Generic Apply commits a valid typed number in `NumericSlider`, new/resized dimensions in `ClassicPaintActivity.dimensionsDialog`, or coordinates in `AssemblyPositionDialog`. Source checks preserve their validation before mutation.
- `ImageCropDialog` binds Apply crop to its positive button. Submission constructs every selected crop rectangle before invoking the apply callback.
- The failure resource is used only for a null exception message in that submission listener; existing diagnostic messages remain visible. The listener includes validation, apply and dismissal. No failure-atomicity or unchanged-state guarantee is inferred from this wording.
- 62 host tests pass: translations, translation boundaries, priority accounting, current localization contracts and numeric-entry source coverage. All 171 offered catalogues and the priority manifest pass structural validation. Six English/Zhuang Java resource-render checks pass; these three strings contain no format arguments.
- Missing-only integration preserves attributes, formatting, newlines, escaping, earlier values and XML prefix bytes. Temporary consumer checks cover the routes above; they do not execute Android controls.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 249 other non-tree entries are retained. The publication procedure uses an expected parent and non-force branch lease, followed by full-tree and changed-file verification.

Zhuang direct presence becomes 156 resources: P0 68/94, P1 88/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,406 to 1,403; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

Reset crop remains unchanged: its actual action zeros the four margin inputs and refreshes the full-original-extent preview, not cancellation or immediate Undo. A suitably precise reset label was not established in this bounded review.

No Android build/AAPT, installed dialog/crop operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
