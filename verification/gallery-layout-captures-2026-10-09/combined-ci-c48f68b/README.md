# Combined integration: host pass, installed font-transition failure

Source head `c48f68b95360f87e21ccd4c59b995f25ee5d2462`, tree
`c85b44e3b97cd146644776573d02b654c0102cd9`, was tested by
[run 37946657315](https://github.com/c933103/AN-Paint/actions/runs/37946657315).
Tested merge `48850ca5d20eb50bcbdb0553434eec196d5c4fef` has the identical tree.

## Integration proof

The actual merged develop `55a6158a9b651871d0d204e52fb34c0f8a20d2a0` is the
second parent of this merge. Relative to common base `8a75b825`, PR30 changed
38 paths and PR31 changed 94 paths, with **zero overlap**. Every resulting one
of 1,242 remote tree leaves matches the independent local Git union. The
original PR30 diff against updated develop remains exactly those 38 paths.
`integration-proof.json` retains every affected path/mode/blob identity.
Accepted translations and the Python 2m/JVM 12m/lint 6m phases are preserved
byte-for-byte, with the unchanged 20m outer job and failure propagation.

## Verified results and explicit failure

- APK/source and instrumentation compilation passed.
- **716 JVM tests passed**, zero failures/errors/skips; **lint zero issues**.
  The ten added tests are PR31 regressions; no previous JVM case was removed.
- Python: **336 local tests passed** without skips in 52.451s. CI ran 336 in
  47.360s with two optional independent Pillow decoder tests skipped because
  Pillow is unavailable there. Both execute locally; exact IDs are retained.
- CI phase wall times: Python47.519s, JVM285.055s, lint178.439s, exit0 each.
- All 1,680 catalogue layout cases and 72 Activity scenarios pass; all 504
  action/window/vertical files are byte-identical to the reviewed 03abccd run.
- Installed API35: **74 library +17 ordinary tests passed; one ordinary test
  failed**. Ordinary instrumentation156.006s; the runner did not time out.
- The French gallery reached both real portrait/landscape viewports at system
  2x. Full browser reserves, wrapped queries and actual Search EditorInfo passed.
- Before the Mongolian gallery launched, the requested system font transition
  1x to2x never reached2x: persisted setting, system Resources and target Resources
  remained1x at the ten-second assertion deadline. This is a failed setup
  transition; it does not establish a production layout defect or harmless
  flakiness. The exact setting writer/cause is under investigation.
- **Both restart tests were never run** after this failure. This combined run is
  not an acceptance pass and does not authorize merge.

The failing transition follows ATMS's logged1x change at15:00:16.849; the fixture
observed all three values1x at16.917 and requested2x at16.918. No later ATMS2x
change appears, and all three values still equal1x at15:00:27.005. The original
shell output was discarded by the existing fixture, so these records cannot
alone distinguish a rejected/lost shell write from later framework write-back.

Both ZIP SHA256s were checked before safe extraction. The manifest preserves
all 1,009 constituent hashes, and all808 executed JVM/installed case identities
and failure details are retained. Raw downloaded ZIPs remain the original local
artifacts; GitHub Actions retains the full originals until2026-10-23. This
receipt is not a claim of permanent archival of every ZIP byte. No held PR29
archive constituent is republished.

[Combined-head Codex Code review](https://github.com/c933103/AN-Paint/pull/30#issuecomment-6083317924)
found no major issues. The Security summary remains explicitly at9bbfad5; no
distinct combined-head Security result is claimed. All three previous P2 threads
are resolved; this new CI failure is open. No physical-device, TalkBack,
every-keyboard or fluent-language acceptance is claimed.
