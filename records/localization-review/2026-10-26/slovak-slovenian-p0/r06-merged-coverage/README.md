# PR179 Slovak / Slovenian: current 171-option coverage

Actual develop merge `e1e5433e63d45f5b76d39ce1a31ffc11fd7cd79d`, tree `98b89d126533df3c0dbaeb729c74e4bcb44a3a8a`; immediate baseline `e5f2d4e2d07e678076f022aa7b3ef923e13c3721`. Fresh actual push [40366731196](https://github.com/c933103/AN-Paint/actions/runs/40366731196) passed all six jobs. All actual source/APK, compiled resources, regression/lint, exact-script and API35 receipts are joined and hash-bound; PR receipts remain distinct. No release.

## Current result

- All171 picker options reconstructed from source; exactly sk/sl change versus the immediate baseline. Other169 rows remain exact.
- Each target adds78 reviewed live-consumer P0 values, reaching205 structural containers and P0 87/92. Existing127 values per locale remain exact. Five no-direct-consumer holds per locale remain absent; absence is not automatically a defect.
- Global structural P0 present6994 / missing8738. English-identical leaf count7051 is unchanged, not a defect count. Canonical717 containers/718 leaves; structural counts are not linguistic completeness.
- New independent AI complete-value/source-static review:148 accepted unchanged and8 revised, total156 newly reviewed values. No new linguistic acceptance is inferred from CI. Prior scopes are preserved, not counted again.
- All802 compiled displayed values match:156 new reviewed SK/SL,254 inherited SK/SL preservation-only,392 prior reviewed values.
- Actual JVM1374 pass with no failures/errors/skips; hosted Python1406 pass plus2 unnamed skips (1408 total), distinct from local1408/zero-skip tests. API35 45 app plus74 native source-selected cases pass; lint0;13 exact-script probes including the expected negative pass.
- Paired120-entry/60-tag warning acceptance, frozen history, absent P1 companion, and scoped59/outside112 classification remain unchanged. No native-human, whole-language, layout, physical-device or release certification.

## Reproduction and qualification

Ordinary and optimized final coverage outputs are byte-identical. The independent DOM parser matches every row and total. Corrected schema-join helpers and nine normal/optimized guard tests are included. FINALIZATION.md explains exact schema bindings and a preparation-only test-count correction. No original receipt fields were fabricated or altered.

Reproduction currently requires five locally validated baseline dependency files omitted from this publication, identified by exact hashes in baseline-dependency-inventory.json. Supply them at their original inputs/baseline paths only from the existing validated local copy or the original publication once resolved. This package does not replace or retry that pending upload. Use source checkout at the actual merge and baseline checkout at e5f2d4e, with their exact trees checked by the included helpers. Run recompute_coverage.py with inputs, both source roots, a fresh output directory, --mode actual-postmerge --actual-evidence actual-evidence --actual-manifest-sha256 5a478b926d24fc11bd2835d989844ba4ce7fdc2db796402ba74cbc39913d1853. Repeat with python -O and compare outputs. Then run verify_independently.py with --mode actual-postmerge --expected-merge e1e5433e63d45f5b76d39ce1a31ffc11fd7cd79d --expected-run 40366731196 and the matching source/output directories.

The prior PR178 coverage package remains separately publication-pending. The five copied baseline payloads are deliberately excluded; only their path/size/hash dependency inventory is supplied. This is not a retry, alternative encoding, or claim that any part of its whole202-file package is published here. Historical inputs/identity.json describes the earlier preview; current result and actual evidence supersede only that preview's execution status, not its source identities or review limits.
