# PR32 real-develop postmerge receipt

Actual merged develop commit: `43148951ac6bd23687e66685855909ac538ba004`.
Tree: `ab5ff7fe6d04d5e22348b979c9e0054eef9b1c0f`, independently fetched and exactly
identical to the accepted PR head `29cbe495b79231df6c1c5e93928fb9821cb6b9e6`.
Merge parents: accepted develop `0b3d737e` and PR head `29cbe495`.

Automatic push [run 37959160542](https://github.com/c933103/AN-Paint/actions/runs/37959160542),
attempt 1, completed successfully in all three jobs. This tests the actual merged
commit, not a PR synthetic merge and not a manually dispatched extra workflow.

## Independently verified reports

- 348 Python contracts pass; phase wall 65.655 seconds.
- 723 JVM/Robolectric executions, 75 suites, zero failures/errors/skips.
- All seven Help cases pass in 7.325 seconds, including the complete Japanese
  sentence and real Help/picker routes under the documented JVM configurations.
- Lint: zero issues. Universal APK, matching source and test APK builds succeed.
- API35 installed: 74 library + 18 ordinary app + 1 restart seed + 1 restart verify
  = 94 completed checks. App coverage union: 20 declared and 20 completed methods.
- Ordinary installed app suite: 153.137017621 seconds / 180, margin 26.862982379.
- JVM phase wall: 418.252 seconds / 720. Lint/native: 301.486 seconds / 360.
  Complete regression job: 875 seconds / 1,200, margin 325 seconds.

The installed results are regression coverage, not new Help-specific installed
checks. API30/35 Help checks are JVM/Robolectric configurations, not two installed
runs. Phase/profile spans are not exclusive CPU time; per-phase maxima do not
promise all phases and uploads fit inside the outer deadline. All existing
assertions, commands and deadlines were retained.

## Preservation

Both original report archives were downloaded and checked against GitHub SHA-256:

- Regression/lint artifact 11630099361, 30,537,570 bytes:
  `5bfb62c03b807176dda602d51f0d1172019e57d92f79abb27b56efded518b864`.
- API35 artifact 11630993794, 1,954,928 bytes:
  `17278d332b568e6765e1b746575e8968328d064cdf482449ec95678f23d74df3`.
- Preserved ZIP, 285,331 bytes:
  `0a511a66cfc3d8ee6983b997b1ead120984a1a9ab87a64ebe9a4707e9b0ab3d5`.

The ZIP contains all JUnit XML/test identities, lint, phase/profile logs, installed
invocation/restart records, full job logs and original artifact inventories.
Rendered previews and system logcat are inventoried, not duplicated. APK/source
artifact metadata and successful CI identity/extraction logs are retained; its
142 MB binary ZIP was not independently downloaded or unpacked in this pass.

The premerge review receipt in `../29cbe49/` retains the corrected Japanese finding,
independent all-60 boundary recheck, resolved thread, clean current Code result,
and exact actual Security boundary. Security completed on `80914c9`; the later
one-byte Japanese/test/evidence delta was reviewed without claiming an unrun
current-head Security review. Earlier source-only cancellation and the original
`80914c9` green CI preceding that finding remain preserved as history.

This closes AN-W05-C03's bounded one-key implementation, review and postmerge
verification. It does not establish native-language fluency, all-language or
whole-Help acceptance, general-layout, TalkBack or physical-device coverage.
