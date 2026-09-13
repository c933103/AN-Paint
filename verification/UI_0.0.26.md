# AN Paint 0.0.26

Version code 79; package `paint.anpaint.android`.

- All sixteen saved palette slots remain visible in the Color panel and picker.
  Empty slots have an add mark. Add colour opens the editor and saves the
  accepted colour to the palette while making it active. Cancel restores the
  prior colour and does not fill the slot. Existing slots support use, editing,
  background selection and removal. Advanced opens the spectrum directly and
  sits beside the Black / white reset control, including in landscape.
- View precedes Draw; Navigate is View's first tile and remains the initial
  tool. Its options move with it. Draw keeps the existing Drawing, Selection
  and Insert categories and classic icon/caption style. Landscape keeps vertical
  side tabs, and top shortcuts remain compact on the first title row.
- Pixel grid reserves top and left ruler bands. Integer tick spacing adapts to
  zoom; labels follow image coordinates through pan, zoom, resize and restored
  drafts. The scrollbars use the same inset viewport. Ruler touches do not draw.
- Cursor x/y update during movement beside the current zoom percentage. Narrow
  screens let the status wrap instead of cutting off the coordinates. New
  drawing settings default anti-aliasing off; saved choices remain respected.
- The language menu has 104 choices plus device language, with International
  English pinned second and all other codes sorted. Regional English, Spanish,
  Korean and Portuguese labels and legacy migrations are explicit. Thirty
  requested names have no new translations and use English UI. Naming sources,
  canonical tags and the Tai language collection are documented in
  `translations/language-options.json` and `translations/README.md`.

The tests exercise palette add/cancel/remove and shared updates; navigation
placement; portrait, narrow portrait, landscape and vertical-script layouts;
live cursor coordinates; ruler tick bounds; resize/restore/scrollbar geometry;
language names, ordering, migrations and fallback. The full build and test
status belongs in the delivery handoff; this change note does not claim a
pending workflow passed.
