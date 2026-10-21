# AN Paint 0.0.41 version preparation

Checkpoint: 21 October 2026, 02:26 UTC. [Version PR #157](https://github.com/c933103/AN-Paint/pull/157) is open and ready for review. It does not publish or sign a release.

## Exact candidate

- Parent: `9a7a052d7458cf08f280ead1173c66c2992e4254`, tree `69a1aebdfe35feefd7292d1b47cc6ef3450f57f9`.
- Version head: `23f88311d8a8a28903975758751e6cf88a3ad536`, tree `5fa767ed5bb57364a1ca4bd3cab95cae36187847`.
- All 1,273 source leaves, blob IDs, types and executable modes matched the reviewed local candidate before the PR was opened. Only root `build.gradle` and the matching sentence in `LOCAL_BUILD.md` change, to version 0.0.41/code 98.
- Published 0.0.40, its notes/signature patch and the automatic publication request remain unchanged. Fresh inventories showed no conflicting release/tag/PR; the new identity branch is the intended reservation.

## Verification

Both full local Python host suites passed 1,082 tests, with no skips, failures or errors (224.005s normal; 226.085s optimized). Focused release contracts passed 61 tests in each mode. The raw logs are preserved in `local-host-logs.zip`; `local-test-results.json` records each uncompressed log's exact hash, size, count and timing. No local JVM/Android execution is claimed.

[Exact-head PR CI 39532712417](https://github.com/c933103/AN-Paint/actions/runs/39532712417) and [Code/Security review](https://github.com/c933103/AN-Paint/pull/157#issuecomment-6306437438) are pending at this checkpoint. Their later outcomes must be checked on the same head before merge; local or earlier-source results are not substitutes.

The integrated base's [natural postmerge 39481127358](https://github.com/c933103/AN-Paint/actions/runs/39481127358) passed all six current-platform jobs on attempt 2. Its first API35 core/aggregate failure remains explicitly failed in `postmerge-failed-gate.json` and the [immutable raw failure receipt](https://github.com/c933103/AN-Paint/tree/4e99474d1f05918ae338191ea98d8f4d6611ae3b). The successful aggregate binds the same source/APK, fresh core attempt 2 and retained position attempt 1, covering 45 app tests and 74 Paintroid tests. Required export payloads passed the unchanged validators. `postmerge-success-gate.json` records the independent terminal job readback. This debug/API35 base result does not replace the future release/API30+35 run.

## Source-backed notes and unresolved scope

`czech-source-diff.json` records the direct resource comparison: 373 → 716 typed resources, 343 additions, eight changed values, no removals. Czech retains 645 bounded static accepts and all 72 holds; the original bulky review archive upload remains separately pending. Public integration summaries do not contain its original full receipt/supplement bodies.

The shared numeric filter retains U+2212 instead of silently stripping it into an accepted positive value. Parsers, ranges and keyboard modes remain unchanged. The [original failing reproduction and controls](https://github.com/c933103/AN-Paint/pull/155) remain preserved. Host Robolectric execution is not physical-device or installed-device paste proof.

The notes draft and checklist retain the three Swedish holds, nine Afrikaans holds, Czech no-consumer/layout/manual limits and wider font, language and accessibility work. They make no whole-locale, native-speaker, universal Android or physical TalkBack claim.

## Release boundary

The PR title and actual merge commit subject must begin `Release `; use `Release AN Paint 0.0.41 (code 98)`. The normal develop push then selects the release variant and all nine API30/API35 gates. Release coordination owns the merge.

Only after exact-source build, inventory, source and existing private upgrade-signing checks pass may a separate publication-input PR be prepared. The current request stays bound to 0.0.40. Neither the publisher's checks nor credentials/access settings are changed. Do not republish or replace 0.0.40 assets.

Files here are bounded public project preparation evidence. Application code remains in the normal version PR; bulky historical reports remain on their existing immutable refs.
