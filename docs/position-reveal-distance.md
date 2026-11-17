# Position native reveal distance

The original failure in PR 514, run 43931683669, completed Manchu portrait
editing and Apply but exhausted its 45-second budget during landscape caption
traversal. Diagnostic run 43940788070 passed; its Manchu trace recorded 26 native
reveals totaling 22,739 ms injection and 2,690 ms settling. This is evidence of
expensive traversal, not proof of a production layout defect.

The previous planner moved the minimum hidden edge plus native touch slop on
each reveal. Consecutive 64 dp caption tiles could therefore each require an
expensive small swipe. The candidate planner uses leading-edge space when it
exceeds that minimum, without exceeding the existing native gesture lane.
The same tile is still checked for visibility after the gesture, and all tiles
are still visited. Narrow targets retain the original slop compensation. For a target nearly as
wide as its viewport, that inherited minimum can exceed leading-edge space;
this is not a universal no-overshoot guarantee. The unchanged visibility loop
must still establish success.

No application code, tile coverage, native input, editable-control avoidance,
focus/text side-effect check, IME assertion, gesture bound, or 8/45-second budget
is changed. The existing stationary-end swipe path is retained. Actual native
motion remains authoritative; the planner does not assume that the content
moves by exactly the requested displacement.

Host validation executes the real Java helper and checks bounds, overflow,
invalid geometry, tight targets and tile containment under a simple touch-slop
model. In that model the first portrait caption from the saved diagnostic
trace (20 tiles,221 x 320 extent, viewport x 38..282 and original x 153) needs one
candidate gesture instead of two. That is a geometric illustration, not an
installed-device reproduction or performance guarantee.

This candidate requires independent review and exact-head Android CI. Do not
call PR 514 fixed on the strength of host checks or one passing device run.
Ainu Kana's separate focus-without-IME failure remains unexplained. Its original
log has clickNoSync at 18:57:08.370, nearby popup activity and no keyboard-show
request; it predates the passive delivered-motion diagnostics and does not
establish why the tap failed to request the IME.

## First candidate device failure and correction

Run 44077666592 on first candidate 63e 613de passed Ainu and Manchu, but Tibetan
exhausted the unchanged budget. Artifact 14325209673 records native overshoot:
for landscape viewport y 115..212 and caption tile y 302..342 before scroll,
scroll 128 led to a 59 px swipe that moved 67 px to 195. The tile top was then 107,
above the viewport. Aggressive reverse alignment requested another 59 px,
oscillating roughly 128..195 until the deadline. This is a candidate regression,
not an infrastructure failure or a passing result.

The planner now lives for one target reveal and uses measured geometry to
notice a direction reversal. On the first reversal it disables lookahead for
that target and retains the original minimum-hidden-edge/slop correction.
Thus the 8 px overshoot requests 18 px correction instead of another 59 px alignment.
Later targets may use lookahead again. The existing visibility and gesture
bounds still decide success. Recorded-geometry and mirrored-direction host
controls reproduce the old planner's distance choice and check the corrected
sequence; real-device verification remains necessary.

The observed device overshoot supersedes any earlier interpretation of the
unit-gain geometry model as a native no-overshoot guarantee.
