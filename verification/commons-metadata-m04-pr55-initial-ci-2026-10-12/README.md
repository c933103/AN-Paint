# M04 / PR55 first hosted run: failed checkpoint

This evidence preserves [run 38239121942, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/38239121942), whose overall conclusion is **failure**. It does not establish merge readiness, full visual acceptance, or a release.

## Exact source

- PR55 head: `b95c9a682c77f5dfa9b9a1f4eacabd9d9a03265a`.
- Stacked PR52 base: `71f4d288669858e7975ec4c094b7f47a9a1ff145`.
- Tested synthetic merge: `14b1fdf8e02ebe6f765d63906f05c7e808524b76`.
- Reviewed and tested tree: `d80218496e45bbefcaa378d40e5cd9846b7988ee`.
- All 1,947 remote leaf paths, modes and Git blob identities matched before PR creation.

The [exact-head Codex code review](https://github.com/c933103/AN-Paint/pull/55#issuecomment-6122883036) reported no major issues. This does not supersede the actual failing test.

## Executed results

- Host contracts: 660/660 pass.
- Exact-script generation: seven successful clean/incremental/debug/release probes, matching source and log hashes.
- APK/source build and test-APK compilation: pass.
- Native dependency build and Android lint: pass.
- JVM: **890 exact identities, 889 pass, one fail**. No missing, extra, duplicate or skipped identities.
- API35 installed regression: **104 source-bound identities pass**, 74 native and 30 app. Raw protocol, JUnit XML, exact source digests, partitions and deadlines were checked. These are existing installed regression flows, not an installed M04-specific error test.
- APK binding: 1,944 included tracked blobs match the reviewed source; the exact three pre-existing archive omissions are `.gitignore`, `colorpicker/.gitignore`, and `.idea/codeStyles/Project.xml`. Sidecar and embedded source ZIP are identical. Extra native-source files remain confined to the four existing declared roots.
- All 14 font-directory assets match the reviewed source, including the three-glyph Nôm extension.
- Compiled M04 resources: exact default +59 scoped values +generated mixed-script Korean alias, 61 configurations. Manchu U+180E and Mongolian U+202F positions remain exact.

## Failure and capture limits

`CommonsMetadataQueryFailureFlowTest.shortLandscapeM04RetainsFullAccessibleTextAtNormalScale` failed at the unchanged line-width guard on line 398. Source loop order and the last emitted frame identify Ainu Kana, Copy credit, 640×320 dp, font scale 1.0 as the first failing profile. The failing frame and line metrics were not saved before the assertion, so actual text clipping versus line-metric or fixture behavior is **unresolved**.

There are **85/112** valid PNG/JSON capture pairs. All 85 match the exact expected metadata, dimensions and script controls; only seven images were directly inspected in the independent review. The other 27 are absent after the assertion. Full visual/shaping acceptance is not claimed.

A separate evidence-quality issue affects vertical screenshots: reading-start reset requests layout, but the original test draws before the requested relayout. Endpoint reachability checks do not establish that these images were captured at reading start. The diagnostic successor must save the failing geometry before the same guard, preserve its threshold, and record/reset scroll position explicitly. No language or production fix is inferred from this failed run.

## Preserved files

[initial-ci-evidence.zip](initial-ci-evidence.zip) contains 336 original or derived evidence files: all 85 capture pairs, all actual JVM JUnit XML, phase logs/timings, exact-script probes, source/build and compiled-resource audits, API35 protocol/XML/coverage receipts, and the independent audit scripts/report. [The manifest](initial-ci-evidence-manifest.json) lists every member's byte count and SHA256. [Archive receipt](initial-ci-evidence-receipt.json) pins the archive itself.

Archive SHA256: `30bb59e92d3f46e6f1f81e06ac783d6dbfdb1c1864960f00c7fd9cda288bb920`.

APK SHA256: `af371c6331f60877b30253273a1cf382cca009a3a1caa47fa17a076fbf6edcda`.
Source ZIP SHA256: `eb167ca58d3ed2b62ce3a937d0b2c19a11e8b5e7454d11cc4e19480567c6c11d`.

APK availability does not imply upgrade signing, release acceptance, physical-device/TalkBack or full language acceptance. PR52 integration and actual-base reconciliation/retesting remain required. The old partial53 and standalone59 checkpoints retain their original source/evidence boundaries.
