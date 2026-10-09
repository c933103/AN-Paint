# PR35 exact-head characterization passed

[Workflow 37974245255](https://github.com/c933103/AN-Paint/actions/runs/37974245255)
passed all three jobs for source head 768959d1aa580ed88beb26abf99db597cf998f5d,
tested as merge fee98d54e2c27ba4d90bcf16ad37b7566930809b. Both point to the same
tree, 7d4245411d699a3cf59018ce8c6d4cb87940dc60.

The earlier README/local-checks.json remain the truthful pre-CI record.
This separately named cohort records the actual first hosted results:
737 JVM cases, zero failures/errors/skips, including all eight new API30/35
characterization cases (2.818 seconds total); lint zero; builds successful; and
94 existing installed API35 cases (74 + 18 + 1 + 1). The ordinary app invocation
took 164.987 seconds within its unchanged 180-second budget. The new cases are
host NATIVE characterization, not new installed-device coverage.

## Actual new findings

- Both APIs retain all five production vertical profiles on system toasts with
  the exact compiled logical resource messages.
- All 30 vertical pixel rows have exact actual-parent/reference equality and
  clear nonempty reference guards. The ten unsupported-ZWJ rows clip; all 20
  ordinary/joined-word rows are contained. Each API's clipped counts are
  309/309/336/372/336 for mn-Mong/mnc-Mong/lzh-Hant/en-XV/qaa-Zsye-XV.
- Both APIs independently reproduce a complete horizontal no-fit case in the
  **new app-theme 124px shrink**: Mongolian/Manchu require 101px but have 92px.
  Actual lost ink is 437/518 pixels respectively, in both fitted and
  edge-to-edge scenes. The historical isolated 180px-window measurement remains
  separate. This directly constrains any proposed horizontal fallback.
- All 160 transition rows retain the same logical node/text through the seven
  geometry phases, then expire at the original 8001ms check with zero toast
  replay. Host injection is not a real IME animation.
- The four event-observer cohorts pass their exact-source explicit-announcement
  and real-text-mutation controls. **API30 emits a text-content-change request
  when the same text is assigned again; API35 emits none in this fixture.**
  Geometry-only phases produce no recorded requests in either API. The explicit
  TYPE_ANNOUNCEMENT events occur only in the marked test-positive-control phase.
  Avoiding unnecessary logical-text rebinding is supported by this observation.

An observed host accessibility request is not a TalkBack utterance or service
delivery. These traces do not prove exactly-once speech, universal platform
silence during resize, or installed-device behavior. No production vertical
route, dismissal/fallback policy or merge is introduced.

## Preserved evidence

characterization-evidence.zip is a **new scoped preservation archive**, not the
original complete Actions ZIP. It contains:

- All eight original new JSON reports
- All 100 original native PNGs, with exact filename matrix verified and every
  file decoded as nonempty RGBA
- Original eight-case JUnit XML, zero-issue lint XML and four installed summaries
- A newly derived full 737-case JUnit inventory with names/classes/times

The archive has 115 entries. artifact-manifest.json records each entry's size,
SHA-256 and whether its bytes are original or derived. summary.json retains
counts, scope, timings and artifact identities.

Eight selected original images were visually inspected: API30 en-XV and API35
Literary Chinese unsupported-ZWJ reference/parent pairs, plus API30 Mongolian
fitted and API35 Manchu edge-to-edge horizontal-shrink pairs. Horizontal pairs
were also viewed with temporary white backing for legibility; those derived
previews are not archived. All 100 original capture bytes remain unchanged.
Visual inspection supports the clipped edge/bottom behavior; it does not certify
native-language correctness.

Original artifact ZIPs were downloaded, CRC-checked and SHA-256 matched:
- [Regression/lint 11639345541](https://github.com/c933103/AN-Paint/actions/runs/37974245255/artifacts/11639345541):
  a13de977b3f2fe7ba329a59e0c9aa3a1d8a6a9b4b725d2405aa9073377bd45de
- [Existing API35 device 11639280731](https://github.com/c933103/AN-Paint/actions/runs/37974245255/artifacts/11639280731):
  08ac75d3b5dfeda22a3d78f5bc6c39f9036edbd08516f0f8c42d93946d48b786

The APK/source and instrumentation build artifacts were produced, but their
larger ZIP bytes were not independently downloaded in this verification.

Run python verify_evidence.py from this directory to check the scoped archive,
entry hashes, exact inventories and the recorded controls. This verifies saved
evidence; it does not execute Android again.

[Exact-head Code Review completed without findings](https://github.com/c933103/AN-Paint/pull/35#issuecomment-6087057620).
Security-review/ready status and any later integration belong to the live PR.
The source-backed policy questions remain open.
