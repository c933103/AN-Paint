# Zhuang selection prerequisites

Base: `2c2e3dff33667471b9fc6f886bba0b6af60968e4` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 strings: selecting an area, selecting an area first, and choosing at least one image. All 156 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent language and consumer review accepted the area prompts and moved the minimum-count modifier before the verb in the image prerequisite. The latter requires one or more images; it does not limit the user to exactly one.

[Published Zhuang prose](https://www.guangximinzubao.cn/szbzw/html/2024-10/16/content_51700.htm) supplies a classifier–place–one construction for a patch of grassland. [Another prose example](https://www.guangximinzubao.cn/szbzw/html/2023-11/22/content_48645.htm) directly uses `benq dieg` for a bounded area. Applying that spatial expression to a canvas region remains a technical extension. [Yang Yuluan's Zhuang/Mandarin comparison](https://www.guangximinzubao.cn/szbzw/html/2018-05/23/content_25838.htm), section four, explicitly illustrates postverbal `gonq` meaning first.

The indexed text of the [2017 government report in People's Daily Zhuang](https://sawcuengh.people.com.cn/158003/15656243.html) uses `ceiqnoix` before a verb and a one-person minimum. The primary text was available through search extraction; direct opening during review returned HTTP 502. The [1984 dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) corroborates at least/minimum and the general individual-object classifier; OCR is supporting evidence, not sole proof. [Published depicted-figure prose](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm) supports the image noun.

Confidence is medium-high for the area prompts and medium for the minimum-image instruction. The exact image-classifier collocation and complete software phrases are not independently attested. Their technical idiomaticity remains an editorial limitation; native-speaker certification is not claimed.

## Consumer and targeted checks

- `ClassicPaintActivity` displays the area prompt in the selection-dimensions slot when no selection exists. The other area instruction handles unsuccessful cut, copy, delete and crop-selection commands.
- `PaintDocument` returns false for those operations when their required selection is absent. Rendering/allocation failures remain distinct exceptions, not evidence of this prerequisite condition.
- `ImageCropDialog` rejects an empty selected set before applying or dismissing. `ImageAssembly.crop(ids, margins)` likewise rejects empty IDs before change. Neither guard requires exactly one image.
- 61 host tests pass: translations, translation boundaries, priority accounting and current localization contracts. All 171 offered catalogues and the priority manifest pass structural checks. Six English/Zhuang Java resource-render checks pass; these strings have no format arguments.
- Missing-only integration preserves attributes, formatting, newlines, escaping, earlier values and XML prefix bytes. Temporary Kotlin source checks cover the consumer routes above; they are not Android execution.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 250 other non-tree entries are retained. Publication uses an expected parent and non-force branch lease, with full-tree and changed-file verification.

Zhuang direct presence becomes 159 resources: P0 68/94, P1 91/249, P2 0/305 and P3 0/71. Global P1 gaps become 1,400; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed selection/crop operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
