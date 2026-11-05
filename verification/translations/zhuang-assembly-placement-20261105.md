# Zhuang assembly selection and placement

Base: `e4ec83e9d61e75a2f9dd44f41c5ab58f890e9d20` on `review/nv-bottom-2038-20261103`.

Adds two missing P1 strings: the instruction to tap an image first and the fallback image-placement error. All 168 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent linguistic and current-consumer review retained both compositions. The selection prompt retains an image as the object and first as a prerequisite. The placement notice uses the established theme-first negative-potential construction and does not add a cause, rollback assurance or claim about saved files.

Digital interaction vocabulary is supported by indexed text of the [23 October 2024 newspaper PDF](https://www.guangximinzubao.cn/szbzw/page/21/2024-10/23/03/2024102303_pdf.pdf), whose parallel Chinese describes opening network settings. The PDF was not directly rendered or visually aligned; this corroborates click/tap interaction, not a touchscreen-specific gesture distinction. [Yang Yuluan's grammatical comparison](https://www.guangximinzubao.cn/szbzw/html/2018-05/23/content_25838.htm), section 4, supports postverbal first. The reviewer obtained indexed text; the publication check also retrieved the complete article body.

[Published prose](https://www.guangximinzubao.cn/zw/f_282584/646040.html), paragraph 27, uses the placement verb for putting bowls into a cupboard. [Sybesma's postverbal-potential study](https://www.researchgate.net/publication/300848712_6_Zhuang_A_Tai_language_with_some_Sinitic_characteristics_Postverbal_%27can%27_in_Zhuang_Cantonese_Vietnamese_and_Lao), section 3.3.2, supports a theme followed by a verb and the negative potential expression. Image placement is a technical extension of this vocabulary. The exact UI sentences and image-classifier combination are compositional judgments, not independently attested software terms. Overall wording confidence is moderate; no native-speaker certification is claimed.

## Consumer and targeted checks

- `AssemblyActivity` uses the tap-first instruction when either unplace or remove is requested with a null selected image. Tray clicks and canvas selection update that selection. The message is a prerequisite prompt, not an instruction to choose the first item in an ordered list.
- The board's error handler uses the placement fallback only when the exception message is null; a non-null message is preserved, including an empty string.
- `AssemblyCanvas.dropImage()` catches exceptions across placement, subsequent selection clearing and status reporting. This message does not establish the exact failing stage or that placement never occurred. No failure-atomicity or rollback guarantee is inferred.
- 61 host tests pass: translations, translation boundaries, priority accounting and current localization contracts. All 171 offered catalogues and the priority manifest pass structural checks. Four English/Zhuang Java resource-render checks pass; these strings have no format arguments.
- Missing-only integration preserves attributes, formatting, newlines, escaping, all earlier values and XML prefix bytes. Temporary Kotlin source checks identify all consumers of these two keys and verify selection and exception-message routing. They do not execute Android touch, toast or placement behavior.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 254 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full tree and changed-file verification.

Zhuang direct presence becomes 170 resources: P0 68/94, P1 102/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,391 to 1,389; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed assembly operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
