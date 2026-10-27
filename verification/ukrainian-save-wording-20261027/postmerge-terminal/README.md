# Ukrainian Save/export/share — actual merge verification

[PR #185](https://github.com/c933103/AN-Paint/pull/185) merged as `0c4f732e7c959bb0829bc537b8e1d34e474e4258`. Fresh develop readback still matched that merge after verification. Its tree `72ff2d3db4bb3319a0914990331165f901f8309f` is identical to reviewed head `323288883accb4c625d70136667600aeae6dbd44`; ordered parents are `c404e7ea31ef0a22c3645d8c73e50b55d7ff959c` and the reviewed head.

## Actual merge-push results

[Run 40447521764](https://github.com/c933103/AN-Paint/actions/runs/40447521764), attempt 1, completed successfully in all six jobs. These are fresh actual-merge results, not substituted PR results.

- Hosted Python: 1,457 passed. Hosted JVM: 1,402 tests across 152 suites; zero skipped, failed or erroneous cases. The exact testcase inventory equals the same-tree PR inventory. All three Ukrainian compiled-resource/dialog/cancellation methods passed again (0.798 seconds total). Android lint: no issues.
- Exact-script generation: all 13 expected probe outcomes, original log hashes and actual merge/tree identity independently verified.
- API35: the complete source-bound app union passed 47/47 and native instrumentation passed 74/74. No missing, excluded or deferred app case. Core/position APK, test APK, source, SDK and run/attempt identities agree and match the independently downloaded actual build.
- The APK/source artifact digest and main APK/source digests match build metadata. The embedded corresponding-source ZIP equals the separately delivered ZIP byte-for-byte. All 1,388 included tracked files match exact reviewed content and modes; observed tracked omissions are two `.gitignore` files and IDE metadata, not application source.

## Bounded localization outcome

Exactly ten missing Ukrainian P0 Save/export/share values were added after independent model-based complete-value/source-context review (six retained candidates, four idiomatic/terminology refinements). All 127 inherited Ukrainian values/attributes, other catalogues and five no-current-consumer holds remain unchanged. Exact-head Codex code/security reviews completed with no findings before merge.

All 171 picker tags, the P0 manifest and catalogue contents were read directly from the actual merged build’s corresponding-source archive: Ukrainian **19/92** P0 present, **73 missing**; global **7,308 present / 8,424 missing**. This is direct resource coverage, not linguistic completion. The 59 scoped/112 open fallback catalogue distinction is unchanged.

## Evidence and limits

Selected ZIPs preserve original JUnit/phase/protocol/summary bytes and selection manifests binding retained members to original artifact digests. Original artifact IDs/digests and six terminal jobs are in `terminal-github-evidence.json`. Build/source identity and source-byte checks are in `build-info.json` and `source-archive-verified.json`.

Earlier [local evidence](https://github.com/c933103/AN-Paint/blob/fc973b46fdeb26227b7462a4757bc1b45cd443bd/verification/ukrainian-save-wording-20261027/local/README.md) and [terminal PR evidence](https://github.com/c933103/AN-Paint/blob/110398fed02b9bc820b070bfe3ec5ce77a1c174d/verification/ukrainian-save-wording-20261027/pr-terminal/README.md) remain preserved separately.

No native-speaker, installed Ukrainian layout, physical-device or whole-locale acceptance is claimed. API30 was not selected for this routine current-platform change. The build uses a CI debug key, not private upgrade signing; this is not an upgrade-ready or release delivery. No release was requested or performed, and existing release/scope holds remain unchanged.
