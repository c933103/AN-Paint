# Test-only C05 fit-observation successor

The first C05 run and original captures are retained separately under `acceptance-38102363951`, tied to `d8132ede`. Their successful behavior checks do not settle text fit, and the original false flags remain unchanged.

This increment changes only the C05 Android observation harness and its host source contract:

- Select/materialize the actual About menu row, require its real text/attachment/visibility and supply that row to the existing item-click callback. No title-only row acceptance.
- Record notice Copy all/Other terms/Done controls, as well as their title.
- Separate intrinsic text truncation from initial ancestor clipping and visibility after a real `requestRectangleOnScreen` traversal. Record view/screen bounds, visible rectangles, ancestor classes and scrolling offsets/capabilities, maximum lines and ellipsis policy.
- Preserve initial PNGs before any reveal request. Save extra reveal-state PNGs only for initially off-screen views.
- Require the actual dialog title explicitly. No fabricated sizes, reduced font, changed resource value, hidden skip or production layout patch.

The new observation fields still do not assert native-finger/TalkBack/physical-device acceptance. A successful rectangle request is evidence about the actual model ancestor chain, not proof of every input route. Text-layout and visual acceptance remain separate from Copy/Save behavior. The shared production UI correction is tracked independently.

Fresh host/optimized checks and normal exact-head Android CI are required for this test increment. The original 17 Hungarian XML replacements, their pinned scope fixture, and all C03/C04/F01/C023 historical endpoints remain byte-identical to `d8132ede`.

## Local final-source results

- Full host discovery: 554 tests, zero failures/errors/skips, 148.163 seconds.
- Focused C05: 8 tests pass normally and with `python -O`.
- Android compilation/execution for this successor is pending its fresh exact-head CI; the preceding run cannot certify new harness code.
