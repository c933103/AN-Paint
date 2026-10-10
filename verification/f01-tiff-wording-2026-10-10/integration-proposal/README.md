# Read-only F01 stack proposal after the strict Korean failure

10 October 2026. This is the historical read-only plan. The later exact candidate and its additional test-only scope-guard composition repair are recorded in [the stacked evidence](../stacked-evidence/README.md). No source edit, PR retarget, ref update or additional CI action has occurred.

## Decision

Stack the bounded F01 patch on exact PR34 head `5703a61394791f18e9f2597272d908d9840599af`, tree `f2333d9ee7aa6e55c584b306e7363bde83dbbf43`, if the independent plan review authorizes it. PR34 remains draft and unmerged. Its existing routing correction is a dependency, not a new F01 implementation.

PR43's initial head `d3ada3e55fb60a6926e7f6c8eede242f3c1f140e`, tree `bde13ca4bbd9a45198ab4da9cadd85d900aaa594`, is based on develop80c and lacks that correction. Automatic run 38047199955 is terminal failure: 746 JVM tests, 744 passed and two comparison failures, zero errors/skips. Seven initial F01 dialog methods pass. Both 26-locale loops fail at ko-Kore-KR, expecting 貯藏/壓縮 but receiving 저장/압축; later loop entries are not runtime-proved by that failed invocation. The Hanja text and selected public tag assertion must remain strict. APK/source, Python, lint and API35 pass independently of that blocker.

This matches PR34's already reproduced persisted-selection defect and its private-resource-variant repair: [prior strict diagnosis](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6092984243), [exact PR34 acceptance](https://github.com/c933103/AN-Paint/pull/34#issuecomment-6094006470). No test-setup bypass is supported. The generic installed tests in PR43 do not test the new localized description.

## Exact mechanical scope

[Compatibility comparison](compatibility.json) re-reads all 37 current PR34 catalogues. Each still contains the exact original TIFF resource line exactly once; all four new test paths are absent. There are no clause/path conflicts.

All 37 complete resource-file blobs have changed since develop80c. Therefore copying PR43's whole XML files would overwrite unrelated PR34 text. Apply only each verified original-line to proposed-line replacement onto the pinned PR34 content. Preserve all other PR34 bytes and modes. Add the four exact accepted test blobs unchanged.

Expected source: 1,388 tracked files, exactly 37 modified resource paths and four added tests relative to PR34, 1,347 PR34 files unchanged, no deletions/mode changes. A new exact tree/manifest must be recomputed from actual bytes and independently reviewed before publication. No new combined tree identity or execution result is claimed here.

To retain source history and avoid a force push, a possible publication shape is an explicit integration commit with ordered parents current PR43 head and exact PR34 head, containing the reviewed union tree; PR43 is then based on PR34's branch so its visible incremental diff is the 37 + 4 F01 change. Base/head identity and operation ordering need fresh verification before publication. Retargeting alone is insufficient: the head itself would still lack the dependency, and the resulting merge/source identity would still need explicit verification. Do not merge either PR into develop or duplicate unrelated production changes into the F01 diff. If the dependency head moves, stop and re-evaluate the exact base/diff instead of silently tracking it.

## Generated resource effect

PR34's unchanged `AppLanguage.resourceLocale` maps public `ko-Kore-KR` to internal configured `ko-Kore-KR-anpaint`; persisted preference, platform application locale and Java default retain the public tag. Its Gradle Sync mirrors every XML file from canonical `values-b+ko+Kore+KR` into build-only `Paintroid/build/generated/exactScriptResources/values-b+ko+Kore+KR+anpaint`.

There is one additional derived compiled description value, copied from the already-counted mixed-Korean canonical entry. It is not a38th canonical translation or an offered locale. Do not commit generated XML or edit a duplicate source. The complete695-entry canonical/internal compiled equality must be checked, including the corrected TIFF string. Keep the existing clean/incremental/stale-output generation probes and routing policy byte-for-byte unchanged.

## Required combined validation

- Re-run structural/host checks on the actual combined tree. Expected host discovery is408 (PR34's400 plus eight F01 methods), but verify the real result; two optional Pillow skips may occur in CI.
- Re-run all nine new F01 Robolectric methods with fixed strings and real callbacks, retaining checked/unchecked/toggle/format-switch/cancel/Welsh-fallback coverage. Expected aggregate775 JVM tests (766 inherited + nine new), subject to actual discovery, with no errors/failures/skips.
- Preserve inherited routing and gallery oracles, the seven exact-script generation stages, full lint and APK/source/test-APK build.
- Use the existing full API30/API35 coverage and real Korean picker/rotation/public-identity checks. Preserve PR34's release-configured validation choice and unchanged deadlines; PR labels do not inherit automatically. Applying existing `ci:full-android` and `ci:release-android` to PR43 would need to be included in the reviewed publication operation, before the final source update, rather than introducing another workflow.
- Verify actual build-info/source/merge tree and all compiled generated values on the resulting head. Prior PR34 success and initial F01 partial passes do not establish combined acceptance.
- Preserve PR34's API35 timing risk: ordinary suite previously178.579s of180s. Do not increase the deadline, remove tests or infer stable headroom.
- Request the single final-head Codex review only after stable exact-head validation. No request has yet been made on PR43.

The original475/3/472 reset states, twelve probable/four uncertain F01 cases, seven no-edit qualified cases and 81 missing-key locales remain unchanged. No native-language, installed TIFF-dialog rendering or full-locale acceptance follows from this plan.
