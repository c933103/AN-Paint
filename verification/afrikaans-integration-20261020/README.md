# Afrikaans PR140 gate reconciliation, 20 October 2026

This is evidence for the existing bounded PR140 work, not an application merge, branch update, release, whole-language certification, or replacement of the prior denied-merge record.

## Exact source composition

- PR head: `bf56a676a6a59ca791fe8eccf0816d80ed52177e`.
- Current develop checked: `f0705a33c6f5aa3bc1e4020eef5f0a3ea1d3e6a6`.
- Expected composed tree: `70b93689fa83422be586e1b49ab1203cff082ece`.
- An isolated exact-develop checkout received only the exact PR delta using three-way application. Plain-context application detected the adjacent newer gallery-redirect line; three-way application completed cleanly without conflict.
- Exactly one resource modified and three original test/fixture files added; no removals. All 1,262 unaffected current-develop leaves retain content, type and mode. Expected composition has 1,266 leaves.
- Afrikaans blob `e67a7036461a69cd4c6b20ed61edfdf2f63d5690` contains all five corrections plus the newer gallery-redirect wording. All nine explicit held entries match the review base, current develop and composed tree.
- No remote application ref was changed. The original 341-pair scope and exclusions remain unchanged.

## Checks

- Focused Afrikaans: 7 tests passed in 0.480s.
- Focused gallery redirect: 5 tests passed in 0.698s.
- Full normal host suite: 1,075 tests passed in 524.004s; exit 0.
- Full optimized host suite: 1,075 tests passed in 515.973s; exit 0.
- Composed Afrikaans XML compiles with AAPT2; exit 0.
- The final worktree still matches its verified index/tree.

Raw logs, the composition proof and exact checks are in `raw-checks.zip`. Negative-fixture stdout deliberately contains unsuccessful instrumentation receipts; those are tested rejection cases, not failed unittest aggregates. No fresh hosted JVM/lint/APK/emulator run was performed on this composed tree. Local timings are not a benchmark or a claim about hosted timeouts.

## Review and merge gate

[Fresh request](https://github.com/c933103/AN-Paint/pull/140#issuecomment-6293387598) produced a [new Codex no-major-issues receipt](https://github.com/c933103/AN-Paint/pull/140#issuecomment-6293439262) at 14:38:04 UTC. The [bot summary](https://github.com/c933103/AN-Paint/pull/140#issuecomment-6265583560) records a new manual code review completed at 14:38:05 UTC, full head SHA `bf56a676a6a59ca791fe8eccf0816d80ed52177e`, and no findings or unresolved findings. The security review remains the existing completed no-findings review on the same full SHA; it was not freshly rerun.

[Original CI run 39240946949](https://github.com/c933103/AN-Paint/actions/runs/39240946949), attempt 2, and all six exact-head check runs remain successful. Capture recovery evidence and its limits remain in [the prior record](https://github.com/c933103/AN-Paint/pull/140#issuecomment-6266479823).

The [prior two guarded merge denials](https://github.com/c933103/AN-Paint/pull/140#issuecomment-6266488780) are preserved as explicit tool-side evidence-verification denials, not owner refusal. No merge retry, indirect merge or ref-update workaround was performed in this reconciliation.

The fetched synthetic merge ref remained `b09f06722bfe08783d93fff14ba02b6dd513f007`, with parents `5d9e490d48804809d07bf3c88abc533306a58257` and the PR head. It is not evidence of composition onto the checked current develop. The independent composition proof above closes the local composition question, not a new hosted integration gate.

GitHub documents a normal [Update a pull request branch](https://docs.github.com/en/rest/pulls/pulls#update-a-pull-request-branch) operation guarded by `expected_head_sha`. The installed connector does not expose that mutation. A normal branch update, if later needed, would change head and require fresh exact-head review and CI; it must not be replaced by a ref mutation that emulates merging develop.

## Subsequent normal merge

After the new review and local composition results were available, a single normal guarded merge retry succeeded as [commit ad3ef6d9e1e44b364a65188a6d20235f68eb16c8](https://github.com/c933103/AN-Paint/commit/ad3ef6d9e1e44b364a65188a6d20235f68eb16c8). Its actual parents are the checked develop `f0705a33c6f5aa3bc1e4020eef5f0a3ea1d3e6a6` and PR head `bf56a676a6a59ca791fe8eccf0816d80ed52177e`. Its fetched Git tree is exactly `70b93689fa83422be586e1b49ab1203cff082ece`, equal to the locally verified composition. The earlier denials remain preserved. Post-merge CI is a separate follow-through and is not claimed complete here.
