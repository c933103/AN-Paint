# PR55 current-develop integration: independent delivery audit

## Result

PASS for fresh artifact binding, seven exact-script probes, corresponding source, font/legal assets, compiled M04/Arabic, and all compiled picker arrays and platform locale XML.

FAIL for a separate, pre-existing platform manifest binding: the actual APK omits `android:localeConfig` from its application element, despite the library source manifest declaring `@xml/app_locales`. The complete 167-entry XML is packaged, but its presence does not establish system-settings exposure. No overall CI, installed execution, rendering, upgrade-signing or release-readiness pass is claimed.

## Exact identity and provenance

- Public head: `b0697fd58a2a37fb94e351f4c4ec68757b0f6b5e`
- Tree: `b5d8cbeac9bf6d613ed7c3be787aa984826daafd`
- Head parents, ordered: `6d603af92ee26d852af62cd1006468ef8472bfcf`, `484d1b31cb113c88351e6d0dbdaa0d503e5dd834`
- Base PR52: `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- Tested merge: `e3dc717586539f8bbfe2ae3e3aae87e83db16d19`, parents base then head
- Run: [38296205283](https://github.com/c933103/AN-Paint/actions/runs/38296205283)
- Artifact-producing jobs: exact-script `114967784621`; build `114967784497`

The coordinator verified remote identity and all 1,094 remote leaves/modes. This reviewer independently checked every actual local byte/mode against the exact tree and the fresh artifact bytes against the supplied metadata. Remote authenticity remains the coordinator's authority; no duplicate remote downloads or polling were performed. The local preparation HEAD differs from the public head; the exact tree is present. The frozen final `source-publication.json` digest is `7ce0a7ac68ef4ea2225b06747434c5f6b0c214d12638d7ea51a3753dd5b54839`. Its other job/artifact records are context, not acceptance claims.

## Fresh artifacts and retained build evidence

| Artifact | ID | Bytes | SHA-256 |
|---|---:|---:|---|
| APK/source | 11767854139 | 139700725 | `166167f4a05bf3ce6b0fb7300122fe6f89c85b2210bec24a96a566377a6acc85` |
| Exact-script | 11768517779 | 6171 | `57548245e01888b5cc87fee0310ece493b50649a816bf48edab408405268d794` |

Archive identities, sizes, digests, run/head and merge-derived names match. Every extracted file equals its archive member: 11 delivery members and eight probe members.

- APK: `fa3dbb33025652e037fd91d13bb96f9a40a65f72f472173b9baa2f3c5d2f4a85`
- Separate and embedded source ZIP: `96689be0a84822c75d51751b4889f6cd974ee68d009533a913fdc558a0163f4e`
- Build log: 273,512 bytes; `0f0409fb304b3223254f54beef927a3df5cf653194dabdb456e69e7933e3a32b`

The build-log audit retains ordered excerpts binding exact merge checkout, source/resource generation, Kotlin compilation, debug assembly, embedded-source extraction and matching artifact upload. The seven raw probe logs, their summary and actual build-info are retained in `receipts/`. The full build log is not duplicated.

## Source, native bundles, fonts and legal assets

All 1,091 bundled tracked files have exact current content and executable modes. Of 1,094 tracked leaves, only the existing three bundler omissions remain: `.gitignore`, `.idea/codeStyles/Project.xml`, `colorpicker/.gitignore`.

The 6,258 extra source files are confined to all four declared native roots: jxl 1,583; webp 338; heif 2,663; tiff 1,674. Per-root content/mode aggregate digests are recorded. Native upstream authenticity was not independently reaudited. Embedded and separately delivered source archives are byte-identical.

All 14 font/inventory assets and 21 legal assets match current source paths and bytes. Every one of 13 font binaries matches its inventory digest. Nôm UI-only identity, embedded naming/licence metadata, attribution, five MIT paragraphs and 21 OFL paragraphs are preserved in individual and aggregate notices.

Ten pre-existing ordinary-font `licence_file` references still do not resolve. The inventory and both aggregate notices are byte-identical to the prior tree. Full font attribution remains in `FONT_NOTICES.txt`, included in `THIRD_PARTY_NOTICES.txt`. This remains an unresolved metadata-reference observation, not evidence of removed aggregate notices. See `preexisting-inventory-observation.json`.

The complete 1,094-row source manifest is computed in memory and not retained as a full-tree dump. Its SHA-256 is `cc07d6cd60d3ed2b1e459a08eaedbbc12bcbce782ab4d0685a2ce911859e0468`. The scoped 35-row font/legal manifest is retained.

## Seven real Gradle probes and compiled M04

All seven retained real pinned-Gradle receipts pass exact source/wrapper/build identity, commands, log digests, task inventories, clean stages and producer-before-consumer ordering: clean; debug/release merges; unchanged up-to-date; input-change regeneration with stale-output removal; restored-input release; second clean; release-first merge. All four complete generated-output dictionaries match current canonical XML or the declared disposable comment mutation. The unchanged source-bound probe implementation verifies output equality and stale-file removal before success. Only corresponding-source bundling is excluded there; the actual delivery checks it separately. Gradle was not rerun by this reviewer.

The APK has exactly 61 compiled M04 configurations: default, 59 scoped locales and the generated Korean alias. All values match current fixtures after Android-escape decoding. Manchu U+180E positions remain 7, 18, 27; Mongolian U+202F positions remain 7, 17, 30. Arabic M04 and both copy/insert wrappers exactly match current Arabic source. Mechanical route compositions are retained without an installed/rendering claim.

The full resource dump was hashed, not retained: `53f73fdcaa0747072bb49b57eb2f9f264aa6f3a3627dee99c045449fda34908b`. Executed aapt2 digest `d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de` equals the fresh artifact's tool. No SDK installation was needed.

## Actual picker and platform XML

All 167 compiled picker names and tags match current XML in exact order and pairing. Both 22-entry alias arrays match too. The actual compiled platform XML contains the same 167 locales, exactly matching source and picker order.

All 27 accepted added options are present with their source-defined names/tags and remain empty resource catalogues. They belong to the unchanged 59-scoped/108-open-fallback partition; there is no new translation or linguistic-acceptance claim. Accepted language identities and wording were not re-reviewed. Per-option positions, catalogue digests and status are retained in `compiled-picker-result.json`.

## Separate pre-existing manifest finding

The source declaration is at `Paintroid/src/main/AndroidManifest.xml:5`. The actual debug APK application contains 12 attributes and no `localeConfig`. This is confirmed twice: pinned aapt2's application excerpt and independent binary XML decoding of every application attribute, including namespace, name, numeric resource ID and typed value. It is not merely a missing symbolic name in printed output.

Evidence: `compiled-platform-manifest.txt`, `compiled-application-attributes.json`, `compiled-picker-result.json`. The picker result labels array/XML checks PASS and the manifest binding FAIL separately.

`preexisting-manifest-observation.json` establishes that the preceding direction-fixture APK and fresh APK binary manifest bytes are identical: 5,320 bytes, SHA-256 `652f94b8e56061f9b4342d258d6d5724717ce059726cf2426a0d56e08f677bdb`. Both source manifest files are unchanged too. Therefore this issue was not introduced by the current develop integration. The supplied delivery artifact has no merged-manifest/blame report; the precise removal stage and installed system-settings behavior remain unverified.

## Reproduce, limitations and preservation

With standard-library Python, Git, Bash, the exact source tree, fresh CI ZIPs and complete extractions, retained build log and hash-pinned aapt2:

```sh
bash run_audit.sh SOURCE_REPO CI_ARTIFACT_ROOT AAPT2 NEW_OUTPUT_DIRECTORY
```

The runner deliberately exits 1 for the manifest binding finding after completing all other checks. It does not relabel this as an all-pass audit. The 16 probe controls and 15 compiled-array/binary-XML parser controls pass normally and under `python3 -O`, 31 per mode. Synthetic parser controls are not APK acceptance. Running the complete audit from `/tmp` produced byte-identical 14 result/scoped-resource/asset-manifest files, including the same explicit manifest failure; see `portable-result-equality.json`.

One-time source and predecessor context checks:

```sh
python3 audit_source_context.py --repo SOURCE_REPO --output-directory EXISTING_OUTPUT_DIRECTORY
python3 audit_manifest_context.py --repo SOURCE_REPO --prior-apk PRIOR_APK --current-apk CURRENT_APK --delivery-result EXISTING_OUTPUT_DIRECTORY/delivery-result.json --output EXISTING_OUTPUT_DIRECTORY/preexisting-manifest-observation.json
```

The prior frozen review's complete file set, sizes and bytes remain unchanged. No source changes, GitHub writes, Work tasks, production/font/guard/deadline changes or installed tests were performed. No APK, source ZIP, full resource dump or full source-tree inventory is included. `DELIVERY-FILES.json` lists the compact retained files.

These byte/resource checks do not establish runtime selection, font shaping, clipping, accessibility, routes, pixel equality, linguistic fluency, native authenticity, ABI/alignment or release readiness. Build-info explicitly identifies the CI debug key; upgrade signing remains a separate private step. Hosted device/regression outcomes are the coordinator's separate review.
