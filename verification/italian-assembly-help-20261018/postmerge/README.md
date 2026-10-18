# Italian assembly Help: post-merge verification complete

Merged PR: https://github.com/c933103/AN-Paint/pull/131
Merge: `3a88bfea931c5fad9b4d8d3d71da34a2a0609376`
Reviewed head: `13cdaf6f8cbf8a764c36aba6bd227f455cbaef8d`
Shared tree: `38f4130f0452db1fab1477d0362cee0304d2fced`
Natural develop run: https://github.com/c933103/AN-Paint/actions/runs/39094504880

All six gates are successful after the bounded retry: regression/lint, APK/corresponding source, exact-script resources, core API35, position API35 and the complete combined API35 gate. Attempt 1 failed after instrumentation passed because the final ADB vertical screenshot pull stopped mid-transfer. Only failed core/combined jobs were retried. No source repair, weakened assertion or deadline change was made. The merge tree is identical to the exact PR head with clean Codex Code/Security reviews and passing pre-merge gates.

## Actual post-merge artifacts

- All 1,126 JVM tests pass across 120 suites, with zero failures/errors/skips. All six source-declared complete Help/crop/toolbar methods pass, including Italian Exact position, German/Spanish counterparts and the real complete Help dialog. Every JUnit XML is retained; the affected suite is also available separately.
- The complete source-bound API35 union contains all 74 native and 45 app methods with no missing, unexpected, failed or timed-out method. Core and position share build/source/test identity: core uses attempt 2, position reuses its successful attempt 1 through the unchanged exact-identity validator. The source-bound app inventory was independently revalidated.
- Actual exported capture transport/inventory passes the unchanged validators: 12 dialog cases, 104 vertical data files and 32 matrix screenshots. This is transport/inventory checking, not independent visual acceptance or Italian-specific installed behavior.
- GitHub artifact hashes match. APK/source hashes match build-info, and the APK embeds exactly the companion source ZIP. All 1,206 packaged tracked files match reviewed blobs/modes. Three omitted metadata files are explicit: `.gitignore`, `.idea/codeStyles/Project.xml`, and `colorpicker/.gitignore`. The APK uses a CI debug key; private upgrade signing is a separate step.
- All nine exact-script generation probes pass on the merge commit/shared tree; their recorded log hashes were independently checked.

`checks.json` contains compact run/job/artifact identity, source binding, counts and affected method durations. The packet retains terminal snapshots, all JVM/device XML/JSON, source/test/transport receipts, verification scripts and exact-script logs. Bulk APKs and screenshots remain in the linked Actions artifacts.

[The failed first attempt and diagnosis](https://github.com/c933103/AN-Paint/blob/9aa1d27c4702858a35111199e66d4768279e591c/verification/italian-assembly-help-20261018/postmerge-attempt1/receipt.json) remain preserved. The ADB exit cause was not established, so it is not labelled a source defect or timeout.

[Pre-merge complete-entry and runtime evidence](https://github.com/c933103/AN-Paint/blob/c602c893b7eaa2ca9f7478a85b17b94a8191cdc0/verification/italian-assembly-help-20261018/terminal/README.md) remains reachable and unchanged. Evidence is additive on a separate source-preserving ref, outside the application branch.

## Scope limits

The bounded complete Italian Help correction and real Help/toolbar/crop regressions are verified. This does not certify the entire Italian catalogue, native-speaker acceptance, installed Italian glyph/layout, enlarged-font, TalkBack or physical-device behavior. Locale routing is unchanged. PR75’s broader obligations remain open; PR56 and existing holds remain untouched.
