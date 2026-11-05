# Zhuang clearing and selection commands

Base: `da54584f6108531c2576826d8f4bcaa4d23843fc` on `review/nv-bottom-2038-20261103`.

Adds the missing P0 clear-image command and P1 delete-selection and selection-category labels. All 139 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent wording and consumer review

Independent linguistic and current-consumer review accepted all three compositions with moderate confidence. Clear-image names everything inside the image rather than deletion of the image file. Delete-selection uses a classifier-plus-verb nominal construction for selected things/content. The category uses the compact select/choose label. These are authored, source-supported UI phrases, not quoted established software terminology or native-speaker certification. No concrete semantic correction was identified; idiomaticity remains less certain than the individual lexical meanings.

[MediaWiki's Zhuang catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/za.json) supports the delete verb and all/entire quantifier. [Primary newspaper prose](https://www.guangximinzubao.cn/zw/f_282583/645942.html) supplies selection and inside/container uses. Further prose supports [all/entire](https://www.guangximinzubao.cn/szbzw/html/2020-03/04/content_34860.htm) and [depicted images/figures](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm), not just photographs. Sio and Sybesma's [Northern Zhuang nominal-phrase study](https://www.academia.edu/214062/The_Nominal_Phrase_in_Northern_Zhuang_A_descriptive_study_2008_), section 3.3.1, examples 26c-d, independently supports a plural classifier followed by a verb as a nominal expression. That grammatical pattern supports the proposed selected-content phrase but does not attest this whole UI expression or settle every dialect's preference.

Current Kotlin consumers were checked:

- `ClassicPaintActivity` applies pending canvas work before `PaintDocument.clear()`. That method finishes any selection, checkpoints, fills the existing bitmap with its background, clears committed credits and marks an edit. It does not delete a file or resize the bitmap.
- Delete-selection calls `PaintDocument.deleteSelection()`. A non-floating selection has its region erased; floating selected content is discarded. The separate no-selection instruction remains English fallback. The label does not merely mean hide a selection outline.
- The selection category names the rectangle/lasso tool group and the Edit selection commands. `ToolCategoryButton` binds the chosen label into its displayed text and expanded/collapsed accessibility description, with selected-tool context. This is a source-binding check, not a device accessibility or layout result.

Neither command promises irreversibility or guaranteed recovery. Existing history/credit paths were inspected, but Android operations and Undo were not executed for this batch.

## Targeted verification

- 61 host tests pass: `test_translations`, `test_translation_boundaries`, `test_string_importance` and `test_current_localization_contracts`. This is not the full repository suite.
- All 171 offered catalogues and the priority manifest pass structural validation. Six English/Zhuang Java resource-render checks pass. These three additions have no format arguments.
- Three unique missing-only additions preserve source attributes, ordered formatting contracts, newlines and Android/XML escaping. All earlier resource values and the XML prefix bytes are retained.
- Temporary static consumer checks verify clear-image, selection deletion, the separate no-selection path, category binding and accessibility-description construction.
- All 1,252 materialized base files match the freshly fetched remote tree's Git hashes and executable modes. The other 245 non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, with full remote-tree and changed-file verification.

Zhuang direct presence becomes P0 67/94, P1 75/249, P2 0/305 and P3 0/71: 142 typed resources. Across 171 offered options, P0 gaps decrease from 165 to 164 and P1 gaps from 1,418 to 1,416; P2/P3 gaps remain 30,129/7,481. The 46 options containing all tracked resources remain unchanged. Direct presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed operation, Undo, device/layout/accessibility test, merge or release is claimed. No implementation, locale list, permissions, fonts, English resources or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
