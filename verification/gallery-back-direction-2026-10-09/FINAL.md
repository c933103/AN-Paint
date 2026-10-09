# Final gallery Back-direction evidence

PR [#33](https://github.com/c933103/AN-Paint/pull/33) merged on 2026-10-09 at 17:23:51 UTC.
This evidence-only branch preserves final PR and post-merge results without changing
the tested source head or develop.

## Identity and completed checks

- Source head: `39a4b15979cfad722f163aa0c3a64f7f153b3d10`
- Accepted Help base: `43148951ac6bd23687e66685855909ac538ba004`
- PR tested synthetic merge: `aac5e630e6c5ab3613f9d964af3a4d7602fa5038`
- Actual merge: `b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61`
- Identical source/tested/merged tree: `eea34eac70c8e425648fd6e1370af9643c710bf3`

Both [final PR run 37962749051](https://github.com/c933103/AN-Paint/actions/runs/37962749051)
and [post-merge run 37965972897](https://github.com/c933103/AN-Paint/actions/runs/37965972897)
completed successfully. Each built the APK/source/test APKs and passed:
- 729 JVM tests, zero failures/errors/skips, including all six gallery configurations;
- all 140 offered tags on both API 30 and 35, with the independent ten-tag RTL oracle;
- zero Android lint issues;
- all 94 existing installed API 35 cases (74 Paintroid + 18 app + 1 restart seed + 1 restart verify),
  with no missing/unexpected cases, errors or timeouts.

The app installed suite took 172.359312402 seconds in the final PR run and
166.637817034 seconds post-merge. The 180-second deadline is unchanged.
All 352 final local Python tests passed in 50.770 seconds. Local Gradle did not run
because the wrapper network download was unavailable; JVM/build/lint/device results
above are hosted CI results.

## Files and verification

[Final PR artifacts](final-ci-39a4b15/artifact-manifest.json) and
[post-merge artifacts](merged-ci-b9a7961/artifact-manifest.json) record original ZIP
byte counts and SHA-256 digests. Both regression ZIPs and both installed ZIPs were
materialized through the artifact tool's supported Sediment references, their bytes
verified against GitHub digests, and their ZIP paths checked before extraction.

Each directory retains the original gallery JUnit XML, both complete locale JSONs,
lint XML and four selected host PNGs. Derived inventories preserve every JVM test
case and all four complete installed test summaries. The complete ZIP archives,
APK/source archive bytes and raw job logs are not republished here. Build success
is a CI job result; this record does not claim an independent download/hash check
of the large APK/source or test-APK archives.

Final and post-merge locale JSONs and all four selected PNGs are byte-identical.
The PNGs also match the physically inspected second-run captures:
Arabic points right; English points left; Classical Chinese's vertical-column
layout keeps its Back glyph horizontal and left-facing. The individual hashes are
in each manifest.

These are actual production Activity/views under Robolectric NATIVE, using
offline ShadowWebView history. Tests assert the translated accessibility name,
full >=48dp arrow, effective app/device-default direction, both history/home
branches and restored state under explicit save/destroy/create. These host tests
do not independently establish real OS-triggered locale recreation, installed
Chromium RTL-arrow behavior, TalkBack acceptance or language-fluency acceptance.
The 94 installed cases are the existing regression set, not a new installed
RTL-arrow test.

## Review and history

[Review provenance](final-reviews.json) records the exact source head. Requested
code review reported no major issues. The single successful draft-ready transition
then triggered configured Code and Security reviews, completed at 17:21:12 and
17:21:22 UTC, followed by the Codex bot's PR +1 at 17:21:28 UTC. No inline threads
or review submissions reported findings. No clean label is asserted.

The [first failed run](first-ci-072bb73/README.md) and
[second failed run](second-ci-f226b4d/README.md) remain preserved. The first had
two expected-left/observed-right failures with the synthetic configuration helper.
The second passed all six production-view configurations but disproved an auxiliary
Resources-identity assertion. Only that invalid auxiliary control was removed;
every direction/accessibility/history assertion was retained. The precise original
synthetic-helper mechanism is not claimed as proven.

Artifact retrieval is resolved. The separate first-run raw-log Git blob cancellation
remains paused; that file is absent and has not been re-encoded, split or repackaged.
This patch has no new translation text, provider traffic, workflow/deadline changes,
font-barrier changes or held archive changes. Broader localization acceptance remains
outside this narrow completed Back-direction correction.

