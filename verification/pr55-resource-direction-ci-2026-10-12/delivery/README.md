# PR55 resource-direction delivery: independent retained-artifact audit

## Result

PASS within the delivery, exact-script, retained-build-log and compiled-resource scope below. No discrepancy was found in those checks. This is not an overall CI, installed-device, rendering, upgrade-signing, release or linguistic-acceptance conclusion. Installed results and any residual visual differences belong to the separate parent review.

- Public head: `da4b40bd47a5d76d45b21d86fdc59368b4b52fd2`
- Current source tree: `ab6f5497e147e81d4c50f4954ea87f364be087aa`
- PR52 base: `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- Merge tested by CI: `daab4b4f2c87bc6475ba6a0d2c0f9b35ea36b7e0`
- Run: [38285607590](https://github.com/c933103/AN-Paint/actions/runs/38285607590)

The parent-verified GitHub receipt in `source-publication.json` binds the exact head/tree, base, ordered merge parents (base then head), merge tree and run. This offline reviewer checked those receipt fields and actual artifact bytes, source objects, logs and APK resources. It did not independently query GitHub or obtain the published head/merge commit objects locally.

## Actual artifacts

| Artifact | ID | ZIP SHA-256 |
|---|---:|---|
| APK and corresponding source | 11763915472 | `eefe0e62eae932b3bfff1b26d9202438dbbd4ef6407d5c6cb49c9a6923364a5d` |
| Exact-script generation | 11762769129 | `95162158bbc05b2e7b1361a6c2a46b17dbb5837346b40349e65a342dbe8609a0` |

All 11 APK/source-artifact members and all eight exact-script members match their complete extractions. The metadata run/head, merge-derived names, sizes and digests agree. The retained publication snapshot SHA-256 is `4ffa2733084ec6343880141fe82904e3142f2d5491f2d8702e3fdc400600499b`. Its other artifact records are contextual and are not audited by this delivery review.

- APK SHA-256: `7ce91b2ddfa890eaaa7e7b6e6c94f9d7c5616025595dfc57946b44db854d0769`
- Separate and APK-embedded source ZIP SHA-256: `1e28eb33dd3936f0e5660a20264afa0740467426ca049e33f021a1b5976aadb8`
- Probe summary SHA-256: `625bd6560e27400239eb212afcb331adbd7b79fea22c2322ade6363f4a012a36`
- Existing retained aapt2 SHA-256: `d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de`
- Full aapt2 resource dump SHA-256: `6e0cadda96f4e7ed41f0594c8a30ef2237d97ba0cde4faa12f325a74ecce9f9e`

`complete-run/build-log-result.json` also binds the exact retained build-log bytes (`4f72149d108c83491cfc07452a8109fae7598f6a580826e9b2d8fac60b31b1f4`) to checkout of the expected merge, source/resource production, Kotlin compilation, debug packaging, successful assembly, extraction of source from the actual APK, and upload of artifact 11763915472 with the same archive digest. It retains only relevant safe line excerpts. Job conclusion and remote log authenticity remain parent-provenance matters.

## Corresponding source, fonts and notices

The checker derives the complete current tracked inventory from the current Git tree: 1,062 leaves. The actual source ZIP contains 1,059 byte-exact Git blobs with exact executable modes. The only tracked omissions are:

- `.gitignore`
- `.idea/codeStyles/Project.xml`
- `colorpicker/.gitignore`

All other 6,258 files are confined to the four native-source roots declared by the current bundling script: jxl-source (1,583), webp-source (338), heif-source (2,663), and tiff-source (1,674). Each root is present. Their content/mode aggregate digests are recorded; upstream native-source authenticity was not independently reaudited.

The source embedded in the APK is byte-identical to the separate delivered ZIP. All 14 packaged font/inventory assets and all 21 legal assets have exact current-source path sets and contents; all 13 font binaries match inventory digests. The Nôm UI-only identity, source attribution, inventory/name/licence metadata, five MIT paragraphs and 21 OFL paragraphs are preserved in the appropriate actual assets. The full combined Nôm notice is included in both displayed aggregates. These are asset/notice-preservation checks, not independent legal advice.

The complete current source inventory is checked in memory; no duplicate whole-tree dump is delivered. Its reproducible aggregate SHA-256 is `95317ab9edfc34be33ab0066011df5223e8173210d3487acec2c4c78afa076ba`. `audit_direction_delivery.py` contains executable reconstruction/check logic, and `delivery-result.json` records counts, exact omissions, native-root aggregate hashes and empty content/mode mismatch lists. The separate 35-row `font-legal-manifest.jsonl` is a compact scoped asset digest list.

Ten pre-existing ordinary-font `licence_file` references still do not resolve. Their font attributions and licence text remain in `FONT_NOTICES.txt` and `THIRD_PARTY_NOTICES.txt`; inventory and both aggregates are unchanged from the previous source tree. `preexisting-inventory-observation.json` records the paths and one-time comparison. This is an existing unresolved metadata-reference issue, not evidence of licence removal by the resource-direction patch. Its separate tracker is outside this audit.

## Seven exact-script probes

All seven current pinned-Gradle receipts pass source identity, success, exact command/task inventories, original log hashes, wrapper/build hashes, required clean tasks and producer-before-consumer order:

1. Clean
2. Clean debug and release resource merges
3. Unchanged generation is UP-TO-DATE
4. Input change regenerates and stale output is removed
5. Restored input precedes release merge
6. Second clean
7. Release-first generation after clean

The four applicable complete generated-resource hash dictionaries match current canonical XML or the declared temporary comment mutation. Missing receipts, unexpected/stale members, incorrect hashes and reordered generation are rejected. The source-bound probe implementation checks complete generated-file equality and stale-output removal before it declares success. Only unrelated corresponding-source bundling is excluded. This verifies actual retained toolchain receipts; Gradle was not rerun here.

Twelve checker tests passed under normal Python and `python3 -O`, including a valid receipt plus corruption, missing/extra generated outputs, changed commands, wrong logs/wrapper/source, false success, missing probe, missing clean task and fully rehashed producer-after-consumer mutations. Raw small probe receipts and build-info are preserved in `receipts/`.

## Compiled M04 and Arabic

The actual source-bound APK contains exactly 61 M04 configurations: default, the current compact fixture's 59 scoped locales, and the generated mixed-script Korean alias. Every compiled value matches the current fixture after decoding Android escapes; there is no unexpected M04 locale.

- Manchu U+180E zero-based positions: 7, 18, 27
- Mongolian U+202F zero-based positions: 7, 17, 30
- The Arabic M04 value and both copy/insert wrappers exactly match current Arabic source. `complete-run/compiled-arabic-result.json` supplies the mechanically composed route texts for the parent's independent installed-record comparison.

The complete resource dump digest matches the earlier build's dump, consistent with unchanged resource inputs; current compiled checks independently compare the current APK with current fixtures. No translation or font-design re-review was performed. Compiled checks do not prove runtime selection across all locales, shaping, clipping, accessibility, route execution, pixel equality, linguistic fluency or completion of the 81 open fallback locales.

## Portable checks and frozen inputs

From any directory, provide a repository containing the current tree object, the retained CI root (both original ZIPs, their complete extractions and `build-job.log`), the existing hash-pinned aapt2 and a new output directory:

```sh
bash run_audit.sh SOURCE_REPO CI_ARTIFACT_ROOT AAPT2 NEW_OUTPUT_DIRECTORY
```

The runner uses the frozen publication snapshot beside its scripts, avoiding unrelated later changes to the parent's live metadata. Standard-library Python, Git, Bash and existing Android SDK Build Tools 35.0.0 aapt2 are sufficient. The aapt2 binary came from the earlier retained diagnostic tool artifact; it is not claimed to have been delivered inside the current APK/source artifact. No SDK installation was performed.

All six audit stages passed. A fresh full portable run produced byte-identical six JSON results and scoped text/asset-manifest outputs; `portable-result-equality.json` records their digests. Duplicate rerun outputs were discarded. `frozen-inputs-result.json` confirms the prior review's complete file set and bytes remain unchanged and `git diff --exit-code` against the current tree remains clean.

`checker-development-selftest.log` is a concise checker-development replay against prior receipts only. It gives no current-delivery credit. Prior source continuity observations and review-file hashes are one-time audit evidence, never application CI dependencies.

## Limits and handoff

Primary current results are in `complete-run/`. This reviewer made no production edits, GitHub writes, user-computer/Work tasks, historical evidence changes, Gradle rerun or installed tests. APK signing identity/upgrade key, alignment, ABI validation, native-source authenticity, installation, hardware and visual acceptance are outside scope. Build metadata explicitly identifies a CI debug key and separate test status; do not label this as an upgrade-ready or fully verified release.

No APK, source ZIP, full source tree or duplicate full-tree manifest is included in this reviewer directory. Preserve these small checkers, receipts and results with the parent's final evidence.
