# Advanced Colour short-landscape corrective work

## Baseline replay, before production changes

Untouched application source is develop `691f8870649a1d21d1441f4e3d0e795660b23e9a`,
complete tree `040a35f40a6e8e143c6a9b2121e804f0704dd5d1`. The first commit contains
only the installed test harness, host contracts, and this evidence record. No
application production file is changed.

The original positive method from `df214fee4f106c4365325412b4f9d3c8530232d5`
is retained byte-for-byte under its original class/method identity. Its original
fixture, font-transition sequence, native pointer helpers, timeouts and assertions
are retained. The two unrelated About/credit test methods are omitted from this
isolated replay. The current bounded app-owned export rule and the font helper
wrapper are carried over from PR49. A source digest is passed by the ordinary
runner. The existing API 35 app phase includes this additional method; API 30
explicitly suppresses it. All prior app methods remain required.

The only positive-test helper change observes dialog, native panels, holder,
editor, overflowing content and fixed-control bounds at the original viewport
wait boundary. It captures an image before the original method's finally block
can dismiss the dialog, on both success and timeout. Measured dimensions must
match the original API 35 640×320 landscape, density 1, en-US, font 1× configuration.
A timeout remains a failed test. There is no ignored test, longer wait, fallback
oracle or negative characterization substituted for acceptance.

Raw app-owned ZIP evidence is pulled in the EXIT collector after success or
failure, with an additional 15-second command and 3-second kill grace. Existing
36-minute device-step and 46-minute job ceilings still admit the source-bound
controlled path: maximum 2087s + 60s operational allowance = 2147s (< 2160s).
This arithmetic excludes universal filesystem/runtime guarantees. The API 35
composed suite cannot be green unless the unchanged positive case also passes.

At the initial harness publication, the installed baseline result was pending. Source contracts alone do not prove the
native allocation, usability, pointer route, state preservation, or any repair.
The original failed run 38109511511 and its archived fixture remain failures.
Once this untouched-base replay is established, a separate production change
will keep the original positive acceptance requirements and add state/large-text
coverage as supported by actual results.

## Untouched-base gate established

[Run 38112708313](https://github.com/c933103/AN-Paint/actions/runs/38112708313)
reproduced the original positive assertion failure on unchanged application
source. The native holder measured 384 × 138; its editor measured 360 × 0 while
containing 470px of content. The 48px Add button had only 25px visible. The original
API 35, 640 × 320, density 1, en-US, font 1× configuration was measured. All 487
tracked production files in the matching source ZIP were checked byte-for-byte;
the APK and source hashes match build-info.json. The focused archive and exact
source binding are in `baseline-run-38112708313/`. This supersedes the earlier
pending replay status, without granting any usability credit to that failure.

## Candidate correction, installed verification pending

The horizontal-language picker uses a wider native window in landscape when the
current visible frame can accommodate it. The same retained editor controls and
fixed palette/preview/Add controls become sibling columns. Portrait keeps a
vertical stack. Measurement reads the live configuration; the existing native
title and action allocation still constrain the custom body. No title/footer,
colour math, field-validation, preview or commit callback is replaced.

The saved-colour grid retains all sixteen original view objects while changing
between sixteen landscape columns and eight portrait columns. No fields are
recreated during rotation, and the width listener is removed on dismissal.
Window width is bounded by the current visible frame and 900dp. Native vertical
script dialogs keep their existing separate form and window path.

The original positive installed method remains unchanged. A distinct installed
case adds same-dialog rotation, draft/selection/wheel-mode retention, all sixteen
finite portrait slots, real horizontal reachability of the final slot, actual
IME appearance and native Back dismissal, Cancel, reopen, invalid submission and
one valid commit. The IME may cover controls or use its extract view: this does
not claim simultaneous field/footer visibility while the keyboard is showing.
The normal controls must be reachable again after keyboard dismissal.

Native-rendered JVM tests cover landscape ancestor bounds, all portrait swatches
and the separate vertical-script form. The prior 1×/2× diagnostic is retained
with its acceptance-comment corrected. Large-text 2× remains diagnostic; a
captured image or a passing diagnostic is not a usability pass.

The ordinary installed phase keeps its 180-second ceiling. The baseline phase
used 139.949 seconds including its failed viewport wait; the new state case must
fit the actual aggregate runtime, not merely its own 45-second interaction limit.

### Corrected native gesture route

Source review found that `ColourSurface` deliberately owns drag gestures by
calling `requestDisallowInterceptTouchEvent(true)`. A centre-of-viewport swipe
can therefore edit colour when the restored viewport shows that surface. Making
its parent steal the drag, or shrinking the viewport to move the test coordinate,
would damage the interaction rather than establish scrolling.

The candidate adds a persistent native scrollbar with a 32dp end gutter, mirrored
for RTL. The installed helper uses the measured gutter only when its target is
the colour ScrollView. Other pointer helpers, the original positive method body,
and its viewport/overflow/real-scroll/fixed-bounds/Cancel/no-commit assertions stay
unchanged. The original source and original gesture remain unmodified in the
historical fixture and untouched-base archive; the successor helper is explicitly
different and is not claimed byte-identical to the original route.

The separate state case also reveals the actual colour surface using native
scrolling, drags on its visible area, and requires the colour value to change
without moving the editor ScrollView or committing. It verifies that native
accessibility exposes scrolling actions. This is pending installed verification;
source preservation and a host contract alone cannot establish that these two
real input routes work.

The successor native scroll gesture keeps both pointer endpoints on the measured gutter x-coordinate, so it is a vertical drag rather than crossing into the colour surface. The source-preservation comparison explicitly normalizes both endpoints back to their historical centre coordinates.

## First candidate outcome and caption/state successor

[Run38115531753](https://github.com/c933103/AN-Paint/actions/runs/38115531753)
passed the original positive viewport case on installed API35: editor364×86,
content470px and a real gutter swipe from scrollY0 to55 with fully visible fixed
controls, native Cancel, one close and no commit. Its separate state case failed
on the reopened-picker UiDevice.pressBack event-wait Boolean; final close-state
and invalid/valid commit checks were unrun. Ordinary18/18 completed in152.365s
without timeout; restart was correctly withheld. All814 JVM methods, lint,
production/test APK compilation and generation passed, but that is not a full
installed-state or usability acceptance. `candidate-run-38115531753/` preserves
raw exports, all original captures/reports and exact source/APK bindings.

Pixel/intrinsic review additionally found Hungarian1× Add-caption clipping in the
new side column and a portrait Honeycomb caption clipped by the baseline-identical
44dp tab construction. The next narrow correction uses intrinsic wrapping heights
with unchanged44dp tab/48dp Add minimums, never smaller fonts. Strict SDK30/35 model
coverage checks every main/submode caption and Add for en-US/hu in portrait and
landscape. A short additional installed Hungarian1× case checks these same captions
and actual Cancel/no commit. The ordinary phase still has180s for all19 methods.

The next state harness uses the exact native Back helper pinned from PR49
d7f1a958: one pressKeyCode(KEYCODE_BACK) DOWN/UP pair, then a new exact target-window,
focus, value/selection and callback outcome recorded before cleanup. The first
trial remains failed; merely changing the key helper grants no acceptance.
The prior IME flag was captured before native onShown and its PNG had no rendered
keyboard. The successor requires a positive IME inset stable for250ms before the
screenshot and one native Back that hides it while retaining the same dialog,
field, draft, selection and zero commits/closes. Reopened-dialog Back instead must
detach that exact root, restore editor focus and produce exactly the second close
without committing. The complete invalid/valid commit sequence must then pass.
Large-text2× still has observed clipped captions/preview and remains unaccepted.

Successor local checks:552 full host tests pass;15 focused inventory/source cases
pass after correcting the local PYTHONPATH invocation (the original import-error
log is retained). Six source contracts also pass under PYTHONOPTIMIZE=1. These are
host checks only; fresh exact-head Android results remain required for the
intrinsic captions, rendered IME and complete native Back/commit outcomes.

## Caption trial and row-alignment successor

Run [38118041931](https://github.com/c933103/AN-Paint/actions/runs/38118041931)
at head `4750d62f` / tree `912a21a7` remains failed. All 814 JVM methods completed;
the two API30/35 portrait Honeycomb whole-view checks found 51px height with only
48px visible. Lint and 812 other JVM methods passed. Hungarian 1× landscape Add
intrinsic sizing improved, but no model image grants installed acceptance.

The installed trial never reached colour UI: all three colour cases failed at the
unchanged initial-editor gate, with black pre-restoration screenshots. Subsequent
gallery/vertical startup fixtures also failed. The root cause and specific failed
gate conjunct are not known; RESUMED/Displayed logs alone do not prove a usable
editor. `caption-run-38118041931/` preserves the original failures and exact binding.

The next narrow production change disables baseline alignment on both tab rows,
retaining intrinsic wrapping and minimum touch sizes. Read-only startup snapshots
are added before the original wait and at its pass/failure boundary, before cleanup.
The fixture body, positive method, startup condition, real input and deadlines remain
unchanged. No activity retry, forced startup/focus or broadened acceptance is added.

## Row-alignment result and fullscreen-IME oracle successor

Run [38119879923](https://github.com/c933103/AN-Paint/actions/runs/38119879923)
at head `b56d769f` / tree `1c2da141` passes all 814 JVM methods, lint, build and
generation. Installed positive viewport and Hungarian caption/Cancel cases pass.
The latter portrait image has a temporary system clipboard preview; it is not an
unobscured portrait-use proof. Startup succeeds without any startup production
change; the prior blank-screen root cause remains unknown.

The one state failure is the positive-dialog-IME-inset assumption. Actual pixels
and native onShown prove a fullscreen extract keyboard, which Android's primary
source explains can leave the underlying app unchanged. `ime-run-38119879923/`
preserves the original failed gate and all source-bound results. Back, later
Cancel/reopen and final invalid/valid commit remain unrun in that trial.

The next test-only helper requires an actual configured TYPE_INPUT_METHOD window
with visible nonempty root/bounds stable for 250ms, then unchanged one-Back exact
state outcomes plus stable native keyboard absence. It records/captures success
and failure before dialog cleanup. Insets remain observations for fullscreen
extract mode. Hungarian capture also awaits the platform clipboard preview's
verified natural absence. No production input-mode, permission or deadline change
is introduced. Fresh complete native outcomes and pixel review remain required.

## Full state pass and final portrait-capture correction

Run [38122366555](https://github.com/c933103/AN-Paint/actions/runs/38122366555)
at head `c711d0c0` / tree `89c3c199` passes all 102 installed methods, 814 JVM
methods, lint, build and generation. All three colour methods pass: native
configured fullscreen IME is visible while the dialog inset is zero, one Back
hides it with the same field/value/selection and zero callbacks, reopened Back
detaches the exact window, invalid submission is rejected and one valid submission
commits `#2468AC` (one commit, three closes). Ordinary19/19 takes152.178s under180s;
the complete state case takes16.435s under45s. Original raw evidence is retained.

Pixel review still finds the temporary clipboard preview on the Hungarian portrait
capture. Its AccessibilityWindowInfo-title absence guard did not observe the
visible overlay and grants no acceptance. The final test-only correction removes
that ineffective guard and performs the same two required orientations in
landscape→portrait order, ending with actual portrait Cancel. The fixture already
starts portrait, so the first real rotation dismisses the platform clipboard
preview through normal Android behavior. Android15 ClipboardOverlayWindow.java
onConfigurationChanged invokes its orientation callback; ClipboardOverlayController
lines198–201 call hideImmediate. No clipboard mutation, other-window dismissal,
blind delay, production change or weakened geometry/callback assertion is added.
The next exact-head portrait PNG and native Cancel must still be checked; green
checks alone do not prove that capture is unobscured.
