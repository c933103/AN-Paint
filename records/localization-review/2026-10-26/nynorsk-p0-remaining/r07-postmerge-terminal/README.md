# PR174 merged-source verification: terminal success

**The actual postmerge run passed.** [Run 40281975192](https://github.com/c933103/AN-Paint/actions/runs/40281975192), triggered by the push of [`df9bc04b848ab5e99457bc67265d771bb839ec9d`](https://github.com/c933103/AN-Paint/commit/df9bc04b848ab5e99457bc67265d771bb839ec9d), completed successfully at 07:13:16 UTC on 26 October 2026. All six jobs passed. This record supersedes only the pending postmerge status in earlier snapshots; it does not rewrite their historical observations or relabel PR artifacts.

## Integrated source

[PR174](https://github.com/c933103/AN-Paint/pull/174) is merged/closed at 06:48:20. The valid signed merge has parents `857a20103285a77846e340b326667c15a402ff9e` and reviewed head `3c8123707106dfc991221517e443276f857797db`. Tree `8ca5fc4f3989cf8c9307432d5e5c28ceef698251` and all 1,367 blobs/modes match the reviewed PR tree. A fresh explicit `branches/develop` read still resolved to df9bc04 at 07:13:37; this snapshot remains pinned if the branch moves later. Exact-head Code review remains the PR-head receipt, not an invented separate review of the merge commit. Optional Security was clean but not a required gate.

## Actual postmerge results

- **JVM:** 1,349 passed across 144 JUnit XML suites; zero failures, errors or skips. All 26 cases in five focused suites exactly match current source method inventories, including the real export/dirty-state regression and the new resource/import/recovery checks.
- **Hosted Python:** 1,364 run, **1,362 passed + 2 skipped**, 260.872 seconds. Skipped identities are not named in its non-verbose summary and are not guessed. The separately recorded ordinary/optimized local results remain distinct.
- **Android lint:** zero issues. Python/JVM/native-preparation/lint phase receipts all have exit status zero.
- **API35 emulator:** exact source-bound **45 app + 74 native** case identities passed. Independent reconstruction matches the composed app receipt and all unique native identities; no missing, unexpected or failed cases. Executed main APK, corresponding source and instrumentation APK hashes match the current prebuilt identity.
- **Exact-script generation:** all 13 probes have verified log hashes and expected exit outcomes, including the deliberate reserved-variant rejection.
- **Compiled resources:** all 72 newly reviewed and eight prior reviewed Nynorsk display values match exactly in the actual merged APK. This is bounded compilation evidence, not installed Nynorsk layout certification.

## Corresponding-source and artifact identity

- APK/source artifact 12632671081 archive SHA-256: `fe6a4d776878f8b6ff011866fd354f9fe8c6e5a71f99c053c3ad9b8765466a7d`.
- Merged APK SHA-256: `5ae3d014d9f41567331194e83496e937f6a6ce3ee51710c967a3d0fa81db42b0`.
- Source ZIP SHA-256: `b4ee706a524ed55902b2829cdf2fd66887cc33df908bd4a76e481de49b4fea33`.
- All 1,364 packaged tracked source files match the exact 1,367-file merged tree; the three normal dotfile exclusions are listed explicitly. Embedded and external source ZIP bytes match.
- APK v1/v2 signatures verify. CI debug certificate SHA-256: `67174ecc196f4f0e8d278819ded7c8f04bc07cbaeeadefacecb675222d73b7ff`. This run's debug identity is distinct from the PR run and is **not private upgrade/release signing**.
- Regression artifact 12633935107 SHA-256: `6dc56c27edd10385e2c5daf6964c34d17ebc16f7c108832810485b7e340aa7ae`.
- Composed API35 artifact 12632624528 SHA-256: `563ece63907779799e98ea152b179fbc17e0e73fc7693568cd8e687d9488338b`.

The four verification scripts accept explicit pinned source, commit/run/artifact/digest inputs. They inspect downloaded artifacts rather than compiling Android locally. Exact source/resource/signature, per-test and phase receipts are in the adjacent JSON files. `verification-events.json` preserves local checker events and their correction; no hosted failure is hidden and no CI rerun occurred.

## Coverage and retained scope

The independently reproduced [171-option CSV/JSON and exact review/source delta](https://github.com/c933103/AN-Paint/tree/708bbaf18874b97815882adacadf4b7a73513a9e/records/localization-review/2026-10-26/nynorsk-p0-remaining/r06-merged-coverage) is unchanged: Nynorsk **190/717 containers; P0 87/92**, five explicit no-current-consumer holds absent, all 118 prior values unchanged. All 170 other options are unchanged. Across 171 options: 50,549 containers present / 72,058 missing; P0 gaps 9,206; P1 gaps 22,557; English-identical leaves 7,051. A further independent audit found no concrete arithmetic, provenance, reproducibility or privacy defect; its exact scope and limitations are recorded here.

The 72 new static AI whole-value reviews are disjoint from the prior eight; their qualifications and every earlier author-only, historical, clause-only, unmatched and synthetic scope remain intact. No whole-language, native-human, physical-device or layout certification. Paired-warning oracle remains 120 entries/60 tags; P1 companion and five holds remain absent. PR56 never-merge, PR159 freeze, PR113 hold/retarget, Help callback/archive identity and release pauses remain unchanged.

The PR174/postmerge monitor is terminal and retired; it does not need further polling. No release was performed.
