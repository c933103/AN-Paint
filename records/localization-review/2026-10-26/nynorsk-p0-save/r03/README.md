# Nynorsk save messages: exact-head validation in progress

Current PR [#173](https://github.com/c933103/AN-Paint/pull/173), head `2d940e411829f991b3399c1fdb572dd12b0ad44f`, tree `6bb4fa11534149df7f8f58cb3d21faf2b802089f`. This record is a source/artifact/host receipt, **not a terminal CI or merge receipt**.

The five-file change remains eight bounded reviewed Nynorsk resources plus regression fixtures/tests. All reviewed values and production code are unchanged by the follow-up test fix. The real configuration-change lifecycle now refreshes resources and rebuilds command captions before navigation. The first-head P2 finding and cancelled workflow are preserved in `historical-run-outcome.json`, not relabelled passed.

- Both full host aggregates passed independently: 1,357 ordinary and 1,357 optimized Python tests; focused tests passed 5 + 5. Exact commands/timings/log digests are in `host-validation.json`; raw local logs are not included in this concise record.
- [Current-head Codex code receipt](https://github.com/c933103/AN-Paint/pull/173#issuecomment-6408393821) found no major issues. A subsequent request is still active at this snapshot; no stale security lane is promoted to current-head acceptance.
- [CI run 40270220462](https://github.com/c933103/AN-Paint/actions/runs/40270220462) has passed build and exact-script jobs. JVM/lint and API35 results remain pending at this snapshot. No terminal pass or merge eligibility is claimed.
- Artifact `12628406797` has exact archive SHA-256 `7d6338579454b299933c20f6b0288114659ff2f8fd7b25d43c8c96642bdfd127`. APK `ef4bc8fe7332ac89df882f0864f29e26ecb922e64fb7be566307c87de86414cd`; corresponding source `8dfe592ffb83c0ec97916eb8d5730c43e919a27d5b273ad5e3f0381b14400610`.
- Build-info identifies test merge `eb570744c0c02bf3ef141a8757ed254fe2ae6946`, whose parents are base `d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4` and current PR head. Its tree equals the reviewed head tree. The embedded source ZIP equals the external ZIP byte-for-byte; all 1,361 packaged tracked files match current source bytes. Three normal packaging-excluded dotfiles are listed explicitly.
- All eight compiled `(nn)` display values match the independent final review exactly. This is compiled-resource evidence, not installed rendering, layout or native-language evidence.
- APK v1/v2 signature verification passed using the CI debug certificate. This is **not upgrade/release signing**. No release has occurred.

The source-bound language report remains pinned to d0e4a386. Its denominator is not silently changed by this pending PR. The 59 scoped / 112 fallback distinction and #56 never-merge, #159 freeze, #113 retarget/held-warning, Help callback/archive identity and release holds remain unchanged.
