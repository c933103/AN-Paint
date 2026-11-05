# Zhuang redo and drawing-resumption commands

Base: `ecd0323c2eb59f37eb600a3ad8f5268fd5c2ee46` on `review/nv-bottom-2038-20261103`.

Adds two missing P1 resources, `ui_redo` and `ui_draw_again`. All 178 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent linguistic and current-consumer review accepted the redo composition at moderate confidence. Review changed the drawing command from a literal repeat-drawing formulation to continuation, because the actual action returns from zoom to the remembered drawing tool. The final commands distinguish reapplying history from resuming drawing and do not instruct the user to redraw the entire image.

The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supplies the senses again (`caiq`, C.htm 17/78), do (`guh`, G.htm 71/110), draw (`veh`, V.htm 12/19) and continue (`laebdaeb`, L.htm 4/49). This is a reproduction of the 1984 dictionary with an explicit incomplete-proofreading caveat, not a current software terminology standard.

A [published translation discussion](https://www.guangximinzubao.cn/szbzw/html/2022-06/22/content_44015.htm), examples 1 and 9, explains continuation and its placement before an activity verb. [Narrative prose](https://www.guangximinzubao.cn/szbzw/html/2025-09/10/content_54490.htm), paragraph 29, uses the same continuation word for walking after an interruption. [Classroom prose](https://www.guangximinzubao.cn/szbzw/html/2025-12/03/content_55130.htm), paragraph 28, supports drawing as an activity. These directly read sources support the words and construction, not the exact final UI collocations. The redo label is a contextual composition, not an independently attested Zhuang software term. Both labels retain moderate confidence; no native-speaker certification is claimed.

## Consumers and targeted verification

- `EditIcon.REDO` resolves the complete redo resource. `ActionButton` uses it for accessibility description and tooltip; the activity also uses the same icon label for tooltip-help feedback. The redo button is enabled only when not busy and redo history is available.
- `ClassicPaintActivity.redoEdit()` cancels pending input, then calls `PaintDocument.redo()`. That moves from redo history to undo history and restores the saved raster and credits; it does not re-execute an arbitrary prior command. The empty-history path returns without restoring an entry. These are source observations, not runtime execution results.
- The zoom options' drawing button uses the complete selected resource as its visible label and accessibility description. It chooses the last non-zoom tool. Tool selection can apply pending content and finish a selection, so this report does not claim the switch is mutation-free or that it automatically draws a new stroke.
- 63 host tests pass in 8.172 seconds: translations, translation boundaries, priority accounting, current localization contracts and locale-tooltip source wiring. All 171 offered catalogues and the priority manifest pass structural validation. Four English/Zhuang Java render checks pass; neither new resource has format arguments.
- Missing-only integration preserves existing values, attributes, placeholders, newlines, literal requirements, escaping and XML prefix bytes. Temporary code-token-aware Kotlin source checks identify both consumers and verify the bindings and action distinction above. The tooltip checks are structural, not installed Android accessibility tests.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 258 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full tree and changed-file verification.

Zhuang direct presence becomes 180 resources: P0 68/94, P1 112/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,381 to 1,379; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed undo/redo or tool-switch operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
