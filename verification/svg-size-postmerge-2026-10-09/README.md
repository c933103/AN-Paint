# PR29 and contained PR19: combined develop verification

## Result

PR29 merged as **8a75b825131f0b24c55a40a3636e9e70792037a8** at 2026-10-09 11:55:55 UTC. Its tree **293708639d4bc3382c4f3de8cf35cc0164257b91** exactly equals the reviewed combined head d601dba. The normal merge preserves develop 2fc36a8 and the earlier #28 work.

[Automatic develop run 37926785579](https://github.com/c933103/AN-Paint/actions/runs/37926785579), attempt 1, completed successfully:
- Host: 326 tests, zero failures/errors, two optional Pillow skips.
- JVM: 690 tests in 70 downloaded JUnit suites, zero failures/errors/skips.
- Lint: downloaded app/build/reports/lint-results-debug.xml has zero issue elements.
- Universal APK/source and both instrumentation APKs built successfully.
- Installed API35: 93 tests, comprising 74 codec + 17 editor/gallery + 1 restart seed + 1 restart verification; all four downloaded JUnit suites have zero failures/errors/skips.
- The 17-test app group reported 156.810 seconds; runner XML wall time 158.301 seconds, both under its unchanged 180-second deadline.

See [summary.json](summary.json) for exact job/artifact IDs, hashes, counts and boundaries. Both regression and emulator ZIPs were downloaded through their returned file references, hash-verified, safely extracted, and the actual XMLs inspected. Artifact metadata alone was not treated as test verification.

## Composition and review scope

The d601dba integration tree contains 1,178 leaves: an exact disjoint union of afbb801's 144 changed paths and develop's 21 changed paths relative to their common base. An independent Git-object comparison found no overlapping paths, unexpected content/mode changes or new integration logic. The imported 21 paths are tests/evidence and an androidTest-only WebKit dependency, with no production-source delta.

[Exact combined-head Code Review](https://github.com/c933103/AN-Paint/pull/29#issuecomment-6080139531) found no major issues, and [combined premerge CI](https://github.com/c933103/AN-Paint/actions/runs/37924730965) passed. Separately recorded Security reviews accepted the unchanged component trees. The [PR29 summary](https://github.com/c933103/AN-Paint/pull/29#issuecomment-6077859772) labels Security at afbb801, not d601dba: no Security-labelled verdict for the combined or merge commit is claimed. The merge decision explicitly used current Code+CI and verified composition with that boundary.

## Translation/display acceptance

The two SVG original-size reasons have 118 source-assisted proposed values across 59 scoped catalogues, plus 2 default resources. The other 81 offered catalogues remain explicitly incomplete with normal fallback. Structural coverage is not native-language or all-language acceptance.

Current SVG suites pass 4 parser, 6 displayed error-path and 8 readability executions. All 64 PNG + 64 JSON captures from this develop run are byte-identical to the inspected d601dba/afbb801 captures. The matrix is native-rendered Robolectric host evidence on API 30/35 at 320×640 dp, scales 1/2 and eight locales. Actual requested/system/application/wrapper/Activity scale preconditions are retained. All 48 horizontal status cases pass full-message/ancestor-clipping checks; 16 vertical samples remain diagnostic-only.

[Separate AN-W04 records](https://github.com/c933103/AN-Paint/pull/20#issuecomment-6080380193) preserve the missing Mongolian/Manchu vertical status and shared gallery control clipping findings, with exact paths and reproduction. This receipt is not whole-gallery, vertical-layout, screen-reader, physical-device or fluent-language acceptance.

## Superseded PR19 run

This successful develop run provides fresh combined-tree coverage for contained PR19, including its installed gallery fixtures and lint. [The earlier PR19 postmerge record](https://github.com/c933103/AN-Paint/tree/461408c726825b3ec7d7df5cc9a06054644b21f0/verification/gallery-routing-postmerge-2026-10-09) remains intact: regression attempt 1 reached the unchanged lint deadline, attempt 2 failed Maven POM resolution with HTTP403, and attempt 3 was superseded/cancelled by existing develop concurrency when PR29 merged. None is relabelled as passed. This receipt does not claim a newly analysed gallery lifecycle/proxy trace.

## Archival boundary

The original afbb801 final-gallery ZIP upload remains held after an interrupted tool with unknown approval association. No retry, re-encoding, splitting or constituent-image upload was used. **Long-term repository archival of those final captures remains incomplete.** The current regression artifact 11614394505, SHA256 aabb9a7bc39364e2ef5e6f5d750323f3e0aced8730d50085dde2c01e9e89d1a4, currently provides actual PNG/JSON/JUnit evidence through Actions; it expires 2026-10-23 according to metadata.

This independent concise provenance record contains only text summaries. It does not replace or claim successful publication of the held archive.
