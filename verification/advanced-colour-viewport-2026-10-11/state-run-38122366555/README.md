# Full native colour state, run 38122366555

This is the preserved **green c711d0c0 trial**, not the later portrait-order trial.

- [Actions](https://github.com/c933103/AN-Paint/actions/runs/38122366555): all 102 installed methods, 814 unique JVM methods, lint, build and generation passed.
- Exact source head `c711d0c0cce6b3ecd2dcecce7063dfdc6cda305f`; tested merge `b8749d7bea1ec7b90668d2fe1a5f44e4af0d6c3f`; common tree `89c3c199c415c48100dace760440efaffd809d4f`.
- API 35 installed emulator: density 1, 640 × 320 landscape / 320 × 640 portrait, font 1×. The original positive editor viewport is 364 × 86px with 470px content; native gutter drag moves scrollY 0 → 55, fixed controls remain fully visible and stationary, and native Cancel closes once without committing.
- The full retained-state case passes in 16.435s: real surface dragging edits colour; mode/value/field selection and sixteen saved slots survive rotation; the actual configured fullscreen keyboard renders; one native Back hides it while retaining the exact dialog and field selection. Cancel restores the initial colour, one Back closes a reopened picker, invalid hex is rejected and valid `#2468AC` commits exactly once. Total close count is three.
- Ordinary 19/19 completes in 152.178s under the unchanged 180s cap. Native 74, gallery 3, vertical 4 and restart seed/verify 2 also pass. The app union contains all 28 declared methods, with no exclusions. The archive includes its coverage receipt and real external restart boundary log.

## Important portrait evidence limit

The Hungarian portrait PNG still shows a temporary SystemUI clipboard preview over lower controls. The accessibility-title absence guard returned green despite those pixels; it is ineffective and is not evidence of clean controls. The landscape PNG is clean. No unobscured Hungarian portrait-use acceptance is claimed from this run.

The [separate successor 512360bf](https://github.com/c933103/AN-Paint/commit/512360bffef3abb393557bce29a30217b03c5ecc) removes that guard and orders the same required native orientations landscape → portrait, preserving all caption/bounds/overflow/no-commit checks and ending with native Cancel in portrait. Production and the successful retained-state method are unchanged. Its own exact-head native PNG and outcome remain required; platform rotation behavior alone is not acceptance. See `portrait-capture-diagnosis.json` for the observed contradiction and primary Android source.

**Font 2× short landscape remains diagnostic and unaccepted.** This evidence does not establish physical-device, TalkBack, linguistic, simultaneous IME/footer-fit, merge or release acceptance. The APK is CI-debug signed.

## Reconstruct and verify

The original focused ZIP is stored in 33 binary parts, without changing any contained raw export. From this directory:

```sh
cat state-focused-evidence.zip.part* > state-focused-evidence.zip
sha256sum state-focused-evidence.zip
unzip -t state-focused-evidence.zip
```

Expected: **1,598,618 bytes**, **149 outer members**, SHA-256 `27156af60a180376f0f2fb38ecbb6d8524effb37eac25c7e36456ce649fa8352`.

`source-binding.json` binds the source digest, tested tree, APK/source hashes, original Actions artifact IDs/hashes and each raw colour export. The APK-embedded source ZIP equals the separately supplied source ZIP; all 487 tracked production files matched. `archive-inventory-inspection.json` lists every exact outer member and records the nested manifest inspection. All three app-owned raw exports and all their PNGs/receipts are retained, alongside all 87 JVM XML suites, 24 model PNGs/eight reports, lint, installed summaries, public CI job log and source binding. Direct receipt and screenshot copies are for convenience; the raw manifest-bound exports are authoritative.

Every archive member and each nested export member was inspected before publication. Images contain synthetic test UI only; clipboard text is the existing synthetic `Artwork作品` fixture. Public credit URLs and public CI paths are project test data. No raw full-device logcat, credentials, secret values or unrelated private data are included.
