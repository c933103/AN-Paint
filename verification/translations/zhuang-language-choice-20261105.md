# Zhuang application and device-language choices

Base: `fc4f315245486d6be73ed41e0c1a95273992dfa6` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 resources: the application-language title, the current-language row with its existing single string argument, and the choice to use Android's language. All 136 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Independent wording and consumer review

All three final values received independent linguistic and current-consumer review. The short labels use the application name as the language's modifier. The device-default label is an authored relative construction meaning use the language Android uses. It does not instruct the user to change Android settings. The relative construction has greater idiomatic uncertainty than the two short labels, but review found no demonstrated correction to make. These are source-supported editorial decisions, not native-speaker certification or attested whole software sentences.

[MediaWiki's Zhuang language label](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/za.json) corroborates the language noun in a selector. A [grammatical discussion](https://www.guangximinzubao.cn/szbzw/html/2019-11/06/content_33679.htm) supports head-before-possessor/modifier order. [Primary newspaper prose](https://www.guangximinzubao.cn/szbzw/html/2015-12/02/content_15642.htm) uses the language-use construction, and [Hoenz Fwen's prose](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24064.htm) supports a noun followed by an explicit relative-clause actor, predicate and closing demonstrative. The latter example also has an initial classifier; it does not independently settle classifier preference in this particular new UI label. All sources were reread for this batch; song lyrics were not used.

Current `AppLanguage.kt` routes were checked:

- The settings row formats either the chosen language name/tag or the device-default label in the retained `%1$s` slot.
- Device language comes from `LocaleManager.systemLocales` on newer Android or `Resources.getSystem` earlier, not the app-language override. Choosing the empty default option clears the application's override without changing the system language.
- `deviceDefaultLabel` deliberately resolves in the device locale. Selecting Zhuang for the app alone does not necessarily display the new Zhuang default-option wording.
- The picker sets the application-language title but installs the translation-note view as its custom title. That note and the settings heading remain English fallback. This batch does not complete the settings UI or claim that its visible custom heading is now translated.

## Targeted verification

- 76 affected host tests pass: translations, translation boundaries, priority accounting, translation-note/picker contracts, production source-text generation and exact resource routing. These include five routing tests and 71 other tests, not the full repository suite.
- All 171 offered catalogues and the priority manifest pass structural validation. Six English/Zhuang Java template render checks pass, including exact argument insertion with percent signs, angle brackets, ampersand and quotes.
- Three unique missing-only additions preserve source attributes, positional formatting and Android/XML escaping. All earlier resource values and XML prefix bytes are retained.
- All 1,252 materialized base files match the freshly fetched remote tree's Git hashes and executable modes. The other 244 non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full remote-tree and changed-file verification.

Zhuang direct presence becomes P0 66/94, P1 73/249, P2 0/305 and P3 0/71: 139 typed resources. Global P1 gaps across 171 offered options decrease from 1,421 to 1,418; other tiers and the 46 options containing all tracked resources remain unchanged. Direct presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed language-switching test, device/accessibility/layout test, merge or release is claimed. No implementation, locale list, permission, font, English-resource or other-locale changes were made. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
