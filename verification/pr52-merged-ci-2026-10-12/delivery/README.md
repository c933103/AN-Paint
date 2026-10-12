# PR52 merged-head: fresh bounded delivery audit

Result: PASS. No new defect found in this read-only source/artifact/probe/compiled-delivery audit. This does not establish overall CI success, installed/device acceptance, translation completeness, rendering or upgrade signing.

## Exact identity

- PR52 head: `eb7451d320ba56e1ece6b1b55797da653966051d`
- Head's ordered parents: `71f4d288669858e7975ec4c094b7f47a9a1ff145`, then accepted PR55 `4a35933ff6b6d0013dac8743cc5eeac1c1033e05`
- Exact head/accepted source tree: `b6bf7626c1d7c4aef669394970046ffc89a5c877`
- Actual PR52 base: `484d1b31cb113c88351e6d0dbdaa0d503e5dd834`
- Tested synthetic merge: `e17f49eddd01007a6e776a5d8981e8c1c41ba571`; ordered parents are that base, then PR52 head. Its tree is the same exact tree above.
- [Hosted run 38308218307](https://github.com/c933103/AN-Paint/actions/runs/38308218307), attempt 1
- [APK/source artifact 11773397420](https://github.com/c933103/AN-Paint/actions/runs/38308218307/artifacts/11773397420): 139,702,188 bytes; SHA-256 `8a51ba66aeccd1646556db9fc0af584eb21d6ea1f1fd0b7c3b1ac75d02cc4cfb`
- [Probe artifact 11773442101](https://github.com/c933103/AN-Paint/actions/runs/38308218307/artifacts/11773442101): 6,166 bytes; SHA-256 `f06e0b59e4fe7d30e3eac3d127a2ba12e38fbcc86298a223bbf53f86ca798e37`
- Fresh APK SHA-256: `838dc461599879a6047e44645bc1a5acad013129167c6535bcbfcd2b3ffcbfb4`
- Corresponding-source ZIP SHA-256: `27319149dda267593130b30eeacf20b89a1a0b05d7233295018dbeab169885dd`

The supplied `source-publication.json` is a parent-verified provenance snapshot. Its nested run still says in progress; that is not a final CI conclusion. This audit independently checks retained bytes and their exact bindings, including nested PR52 head/base/run data. It does not independently query GitHub. Local preparation HEAD is recorded separately; the explicit tree, not that local HEAD, is authoritative.

## Findings

1. All 1,094 local tracked leaves exactly match the required tree's bytes and executable modes. The accepted PR55 tree and merged PR52 tree are identical. There are no documentation, runtime, resource, font, workflow or test changes to rereview.
2. Every extracted artifact member exactly matches its ZIP. The fresh APK's embedded source ZIP exactly equals its delivered corresponding-source ZIP. All 1,091 included tracked-source files match the current exact tree content and modes; the same three packaging omissions remain. All four native-source content/mode manifests are unchanged (6,258 native extra files). The complete fresh corresponding-source ZIP also has the identical SHA-256 recorded in accepted PR55's delivery receipt. The APK as a whole has a different hash; broader APK binary equality is not claimed.
3. All seven retained real-toolchain generation probes bind to this synthetic merge/tree/run: clean debug+release, unchanged/up-to-date, changed input/stale-output, restored input/release, second clean and release-first. Commands, task ordering, generated hashes, log hashes and exact archive extraction all pass. Gradle was not rerun.
4. The complete retained build log is 272,892 bytes, SHA-256 `7f665212f0e0c0169c89231bc525141382cec03b90783160d0c2611b299f7361`. Its ordered checkout, producer/resource/compile/package, embedded-source extraction and upload markers bind to this exact artifact. The checkout is explicitly `refs/remotes/pull/52/merge` and uses actual base `484d1b31...`. This packet retains only expected marker strings with line numbers, not arbitrary surrounding log lines or partial logs.
5. Actual compiled application `android:localeConfig` has framework attribute ID `0x0101065b`, reference type `0x01`, and target `0x7f100000`. Independent resource-table resolution and binary XML/aapt2 inspection bind it to `res/xml/app_locales.xml`. The exact ordered 167 locale entries match the picker; all 22 alias pairs remain.
6. The full aapt2 resource dump, binary manifest, packaged platform XML and scoped picker/M04/Arabic/application-attribute evidence are identical to accepted PR55. M04 has 61 compiled configurations. All 14 font assets and 21 legal assets match exact source. Nom's embedded naming and MIT/OFL paragraphs remain intact. Ten pre-existing individual font-notice metadata references remain unresolved and unchanged; aggregate notices are present. This is not a new removal finding or legal conclusion.
7. Scope remains 59 scoped catalogues plus 108 outside-scope English-fallback catalogues across 167 choices. The 27 previously accepted added catalogues remain empty and untranslated. No linguistic re-review or completeness claim is made.

## Evidence and reproduction

Start with `source-preflight.json`, `artifact-bindings-result.json`, `delivery-result.json`, `probes-result.json`, `build-log-result.json`, `compiled-picker-result.json` and `merged-delivery-context-result.json`. The accepted PR55 baseline remains unchanged: its 59 listed files match its own self-excluding delivery manifest, and all 60 files including that manifest match this audit's `prior-review-freeze-manifest.json`. It was compared without rerunning or overwriting the earlier audit.

Run:

`bash run_audit.sh SOURCE_REPO CI_ARTIFACT_ROOT EXECUTABLE_AAPT2 PRIOR_REVIEW NEW_OUTPUT_DIRECTORY`

Requirements are Python 3, Git, the exact tree's clean-by-content source directory, this run's complete `apk-and-source` and `exact-script-generation` artifacts/extractions/metadata plus complete build log, the frozen accepted PR55 delivery directory, and a fresh output directory. Inputs remain read-only. Test perturbations use disposable temporary storage.

The executable aapt2 is the existing retained Android Build Tools 35.0.0 binary, SHA-256 `d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de`, exactly matching the tool in this fresh artifact. No SDK install was performed. The artifact copy is mode 0644, so the already executable equal-digest tool was used without changing an input.

The portable runner passes in a separate fresh directory after correcting a review-harness receipt-path lookup; the correction affected only audit tooling, not any application input or result. `portable-result-equality.json` records byte equality for all deterministic results and scoped evidence. Checker-only controls pass both normally and under Python `-O`: 16 probe checks, 15 compiled-parser checks, 33 platform-binding checks and 10 merged-identity/build-marker checks, 74 per mode. These do not count as app/device/regression tests.

`evidence-screen-result.json` records conservative raw-input and selected-packet screening without suspected values or value hashes. The one build-log authorization marker is provider-masked. No raw prior API30 packet, raw logcat, full build log, APK, source ZIP, full source inventory or tool binary is copied. `DELIVERY-FILES.json` binds this compact packet.

## Boundaries

No app edits, GitHub writes, fresh Gradle/Android/full-suite execution, installed app execution, user-computer/Work task, new linguistic acceptance, raw evidence repackaging or source re-review occurred. No ABI, alignment, signing-certificate or upgrade-key acceptance is asserted. The CI artifact uses the CI debug key; upgrade signing is a separate private packaging step. Overall run status and installed findings belong to their separately attributed assessments.
