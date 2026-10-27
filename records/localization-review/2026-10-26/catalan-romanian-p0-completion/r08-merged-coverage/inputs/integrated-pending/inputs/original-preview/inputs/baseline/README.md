# PR177 integrated coverage — actual postmerge checks passed

**Actual merge push [40327501312](https://github.com/c933103/AN-Paint/actions/runs/40327501312) completed successfully at 2026-10-26 13:25:59 UTC, with all six checks successful.** This report is pinned to merge [`ce796879f4568a27b9d905a8e8db639dd0a93a30`](https://github.com/c933103/AN-Paint/commit/ce796879f4568a27b9d905a8e8db639dd0a93a30), tree `f7c5f2fca54eb06b4a0c55df25a0b80b2ac4c12c`. The terminal receipt observed `develop` at that merge. Later movement does not silently change the pin.

[Immutable actual postmerge evidence](https://github.com/c933103/AN-Paint/tree/c094a1b7bffdce01dd0ae6a7ab51f0d165fd2ffe/records/localization-review/2026-10-26/catalan-romanian-p0-import/r07-postmerge-terminal) is separately bound by `terminal-status-supplement.json`. These are fresh actual-merge results, not successful PR results relabelled as postmerge execution.

## Pinned coverage

- **171 options:** 50,751 containers present / 71,856 missing; P0 6,728 present / 9,004 missing. English-identical leaves remain 7,051 and are not automatically defects.
- **Catalan and Romanian:** each 150 containers, P0 **32/92**. Each has **60 missing P0 values: five explicit no-current-consumer holds and 55 outside this batch**, not newly held or declared defects.
- Exactly 26 missing-only values were added. All 274 inherited values and all 169 other option rows remain unchanged.

Full tables: [CSV](structural-per-locale.csv) · [JSON](structural-per-locale.json). These are byte-identical copies of the previously verified integrated tables; stable arithmetic was not rerun for this terminal wrapper.

## Actual merge-run results

| Evidence | Verified result |
|---|---|
| Hosted JVM | 1,361 tests; zero failures, errors or skips; all eight focused suites passed |
| Hosted Python | 1,389 total: **1,387 passed + two unnamed skips**; skipped identities are not guessed |
| Android lint | Zero issues |
| API35 emulator | 45 source-bound app cases + 74 native cases completed |
| Compiled resources | 26 new + 256 prior bounded reviewed values; 282 total, without duplicate new/prior ca/ro keys |
| Exact-script generation | 13 probes matched expected outcomes, including one deliberate reserved-variant rejection |

Source/APK/archive hashes and exact run identities agree. The APK is CI-debug-signed; this is not release or private upgrade-signing evidence. Packaged tracked source is verified; extra vendored/generated archive members are counted, not authenticated by the project Git tree. Artifact availability alone is not taken as proof that tests passed. Local/optimized results are not substituted for hosted outcomes.

## Runtime inheritance is not new translation acceptance

For `save20_unsupported_image_colour`, structural presence remains **70 direct catalogues / 101 absent catalogues**. Runtime resolution is separately **70 direct + one parent-inherited + 100 English defaults**. The actual postmerge `TaggedColourImportTest` oracle passed, including `ca-ES-valencia` inheriting the reviewed `ca` value. This does not create a Valencian resource or grant independent Valencian linguistic acceptance. The family-specific split does not replace global scoped59/fallback112.

The original head's failed run 40319792630, subsequent successful corrected PR run 40323966400 and fresh actual postmerge run 40327501312 remain distinct evidence. The original failed assertion and PR proof are preserved, not rewritten or removed.

## Historical pending package preserved unchanged

`integrated-pending/` contains **all 25 original files byte-for-byte**, including the original pending README, merge identity, arithmetic, 78 controls, review qualifications, original failure evidence and separate corrected PR runtime proof. Its manifest SHA-256 is `070bca0f14f94c46d415e58749e9503e563eac12a0a910ebc46fb22700105a04`.

Those earlier pending observations are historical. **This terminal supplement supersedes their current-status implication without rewriting their bytes or validators.** `terminal-evidence/` likewise preserves the complete 11-file published terminal package, manifest SHA-256 `1be9b4be8f93edc7153747b8310cb3877b269b5eda9b54aaefcd3eaea54249f8`.

`verify_terminal_supplement.py` checks the six terminal receipt joins, source/run/check/job identities, archive/APK hashes, 26 exact new compiled-value/review hashes and actual inheritance-oracle result. Jobs in the supplied receipt omit their own head field; their exact IDs/names join the six source-bound check records. The wrapper neither reruns CI nor re-extracts artifacts. Its **44 focused malformed/semantic controls** reject in ordinary and optimized Python, with identical outputs.

```sh
python3 verify_terminal_supplement.py --report-root REPORT_DIRECTORY
python3 test_terminal_guards.py --report-root REPORT_DIRECTORY
```

All original [full-value qualifications](integrated-pending/review-scope-reconciliation.json), 18 static composition examples, prior accepted/qualified/clause-only/author-only/historical/unmatched/synthetic scopes and explicit holds remain intact. Global linguistic accepted count stays null. CI success does not grant native-human, physical-device, layout or whole-language certification. NN/DA/NO holds; paired P1/frozen/global59/112 boundaries; PR56 never-merge, PR159 freeze, PR113 hold/retarget, Help callback/archive identity, interrupted-archive and release pauses remain unchanged. **No release was performed.**
