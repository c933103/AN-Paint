# PR42 independent exact-source CI/artifact review

## Result

**The earlier Kotlin/Robolectric execution blocker is cleared by successful CI. No actionable code defect or failed required CI check was found.** All nine new title-test methods and all five existing import-flow methods compiled and passed on the accepted source. The run also passed the broader JVM/lint/build and installed API35 regression suites.

This supports the bounded engineering correction, not actual-device title visual acceptance, physical-device verification, native-language acceptance, API30 execution, upgrade signing or closure of the broader localization/reset obligations.

- PR: https://github.com/c933103/AN-Paint/pull/42
- Completed successful run, attempt 1: https://github.com/c933103/AN-Paint/actions/runs/38041522544
- All three jobs completed successfully: regression/lint `114182563633`, build `114182563739`, API35 emulator `114184010778`.

## Exact source identity

- Base commit: `80c14372b0504bc44f9f2809ad477247fdc8100b`
- PR head: `f89fb76e6721e14f3e0b714116795530088812a6`
- GitHub synthetic merge checkout: `424cf44986195bab369b75c472d4ee1168c59e9c`
- Both commits' remote Git tree: `5d7ce333311c452cd7587fd871cdf45d6b6a72ca`, identical to the independently reconstructed frozen candidate.
- The synthetic merge has precisely the base/head above as parents. The run identifies the specified PR head; its workflow uses the standard pull-request merge checkout. Artifact names and build-info therefore use the merge SHA, not the head SHA.

Independent raw Git API reads, terminal job/artifact metadata and the verified local frozen candidate establish this chain. See `pr42-source-chain.json` and `pr42-terminal-ci.json`.

## Artifact integrity and build result

All four downloaded archive sizes and SHA-256 values independently match GitHub's artifact metadata. The author owned downloads; the reviewer inspected those materialized bytes without repeating the download. The successful instrumentation download was the `-retry.zip` file. A reported earlier truncated copy was not used.

- Build/source artifact `11666282138`: `9733835a0337959d17b18f05f0efab8ad5cdca7a047575a38ec3bbb0adb63033`, 143,638,005 bytes.
- Instrumentation artifact `11666052471`: `43a42315a8de515e63b39541ba264062e0af9a4f9044b602b5b245b3743509dd`, 96,547,866 bytes.
- Regression/lint artifact `11666497670`: `152bbe07adce86aa504053ca817fc7c65d6654fa82d884c03ba040e3bbdf02f6`, 32,272,025 bytes.
- API35 reports artifact `11665559033`: `c85d8355a151da692b0d8aa8d04a0ff9a9b2375b814361e2700f8be8cb63a0c2`, 1,855,511 bytes.

The APK SHA-256 is `32dcf9ad6d5488032eadf1322ce19ac96e7178d93efbffdca9ae0b7ac1830a03`. Its embedded source ZIP is byte-identical to the separately supplied source ZIP, SHA-256 `d3df44d630f083e590f2d9b5f0f6fd22cfe84d629ddca263ec6966821fc51cdf`. Both match build-info for run 38041522544 and merge 424cf449.

All 1,289 bundled tracked files match the candidate's Git blobs, including all three changed/added files. Three non-runtime tracked files are absent: `.gitignore`, `colorpicker/.gitignore`, `.idea/codeStyles/Project.xml`. No bundled tracked file differs. The archive additionally contains 6,258 files in the existing four vendored native-source directories; this review did not independently audit every external native source file. The APK contains the expected four ABI payloads. Build and instrumentation-APK compilation succeeded. This is the CI debug-key build, not an upgrade-signed release.

Build detail: `pr42-build-verification.json`; instrumentation APK hashes: `pr42-instrumentation-verification.json`.

## Independently verified test evidence

### JVM / Robolectric

- `compileDebugUnitTestKotlin` and `testDebugUnitTest` appear in the successful JVM phase log.
- 78 JUnit XML suites contain **746 unique test cases, 0 failures, 0 errors, 0 skipped**. Per-suite declared counts equal XML testcase counts; there are no duplicate identities.
- `ImportSelectionTitleTest`: **9/9 passed**, 9.305 seconds.
- `ImportSelectionFlowTest`: **5/5 passed**, 0.261 seconds.
- Both focused classes' exact method sets match the accepted source inventory. No method is omitted or substituted.
- The nine new tests execute the production scanner, ImportSelection and dialog decisions under **API33 Robolectric native-graphics simulation**. This includes unknown zero/one-frame titles, confirmed exact/lower-bound counts, APNG poster distinction, English/pt-BR wording, Welsh fallback, still bypass, ownership and cancellation/disposal.

### Other host checks and lint

- Python reports **371 total: 369 passed, 2 skipped**. The two skipped test identities were reconstructed from the exact source's 371-case discovery order and the nonverbose progress record: optional Pillow ICO export decoding and Adam7 fixture pixel decoding. No skip is claimed as a pass.
- Android lint XML has **zero issues**.

### Installed API35 emulator

The raw instrumentation protocols were independently re-parsed and compared with the accepted source's declared API35 method inventories. JUnit XML, summary JSON and raw protocols agree. All 94 methods are unique, passed, and cover the complete eligible inventory with no missing, unexpected, failed, skipped or timed-out cases:

- Native/import: **74**
- Ordinary editor: **18**
- Restart seed: **1**
- Restart verification: **1**

The 18+1+1 editor partition is an exact disjoint union of all 20 source-declared API35 editor methods. All four `AnimationImportTest` methods passed: GIF/WebP first-frame pixels, APNG animation-as-default pixels, and APNG separate-poster pixels. The startup log records main APK installation and successful instrumentation completion.

**These four installed animation tests invoke metadata inspection and pixel decoding; they do not display the ImportSelection warning dialog.** No screenshot/image artifact exists in the API35 report. Consequently, the changed title's visual/layout/accessible rendering on an actual installed device has not been established. Title and locale fallback assertions are current-source Robolectric evidence, not installed-device visual evidence.

Detailed checked counts/inventories and limits are in `pr42-test-verification.json`; exact focused XML and raw phase logs are retained beside it. Reproducers: `check_pr42_build.py`, `check_pr42_tests.py`.

## Disposition

Retain the original no-actionable-source-defect review and replace only its historical compilation/Robolectric blocker with the successful exact-source CI evidence above. No source change is requested by this independent review. Broader semantic/localization reset states and F01 remain outside this bounded conclusion. No reviewer source edits, publication, CI dispatch, retry or new Work task occurred.

## Remaining external review gate

At the final independent metadata check, PR42 is still draft and unmerged, with unchanged head f89fb76e and base 80c14372. The Codex bot's [09:46:48Z response](https://github.com/c933103/AN-Paint/pull/42#issuecomment-6096261882) explicitly reports a code-review usage limit. It is not a substantive review or clearance. This independent model review and successful CI do not substitute for any separately required clean Codex review.
