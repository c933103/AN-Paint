# Position-dialog native scroll lanes

The position instrumentation reveals complete captions using actual touch
swipes. Its old cross-axis-center lane could cross an editable control instead
of an inert part of the scroll container. The same native editor also handles
cursor movement, selection and long presses, so that path did not isolate the
intended scrolling interaction.

The helper now selects a free lane outside the visible editable descendants
over the swipe's full extent. It uses measured geometry, a 2dp clearance,
half-open coordinates and a fail-closed result when no lane exists. Every swipe
checks that field contents and the focused view remain unchanged. Gesture and
field-selection diagnostics are retained in logcat.

The correction does not change application code, disable editing or autofill,
force focus/IME, use programmatic scrolling, retry field taps, remove checks,
or extend deadlines. Complete caption and accessibility coverage, native
input, IME visibility, Apply/reload, Cancel and Back remain required.

## Evidence and limits

[Preserved failure and passing comparison](https://github.com/c933103/AN-Paint/blob/177b1b840bde630f3d873b544097a63be20895cb/README.md)
includes the original failing develop receipt and the successful PR150
comparison with the identical instrumentation-source digest. The failed
landscape tap had focus but no IME-show request, with nearby native popup
activity and system pressure. The exact popup owner/event mechanism is not
proved by those logs.

`tools/test_native_scroll_lane.py` executes the device test's real Java
geometry helper and its blocked-path controls. Host tests do not establish
Android dispatch, visual acceptance, or an installed-device pass. This is a
harness-hazard correction, pending exact-source device verification, not a
claim that a production IME bug has been proved or fixed.
