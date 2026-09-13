# AN Paint 0.0.27 development update

Package `paint.anpaint.android`; version code 80.

- The Mongolian language option expands to fit the vertical autonym and `[mn-Mong]` code. The old dialog row imposed a fixed 48 dp height; verification now uses the mounted menu row.
- Swap arrows follow the colour arrangement: up/down for stacked swatches and left/right for side-by-side swatches in vertical text layouts.
- The zoom slider has an unlabelled actual-size tick. The status area still shows the current zoom.

All previous features remain included. See [0.0.26 verification](verification/HANDOFF_0.0.26.md) for the preceding completed build.

Local layout and interaction checks passed (46 tests). The nine language checks passed again after the final padding adjustment; lint reported zero issues. Universal APK production and current-platform CI verification follow source publication; this source snapshot does not claim those pending checks passed. The completed delivery handoff records the final observed status.
