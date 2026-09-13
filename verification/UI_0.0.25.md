# AN Paint 0.0.25 interface correction

Version 0.0.25 (code 78), package `paint.anpaint.android`.

- Panel captions are centered in the final measured tile width, including
  horizontally scrolling Main tools and category tools. The platform text
  layout is measured again at that width; changing gravity alone was insufficient.
- Edit and View commands, plus Color's Swap, Reset and Edit palette actions,
  use the same square icon tiles and captions as Main. File retains text commands.
  Icon/action pairs share one command definition. Existing labels are retained.
- The filename and AN Paint subtitle share one header with six compact shortcuts
  at its right, including on 320 dp portrait screens.
- Landscape uses a vertical tab rail for every language. Main tools scroll down
  beside it, and category tools/options open to the right. Closing the drawer or
  panel releases canvas width. File, Edit, View and Color occupy the side panel.
- Literary Chinese and traditional Mongolian keep their natural vertical captions
  beside icons, vertical status rail and dedicated dialog layout.

Regression checks exercise rendered caption bounds, narrow headers, side-panel
geometry, rotation, drawer collapse, fullscreen, every tool and both vertical
scripts. The current-platform CI also runs the existing format, translation,
canvas and file-workflow checks. See the delivery report for completed results;
this source note does not claim that a pending workflow passed.
