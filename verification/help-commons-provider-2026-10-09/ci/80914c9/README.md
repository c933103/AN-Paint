# PR32 integrated-head CI receipt

Source head: `80914c9e86111ead4f24bf8463dbdeddd0e43646`.
Source tree: `69dcea7bf38e4a3491dc01005ab090108b69d524`.
CI synthetic merge: `f8ca8d865dcbd31f270610b4b80c2b10008a83ac`, whose tree was
independently fetched and matches the source tree exactly. Base is actual merged
develop `0b3d737e19448c47d36deee8cebfffd5d40c1ea3`.

[Run 37953314026](https://github.com/c933103/AN-Paint/actions/runs/37953314026),
attempt 1, completed successfully in all three jobs. The earlier source-only
run 37952662763 was cancelled by normal integration; no pass is claimed for it.

## Verified results

- 347 Python contracts passed; CI phase wall 62.566 seconds.
- 723 JVM/Robolectric executions in 75 suites: zero failures, errors, or skips.
- All seven new `CommonsHelpProviderTranslationTest` cases passed in 7.094 seconds.
  Those are API30/35 JVM/Robolectric configurations, not two installed-device runs.
- Android lint: zero issues. Universal APK, matching source, and test APK builds passed.
- API35 installed: 74 library + 18 ordinary app + 1 restart seed + 1 restart verify
  = 94 completed checks. The app coverage union independently reports all 20
  declared app methods completed, without omissions or overlap.
- Ordinary installed app suite: 157.661778394 seconds of the unchanged 180-second
  budget, leaving 22.338221606 seconds. This is installed regression coverage,
  not new Help-specific instrumentation coverage.
- JVM phase wall: 398.621 seconds of 720; lint/native wall: 244.957 seconds of 360.
  Complete regression job: 786 seconds of 1,200, leaving 414 seconds.
  Profile spans may overlap and are not exclusive CPU time. Per-phase ceilings
  do not guarantee all phases and upload fit inside the outer job deadline.

The integration independently preserved every one of the 68 C03 paths and 41
accepted develop-delta paths exactly; no overlap. All 1,253 remote leaves matched
that composition. The separate local combined Python pass was 347 tests in
51.660 seconds; its raw log and composition record are retained here.

## Evidence and hashes

`summary.json` includes exact job/artifact identities, JUnit counts and individual
Help-suite timing, installed invocation results, phase walls, profile rows, and
scope limits. `verified-ci-evidence.zip` contains all JUnit XML and test identities,
lint reports, phase/profile logs, installed invocation/restart records, complete
job logs and original artifact inventories. Large rendered preview files and
system logcat are inventoried, not duplicated.

Original downloaded archives were checked against GitHub's published SHA-256:

- Regression/lint artifact 11626819539, 30,538,257 bytes:
  `9155483d253fd78803a7926f5d5e10c8c8f8b3e4b6913574f07922b9ca6bd815`.
- API35 artifact 11628160470, 1,860,743 bytes:
  `435f0793a3b0d1e05330174938a54d2261155179c84d1d69853a4c75f9bb784d`.
- Preserved evidence ZIP, 286,363 bytes:
  `d7c025d8e9687752c7bf11f0c7445b9671c14424d255895406dc6860ebe4e097`.

APK/source artifact metadata and successful build identity/source-extraction logs
are retained. The 142 MB binary artifact was not separately downloaded or
independently unpacked during this evidence pass; its CI checks are distinguished
from the two independently downloaded/hash-verified report archives.

Current-head Code review [6084207332](https://github.com/c933103/AN-Paint/pull/32#issuecomment-6084207332)
completed with no major issues and no inline threads before the single normal
ready transition. Ready-triggered final Code/Security outputs are separate and
will be reported in the PR; this receipt does not pre-claim them.

This bounded C03 pass does not establish native-language fluency, acceptance of
all Help wording or languages, physical-device/TalkBack/general-layout coverage,
or a post-merge result. The root merge gate remains separate.
