# NumericSlider gesture ownership correction

This is a proposed production correction, not a device-verification pass.

## Observed failure retained

PR #41's diagnostic head `84ab659548eb920f9db5001aa2114f106729aa65`
has tree `8c07c1dfea36e614062f86131ff0508c3f3c40b1`.
[API 35 run 38029694670](https://github.com/c933103/AN-Paint/actions/runs/38029694670),
artifact `11660944852`, failed all four initial portrait slider drags.
The native SeekBar received DOWN, MOVE, CANCEL; its quality stayed 95.
The containing ColumnScrollView moved horizontally: en-XV 296 to 349,
mnc-Mong 324 to 377, lzh-Hant 49 to 0, qaa-Zsye-XV 66 to 11.
The trace reported no observation errors or dropped events, and removed its
observers. The other 94 installed checks passed. The app-vertical phase took
120.055 seconds, within its unchanged 180-second deadline.

This supports ancestor interception for these specific drags. It does not show
that every possible input route fails. The landscape and later action paths
were not reached by these failed cases. Original failed receipts, screenshots
and the [independent review](https://github.com/c933103/AN-Paint/pull/41#issuecomment-6094627822)
remain evidence of failure; the fix does not reclassify them.

## Cause and narrow change

The real shared NumericSlider used a stock SeekBar inside a horizontal scroll
ancestor. In Android 15, AbsSeekBar delays drag start until movement passes touch
slop when inside a scrolling container. HorizontalScrollView can intercept that
same movement before the child can claim it. The new anonymous SeekBar subclass
claims an enabled child DOWN before delegating to the native handler.

Every event and the return value still come through native SeekBar.onTouchEvent.
Native value mapping, minimum/maximum, listeners, keyboard/accessibility input,
RTL behavior, and exact-value entry are unchanged. The stored parent claim is
released after UP/CANCEL, rejected or throwing native handling, disable, and
detach. A secondary POINTER_UP is not treated as the end of the gesture.
No ColumnScrollView behavior changes. Gestures outside the interactive slider
remain ordinary native form scrolling; disabled sliders do not claim DOWN.

Primary references:

- [Android touch dispatch and interception](https://developer.android.com/develop/ui/views/touch-and-input/gestures/viewgroup)
- [Android 15 AbsSeekBar.onTouchEvent/startDrag](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/AbsSeekBar.java#L831-L950)
- [Android 15 HorizontalScrollView interception](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/HorizontalScrollView.java#L546-L628)

## Regression expectations

The existing four-language/two-orientation installed probe still performs the
same native UiAutomator swipes, range endpoints, visible readout/geometry checks,
ordinary form scrolling, Cancel/reopen, Back, destination and document checks.
It now additionally requires child DOWN/MOVE/UP without CANCEL, no dropped
observations, and stable ancestor scroll offsets throughout each slider drag.
The probe never claims a gesture or sets progress to make the test succeed.

`NumericSliderGestureTest` dispatches MotionEvents through the actual
ColumnScrollView/child hierarchy on Robolectric API 30 and 35. It covers repeated
minimum/maximum changes and the existing value callback, ordinary scrolling
after UP/CANCEL, secondary pointer release, disabled controls, and detach cleanup.
The isolated detach case deliberately bypasses parent dispatch so that a parent
CANCEL cannot conceal missing detach cleanup. These JVM tests supplement the
installed probe; they are not a substitute for installed native input evidence.

Local Python contracts may be run with:

```
python3 -m unittest discover -s tools -p 'test_*.py'
```

The focused JVM/instrumentation compilation attempt was blocked before
compilation because the Gradle 8.13 download returned `Network is unreachable`.
No JVM, compile, lint or installed-runtime pass is claimed for this candidate.
Independent source review and an exact-source current-platform run remain
necessary before crediting the correction. The API 30/35 Robolectric cases do
not constitute a completed full installed matrix.
