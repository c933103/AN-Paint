# Zhuang: blocked file picker and acknowledgment

Date: 2026-11-05 (UTC). Base: `94fd608d5d408b093107636191d5cbc857b8ef2d`, tree `52fb32c6718527fa3e87293c7ae124764b894a46`.

## Change and independent review

Added P1 `ui_android_blocked_the_file_picker` and `ui_ok` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 213 previous typed resources remain unchanged. Canonical XML owns the wording.

Independent review accepted both revised entries. The picker notice explicitly names a file-selection tool: Android does not allow opening that tool, followed by the complete diagnostic argument. Adding the tool noun resolved the initial ambiguity between a selection operation and its interface. This also fits the create-document destination role without asserting that an existing file is being opened, an app is missing or a file is corrupt. The acknowledgment uses the contextually supported concluding/agreement term, rather than a generic adjective meaning good. Confidence is narrower for idiomatic software terminology: the picker compound is a supported composition, not an independently attested standardized term. Exact sentence attestation and native-human approval are not gates or claimed certifications.

Sources directly checked:
- [Sawloih Cuengh-Gun OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html): `hai`, open/start (H.htm 15/45); `hawj`, permission/allow (H.htm 22/45), with a negative-permission example also in the Sawndip appendix; `hongdawz`, general tool and agricultural tool (H.htm 38/45); `senj`, choose (S.htm 24/52); `vwnzgen`, document/file (V.htm 19/19). The OCR warns of incomplete proofreading.
- [Zhuang Wiktionary PDF-file page](https://za.wiktionary.org/wiki/File%3AIntroduction_to_Wikipedia_and_its_principles.pdf): `Hongdawz bonjfaenh` in the personal-tools section and `Vwnzgen` on the file tab corroborate digital-interface use. This is community evidence, not normative terminology; surrounding text includes Chinese fallback.
- [Guangxi Minzu Bao, 20 June 2018](https://www.guangximinzubao.cn/szbzw/html/2018-06/20/content_26157.htm), section VII, example 23, by 覃海恋 of the China Ethnic Languages Translation Centre: `ndaej` is explicitly discussed for concluding acknowledgment. This is stronger contextual evidence than a loose song-title gloss of `ndei` as “okay”; it does not imply that the latter is universally incorrect.

## Actual consumer boundaries

`ClassicPaintActivity.launchPicker` and `AssemblyActivity.launchPicker` use the warning for a SecurityException from their primary picker launch. Their callers include open/import and create-document save destinations. Both pass the whole nullable exception message; the classic editor also clears `afterSave`. The separate ActivityNotFoundException branches keep their missing-picker instructions. A SecurityException thrown inside the nested ACTION_GET_CONTENT fallback is not handled by the sibling primary SecurityException catch, so this report does not claim universal fallback coverage or alter that existing boundary.

`LegacyImageCreditsActivity` uses the warning for a SecurityException while launching a text-export create-document picker. Its exception handler clears `pendingExportToken` and displays inline status. Unlike the two main picker consumers, it substitutes `ui_could_not_complete_the_operation` when the exception message is null.

`ui_ok` has two actual bindings: the classic editor and assembly message dialogs. Both use a null positive-button click listener and lifecycle gates. The label acknowledges/dismisses a message; it is not save, retry, grant-access or destructive-action confirmation. The legacy-credit inline status does not use this button.

`UiText` passes nullable arguments unchanged to `LocaleText.resolve`. The formatter treats a supplied null as a valid `%s` value, rendering “null”, not an omitted argument. This resource-only change neither rewrites diagnostics nor changes null handling. Diagnostic text containing format-like sequences is data, not a second template.

## Verification

- Fresh remote head/tree reconciled with the preceding verified publication. All **1,255 materialized files** matched base Git hashes and executable modes; **269 unmaterialized leaves** remain retained, for 1,524 base leaves.
- All 213 original nodes, attributes and prefix bytes are preserved; two missing scalars are appended. XML/Android escaping, source attributes, ordered typed `%1$s`, numerals, newlines and required literal tokens pass. New XML Git blob: `3b8af8db3a3dd7a44badc8a81119873317a20b31`.
- All **171 offered catalogues** and the priority manifest pass structural checks.
- **61 host tests passed** in 9.595 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- **18 host Java formatter/literal cases passed** across English and Zhuang: null, empty, ordinary, percent-like, Unicode, multiline and 4,096-character diagnostics, each catalogue's actual operation-error fallback, plus the acknowledgment label. Full diagnostic insertion is preserved.
- Targeted token-aware source checks passed for all five bindings, primary security-handler arguments, legacy fallback and pending-token clearing, both null button listeners and lifecycle gates, and nullable argument forwarding to the formatter. These are static checks, not executed Kotlin or Android flows. Existing legacy-credit JVM cases cover security errors with a message and with null; inspected but not run here.

Zhuang now has **215 typed resources**: P0 **69/94**, P1 **132/249**, P2 **14/305**, P3 **0/71**. Global missing-entry counts across 171 options: P0 162, P1 1,359, P2 30,115, P3 7,481; 46 options have complete presence. These are presence counts, not linguistic acceptance or runtime coverage. Scope remains 59 scoped catalogues plus 112 outside-scope explicit-English-fallback catalogues.

## Limits

No Android build/AAPT, executed picker/dialog/export path, device layout, accessibility or font checks were run. Technical phrasing and actual display fit remain less certain than structural/formatter validity. No merge, release or deployment is claimed. Only canonical locale XML and this report are intended to change; temporary harnesses and sentence mirrors are not published.
