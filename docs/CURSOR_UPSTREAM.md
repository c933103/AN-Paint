# Cursor drawing in AN Paint 0.0.30

The reference is [Catrobat/Paintroid at 853ce3c346910ea73aa4de5514f2a76ace1396fb](https://github.com/Catrobat/Paintroid/tree/853ce3c346910ea73aa4de5514f2a76ace1396fb), under AGPL-3.0-or-later.

- `tools/implementation/CursorTool.kt`, blob `dbfeb38d1134aaf782ff7cc3e510d0895e4c1616`:
  `drawCircle`, `drawRect` and `drawShape` are directly adapted in
  `PaintroidCursorOverlay.kt`. The brush size, cap and current ink colour drive
  the marker; density and zoom retain the upstream stroke-width calculation.
- Relative finger travel moves the cursor. Version 0.0.29 copied the upstream
  tap-to-toggle interaction but initially disabled ink and cancelled movements
  shorter than Android's touch slop. That made short precision strokes disappear
  and could toggle drawing off. Version 0.0.30 enables ink immediately and exposes
  **Draw with cursor** beside the brush options. Turn it off to reposition without
  ink; taps and drags never change that switch. Every movement is drawn without a
  touch-slop threshold, and a tap places one undoable point. The explicit mode is
  retained in drafts; older cursor drafts default to drawing enabled.
- `ui/zoomwindow/DefaultZoomWindowController.kt` and
  `listener/DrawingSurfaceListener.kt`: the circular preview samples the cursor
  coordinates independently of touch coordinates. It switches upper corners to
  avoid the finger, updates while moving, and disappears on lift or pinch.

AN Paint integrates this into its existing bitmap and history rather than
restoring the removed workspace/layer/command stack. Cancellation rolls back
an unfinished stroke. Scrollbars and pinch retain the existing viewport rules.
The lens draws directly into a clipped Canvas, avoiding upstream's per-frame
full-image background bitmap allocations. Magnification is adjustable from
100–400%; cursor magnification defaults on and has its own saved setting.
Cursor brush options expose Round/Square; freehand drawing retains calligraphy. Pencil
retains its crisp square tip. The magnifier settings are reachable alongside
cursor drawing options and through View.

Regression tests exercise the explicit draw/move switch, short strokes and undo
for all four cursor brushes, out-and-back movement,
cancellation, actual circle/square rendering, correct magnifier sampling and
saved preference restoration. The language picker tests compare the native
radio bounds of Mongolian and an adjacent ordinary row in three layouts.
An installed-app test injects an actual Android swipe and checks that the bitmap
contains a line extending beyond the initial dot; an undo entry alone is not
proof of a working stroke.
