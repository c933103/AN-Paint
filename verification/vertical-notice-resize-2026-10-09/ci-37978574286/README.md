# PR35 post-merge verification passed

[Post-merge workflow 37978574286](https://github.com/c933103/AN-Paint/actions/runs/37978574286)
completed successfully at 2026-10-09T19:27:53Z on develop merge
7e8a0d2377693a35cd9392f2082ef88548a6f67f (attempt 1, push event).
All three unchanged jobs passed. The merge tree
7d4245411d699a3cf59018ce8c6d4cb87940dc60 exactly equals the accepted source
768959d1aa580ed88beb26abf99db597cf998f5d and premerge tested tree.
The merge parents are b9a79613b088c9ff54f2c225f6ae53d5b8d8ae61 and that source head.

This is a separate execution and preservation cohort from
[premerge run 37974245255](https://github.com/c933103/AN-Paint/tree/59c0d154f4ae422d361b22c271dc2918ba8240cd/verification/vertical-notice-resize-2026-10-09/ci-37974245255).
The original source README/local checks remain the historical pre-CI record.
Neither this package nor the premerge package replaces PR26's historical evidence.

## Actual results

- All 77 original JVM XML files were parsed: 737 unique cases, zero failures,
  errors or skips. All eight new API30/35 compiled-resource NATIVE cases passed,
  taking 3.125 seconds in this run. Lint contains zero issues.
- All 94 existing installed API35 cases passed (74 + 18 + 1 + 1), with exact
  expected identities and no missing/unexpected cases, process errors or timeout.
  The ordinary app partition took 150.814 seconds within the unchanged 180-second
  limit. These existing tests do not add installed coverage for the new notices.
- All eight new JSON reports identify this merge and run, with completed=true.
  Each API has ten route rows, 80 transition rows and 15 vertical pixel rows;
  the event logs have ten rows on API30 and eight on API35.
- Each API reproduces all five unsupported-ZWJ clips: 309/309/336/372/336 lost
  ink pixels for mn-Mong/mnc-Mong/lzh-Hant/en-XV/qaa-Zsye-XV. All ten ordinary
  emoji/joined-word controls per API remain contained. Actual-parent/reference
  equality, nonempty ink and clear reference guards remain required.
- The 124px horizontal shrink again requires 101px where 92px is available for
  Mongolian/Manchu, with 437/518 lost ink pixels in both fitted and edge-to-edge
  hosts. Every geometry sequence preserves the logical node/text and original
  8001ms expiry check, with zero toast replay.
- The observer's explicit-announcement and real-text-mutation positive controls
  pass with exact source/event payloads. API30 again records one text-content-
  change request per locale after same-text assignment; API35 records none.
  Geometry-only phases record none in these bounded cohorts.

Those are host accessibility requests, not TalkBack speech or installed-service
delivery. These checks do not establish exactly-once speech, universal resize
silence, physical-device acceptance or native-language correctness. Existing
production vertical profiles still use system toasts. No production vertical
route or post-exposure resize/dismissal/fallback policy is selected or changed.

## Image and artifact preservation

All 100 expected PNGs independently decoded as nonempty RGBA. Every PNG's bytes
also match its independently preserved premerge counterpart. Eight selected new
originals were viewed again: API30 en-XV and API35 Literary Chinese unsupported-
ZWJ parent/reference pairs, plus API30 Mongolian fitted and API35 Manchu edge-to-
edge horizontal-shrink pairs. The visible edge/bottom clipping agrees with the
pixel evidence. No derived preview image is included.

Both original Actions ZIPs were downloaded, CRC-checked and SHA-256 matched:

- [Regression/lint artifact 11641121530](https://github.com/c933103/AN-Paint/actions/runs/37978574286/artifacts/11641121530),
  32269727 bytes: cf5cbd6a6f0c25963540695008283dd9ed7aa4f6cf1cc71bfed50b07d3cf197f
- [Existing API35 artifact 11640646738](https://github.com/c933103/AN-Paint/actions/runs/37978574286/artifacts/11640646738),
  1925447 bytes: 85dd7f63a6dfe2436080c6993df503f6d3fff70c558658cf0e2a590fa8335602

The larger APK/source and instrumentation archives were produced but were not
independently downloaded in this verification.

characterization-evidence.zip is a newly named scoped preservation archive,
not either complete Actions ZIP. Its 115 entries preserve the original eight
JSON reports, 100 PNGs, new-case JUnit XML, lint XML and four installed summaries,
plus a newly derived full JVM name/class/time inventory. artifact-manifest.json
records exact sizes, hashes and original/derived provenance for every entry.
The archive SHA-256 is
52613ddeee7c201b10ff7ad66af16cacfc80d872390ff6e9d996b739ea1bf7e5.

Run `python3 verify_evidence.py` from this directory. It pins this cohort,
checks the exact archive and test/report matrices, validates event controls and
pixel arithmetic, and decodes every PNG with chunk CRC and report-matched ink
counts. It passes normally and under Python -O. This validates saved evidence;
it neither reruns Android nor independently authenticates GitHub provenance.
final-run-receipt.json records the separately checked GitHub run/jobs, merge
identity, artifact provenance and [completed exact-source Code/Security reviews](https://github.com/c933103/AN-Paint/pull/35#issuecomment-6086973627).

The [source-backed policy questions](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/verification/vertical-notice-resize-2026-10-09/README.md#decisions-deliberately-still-open)
remain open. In particular, horizontal fallback is not guaranteed to fit,
unnecessary same-text rebinding can generate another host request, and installed
real-IME/resize plus observed TalkBack checks remain necessary before accepting
a production announcement policy.
