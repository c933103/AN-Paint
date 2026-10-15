# PR88 gallery native-component diagnostic candidate

## Finding and bounded change

The intentional draft tracker [PR88](https://github.com/c933103/AN-Paint/pull/88)
still describes an unfixed, conditional diagnostic mismatch. Current develop
`b765b8b2396d9b4c05f7272fa982d115ce18469a` routes the gallery's broad
`LinkageError` catch to a colour-converter-specific resource. JXL dimensions
validation can initialize `anpaint_jxl` without starting that converter. The
tracker/master comments and open PR inventory showed no competing implementation
or hold on a bounded fix. No live provider or native incident is asserted.

This candidate changes the broad gallery catch to the new generic reason:

> A required image component is unavailable. The image was not imported.

`PlatformImageColour.convert` and all 60 existing `colour_converter_unavailable`
values remain unchanged for actual converter-specific failures. The new key is
added to the default and existing 59 scoped catalogues and classified P2; 112
other selectable locales retain explicit English fallback. No review counters,
provider policies, redirect handling, native packages, permissions, editor
mutation rules or failure cleanup behavior are changed.

The only other production change is a narrow `JxlCodec.readNativeInfo` seam,
defaulting to the existing native call and used only by dimensions inspection.
`sourceBitDepth`, decode and encode remain unchanged. The seam permits controlled
failure at the actual JXL native-info boundary after production byte sniffing and
`ImportedImage` construction; it does not replace the gallery validator.

## Behavior tests and source review

Seven new Robolectric methods declare API30 and API35 coverage (14 invocations
when executed). They test the real WebView selection/download/status/result path
using fixture HTTP connections and the narrow native-info seam:

- Actual JXL bytes under a misleading `.png` source name, initial
  `UnsatisfiedLinkError`, repeated `NoClassDefFoundError`, full visible/accessibility
  message and unchanged document, credits and clipboard.
- Valid PNG under a misleading `.jxl` name retries successfully through editor
  insertion without invoking the failing JXL seam.
- Successful JXL-info stub validates and hands back the exact downloaded bytes.
  This proves the metadata route only, not actual native decode.
- Finish and destruction during pending native info suppress late status/result
  delivery and clean temporary files. Gates always release in `finally` and do
  not manufacture the failure through a timeout.
- Unsupported URL selection is rejected before transport/native info.
- Genuine profiled JPEG passes gallery validation, then the actual editor decode
  path reports the precise converter failure without document/credit mutation.
- Every one of 171 offered locale choices resolves the complete new message or
  its explicit default-English fallback.

The JPEG failure follows the existing Robolectric convention of absent Android
converter JNI; it is not a mocked failure at the wrong gallery stage. Existing
`NativeCodecTest` and `PlatformColourImportTest` retain actual native success
controls and are byte-for-byte preserved. Their current runtime results are not
claimed here.

Independent source review found a locale-state teardown gap. It was corrected by
preserving raw preference absence/values and complete platform locales before any
migration-prone lookup, then re-reviewed. Final test SHA256:
`55aed7bdbf307a4fb4f8036a568282a1e88db32029e9feb2d58623d0bb562e4b`.
No blocking source finding remains. This is source review, not Kotlin execution.

## Translation review

All 60 complete new statements have initial candidates and separate source-context
reviews. Six corrections received a further cross-review: Cebuano, Turkish,
Vietnamese, Hokkien Han/Latin and Nôm. The outcome corrections avoid suggesting
that the failed import is merely pending. Final confidence is 31 high, 21 medium
and 8 low. The low-confidence values are Ainu Kana/Latin, Dzongkha, romanized
Hakka, traditional Mongolian, Manchu, Okinawan and Nôm. Their exact idiom,
terminology, attestation or script limitations are retained in the per-value
receipts; these are provisional model-reviewed translations, not native-speaker
or whole-language certification. Nôm uses existing catalogue glyphs covered by
its bundled font; Wu adds no supplementary glyphs.

`final-language-coverage.json` is the authoritative full-value evidence. Initial
candidate files are historical inputs where a later correction exists. Both
clauses of every statement were reviewed; no old converter value was rewritten.

## Packet and integration constraints

- `publication-files.json`: 67 complete UTF-8 files with blob SHA256/Git SHA/mode.
- `implementation.patch`: 63 modified files plus four new files; no removals.
- `changed-files.json`: exhaustive source manifest and expected Git tree.
- `resource-delta.json`: the 60 additive message values and unchanged anchors.
- `reconcile-resource-delta.py`: guarded, key-only temporary integration helper.
- `patch-verification.json`: exact full-tree reconstruction and whitespace checks.
- `integration-rehearsal.json`: isolated PR103 resource-delta preservation proof.
- `test-source-review.txt`, `final-language-coverage.json`, `test-results.json`:
  source/language evidence and exact executed-versus-unrun test status.

Baseline commit: `b765b8b2396d9b4c05f7272fa982d115ce18469a`.
Baseline tree: `690cad93cea0968cbe6b280e9f51c3977af54c4d`.
Expected candidate tree: `4311d103479b85f9c4ab84e185a04e33972d4048`.
All 1,142 baseline blobs/modes were verified; the full Git tree reconstructs the
verified develop tree. The patch reconstructs all 1,146 candidate files/modes,
with all 1,079 unaffected original blobs preserved. No synthetic local commit
is required for publication.

PR102's resource values and synchronization fix remain intact. An isolated
rehearsal applied PR103's local candidate redirect-value delta, then the PR88
helper; all 60 redirect values and every other resource byte remained exact.
The helper is idempotent. The PR103 workspace/branch was never written. This
rehearsal is not a merged-source or combined-runtime acceptance claim.

If develop advances, materialize and verify the fresh tree and use the helper;
do not overwrite newer resource files with stale full-file payloads. Re-run the
applicable checks on the integrated source. Keep bulky logs and receipts on the
project's evidence ref, outside the application tree. Preserve PR88 as its
separate intentional draft tracker. No publication, tracker mutation, workflow
trigger, review request or release action was performed by this task.

## Validation limits

The exact command/result list is in `test-results.json`. All 56 focused resource/catalogue/font/importance checks passed. The complete
host suite passed 730 tests normally and 730 tests with Python optimization,
sequentially, without failures, errors or skips. All 60 old converter-specific
values are rejected by the new resource negative controls. These checks do not
exercise Kotlin/JVM/Android behavior.

The local runtime has Java21, no installed Gradle8.13 and no configured Android SDK/toolchain.
A focused wrapper attempt failed during Gradle bootstrap with
`java.net.SocketException: Network is unreachable`, before compilation. Kotlin,
Robolectric, Android lint, generated resources, native/APK builds and installed
API30/API35 tests are therefore **unrun locally**. Native failure handling and
rendering remain pending exact-source CI. Source checks and human-readable
reviews must never be substituted for that runtime evidence.
