# AN Paint 0.0.41 preparation checklist

Current checkpoint: version PR #157 is open and ready for review, 21 October 2026, 02:25 UTC. Release coordination owns all final merges. The version branch exists; no 0.0.41 tag or release has been created. The 0.0.40 release, request, notes, signing patch and assets remain unchanged.

## Frozen inputs and scope

- Published baseline: v0.0.40, source `d664b3e72ea3261dba662119a429b0bb3914c04a`, version code 97.
- Fresh integrated develop: `9a7a052d7458cf08f280ead1173c66c2992e4254`, tree `69a1aebdfe35feefd7292d1b47cc6ef3450f57f9`. All 1,273 source leaves, contents and executable modes were independently matched to the remote before making a separate local candidate.
- Fresh release/tag inventory and all 321 branches show no 0.0.41 reservation; no open release PR exists. The next available identity is 0.0.41/code 98, subject to rechecking immediately before branch creation.
- The direct Czech resource diff is 373 → 716 typed resources: 343 additions, eight changed values, no removals. All 645 bounded accepts and 72 holds remain; the original bulky archive upload is separately pending. Its summaries must not be represented as the full archive.
- The only new production-code change is addition of U+2212 to the shared numeric filter's retained character set. Parser, range, input type and layout are unchanged. Test-first reproduction established real accepted-positive coordinate mutation; original failed baseline and green controls are retained at [immutable baseline evidence](https://github.com/c933103/AN-Paint/tree/8138fa0f95dccc1696d756fb5587122d01eb9d08).
- No new Swedish/Afrikaans feature claims, whole-locale acceptance or physical-device proof are inferred. Published 0.0.40 remains immutable.

## Version preparation and natural release selection

- [x] Confirm natural integrated postmerge [39481127358](https://github.com/c933103/AN-Paint/actions/runs/39481127358) passed all six required current-platform jobs on attempt 2, after independent raw exact-source report verification. Attempt 1 remains failed: Core emulator API 35 and its aggregate failed during mandatory evidence collection; the other four jobs passed. The one coordinated failed-job retry succeeded on unchanged source, using fresh core attempt 2 and retained position attempt 1. Original failure evidence remains preserved. Earlier combined PR [39476623276](https://github.com/c933103/AN-Paint/actions/runs/39476623276) and Czech postmerge [39473371093](https://github.com/c933103/AN-Paint/actions/runs/39473371093) are separate passed runs, not substitutes for this gate.
- [x] Fresh-check develop/tag/release/version reservations. Rebase/revalidate if the frozen source changed; do not silently add scope.
- [x] After release sequencing confirmation, publish the normal draft version PR changing only root `build.gradle` to 0.0.41/code 98 and the matching current-version sentence in `LOCAL_BUILD.md`. Keep `verification/releases/request.json`, all old notes/signature patches, workflows and publisher logic byte-for-byte unchanged.
- [x] Verify complete remote path/blob/type/mode equality to the locally tested tree and expected parent. Run applicable host contracts and full normal/optimized host suites; report real counts and skips separately. Mark ready and request exact-head Codex Code/Security review through the established integration.
- [ ] Require applicable exact-head PR CI and reviews. Release coordination owns guarded merge. PR title and actual merge commit subject must begin `Release `, for example `Release AN Paint 0.0.41 (code 98)`, so the normal push selects the release variant and API30+35.
- [ ] Wait for the exact version-merge source's successful natural `push` to `develop` Android run: regression/lint, universal APK/source, exact-script generation, core API30/API35, position API30/API35 and both final emulator gates. All nine jobs are required. Do not dispatch a substitute or reuse debug/old-version results.
- [ ] Download exact-run artifacts, verify their IDs/digests/run/source/variant, and validate SDK-aware disjoint inventories, JUnit/lint results, screenshots/exports and source binding with the current unmodified validators. Missing, excluded, failed, timed-out and unrun checks remain distinct. Preserve needed raw receipts before Actions expiry.

## Signing and publication, only after later sequencing authorization

- [ ] Sign a separate copy of the exact tested release APK using the existing private local key/setup, never the old debug/code94 packager. Do not expose or upload key/password/alias values, create credentials or change access settings.
- [ ] Require the sole existing upgrade certificate, package `paint.anpaint.android`, version 0.0.41/code 98, non-debuggable manifest, all four ABIs, 16 KB alignment, unchanged non-signature payload and embedded/delivered source equality. Independently bind the source ZIP to the final source tree and pinned inputs.
- [ ] Generate a new public-only format-1 signature patch. Keep existing allowed ranges and publisher acceptance unchanged. Verify reconstruction through the unmodified apply routine produces the exact signed APK hash. Preserve any failed attempt honestly; a memory-bounded implementation is not permission to weaken format or payload checks.
- [ ] Prepare a separate draft publication-input PR with only the new version's notes/signing patch and replacement request bound to the final source/run. The current request is an automatic publication trigger, not a harmless draft location. Require exact-head review, applicable contracts/CI and full tree readback; release coordination owns its merge.
- [ ] Monitor the natural publisher. Reconcile an uncertain existing draft or asset read-only before any permitted retry. Never overwrite a mismatching release asset or change publisher acceptance to force success.
- [ ] Independently verify public tag/source, non-draft/non-prerelease release and exact reviewed notes. Freshly download all four assets via their actual public URLs; verify names/sizes/hashes, both checksum and provenance contracts, signature/metadata/ABIs/alignment and embedded source. Freshly compare all 0.0.40 public asset bytes and identities to the preserved baseline. Preserve final evidence and update the board.

## Local candidate identity

Prepared tree: `5fa767ed5bb57364a1ca4bd3cab95cae36187847`.
Only changed files: `build.gradle` and `LOCAL_BUILD.md`. Current publication inputs are untouched. Focused release contracts passed 61 normal and 61 optimized tests. Full Python host suites each passed 1,082 tests with no skips, failures or errors (normal and optimized); exact timings and complete raw logs are recorded in local-test-results.json. No local JVM/Android execution is claimed.

Current version PR: https://github.com/c933103/AN-Paint/pull/157, head `23f88311d8a8a28903975758751e6cf88a3ad536`. Natural PR CI: https://github.com/c933103/AN-Paint/actions/runs/39532712417. Exact-head Code/Security reviews and hosted CI remain pending at this checkpoint.
