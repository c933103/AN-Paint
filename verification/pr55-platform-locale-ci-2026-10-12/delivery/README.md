# PR55 platform locale-binding successor: independent delivery audit

## Result

PASS for the fresh delivery artifact, corresponding source, seven exact-script probes, font/legal assets, compiled M04/Arabic, picker arrays/platform XML, and the actual application manifest binding.

The fresh APK now declares the application-level Android `localeConfig` attribute as a typed reference to its exact packaged `res/xml/app_locales.xml`. This is independently confirmed by pinned aapt2 and binary XML decoding. All 167 names/tags/platform locales remain exact. This closes the predecessor's **compiled binding finding**; it does not claim installed LocaleConfig execution, Settings UI visibility, overall CI success, rendering, upgrade signing or release readiness.

## Exact source and artifact identity

- Public head: `e19c766eb3eaedc1b3cd3657bb92864f81a9498a`
- Tree: `dc1ba97dacc573ead73729297eb739ecb244dcf5`
- Head parent: `b0697fd58a2a37fb94e351f4c4ec68757b0f6b5e`
- Base: `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- Tested synthetic merge: `a437d0a7daa51c7c339bf04add38545cd74b0fc2`, same tree, ordered parents base then head
- Run: [38299305241](https://github.com/c933103/AN-Paint/actions/runs/38299305241)
- Artifact-producing jobs: build `114978023561`; exact-script `114978023632`
- Frozen coordinator receipt SHA-256: `eb404e011bdb170ea940560d8963385289b64dcaebbe753f923c1370d17c9539`

The coordinator verified all 1,094 remote leaves/modes. This reviewer checked every local source byte/mode against the exact tree, and artifact bytes against supplied metadata. Remote authenticity remains the coordinator's authority; no duplicate GitHub downloads or polling were performed. Local preparation HEAD is not the public-head identity. Other jobs in the frozen receipt are context, not acceptance claims, and their live status may subsequently change.

| Artifact | ID | Bytes | SHA-256 |
|---|---:|---:|---|
| APK/source | 11769343484 | 139701485 | `073ee0409cab14155a4d6cc5d297c809a21252f7920ca45dc49c665bff26a3fd` |
| Exact-script | 11769262901 | 6180 | `0aa8e943e2cee34b707cd464166117fcdc5784044c0aa769be769ea01959b987` |

Both archives' digest, size, run/head and merge-derived name match. Every extracted file equals its ZIP member: 11 delivery files and eight probe files.

- APK: `cdc5e7255401e8557a31db0bd04d26f3ef486b0b749e596857eb9dfdb9741126`
- Separate and embedded source ZIP: `f80c249525eab8b5bccd3ae01aafbfc5fa3ea9b2731452fbc8466cd52abbe28c`
- Complete build log: 272,775 bytes; `2b1e0e61d75c13bef6e37ccd2986b802e56b77100b9fc6272888f26cef5d69de`

The retained build-log audit binds the exact merge checkout, corresponding-source/resource production, Kotlin compilation, debug packaging/assembly, embedded-source extraction and matching artifact upload in order. Raw probe logs, summary and build-info are retained in `receipts/`; the full build log is hashed and excerpted rather than duplicated.

## Actual application binding

The application has 13 attributes. Its `http://schemas.android.com/apk/res/android:localeConfig` has framework attribute ID `0x0101065b`, typed-reference value `0x01`, and target `0x7f100000`. The **target is derived from this APK's compiled resource table**, which maps it to the default `xml/app_locales` entry and exact file `res/xml/app_locales.xml`, type XML. No APK target ID is hardcoded.

The stable framework attribute ID is separately checked against the [AOSP API-finalization commit](https://android.googlesource.com/platform/frameworks/base/+/637acc5b42539a1a26ea81bf960c6bcf8359a2c1%5E%21/); its short source receipt is retained. This framework identity is distinct from the APK-specific target ID.

The aapt2 check is scoped to immediate application attributes, so a child activity attribute cannot satisfy it. The independent binary XML parser reports namespace, name, numeric name-resource ID, value type and data for every application attribute. Both application and library source manifests declare `@xml/app_locales`.

- Fresh binary manifest SHA-256: `e9b5fb6516917ba8cb1bf3cdfe09b5ad97d6d748d28cb7b32c1c920e4371f392`
- Packaged binary platform XML SHA-256: `cfb795c2dcf3d51c7d7c966f5aeb22812cbbd7e7b84eea0551396e5a72af31ec`
- Full compiled resource dump SHA-256: `53f73fdcaa0747072bb49b57eb2f9f264aa6f3a3627dee99c045449fda34908b` (not retained)
- Executed aapt2 SHA-256: `d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de`, also equal to the tool delivered in the fresh artifact; no SDK installation

The predecessor's 12 application attributes have unchanged decoded semantics; three string-pool indices relocate while retaining identical decoded values. `localeConfig` is the sole semantic attribute addition. The predecessor finding and complete old review remain frozen and unchanged.

## Exact inventories and corresponding source

All 167 compiled picker names/tags match current source in exact pairing and order, with 22 alias pairs. The actual platform XML's root, locale elements, nesting, Android name attributes and all 167 tags/order also match. The 27 accepted added options remain empty catalogues within the unchanged 59-scoped/108-open-fallback partition. No new translation or linguistic-acceptance claim is made.

All 1,091 bundled tracked files match the exact tree's content and executable modes. The only omissions among 1,094 leaves remain `.gitignore`, `.idea/codeStyles/Project.xml`, and `colorpicker/.gitignore`. All 6,258 extra files are confined to the four declared native roots: jxl 1,583; webp 338; heif 2,663; tiff 1,674. Per-root content/mode digests are retained; upstream native authenticity was not reaudited. Embedded and separate corresponding-source ZIPs are byte-identical.

All 14 font/inventory assets and 21 legal assets have exact paths/bytes. All 13 font binaries match their inventory digests. Nôm UI-only metadata, embedded names/licence metadata, attribution, five MIT paragraphs and 21 OFL paragraphs remain present in the individual/aggregate notices.

Ten existing ordinary-font `licence_file` references still do not resolve. Inventory and both aggregate notices are unchanged; full font attribution remains in the packaged aggregate notices. This is an unresolved pre-existing metadata-reference observation, not a new removal or independent legal conclusion.

The complete 1,094-row source content/mode inventory is computed in memory, not retained as a full-tree dump. Its digest is `6e271349ca1c2d6a2528e970e7f912e9e9643b10d01bfc17cd17980527a0354b`. Only the scoped 35-row font/legal asset manifest is retained.

## Probes, compiled wording and checker controls

Seven real retained Gradle probes pass source/wrapper/build identity, commands, log hashes, exact task inventories, clean stages, up-to-date behavior, input-change regeneration, stale-output removal receipts, restored-input release and release-first production order. The four generated-output dictionaries equal canonical XML or the declared disposable comment mutation. The probe implementation is source-bound and unchanged. Corresponding-source bundling is excluded only from these probes and independently checked in the actual delivery. Gradle was not rerun here.

Exactly 61 compiled M04 configurations match source fixtures: default, 59 scoped locales and the generated Korean alias. Manchu U+180E positions are 7, 18, 27; Mongolian U+202F positions are 7, 17, 30. Arabic M04 and copy/insert wrapper strings remain exact. Mechanical compositions are retained without installed/rendering claims.

The compiled picker, platform XML, M04, Arabic and 35-asset scoped evidence is byte-identical to the prior review. Exactly three source paths changed: HANDOFF.md (81 to 108), the application manifest declaration, and the existing installed language test's actual LocaleConfig check.

All **64 checker controls pass per mode**, both ordinary Python and `python3 -O`: 16 probe controls, 15 array/binary-XML parser controls, and 33 controls bound to compact fresh-APK evidence. Binding controls reject missing/duplicate declarations, wrong namespace/type/framework ID, wrong target in either or both views, child-only declarations, absent/duplicate/wrong-type/wrong-path/multi-configuration resources, XML root/nesting/attribute changes, and tag removals/additions/duplicates/order differences. A consistently changed APK-specific resource ID passes, confirming target derivation. Controls are synthetic perturbations of decoded real evidence, not mutated APK or installed-device acceptance.

## Reproduce and preservation

Using Python's standard library, Git, Bash, the exact source tree, fresh artifact ZIPs and complete extractions, the full retained build log and pinned aapt2:

```sh
bash run_audit.sh SOURCE_REPO CI_ARTIFACT_ROOT AAPT2 NEW_OUTPUT_DIRECTORY
```

The runner returns zero only after all artifact, source, probe, compiled and control gates pass. A fresh run from `/tmp` produced byte-identical output for all 16 result/scoped-resource/asset files. See `portable-result-equality.json`.

One-time contextual checks:

```sh
python3 audit_source_context.py --repo SOURCE_REPO --output-directory EXISTING_OUTPUT_DIRECTORY
python3 audit_successor_context.py --prior-review FROZEN_PREDECESSOR_REVIEW --current-review EXISTING_OUTPUT_DIRECTORY
```

The complete predecessor file set, sizes and bytes are unchanged. No application edits, GitHub writes, Work tasks, source publication, production/font/guard/deadline changes or installed tests were performed. No APK, source ZIP, complete resource dump, full build log or full source-tree inventory is included in this packet. `DELIVERY-FILES.json` inventories its compact files.

This scoped pass does not establish runtime selection, installed LocaleConfig status, Settings UI behavior, font shaping/clipping, accessibility, route execution, pixel equality, linguistic fluency, native authenticity, ABI/alignment or release readiness. Build-info explicitly uses the CI debug key; upgrade signing remains separate. Hosted JVM/device/regression outcomes belong to the coordinator's separate review.
