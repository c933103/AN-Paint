# Zhuang crop-input amounts

Base: `a9ad3129cc7d381a21c3c100a928e9057ac385a9` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 strings: an amount for every crop edge, all four amounts, and the nonnegative-amount constraint. All 165 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent linguistic and current-consumer review retained all three compositions at moderate confidence. The validation text says zero or a positive number, preserving zero-or-greater without implying positive integers. The two completeness prompts distinguish every side from explicitly all four sides.

The independent reviewer directly checked the [1984 Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): zero, number/amount, positive number, every, complete, write, cut and side have the intended lexical senses. Direct [zero](https://en.wiktionary.org/wiki/lingz#Zhuang) and [number/quantity](https://en.wiktionary.org/wiki/soq#Zhuang) entries provide additional lexical support. Mathematical positive number remains distinct from integer.

The [language commission's eighth terminology announcement](https://www.guangximinzubao.cn/sy/jxzw/390966.html), entry 161, uses `gij soq` followed by a clause describing a quantity. [Published translation prose](https://www.guangximinzubao.cn/szbzw/html/2025-09/10/content_54492.htm) supports controlled cutting and numbered sides; [another newspaper article](https://www.guangximinzubao.cn/szbzw/html/2024-10/16/content_51700.htm) supports edge/side vocabulary. These sources support components and construction, not the exact new UI sentences or established software terminology. In particular, the composed trim-amount expression and complete-input wording retain idiomaticity uncertainty. No native-speaker certification is claimed. A search hit criticizing an awkward broadcast translation was not used as positive sentence evidence.

## Consumer and targeted checks

- `ImageCropDialog` creates four fields in left/top/right/bottom order. `margins()` parses every field; any unparseable entry returns null. `refresh()` uses the every-edge prompt, while submission uses the all-four prompt. These notices cover invalid input as well as empty fields.
- Submission obtains all selected crop rectangles before calling `apply`. Preview and submission display their caught diagnostic in the status view; this source observation is not an executed crop or failure-atomicity test.
- `CropMargins.rect()` first requires every amount to be finite and nonnegative. Zero is permitted. A separate guard checks each amount against its image extent and requires integral pixel-unit amounts; fractional percentages are allowed. Another separate guard rejects a remaining rectangle with nonpositive width or height. The new sign-check wording does not promise that all nonnegative amounts produce admissible crops.
- 62 host tests pass: translations, translation boundaries, priority accounting, current localization contracts and numeric-entry source coverage. All 171 offered catalogues and the priority manifest pass structural checks. Six English/Zhuang Java resource-render checks pass; these strings have no format arguments.
- Missing-only integration preserves attributes, formatting, newlines, escaping, all earlier values and XML prefix bytes. Temporary Kotlin source checks identify every consumer of the three keys and verify the guards above. They do not execute Android input or dialogs.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 253 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full tree and changed-file verification.

Zhuang direct presence becomes 168 resources: P0 68/94, P1 100/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,394 to 1,391; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed crop operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
