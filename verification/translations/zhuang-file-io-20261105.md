# Zhuang file locations and readable image data

Base: `d79d98e34ebd8313bb148e112c3e67a3d6d5fd27` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 strings: choosing a location, retrying with another file/location, and no readable image data. All 147 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent review and evidence

Independent linguistic and current-consumer review accepted the final compositions at moderate confidence. The location label follows the concise English wording. The retry instruction explicitly offers another file or another place and asks to repeat the failed operation, without promising success. The image-data notice denies the availability of readable data; it does not assert that no bytes exist or blame a provider.

The review retained the original patient-centred readable construction after checking [Sybesma's postverbal-ndaej study](https://www.researchgate.net/publication/300848712_6_Zhuang_A_Tai_language_with_some_Sinitic_characteristics_Postverbal_%27can%27_in_Zhuang_Cantonese_Vietnamese_and_Lao), section 3.3.2: a theme followed by a verb and ndaej can express an -able property. A tentative variant naming AN Paint as the reader was dropped because it added an unnecessary agentive clause. [Sio and Sybesma, section 6.1](https://www.academia.edu/214062/The_Nominal_Phrase_in_Northern_Zhuang_A_descriptive_study_2008_), supports postnominal modifiers without a linker.

[Teaching prose](https://www.guangximinzubao.cn/szbzw/html/2016-10/12/content_19085.htm) supports another place and a negative existential restricted by a following verb. [The terminology commission's list](https://www.guangximinzubao.cn/sy/jxzw/412847.html), entry 102, and [machine-data prose](https://www.guangximinzubao.cn/zw/s/645936.html) corroborate the data noun. [MediaWiki](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/za.json) corroborates file/read vocabulary. Published [instrumental-action prose](https://www.guangximinzubao.cn/zw/f_282584/646040.html) and [repeated-action prose](https://www.guangximinzubao.cn/szbzw/page/21/2024-02/07/06/2024020706_pdf.pdf) support the retry composition. Reading image data is a technical extension; none of these sources attests the complete new UI sentences. No native-speaker certification is claimed.

## Consumer and targeted checks

- `SaveOptionsDialog` binds the location button in save/export/share flows and validates the filename before confirming its `SaveRequest`.
- `ClassicPaintActivity.ioFailed()` uses the retry instruction only when the exception message is null, preserving actual diagnostic details otherwise.
- `AssemblyActivity` uses no-readable-data for a null input stream. `IcoCodec` and `DibCodec` use it for their specific invalid-image parser exceptions. Unsupported colour remains a distinct diagnostic; generic I/O errors are not relabelled by those parser wrappers.
- 61 host tests pass: translations, translation boundaries, priority accounting and current localization contracts. All 171 offered catalogues and the priority manifest pass structural checks. Six English/Zhuang Java resource-render checks pass. These strings have no format arguments.
- Missing-only integration preserves attributes, formatting, newlines, escaping, all earlier values and XML prefix bytes. Temporary Kotlin source checks cover the consumer routes above; they do not execute Android flows.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 247 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full tree and changed-file verification.

Zhuang direct presence becomes 150 resources: P0 67/94, P1 83/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,411 to 1,408; P0/P2/P3 remain 164/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed provider/dialog operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
