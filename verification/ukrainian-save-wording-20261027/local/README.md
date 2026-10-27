# Ukrainian Save/export/share bounded evidence

Source: [323288883accb4c625d70136667600aeae6dbd44](https://github.com/c933103/AN-Paint/commit/323288883accb4c625d70136667600aeae6dbd44), [PR #185](https://github.com/c933103/AN-Paint/pull/185).

- Exactly ten missing Ukrainian P0 values; all 127 inherited values/attributes and every other catalogue preserved.
- Independent model-based complete-value/source-context review, with six candidates retained and four refined. Not native-speaker or installed-layout acceptance.
- Focused host checks: 8 passed in ordinary and optimized modes.
- Full host checks: 1,457 passed in each mode, exit 0. Expected negative-fixture output in the raw logs is not an aggregate failure.
- Local JVM tests did not run: the wrapper could not download Gradle. Hosted exact-source JVM/build/lint/resource/API35 checks remain required.

`linguistic-source-review.json` records the review scope and source binding. `source-audit.json` records the one-file missing-only resource change and three test/fixture additions. `summary.json` binds commands/results to the PR head. Raw local logs are retained with machine-specific paths sanitized.

[Hosted run 40444961260](https://github.com/c933103/AN-Paint/actions/runs/40444961260) was still running when this local evidence snapshot was published. No CI or release success is implied.
