# M02 exact-head CI and rendered-status acceptance

Bounded item **AN-W05-METADATA-M02**, [draft PR47](https://github.com/c933103/AN-Paint/pull/47). This evidence-only branch preserves results without changing the tested source head. No release, merge, whole-language completion, or competent-language approval is implied.

## Archive publication status

**Raw archive copying is incomplete.** This branch durably publishes the small receipts, checks, exact hashes, generator artifact and ten reviewed contact sheets. It does **not** contain `current-api35.zip`, `current-scoped-regression.zip` or `initial-scoped-regression.zip`; those three locally verified archives remain pending. Their expected byte hashes and sizes are recorded in `publication-status.json`. All 40 unmodified current M02 PNG/JSON pairs remain available in the original [regression Actions artifact](https://github.com/c933103/AN-Paint/actions/runs/38099501387/artifacts/11686269936), subject to Actions retention. The committed contacts show all 40 status crops; they are not substitutes for full originals. Do not describe raw ZIP archival as complete.

## Identity and gate result

- Source head: `a8074c5c4f3b76767f479c6716d823e61ab06aed`; source tree: `b93546e32cf5ae300eaf09ee64813606f22fd4a0`.
- Original implementation base: `2c1bd8622eb6c57444eee8f816194b309fff136e`.
- [Run 38099501387](https://github.com/c933103/AN-Paint/actions/runs/38099501387) tested merge `c84566f75928362e3401029869019e57fec985f0`, tree `9408017c3e0cdb1403b254d2aea5e950f99f7205`.
- Actual Git merge parents are current develop `691f8870649a1d21d1441f4e3d0e795660b23e9a` and source head above. Develop was read back at 2026-10-11 01:09 UTC. The PR metadata's stale `base.sha=11559a8...` is not used as the tested-parent oracle.
- All 1,535 composed leaves match the source delta plus accepted upstream release-only changes. No changed-path overlap with that upstream delta. See `manifest.json`, `acceptance-inputs.json`, and `github-state.json`.
- Four current-head jobs succeeded: build/source, exact-script generation, regression/lint, and API35 emulator. [Code review](https://github.com/c933103/AN-Paint/pull/47#issuecomment-6103894949) reported no major issues for the corrected head. PR remains draft and unmerged; the owner coordinates the remaining transition/merge gate.

## Independently checked results

| Check | Accepted evidence and limits |
|---|---|
| Host contracts | Corrected source: 516 passed, zero skips, 149.539 s. Hosted composed tree: 552 total, 550 passed, two inherited optional-Pillow ICO skips. |
| JVM | All 813 cases in 87 XML suites passed; zero failures/errors/skips. Exact 804 inherited plus 9 M02 case identities verified, not merely totals. M02 resource resolution covers all 140 offered tags on API30 and API35. |
| Lint | Zero issues in raw XML. |
| New UI capture matrix | All **40 PNG/JSON pairs** present: 10 language/script profiles × Copy credit/insertion × actual font scales 1 and 2. Every original is 640×1280 and all 40 decoded pixel hashes differ. Actual pixels inspected in ten lossless contact sheets. See [visual observations](VISUAL_REVIEW.md). |
| Installed API35 | All **99 methods**, 74 native and 25 app, match exact source-declared selections and raw protocol/XML, with no failures/skips. Process restart boundary, cold gallery process and exact-script rotation verified. These are inherited installed regressions; the new M02 statuses are covered by Robolectric, not a new installed-device status fixture. |
| Existing vertical evidence | All 96 inherited captures decoded and inventories/transport hashes matched; 28 native drag traces have DOWN/MOVE/UP, no CANCEL, stationary ancestors and clean observer removal. These original UI pixels were not visually reaccepted in this M02 pass. The receipt explicitly retains that distinction. |
| Generator | Seven exact clean/incremental/input-mutation/restoration probes and their log hashes verified; generated Korean bytes match the canonical resource at the tested tree. |
| APK/source | Build identity matches tested merge/run; embedded and separately delivered corresponding-source ZIPs are byte-identical. All 1,532 included Git source blobs checked; only three declared tracked omissions (`.gitignore`, `.idea/codeStyles/Project.xml`, `colorpicker/.gitignore`). Four declared bundled upstream-native source prefixes are inventoried, not individually recertified. |

The debug APK SHA256 is `f38b709e14b8fd25aa0cec5c15b099a61d0495b39bd127130ced3ce5ab44aef0`; corresponding source ZIP SHA256 is `05c366941a33636cd149dc3e0e26133b37bdd21b8f4a69cd7b6355590dbfe565`. It is a CI debug-signed build, not a release/upgrade-signing assertion.

All CI phases retained their existing deadlines: Python 161.867/240 s, JVM 491.969/720 s, native prep 78.548/360 s and lint 112.874/360 s. Installed ordinary/gallery phases took 118.624/180 s and 44.027/90 s; the two vertical shards took 114.462/180 s and 108.524/180 s; seed/verify 5.983/60 s and 7.136/60 s; native tests 65.726/180 s. No budget was relaxed.

## Original failure and correction

Initial head `9f985b7a144fd49cb33a87ba5a5a73fc7be84a2b`, run [38098843107](https://github.com/c933103/AN-Paint/actions/runs/38098843107), tested merge `82399d103426b45633d87bd54fddb1132d61d7f3`, tree `86aae7b0903edd98da675e4c9177d06f8920fae8`: 813 JVM cases ran, 812 passed and the double-scale M02 case failed before application setup because Robolectric 4.14.1 rejects the `fontScale200` qualifier. Later lint/device stages were cancelled by synchronization, not accepted.

The correction uses `@Config(qualifiers="w320dp-h640dp-port-xhdpi", fontScale=2f)` and adds a host guard preventing regression. Only the new flow test, M02 host guard and three follow-up evidence files changed. Production/resources remained byte-identical. The original failed XML, all initial 87 JVM suites, 20 produced normal-scale M02 pairs and phase logs remain in the prepared, pending `initial-scoped-regression.zip`; `initial-jvm-failures.json` identifies the failure. Initial build/source checks remain historical, not substituted for current acceptance.

## Replaying, durable receipts and pending archives

- `original-artifacts.json` records original GitHub artifact IDs, byte counts and SHA256 values. Current artifact hashes are: build `50c5f02ab6d56acee0f4b96f6e9c6242a477b16ad945106c187ebede02d29908` (153,938,699 bytes); regression `52d80848b144542992ad4d870aff9423289af1a2fffe3c68850856a85d56e5c7` (38,205,620 bytes); generator `a978cf247ff17adb2f76dcf000f3d5fd00f847cc6133c48dafd87aaa66762729` (6,173 bytes); API35 `7e3ea435336ca78847b4b322ae6c8132a197212d9088afb73aee245276d25ea8` (8,128,049 bytes).
- The prepared, not-yet-committed `current-scoped-regression.zip` preserves all 87 JVM XMLs, all 40 **unmodified original** M02 PNG/JSON pairs, lint XML/text and full phase logs/timing records. It is deliberately a derivative, not the original 38 MB artifact; member hashes are in `current-scoped-regression-members.json`.
- `current-api35.zip` (pending) and `current-generator.zip` (committed) are unmodified original artifacts. Contact sheets only crop the lower 320 pixels of each original for convenient status comparison; they do not resize/repaint the application pixels.
- `verify_ci.py` verifies build, generator, regression and device modes. Supply `--source` as a checkout of the tested source, `--manifest manifest.json`, and an empty `--directory`. Device mode additionally takes `--sdk 35`. The source `tools/` helpers used here are unchanged between PR head and tested merge. For regression, the prepared scoped ZIP contains all required inputs; use the original Actions regression artifact until its archival copy is available. Its archive hash intentionally differs from the original receipt's hash. Extract that ZIP into `regression/`, then run `inspect_m02_captures.py` for the exact capture inventory/contact sheets. Pillow is required for decoding.
- Build/source bytes remain at the Actions artifact link, subject to Actions retention; the large build ZIP is not duplicated into Git. Source commits/tree, `build-info.json`, source manifest and exact artifact hashes are durable here. Existing full source and source verifiers are in Git.
- `SHA256SUMS` covers every committed evidence file except itself, excluding the three pending ZIP copies. Receipts distinguish source assertions, raw execution evidence and visual/native-language limits.

## Remaining independent obligations

Only M02's application-owned reason is changed. HTTP status retains exact ASCII digits; both action wrappers and untyped/provider details retain their established behavior. Per-tag dispositions remain [59 scoped entries plus 81 deliberate missing-key English fallbacks](../all-language-dispositions.json). The 50 target-language/script proposals have no competent/native review; English/symbolic conventions are separately identified. M01 and M03–M12 remain open. The reset register is still **475 total / 3 structural completed / 472 pending**. No full-language, physical-device, accessibility-service or release acceptance is claimed.
