# PR 158 final hosted validation

This directory preserves final receipts for AN Paint PR 158 candidate
`8f63233ed720dee38f8067ee95a93c398da6c292` (tree
`708ff87d2a68f08e4aebb3ce7b6d2a09460fba4e`). GitHub Actions run
`39705831860` tested the signed GitHub pull-request merge commit
`ff307eaca74bddaf9ce3b486199a620683f9703f`, whose tree is exactly the same
`708ff87d2a68f08e4aebb3ce7b6d2a09460fba4e`.

## Raw artifacts

`artifact-digests.txt` records the immutable IDs, names, sizes and GitHub
SHA-256 digests for the complete composed API30/API35 union artifacts. They were
downloaded through the GitHub API and their ZIP bytes matched those digests.
The run retains the raw ZIPs until 2026-11-05. `raw/` durably preserves every
reviewed capture from those archives: 96 API30 vertical-locale PNGs, 96 API35
vertical-locale PNGs and 39 API35 installed-dialog PNGs.

## Source

`source/` contains the build identity and resolved runtime dependency receipt.
The release-configured CI APK and corresponding source archive are identified
by hashes in `build-info.json`; neither binary is a release or release
candidate. CI used its debug key. Release 0.0.41 remained paused.

## Provenance

`provenance/installed/` preserves device/build identities, exact core/position
selection receipts, all instrumentation XML/summaries, screenshot/export hash
inventories, collection status, and the API35 dialog manifests/receipts.
`provenance/jvm/` contains all 141 raw Gradle JUnit XML suite receipts:
1,335 tests, 0 failures, 0 errors and 0 skips. `provenance/lint/` records the
zero-issue lint result. `provenance/exact-script/` records the successful clean,
incremental, stale-output and reserved-variant resource-generation probes.

Every one of the 231 installed PNG captures in the two union artifacts was
decoded with ImageMagick 6.9.11-60. Contact-sheet visual review covered all 96
API30 vertical captures, all 96 API35 vertical captures and all 39 API35 dialog
captures from the digest-matched ZIPs. The images were populated and correctly
oriented, with localized UI and the required control states visibly present;
no blank, truncated export or transport placeholder was found.

GitHub run: https://github.com/c933103/AN-Paint/actions/runs/39705831860
