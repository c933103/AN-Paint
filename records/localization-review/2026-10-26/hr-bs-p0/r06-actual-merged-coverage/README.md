# PR183 actual merged coverage and runtime verification

Actual source merge `33472a55aee482bbdc7c0bebd93356ef2b1a1ae3`, tree `d41defc26ef6870aa35393c2f3fb909c5e803747`, ordered parents `[0ebd41d4d9b665213c776f5a0479a29ecabdd243, b97ba1e0b4abe31f9758242a82e8ff58f356ffe4]`. Independent Git/develop readbacks retained. All 1,388 current / 1,385 immediate-baseline bytes and modes reverified; exactly 18 changed paths, three additions, only Croatian/Bosnian production XML changes.

## Fresh all-option coverage

Immediate actual baseline is immutable R14 at records commit `f3c1b1297931a175222175711c76b64df91c2146`, manifest SHA256 `74c64ac05dba3f76ff4235169ee3a2adf1611415a5131d24b20d3a74db421e87`. Selected output indexes are hash-verified and every one of 171 locale rows is freshly recomputed, not relabelled.

Croatian P0 8→86/92; Bosnian 9→87/92, +78 each. Global P0 present/missing 7,298/8,434; all containers 51,321/71,286; leaves 51,355/71,423; English-identical leaves 7,051 unchanged; source-different leaves 44,304. Other 169 rows unchanged. All 98 Croatian + 117 Bosnian prior values/attributes preserved (215). Five protected absences per locale plus Croatian `save20_title` and P1 companion absence remain unchanged. Existing frozen prior categories and 59 scoped/112 outside boundary preserved.

Exactly 156 independent full-value decisions (155 accept + one reviewed revision) are bound to accepted value/attribute/source-token hashes and current source. Composition qualifications remain per value. Current Serbian 149 reviewed/337 preserved and historical PR180 148/338 remain distinct. Bounded compiled-reviewed arithmetic: 156 new HR/BS + 697 prior (149 Serbian + 548 earlier families) = 853, not 853 new acceptances or an invented global linguistic count. Inherited compiled preservation: 215 HR/BS + 591 prior = 806, not linguistic acceptance.

## Actual natural push evidence

Actual push `40413135176` completed success at attempt 1; all six jobs succeeded without retry. Five original verifier receipt families are retained under `actual-evidence/`, along with fresh actual terminal run/jobs/artifacts, exact case bindings and independently derived selection.

Producer manifest SHA256 `315e17e51b1a7b06e8ece142fbb9750cf45744ff08401a7cc4b701cd8c5a26e4`; combined envelope manifest SHA256 `b4d7d0687a7dfb452e3c05e894b29b61299c2686230f16d52a12e018c809ae00`.

- APK/source: 1,385 packaged tracked source files exact against 1,388 tracked files, three documented exclusions; 1,659 compiled displays checked (853 bounded reviewed + 806 preservation-only).
- Regression/lint: 1,394 JVM identities / 151 suites; hosted Python 1,433 passed + 2 skipped; zero lint issues. Hosted skips remain explicit, not a zero-skip claim.
- Exact-script generation: 13 source-bound probes including expected deliberate rejection.
- API35: exact source-bound 45 app + 74 native cases, independent artifact producer selection at attempt 1. No PR-run substitution.

All source+actual joins rerun under normal and optimized Python with byte-identical outputs. Independent minidom parsing matches all 171 rows and totals. Fourteen local source/identity/scope/promotion guard tests pass per mode without skips. Missing producer fields join via exact APK bytes/run/commit/tree rather than fabricated fields. Prior PR artifact IDs were freshly read as remote metadata only and are used solely to reject substitution; no PR artifact payload was copied.

## Immutable history and unresolved publication boundary

Frozen source preview is retained under `historical-source-preview/`, manifest SHA256 `7a30a1e3a57b35982276c561e513eb4fc38d15b4c4616b78841d6bded6fd5964`. Its pending-merge/CI descriptions are historical, not this report's current verification status. Parent's earlier `actual-source-recomputation.json` is also historical; final integrated results are under `ordinary/` and byte-identical `optimized/`.

R05 publication remains unresolved. A pending-confirmation operation was reported as `manager:8ecf0080edb64d05b11effdbd9ce3819:2`; attribution to the uploader and exact target metadata are not confirmed until the operation returns. This report does not claim missing user authorization or denial. It does not retry, copy, re-encode, reroute or upload the pending payload. No records-ref lease is acquired, and no upload or ref mutation has been made by this final-report preparation. Successor PR184 remains independent.

Before copying, every selected newly produced actual postmerge payload and frozen preview payload was hash-compared with `r05-publication-inventory.json`; zero overlap. Only `postmerge-ci` supplied actual execution bytes. No `ci/` or `hosted-public/` payloads copied. Coincident plain-text verifier logs were excluded by the producer before its manifest freeze. The final complete payload audit is retained in `pending-r05-overlap-check.json`. Root subsequently authorized ordinary new-record publication on a distinct branch `records/hr-bs-p0-postmerge-20261026`, pinned base `2ed70e24c609f587beffe43a611df03ccc6ed737`, prefix `records/localization-review/2026-10-26/hr-bs-p0/r06-actual-merged-coverage`. This separate branch does not acquire or move the original `records/hr-bs-p0-20261026` lease. Every new payload remains disjoint from the R05 inventory; no pending action is retried, rerouted or substituted. The unresolved R05 provenance stays explicit; current actual verification is independently complete. Publication receipt/readback is separate from this immutable package.

No pending PR178 payload handling, Serbian records branch write, PR56 body change, source edit, release, upgrade signing, physical-device/native-human/layout/whole-language certification or extra linguistic acceptance.

## Reproduction

Run `recompute_actual.py --inputs inputs --source-root <exact reviewed tree snapshot> --baseline-source-root <exact immediate baseline snapshot> --actual-evidence actual-evidence --actual-manifest-sha256 b4d7d0687a7dfb452e3c05e894b29b61299c2686230f16d52a12e018c809ae00 --out <fresh output>`. Repeat with `python -O`; compare outputs. Run `verify_independently.py --mode actual-postmerge --expected-merge 33472a55aee482bbdc7c0bebd93356ef2b1a1ae3 --expected-run 40413135176` against each output and unittest discovery for `test_*.py` in both modes. No synthetic fixture is actual execution evidence.
