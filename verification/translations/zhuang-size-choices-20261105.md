# Zhuang image-size choices and limits

Base: `c17ab16a688707841f35d0d9e12d6ea1baa1f48f` on `review/nv-bottom-2038-20261103`.

Adds five missing P1 resources: original size, choosing a smaller size, excessive selection dimensions, resize-and-load, and the instruction to choose dimensions no larger than the original. All 142 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Wording and current consumers

Independent linguistic/context review accepted four drafts and recommended expanding the fifth comparison target; that revision is included. Confidence is moderate for the selected-content noun phrase. The resize-and-load label uses ordinary open in this import-dialog context, not a separately established technical term for loading. No concrete grammatical blocker remains; these are source-supported editorial compositions, not native-speaker certification.

The size noun is independently attested in a [craft-construction account](https://www.guangximinzubao.cn/zw/s_282578/382779.html). Published prose supports [smaller](https://www.guangximinzubao.cn/szbzw/html/2024-01/17/content_49035.htm), [excessive physical size](https://www.guangximinzubao.cn/szbzw/html/2024-02/07/content_49215.htm), and [greater/less-than comparisons](https://www.guangximinzubao.cn/zw/f_282583/390903.html). A [parallel Chinese/Zhuang Civil Code passage](https://www.guangximinzubao.cn/szbzw/html/2021-09/29/content_41823.htm), articles 312–313, supports original as a post-nominal modifier. This is linguistic evidence, not a legal claim about the app.

The change-dimensions wording is also consistent with a [published account of enlarging a photograph](https://www.guangximinzubao.cn/zw/f_282583/377720.html). Review checked open against the hai entry in a [dictionary transcription](https://dokumen.pub/sawloih-cuengh-gun-ocr.html); this is secondary OCR, not verification against an original dictionary scan.

Sio and Sybesma's [Northern Zhuang nominal-phrase study](https://www.academia.edu/214062/The_Nominal_Phrase_in_Northern_Zhuang_A_descriptive_study_2008_), sections 3.3.1 and 6.1, supports classifier-plus-verb/adjective nominal expressions and post-nominal modifiers. The selected-content construction is grammatically supported but is not an independently attested conventional software term. The no-larger instruction repeats the size noun in the comparison target to avoid unnecessary ellipsis. Its negated greater-than comparison allows equality; it is not the separate strictly-smaller instruction.

Current Kotlin consumer review and static binding checks establish:

- `ClassicPaintActivity` binds original size to `PaintDocument.restoreSelectionSize()`. It restores the selection rectangle to its source image's width and height around the current centre. It does not reset the canvas dimensions or resample the source pixels. The caller also adjusts the viewport.
- `AssemblyActivity.outputSizeDialog()` appends the smaller-size instruction when a valid output size fails `renderer.fits(size)`. The create-output button remains disabled for an invalid or non-fitting size. This label alone does not explain every memory constraint.
- `PaintDocument.transformedSelectionImage()` binds the selection-size error to a check that transformed bounds fit the positive integer dimension range before allocation. The English error also covers the lower-bound check; this batch does not change that existing diagnostic or claim all failures are memory shortages.
- Both `ImportPlan.create()` and `IcoCodec.decode()` use the no-larger instruction for per-axis comparisons against source dimensions. Equal width/height is allowed; excessive width or height is rejected.
- `ImageResizeDialog` binds resize-and-load to the positive button, enables it only for an accepted plan and invokes the resize callback after refreshing validation. The label makes no promise that the original file is rewritten. Surrounding explanations remain English where untranslated.

## Verification

- 61 host tests pass: `test_translations`, `test_translation_boundaries`, `test_string_importance` and `test_current_localization_contracts`. These are targeted checks, not the full repository suite.
- All 171 offered catalogues and the priority manifest pass structural validation. Ten English/Zhuang Java resource-render checks pass; these five additions have no format arguments.
- Missing-only integration preserves source attributes, formatting contracts, newlines and Android/XML escaping, plus all previous values and XML prefix bytes.
- Temporary static checks cover all five consumer paths above. They inspect Kotlin source bindings; they do not execute Android import, sizing, rendering or UI interactions.
- All 1,252 materialized base files match the fresh remote tree's Git hashes and executable modes. The other 246 non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, with full remote-tree and changed-file verification.

Zhuang direct presence becomes P0 67/94, P1 80/249, P2 0/305 and P3 0/71: 147 typed resources. Global P1 gaps across 171 offered options decrease from 1,416 to 1,411. P0/P2/P3 gaps remain 164/30,129/7,481, and the 46 options containing all tracked resources are unchanged. Direct presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed import/selection operation, device/layout/accessibility test, merge or release is claimed. No implementation, locale list, permissions, fonts, English resources or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
