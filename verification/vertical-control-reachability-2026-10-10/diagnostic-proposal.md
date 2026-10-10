# Observation-only native-drag diagnostic proposal

[PR41](https://github.com/c933103/AN-Paint/pull/41) · [failed first-run evidence](https://github.com/c933103/AN-Paint/tree/69a36a16d3d5e03473607333e1fc0974fc16831a/verification/vertical-control-reachability-2026-10-10/api35-attempt-1) · [parent PR18](https://github.com/c933103/AN-Paint/pull/18) · [board PR39](https://github.com/c933103/AN-Paint/pull/39)

This proposal starts from tested PR41 head `7549abdcc9a65945ec18bbab6a25d54b4ce0bce8`,
tree `735c79b8dd14a243c62447a8de337b05ed16cbbc`. It adds observations around the
same native drag. It does not repair or declare a production defect. The four
failed portrait cases and unexecuted landscape/action coverage remain unchanged.

## Observed data

Each `native-drag-trace` records the requested quality and screen coordinates
before injection, together with the actual SeekBar/readout/thumb geometry,
padding, thumb offset, layout direction, touch slop, enabled/pressed/focus state,
draft filename, progress and ancestor scroll offsets. It records requested
coordinates before injection even if input fails.

The SeekBar's temporary OnTouchListener records delivered DOWN/MOVE/UP/CANCEL,
action codes, event/down times, source, pointer/history counts, local/screen
coordinates and the current state. Its observation phase is explicitly
`before-widget-handler`; that event has not yet run SeekBar.onTouchEvent.
The listener always returns false. A ViewTreeObserver scroll callback records
subsequent progress and ancestor offsets without replacing a view scroll listener.
The receipt preserves post-injection and final/error states, observer cleanup,
trace errors and explicit event/scroll drop counts (caps128/64). MotionEvent
objects are not retained. JSON serialization is copied on the main thread.

Delivered child DOWN followed by CANCEL plus parent scroll displacement would
support an interception diagnosis. Missing child DOWN leaves injection/window
hit-testing in question. Delivered motion with the wrong resulting value points
toward mapping/widget behavior. No automated diagnosis is asserted from these
patterns: actual traces and pixels still require review. A failed drag does not
establish whether a native tap or all other endpoint routes are inaccessible.

## Listener assumptions and unchanged behavior

At the exact base, `NumericSlider.kt` constructs a plain SeekBar and installs only
its OnSeekBarChangeListener, which updates the visible number and changed callback.
`SaveOptionsDialog.kt` constructs that NumericSlider for `export_quality`; neither
file sets an OnTouchListener. These source assumptions are checked by host tests.
The production value listener, callbacks and model fields are not replaced.

The diagnostic installs a temporary non-consuming touch listener on this known
listener-free test instance. It clears that listener and unregisters the added
scroll observer in finally, on both pass and failure. This restoration-to-null
assumption is scoped to the verified current source; it is not a generic listener
stacking facility. An existing production touch listener would require renewed
review rather than overwriting it. Observation adds timing overhead, so a future
trace is evidence under observation, not proof of zero observer effect.

There are no production changes, native routing overrides, scroll-flag changes,
synthetic touch dispatch, direct progress/scroll setters, tap fallbacks, or new
retries. Original gesture points/12-step swipe, exact endpoints, 15-second wait,
state assertions, distinct Cancel draft, screenshot inventory and 180-second
phase/outer deadlines remain unchanged. The proposal adds no system log capture.

## Verification scope

Ten targeted host receipt/source contracts pass, including a negative that
rejects a consuming observer and checks preserving original gestures/assertions.
These are source/mock checks, not Kotlin compilation or event-delivery execution.
The full host run observed 392 tests:391 passed and one existing, unchanged
GallerySink oversized-request contract failed (`Missing budget failure`). The
failure log is retained and the separate issue is under investigation; this
proposal does not claim a clean full-host result or change that fixture.

Android compilation and actual API35 telemetry remain unexecuted. Independent
source review is required before publication or another existing CI run. No
prior screenshot or failed test is reclassified by this proposal.
