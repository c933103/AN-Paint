# PR41 current-base integration preparation

Prepared 10 October 2026. This is local exact-source preparation evidence, not fresh Android/installed validation or merge acceptance.

## Exact candidate

- Original PR41 head: `107376cbd9a0eafcd3cedbae0365802702b525ff`, tree `52901eb86069390da168b6c86b99b67d3e1db8f5`.
- Updated PR18 head: `66c6fd8411dd799c2d2ceb9250c1de500346f3f5`, tree `2ca29f84ce77e8d3be1aa2b7602fa6cca0ca6c31`.
- Shared base: `66c39ca345ef7bc8c5fe1da8ce64cb872c3a0e88`.
- Candidate tree: `fd9ccb67bba4d053eda1d939738b7af3b7c77ccb`.

The clean merge is the exact disjoint union of 37 intended PR41 paths and seven upstream PR37/PR42 paths. All 1,370 candidate paths, file modes and blob identities are in composition.json. Every intended PR41 path and every unaffected upstream path is unchanged. The complete PR41 patch and complete upstream patch both compare byte-for-byte before and after integration. No conflict resolution or new source edit was needed; PR34 and PR43 were not integrated.

## Checks

- Full host suite: 419 passed in 179.311 seconds; zero failures/errors/skips.
- Focused reachability/redraw: 11 + 2 passed.
- Shell syntax, Python compilation, current integration diff and non-archived source diff checks passed. Whole-PR diff checking reports 17 pre-existing whitespace warnings inside three immutable historical .patch evidence files. Those original bytes are preserved.
- Actual-history verifier replays in normal, -O and PYTHONOPTIMIZE=1 modes all passed and matched the accepted source-results.json byte-for-byte (SHA-256 `b7ebadb5eb9d13a4f95bb5499ccce4f5efa493764f5eaf2f1d17105187c7a016`). One initial partial-clone replay encountered a lazy GitHub fetch CONNECT 403; successful runs used the existing materialized local repository history without changing source.
- API35 app source inventory is 24 methods: 18 ordinary, two English/Manchu, two Literary Chinese/emoji, one restart seed and one restart verify. Vertical budgets remain two 180-second invocations and the enclosing 15-minute cap is unchanged.

Android/JVM and installed checks were not run in this executor: Android SDK, adb and a cached Gradle distribution are absent. Previous PR41 runtime acceptance remains historical exact-source evidence, not a pass for this new candidate. Negative-fixture JSON printed after the host suite summary is intentional test output, not an installed test result.

## Publication gate

This separate evidence branch preserves all original PR41 source. It does not move that PR's branch or start CI. The real PR18 merge must be confirmed and the candidate recomputed against its actual develop commit before source publication, followed by new exact-head CI and review as required.
