# AN Paint 0.0.26 development build

Package `paint.anpaint.android`; version code 79. Signed with the existing
certificate to update the previous installation.

## Changes

- All sixteen saved palette slots remain present, including empty boxes.
  Add colour opens the editor and saves the accepted colour directly. Empty
  slots open the same flow. Advanced is beside Black / white; saved colours
  support editing, background selection and removal.
- Pixel grid adds top/left rulers in image pixels. Rulers follow zoom/pan,
  resizing and draft restoration, sharing the scrollbar coordinate model.
- Cursor drawing shows live x/y beside the zoom percentage, including during
  movement. Narrow status layouts reserve enough space without causing an
  autosave/viewport resize loop.
- View precedes Draw. Navigate is first in View and remains the default tool;
  its options move with it. Classic icon tiles, compact title-row shortcuts,
  the subtitle and vertical landscape tabs remain.
- Anti-aliasing defaults off; previously saved choices are retained.
- Device language is first, English (International) second. The menu adds the
  requested English regions and Spanish/Korean splits, labels pt-PT, fixes
  language names/capitalization/codes and keeps the other options sorted.
  The thirty requested name-only choices use English UI until translated.
  Hokkien tags use canonical nan-Hant-TW/nan-Latn-TW ordering; tai is labelled
  Tai languages. See translations/README.md for naming sources and coverage.

All earlier format support, PDF/TIFF page selection, animation warnings,
Save/export behavior, gallery credits and Japanese flip corrections remain.
The complete 0.0.25 workflow, including its previously pending API 35 checks,
has passed.

Source: https://github.com/c933103/AN-Paint/commit/438fab32575139e64e2260f33e6df08887148047
CI: https://github.com/c933103/AN-Paint/actions/runs/34776649817

## Verification

- Universal APK built for arm64-v8a, armeabi-v7a, x86 and x86_64.
- CI regression: 249 tests, 0 failures, 0 errors, 0 skipped.
- CI lint: 0 issues.
- Final local Android checks: 59 passed; local lint: zero issues. Host checks: 68 passed, including generation with reversed filesystem enumeration.
- API 35 emulator checks passed after packaging (job `103777089974`). The private backup retains the accurate earlier packaging-time snapshot.
- All 766 repository files and modes matched before the build. The embedded source ZIP matches the exported archive and its 763 repository files, plus all four pinned native source trees.
- APK package/version, signature, original certificate, archive integrity and 16 KiB ZIP alignment verified after signing.

APK SHA-256: `971e98c7c64874094fb777f96e4488d92f62d1c36b495308817c73a1aa22d2d2`
Source ZIP SHA-256: `d79c0553d4b2ee33d09fc4134e4bc791015b69070a1204e64e54aa92df56d03b`
Certificate SHA-256: `f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`

The private backup contains this signed APK, matching source ZIP, original
signing key, packaging tools, reports and rendered layout previews. Keep this
backup private; the signing key is not published to GitHub.

Packaging snapshot: 2026-09-13T19:17:50.060358+00:00

API 35 completion confirmed: 2026-09-13T19:22:13.655749+00:00
