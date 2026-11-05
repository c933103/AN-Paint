# Zhuang text styles

Base: `ed8e5cb672230257e99e37c4f9fbfb91d9335d9c` on `review/nv-bottom-2038-20261103`.

Adds the missing P1 bold, italic and underline controls (`ui_bold`, `ui_italic`, `ui_underline`). All 187 earlier typed resources and attributes remain unchanged. Only Zhuang XML and this report change.

## Wording and evidence

Independent review recommends descriptive compositions for thick characters, slanted characters and a line below characters. Confidence is moderate: the component meanings are supported, but the complete labels are not established standardized typography terms in the sources checked. Strikethrough remains in English fallback because a comparably clear supported composition was not ready.

- [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `co`, C.htm 59/78, includes thickness with a thick-thread example, not just roughness; `ngeng`, N.htm 43/72, means tilted or sideways; `sienqdiuz`, S.htm 29/52, means a line or stroke; `laj`, L.htm 1/49, means below. The full line/stroke compound avoids relying on the narrower bare metal-wire entry. The mirror warns that proofreading is incomplete.
- [Gyaep Rongh Baenaj, 3 December 2025](https://www.guangximinzubao.cn/szbzw/html/2025-12/03/content_55130.htm), the classroom-activities paragraph containing “sij cih,” corroborates writing characters/text. This article was directly readable. The labels describe styled text, not a limit to one character.
- [Guangxi Minzu Bao, 29 May 2024, page 5](https://www.guangximinzubao.cn/szbzw/page/21/2024-05/29/05/2024052905_pdf.pdf) corroborates the slant word in an umbrella-tilting context. Only indexed text was available; opening the PDF returned an inaccessible-URL tool error. This is corroboration of a component meaning, not direct attestation of italic typography.

## Actual consumers

`TextStyleDialog` displays each whole resource as an independent checkbox label. Bold and italic set separate Android Typeface style bits. The live update supplies those bits through `FontCatalog.faceForText` to both the input and preview typefaces. Underline updates preview paint. The positive action returns the chosen typeface and underline setting; the separate Cancel action does not commit text. Font selection and fallback can affect appearance, so the labels do not promise identical visible results for every font.

`PaintDocument.text` carries the selected underline flag into text paint and uses the shared `VerticalText` renderer, as does the preview. That renderer copies paint into shaping paint. Sideways runs rotate text and its decoration together; “below characters” describes the ordinary text-baseline relation, not a promise that the line is always below the text on the physical screen in vertical modes. No implementation changes are made.

## Checks and limitations

- 61 host tests pass in 10.142 seconds: translations, translation boundaries, priority accounting and current localization contracts. All 171 offered catalogues and the priority manifest pass validation. Six English/Zhuang Java literal render checks pass.
- Missing-only XML checks preserve all prior values, source attributes, typed ordered placeholders, newlines, literal requirements, Android escaping and prefix bytes. Temporary token-aware source checks identify the sole actual binding of each key and verify checkbox wiring, style bits, live input/preview propagation, font handling, separate commit/cancel actions, paint flags and shared vertical rendering. These are static checks, not executed Android interactions.
- All 1,252 materialized base files match fresh Git hashes and executable modes; 262 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full-tree and changed-file verification.

Zhuang direct presence is now 190 resources: P0 68/94, P1 122/249, P2 0/305 and P3 0/71. Global P1 gaps decrease from 1,372 to 1,369; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed style-toggle behavior, font appearance, cancellation, vertical rendering, device layout/accessibility, merge or release is claimed. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
