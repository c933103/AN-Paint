# PR182 actual merged coverage and runtime verification

Actual merged source: `0ebd41d4d9b665213c776f5a0479a29ecabdd243`, tree `bc5e10affc54ba2e0788c749b4b78968379596ba`, ordered parents `[3160b02e939cd732536f4f3c896e082b19325eee, a17194b2402fbcea85ee526964b4adc497295ebf]`. Actual merge and develop independently read back. All 1,385 current and immediate-baseline file bytes/modes verified; exactly five changed paths, only one production XML. No source edits made by this verification.

## Coverage and reviewed wording

Immediate immutable actual baseline: R11 records commit `cd6dd599877b693d3b305b8aceb18de0c97618e4`, manifest `7eaeba5758fe3e19469fd2e9db2977ed35ff9a2c0e0dd3c8c07deadf8e892da1`. Selected actual outputs are hash-verified and all 171 options freshly recomputed, not relabelled. All structural/leaf/English-identical metrics remain unchanged. Serbian Cyrillic/Latin each stays 87/92 P0; global P0 7,142 present / 8,590 missing. Other 169 rows remain exactly unchanged; five held absences each and all frozen prior review categories preserved.

Accepted atomic Cyrillic pair: `save20_file_format` now says `Формат датотеке`; `ui_autosave_is_paused_to_protect_that_draft_use` names that exact field. Independent full-value/source-context review `a2e91394fd6fcbbeaefafe4ee879df23fd4791a33dba565b0a31bfbc2f78b164` is bound to the unchanged accepted bytes/attributes and current tree. Current Serbian review family: 147 previously reviewed unchanged + 2 corrected/reviewed = 149 unique values; 337 inherited values preserved. One identity is newly reviewed and one already-reviewed identity is reworded. No structural additions and no double counting. Historical PR180 148 newly reviewed / 338 preserved remains explicit and unmodified.

## Fresh actual runtime evidence

Natural actual push run `40402389745` completed success at attempt 1. All six jobs succeeded, no retry. All five original receipt families are retained under `actual-evidence/`: APK/source, compiled values, regression/lint, exact-script generation and API35. Producer manifest SHA256 `1ed57fde279530b33cb2c29888cba01fcfc4e72eff672fb083a8a6c5a0dfd404`; combined envelope manifest SHA256 `8c941cae6853c7c42a55edd12cdfb6831a6422a1bde59ce9dcdb95a6d3af29ef`. Original terminal run/jobs/artifacts, independently selected producer attempts and exact API35 case bindings are included.

- APK/source: 1,382 packaged tracked source files exact against 1,385 tracked files (three documented exclusions); 1,288 compiled displays checked. Current reviewed Serbian 149 plus prior reviewed 548, and preserved inherited 591 (Serbian 337 + SK/SL 254). Preservation checks do not create linguistic acceptance.
- Regression/lint: 1,384 JVM identities in 150 suites, 13 focused classes / 71 methods; hosted Python 1,421 passed + 2 skipped; zero lint issues. These two hosted skips are reported, not described as a zero-skip runtime suite.
- Exact script: 13 source-bound probes, including expected deliberate rejection, verified.
- API35: exact source-bound 45 app / 74 native cases; producer attempts core 1 / position 1 / composed 1; independent artifact selection and case-identity bindings matched. No PR-run artifact substitution.

Ordinary/optimized full source recomputation and actual joins are byte-identical. Independent minidom parsing matches all 171 rows and totals. Thirteen local report/identity/negative-join guard tests pass in each mode without skips. Guards reject prior PR180 148/338 scope, PR182 PR execution as actual push, wrong merge/parents/artifacts, missing receipt families, partial/failed run, corrupted pins and invented acceptance. Absent producer fields are joined through exact APK bytes/commit/tree, not fabricated.

Historical source-only preview is preserved under `historical-source-preview/`, manifest `f5028d051bfa2412279f3256b464632b6daca7f3a2fedba6de50fec9e1842391`. Its pending-runtime labels are historical, not current status. PR180 attempt-1 failure/retry remains in immutable R11; PR182 historical PR test failures remain in earlier records. Neither is rewritten or conflated with this successful natural actual push.

## Reproduction and boundaries

Run `recompute_actual.py` with `--inputs inputs`, exact successor `--source-root`, immediate PR180 merged-tree `--baseline-source-root`, `--actual-evidence actual-evidence`, combined manifest pin above and a new `--out`. Repeat using `python -O`, compare outputs, then run `verify_independently.py --mode actual-postmerge --expected-merge 0ebd41d4d9b665213c776f5a0479a29ecabdd243 --expected-run 40402389745` against each output. Run unittest discovery on `test_*.py` in both modes.

No underlying pending PR178 dependency payload is copied, retried or uploaded. No release, upgrade signing, physical-device, native-human, layout or whole-language acceptance is inferred; no cumulative global linguistic accepted count is invented. Publication is scoped to new R14 records, preserves previous records and does not modify PR56's body or source branches.
