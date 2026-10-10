# Custom vertical text redraw correction

Proposed source correction based on the failed [API35 run 38031416670](https://github.com/c933103/AN-Paint/actions/runs/38031416670),
head `f22ff7a206b6e871e54fec4b0e02ae32f7cc4700`, exact source tree
`d21df4db395b12aeac71600d73394323fa040d51`.

## Actual pixels differ from current native state

The original emulator artifact `11662561776`, SHA-256
`c804b59b9d9eb75ca6b24af696d2ae09cdf9ffa0c81582f75ffc30fd18c2397c`,
contains these independently observed examples:

- `en-XV-portrait-minimum.png` visibly reads Quality (%): 76 while its native thumb
  is at minimum; the receipt/model/readout property says 1.
- The later `en-XV-portrait-maximum.png` still visibly reads 76 while its thumb
  is at maximum; the model/readout property says 100.
- `en-XV-landscape-maximum.png` and the later `en-XV-landscape-cancel-ready.png`
  visibly read 1 although their thumbs and recorded values indicate 100.
- The filename preview still draws Untitled.png beside the updated native field
  Untitled.jpg, including the dedicated portrait filename capture.

These are the original PNGs, not synthetic renders. The disagreement persists
through multiple captures after native changes and frame-commit synchronization.
The successful gesture/model receipts therefore do not establish correct visible
text. They remain partial evidence; the full run also hit its separate unchanged
180-second vertical-phase deadline before Literary Chinese completed.

## Source explanation and correction

FlowButton and FlowTextView both measure and draw their own vertical text without
calling the corresponding TextView implementation. TextView's native Layout can
therefore remain null. In [Android 15 TextView.setText](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/TextView.java#L6958-L6962),
checkForRelayout is conditional on that Layout already existing. Updating the
text property does not by itself guarantee that these custom display lists or
column dimensions are refreshed.

Both custom widgets now forward onTextChanged to super and, only in vertical
mode, requestLayout and invalidate. This targets the renderer's own ink and
measurements. Horizontal TextView behavior, text content, fonts, glyph shaping,
native slider input, and existing screenshot synchronization remain unchanged.
The fix does not add a test-only forced redraw or longer capture wait.

## Regression scope and limits

New Robolectric API30/API35 cases cover both widgets in all four vertical
profiles: same-length PNG-to-JPEG preview changes, repeated 95/76/1/100 readouts,
and growing/empty wrapped columns. They explicitly establish a null native
Layout, clear prior layout/invalidation observations, then require text changes
to schedule both actions themselves. The tests never call invalidate or
requestLayout to manufacture that outcome. Host source guards include negative
mutations removing each required notification.

Host source checks are not Android execution or hardware pixel evidence. The
local Gradle distribution remains unavailable; JVM compilation/execution and
fresh installed screenshots must be verified before accepting this correction.
The existing partial/visually incorrect run remains failed. This candidate makes
no timing, gesture, test partition or budget changes; that issue is separate.
