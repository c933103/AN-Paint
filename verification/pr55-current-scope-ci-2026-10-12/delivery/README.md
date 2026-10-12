# PR55 documentation-only successor: bounded fresh delivery audit

Result: PASS for this read-only source/artifact/probe/compiled-delivery audit. No new defect found within its scope. This is not overall CI, installed/device, translation, rendering or upgrade-signing acceptance.

## Exact identity

- Public head: `4a35933ff6b6d0013dac8743cc5eeac1c1033e05`
- Exact tree: `b6bf7626c1d7c4aef669394970046ffc89a5c877`
- Accepted parent: `e19c766eb3eaedc1b3cd3657bb92864f81a9498a`
- Base: `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- CI merge: `0c01e5fca04da3713c3595acbf45b60ad3538d30`
- [Hosted run 38303992927](https://github.com/c933103/AN-Paint/actions/runs/38303992927)
- [APK/source artifact 11771394989](https://github.com/c933103/AN-Paint/actions/runs/38303992927/artifacts/11771394989), 139,702,184 bytes; SHA-256 `568abefebae47325172364417e23243c562648a7103ef569541aa54ffb8ae9d8`
- [Probe artifact 11772090212](https://github.com/c933103/AN-Paint/actions/runs/38303992927/artifacts/11772090212), 6,179 bytes; SHA-256 `1b260b054209b9727549cb20f8a3653c97d28b591f49609ea09d3c3750d49382`
- APK SHA-256: `74c983ebbabc55c65a9d99aeba25b2ec0424b38b932e36f9e404ef68593dae34`
- Matching-source ZIP SHA-256: `27319149dda267593130b30eeacf20b89a1a0b05d7233295018dbeab169885dd`

The parent-supplied `source-publication.json` is a state snapshot with SHA-256 `8866bbb78c44ce97f0b7ad81e7f14852a719072914c29d9f85fd92e19873acdc`; its pending/in-progress job values are not a final CI result. Remote identity/authenticity comes from that verified receipt. This audit independently verifies retained bytes and their exact bindings; it does not independently query GitHub.

## Findings

1. All 1,094 local tracked files match the exact current tree's bytes and executable modes. Only `AGENTS.md`, `README.md` and `TRANSLATING.md` differ from accepted e19. The other 1,091 tracked leaves, including runtime, tests, resources, fonts, workflows and toolchain inputs, are byte/mode-identical.
2. Every artifact-extracted member exactly matches its ZIP. The fresh APK's embedded source ZIP exactly equals the delivered source ZIP. All 1,091 included tracked-source files match current tree content and modes; the same three declared packaging omissions remain. The four native-source root content/mode manifests are identical to accepted e19 (6,258 native extra files). Thus the bundled tracked-source changes are exactly the three Markdown files; no ZIP timestamp/compression equality is claimed.
3. All seven retained real-toolchain generation probes bind to this merge/tree/run: clean debug+release, unchanged/up-to-date, changed input/stale-output, restored input/release, second clean and release-first. Commands, task order, generated hashes, log hashes and extracted bytes pass. This checks receipts; it does not rerun Gradle.
4. The complete retained build log (272,805 bytes, SHA-256 `6833d6bd99505e3a91ba42b93e0da38b60f0be1e2e061b81916afe4b5928cce7`) binds checkout, producer/resource/compile/package steps, embedded-source extraction and upload to the exact artifact. Only compact ordered markers are retained here; partial logs are excluded.
5. Actual compiled application `android:localeConfig` has framework attribute ID `0x0101065b`, reference type `0x01` and target `0x7f100000`. The target is independently resolved from this APK's resource table to the packaged `res/xml/app_locales.xml`. Binary XML and aapt2 agree. The XML contains the exact ordered 167 locale entries and matches the picker; 22 alias pairs are preserved.
6. The full aapt2 resource dump, binary manifest and packaged platform XML match accepted e19. All scoped picker, M04 (61 compiled configurations), Arabic, application-attribute, font and licence evidence is byte-identical. All 14 font assets and 21 legal assets match exact source; Nom's embedded naming and MIT/OFL paragraphs remain intact. Ten pre-existing individual `licence_file` metadata references remain unresolved, unchanged; aggregate notices are present. This is no new removal or legal conclusion.
7. The current scope remains 59 scoped catalogues and 108 outside-scope English fallbacks across 167 options. The 27 accepted added catalogues remain empty and untranslated. No linguistic re-review was performed or implied.

## Immutable baseline and evidence

The accepted e19 audit remains unchanged at [immutable evidence commit f066e90b8fc](https://github.com/c933103/AN-Paint/tree/f066e90b8fc7682023e0bf260da55959e6ebf9e5/verification/pr55-platform-locale-ci-2026-10-12/delivery). All 67 local predecessor files matched the parent-verified transport manifest by size and SHA-256. `prior-review-freeze-manifest.json` freezes those exact inputs; `receipts/accepted-e19-baseline.json` gives direct immutable links and hashes for used evidence. The earlier audit was compared, not rerun or overwritten.

Start with `source-preflight.json`, `artifact-bindings-result.json`, `delivery-result.json`, `probes-result.json`, `build-log-result.json`, `compiled-picker-result.json` and `docs-delivery-context-result.json`. `DELIVERY-FILES.json` binds the delivered compact packet. Raw APKs, source ZIPs, full logs, full source inventories and tool binaries remain external CI inputs and are not copied into this packet.

## Portable reproduction

Run `bash run_audit.sh SOURCE_REPO CI_ARTIFACT_ROOT EXECUTABLE_AAPT2 PRIOR_REVIEW NEW_OUTPUT_DIRECTORY`.

Requirements:

- Python 3, Git and the pinned Android Build Tools 35.0.0 aapt2, SHA-256 `d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de`.
- A clean-by-content source directory matching the current exact tree, with Git objects for that tree and accepted e19 tree `dc1ba97dacc573ead73729297eb739ecb244dcf5`. Its local preparation HEAD need not equal public HEAD; both are labelled in the receipt.
- CI root containing `apk-and-source.zip`, `exact-script.zip`, their exact complete extraction directories, both `*.metadata.json` records and `build-job.log` with the pinned bytes.
- The exact 67-file accepted e19 `delivery/` directory from the immutable baseline above.
- A new output directory. Inputs are read-only; temporary checker perturbations are confined to disposable output storage.

The artifact-extracted aapt2 had mode 0644, so it was not executable. The audit used the already executable, previously retained aapt2 with the identical pinned digest instead; no predecessor or app file was changed. This was an ordinary executable-bit limitation, not an authorization denial.

The portable runner was executed successfully into a second fresh directory. All deterministic result and scoped evidence bytes matched (`portable-result-equality.json`). The checker-only suites passed in normal Python and `-O`: 16 probe checks, 15 compiled-parser checks and 33 actual-platform-binding checks, 64 per mode. These are audit-checker controls, not app, device or full regression tests.

## Boundaries

No app edits, GitHub writes, fresh Android/Gradle/full suite, installed app execution, new linguistic acceptance, raw evidence repackaging or user-computer task occurred. No ABI, alignment, signing-certificate or upgrade-key acceptance is asserted here. The CI debug-key artifact still needs any separately authorized private packaging step before an upgrade-signed delivery. Await the parent's final run/job assessment for overall CI status; this packet does not infer it from artifact availability.
