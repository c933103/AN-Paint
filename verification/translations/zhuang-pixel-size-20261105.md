# Zhuang pixel-size labels

Base: `87e8d867d3a50b27ed53f56f622f7466e9648627` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 strings: two pixel-size labels and the 1–1024-pixel text-size instruction. All 170 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent linguistic and current-consumer review accepted the three compositions. The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports size/dimensions and use; [contemporary newspaper prose](https://www.guangximinzubao.cn/zw/s_282578/382779.html), paragraph 65, uses the dimension noun in frame construction. The technical abbreviation `px` is already explicit in the English size label and neighboring source resources. Using it in the other label and range instruction preserves the pixel unit without inventing a Zhuang pixel term. It does not mean points or density-independent units.

The range and unit have strong semantic support; complete UI idiomaticity remains a compositional judgment. Abbreviation may be less familiar than an expanded unit word or less clear when read aloud. No device, TTS or screen-reader claim is made.

Two draft text-entry labels were excluded. Their verbs were supported, but a bounded independent check did not establish the existing bare `vwnz` noun as text. Catalogue consistency alone was not accepted as proof. This is an evidence gap, not a finding that the existing noun is wrong. Existing text labels remain unchanged, and neither omitted key receives completion credit.

## Consumer and targeted checks

- `TextStyleDialog` pairs the expanded-source pixel-size label with its size field, not line spacing. The field enables decimal input; submission parses a float and accepts the inclusive 1–1024 range. The translation preserves both bounds and adds no integer-only restriction. Line-spacing validation remains separate at 50–300 percent.
- Preview and final document text assign the selected size to `Paint.textSize`. The preview additionally scales its drawing to fit its available display area; no claim of identical on-screen and committed glyph dimensions is made.
- `ClassicPaintActivity` uses the short size label for pencil and stroke-width sliders. These have their own 1–100 range; the text-size error is not used for those sliders.
- 62 host tests pass: translations, translation boundaries, priority accounting, current localization contracts and numeric-entry source coverage. All 171 offered catalogues and the priority manifest pass structural checks. Six English/Zhuang Java resource-render checks pass; these strings have no format arguments.
- Missing-only integration preserves attributes, formatting, source numerals, newlines, escaping, all earlier values and XML prefix bytes. Temporary Kotlin source checks identify every consumer and distinguish text size, spacing and slider ranges. They are static checks, not Android input or rendering tests.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 255 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full tree and changed-file verification.

Zhuang direct presence becomes 173 resources: P0 68/94, P1 105/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,389 to 1,386; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed text operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
