# PR42 post-merge verification

Verified 10 October 2026, after merge at 15:24:12 UTC.

## Accepted source and merge

- [PR42](https://github.com/c933103/AN-Paint/pull/42) was merged as [`165a6a503529736527c689e3ac1b5432253d19ee`](https://github.com/c933103/AN-Paint/commit/165a6a503529736527c689e3ac1b5432253d19ee).
- Parents are unchanged base `80c14372b0504bc44f9f2809ad477247fdc8100b` and reviewed head `f89fb76e6721e14f3e0b714116795530088812a6`.
- Actual merge tree `5d7ce333311c452cd7587fd871cdf45d6b6a72ca` exactly matches both the accepted head and successful pre-merge synthetic checkout `424cf44986195bab369b75c472d4ee1168c59e9c`.
- Fresh pre-merge readback found all three head checks successful, no inline review threads and no changes-requested review. [Codex's clean review](https://github.com/c933103/AN-Paint/pull/42#issuecomment-6099030308) explicitly identifies `f89fb76e67`.
- The only production change is the fewer-than-two-proven-frames title expression. Two regression-test files were added. Resources, bodies, actions, scanners and decoders are unchanged.

## Actual post-merge CI

[Push run 38063463830](https://github.com/c933103/AN-Paint/actions/runs/38063463830), attempt 1, completed successfully on actual merge `165a6a503529736527c689e3ac1b5432253d19ee`. All three jobs passed. See [terminal CI identities](terminal-ci.json).

- Build APK and corresponding source: success.
- Regression and lint: 746 unique JVM methods across 78 XML suites, zero failures/errors/skips; 9 new title methods and 5 existing import-flow methods all passed. Android lint XML contains zero issues. Python ran 371 tests: 369 passed and 2 optional Pillow skips. See [test verification](test-verification.json), focused XML and [Python phase log](python.log).
- Installed API35 emulator: 94 unique methods passed, split 74 native/import + 18 editor + one restart seed + one restart verify. For every phase, the raw instrumentation start/pass identities equal both the XML identities and summary identities; each phase reports SDK35, return code 0, no timeout, missing or unexpected test. All four AnimationImportTest pixel/metadata methods passed. See [device verification](device-verification.json) and [selected raw evidence](selected-emulator/).

## Artifact and source verification

All four downloaded ZIP archive SHA-256 values were verified against GitHub artifact metadata:

- APK/source `11674220650`: `69258b90267d26ca201e0ac5380072a2473d963b54c3b460dc6b3aacaf289650`.
- Instrumentation APKs `11674645432`: `f0a852edfbe29fe9cabcea4f072e2ac44bc687d4fe6b0323f830b8e10e6bb386`.
- Regression/lint `11674521510`: `4680a014a80580d225244f25ec2e554d5851a42ef24345479f30a6e2850cafbe`.
- API35 `11674426059`: `2b4ec470c42a88d916a74068d7ef921407c4444feebac60a6321fac4f647c765`.

Build-info identifies the actual merge and run. APK SHA-256 is `f1d56aa4bb1a1e4942aa6c37c3c0863b2da5ad47de89f0f09c707afb51178731`; corresponding-source SHA-256 is `d3df44d630f083e590f2d9b5f0f6fd22cfe84d629ddca263ec6966821fc51cdf`. Both were recalculated. The APK-embedded source archive is byte-identical to the delivered source archive. Every one of its 1,289 bundled tracked files matches its reviewed Git blob. Three non-runtime tracked files are omitted by source packaging: `.gitignore`, `.idea/codeStyles/Project.xml`, and `colorpicker/.gitignore`. No bundled tracked file differs, and the exact new title expression is present. See [build verification](build-verification.json).

The CI artifacts expire on 24 October 2026; these selected text reports, test XML and raw test protocols are archived durably in the repository. The APK is a debug build signed with a CI debug key. No release or upgrade signing is claimed.

## Limits retained

Title assertions are API33 Robolectric simulation. The installed API35 animation checks verify decoder behavior, not dialog title layout, accessibility or language suitability. No installed-title screenshot, physical-device run, API30 run, broader locale acceptance or native-speaker certification was added. A01's wider runtime/localization acceptance and P07-007 remain open as applicable. The parent register remains 475 total / 3 structural completed / 472 pending. F01 remains separate and unimplemented.

A fresh run listing for the merge contains only Android build and checks; no release-publication run exists for this merge. The release request file was unchanged and the publication workflow was not dispatched. Final readback still finds develop at `165a6a503529736527c689e3ac1b5432253d19ee`.
