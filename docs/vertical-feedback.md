# Foreground vertical feedback

Vertical resource contexts (`mn-Mong`, `mnc-Mong`, `lzh-Hant`, `en-XV` and the
`qaa-Zsye-XV` test profile / exact-script resource alias) use the shared full-text
column viewport for foreground API30+ messages and API26+ tooltips. Direction
comes from the view's resource context, not the process-default locale.

- Fitting messages remain touch-transparent and use accessibility-adjusted timeouts.
- Overflow is retained until explicit dismissal, replacement or loss of its owning
  window. Once retained, a later reflow does not start a new expiry timer.
- Horizontal column scrolling and vertical scrolling of indivisible shaped words
  keep the original text. The complete logical text remains accessible.
- The dismiss action is outside both message scroll rails. The full localized
  caption is shown when it fits. Constrained windows use a 44dp close icon with the
  complete localized dismissal accessibility name, not a clipped caption.
- Decoration shrinks first. If a usable message viewport and dismiss target cannot
  fit, the same card is retained invisibly and revealed when safe space returns.
  This is deliberate visual deferral, not a claim that accessibility-only text is
  visually complete. No overflow notification is silently converted to a toast.
- Only gestures beginning inside a visible retained card are captured. Outside
  drawing and the editor's keyboard focus retain their existing targets.
- Tooltips are anchored ordinary children of the same window, bounded by the
  visible frame, system bars, cutouts and IME. Dialog anchors stay in their dialog.
  Unchanged caption assignments preserve pending hover dwell and existing cards.
- Horizontal/Wu/Nôm native-tooltip routes and explicit drawing fonts are unchanged.
  The editor's four explicit Help actions remain distinct from tooltip display.

## Verification boundaries

`VerticalFeedbackViewTest`, `VerticalNotificationTest` and
`VerticalTooltipOverlayTest` cover profile/resource identity, 1×/2× portrait and
landscape measurement, both scroll gestures, complete accessibility text, fixed
controls, compact/deferred geometry, unchanged-caption refresh, hover, timeout,
replacement, window/detach lifecycle, dialog ownership and synthetic IME bounds.
`LocaleTooltipControlsTest` additionally exercises the actual editor Help routes
and the canvas Text-tool callback’s real input connection while feedback is shown,
including input-focus and drawing-typeface preservation.
Existing horizontal, font and notification lifecycle tests remain in place.

The older resize characterization now checks the enabled foreground route. Its
horizontal geometry/deadline/observer diagnostics explicitly choose a horizontal
resource wrapper; exact-pixel negative controls are retained unchanged. This patch
does not change `VerticalText` shaping or resolve its known unsupported-ZWJ
ink-bounds counterexample. Logical text/scroll reachability is not a pixel-level
glyph-containment or linguistic-acceptance claim.

Local Gradle bootstrap could not download its pinned distribution because the
network was unreachable. Initial hosted head `fbee93e` compiled, but its JVM
aggregate failed nine of 1,237 test instances in five methods. The unmodified
failure XML and corresponding dialog pointer/capture evidence are preserved
[under an immutable evidence commit](https://github.com/c933103/AN-Paint/blob/5f625f3bc7ca221c8a0ae07a296a771f41fc392b/verification/vertical-feedback/2026-10-20-fbee93e-failures.zip).
Those failures are not retrospectively counted as passes:

- Pinned [Robolectric 4.14.1’s Activity shadow](https://github.com/robolectric/robolectric/blob/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowActivity.java)
  returns a manually assigned `currentFocus` field, not framework view focus.
  Tests now establish and verify the actual decor hierarchy focus before and after
  adding feedback; they do not populate that shadow field.
- Native View accessibility initialization returns early while unattached. The
  narrow emoji close-button case now mounts the hierarchy and checks its full
  accessible name, visible 44dp bounds and delivered accessibility click action.
- The original short English resize fixture never overflowed. Its replacement
  explicitly proves initial overflow before checking sticky persistence after fit.
- At 2× on API30, Copy’s localized confirmation can itself overflow. The dialog
  test now verifies and dismisses that visible feedback through root-dispatched
  pointer input before the underlying Done action. Fitting feedback remains in
  place during Done, retaining the touch-transparency check.

These harness corrections do not change production layout or relax full-text,
focus, reachability, accessibility, timeout or pixel-negative-control assertions.
A fresh exact-head hosted result is required for the corrected tests; local
Python contracts cannot certify them. Simulated IME insets and input connections
are not a physical keyboard or TalkBack session. No verified release is claimed.
