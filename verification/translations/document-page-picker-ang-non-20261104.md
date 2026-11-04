# Document page picker: Old English and Old Norse

Base commit: 1ba12f11518182e53e0a647adec455da50f1b92f.

Adds 12 previously absent page-picker strings to each offered `ang` (Ænglisc) and `non` (Norrœna) catalogue. Independent semantic review accepted all 24, including the Old English `cyre` refinement. The batch covers selection, previous/next navigation, opening, preview status, page numbering/dimensions and an invalidated PDF-page selection. Technical vocabulary follows the existing catalogues; modern compounds are adaptations, not claimed historical computing terminology.

The instructions retain the page-range lower bound of 1, one-of-total numbering, dimensions and pixel units, a selected-page preview, a pending loading label, unavailable-preview reason, total page count and the choice of one page to edit as an image. The stale-selection warning says the selection is no longer valid and asks for another page from this document. It does not assert file damage, deletion or successful loading.

Validation passed:
- Exact English and target base file Git identities; both offered picker entries; XML parsing and duplicate-name checks; exactly 12 additions per locale; all 343 previous entries, attributes and surrounding bytes unchanged.
- Android escaping and formatting; typed placeholder sequences; escaped newline parity; literal PDF identifiers; source attributes and numerical lower bound preserved.
- 78 host tests: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery.
- Structural catalogue validation passed for all 171 offered options. All 1,276 materialized tracked base files matched their Git blob identities and executable modes. The 156 unmaterialized research/verification documents are retained unchanged in the publication tree and were not needed by these checks.

Priority coverage is direct key presence, not a whole-catalogue quality rating. Each locale changes from P2 0/305 to 12/305, leaving 293 P2 keys absent. P0 remains 94/94, P1 249/249, and P3 0/71. The priority manifest is unchanged.

Terminology follows current page, preview, pixels, numbering, loading and editing resources. Supplemental lexical checks: [Zoëga, aptr-fœrsla](https://norroen.info/dct/zoega/a.html) supports the noun family used for the authored Old Norse loading compound; the [Bosworth-Toller supplement](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/d0122.html) marks ceosung for deletion, so the Old English warning uses cyre, whose plural cyra already appears in the catalogue. These are lexical witnesses, not full-sentence historical attestations.

Limits: no historical-language specialist certification, whole-catalogue linguistic acceptance, Android build, device/rendering check or CI result is claimed. Canonical Android resources own current wording; this evidence is not a wording freeze.
