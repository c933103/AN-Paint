# Cursor drawing in AN Paint 0.0.32

Reference: [Catrobat/Paintroid at 853ce3c346910ea73aa4de5514f2a76ace1396fb](https://github.com/Catrobat/Paintroid/tree/853ce3c346910ea73aa4de5514f2a76ace1396fb), AGPL-3.0-or-later.

`tools/implementation/CursorTool.kt` (blob dbfeb38d1134aaf782ff7cc3e510d0895e4c1616)
supplies the circle/square geometry and four alternating crosshair segments in
PaintroidCursorOverlay. The outline surrounds the brush width; its circle/square shape is an independent display setting.

Enabling cursor mode starts with positioning only. Start drawing / Stop drawing
is available on the canvas while a compatible tool is active, including fullscreen. With
ink enabled, dragging draws at the cursor and tapping places a dot. Without ink,
both gestures only position it. Every movement is retained, including strokes
shorter than Android touch slop. Cancellation rolls back an unfinished stroke.
Switching tools, opening cursor settings and reopening a draft pause ink.

View → Cursor drawing expands the enable switch, Round/Square cursor outline,
magnifier visibility and zoom, and cursor marker size. Brush, width and tip stay
under Draw → Drawing. Pencil keeps its square pixel tip. Magnifier and marker settings survive drafts;
ink deliberately does not resume automatically.

BaseToolWithShape's original marker stroke uses 5 dp divided by canvas zoom,
clamped to 1–10 image pixels. That clamp can shrink the marker at fitted zoom on
AN Paint's larger images. AN Paint now retains the 5 dp screen size, with a
100–200% visibility control. Brush radius remains in image coordinates; enlarging
the marker does not enlarge the painted stroke.

The circular preview adapts DefaultZoomWindowController and DrawingSurfaceListener,
samples cursor coordinates independently of the finger, avoids the finger's upper
corner, and disappears on lift or pinch. It draws directly into a clipped canvas
and supports 100–400% zoom without per-frame full-image allocations.

Tests cover positioning without ink, explicit Start/Stop through Android input,
short strokes for all four supported brushes, undo/cancellation, circle/square
geometry, marker visibility at fitted zoom, cursor-centred magnification, settings
placement and safe restoration. Pixel filtering remains explicitly off in the
main image view and magnifier; drawing antialiasing remains off by default.


Version 0.0.32 keeps the original marker geometry but exposes its circle/square
outline as `cursorShape`, independently of the selected brush tip. Both the main
canvas and magnifier use that outline. The cursor drawer contains only cursor
controls. Drawing tools keep their usual settings, including calligraphy. The
on-canvas Start/Stop button uses a non-modal toast and the existing active/inactive
crosshair colouring; it does not reserve another bar below the canvas.
