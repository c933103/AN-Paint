# Position-dialog IME failure evidence, 20 October 2026

## Exact observed results

- Failed: [run 39408097942, job 118583133645](https://github.com/c933103/AN-Paint/actions/runs/39408097942/job/118583133645), develop `d7436b3df842b9be9aa12be622ebc88ed8e8e2b9`, API35.
  `ainuLatinPositionTextAndNativeEditing` timed out at its existing 8-second
  IME-visible wait for `assembly_position_y`. The other six position methods passed.
  This is a failed run, not a successful run with an ignored error.
- Passed comparison: [run 39408857136, job 118583541760](https://github.com/c933103/AN-Paint/actions/runs/39408857136/job/118583541760),
  PR150 head `fbee93eb5f7d7c85b290ba6dec54e0fe174d4f26`, tested merge
  `226961df4dd251cf1ff4d5e1c729be5c01a3a08e`, API35, all seven position methods.
- Both original receipts identify instrumentation source digest
  `3022fe07657c952e64e63bfc0fcc3da622cf2c337827df9f601be7cb22c826f4`.
  PR150 changes 18 files but not the position instrumentation, placement dialog,
  input configuration, or vertical dialog shell. Its success does not repair,
  supersede, or erase the develop failure.

## Trace interpretation

The failing method completed three portrait edit/IME-show/hide cycles and
committed `(5,4)`. The failure is the later landscape edit used to test Cancel,
after the second dialog's caption/field visibility traversal.

At 10:41:10.375 the failing trace records landscape geometry `416x272`.
A `PopupWindow` appears at 10:41:19.054, before the native field tap at
10:41:20.653 `(320,200)`. Popup windows are removed/created around that tap.
The input method starts the numeric editor, but the trace contains no
`SHOW_SOFT_INPUT` request for this tap. Focus and window focus are true when
the 8-second assertion fails. In the passing comparison, the corresponding
landscape tap at 10:42:19.410 `(320,191)` immediately requests and shows the IME.

The old caption-reveal helper always uses a scroll container's cross-axis
center. That lane can intersect native editable fields: the failing field's
screen rectangle is `(144,177)-(496,223)`, containing x=320. Such scroll
injection is not guaranteed to remain a scrolling interaction. Android's
native editor owns cursor/selection gestures, can disallow parent interception,
and can consume a release before the ordinary IME-show path.

This establishes a harness hazard, not the exact causality of this one failure.
`PopupWindow` alone does not identify whether it belongs to text selection,
autofill, or another native popup. The trace also reports a GMS persistent
process ANR at 10:41:19.089 and 99% total CPU over its reported sample.
The retained logs do not contain the field's actual MotionEvent sequence.
Do not call this a proved application regression, a proved long-press race,
or a proved fix solely from source inspection.

Android reference:
[TextView.java, API35 baseline](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/TextView.java#L13124-L13183)
and [Editor.java](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-15.0.0_r1/core/java/android/widget/Editor.java#L6891-L6935).

## Correction and remaining verification

The proposed harness correction chooses a genuine touch lane outside visible
editable descendants. It preserves native swipes, one native field tap,
full caption/accessibility coverage, IME visibility, real text input,
Apply/reload/Cancel/Back checks, and all existing deadlines. A blocked lane
fails instead of silently using a programmatic scroll, forcing IME/focus,
retrying a tap, or weakening an assertion. Each scroll now checks that focus
and field text are unchanged and records its coordinates.

Host tests execute the same Java lane planner, including the failing horizontal
coordinate extent, both axes, overlapping/out-of-order/clipped obstacles,
one-pixel free lanes, blocked paths, invalid inputs, and integer-boundary cases.
Those tests do not simulate Android event dispatch or establish an installed
device result. The changed source must pass fresh exact-source device testing.
If it still fails, use the new gesture/focus/selection diagnostics and preserve
that failure; do not blindly rerun it to obtain green.

## Preservation scope

`manifest.json` records the downloaded ZIP hashes, matching the original GitHub
artifact digests, and the retained files' SHA-256 values. This evidence ref
retains original device identities, shard instrumentation/JUnit/summary
receipts, the failing job output, and explicitly filtered raw IME/popup/system
pressure timelines. It does not retain unrelated bulk emulator logcat output.
Original artifacts:
[failed 12259670000](https://github.com/c933103/AN-Paint/actions/runs/39408097942/artifacts/12259670000),
[passed 12259525337](https://github.com/c933103/AN-Paint/actions/runs/39408857136/artifacts/12259525337).
