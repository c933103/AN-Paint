# Zhuang recent-colour slot descriptions, 5 November 2026

## Scope and wording review

The live review branch was reconciled at parent `66035dd43e1f62f0480a2ba594aef8c4b1555bee`, tree `3eae828048ab6ba7683096560f0aecfd0846c894`; no prior operation was pending. This fills the two missing P2 resources `ui_recent_colour_d_06x_tap_foreground_hold_background` and `ui_recent_colour_empty`. All 257 preceding typed resources remain unchanged; the total is 259. The populated description retains `%1$d`, the hash prefix and `%2$06X`; the empty description retains its separately formatted `%1$s` index. Only canonical XML and this report change.

Independent linguistic and actual-consumer review accepted the wording with **moderate confidence**. The shared category description means recently selected colour. Selection, rather than drawing use, is deliberate: a choice enters history even if the user never paints with it. The absence predicate in the empty entry does not describe transparent or white colour. Reusing the category name for an empty numbered entry is UI ellipsis; it does not assert that the slot was previously occupied.

The [Zhuang–Chinese dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), main M25, supports `mboengqneix` as recently; S24 supports `senj` as choose/select. Examples elsewhere in the same source attest the spaced `mbouj miz` absence construction. The [opening paragraph of Guangxi Minzu Bao, 18 May 2022](https://www.guangximinzubao.cn/szbzw/html/2022-05/18/content_43635.htm) independently demonstrates the temporal expression introducing a recent publication event. The dictionary is OCR, not an error-free scholarly edition.

The initial bare colour-plus-time proposal was refined to a post-nominal description with selection and the closing demonstrative. Independent review accepted this construction. The complete UI phrase is **compositional and not directly attested** in the checked sources. Existing relative descriptions in the catalogue support consistency, not independent linguistic proof. No native-user or established-terminology acceptance is claimed.

Tap/hold and front/back role wording retain the prior [standard-palette review's qualifications](zhuang-palette-gesture-20261105.md): the press sense is dictionary-supported, but the attested continued-press construction is figurative persistence, not literal finger pressure. It remains a contextual touchscreen translation with moderate confidence. This batch does not broaden that claim or invent a duration/pressure requirement. Canonical XML owns the complete current wording.

## Actual consumer

`ClassicPaintActivity.makePalette` creates four focusable recent-colour cells after the scrolling standard palette. Populated cells choose foreground on tap and background on long press, guarded against busy state and absent entries; long clicks are consumed. `refreshRecentColours` supplies the full state-specific description for every cell. Populated arguments are the one-based index and RGB masked to 24 bits. Empty entries are disabled and receive an already formatted index from the unchanged nontranslatable `ui_display_integer` resource in `values/display_numbers.xml`.

`RecentColours` stores at most four distinct opaque choices, newest first. Selecting a duplicate moves it to the front rather than adding another copy. Rebuilding the UI does not add a choice. The history is preference-backed, not a timed-expiry list. `setColour` updates the chosen document role, records the choice and refreshes the cells and indicator. No history, selection, persistence or callback implementation changes.

## Executed verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing-node identity, source attributes, ordered typed arguments, literal tokens and escaping were checked.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 9.650 seconds**.
- Host Java parsed the actual shared number resource plus English and integrated Zhuang XML and ran **58 cases**: 40 populated-slot compositions spanning all four indices and five RGB boundary/leading-zero values; eight empty-slot compositions using the shared integer formatter; four opaque index payloads; six missing/wrong-type argument failures. Full resources, argument order and uppercase six-digit RGB survive formatting. These are host XML/Java checks, not Android execution.
- The first temporary Java harness incorrectly expected the shared number resource inside `strings.xml`. It failed before host tests ran. The harness was corrected to load the actual `display_numbers.xml` resource, and the complete final checks above passed. No production-resource change was needed.
- Temporary token-aware source checks passed for complete state-specific binding, one-based indices, RGB masking, disabled empty cells, null/busy guards, tap/long-press role routing, deduplication, four-entry bound and preference writes.
- Base snapshot checks verified Git blob identity and executable mode for **1,277 materialized files**. **269** unmaterialized non-tree entries remain retained. Publication verifies the full resulting path/mode/type/blob overlay, a fresh expected-parent non-force lease and exact remote bytes.

Existing `NumericDisplayLocaleTest.recentColourIndicesLocalizeWhileHexAndStoredValuesStayInvariant` and `UnifiedEditorTest.fourRecentCellsKeepDistinctColoursAndStayAfterTheScrollablePalette` were inspected, not run. The former exercises populated/empty transitions and numeric routing in its existing locale set, which does not include Zhuang. No permanent per-edit wording mirror or test package is added.

## Coverage and limits

Zhuang presence is P0 **69/94**, P1 **138/249**, P2 **52/305**, P3 **0/71**. Global missing typed resources across 171 options are P0 **162**, P1 **1,353**, P2 **30,077**, P3 **7,481**; 46 options have complete resource presence. Scope remains 59 scoped catalogues plus 112 outside-scope catalogues with explicit English fallback. Presence does not establish fluency or runtime acceptance.

Android compilation, Robolectric, actual clicks/long presses, preference lifecycle, TalkBack comprehension and device layout were not executed. Exact-head Actions state is checked after publication and reported separately; review-branch pushes do not normally trigger CI. No merge, release, complete-language or CI-pass claim is made.
