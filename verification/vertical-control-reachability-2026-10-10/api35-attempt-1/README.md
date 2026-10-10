# PR41 API35 attempt 1: bounded failed-drag evidence

[PR41](https://github.com/c933103/AN-Paint/pull/41) · [failure comment](https://github.com/c933103/AN-Paint/pull/41#issuecomment-6094296448) · [run 38027075427](https://github.com/c933103/AN-Paint/actions/runs/38027075427) · [parent PR18](https://github.com/c933103/AN-Paint/pull/18) · [project board PR39](https://github.com/c933103/AN-Paint/pull/39)

Executed PR41 head: `7549abdcc9a65945ec18bbab6a25d54b4ce0bce8`.
Tested merge: `4be3b6afc2030e08536fb13a403e1ab57bfe074e`.
Identical source tree: `735c79b8dd14a243c62447a8de337b05ed16cbbc`.
API35 artifact 11660233697 SHA-256:
`a0939820d19fade53fd5c65b5d2131f1324debe3941fdb5fba3cbcd520472416`.

This is a deliberately selected subset, not a copy or sanitization of the whole
artifact. The eight PNGs, four partial geometry JSON receipts and two vertical
JUnit/summary files are byte-identical individual files from that artifact.
Complete emulator/logcat and build logs are excluded. `files.json` records each
selected file's SHA-256 and length. No prior evidence is overwritten.

## Observed result and limits

All four vertical methods failed in portrait on the first attempted native drag
to JPEG quality 1. The JUnit phase lasted 120.706 seconds; its summary reports
`timed_out: false`. The unchanged phase ceiling is 180 seconds. Landscape,
successful endpoint captures, later Cancel/reopen and Choose location actions
were not reached. Missing states remain unverified; this run is failed.

Before injection, native horizontal reveal brought each complete quality column
into the clipped viewport, and SeekBar/readout/thumb geometry checks passed.
The before/failure pixels show horizontal form displacement while the dialog
stays fixed. English and Manchu visibly retain quality 95; the RTL failure views
move the numeric readout offscreen. In English, the recorded column moved from
partly clipped `[118,138,294,212]` to fully visible `[103,138,279,212]` before the
failed drag. Clipping alone is not a production-defect finding.

A second independent visual inspection of the two original English PNGs also
observed quality 95 in both, with the slider and label shifted left in the failure
image while the dialog remained fixed. That corroborates the bounded pixel
observation only; it does not determine touch routing or certify other states.

The unchanged production widget is a SeekBar inside NumericSlider inside a
HorizontalScrollView subclass. Android 15's scrolling-container drag handling is
consistent with parent interception, but interception remains an inference:
this first probe lacks directly delivered child DOWN/MOVE/CANCEL events and
post-drag parent offsets. A failed drag does not establish that every endpoint
route, including a tap, is inaccessible.

Primary platform references: [AbsSeekBar](https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-15.0.0_r1/core/java/android/widget/AbsSeekBar.java),
[HorizontalScrollView](https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-15.0.0_r1/core/java/android/widget/HorizontalScrollView.java).

Next proposal: read-only test telemetry for requested coordinates, actual
SeekBar events, progress and ancestor scrolling, with existing gestures,
assertions and deadlines retained. It must be reviewed before publication or
another CI run. No production routing override is included in that proposal.
