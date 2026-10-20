# Frozen-source host verification

Candidate: `ac60801eb7c5e86099f1e17a3bf79132d1f8e9d8`
([PR152](https://github.com/c933103/AN-Paint/pull/152)).

- `python3 -m unittest discover -s tools -p 'test_*.py'`: all 1,054 tests passed,
  218.246 seconds.
- `python3 -O -m unittest discover -s tools -p 'test_*.py'`: all 1,054 tests passed,
  226.301 seconds.
- The source stayed fixed throughout both final runs. `source.json` identifies
  the published commit, instrumentation-source digest and four changed files.
  Those files were checked again after both suites completed.
- The complete candidate tree was compared with the immutable develop tree
  plus its four intended changes before creating the PR. Remote path, blob and
  mode checks covered 1,253 files.

## Earlier invalidated run

`invalidated-normal.log` is retained, not replaced by the final pass.
That initial 1,054-test run ended with seven failures and one error because
additional diagnostic lines were edited into the position instrumentation
while the run was active. The installed-glyph evidence tests captured the
source digest at import and then correctly rejected the changed live source.
This was an invalid test run, not an application defect or a valid aggregate
pass. It demonstrates the source-binding guard's response to an actual
in-flight edit; it was not a planned negative-control experiment.

No assertion was removed or relaxed. The corrected procedure restored all
remaining base metadata, froze the source and ran both full modes again.

The stdout includes expected negative-fixture diagnostics emitted by the test
suite. The unittest result is recorded separately near the top of each final
log. Host success does not establish Kotlin/Android compilation or a device
pass; [exact-source Android CI](https://github.com/c933103/AN-Paint/actions/runs/39412208315)
remains the source for those outcomes.
