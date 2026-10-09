# Terminal post-merge verification

PR30 merged as `0b3d737e19448c47d36deee8cebfffd5d40c1ea3`. Its actual Git tree is
`9a456494701a1e9fe46c401f389d16891f674311`, identical to accepted head 37da2a7.
The automatic develop-push [run 37952959651](https://github.com/c933103/AN-Paint/actions/runs/37952959651)
completed successfully on its first attempt. All three jobs passed; no rerun or
source change was needed after merge.

## Verified terminal results

- **716 JVM tests pass**, with zero failures/errors/skips; **lint zero issues**.
- **94 installed API35 tests pass**: 74 library +18 ordinary +1 accepted-credit
  restart seed +1 fresh-process verification, with no missing/unexpected cases.
- Ordinary instrumentation 162.953s; full ordinary runner **164.523s /180s**.
  No runner timeout occurred.
- CI Python 342 ran in 59.444s, with two optional Pillow decoder skips. Both were
  exercised by the accepted local 342 run; exact skip IDs remain in the receipt.
- Phase wall times: Python 59.619s, JVM 424.360s, lint 299.229s, exit 0 throughout.
  The accepted 2m/12m/6m split, 20m outer job and all required checks remain.
- All 810 JVM/installed case identities match the acceptance run. All 504 native
  gallery action/window/vertical files remain byte-identical to reviewed evidence.
- All four real French/Mongolian 2x viewport records are byte-identical to acceptance:
  full browser 320x120px portrait and 640x90px landscape, wrapped query 6/3 lines,
  actual Search EditorInfo 3, same Activity/browser/query through rotation.
- The real target timeout probe again returned 137. All five settings writes and
  five system-loop barriers returned 0; every barrier ended with drained loopers
  and final success. All five transitions, including restoration, ended with
  requested/persisted/system/target agreement. Minimum recorded remaining time
  after a command was 9,573ms of the original 10,000ms budget.

The downloaded regression archive SHA256 is
`e82ccf40f309fae7c9a4f5e899f4ab29f01645ab594d147f39076e4b26a9625b`;
the installed archive SHA256 is
`9bb2f37415f6c6617a6fa7cfa864de7248632e5e007921185c8c514349c02241`.
Both were verified before safe extraction. The manifest preserves all 1,019
constituent hashes, all 810 result identities, full relevant shell/configuration
records, phase times and exact merge identity. Full original Actions archives
expire 2026-10-23; this does not claim permanent archival of every ZIP byte.

## Unchanged scope and limits

The [accepted-head receipt](../font-barrier-ci-37da2a7/README.md) retains the Code
review and explicit Security-reviewed-head boundary. Post-merge CI is an
independent same-tree execution, not a new review or broader coverage claim.
All accepted PR31 translations and CI changes remain intact. The earlier
[c48f68b failure](../combined-ci-c48f68b/README.md) remains a failure; its historical
writer is not proven by this later passing run.

API30–33 still have explicitly weaker installed font synchronization; no equivalent
system-loop barrier is verified there. API30 native-host checks are not a current
installed API30 run. The all-language host matrix and real French/Mongolian API35
checks do not constitute physical-device, TalkBack, every-keyboard or fluent-
language acceptance. No held PR29 archive constituent is republished.
