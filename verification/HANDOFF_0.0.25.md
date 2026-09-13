# AN Paint 0.0.25 development build

Package: `paint.anpaint.android`, version code 78. Signed with the existing
certificate for upgrading the previous installation.

The update centers Main captions in their tile width; applies matching icon
tiles to Edit, View and Color commands; keeps all six shortcuts at the right
of the first header row in portrait and landscape; restores the filename and
AN Paint subtitle; and restores vertical tabs and side panels in landscape for
every language. File retains its text commands. Vertical-script captions,
status rails and dialogs remain supported.

Source: https://github.com/c933103/AN-Paint/commit/96d8f7d64dcdc98a6efe14aedea272bf08950e6c
CI: https://github.com/c933103/AN-Paint/actions/runs/34767059225

## Verification at packaging

- Universal APK built successfully for arm64-v8a, armeabi-v7a, x86 and x86_64.
- All 240 regression tests passed; no failures, errors or skipped tests.
- CI lint: zero issues. Final local layout checks: 13 passed, including
  320 dp portrait headers, rendered caption centering and both vertical scripts.
- API 35 emulator checks are still running at this snapshot. This is a
  development build; this report does not claim those pending checks passed.
- All 751 repository blobs/modes matched the intended tree before the build.
  The embedded source ZIP matches the archived source and its 748 included
  repository files. The ZIP excludes three Git/editor metadata files and also
  includes all four pinned native source trees.
- APK signature, the existing certificate, archive integrity and 16 KiB ZIP
  alignment verified.

APK SHA-256: `71eeb13157809c4f7b9fd3c1c5ab690b68015393bb2ca5d333ec7a4d90b02d76`
Source ZIP SHA-256: `d6aaae3aa78666b68ac62f0b48013a38e3c706629ee16747455a7d74ffe033a1`
Certificate SHA-256: `f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`

The private backup contains this signed APK, matching source ZIP, the original
signing key, packaging tools, reports and rendered layout previews.
Snapshot: 2026-09-13T16:06:54.940573+00:00

## Subsequent completion

Rechecked during 0.0.26 work: the complete workflow finished successfully.
The API 35 emulator job `103751118750`, including its prebuilt device tests,
passed. The build and regression/lint jobs also remain successful. This updates
the pending emulator status above without changing the delivered APK.
