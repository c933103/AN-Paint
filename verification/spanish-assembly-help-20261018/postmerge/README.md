# es-ES assembly Help: post-merge verification complete

Merged PR: https://github.com/c933103/AN-Paint/pull/130
Merge: `7ee75e4a1400587a775db420c1e1bebdbe88fa1d`
Reviewed PR head: `94869be423441fc943ff0b2eeb8dfe76036c83bb`
Shared tree: `e3ba7b23a38230f7820d148d5e99eaf364f7c20c`
Natural develop run: https://github.com/c933103/AN-Paint/actions/runs/39090888009

## Terminal result

All six gates passed on the first attempt: regression/lint, APK/corresponding source, exact-script resources, core API35, position API35 and the complete composed API35 gate. No source repair, test relaxation, deadline change or rerun was needed. The merge tree is byte/mode identical to the exact PR head that received clean Codex Code/Security reviews and passing pre-merge gates.

## Actual artifacts checked

- The downloaded post-merge regression artifact contains 1,125 passing JVM tests, zero failures/errors/skips, across 120 suites. All five complete Help/crop consumer methods pass, including Spanish toolbar/Exact position/conditional Unplace (0.217 seconds). Every JUnit XML is retained in this packet.
- The composed API35 artifact contains all 74 native and 45 app methods, with no missing, unexpected, failed or timed-out method. The complete source-bound app inventory was independently revalidated against the unchanged repository checks. Core and position both use attempt 1 and match the same build/source/test identity.
- Actual exported capture packages pass the unchanged transport/inventory validators: 12 dialog cases, 104 vertical data files and 32 matrix screenshots. This verifies transport/inventory, not independent visual acceptance or Spanish-specific installed behavior.
- Artifact SHA-256 values match GitHub. APK/source payload hashes match build-info; the APK embeds exactly the companion source ZIP. All 1,206 packaged tracked files match reviewed Git blobs and executable modes. The source pack omits `.gitignore`, `colorpicker/.gitignore` and `.idea/codeStyles/Project.xml`, as recorded explicitly. The APK uses a CI debug key; upgrade signing is a separate private step.
- All nine clean/incremental exact-script generation probes passed on the merge commit and shared tree.

`checks.json` records run/job/artifact IDs, hashes, results and method durations. The compact packet retains terminal snapshots, all JVM/device JUnit XML, complete device identity/coverage/capture receipts, source bindings and independently rerun transport receipts. Bulk APKs and screenshots remain in the referenced Actions artifacts.

The [pre-merge full-entry and runtime evidence](https://github.com/c933103/AN-Paint/blob/26de4d3cfd62820e885123d99f23061871ecf627/verification/spanish-assembly-help-20261018/terminal/README.md) remains reachable and unchanged. Evidence is additive on a separate source-preserving ref, outside the application branch.

## Scope limits

The bounded complete es-ES Help correction and real Help/toolbar/crop assertions are verified. This does not certify a whole Spanish catalogue, native-speaker acceptance, installed Spanish glyph/layout, enlarged-font, TalkBack or physical-device behavior. Generic-es/es419 routing was not changed. PR75's broader obligations remain open; PR56 and existing holds remain untouched.
