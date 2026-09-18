# Cursor drawing in AN Paint 0.0.38

Reference: [Catrobat/Paintroid at 853ce3c346910ea73aa4de5514f2a76ace1396fb](https://github.com/Catrobat/Paintroid/tree/853ce3c346910ea73aa4de5514f2a76ace1396fb), AGPL-3.0-or-later.

`tools/implementation/CursorTool.kt` (blob dbfeb38d1134aaf782ff7cc3e510d0895e4c1616)
supplies the circle/square geometry and four alternating crosshair segments in
PaintroidCursorOverlay. The outline surrounds the brush width; its circle/square shape is an independent display setting.

Enabling cursor mode starts with positioning only. Start drawing / Stop drawing
is available on the canvas while a compatible tool is active, including fullscreen. With
ink enabled, dragging draws at the cursor and tapping away from the cursor places
a dot. Without ink, those gestures only position it. A deliberate tap on the
cursor itself toggles ink without painting a dot; dragging that target still
moves or draws after touch slop. Short strokes away from the target are retained.
Cancellation rolls back an unfinished stroke.
Switching tools, opening cursor settings and reopening a draft pause ink.

View → Cursor drawing expands the Enable/Disable button, Round/Square cursor outline,
magnifier visibility and zoom, and cursor marker size. Brush, width and tip stay
under Draw → Drawing. Pencil keeps its square pixel tip. Magnifier and marker settings survive drafts;
ink deliberately does not resume automatically. Enabling cursor mode and
starting/stopping ink leave the settings drawer open. The on-canvas control uses
the existing labelled 64 dp tool tile, including visible Start/Stop text.

BaseToolWithShape's original marker stroke uses 5 dp divided by canvas zoom,
clamped to 1–10 image pixels. That clamp can shrink the marker at fitted zoom on
AN Paint's larger images. AN Paint retains a compact 3.5 dp screen stroke, with a
100–200% visibility control. Brush radius remains in image coordinates; enlarging
the marker does not enlarge the painted stroke.

The circular preview adapts DefaultZoomWindowController and DrawingSurfaceListener,
samples cursor coordinates independently of the finger, and moves corners only
when the finger approaches it. It remains visible between cursor strokes and is
hidden during pinch/scrollbar gestures. Finger preview disappears on lift.
The lens retains its 120 dp area, bounded by the available viewport. Its scale is
max(canvas zoom, 1) times the selected 100–400% magnification. Explicit source-pixel
bounds prevent Android bitmap-density rescaling from changing that factor. The
cursor uses the main viewport's geometry inside the enlarged canvas, so its
outline and crosshairs magnify along with the drawing. No separate preview
shrink factor cancels this enlargement. The lens draws into a clipped canvas
without per-frame full-image allocations.

Tests cover positioning without ink, explicit Start/Stop through Android input,
short strokes for all four supported brushes, undo/cancellation, circle/square
geometry, marker visibility at fitted zoom, cursor-centred magnification, settings
placement and safe restoration. New rendering tests measure pixel and cursor
outline sizes across magnifications, including differing bitmap densities.
The magnifier and actual-size/enlarged main canvas use crisp pixels; reduced
main views use filtered overviews. Drawing antialiasing remains off by default.


Version 0.0.32 keeps the original marker geometry but exposes its circle/square
outline as `cursorShape`, independently of the selected brush tip. Both the main
canvas and magnifier use that outline. The cursor drawer contains only cursor
controls. Drawing tools keep their usual settings, including calligraphy. The
on-canvas Start/Stop button uses a non-modal toast and the existing active/inactive
crosshair colouring; it does not reserve another bar below the canvas.
