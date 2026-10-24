# Amharic view controls: primary-source lexical draft

2026-10-24. Seven review candidates, not native-speaker acceptance or implementation approval. Research only: no production edit, build, CI, Work task, or remote publication. Inherited zoom-in/out labels are untouched. Static `ui_canvas_zoom` is excluded because the consumer replaces it with formatted `ui_canvas_zoom_771f84`; this packet does not claim live zoom accessibility coverage.

## Recommended review candidates

| English | Exact draft | Form / confidence | Basis and qualification |
|---|---|---|---|
| Fit | በመስኮቱ ልክ | Elliptical view-setting phrase; medium-high | Exact LibreOffice “Fit To Window” wording, MathCommands `.uno:FitInWindow`. Implies the window-sized view rather than changing the bitmap. Not an imperative equivalent to “resize.” |
| Fit entire canvas in view | የመሳያ ቦታውን በሙሉ አሳይ | Newly composed imperative; low-medium, HOLD for review | Literally intended as “show the whole drawing area.” LO attests Drawing → መሳያ and Android attests imperative አሳይ, but this full phrase and this rendering of canvas are NOT independently attested. Descriptive wording avoids pretending that a fuzzy GIMP canvas match establishes a technical noun. Review whether drawing area clearly denotes the bitmap canvas rather than the whole editor viewport. |
| Draw again | ድጋሚ ሳል | Imperative; medium-high lexical, medium contextual | Exact Android Settings `lockpattern_restart_button_text` Redraw. Pattern-entry context invites the user to draw again, not automatic repaint. Here it returns to the prior drawing tool; it does not generate a stroke. Optional behavior-explicit alternative `ወደ መሳያው ተመለስ` is a NEW composition (“return to the drawing tool”), not an exact source string. |
| Pixel grid | የፒክሰል ፍርግርግ | Newly composed noun phrase; medium, REVIEW | Android separately attests grid ፍርግርግ and pixel stem ፒክሰል (including ፒክሰሎች and ሜጋፒክሰል). No exact pixel-grid compound found. It names the displayed overlay, not a snap setting. Alternative LO-family `የፒክስል መጋጠሚያ` is also composed and less preferred because መጋጠሚያ is broad junction/alignment terminology. Do not mark either as exact attestation. |
| Full screen | ሙሉ ገጽ ዕይታ | Noun phrase/mode label; medium-high | Exact Android Settings `user_aspect_ratio_fullscreen`. It names the full-screen view, not a request to resize the image. In this app it hides editor controls/status bar. Android also has `ሙሉ ማያ ገፅ`; LO uses the different exact phrase `በሙሉ መመልከቻው`. |
| Show controls | መቆጣጠሪያዎችን አሳይ | Derived imperative; medium-high | Android exact Show device controls → `የመሣሪያ መቆጣጠሪያዎችን አሳይ`; remove the device qualifier. Android separately attests Controls → `መቆጣጠሪያዎች`. Full shortened phrase is derived, not an exact quotation. Restores editor controls by leaving full-screen; not a new controls customization panel. |
| Navigate | እይታ ማንቀሳቀሻ | Derived tool/action noun; medium | LO exact Zoom & Pan → `ማሳያ & ማንቀሳቀሻ`; Android panning instruction uses `ያንቀሳቅሱ`. Explicit “view movement” helps distinguish panning from moving image content. LO's exact Navigate → `መቃኛ` is a shorter alternative, but its general navigation/menu context does not establish a pan-specific tool. Choose after independent review of consistency with existing tool nouns. |

Confidence is confidence in source support and semantic transfer, not a native quality score. Exact source reuse does not itself prove that a label is suitable for AN Paint. No candidate is asserted accepted. Canvas caption is deliberately held; pixel-grid compound and Navigate composition need explicit scrutiny. If an all-seven package is required, it is a seven-row DRAFT, not seven cleared translations.

## Semantics that review must preserve

- Fit changes the viewport zoom/position, not bitmap size. Bounds include the whole canvas PLUS any outlying floating-selection/trim bounds. “Entire canvas” describes included content, not exclusion of outliers. The short caption need not expose all bounds, but documentation must not promise canvas-only fitting.
- Draw again selects the remembered previous non-ZOOM tool via `chooseTool(drawingTool)`, default Pencil. The remembered tool can include selection/fill, so it is a return-to-drawing-workspace command rather than necessarily freehand drawing. Navigate/Draw again can commit prior geometry or floating selections through `selectTool` → `applyPending`. Do not claim switching is mutation-free. Returning to a drawing tool creates no automatic stroke.
- Subsequent Navigate drag pans the view; a single tap does not draw or zoom. Avoid move-object terminology without a view qualifier.
- Pixel grid toggles the overlay. Grid lines require zoom ≥ 8 (800%); ruler inset depends on the toggle alone. Do not say rulers are 800%-only. Neither snapping nor pixelation/resampling is implied.
- Full screen hides editor controls/status bar and sets SYSTEM_UI_FLAG_FULLSCREEN; Show controls restores them. No immersive navigation-bar hiding is promised. Neither changes image dimensions.

## Evidence and audit

`sources.json` gives commit-pinned primary URLs, SHA-256 for each retained file, and fresh byte-comparison results. Source snapshots were copied from the same-day lexical packet and independently refetched at pinned URLs for comparison; the extra LibreOffice svx file was fetched directly. `po-evidence.json` includes source line, context, raw gettext record, English/Amharic and explicit fuzzy flag. `android-evidence.json` includes matched English key, Amharic key, Android message ID, line and raw source line. Android quote wrappers are source syntax; the cleaned Amharic value removes only matching outer quote characters. XML does not have gettext fuzzy status.

Primary source set:
- LibreOffice/translations commit `681a7f1e79cd6e27496259dab7940c8e490059de`: Office/UI.po, shared help 01.po/02.po, and svx/messages.po.
- Android Settings commit `7c598253ff60f06f8e6fe046f18fd88e9daa72d3`: matching English and Amharic strings.xml.
- Android Gallery2 commit `c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb`: matching English and Amharic strings.xml.
- GNOME/gimp commit `7d518c7971e80719ce30f70ec44b55e49ab2aeb7`: po/am.po, checked for positive and negative evidence.

### Important exact nonfuzzy LibreOffice records

- MathCommands.xcu / `.uno:FitInWindow` / Label: Fit To Window → `በመስኮቱ ልክ`.
- DrawImpressCommands.xcu / `.uno:ZoomMode` / Label: Zoom & Pan → `ማሳያ & ማንቀሳቀሻ`; tooltip separately pairs Shift to Pan with `Shift ለ ማንቀሳቀሻ`.
- GenericCommands.xcu / `.uno:NavigateMenu` / Label: Navigate → `መቃኛ`; navigation context is general, not proof of pan semantics.
- GenericCategories.xcu / category 24: Drawing → `መሳያ`.
- GenericCommands.xcu / `.uno:GridVisible`: Grid → `መጋጠሚያ`, Display Grid → `መጋጠሚያ ማሳያ`.
- GenericCommands.xcu / `.uno:Repaint`: Redraw → `እንደገና መሳያ`. This is repaint, NOT semantic identity with returning to a drawing tool; Android user-draw wording is better evidence.

### Important Android records

- Settings `privacy_controls_title`: Controls → `መቆጣጠሪያዎች`.
- Settings `lockscreen_privacy_controls_setting_toggle`: Show device controls → `የመሣሪያ መቆጣጠሪያዎችን አሳይ`.
- Settings `user_aspect_ratio_fullscreen`: Full screen → `ሙሉ ገጽ ዕይታ`.
- Settings `lockpattern_restart_button_text`: Redraw → `ድጋሚ ሳል`.
- Settings `trackpad_go_back_title`: Go back → `ተመለስ` (supports return alternative only).
- Settings `keywords_wallpaper` aligns grid with `ፍርግርግ`; corroborated by Gallery2 `switch_photo_grid`: Grid view → `የፍርግርግ ዕይታ`.
- Gallery2 `pref_camera_picturesize_entry_13mp`: 13M pixels → `13ሚ ፒክሰሎች`; `pref_camera_picturesize_entry_8mp`: 8M pixels → `8 ሜጋፒክሰል`.
- Settings `accessibility_magnification_one_finger_panning_summary_on`: Move the magnification area by dragging one finger → `አንድ ጣትን በመጎተት የማጉያ ቦታውን ያንቀሳቅሱ።` Supports view-area movement, not moving drawn content.

### Exclusions and limitations

GIMP `_Fit Image in Window`, `Fit to window`, `Pan view`, `F_it Canvas to Selection`, Configure Image Grid and Default Image Grid have fuzzy localized matches. They are not usable positive evidence merely because their English matches the requested functionality. In particular the fuzzy Fit to window translation must not be used to claim an exact authoritative fit imperative. GIMP navigation/zoom records with fuzzy flags stay excluded; existing zoom-in/out decisions are outside scope.

No checked nonempty nonfuzzy canvas term was found in the scoped files. `የመሳያ ቦታ` is transparently composed from drawing + area, NOT a claimed dictionary quotation or a canonical project term. A reviewer can hold this row instead of forcing unsupported terminology. Source nonfuzzy status does not guarantee correctness: the LO entire-page help paragraph has apparent English/Amharic drift and is not used as a model full sentence. No Microsoft corrupted Ethiopic PDF extraction was used.

Web open of the pinned LO raw URL returned cache miss; the ordinary permitted HTTPS file retrieval succeeded. This was a retrieval failure, not an access denial. No blocked action was bypassed, and no authorization is inferred from retrieval success.
