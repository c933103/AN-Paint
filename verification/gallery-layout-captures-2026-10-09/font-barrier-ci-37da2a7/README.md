# Combined gallery acceptance with real system-loop synchronization

Source head `37da2a7806cc09185b1fc097104068a74bbe00d2`, tree
`9a456494701a1e9fe46c401f389d16891f674311`, passed all three jobs in
[run 37950555176](https://github.com/c933103/AN-Paint/actions/runs/37950555176).
Tested merge `68cec7c4b0f85cdab4e8e2e30347f7196af3b4ac` has the identical tree.
All 1,245 remote tree leaves were independently matched to local Git.

## Exact results

- APK/source and instrumentation compilation passed.
- **716 JVM tests passed**, zero failures/errors/skips; **lint zero issues**.
- **94 installed API35 tests passed**: 74 library +18 ordinary +1 restart seed
  +1 fresh-process verification. No missing/unexpected cases or runner timeout.
- Ordinary instrumentation: **158.040s**; full runner: **159.496s /180s**.
- All **1,680** catalogue cases passed. Four matrix JUnit executions: 18.599s.
- All **72** Activity reachability scenarios passed. Eight executions: 13.111s.
  The four vertical/status executions passed in 3.347s. Existing full status,
  native semantics, live query, wrapping, scrolling and rotation checks remain.
- All **504** action/window/vertical files are byte-identical to the reviewed
  03abccd captures. The evidence equivalence compares every constituent byte.
- Python: 342 local tests passed without skips in 52.717s. CI ran 342 in 57.389s,
  with the same two optional independent Pillow decoder tests skipped. Both
  executed locally. Exact IDs and reason are retained in phase-timings.json.
- Split phase wall times: Python 57.596s, JVM 353.330s, lint 226.198s, exit 0 each.
  Accepted 2m/12m/6m phase budgets and 20m outer job remain unchanged.

## Actual target protocol, not only a host model

The installed API35 artifact records **11 shell commands**: one support probe,
five setting writes and five system-loop barriers. The real target's decimal
SIGKILL timeout probe returned 137. Every write and barrier returned 0 with empty
stderr; every barrier reports drained loopers and a final passed barrier.
Some barrier outputs include intermediate pending-broadcast diagnostics before
that final success; the complete output is preserved rather than removed.

All five transitions end with requested/persisted/system/target agreement,
including both locales' 1x-to-2x setup and final restoration. The smallest
remaining budget recorded after a command was 9,726ms of the original 10,000ms.
The real assertions retained one write and one absolute deadline per transition.

French and Mongolian each passed real 2x portrait and landscape layouts with:

- Full visible browser reserves of 320x120px and 640x90px respectively.
- Six portrait and three landscape wrapped query lines.
- Actual EditorInfo.imeOptions=3 (Search), no NO_ENTER_ACTION flag, and multiline
  inputType 131073.
- The same Activity, WebView and query retained across rotation, followed by
  exact locale/preference restoration and verified browser destruction before
  the rejecting process-local proxy is restored.

These are installed provider/layout observations. Host frame shadows and queue
models do not substitute for them. No physical-device, TalkBack, every-keyboard
or fluent-language acceptance is claimed.

## Preserved boundaries

The [first combined failed run](../combined-ci-c48f68b/README.md) remains a failure:
its Mongolian setup timed out and both restart tests were never run. AOSP's
asynchronous write-back is a source-supported explanation, not a proven trace
of that historical writer. This passing run validates the corrected protocol;
it does not retroactively reclassify the failure as harmless.

API30–33 retain explicitly weaker legacy synchronization. This API34+ fixture
correction does not establish an equivalent system-loop barrier on those APIs.
The [source-linked analysis](https://github.com/c933103/AN-Paint/blob/37da2a7806cc09185b1fc097104068a74bbe00d2/verification/gallery-layout-2026-10-09/review-font-writeback.md)
separates framework evidence, deterministic sensitivity and installed acceptance.

All 94 accepted PR31 paths, including translations and the CI phase split, are
unchanged. The four-file correction after integration affects only the installed
fixture, host tests and evidence. Production source is byte-identical to the
previously Code-reviewed combined head.

[Current-head Codex Code review](https://github.com/c933103/AN-Paint/pull/30#issuecomment-6083834035)
found no major issues. All three previous P2 threads are resolved. The distinct
Security summary remains at 9bbfad5, and no current-head Security result is claimed.
The complete lineage/review boundary is preserved in its JSON; root owns merge.

Both original ZIP hashes were verified before safe extraction. The manifest
retains all 1,019 constituent hashes and the result inventory all 810 JVM/installed
case identities. Full Actions archives expire 2026-10-23; this receipt is not a
claim of permanent archival of every ZIP byte. No held PR29 constituent is
republished, and no new duplicate PNG upload is needed.
