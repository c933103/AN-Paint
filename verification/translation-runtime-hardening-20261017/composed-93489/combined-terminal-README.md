# Exact-head terminal verification: PR114

Source `93489b4138e84f73356302a1e75a5cb377954e88`, tree
`2c61c517f00d800bd5cc0ff1bf8f783a9b687a56`.
Hosted merge `bcad0b45e6b9fbcd979f2a46f1e9863d2596aa38` has the identical tree.

[Run 39021174915](https://github.com/c933103/AN-Paint/actions/runs/39021174915)
completed successfully on 17 October 2026 at 09:50:38 UTC. **All six CI jobs passed.**
The exact-head [Codex code review](https://github.com/c933103/AN-Paint/pull/114#issuecomment-6232356589)
found no major issues. The security summary still refers to `db076197`; current-head
security is **not verified**, despite a request comment. PR114 remains blocked on
that review prerequisite. This receipt does not authorize a merge.

## Actual hosted results

- Full JVM suite: 114 suites and 1,127 cases; zero failures, errors or skips. Every
  current Kotlin test file with `@Test` has a matching suite. The full Gradle Test
  task executed normally; no test filters or exclusions were added.
- Native composed controls: six Mongolian suffix pixel cases on SDK30/35, four
  SDK33 caption-safety cases, three linear run cases, 25 resource-boundary cases,
 11 formatter cases and four prefix-search cases all passed. The exact suffix
  pixel oracle rejects the old marker and ordinary-space substitution. New native
  incremental measurement includes the cross-token suffix boundary.
- JVM preparation: 93.946s, 48 producer tasks, 11 direct dependencies, 1,005 input files,
  no scheduled Test. All relevant Kotlin/Java compilation and source generation
  were UP-TO-DATE in the actual full-test invocation. Actual JVM phase 344.867s;
  lint 79.702s; Python 128.894s; native preparation 39.230s. All phase exits were zero.
  The 6-minute preparation, 12-minute test and 22-minute job caps are unchanged.
- Android lint reported zero issues. All 11 clean/incremental/release-first source
  resource probes passed their expected classification, including the deliberately
  failed reserved-ID app/debug/English overlay. Hosted generated source XML matches
  the local AAPT sweep input exactly.
- API35 emulator reports contain 119 unique passing identities across 10 phases:
 74 library/native and 45 app methods. The existing composition checker was rerun
  against this exact source; source hashes, SDK-aware inventories, split groups and
  complete identities match. No missing, unexpected, failed, skipped or timed-out
  method was accepted. Both device jobs and the aggregate passed.
- All 60 Commons native-capture metadata receipts retain complete character layout.
  Selected Mongolian/Manchu portrait and 2× landscape scroll endpoints were visually
  inspected: the Latin-to-suffix separator has no diagnostic marker. These are
  single-viewport Robolectric NATIVE captures, not installed-device or TalkBack
  evidence, and do not certify every control or translation.

## APK and corresponding source

Artifact 12096637517 SHA256:
`ccc655bed457742bac0768266dc162e988f7890d2b8b9b2e3048cb8b094ed9fe`.
APK SHA256:
`8b11f32952219adcad48830678359d9def02f66db7a6ac0e8792ab9835249c45`.
Embedded and separately extracted source ZIP SHA256:
`0f0652f4213f4fb3f288665e64be53d25a5322fb07c67b7e135829ea0ff08754`.
All 1,188 included tracked files match source bytes and executable modes. The
archive omits only `.gitignore`, `colorpicker/.gitignore` and
`.idea/codeStyles/Project.xml`; no included code/resource discrepancy was found.
The APK verifies with CI-debug v1/v2 signing. It is not upgrade/release-signed.
Raw verifier warnings remain in the archive without being reclassified as findings.

## Preserved evidence and limits

`combined-terminal-evidence.zip` preserves actual JUnit XML, phase logs/profiles,
preparation graph, lint XML, source/resource receipts, API35 reports, selected
native captures and verification scripts. The manifest records all member hashes.
The large APK and original Actions artifacts are identified by hashes instead of
being duplicated into the application branch.

The earlier two JVM-step deadline failures remain failures. Initial local combined
runs' stale phase-sum assertion failures are preserved in the preceding evidence
commit; final normal/optimized aggregates both passed 867 tests. This successful
run is evidence for this head, not a promise that every future run fits its caps.

Runtime robustness, translation correctness and valid XML packaging remain distinct.
Finite memory, caller argument size, native/OS/font/layout behavior, API21–27 caption
cache comparison, real WebView and broader physical-device/TalkBack coverage retain
separate limits. No universal error-proof or linguistic acceptance claim is made.
