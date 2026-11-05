# Zhuang text alignment options

Base: `fdb5d8a4f450d2f61a0674e6a37b07c8577877b7` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 resources: `ui_left_aligned`, `ui_centred` and `ui_right_aligned`. All 183 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Wording review and evidence

Independent review supports concise positional options meaning left, middle and right. Lexical confidence is strong; fitness as text-alignment spinner labels is moderate. These are descriptive choices, not a claim of established Zhuang typography terminology. The middle label is axis-neutral because the same resource is used for horizontal and vertical writing. The existing left/right spelling is reused without changing those earlier resources.

- The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), B.htm 15–16/80, supports the left/right-side terms; C.htm 75/78 defines `cungqgyang` as middle, with the shorter `gyang` cross-reference at G.htm 102/110. The longer form avoids the shorter word's additional half-quantity sense. The mirror warns of incomplete proofreading.
- [Guangxi Minzu Bao, 5 June 2024, page 8](https://www.guangximinzubao.cn/szbzw/page/21/2024-06/05/08/2024060508_pdf.pdf), two prose translations, directly uses the left/right-side terms for two attendants, with a parallel Chinese original specifying left and right. The PDF text was directly readable; this is spatial evidence, not typography evidence.
- [Lu Yong's bilingual mathematics-teaching account, 22 April 2020](https://www.guangximinzubao.cn/szbzw/html/2020-04/22/content_35282.htm), section one, explicitly explains `cungqgyang` as middle/between. The article was directly read. It corroborates the spatial meaning, not an exact software label.

`ui_text_alignment` remains in English fallback. A verified technical noun for alignment was not established; substituting a broad text-position phrase would expand its meaning. This limited batch does not claim the entire text dialog is localized.

## Consumers and verification

- `TextStyleDialog` supplies the complete left/centre/right resources as horizontal spinner options in indices 0/1/2. Its accessibility description uses the separate alignment resource above. No added wording claims alignment to the whole canvas.
- Changing to vertical writing replaces the first and last choices with top/bottom, retains the middle resource and preserves the selected index. The shared middle label therefore does not specify a horizontal side.
- Preview and committed text map the indices to `Paint.Align.LEFT/CENTER/RIGHT`. `VerticalText.draw` offsets individual lines or columns within maximum text bounds. `PaintDocument.text` additionally shifts the whole block relative to the selected insertion point: half the text length for centre and full length for right/bottom. The changes do not alter these behaviors.
- 61 host tests pass in 14.611 seconds: translations, translation boundaries, priority accounting and current localization contracts. All 171 offered catalogues and the priority manifest pass structural validation. Six English/Zhuang Java literal render checks pass; the new strings have no format arguments.
- Missing-only integration preserves earlier values, attributes, placeholders, newlines, literal requirements, Android escaping and XML prefix bytes. Temporary code-token-aware Kotlin checks identify every added-key consumer, the axis-specific option order, retained selection, preview/commit mapping and insertion-anchor behavior. These are source checks, not Android interaction tests.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 260 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by complete tree and changed-file verification.

Zhuang direct presence becomes 186 resources: P0 68/94, P1 118/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,376 to 1,373; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed spinner/direction-change operation, device rendering/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
