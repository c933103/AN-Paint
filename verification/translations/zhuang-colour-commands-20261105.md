# Zhuang colour controls and validation

Base: `e8685e625e7c4cadd563408384564c843386e38a` on `review/nv-bottom-2038-20261103`.

Adds three missing P1 resources: `ui_swap23`, `ui_selected_colour23` and `ui_invalid_colour`. All 180 earlier typed resources and their attributes remain unchanged. Only Zhuang XML and this report change.

## Wording review and evidence

Independent review retained the exchange-colours and unusable-colour compositions. Further grammar checking corrected the selected-colour label by adding a classifier before the noun; the final form was independently re-reviewed. It describes the current selected colour, without claiming it has been saved or permanently applied. Confidence is medium-high for the exchange command and moderate for the two other compositions. Exact UI collocations and device idiomaticity remain unverified.

- The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports exchange/mutual exchange (`doxvuenh`, D.htm 75/110), colour (`saek`, S.htm 6/52) and choose (`senj`, S.htm 24/52). The mirror explicitly warns of incomplete proofreading.
- [Guangxi Minzu Bao, 15 May 2019, page 8](https://www.guangximinzubao.cn/szbzw/page/21/2019-05/15/08/2019051508_pdf.pdf) has exchange followed by an object, herb seeds, in its market account. Indexed passage text was readable; direct PDF retrieval timed out. This supports the exchange construction, not an attestation of the exact colour command.
- [Sio and Sybesma, The Nominal Phrase in Northern Zhuang](https://www.academia.edu/214062/The_Nominal_Phrase_in_Northern_Zhuang_A_descriptive_study_2008_), sections 3.2, 5 and 6.1, supports the mass/abstract classifier, noun–modifier–demonstrative order and the distinction between proximal classifierless phrases and the distal demonstrative used here. The classifier was retained rather than silently extrapolating the proximal exception. [Published prose about a woven design](https://www.guangximinzubao.cn/szbzw/html/2025-08/27/content_54381.htm), paragraph 27, directly corroborates the classifier–colour combination.
- [Sybesma's postverbal-can study](https://www.researchgate.net/publication/300848712_6_Zhuang_A_Tai_language_with_some_Sinitic_characteristics_Postverbal_%27can%27_in_Zhuang_Cantonese_Vietnamese_and_Lao), section 3.3.2, directly gives the underlying-object–verb construction and its negative unusable counterpart. The invalid-value label is a functional paraphrase, not a claim about an aesthetic defect, a particular input format or a specific numeric range.

## Consumers and checks

- `ClassicPaintActivity` exchanges `document.foreground` and `document.background`, then updates the colour controls. This is not image inversion or palette reset. The complete swap label reaches visible text, accessibility description and tooltip.
- `AdvancedColourDialog` labels the sample drawn from live `value.colour`. Synchronization refreshes the sample and can invoke a preview callback that temporarily updates document foreground/background. Acceptance is a separate action; dismissal without acceptance restores the original preview. The caption is not a commit confirmation, and the preview is not claimed to be visually unapplied.
- The generic invalid-colour error is assigned to the affected field on `IllegalArgumentException` in `readFields`. Malformed hex input and invalid numeric ranges have separate diagnostics. Acceptance is blocked while field errors exist. No claim is made that this generic branch handles every invalid entry.
- 64 host tests pass: translations, translation boundaries, priority accounting, current localization contracts, locale-tooltip source wiring and numeric-input source coverage. All 171 offered catalogues and the priority manifest pass structural validation. Six English/Zhuang Java render checks pass; the new strings have no format arguments.
- Missing-only integration preserves earlier values, attributes, placeholders, newlines, literal requirements, escaping and XML prefix bytes. Temporary code-token-aware Kotlin checks verify all three consumer bindings and the conditions above. These checks are structural, not Android interaction tests.
- All 1,252 materialized files match the fresh base tree's Git hashes and executable modes; 259 other non-tree entries are retained. Publication uses the expected parent and a non-force branch lease, followed by full tree and changed-file verification.

Zhuang direct presence becomes 183 resources: P0 68/94, P1 115/249, P2 0/305 and P3 0/71. Global P1 gaps fall from 1,379 to 1,376; P0/P2/P3 remain 163/30,129/7,481. The 46 options containing all tracked resources remain unchanged. Presence is not linguistic completeness or runtime fallback coverage.

No Android build/AAPT, installed colour-input/swap/cancel operation, device/layout/accessibility test, merge or release is claimed. No implementation or other locales change. Canonical XML owns wording; no permanent sentence mirror or per-batch test package is added.
