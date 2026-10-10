# Diagnostic-source release runtime review

11 October 2026, UTC+08. Head `9b62193455f3794192fe7e8b8ef6c3360d6e297f`, tree `d071e57d5774a639b7352f0cfa876b8922b4d899`. Tested merge `da8c027eb0e2c018c225240df0638b53a85d5e24` has exactly that tree and actual develop/head parents.

[Run 38081755104](https://github.com/c933103/AN-Paint/actions/runs/38081755104) completed all five jobs successfully. [Durable public checkpoint](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6101835290).

## Independently verified

- Release APK build took 861.830s with exit 0. Embedded/delivered corresponding-source ZIPs are byte-identical; build-info binds the run/commit/variant and APK/source hashes. All 1,475 included tracked blobs match the 1,478-entry source tree; three declared ignore/IDE paths are omitted. Bundled native-source prefixes are inventoried, not independently recertified.
- 793 JVM identities across 83 suites match the accepted-parent union exactly; no errors/failures/skips. Lint 0. Seven resource-generation stages, mutation/restoration behavior and log/source bindings pass.
- API30: 73 native+22 app methods, raw protocol/XML and source digest match. Ordinary 83.102s, gallery 34.651s, vertical 99.933s/90.449s. Seed/verify exclusions remain explicit.
- API35: 74 native+25 app methods and restart boundary. Ordinary 130.394s, gallery 47.233s, vertical 109.045s/104.676s. Complete runner 481s. Strict Korean/viewport/process log checks pass.
- Each API's four app-owned export ZIPs reconstruct all 104 original data files byte-identically, with 96 decoded/hash-bound PNGs, eight reachability receipts and 28 native gesture traces. This establishes the tested release MediaStore export on both API30 and 35; debug behavior is not inferred.
- Parent inspected all 192 actual PNGs across 16 complete contact sheets. Bounded JPEG quality endpoints, filename/description/control reachability and returned-editor states are supported. Initial dialog clipping remains visible. No full-dialog-fit, linguistic, accessibility or JXL/AVIF claim.

## Preserved auxiliary-evidence failure

The strict API30 verifier fails at absent four `ExactScriptResourceTest` log rows. The exact-source Korean method and its assertions passed in raw instrumentation; the snapshot records many app-PID `chatty ... expire ... lines`, consistent with pruning but not proof of each missing row's disposition. `api30-strict-failure.log` is preserved. `device30-core-receipt.json` reports only the separately revalidated core and explicitly records incomplete auxiliary evidence. No original test assertion, source method or CI gate was removed. API35's complete log audit must not be substituted for API30's missing rows.

`replay.py` requires a clean source checkout and original ZIPs, checks archive hashes, verifies all independent core checks, retains the exact auxiliary failure, and exits 2 when that evidence remains incomplete. Install Pillow for image decoding. Source/trace checks do not automate visual or native-language approval.

## Artifact identities and retention

See `archive-manifest.json` for every ZIP and contact-sheet hash. Original Actions artifact IDs:
- build 11681511169; diagnostics 11681086774; regression 11680678701
- generator 11681340062; API30 11681037733; API35 11681172724

Raw ZIPs and actual images remain in Actions (14-day retention) and the temporary analysis workspace; this text evidence package is durable, but is not a permanent full binary archive. Full archival remains open. Both previous 22-minute build timeouts remain failed historical evidence; later success is not proof of their detailed native/Gradle cause or of a diagnostic patch performance fix.

The PR has since advanced to cache correction 9a780d76, with its own review and CI. This review applies to 9b621934 only; it cannot establish current-source merge or release eligibility.
