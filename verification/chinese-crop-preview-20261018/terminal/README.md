# PR135 exact-head terminal verification

Reviewed head: `fc0e71c30a9bfd0422c134d426535c4d70b96059`.
Application tree: `3b84956dd6427f8a88d71e270922a4477e307bc0`.
PR checkout: `01c315499475fba6d1a983f62f4f1c7dc21c162c`, verified to have that identical tree.

[All six CI gates](https://github.com/c933103/AN-Paint/actions/runs/39124709635) passed on attempt 1. Both [Codex Code/Security reviews](https://github.com/c933103/AN-Paint/pull/135#issuecomment-6249552496) completed with no findings on the exact head and no unresolved review threads.

Actual downloaded artifacts were verified, rather than inferring runtime success from source or the job label:
- 1,135 JVM tests across 122 suites; zero failures, errors or skips. All three new `ChineseCropPreviewTest` methods match the source-declared identities and pass, including both actual regional toolbar consumers and complete accessible text.
- 946 hosted Python checks, matching both local ordinary/optimized runs.
- Complete source-bound API35 union: 74 native and 45 app methods, with matching checkout, run, SDK, APK/source hashes and no missing, unexpected, failed or duplicate identities.
- APK and separately supplied corresponding-source hashes match the build receipt; embedded source is byte-identical to the companion ZIP. All 1,212 packaged tracked blobs and executable modes match the reviewed source. Only the three documented metadata files are omitted from the source package.
- Nine clean/incremental exact-script resource probes pass with checked log digests.
- Unchanged evidence validators independently accept 12 dialog cases, 104 vertical data files, reachability inventory and 32 screenshots. This validates transport/inventory and source binding, not independent pixel or Chinese installed-device appearance review.

`verification-packet.zip` retains raw JUnit XML, app/native JSON/XML receipts, exact-script logs, run/jobs/review/artifact metadata, the verification script and a hash manifest. Additional compact receipts and the three affected JVM suite XML files are adjacent.

No CI failures, retries, source repairs, weakened assertions or deadline extensions were needed. A supplementary local reachability-validator invocation initially supplied the extraction root rather than its `reachability/` child. Its rejected inventory diagnostic is preserved; rerunning against the correct existing directory passes without changing data or tests. The earlier local Gradle network block is retained in [initial evidence](../initial/README.md), not counted as an Android pass.

PR135 was merged as `614f28f9f8edd489e5d13cffbe481d3b49c99d7f`. Natural [postmerge run39126110768](https://github.com/c933103/AN-Paint/actions/runs/39126110768) is pending separately. This is a bounded TW/CN preview-warning correction, not a release, whole-language, native-speaker, installed Chinese glyph/layout, enlarged-font, TalkBack or physical-device acceptance. CN Help and eight Sinitic-variety follow-ups remain in tracker75.
