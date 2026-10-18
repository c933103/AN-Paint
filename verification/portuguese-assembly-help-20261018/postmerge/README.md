# Portuguese assembly Help: post-merge verification

Merged PR: https://github.com/c933103/AN-Paint/pull/132
Merge: `702f0d8afa5bd5c950ec22ae14f29aecf4140482`
Reviewed head: `cadee014aacdc2d3422d533f76e626f3d4433dd9`
Shared tree: `c0474eab8fccd272b90fb181d3989862044be7f0`
Natural develop run: https://github.com/c933103/AN-Paint/actions/runs/39098747893

All six gates passed on attempt 1: regression/lint, APK/corresponding source, exact-script resources, core API35, position API35 and the complete combined API35 gate. The merge tree is identical to the exact PR head with clean Codex Code/Security reviews and passing pre-merge gates. No production source repair, weakened assertion or deadline change was made.

## Actual post-merge artifacts

- All 1,127 JVM tests pass across 120 suites, with zero failures/errors/skips. All seven source-declared complete Help/crop/toolbar methods pass, including Portuguese Exact position, German/Spanish/Italian counterparts and the real complete Help dialog. Every JUnit XML is retained; the affected suite is also available separately.
- The complete source-bound API35 union contains all 74 native and 45 app methods with no missing, unexpected, failed or timed-out method. Core and position share exact build/source/test identity; their actual attempt numbers are retained in the device receipt. The source-bound app inventory was independently revalidated.
- Exported capture transport/inventory passes the unchanged validators: 12 dialog cases, 104 vertical data files and 32 matrix screenshots. This is transport/inventory checking, not independent visual acceptance or Portuguese-specific installed behavior.
- GitHub artifact hashes match. APK/source hashes match build-info, and the APK embeds exactly the companion source ZIP. All 1,206 packaged tracked files match reviewed blobs/modes. Three omitted metadata files are explicit: `.gitignore`, `.idea/codeStyles/Project.xml`, and `colorpicker/.gitignore`. The APK uses a CI debug key; private upgrade signing is a separate step.
- All nine exact-script generation probes pass on the merge commit/shared tree; their recorded log hashes were independently checked.

`checks.json` contains compact run/job/artifact identity, source binding, counts and affected method durations. The packet retains terminal snapshots, all JVM/device XML/JSON, source/test/transport receipts, verification scripts and exact-script logs. Bulk APKs and screenshots remain in the linked Actions artifacts.

[Pre-merge complete-entry and runtime evidence](https://github.com/c933103/AN-Paint/blob/861d24cd900af622a7d7c1406672d09d4cd24f2a/verification/portuguese-assembly-help-20261018/terminal/README.md) remains reachable and unchanged. Evidence is additive on a separate source-preserving ref, outside the application branch.

## Scope limits

The bounded complete pt-PT Help correction and real Help/toolbar/crop regressions are verified. This does not certify the entire Portuguese catalogue, native-speaker acceptance, installed Portuguese glyph/layout, enlarged-font, TalkBack or physical-device behavior. Production model and locale routing are unchanged. PR75’s broader obligations remain open; pt-BR, PR56 and existing holds remain untouched.
