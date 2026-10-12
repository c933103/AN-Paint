# PR52 context-typography: independent delivery audit

**PASS, bounded delivery review.** No new defect found in corresponding source, embedded source, retained generation probes, build provenance, packaged fonts/legal assets or compiled locale resources. This is separate from regression, installed/device, visual and linguistic acceptance.

## Exact candidate

- Head `ff8553d29a4c135c16b00beadf9cabba1e8d6fae`; sole parent `eb7451d320ba56e1ece6b1b55797da653966051d`
- Tree `cf1ffdb16e4e8401edce81a50b16ad6f21cdcaa8`
- Synthetic merge `a73e9482253d9774c14af72951697390d9f0141a`; ordered parents: base `484d1b31cb113c88351e6d0dbdaa0d503e5dd834`, then this head; same tree
- [Run 38319915849](https://github.com/c933103/AN-Paint/actions/runs/38319915849), attempt 1
- [APK/source artifact 11778765976](https://github.com/c933103/AN-Paint/actions/runs/38319915849/artifacts/11778765976): SHA-256 `1e68d26f4e6f2d159aff4229c20bdcc4b503620d9c6cf0b76ddab2771812b7b4`
- [Probe artifact 11778631396](https://github.com/c933103/AN-Paint/actions/runs/38319915849/artifacts/11778631396): SHA-256 `4bc45ce05cb5c4a680e5ca31c5fd9c0bb03725160b9aa24f24f9a1be2fc7bfb1`
- APK SHA-256 `3c775f01a485dc99b1ceca15278bcf79252721664b96cff9a3abec7ff149d52a`
- Source ZIP SHA-256 `e8b5851e43940c67c9a3d7a2cf826a5a86d9db2f34b9bea9926ab9a85dd65954`

Final parent-verified `source-publication.json` has SHA-256 `7ee33eb8674bf6d2bf9eff17bb2d2cb4b82e8b36af4e88b815d4b8851d496989` and reports all five jobs completed successfully. Its artifact-review-pending label is deliberately unchanged; this packet supplies the separate delivery verdict. This offline audit did not independently query GitHub. The local explicit tree is authoritative; the public head/merge objects are not present locally.

## Verified results

1. All **1,095** current tracked leaves match exact Git bytes and full permission modes. The **15** changed paths and hashes match the frozen authoring review; four are production files. Historical delivery (60 files) and authoring review (19 files) remain unchanged.
2. Every member of both artifact ZIPs matches its extraction and metadata. The APK's embedded source ZIP equals the separately delivered source ZIP. All **1,092** included tracked files match exact current source and modes. Only the same three packaging omissions remain: root and colorpicker `.gitignore`, and `.idea/codeStyles/Project.xml`. The four declared native source roots contain **6,258** extra files; their complete content/mode manifests equal the historical reference.
3. All **seven** retained real-toolchain probes match current source, merge/tree, authenticated artifact/run receipt, exact commands, successful logs, task order and generated hashes. Clean debug/release, unchanged, stale-output/input-change, restoration and release-first behavior are represented. Nothing was rerun in Gradle.
4. The complete build log is **272,808 bytes**, SHA-256 `d1c0e5ea707549777c969c1a00c4c9b54925dc1f74d95cb887929fed81ab2bad`. Ordered checkout, producer, compile/package, embedded-source extraction and upload markers bind to this exact delivery. Only predetermined marker strings and line numbers are retained here.
5. All **14 font assets (13 faces plus inventory)** and **21 legal assets** equal current source. Nôm embedded naming and MIT/OFL paragraphs remain intact. The same **ten** individual font-notice metadata paths remain unresolved; complete aggregate notices are present. This is unchanged metadata, not a new removal or legal conclusion.
6. Actual compiled M04 has **61 configurations**, including exact Mongolian-script controls; Arabic M04 and both wrapper strings equal source. All **167** picker names/tags, **22** alias pairs and **167** platform locales match source exactly and in order. Actual application `android:localeConfig`, framework attribute `0x0101065b`, reference type `0x01`, points to independently resolved `0x7f100000` / `res/xml/app_locales.xml` in both binary XML and aapt2 inspection.
7. Full compiled resource dump, binary manifest, packaged locale XML and scoped resource/font/legal evidence equal the historical reference. The APK and source ZIP themselves changed. Resource equality is not runtime typography, shaping or pixel equality. Scope remains 59 scoped catalogues and 108 explicit English-fallback catalogues; the 27 added catalogues remain empty.

## Reproduction and retained evidence

Start with `REVIEW-RESULT.json`, `source-preflight.json`, `artifact-bindings-result.json`, `delivery-result.json`, `probes-result.json`, `build-log-result.json`, `compiled-picker-result.json` and `historical-comparison-result.json`.

Run `bash run_audit.sh SOURCE_REPO CI_ROOT EXECUTABLE_AAPT2 HISTORICAL_REVIEW AUTHORING_REVIEW NEW_OUTPUT_DIRECTORY` with Python 3, Git and the retained inputs. CI_ROOT uses `apk-and-source` and `exact-script` directories/ZIPs and their `-metadata.json` files, plus the complete build log. The runner reads inputs and creates only a fresh result directory and disposable checker fixtures. It does not rerun or modify either prior review.

The existing Android Build Tools 35.0.0 aapt2 has SHA-256 `d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de`; it matches the tool in this artifact. No SDK was installed. A separate fresh-directory reproduction passes; deterministic output equality is recorded in `portable-result-equality.json`. Checker-only controls pass **92 per mode**, ordinary and Python `-O`: 16 probes, 15 compiled parser, 33 actual platform binding, 28 publication/artifact/build controls. These are not app tests.

Selected clean probe logs/summary, build-info, metadata, scoped compiled inputs and portable checkers are retained. `evidence-screen-result.json` reports field/token and sensitive URL query-key checks without suspected values or value hashes. The single build authorization marker is provider-masked. No APK, source ZIP, full build log, raw logcat, full source inventory or executable tool is duplicated. `DELIVERY-FILES.json` binds this compact packet.

## Limits

No application/source edits, GitHub writes, fresh Gradle/Android execution, installed acceptance, new linguistic acceptance, previously held raw evidence, or PR53 worker/upload occurred. This is a CI debug-key APK; upgrade signing, ABI/alignment/signature acceptance and release readiness are separate. Exact artifact bindings and terminal metadata do not substitute for independently reviewed regression or installed diagnostics.
