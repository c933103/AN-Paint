# Zhuang crop reset

Base: `f36e53befc62216cb1c040da1e7d375b9ff66963` on `review/nv-bottom-2038-20261103`.

Adds the missing P1 `ui_reset_crop` button. All 186 earlier typed resources and attributes remain unchanged. Only Zhuang XML and this report change.

## Wording and scope

Independent review recommends a descriptive “use the whole image again” label. It describes the resulting crop setting, not immediate application, selecting every batch image, or recovery of pixels absent from the source image. Confidence in the composition and UI idiomaticity is moderate; the complete button phrase is not attested in the sources.

- [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): again at C.htm 17/78, whole at D.htm 20/110 and use at Y.htm 29/31. The whole-quantity entry includes direct noun constructions. The mirror warns of incomplete proofreading.
- [Official terminology list, 3 September 2025](https://www.guangximinzubao.cn/szbzw/html/2025-09/03/content_54472.htm), entry 103, corroborates use/application in a digital-technology context.
- [Hoenz Fwen, 27 December 2017](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm), the paragraph beginning “De doq gangj,” corroborates the image term for depicted figures, with parallel Chinese prose. Both newspaper sources were directly readable; neither establishes the exact software phrase.

The proposed crop-boundary companion remains in English fallback. Review found that its draft did not clearly distinguish the retained rectangle from the cutting operation or removed margins. The actual guard permits equality at image boundaries and also requires positive width and height; it is not a strict-interior-only rule. No ambiguous companion is published merely to increase coverage.

## Consumer and checks

`ImageCropDialog` displays the whole selected resource. Reset sets the full reference-image rectangle, which yields four zero trim amounts in either pixel or percentage mode, and refreshes the preview. It does not apply, dismiss or change selected-image membership. Apply is separate, derives each selected image's rectangle using that image's own dimensions, and sends crop metadata to `ImageAssembly`. This is not a promise to undo a previously destructive raster crop.

- 62 host tests pass: translations, translation boundaries, priority accounting, current localization contracts and locale numeric-input source coverage. All 171 offered catalogues and the priority manifest pass validation. Two English/Zhuang Java literal render checks pass.
- Missing-only XML checks preserve prior values, attributes, placeholders, newlines, literal requirements, Android escaping and prefix bytes. Temporary token-aware source checks cover the sole reset binding, four-margin calculation, both unit modes, separate Apply and selected-image filtering. These are structural checks and arithmetic inspection, not executed Android behavior.
- All 1,252 materialized base files match fresh Git hashes and executable modes; 261 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full-tree and changed-file verification.

Zhuang direct presence is now 187 resources: P0 68/94, P1 119/249, P2 0/305 and P3 0/71. Global P1 gaps decrease from 1,373 to 1,372; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed reset/apply/cancel interaction, device layout/accessibility, merge or release is claimed. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
