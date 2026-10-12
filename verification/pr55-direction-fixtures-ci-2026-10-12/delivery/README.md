# PR55 direction-fixture delivery: independent retained-artifact audit

## Result and identity

PASS for the fresh delivery, exact-script receipts, retained build log and compiled-resource checks below. This does not establish overall CI, installed execution, rendering, upgrade signing, release readiness or linguistic acceptance.

- Public head: `6d603af92ee26d852af62cd1006468ef8472bfcf`
- Exact source tree: `d2379b932cc976bb5347515887ecdfc4729ee70d`
- Base: `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- Tested merge: `30abe4aa8d6089b11949635dc2d81f7a4b692073`, ordered parents base then head
- Run: [38290638790](https://github.com/c933103/AN-Paint/actions/runs/38290638790)
- Artifact-producing jobs: exact-script `114949610313`; build `114949610809`

The frozen parent-verified receipt `source-publication.json` binds these identities, remote content/mode verification and artifact metadata. This reviewer independently checked its identity fields and actual fresh bytes, but did not query GitHub or acquire the public head/merge commit objects. Local preparation HEAD differs from public HEAD; the exact tree is present. `audit_source_context.py` independently hashed all 1,062 local tracked files and checked executable modes against that tree. Only two JVM fixture files differ from the prior tree, as listed in `source-tree-diff.log`.

## Fresh artifacts and build binding

| Artifact | ID | Bytes | SHA-256 |
|---|---:|---:|---|
| APK and source | 11767490025 | 139658703 | `44ba566871c8351e2bed18ebf28aeccd6e78b626d6771b505af9057aca7f2cac` |
| Exact-script probes | 11766165812 | 6181 | `9bdc75f17223252caa3dbf23a8c43ed15a64f3466b118ad744e61c0eb3370523` |

Both ZIPs match metadata sizes, digests, run/head and merge-derived names. Every member matches the complete extraction: 11 APK/source members and eight probe members. The publication snapshot SHA-256 is `cdc96c41eff3fe055d3c2261815962a434477ca4cf4c886ce6bd10916698ae17`. Other artifact/job records are context, outside this review.

- Actual APK: `1a51061a64cb628b239cf3b442a4e6d372563cc5d7be789a4a41489d6aa054b2`
- Separate and APK-embedded source ZIP: `c4c4d696379d5ca9283a252f142507a5690c6eead7844c0e52d6fc6183fed70c`
- Build log: `c7fc5b1cbe81b974af4b71dde7ab1bed844bb4f679403036c0b7b5d62c81b5c8`, 273,208 bytes

`complete-run/build-log-result.json` retains ordered safe excerpts binding the expected merge checkout, source/resource production, Kotlin compilation, debug packaging and successful assembly, source extraction from the actual APK, and upload of artifact 11767490025 with the same archive digest. Log text does not independently establish remote authenticity or job conclusion. Raw build-info and all eight small probe receipts are retained in `receipts/`.

## Corresponding source, fonts and notices

All 1,059 bundled tracked blobs have exact current Git content and executable modes. The only tracked omissions, unchanged from the existing bundler, are `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore`. The other 6,258 files are confined to every declared native-source root: jxl-source 1,583; webp-source 338; heif-source 2,663; tiff-source 1,674. Per-root content/mode aggregate digests are recorded. Their upstream authenticity was not reaudited.

Embedded and separately delivered source ZIPs are byte-identical. All 14 font/inventory assets and all 21 legal assets have exact current-source path sets and bytes. The 13 font binaries match their inventory digests. Nôm UI-only identity, source attribution, inventory/name/licence metadata, all five MIT paragraphs and 21 OFL paragraphs are preserved. Both displayed aggregate notices include the full combined Nôm notice.

Ten pre-existing ordinary-font `licence_file` paths still do not resolve. `preexisting-inventory-observation.json` checks that the inventory and both aggregate notices are byte-identical to the prior tree. All current font attributions remain in `FONT_NOTICES.txt`, which is included in `THIRD_PARTY_NOTICES.txt`. This is an existing unresolved metadata-reference issue, not evidence of missing aggregate notices or licence removal by these fixture changes. Separate tracking is outside scope.

The 1,062-row complete source inventory is derived and checked in memory, not delivered as a full-tree dump. Its aggregate digest is `1edaebf615374212013b08742bae126ad108d1aeac19db3b2570fe1e145cade8`. The scoped 35-row font/legal manifest is retained.

## Exact-script and compiled resources

All seven real pinned-Gradle probe receipts pass exact source/wrapper/build identity, success, command/task inventories, log hashes, clean tasks and producer-before-consumer ordering: clean; debug/release merges; unchanged up-to-date; input-change regeneration and stale-output removal; restored-input release merge; second clean; release-first merge. All four complete generated-resource dictionaries equal current canonical XML or the declared temporary comment mutation. The source-bound probe implementation verifies complete output equality and stale-file removal before success. Only unrelated corresponding-source bundling is excluded. Gradle was not rerun here.

The standalone checker now requires exactly the eight expected archive files. Sixteen tests pass normally and with `python3 -O`: one valid fixture plus missing/extra archive members, missing/extra/wrong generated content, receipt omission, source/wrapper/build/log corruption, false success, changed command, missing clean task and fully rehashed producer-after-consumer controls.

The actual fresh APK has exactly 61 compiled M04 configurations: default, 59 current scoped locales and the generated Korean alias. Every value matches the current compact fixture after Android-escape decoding, with no unexpected locale. Manchu U+180E remains at zero-based positions 7, 18, 27; Mongolian U+202F at 7, 17, 30. Arabic M04 and both copy/insert wrappers exactly match current Arabic source; their mechanically composed route texts are in `complete-run/compiled-arabic-result.json`.

The full fresh resource-dump SHA-256 is `6e0cadda96f4e7ed41f0594c8a30ef2237d97ba0cde4faa12f325a74ecce9f9e`, equal to the prior dump, consistent with unchanged resource inputs. Current APK values were nevertheless independently compared against current fixtures. Executed aapt2 SHA-256 is `d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de`; the existing retained executable is also byte-identical to the fresh artifact's aapt2. No SDK was installed.

## Reproduce and preserve

From any working directory, with standard-library Python, Git, Bash, the exact source tree object, both fresh CI ZIPs and complete extractions, retained build log, and the hash-pinned aapt2:

```sh
bash run_audit.sh SOURCE_REPO CI_ARTIFACT_ROOT AAPT2 NEW_OUTPUT_DIRECTORY
```

The runner uses its adjacent frozen publication receipt. Six audit stages and 16 checker tests in both Python modes pass. A second full run from `/tmp` produced byte-identical six JSON results, two scoped resource texts and the font/legal manifest; see `portable-result-equality.json`. Duplicate rerun outputs were discarded.

For the one-time local/predecessor context check, the repository also needs the prior tree and an exact current-tree working copy:

```sh
python3 audit_source_context.py --repo SOURCE_REPO --output-directory EXISTING_OUTPUT_DIRECTORY
```

The prior frozen review's file set and bytes remain unchanged, confirmed by `frozen-inputs-result.json`. No source edits, GitHub writes, Work tasks, historical evidence changes or installed tests were performed. No APK, source ZIP or full-tree dump is included here. `DELIVERY-FILES.json` lists the compact evidence files.

Compiled/asset checks do not establish runtime selection, shaping, clipping, accessibility, route execution, pixel equality, linguistic fluency or completion of the 81 fallback locales. Signature/upgrade-key, ABI/alignment, native authenticity, device and visual acceptance are outside scope. Build-info explicitly identifies a CI debug key and separate test status; this is not an upgrade-ready or fully verified release.
