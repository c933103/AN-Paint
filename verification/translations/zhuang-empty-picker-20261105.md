# Zhuang empty file-selection results

Base: `262572051838bf41279f4f36567e0a7e02fb70a0` on `review/nv-bottom-2038-20261103`.

Adds two missing P1 result notices: `ui_the_picker_returned_no_file_please_choose_the` and `ui_the_picker_returned_no_files`. All 190 previous typed resources and attributes remain unchanged. Only Zhuang XML and this report change.

## Wording and confidence

Both notices describe AN Paint not obtaining a file. The first also asks the user to choose the file again. Independent review found this a defensible plain-language description of absent file-selection or destination information at the actual consumers. It omits the literal component name “picker,” so explicit component attribution is reduced. It does not attribute a defect to a provider, say that the device contains no files, or claim that received file bytes failed to decode.

Confidence is moderate, not idiomatic verification. The acquisition verb's extension to a digital file is a composition, not an attested contemporary UI collocation. Its noun object and application subject support a result reading rather than a prohibition; the immediate result context supplies the event time. No “not yet” wording is added that would imply the operation remains pending. A bare file noun does not force a singular count in the empty multi-selection notice.

- [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), N.htm 14/72, gives the lexical acquisition sense of `ndaej` and an example of obtaining a flag, separate from its modal senses. A fruit-object example is in the separate sawndip/N.htm appendix, not the principal standard-language entry. The same source supports choose at S.htm 24/52, please/request at C.htm 53/78 and preverbal again at C.htm 17/78. The mirror warns of incomplete proofreading.
- [Sybesma, 2008, section 3.1](https://www.researchgate.net/publication/300848712_6_Zhuang_A_Tai_language_with_some_Sinitic_characteristics_Postverbal_%27can%27_in_Zhuang_Cantonese_Vietnamese_and_Lao) is important counterevidence: it observes that standalone acquisition usage principally concerns ranking, age and profits. This limits confidence in freely extending the verb to files, without establishing a categorical grammatical prohibition. Review retained the composition after reconciling this restriction with the dictionary, rather than presenting the broad gloss alone as proof of idiomaticity.
- The language commission's [fourth approved terminology list](https://www.guangximinzubao.cn/sy/gg/383691.html), item 11, corroborates an acquisition verb–noun construction in a benefits context only. [Guangxi Minzu Bao, 4 March 2015](https://www.guangximinzubao.cn/szbzw/html/2015-03/04/content_12240.htm), the paragraph beginning “Bouxdaeuz baijcauhfanj,” corroborates the classifier–document-noun combination. Neither attests the complete software sentences. Both were directly readable.

## Consumers and verification

`ClassicPaintActivity.onActivityResult` delegates or defers to `handleActivityResult`. Unsuccessful results return before the missing-URI notice. After special-result branches, a null URI produces the complete resource message, clears `afterSave` and returns before I/O dispatch. The following routes include open, import, save, source export and recovery export, so this is not exclusively an import error or evidence that file bytes were obtained.

`AssemblyActivity` uses the other notice only for `ADD_IMAGES` with `RESULT_OK` and an empty URI list, before image import. It gathers ClipData entries or falls back to the single data URI. Assembly saving uses a separate branch. Both activity message helpers pass the whole resource to the dialog message.

- 61 host tests pass in 8.495 seconds: translations, translation boundaries, priority accounting and current localization contracts. All 171 offered catalogues and the priority manifest validate. Four English/Zhuang Java literal render checks pass.
- Missing-only XML checks preserve prior values, source attributes, typed ordered placeholders, newlines, literal requirements, Android escaping and prefix bytes. Temporary token-aware consumer checks verify the actual bindings, result guards, separate routes and whole-resource dialog delivery. They are structural checks, not executed Android activity-result or provider behavior.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 263 other non-tree entries are retained. Publication uses the expected parent and non-force branch lease, followed by full-tree and exact changed-file verification.

Zhuang direct presence is now 192 resources: P0 68/94, P1 124/249, P2 0/305 and P3 0/71. Global P1 gaps decrease from 1,369 to 1,367; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed picker/cancellation/provider behavior, device dialog layout/accessibility, exhaustive result-input robustness, merge or release is claimed. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
