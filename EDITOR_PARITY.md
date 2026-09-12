# Original-editor consolidation — 10 September 2026

Compared against the original editor retained in AN Paint `2.14.1-local.15`,
derived from Catrobat/Paintroid `v2.14.1`.
The audit covers its `ToolType`, tool option interfaces, menus, advanced settings,
zoom-window settings, import/export and save flows. The original implementation
and its tests remain available in Git history.

| Original function | Consolidated editor |
|---|---|
| Brush, eraser, round/square tips | Toolbox; size up to 100 px, slider plus exact number entry. Calligraphy remains an additional brush tip. |
| Watercolor | New toolbox tool beside Brush/Airbrush, with strength and size controls. Strokes blend colour onto the opaque canvas. |
| Spray radius | Airbrush options, up to 100 px with numeric entry. |
| Straight and connected lines, rectangle, ellipse | Toolbox tools with outline/fill choices. Polygon with Close polygon switched off draws connected open line segments. Curve and rounded rectangle also remain. |
| Heart, star, arrow | Separate toolbox tools with outline/fill choices. |
| Text and font options | Text dialog: 19 faces, actual-font previews, formatting, alignment, line spacing and optional background box. |
| Cursor drawing | View > Enable cursor drawing. Drag moves the crosshair; tap toggles ink. Drawing uses Brush, Pencil, Watercolor or Eraser. |
| Magnified drawing window | View > Magnified preview, with enable switch and adjustable magnification. |
| Antialiasing, stroke smoothing | View > Drawing settings. Pencil keeps crisp hard-edged strokes, with independent 1–100 px width. |
| Eyedropper and fill tolerance | Toolbox Eyedropper and Bucket fill. |
| Clipboard/stamp, rectangular and free-form clipping | Cut/Copy/Paste/Select all, reusable paste, rectangle/lasso selections, corner and edge resizing, rotation and aspect lock. |
| Hand/pan, zoom | Navigate, two-finger pan/zoom, 100% centre tick and step-stop, Fit. |
| Centre canvas | Fit both fits and centres the canvas in the viewport. |
| Resize, rotate, flip, canvas bounds | Image menu; pixel/percentage dimensions, aspect lock and touch trim/expand. Counterclockwise rotation is also attainable with repeated clockwise rotation. |
| Colour presets/history and numeric selection | Palette, Honeycomb, RGB/HSV/HSL/hex, custom swatches and four additional recent-colour cells at the far right. |
| Load/replace and insert | File > Load image; File > Insert image into canvas. |
| Online media gallery | File > Catrobat sticker gallery, directly below Insert image; source links and attribution under Help > Image credits. This is an online gallery, not a bundled image collection. |
| PNG/JPEG export and JPEG quality | File Save options; JPEG quality slider and exact numeric entry. JPEG XL adds lossless/lossy export and import, including assembly crops. |
| Save copy and sharing | Save exports to an Android-selected location; Save and share exports successfully before opening Android sharing. |
| New/discard, undo/redo and recovery | New/Load/Back protect unsaved work; undo/redo, atomic autosave and recovery-copy export remain. |
| Fullscreen/hide controls | View > Hide editor controls, with Show controls and Back to restore them. |
| General Android image intents | VIEW, EDIT and SEND image intents open in the consolidated editor. |
| Help, credits and source | Help includes attribution, full licence texts, fixed Copy all/Other terms/Done buttons and offline corresponding source. |
| Layers, transparency controls and transparent document output | Removed as requested. Opening an image composites transparency onto the main editor's BG colour; inserting an image composites its mask onto existing canvas pixels; assembly output uses white. Internal masks still preserve the geometry of free-form and rotated selections. |
| Smudge and automatic crop | Removed as requested. Selection crop and manual canvas trimming remain. |
| Native Paintroid/OpenRaster project save/load | Removed with layers as requested. Autosave is private draft recovery, not a public project format. |
| Upstream-specific Pocket Code integration and store/feedback links | Original-app integration is not part of the independently packaged AN Paint. Standard Android image intents and sharing remain; rating/feedback links were already hidden in earlier local builds. |

All retained user-facing editing capabilities in this audit have a corresponding
location above. Removed capabilities are explicit, rather than hidden behind an
inaccessible old activity. This is feature coverage, not a claim that new brush
rendering is pixel-identical to the original implementation.

## Requirement recheck — 12 September 2026

The original `ToolType`, every surviving tool-options interface, the original
More options menu, advanced-settings dialog and zoom-window settings were checked
again against the consolidated workspace. No further standalone editing command
was found without a corresponding entry in the table. The deliberately removed
features and original-app Pocket Code integration remain the explicit exceptions.

The requested Watercolor, shape tools, numeric size entry, cursor and magnifier,
four recent colours, insertion/gallery ordering, JPEG quality, Save and share,
and Fit/centre behavior have executable regression coverage in
`UnifiedEditorTest`. Older selection, full-resolution, autosave, canvas-bounds and
assembly regression classes cover the retained workflows. These tests complement
the source audit; neither source coverage nor emulator execution establishes
physical-phone verification.

Translation preparation uses Android resources for editor and dialog text,
positional formatting, plurals, stable persistence/menu identifiers and separate
legal notices. The RTL audit found and corrected a detached-sidebar-toggle risk:
physical image workspace geometry stays left-to-right while text can follow the
locale. Numeric slider formatting is resource-based. `TRANSLATING.md` describes
the complete resource catalogue and future-language review. Supplying unspecified
human translations is not a pending part of this request.

## Font-test explanation

The old `TextToolFontListTest.kt` substitutions followed removal of the bundled
Dubai and STC-labelled font binaries during the earlier licence review. The old
selector entries then used Android system fonts.
Variables still named `dubaiFontFace` and `stcFontFace` were misleading: those
assertions tested system-font fallbacks, not the named proprietary fonts.

That selector and its obsolete tests have now been removed with the original
editor. Current tests check the current font inventory and load the actual ten
bundled OFL font files, along with the nine device-supplied font choices.

The [documented licence investigation](FONT-LICENCE-REVIEW.md) checks the exact
upstream bytes and official foundry statements. They are Dubai Regular 1.10 and
Boutros GE SS Text Light 1.200; the latter was labelled STC upstream, without
an explanation of that name in the records reviewed. Dubai’s original
binary contains a limited-use notice, and the separately published Dubai EULA
also excludes image-generating applications. Boutros’s public terms restrict
copying and distribution without an additional agreement. Both remain excluded
under the terms established for AN Paint. Upstream inclusion for Arabic text
support does not establish the applicable grant; this is not a finding that
Catrobat lacked permission. The report distinguishes direct binary evidence, official
foundry terms and the third-party preservation of Dubai’s EULA, and retains the
[full metadata evidence](verification/legacy-font-metadata.json). Restoration
would require documented additional permission; this is no longer merely an
absence-of-metadata finding.
