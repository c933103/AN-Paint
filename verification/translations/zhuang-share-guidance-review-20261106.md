# Zhuang Save-and-share guidance and complete-value review

Date: 2026-11-06 UTC. Base `8a76c9ecd7aa4d1a9a312f7ad6ddbe2a321467bd`, tree `466ab917f8c25a3863e494f80c22e8e413a41e2d`.

## Change and review

Added missing P0 `ui_share_explanation34` to canonical `Paintroid/src/main/res/values-b+za/strings.xml`. All 316 preceding resource nodes, attributes and prefix bytes remain unchanged.

The guidance tells the user to save separately at their chosen location, then choose an application for sharing, while the ordinary Save destination remains unchanged. Independent review added `lingh` to the initial draft so that the separate-copy operation is explicit rather than merely “save as a file.” The final wording does not assert that the selected destination must be newly created, that output is pixel/byte-identical, or that the chooser or receiving application will succeed. `yonjgen` uses an attested software noun for application; `lingh rom` is a functional authored construction, not an attested complete UI command.

Independent complete-value review also retained four existing resources:
- `ui_save_and_share` and `ui_save_and_share_41edb4`: menu and dialog captions preserve Save-and-share meaning; the menu retains its ellipsis.
- `ui_share_saved_image`: chooser title identifies the image AN Paint has saved.
- `ui_the_image_was_saved_but_android_could_not`: contrasts completed file saving with inability to open sharing and preserves `%1$s` diagnostic detail. It does not claim that the working document was marked saved, or that a receiving application reported delivery failure.

Confidence is moderate for complete Zhuang wording and high for the static consumer interpretation. No native-speaker certification is claimed or imposed as a gate. These five values are the complete review cohort; other translated resources, fallback and release readiness remain separate obligations.

## Evidence and consumers

[Dictionary OCR](https://dokumen.pub/sawloih-cuengh-gun-ocr.html) supports `lingh` separately/additionally/again (L.htm 27/49), first/then/choose/change vocabulary and `faenyiengj` share (F.htm 5/29). The OCR warns of incomplete proofreading. [Modern software prose](https://www.guangximinzubao.cn/szbzw/html/2024-11/06/content_51822.htm), paragraph 29, attests `aen yonjgen` for software. [A translation discussion](https://www.guangximinzubao.cn/szbzw/html/2024-07/17/content_50661.htm) explicitly glosses `faenyiengj` as sharing in its terminology analysis. Both reviews directly retrieved the relevant text; an initial short extraction/find missed it and was not treated as evidence of absence. These sources support components and construction, not the entire new UI sentence.

The File-menu command calls `showSaveOptions(..., share=true, export=true)`. `SaveOptionsDialog` gives sharing precedence over the export explanation and displays the complete resource in both ordinary and vertical layouts. Sharing exposes all offered export formats, including derived outputs, which is why the explanation does not promise an identical full-image copy.

Confirmation selects a destination through `ACTION_CREATE_DOCUMENT`. `writeImage` encodes and finishes writing/closing the chosen output before attempting the share chooser. Because this route is exporting, it does not update `filename` or `savedTarget`, mark the drawing saved, or schedule ordinary-save autosave. The chosen output can overwrite an existing destination through the writer's `wt` mode; no claim of a guaranteed brand-new file is introduced.

Sharing passes the cached encoded file through FileProvider with a read grant, rather than necessarily passing the chosen destination URI. The chooser title identifies the saved image. The failure message catches preparation/chooser-launch exceptions after file writing; it does not observe later receiving-app delivery. Dialog cancellation and cancelled picker results clear the sharing flag. No application, destination or permission behavior changes.

## Verification

- Fresh review head reconciled with the previous verified publication. Develop remained `412aab0c604060fb66fbd2edc6bb05572d10b56d`; separate Navajo work untouched. All 1,590 base file contents and executable modes matched the reviewed checkout.
- One unique missing scalar added; source attributes, placeholders, literal/numeric/newline boundaries, escaping and previous values preserved. All 171 offered catalogues and the priority manifest pass structural checks. XML blob `a6118bec93bbb944e4083ed1e286a791c1241157`, 31,862 UTF-8 bytes.
- 61 host tests passed in 5.667 seconds: `test_translations`, `test_translation_boundaries`, `test_string_importance`, `test_current_localization_contracts`.
- 16 English/Zhuang host Java checks passed for the five static/error-detail resources, including percent, Unicode, empty and null diagnostic robustness values. They are XML-template checks, not Android resource execution.
- Temporary token-aware checks verified all six resource bindings, share/export flags, dialog explanation precedence, file-before-chooser ordering, preserved ordinary Save association, cached-file/read-grant sharing, separate save success/chooser failure and the quoted current `Rom` caption. `git diff --check` passed.
- `UnifiedEditorTest.jpegQualityIsChosenBeforeFilePickerAndSaveAndShareWritesTheFileFirst` was inspected, not run. It covers picker cancellation, real write-before-chooser and outgoing intent/data permissions. Related `DerivedExportStateTest` assertions cover retained ordinary Save associations for derived exports; that is related coverage, not execution of this Zhuang share route.

Zhuang has 317 typed resources: P0 76/94, P1 158/249, P2 80/305, P3 3/71. Global missing counts over 171 options are 155/1,333/30,049/7,478 for P0–P3; 46 options have complete presence. Presence is not linguistic acceptance or complete review.

Android SDK/Kotlin compiler are unavailable here. Android build/AAPT, actual file/picker/share operations, lifecycle, device layout, accessibility and glyph checks were not executed. No merge or release is claimed. Only canonical XML and this compact report change; no permanent wording mirror or per-edit test package is added. The conditional P0/P1 completion and all-translated-string review release plan remains in force.
