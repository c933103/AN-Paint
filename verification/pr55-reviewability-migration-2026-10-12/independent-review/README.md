# Migration authoring-review bundle

Read `REVIEW.md` for the bounded result and `CI-ACCEPTANCE.md` for the fresh-run gates. This bundle is intended for a separate evidence ref, never as a new permanent application snapshot requirement.

Source reviewed: staged tree `592a60877524c5c118695cb45a4d0d5cd257b25a`; complete local/index binding and one-time removals are in `source-binding.json`. No production files were edited by the reviewer.

## Results

- Independent 114 focused methods pass normally and optimized; separate38 font methods pass.
- Both writer full modes:642/642, exit0, no skips, under the unchanged240-second cap. `writer-aggregate-audit.json` independently reconciles every raw identity against current discovery.
- One-time audits preserve677 parsed wording/import values, production/resources/fonts/workflow and selected operational/licence inputs.
- All six initial source-review findings are repaired. Four originally accepted malformed-font/licence cases now independently reject.
- Revised JVM raster policy still needs fresh compilation/native artifacts. Installed zero-difference policy remains separate and unchanged. No release/fluency/Android-readiness claim.

## Portable checks

Run with the reviewed source checkout and writer evidence directory supplied explicitly:

```sh
python3 bind_review_source.py --repo SOURCE --output binding.json
python3 audit_migration_data.py --repo SOURCE --output data.json
python3 recheck_font_fail_closed.py --repo SOURCE --output font-recheck.json
python3 audit_writer_aggregates.py --repo SOURCE --writer-evidence WRITER_EVIDENCE --output aggregates.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=SOURCE/tools python3 -m unittest -v test_current_font_contract test_locale_font_coverage test_font_disclosures_pr12 test_current_localization_contracts test_help_commons_provider test_localized_dialog_composition test_ci_timeout_budget test_translations test_extend_nom_ui_font
```

For the focused command, use SOURCE as the working directory and add `-O` before `-m` for the optimized mode. The binding/audit scripts intentionally refer to this one reviewed snapshot; do not install them as normal product CI gates or rebind old receipts to a successor.

The writer separately delivers `final-host-ordinary.{log,json}`, `final-host-optimized.{log,json}` and `host-method-retirement.json`; this review manifest does not duplicate them. Their exact hashes are bound by `writer-aggregate-audit.json`. Runtime baselines and raw historical reports are already archived separately.

`EARLY-FINDINGS.md` and the `early-draft` inputs are provisional review history. The small `post-fix-stale-repro-partial.log` records two correct repaired rejections before an obsolete probe expectation failed. It is not a completed test or a product regression. The final in-memory recheck and JSON supersede that partial probe. No source translations or language decisions were re-reviewed.
