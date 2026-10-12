# Independent actual-artifact review: PR55 resource-context direction

## Outcome

The exact run remains **FAILED**: JVM executed 906 expected identities, with 902 passing and four assertion failures. Installed API30 passes 95/95 and API35 passes 104/104. Delivery/source, compiled resources, exact-script probes, native preparation and lint pass their reviewed scopes. No overall PR/release approval is given.

The four JVM failures and source-backed fixture diagnosis are in `JVM-FAILURES.md`; all original XML stacks remain in the replay pack. Twelve new API30/35 native mismatch/lifecycle executions passed. The two API21/24 LEGACY geometry assertions and two retained-notice offset assertions remain failed. A separate successor is required; this checkpoint is not retrospectively relabelled.

## Exact binding

- Public head: `da4b40bd47a5d76d45b21d86fdc59368b4b52fd2`
- Reviewed tree: `ab6f5497e147e81d4c50f4954ea87f364be087aa` (1,062 leaves)
- Base: `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- Synthetic merge: `daab4b4f2c87bc6475ba6a0d2c0f9b35ea36b7e0`, ordered base/head parents, same tree
- Run: [38285607590](https://github.com/c933103/AN-Paint/actions/runs/38285607590)

The parent independently read back the remote tree/parents/run. This review checks exact downloaded bytes, local tree contents, retained checkout/build/install/upload receipts and source-derived expectations. It does not authenticate GitHub independently of those parent-provided remote receipts. `source-publication-final.json` retains final metadata; `run-binding.json` is the earlier exact binding used by the regression checker, with the same source/run and regression artifact digest.

Artifacts:

- Exact-script 11762769129: SHA256 `95162158bbc05b2e7b1361a6c2a46b17dbb5837346b40349e65a342dbe8609a0`
- APK/source 11763915472: `eefe0e62eae932b3bfff1b26d9202438dbbd4ef6407d5c6cb49c9a6923364a5d`
- Regression 11764101989: `459d6ddd95b4ae8f3126477cf8d45d8c01182bf4b342ddb3f1e77e68abae9e7e`
- API30 11763119963: `72f9387c99e9d1cdc33b0cbb1e0fef813dea96b30cc714e5dbb6c3dba5d79b1d`
- API35 11764510950: `b7de7d098fd25d60b4a0f743f0f55e867555d61fc36744a8f5c65d1ffd6eada5`

Every original archive/extraction was byte/digest/path checked by its respective reviewer. Existing source and prior review directories were left unchanged.

## Build, probes, corresponding source and compiled values

`delivery/README.md` and its six-stage results provide the independent detailed audit. All seven exact-script probes passed their exact command/task, source, ordering, hash, regeneration and stale-output checks. Twelve checker controls passed ordinary and optimized Python; a portable rerun reproduced the six result JSONs exactly.

The delivered source accounts for all 1,062 tracked leaves: 1,059 exact Git blobs/modes, and only the existing `.gitignore`, `colorpicker/.gitignore`, `.idea/codeStyles/Project.xml` bundle omissions. All 6,258 extra files are within the four currently declared native-source roots. Embedded and delivered source ZIPs are identical. All 14 font/inventory assets and 21 legal assets match current source. The known ten individual inventory licence paths remain unresolved; aggregate attributions/notices are retained. This existing metadata issue is a separate tracker follow-up, not a licence-removal finding.

All 61 actual APK M04 configurations match current fixtures: default, 59 scoped locales and the generated Korean alias. Manchu U+180E positions 7/18/27 and Mongolian U+202F positions 7/17/30 are retained. Arabic reason/wrappers equal current source and installed route text. These checks are not a new linguistic review or completion claim for the 81 open fallbacks.

## Host/JVM and exact raw outcomes

Hosted Python reports 643 total, 641 passed and two skipped in 162.045 seconds. Its compact output does not name skipped identities. This differs from the separately archived local 643/643 no-skip authoring runs; do not conflate them.

The current-source-derived JVM multiset has exactly 906 executions, all present once. 902 pass, four fail, none are skipped. Native compilation completed sufficiently to execute all cases, including all 14 new direction identities. The four failures are preserved, not treated as missing or infrastructure-only results.

`phase-results.json` independently binds raw phase logs/times: Python exit0/162.346 wall seconds, JVM exit1/525.020, native preparation exit0/77.779, lint exit0/118.363. `regression-job-provenance.json` verifies checkout of the exact merge, unit-test Kotlin compilation, 906/4 failure summary and upload of the exact regression ZIP. The full raw job log is retained compressed.

## M04 actual rasters and controls

The complete automated reconciliation passes its integrity and hard-readability scopes:

- 112 success PNG/JSON pairs
- 28 normal-landscape pre-assertion diagnostics
- 189 complete-layout/actual-textview/JSON triplets (378 PNGs)
- 78 genuine native mutation controls and four summaries
- 110 positive frames, of which 109 are exact and one remains explicitly review-required

All arrays, alpha samples, component/opaque-loss metrics, independent complete references, mutation relations and source-bound messages were recomputed. The old Ainu advance guard is still false at right1233.043 versus width1232; visible ink outside the layout remains zero. It is diagnostic only.

Fresh mixed-Arabic disposition: the original actual and complete-reference images were viewed, and every original pixel was recomputed. The only losses are layout(1232,29) RGBA[0,0,36,7] and (1232,30) RGBA[0,0,0,1]. They belong to a 78-sample component whose other 76 samples and all opaque ink survive. Component alpha sum is10633, lost alpha8; no component or opaque sample disappears, no finite-allocation edge is touched and all other ARGB samples match. This specific frame is reviewed as a low-severity antialias fringe with no demonstrated material glyph/mark/line loss. `exact_pixel_comparison_passed=false` and producer `review_required=true` remain intact. There is no new universal tolerance or production workaround. `fresh-positive-disposition.json` binds the two inspected image paths/hashes and original-resolution forensic result.

The actual/reference PNGs also equal the prior run's bytes, which is corroboration only. The fresh pixels and metrics were reviewed independently. Double-scale whole-glyph and detached-mark native controls were also visually inspected: the former removes the A while retaining the mark; the latter removes the mark while retaining the A. All six focused controls, including the independent opaque-stroke removal, are recomputed across both scales. Components are image structures, not linguistic glyph segmentation.

## Installed proof and limits

`installed/README.md` and its expiry-safe replay preserve the full independent audit. All 13 source-derived phase protocols, terminal records, XML identities and coverage unions reconcile. API30 has95 scheduled tests of97 eligible with the two explicit restart omissions; API35 has104 scheduled tests. All scheduled identities pass. Exact same-run main/test artifact download/install provenance and the API35 force-stop/restart boundary pass; no on-device APK hash or private upgrade signature is claimed.

The previously failed Literary Chinese native Save method passes. Actual landscape workspace, Save, format-popup and JPEG frames show mounted vertical columns. The target becomes visibly reachable before native DOWN/UP; busy=false. Both APIs' 192 vertical frames and four Arabic PNGs were inspected by the installed reviewer. Input/geometry/export receipts preserve all controls and original deadlines.

Installed Arabic COPY/INSERT references have4,287/4,435 ink pixels, with zero missing, overflow or different-ARGB pixels. Natural-update receipts show different full text, equal88→88 positive layout heights, actual requestLayout and settled completion. The installed strict zero-difference comparator was unchanged.

Save telemetry records24 opens/72 snapshots per API. At recorded points, process/activity/target/workspace-root locales match the selected locale; application is en-US. The successful observer runs before click dispatch, so dialog locale is absent. It does not observe the hypothesized reset, a process/resource mismatch or the mounted dialog's resource locale. Successful mounted geometry establishes the repair-path result, not the historical callback mechanism.

Installed software captures do not prove hardware-compositor rendering, every language's shaping, external provider/network routes, document-provider file writing, signing/upgrade readiness or general release acceptance. Four failed JVM assertions still block the exact full gate.

## Reproducibility and transport

The bounded `regression-replay-inputs.zip` retains991 raw files: all M04 PNG/JSON inputs, all95 JVM XMLs and phase logs/timing receipts. It is18,791,932 bytes, SHA256 `047c412858373a4db216ca683bfd8c71caf1d6d18d98b17d0d6c8fe1cb9c4683`. Per-member digests are in `regression-replay-manifest.json`. A replay was actually run and reproduced all four complete result sections, including the failures. Ordered transport parts may be used only if reconstruction matches that exact ZIP digest/length.

Run `replay_regression.py --repo SOURCE_REPO --output RESULT_JSON --evidence REVIEW_DIRECTORY`. The repository must contain the reviewed tree object and current helper dependencies. Run `forensic_fresh_mixed_reset.py --frames EXTRACTED_FRAME_DIRECTORY --output RESULT_JSON` for the component/mutation forensic check. `audit_regression_job.py` accepts the retained compressed job log. Original outer APK/source/regression ZIP rehash is explicitly excluded from expiry replay; their original audited digests/receipts remain recorded separately.

The installed component includes its own executed expiry-safe replay and compressed raw input pack. No APK/source ZIP, full source tree or duplicated whole-tree manifest is part of this review. The final delivery manifest lists only the frozen intended payload. No production edits, public writes, old-checker rebinding or threshold/deadline changes were made by this reviewer.
