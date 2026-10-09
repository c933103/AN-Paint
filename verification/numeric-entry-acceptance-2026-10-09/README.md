# PR #27: final-head verification receipt

Recorded 9 October 2026. This evidence-only branch preserves results for the
[AN-W04 numeric-entry and API21 dialog correction](https://github.com/c933103/AN-Paint/pull/27)
without changing its reviewed code head. It was merged at
`5bf82b67199aaecbd341a8b150a887f8d60b5567` (06:50:08 UTC). The accepted merge
tree equals the candidate and tested-merge tree below. The automatic
[post-merge run 37895625554](https://github.com/c933103/AN-Paint/actions/runs/37895625554)
was still running at the initial receipt. It subsequently passed all three jobs
at 07:05:07 UTC: 661 JVM tests, lint 0, and 89 installed API35 cases. Its separately
verified archives and full evidence are retained in the [post-merge receipt](post-merge/README.md).

## Exact source and outcomes

- Candidate: `4f2eb8c5ad090dc3590f3f21db82ff2aa9c72abd`.
- Base: `f68807257ec61c71ac119425d26c109124a18792`.
- Candidate and tested-merge tree: `05f9f6aa330f2f1432264938d5d0e41dfe8d86ee`.
- Tested merge: `c7ba3e7ccd7e069292032b87e537a41e36230dd2`.
- [Run 37893883069](https://github.com/c933103/AN-Paint/actions/runs/37893883069):
  all three build, regression/lint and API35 emulator jobs succeeded.
- Local Python suite: **310 passed**, no failures, errors or skips.
- JVM suite: **661 passed**, no failures, errors or skips. The new numeric-entry
  class contributes **35 executed cases** across SDK21/25/30/35; it covers all
  140 picker tags in both numeric modes, actual editable insertion in all seven
  routes, existing validation, repeated modes, cancel/reopen, accessibility
  metadata, and controlled restart/dialog ordering.
- Lint: **0 issues**.
- Installed API35 suite: **89 passed**, no missing, unexpected or unsuccessful
  cases: 74 library, 13 ordinary editor, one accepted-credit seed and one
  post-force-stop verification. These are the existing installed regressions.
- [Code and Security reviews](https://github.com/c933103/AN-Paint/pull/27#issuecomment-6075105519)
  both completed on this exact head after the draft was marked ready. Code
  completed at 06:45:57 UTC, Security at 06:47:12; the bot's clean-result reaction
  followed at 06:47:17. No open review thread remains. The earlier IME finding
  was fixed and its regression passed; the prior
  [explicit clean code review](https://github.com/c933103/AN-Paint/pull/27#issuecomment-6075701399)
  also covers this head.

## Retained, reproducible evidence

`acceptance.json` records source, totals, original artifact SHA-256 identities,
file byte counts, SHA-256 and Git blob hashes. `ci-jobs.json` and `reviews.json`
retain the observed CI/review receipts. The original regression and API35 ZIPs
were downloaded and their GitHub SHA-256 digests independently verified.

- `unit-and-lint-xml.zip`: all 67 original JUnit XML files plus the lint XML.
- `unit-and-lint-manifest.json`: complete retained XML inventory and hashes.
- `device-results.zip`: all four runner summaries, their JUnit XML and raw
  instrumentation output. Full emulator/logcat logs are not republished here.
- `device-manifest.json`: retained device-file inventory and hashes.
- `all-device-cases.json`: every installed case and its runner summary.
- `focused-unit-cases.json`: all 35 new numeric-entry test cases.
- `host-python.log`: complete local suite output. Its `success: false` fixture
  records are expected negative-control output from passing runner tests; the
  actual unittest summary is `Ran 310 tests` / `OK`.

Run `python3 verify_results.py` here. The checker validates retained file and ZIP
entry hashes, inventories, full JUnit case totals, zero lint issues and each
installed runner's complete successful inventory. It does not rerun Android.

## Failed iterations and evidence limits

The [candidate evidence directory](../numeric-entry-2026-10-09/README.md) retains
the baseline API21/25 framework probes, 140-tag tables, original failing tests,
the API21 lifecycle reproduction and exact upstream source identities. The first
Android regression run had 656 cases with eight failures. The next iteration's
API21 attached-font control exhausted memory and reached the unchanged timeout,
so it has no completed unit total. Neither failed run is relabelled as passing.

The final narrow API21 test shadow models AOSP's family/style Typeface identity
cache. The original failing dialog order and repaired order use the same shadow
and real app theme, including French, Arabic, Nôm and Manchu; stable identity,
actual bold/italic changes and the default-shadow counterexample are asserted.
No locale or test was skipped, and no heap/timeout or production typography was
changed. This is source-backed host modelling, not native glyph rasterization.

New locale-specific entry checks use Robolectric. Direct framework probes use
host locale data. Neither establishes physical-device, real-IME, linguistic or
all-language layout acceptance. The built APK/source artifact was observed but
was not independently downloaded or upgrade-signed. The separate post-merge receipt establishes the completed automatic run; no
release is claimed. Broader AN-W04 work remains open.
