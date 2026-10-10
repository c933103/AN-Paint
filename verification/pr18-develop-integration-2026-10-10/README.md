# PR18 current-develop integration evidence

This evidence-only branch records source/host acceptance for PR18 head `66c6fd8411dd799c2d2ceb9250c1de500346f3f5`, tree `2ca29f84ce77e8d3be1aa2b7602fa6cca0ca6c31`. It is not an executed source head and adds no production, test, workflow, or historical-evidence changes. The tested PR head remains unchanged.

## Exact composition

- PR18 original head: `66c39ca345ef7bc8c5fe1da8ce64cb872c3a0e88`.
- Accepted develop after PR37: `699f3cb0d3e0fe932fbf39779f852c2b5e9dbf3c`.
- Real merge base: `ff2db040272fa522226da60744316bfeb8695cf0`.
- The source commit has the PR18 and develop commits as its ordered parents, retaining both histories without force.
- PR18's 44 delta paths and develop's seven later delta paths are disjoint. The source union is conflict-free and contains exactly 1,344 tracked file entries.
- Every candidate blob/mode/type equals the PR18 entry for its intended delta or the accepted develop entry otherwise. All accepted production, JVM tests, workflow YAML, PR37 optimized validation/evidence, and PR42 title correction are preserved.
- Both input manifests were checked against fresh remote recursive trees (1,341 original PR18 and 1,303 develop file entries). All 1,344 remote candidate entries were compared before branch publication. The parent independently recomputed and accepted the exact union.
- Full composition manifest: `composition.json`, SHA-256 `eca6b2ecd8071a2a90cdc11cfe58cb54fb0f298694c6665dff06a2ba3e3935ec`.

## Host checks

Command from the exact candidate checkout:

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'`

Result: **390 tests passed, zero failures/errors/skips, 143.318 seconds**. `host-tests.log` SHA-256: `eb37ca97a46fa0f773acc157b4355db0faf31286249ea06ed223e7b09b96bb7e`. Deliberately unsuccessful protocol fixtures printed after the unittest summary are negative controls, not test failures or Android runtime observations.

`bash -n tools/ci_emulator.sh`, staged and unstaged `git diff --check` passed. The source tree was rechecked after tests. No local Android SDK/ADB was present, so Android compilation and runtime are delegated to the existing exact-head CI; no local Android pass is claimed.

The preserved PR37 mode suite exercises 23 invalid prerequisites in each of normal Python, `-O`, and `PYTHONOPTIMIZE=1`, plus valid controls and receipt regressions. Actual historical `verify_scope.py` replay was also run in all three modes. Each output matches the accepted `verification/pr7-pr9-recheck-2026-10-10/source-results.json` byte-for-byte. One identical copy is retained as `replay-normal.json`; all three SHA-256 values are `b7ebadb5eb9d13a4f95bb5499ccce4f5efa493764f5eaf2f1d17105187c7a016`.

The SDK-specific source inventories remain API35: 18 ordinary + 4 vertical + 1 seed + 1 verify = 24; API30: 17 ordinary + 4 vertical = 21, with the two restart methods explicitly omitted and one ordinary method separately SDK-suppressed. Omissions are not passes.

## Pending exact-head acceptance

[Run 38067267565](https://github.com/c933103/AN-Paint/actions/runs/38067267565) is the fresh PR run for head `66c6fd8411dd799c2d2ceb9250c1de500346f3f5`. Artifact identity established the actual tested merge as `5c791111d6b29035a59267125d0a6e02e4603e0b`, with former PR37 head `dbd4d22e1f140618f726d43f830bde178cfa589d` and new PR18 head `66c6fd8411dd799c2d2ceb9250c1de500346f3f5` as parents. This ref was captured before retargeting completed. Its exact tree is `2ca29f84ce77e8d3be1aa2b7602fa6cca0ca6c31`; the new PR18 head already includes accepted develop `699f3cb0`. After retargeting, the current synthetic merge ref `c60c1b79503cebeb4e28bd0b9d9b381aad455fa2` has the same tree and current develop/head parents. Both were fetched and verified. The synthetic current ref is not the ref executed by this run. Its completion, artifacts and 32 fresh screenshot states are not yet accepted by this source/host receipt.

A normal draft-to-ready transition triggered Code and Security reviews for exact head `66c6fd8`; both were verified running. No duplicate manual request was sent. Existing CI deadlines, including the 120-second Python step and 180-second ordinary/vertical invocations, were not changed. The local host timing exceeds that CI step limit; fresh CI must establish its own timing and any failure must be retained and diagnosed.

Earlier PR18 screenshots remain historical evidence for their exact old tree. Full-range control reachability remains PR41's separate follow-up. PR34/PR43, original localization reset obligations, linguistic correctness, API30/release certification and private upgrade signing are not completed by this integration.
