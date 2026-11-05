# Zhuang contextual-help entry points, 5 November 2026

## Scope and language review

The live review branch was reconciled at parent `b0c0482076018df1b2228e4b10066b22ceeb38dc`, tree `5c6969666751f8f5b9e34bd65db34e083ae66a20`. No write was pending or uncertain. This fills missing P3 `ui_how_to_use`, shared by five contextual-help entry points. All 284 preceding typed resources remain unchanged; the total is 285. Only canonical XML and this report change.

The working draft was corrected from verb-first order to “how + use” after checking published wording. [Guangxi Minzu Bao, 20 February 2013](https://www.guangximinzubao.cn/szbzw/html/2013-02/20/content_1178.htm), directly retrieved, gives the bilingual article title beginning `Baenzlawz Yungh` for “how to use” educational media. This is direct support for the construction and order, although the complete article title includes an object and is not a software button. The short UI label leaves its object implicit in the surrounding tool or application context.

Independent review confirmed this order and all five consumer bindings. The [Sawloih Cuengh-Gun dictionary](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), B8/Y29, supports the component words. Confidence is **high for the meaning and moderate-to-high for the short wording**. Native software usability and the visible fit of this exact label have not been established. Canonical Android XML owns current wording.

## Actual consumers

The resource is used in four places in `ClassicPaintActivity` and once in `AssemblyActivity`:

- Tool options open the selected tool's hint, with the existing cursor-mode-specific branch for pencil, brush, watercolor and eraser.
- The File command opens the general application help resource.
- The View command opens pixel-grid help.
- Cursor settings open the existing combined cursor instructions, tap hint and marker guidance.
- The assembly toolbar opens its existing image-assembly instructions.

The complete label is passed to the corresponding buttons or commands. Classic buttons/command updates also assign the label to accessibility descriptions. The assembly button receives it as visible text. Help contents, routes, controls and drawing state logic are unchanged. Translating the entry label does not claim that the help bodies are translated or complete in Zhuang.

## Verification

Work and tests used the available temporary filesystem because the main workspace filesystem is full. No unrelated files were removed, and no existing work was overwritten to create space.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 15.991 seconds**.
- Two host Java XML-to-string cases check nonempty English/Zhuang labels and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verify all five resource bindings, the cursor-specific tool branch, the general/grid/cursor/assembly help destinations and complete label assignment. These are static checks, not dialog execution.
- Base snapshot verification matched Git blobs and executable modes for **1,277 materialized files**, retaining **288** unmaterialized entries. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `FrenchAssemblyHelpTest.actualHelpToolbarDisplaysCompleteFrenchEntryAndReopens` opens and dismisses the assembly help twice and checks its body and unchanged empty assembly. `ResponsiveToolboxTest.pixelGridKeepsAShortCaptionAndExplainsItsThresholdInHelp` exercises the grid-help paths. These tests concern existing consumers and other wording; their inspection is not execution evidence for this Zhuang label or every help route. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **154/249**, P2 **61/305**, P3 **1/71**. Across 171 options, missing resources are P0 **162**, P1 **1,337**, P2 **30,068**, P3 **7,480**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, actual help dialogs, dismissal/reopening, TalkBack and label layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
