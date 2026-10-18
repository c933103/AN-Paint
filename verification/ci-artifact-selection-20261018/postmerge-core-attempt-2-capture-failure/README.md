# Postmerge attempt 2: successful instrumentation, failed capture transport

Integrated develop source `8700ca4d921875bdc9f3cf824290cfb83cda2037` (tree `9c7d9123a134ab75e8bc5f2d090e283f4ac0f218`, including #123/#133/#135/#136). [Run 39131791712](https://github.com/c933103/AN-Paint/actions/runs/39131791712), attempt 2, is terminal **failure**. [Core job 117692571501](https://github.com/c933103/AN-Paint/actions/runs/39131791712/job/117692571501) executed from 2026-10-18 13:50:40 through 14:03:24 UTC. Aggregate job `117695484424` failed at 14:03:29 because core did not pass; this is not a stale-artifact selection failure.

## What passed, and what failed

An independent replay of the exact-source inventory verifier confirms all 74 native/import methods and all 38 selected core app methods passed with no missing, unexpected, failed, skipped or timed-out method. The core app phases were 17 ordinary, 3 gallery draft, 12 installed dialog, 2 English/Manchu vertical, 2 Literary Chinese/emoji vertical, and one each restart seed/verify. The original source digest and all phase deadlines match. These are method-execution results only, not acceptance of the job or the complete composed evidence.

At 14:03:18.649 UTC cleanup began after instrumentation result 0. Both required `adb pull` operations then reported `adb: error: failed to get feature set: device offline`: installed-dialog evidence at 14:03:18.844, vertical-locale screenshots at 14:03:18.853. The uploaded artifact contains no dialog or vertical capture files. `logcat.txt` also ends mid-stream. The source performs both pulls before its `adb emu kill`; the latter was logged at 14:03:18.856. The available evidence establishes an ADB capture-transport failure, but does not establish the underlying disconnect cause or a premature-cleanup code defect. Required capture and composer gates correctly remain failed.

## Original artifact and source binding

Artifact `12138599799`, named `emulator-core-api-35-8700ca4d921875bdc9f3cf824290cfb83cda2037`, was created/updated at 14:03:22 UTC. Its original 184,796-byte ZIP has 42 files and SHA-256 `26a6c5b5efa6ca79bf2db55f10118a8d1b931ccec532a2cf6b9545f451fc9f96`, independently verified after download.

The original device identity binds run/attempt `39131791712/2`, SDK 35, debug variant and source `8700ca4d` to:
- app APK SHA-256: `0f0f4cb1c1ef989646ba0808391dee64f2cce812e6548b5f024e025035821aa2`
- corresponding source ZIP: `6152543a5caee9d64ddd6b435c5fed47c8030b9f2655808d43f76cc0008afc65`
- test APK: `180fa5fbc0858512f662ca153ad79c76daa5f250f7dca23be0d76858fb0e81dc`
- app test source: `3022fe07657c952e64e63bfc0fcc3da622cf2c337827df9f601be7cb22c826f4`

## Actual retry scope

The API created new attempt-2 job IDs for successful prerequisites, but preserved their original execution intervals. Build `117692572088` retains 13:29:53–13:35:36; exact-script `117692572481` retains 13:29:53–13:32:10; position `117692572597` retains 13:35:38–13:40:41; regression/lint `117692595754` retains 13:29:54–13:48:23. The corresponding artifacts retain their attempt-1 creation times. Only core and its dependent aggregate have fresh execution intervals. Job IDs or the copied `run_attempt` field alone therefore do not demonstrate fresh execution.

The successful position artifact remains `12138940115`, created 13:40:39, SHA-256 `0a61a56df21555f349e540385b3d0e1fec13a43ca3fd641de1a111bc8e89392e`. The failed attempt-1 core artifact `12138303007`, created 13:36:09, SHA-256 `8d538b15952eae98701accaa03807ffca0beca61a82143013c10071afed86c7b`, also remains available. Its SDK download/setup failure and zero executed core methods stay separately recorded in the prior additive evidence commit.

## Preservation and next observation

`failure-packet.zip` is 272,955 bytes, SHA-256 `cff35fe07fe35214857db1294804236de73f14575e9e47a2ad712bbc02be3d66`. It contains the original artifact ZIP, complete core job log, terminal attempt-2 run record, all-attempt job metadata, all artifact metadata, independently checked source inventory, extracted failure logs/identity and a per-member SHA-256 manifest. Every member was verified against that manifest. No earlier evidence or source is replaced.

After preserving these raw records and confirming unchanged develop source, one targeted retry of core job `117692571501` was accepted at 14:12 UTC. Its results are pending and cannot supersede this failure. All capture requirements, assertions, deadlines and the full composer remain unchanged. If the same device-offline failure recurs, investigate runner/capture lifecycle rather than repeatedly retrying. This record makes no release, whole-language, or additional device-specific appearance claim.
