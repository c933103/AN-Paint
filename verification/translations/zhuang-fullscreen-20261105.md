# Zhuang fullscreen viewing command, 5 November 2026

## Scope and language review

The live review branch was reconciled at parent `052d668b9acab38127efa8cccef15a38fdaf4c9a`, tree `83e1bced380ebbc7462800d5fc88a636d9f9b8d1`. No write was pending or uncertain. This fills missing P2 `ui_fullscreen33`. All 283 preceding typed resources remain unchanged; the total is 284. Only canonical XML and this report change.

Independent review recommended the composition “whole screen”. It names the viewing mode without suggesting that image pixels are enlarged or the document dimensions are changed.

Evidence:

- [1984 Sawloih Cuengh-Gun dictionary transcription](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), retrieved by the reviewer, defines `daengx` as all/whole and supplies examples placing it before a noun. The associated dialect annotation applies to an alternative form, not to `daengx` itself. The transcription warns that proofreading was incomplete.
- [People's Daily Zhuang homepage](https://sawcuengh.people.com.cn/), retrieved as indexed primary-source text, uses `dennauj bingzmu` in computer-screen resolution advice, supporting `bingzmu` as screen. Direct opening returned HTTP 502. This is indexed-text evidence, not a successful fresh full-page read.

Confidence is **moderate**. Component meanings and order are supported, but the exact fullscreen-command phrase was not independently attested. No established technical-term status or native-speaker certification is claimed. Canonical Android XML owns current wording.

## Actual consumer

The View command in `ClassicPaintActivity` takes the complete resource as its command title and toggles the existing fullscreen state. Command updates assign the complete title to text and accessibility description.

`syncFullscreen` hides editor chrome while retaining the workspace overlay, hides the side/vertical rails, and installs a Show controls exit button. It removes an existing exit button before adding the current one. Show controls and Back both exit the mode. The method sets Android's fullscreen flag and restores the visible flag on exit; it does not explicitly hide the navigation bar, so “fullscreen” must not be reported as a guarantee that every system bar disappears on every device.

The synchronization method changes viewing controls, not document pixel dimensions. No fullscreen, image, viewport or input implementation changes. The retained exit control is intentional; this is a mode name, not a promise that the workspace has no controls at all.

## Verification

The previous temporary checkout was absent in this execution workspace. Required files were reconstructed from matching local Git blobs and exact-head repository reads, then checked against the current complete tree before testing. No older checkout was accepted as equivalent merely by directory name or timestamp.

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 12.588 seconds**.
- Two host Java XML-to-string cases check nonempty English/Zhuang labels and unchanged no-argument formatting. These are not Android resource compilation.
- Temporary token-aware Kotlin checks verify the sole resource binding, full command title assignment, state toggle, chrome visibility, exit-button replacement, Show controls/Back exits and the fullscreen flag. They also check that the synchronization method contains no document resize or explicit navigation-bar-hiding call. These are static checks, not Android execution.
- Base snapshot verification matched Git blobs and executable modes for **1,276 materialized files**, retaining **288** unmaterialized entries. All required catalogue/check files and affected application/test sources were materialized. Publication verifies the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected but not run: `ResponsiveToolboxTest.landscapeSideTabsRemainVisibleAndFullscreenReturnsTheirSpace` enters the mode, checks the vertical ribbon is hidden and the canvas fills root width, then clicks Show controls and checks the ribbon and reduced canvas width return. It does not establish this Zhuang label's fit, system navigation-bar behavior or the Back path. No permanent per-edit wording mirror or test package is added.

Zhuang presence is P0 **69/94**, P1 **154/249**, P2 **61/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,337**, P2 **30,068**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, system bars, repeated toggles, Back, viewport behavior, TalkBack and label layout were not executed. Exact-head Actions state is checked after publication and reported separately. No merge, release or CI-pass claim is made.
