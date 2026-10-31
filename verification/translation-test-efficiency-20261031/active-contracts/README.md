# Active priority contracts: exact-source evidence

[PR #251](https://github.com/c933103/AN-Paint/pull/251), source `0acbc50da25a7ef3b4b55de0a6b25290e60f9fe8`, tree `2fc050281995f22e72c5249012c756a6012cca29`. Dependency: #250 at `f74981bb4cb9be1ac69d6f448b9790e3951435c3`. Do not merge into the temporary cleanup base; retarget actual develop after dependency acceptance and post-merge observation.

## What changed

52 existing files; no production wording, workflow or new framework. The existing `verification/README.md` contains the responsibility map.

- 24 fixture payloads shrink from **6,051,757 to 4,333,287 bytes**. Only historical `priority_rows` are removed. All other field values remain equal.
- The 8,184 archived records map without conflict to 6,178 edited targets, 1,801 retained targets and 205 absences. `historical-recovery.json` identifies every original path, blob and SHA-256 at already-merged immutable `f3d617d0`; all blob IDs were checked against its remote tree. No duplicate archive payload.
- All 6,451 edited-resource positive checks remain. Generic negative probes fall from 19,353 to 162 across 54 locale/type/successor paths. Classification matches the validator for every edited key. Existing structural, source/predecessor, script and option checks remain.
- Eight historical-disposition mutation methods are removed. Retained canonical-binding tests exercise the same mismatch path; 144 temporary probes verified that current holds/context/display/predecessor tampering still fails. No permanent test package was added.
- Six identical animation methods are removed, avoiding 54 scanner/dialog executions. LTR/RTL representatives, `ImportSelectionTitleTest` and all 120 complete locale animation value/formatting checks remain. Exact identities are in `animation-responsibility.json`. No removed method tested layout; no layout coverage is claimed. Five non-identical variants remain.
- The 19 existing digest consumers change only hash constants plus the six explicitly mapped method removals. All other helper/JVM logic remains unchanged. All 1,643 candidate remote leaf paths, content SHAs and executable modes match the reviewed checkout.

## Results and limits

| Selected work | Result | Wall time |
| --- | --- | --- |
| Before: eight affected host modules | 135/135 pass | 321.260 s |
| Final after: same eight modules | 119/119 pass | 275.437 s |
| Additional direct consumers | 14/14 pass | 197.078 s |

The single paired affected-run observation is **45.8 s / 14.3% shorter**. It is not a global, guaranteed or controlled multi-run speedup.

The initial changed run had 118 passes and one `NameError`: my Tibetan test edit missed a module-scope `residual_rows` import. Its failed receipt remains separate. After fixing that import, the failed test and affected JVM-source guard passed; the final 119-test run then passed on frozen source. No full-host or optimized local aggregate was run. Local Android SDK is unavailable; hosted JVM/Android gates remain required.

Parent artifact `13043351462` was independently downloaded and verified against SHA-256 `0f83403ef0f925df54e6c8cada7498813a50788f2af7a32cd51c71f5a7b49b82`: 1,962 JVM cases, zero failures/errors/skips. The six removed methods consumed **11.34 s combined** there. This is a parent-source observation, not a candidate pass or a large whole-JVM speedup claim.

Exact-head Codex request: `6543649169`. Required CI: `41203339966`, pending when saved. Baseline, failed-attempt, final-after and consumer logs are separate. No release or claim that project-wide cleanup is complete.
