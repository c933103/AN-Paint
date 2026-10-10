# Failed PR41 API35 run 38031416670: original timeout and pixel evidence

[Run, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/38031416670) ·
[Exact-source failure and independent pixel review](https://github.com/c933103/AN-Paint/pull/41#issuecomment-6094873111) ·
[PR41](https://github.com/c933103/AN-Paint/pull/41) · [parent PR18](https://github.com/c933103/AN-Paint/pull/18) ·
[project board PR39](https://github.com/c933103/AN-Paint/pull/39)

## Exact original bytes and source binding

`api35-original.zip` is the unchanged complete artifact 11662561776: 4,289,911 bytes,
SHA-256 `c804b59b9d9eb75ca6b24af696d2ae09cdf9ffa0c81582f75ffc30fd18c2397c`.
All 106 original entries remain intact, including all 72 PNGs, six reachability
receipts, their native-event traces, installed outcomes and full emulator/logcat.
`original-entry-manifest.json` hashes every original entry; `png-manifest.json`
also records all image dimensions. The two directly browsable examples are exact
copies of entries, not crops, edits or newly rendered images.

Executed head: `f22ff7a206b6e871e54fec4b0e02ae32f7cc4700`.
Test merge: `b9d9375f8c9e494f83478cd88090c30a6065bfa0`.
Both trees: `d21df4db395b12aeac71600d73394323fa040d51`.
These identities and the artifact digest were independently checked against GitHub.

`supporting-reports-selected.zip` is a newly assembled selection, not the original
regression ZIP: it preserves the bytes of the emulator job log, all 78 JVM XML
reports, lint XML and 12 phase log/timestamp/timing files. Its 92 entries have
individual hashes in `supporting-entry-manifest.json`. The original regression
artifact 11663260512 is separately identified in `failure-receipt.json`.

## This run remains failed

- Of 98 declared installed source methods, 97 completed and one was interrupted.
  The other phases passed 74 native, 18 ordinary, one seed and one verify method.
- The vertical phase completed three of four declared methods, then exceeded
  its tested 180-second ceiling: 180.635590254 seconds, timed_out=true, return -9.
- Literary Chinese began initial portrait navigation but produced no retained
  image or reachability receipt. Its portrait and landscape cases are missing.
- Six completed input/model cases cover English, Manchu and vertical emoji in
  both orientations. Their receipts record 21 successful native endpoint drags,
  stable parent offsets, no CANCEL, zero trace errors/drops and observer cleanup,
  plus the draft/document/Cancel/Choose-location checks.
- Those successful input/model assertions do not establish rendered acceptance.
  Independent review of all 72 images found stale quality labels and filename
  previews. The artifact's 24 original-state images and 48 reachability images
  are retained as failure evidence, not an accepted full matrix.

In particular, English portrait endpoints show quality 76 while recorded progress
reaches 1 and 100. Manchu portrait labels retain 95; emoji portrait labels retain
77. Completed landscape maximum images retain 1 while the thumb and recorded
value reach 100. Filename previews can retain Untitled.png beside fields showing
Untitled.jpg. The two original English examples here independently corroborate
these visible mismatches. Rendering cause and later fixes are outside this record.

Compilation passed. The exact-run JVM reports contain 749 cases with no failures,
errors or skips, including 12 slider cases across API30/API35; lint has zero issues.
CI Python ran 397 tests with no failures and two optional Pillow-related skips.
These separate successes do not override the installed timeout or stale pixels.

## Preservation and verification scope

Full original content and selected reports were inspected before publication;
the resulting bounded classification is recorded in `content-inspection.json`.
Generic diagnostic words are not treated as credentials or private-data findings.
No archive entry is silently removed or changed.

This addition is confined to the existing evidence branch. All earlier archives,
failures and screenshot identities remain preserved. It changes no production
source, PR41 ref, workflow or CI trigger. Later source or budget changes cannot
retroactively turn this run green.

Local archive/entry SHA-256 and Git blob identities are verified. The connector
has a UTF-8-only binary readback limitation, so matching remote blob/tree identities
are reported without claiming independently decoded remote archive bytes.
