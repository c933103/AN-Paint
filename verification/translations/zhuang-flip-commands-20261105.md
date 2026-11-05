# Zhuang image-flip commands, 5 November 2026

## Scope and wording

The live branch was reconciled at parent `0a9f923948a4a516191f7aad5e64ca7c86c14161`, tree `03fc638ca05c9c601b1da66456aea50e861d23d5`; no operation was pending. This fills P1 `ui_flip_horizontal` and `ui_flip_vertical`. All 270 preceding typed resources remain unchanged; the total is 272. Only canonical XML and this report change.

Independent wording/context review preferred the flip/reverse verb `fan`, with explicit left/right and top/bottom direction pairs. It rejected the proposed `doxvuenh` swap/exchange wording: exchanging two intact halves would not necessarily reverse internal pixel order, whereas these commands reflect the full image. The separate rotation vocabulary is not reused.

Sources:
- [Sawloih Cuengh-Gun dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html), F10, supports `fan` as flip/turn over and reverse. D75 supports the distinct exchange meaning of `doxvuenh`; B15–16 supports the four directional components. B9 gives `baenq` rotation, which is not substituted for reflection. This is an OCR transcription, not official software terminology.
- [Guangxi Minzu Bao, “Riep Baengzndaij,” 10 September 2025](https://www.guangximinzubao.cn/szbzw/html/2025-09/10/content_54490.htm), paragraph describing a warmed leaf compress, uses `youh fan baez ndeu`, turning it again. This supports ordinary physical turning, not image-reflection axes or the complete UI phrases.

Confidence is **moderate** in the descriptive composition, stronger in the lexical operation/direction distinction. Whether users find the coordinated direction pairs idiomatic remains unverified. These are reasoned translations, not fully validated native software terminology. No native-human certification or complete-language acceptance is claimed. Canonical XML owns the wording.

## Actual consumers

`ClassicPaintActivity` has one direct binding for each command. Horizontal flip applies `Matrix.setScale(-1f,1f)`; vertical flip applies `setScale(1f,-1f)`. Thus the horizontal operation reverses the x direction only, while the vertical operation reverses y only. These are full-image reflections, not exchanges of two halves, foreground/background swaps or 180-degree rotation. The separate rotation command remains unchanged.

The activity first applies pending work. `PaintDocument.transform` checks memory, finishes the selection, transforms the entire bitmap, replaces it as an undoable edit and performs the existing temporary-bitmap cleanup. A selected/floating object is therefore committed before transforming the whole document; this is not a selection-only flip. No matrix, bitmap, selection, memory or history implementation changes.

## Verification

- All 171 offered-option catalogue checks and the importance manifest passed. Existing nodes, source attributes, ordered arguments, numerals, literal tokens, newline escapes and XML escaping are preserved.
- `python -m unittest -v test_translations test_translation_boundaries test_string_importance test_current_localization_contracts`: **61 tests passed in 13.202 seconds**.
- Four host Java XML-to-string cases check no-argument labels without added ellipses or newlines. This is not Android resource compilation.
- Temporary token-aware Kotlin checks verify both label bindings and exact negative-unit matrix axes, separate rotation, pending-work/selection sequencing, whole-bitmap transformation, undo checkpoint and cleanup. They do not execute Android matrix rendering.
- Base snapshot verification matched Git blobs and executable modes for **1,286 materialized files**, retaining **269** unmaterialized entries. Publication checks the complete path/mode/type/blob overlay, expected-parent non-force lease and exact remote bytes.

Inspected, not run:
- `ClassicWorkspaceTest.paletteForegroundBackgroundAndImageTransformMenusWork`: a horizontal-flip pixel relocation and undo, alongside other controls.
- `RegionalPersianJapaneseFrenchWordingTest.regionalFlipUndoAndAirbrushPerformTheirNamedOperations`: a 4×3 all-pixel vertical reflection and undo under `fa-IR`, not Zhuang layout acceptance.

No permanent per-edit wording mirror or test package is added. Zhuang presence is P0 **69/94**, P1 **149/249**, P2 **54/305**, P3 **0/71**. Across 171 options, missing resources are P0 **162**, P1 **1,342**, P2 **30,075**, P3 **7,481**; 46 options have complete presence. Scope remains 59 scoped catalogues and 112 outside-scope catalogues with explicit English fallback. Presence is not fluency or runtime acceptance.

Android SDK/Kotlin compiler are unavailable here. Android compilation, Robolectric, reflection/undo behavior, TalkBack and label layout were not executed. Exact-head Actions state is checked after publication and reported separately; this review branch does not normally trigger CI. No merge, release or CI-pass claim is made.
