# Current Swedish catalogue evidence

Latest application head: `994e448a7cf424ee33439662956fe46b221ba3f4`.
Its current hosted merge combines develop `4feab3d6a13ac8c8e049393498ecf059ebd2f9d7`
with this head; all 1,263 leaf contents/modes match the locally checked composition.

Current source baseline: `d7436b3df842b9be9aa12be622ebc88ed8e8e2b9`.

The original independent review is preserved unmodified in `README.md` and
`independent-review.json`. It accepted 373 new current-source entries and
preserved 340 earlier bounded entries without new linguistic review. It also
independently read and accepted the complete corrected assembly Help proposal
relative to its explicit proposed English source, while holding released-source
binding until that source was integrated.

PR #122 has now integrated that exact English source. The entire merged English
value equals the frozen reviewed proposal, and the unchanged reviewed Swedish
value is now applied. `assembly-current-source-rebind.json` records this
mechanical author-produced source rebinding, not a second independent review.
The original full table plus this explicit one-entry replacement is the complete
current source/target/context record; no earlier receipt has been rewritten.

Initial bounded result before the later Curve correction:
- 350 newly added resources, including the complete crop plural.
- 8 repaired existing labels, and 16 unchanged formerly unknown entries reviewed.
- 374 newly reviewed current-source entries: 334 direct production-call-context,
  40 source-semantics-only.
- 340 earlier entries retained exactly, not newly rereviewed.
- 715/717 typed resources present; 714/717 bounded current-source wording accepts.
- 3 holds: dormant Main label, ambiguous legacy palette argument, dormant full
  manual awaiting its explicit complete English correction.

`source-correction-proposals-reviewed.json` preserves both full manuals proposals.
Only assembly Help is now rebound; the legacy manual proposal remains held.

`verify_current_source_rebind.py` checks all current source entries, bounded
application targets and explicit holds against a supplied checkout. Its passing
result is in `current-source-binding.txt`. `validation-summary.md` distinguishes
host tests from unavailable local JVM/runtime checks. These counts and checks are
not native-speaker, installed-layout, TalkBack or whole-language certification.

## Subsequent Curve hint correction

Codex review of PR #151 found that `fästa` incorrectly suggested attachment rather
than committing the current curve. `curve-hint-author-correction.json` records the
complete original and corrected pair, actual call path and review finding. The
replacement explicitly says to finish the curve before both bends are set. The
original independent receipt is unchanged, but its acceptance of this superseded
target is not carried forward. Current source/target evidence comprises the
original full table plus the assembly rebind and this explicit author correction.

There are now 713 unchanged bounded accepts (373 newly reviewed plus 340 prior)
and one author-corrected target awaiting new-head review. Presence remains
715/717; three unrelated holds remain. Source-binding verification checks all
complete target values including this explicitly labelled pending correction,
without turning structural verification into linguistic acceptance.

## Hosted JVM fixture repair

Hosted run [39412001502](https://github.com/c933103/AN-Paint/actions/runs/39412001502)
on `cafb244e8bd8342926d5696ce63a67860cb9b9ad` completed with two failures among
1,186 JVM tests (127 suites, zero errors/skips). The five other CI jobs passed.
The actual Swedish empty-credit text was correct, but its test still expected
English because it ignored the explicit family-specific review extension.
The Exact position fixture clicked before processing the queued OnShow handler
and did not select the app/process locale; its failure lacked a per-input label.
`jvm-fixture-repair.json` preserves the exact reports, source-backed diagnosis,
parser-probe limits and strengthened checks. It is author-produced test evidence,
not a replacement translation review or a claim that Android was rerun locally.

Application head `c8bf159e06cacf351407a0ac7cdd28a2a3e16b3f` changes only those two
JVM fixtures, retaining every application/translation value. The test now uses
the explicit reviewed locale family, selects/restores Swedish through the real
app path, drains OnShow before interaction, and checks retained invalid syntax,
localized errors, open-dialog state and unchanged project bytes on both axes.
The original independent receipt and the three genuine language holds remain.
`jvm-fixture-publication-receipt.json` records the expected-head lease and full
remote-tree comparison. Current-head Codex review and hosted run
[39427728235](https://github.com/c933103/AN-Paint/actions/runs/39427728235) have
started; only their eventual current-head results can close the runtime gate.

## Runtime repair verification and finite CI budgets

The finalized c8bf159 artifact verifies all 1,186 JVM tests passed, including both
repaired fixtures and the Curve button regression. All 1,066 Python tests were
reported OK with two skips. Nevertheless, Actions explicitly timed out Python
at 4 minutes and JVM at 12 minutes: their zero-exit command receipts took
250.311 and 773.047 seconds. The regression job's final conclusion was cancelled;
the available log does not separately prove why that aggregate state was chosen.
`hosted-jvm-repair-verification.json` preserves exact artifact identity, verified
SHA-256, full suite inventory, target results, timings and interpretation limits.
All five other jobs passed. This is runtime evidence, not a new linguistic review.

Head 994e448 keeps all tests and assertions while setting finite Python/JVM caps
of 8/20 minutes and a 55-minute regression-job cap. Explicit phase maxima total
50 minutes, with 5 minutes reserved for checkout/cache/evidence overhead. Device
interaction caps, strict compiler cache rules and failure propagation are unchanged.
`ci-budget-correction.json` records the measured rationale and strengthened finite
budget contracts; `ci-budget-publication-receipt.json` records both complete remote
trees and expected-head publication lease. All 56 CI contracts and the full
1,068-test normal host suite passed on the fresh combined source. The optimized
suite and [new hosted run 39434720839](https://github.com/c933103/AN-Paint/actions/runs/39434720839)
are pending. No earlier passing report is relabelled as a pass for this new head.
The original independent receipt, all production/translation values and three
language holds remain unchanged.


## Optimized host follow-up

The first optimized combined-source run completed 1,068 tests in 633.401 seconds
with three TimeoutExpired errors in subcases of the existing legacy CLI-omission
test. Each exceeded its unchanged 10-second subprocess limit; no assertion
mismatch was reported. This optimized aggregate is failed, not pending or passed.
The normal suite passed those same normal/-O/environment CLI modes. An unchanged
focused diagnostic is running; no host-load or other environmental cause is
claimed as established. `host-budget-current-develop-optimized-attempt1.log`
preserves the complete failure. The current hosted Python step independently
succeeded; JVM and later hosted stages are still pending.

The focused optimized legacy suite subsequently passed all seven tests unchanged
in 36.155 seconds, including every timed-out subcase with the original limits.
One full unchanged optimized confirmation run is now running. Focused success
does not relabel the failed aggregate or establish its environmental cause.


## Final local optimized limitation and current hosted regression

The second full optimized confirmation also failed: 1,068 tests in 764.947 seconds,
with three TimeoutExpired errors at unchanged 10-second subprocess limits and
no assertion failures. One is the legacy SDK24 -O CLI stale-report case; two are
native-scroll Java harness cases (fully obstructed path and horizontal geometry).
Both failed aggregates are preserved and no further retry or limit change is
planned. `optimized-validation-limits.json` records exact cases and distinctions.
The full local optimized aggregate is NOT PASSED; no environmental cause is claimed.

The current hosted regression job independently succeeded on exact merge d2785884:
all 130 JVM suites / 1,245 tests passed with zero failures/errors/skips. Python
reported 1,068 tests OK with two unrelated optional Pillow ICO-decoder skips.
Its legacy case explicitly exercised normal/-O/environment CLI modes, and all
three second-attempt error identities passed there. This does not certify the
whole local optimized aggregate. `current-head-hosted-regression.json` records
verified artifact SHA-256, source/merge identity, target results and timings.
Current-head Codex Code review is clean. The remaining required hosted jobs and
merge are parent-owned gates; no whole-language or release certification is made.
