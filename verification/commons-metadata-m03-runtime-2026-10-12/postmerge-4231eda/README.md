# M03 postmerge acceptance

PR [54](https://github.com/c933103/AN-Paint/pull/54) merged as `4231edaac45d89c52f51e2b77d0f94a1176ad88c` on 12 October 2026 at 03:11 UTC. Its tree `c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1` exactly equals reviewed head `d4ee9762580bbaf983fc58edb84755840c31626c`. Parents are the unchanged develop baseline `79b1f990a98eaf44c28351cd02c20157c70d8dff` and that reviewed head.

Fresh ready-triggered Code and Security reviews completed without findings at 03:08:54 and 03:09:45 UTC; the bot added its clean-result reaction at 03:09:48. [Review summary](https://github.com/c933103/AN-Paint/pull/54#issuecomment-6116030611). No review threads remain.

## Accepted checks

[Postmerge push workflow 38198762160](https://github.com/c933103/AN-Paint/actions/runs/38198762160) passed all four jobs on attempt 1, without retries.

- Hosted Python: 568 methods, **566 passed and 2 skipped**, 148.125 seconds. Local author aggregate: all 568 passed.
- JVM: 820 unique cases in 87 suites, no failures, errors or skips. M03 stream/callback flow 12; resource-routing tests 4 across API30/35.
- Lint: zero issues. Seven resource-generation probes passed, with every retained log hash verified.
- Installed API35: exact source-bound native inventory 74 passed; complete composed app inventory 25 passed, without exclusions or skips. Actual bundled-font hash and Typeface loading passed.
- Strict export replay passed: 104 data files, 32 matrix screenshots, 8 reachability cases and 64 supporting images.
- All 48 M03 Robolectric status PNGs are byte-identical to the reviewed premerge captures. The earlier independent visual review remains applicable within its stated scope.

## Python count correction

Earlier hosted summaries saying “568 passes” were inaccurate. Both premerge job `114624058307` (147.091 seconds) and postmerge job `114647221120` explicitly report `Ran 568 tests` and `OK (skipped=2)`. Their complete sequential progress strings are identical. Exact-source unittest discovery maps the two skip positions to:

1. `IcoContainerTest.test_adam7_fixture_pixels_match_independent_pillow_decoder`
2. `IcoContainerTest.test_export_opens_with_independent_pillow_ico_decoder`

Both explicitly skip when importing the optional `PIL.Image` dependency fails. Other source/test guards still execute. The Node-dependent method is not skipped. A fresh named local rerun with Pillow 12.3.0 passed both methods in 1.350 seconds; the original local 568-method aggregate also passed without skips. The two hosted omissions are not represented as hosted passes. Raw progress/summary excerpts, exact identity mapping and local recheck log are retained beside this report.

## APK and source binding

Artifact `11723893888` is the debug build for the exact merge and run. Its ZIP SHA-256 is `cbdae3799e03490647ab96ec13d5db87d080b49c1191dd2a0ed55ccaa34781b2`.

- APK SHA-256: `06d21bc20318e0f9bf2b3c523a6d59e80959f04a97eeb87225daf9947cb51891`
- Corresponding-source SHA-256: `50734244e9bd0bd9f647b2e565601ef73205b55a14f17cb7d8e905152307d0d2`
- Embedded source equals the delivered sidecar byte-for-byte. All 1,591 delivered tracked blobs match the accepted Git tree. The only absent tracked files are the two established Ant/Gradle `.gitignore` exclusions and explicitly excluded `.idea/codeStyles/Project.xml`; no production or M03 file is omitted.
- Additional archive members are confined to the four declared native-source prefixes. Their upstream sources are not separately recertified here.
- Packaged Nôm font SHA-256 is the reviewed `4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05`.

The raw Actions artifacts are identified and hashed in `acceptance.json`; they expire on 26 October 2026. This directory preserves bounded receipts, not a new full binary archive or release. The APK uses the CI debug key; upgrade signing remains separate.

## Retained limits and history

Default plus 59 scoped values and exactly 81 declared fallbacks retain their strict guards. Source-assisted independent review of the three added language paraphrases has moderate confidence; no native-speaker certification is claimed. M03 captures use Robolectric native graphics. Installed API35 tests cover actual font loading and broader app flows, not exact M03 screenshots. Manchu double-scale stills show the trailing scroll position, so offscreen columns are not visually certified. New Nôm glyph pixels differ from the full source font at 24px despite matching outlines/metrics; universal pixel equivalence is not claimed.

These are scope disclosures, with no demonstrated remaining M03 defect or failing acceptance gate. The premerge first collector failure and its single successful failed-job-only retry remain preserved in the parent evidence directory. This bounded completion does not close M02, M09, broader localization/reset obligations, release work or unrelated holds.
