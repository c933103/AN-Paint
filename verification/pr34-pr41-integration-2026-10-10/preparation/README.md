# PR34 / PR41 partition integration preparation

Status: published at `739a3dcf1a59785d98a5f5a00f4b76a1b00e6472`; fresh combined review and installed CI remain pending.

The preparation history below remains scoped to its original checkpoint. Publication used actual develop `a758daceda1d4fc37c605e50715f892557da9fc8`, whose verified tree exactly matches the accepted PR41 input. Both parents are preserved. All 1,469 remote file identities were checked before a non-force update with the exact old-head lease. PR34 remains draft on develop; existing release/full labels were verified.

[Current CI run](https://github.com/c933103/AN-Paint/actions/runs/38073935029) · [Preparation receipt](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6100474420)

The separate standalone archive operations remain unchanged and were not used as a source-publication gate. This archive contains only the new composition preparation and host evidence, not duplicate standalone runtime archives.

- Candidate tree: `6d6b90c1999d9e771970ab08e4c275e999c446ca`
- PR34 input: `aa266c2cc8538a04724d06d3b207873c89c342d1` (standalone release run 38064577479)
- PR41 input: `2e512e0c7817cd66a3ec54ca567fc154ea6c83b2` (standalone debug run 38069153905)
- Common base: `165a6a503529736527c689e3ac1b5432253d19ee`
- At the preparation checkpoint no remote source ref, parent checkout, pending evidence upload or CI invocation changed. The later verified source publication is recorded above.

## Exact composition

The three textual merge conflicts were `CI.md`, `tools/ci_emulator.sh`, and
`tools/test_ci_emulator.py`. The final deliberate composition changes seven paths:

- `CI.md`
- `tools/app_instrumentation_matrix.py`
- `tools/ci_emulator.sh`
- `tools/test_app_instrumentation_matrix.py`
- `tools/test_ci_emulator.py`
- `tools/test_vertical_locale_matrix.py`
- `tools/vertical_locale_matrix.py`

The driver retains the PR41 vertical functions and restart boundary, adds the
unchanged PR34 gallery invocation, excludes both special test classes from the
ordinary invocation, and calls one authoritative composed verifier. The legacy
vertical CLI delegates to that verifier. Separate canonical/gallery/vertical/
restart receipt paths all attest the exact complete union and are cleared before
validation. Original raw per-phase reports remain separate.

The complete path inventory is in `composition.json`, with exact old/new blob,
mode and origin for every path. There are 1,469 paths: 1,212 unchanged from the
common base, 169 inherited PR34-only, 79 PR41-only, two identical parent changes,
and seven deliberate composition paths. No tracked path is deleted.

The delta from PR41 is 176 files, +34,712/-162; the delta from PR34 is 86 files,
+10,425/-65. `delta-from-pr34.tsv` and `delta-from-pr41.tsv` give every path and
line count; the published source commit and its exact parents reproduce both binary-capable
Git diffs. Each patch was reapplied to its exact accepted parent through an isolated
Git index and reproduced the candidate tree exactly; their digests are recorded in
`integration-report.json`. The archive omits those full patches to avoid duplicating
historical binary runtime evidence already present in the accepted source parents.
The direct-ADB runner and its test file are byte-identical to both accepted heads.
Every Android source file is the exact accepted-parent union; no Android test
method/body/assertion or production source is altered by conflict resolution.

Host-method preservation is scoped to composition-edited files. One inherited
PR38 change is explicitly retained: in `tools/test_gallery_font_transition.py`,
`FontShellProtocolTest.test_public_pipe_api_is_gated_and_older_path_is_not_called_equivalent`
was replaced by
`FontShellProtocolTest.test_public_pipe_api_is_gated_and_older_path_requires_display_ack`.
That entire file is byte-identical to accepted PR34 `aa266c2c`; this integration
neither deletes nor rewrites the older accepted fixture change.

## Inventory and budget

- API30: 73 native + 15 ordinary + 3 gallery + 2 + 2 vertical = 95 installed methods.
  One app method is SDK-suppressed; the two restart methods remain explicit exclusions.
- API35: 74 native + 16 ordinary + 3 gallery + 2 + 2 vertical + 1 seed + 1 verify = 99.
- App test-source SHA-256: `d8e7d5179f36028d9c25532f357ca08f062a95d046db08a415c570cd8ce1446c`.
- Native/ordinary/two vertical ceilings stay 180 seconds each; gallery stays 90;
  seed/verify stay 60. API35 instrumentation ceilings sum 930 seconds before
  overhead, above the unchanged 900-second outer step. Actual combined CI must
  establish feasibility. The 25-minute job cap also stays unchanged.
- Ordinary/gallery margin targets remain 30/20 seconds. Insufficient margin or
  timeout needs diagnosis; no retry, dropped method, weaker oracle or cap increase
  is used to manufacture acceptance.

## Verified input provenance and host evidence

`source-artifact-binding.json` verifies the source ZIP against each downloaded
build-info digest, then 773 PR34 and 776 PR41 Android/source/tool blobs against the
accepted Git identities. Standalone debug/release differences remain explicit.
These artifacts validate the inputs, never the new combined execution.

Focused checks: 9 composed-app tests, 15 vertical tests, 16 startup/restart tests.
The composed tests exercise both CLIs and both APIs in normal, `-O` and
`PYTHONOPTIMIZE=1`: every missing phase and duplicate method fails; extra paths in
each report subtree fail; stale success receipts are removed; standalone reports
cannot pass a composed union. Dispatch controls preserve ordering and failures.

The first complete host run passed 462 tests with zero skips in 144.499 seconds;
the final frozen run passed the same 462 tests in 167.102 seconds with zero
failures/errors/skips. Independent source review found no additional blocker;
the separate nine-test composition run passed in 40.628 seconds. All three
actual-history PR7/PR9 replays pass with identical SHA-256
`02c069604c6dfb0894bae53081d0c1efe128249a4bd2f4228c407758aaa70af4`.
This replay includes accepted PR34 catalogue additions, so it is not relabelled
as the old PR41 output. Original preservation and optimized-mode controls pass.
Source diff checks, shell syntax and Python compilation pass. Whole staged diff
checking reports 17 inherited whitespace lines in immutable PR34 log evidence;
those bytes remain unchanged.

No Android SDK, adb or installed Gradle is present. Local results are host/
fake-ADB checks, not Android compilation, JVM, installed runtime, lint or pixels.

## Original preparation plan and current acceptance requirements

Items 1–4 below describe the preparation plan. Actual-base source publication is now complete; the separate archival wait in item 3 was explicitly removed as a publication gate. Review and combined runtime requirements remain open.

1. Wait for PR41 evidence archival and exact-source merge by its owner; verify actual develop merge SHA and tree with parent.
2. If merged develop tree is fd9ccb67bba4d053eda1d939738b7af3b7c77ccb, use this candidate tree with PR34 aa266c2c and actual develop merge commit as parents. If source differs, recompose and rerun affected checks.
3. Coordinate with PR34 owner so its existing evidence upload completes or is reconciled before any branch update. Preserve all standalone failure/pass archives.
4. Publish the complete intended tree only after parent coordination; verify all 1469 path/mode/blob identities and absence of removals before a non-force expected-head ref update.
5. Request fresh Codex review for the exact published source and let the release/full PR workflow run once. Do not relabel standalone receipts or request repeated unchanged reruns.
6. Require exact-source release APK/test APK and source binding, generator, Python/JVM/lint and API30/API35 combined execution. Expected installed totals: API30 73 native +22 app; API35 74 native +25 app.
7. Require complete ordinary/gallery/vertical-shard/seed/verify phase union, original restart boundary, font/Korean oracles, all original per-platform 32+64 images and eight reachability receipts, native-drag traces and actual-pixel review.
8. Measure final inner durations and complete outer elapsed time: unchanged API35 instrument ceilings sum930s versus900s outer before overhead. Keep ordinary/gallery margin targets30/20s, preserve timeouts as failures and diagnose deficient margins.
9. Merge only after exact-head review and CI acceptance; no release publication or upgrade-signing scope is implied.
