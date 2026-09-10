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
| Antialiasing, stroke smoothing | View > Drawing settings. Pencil keeps crisp one-pixel strokes. |
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
| Layers, transparency controls and transparent document output | Removed as requested. Imports flatten onto the main editor's BG colour; assembly output uses white. Internal masks still preserve the geometry of free-form and rotated selections. |
| Smudge and automatic crop | Removed as requested. Selection crop and manual canvas trimming remain. |
| Native Paintroid/OpenRaster project save/load | Removed with layers as requested. Autosave is private draft recovery, not a public project format. |
| Upstream-specific Pocket Code integration and store/feedback links | Original-app integration is not part of the independently packaged AN Paint. Standard Android image intents and sharing remain; rating/feedback links were already hidden in earlier local builds. |

All retained user-facing editing capabilities in this audit have a corresponding
location above. Removed capabilities are explicit, rather than hidden behind an
inaccessible old activity. This is feature coverage, not a claim that new brush
rendering is pixel-identical to the original implementation.

## Font-test explanation

The old `TextToolFontListTest.kt` substitutions followed removal of the bundled
Dubai and STC/GE SS font binaries, whose bundled metadata did not establish app
redistribution rights. The old selector entries then used Android system fonts.
Variables still named `dubaiFontFace` and `stcFontFace` were misleading: those
assertions tested system-font fallbacks, not the named proprietary fonts.

That selector and its obsolete tests have now been removed with the original
editor. Current tests check the current font inventory and load the actual ten
bundled OFL font files, along with the nine device-supplied font choices.
