# AN Paint 0.0.27 development build

Package `paint.anpaint.android`; version code 80. Signed with the existing
certificate to update 0.0.26 and other installations of the same package.

## Changes

- The traditional Mongolian language option expands to fit its vertical autonym,
  English name and `[mn-Mong]` code, with vertical padding. The dialog theme had
  constrained the mounted choice row to 48 dp. The earlier detached-row test
  missed that constraint; the regression test now measures the real menu row.
- Swap arrows point up/down when foreground and background are stacked, and
  left/right in the vertical text layouts where the colours are side by side.
- The zoom slider retains its actual-size tick without a fixed `100%` label.
  The status area continues to show the current zoom percentage.

All earlier editing, file-format and translation features remain included.

Source: https://github.com/c933103/AN-Paint/commit/c0d8e105b21bb0032ff1178a391f291f0bda5a99
CI: https://github.com/c933103/AN-Paint/actions/runs/34789409967

## Verification at packaging

- Universal APK built for arm64-v8a, armeabi-v7a, x86 and x86_64.
- Local checks: 46 tests passed; the nine language checks were rerun after adding row padding. Local lint: zero issues.
- Rendered menu checks: mounted Mongolian row at normal and large text sizes on 412 dp and 320 dp portrait screens. Colour and zoom controls inspected in horizontal and vertical text layouts.
- CI regression: 250 tests, 0 failures, 0 errors, 0 skipped.
- CI lint: 0 issues.
- API 35 emulator job: in_progress.
- Pending checks are not counted as passed.
- The complete repository tree and file modes matched before the build. The source ZIP matches its 765 repository files plus all four pinned native source trees, and the APK embeds the identical ZIP.
- Package/version, original signing certificate, archive integrity and 16 KiB ZIP alignment verified after signing.

APK SHA-256: `ef6801d575919841c3084b411a0dd88339e2c16753354c1823f51547d2f50494`
Source ZIP SHA-256: `6e98d5f3f00566b0ebf08d7ab9465482858677d4cada93613183dbd3c61fb353`
Certificate SHA-256: `f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`

The private backup contains the signed APK, matching source, original signing
key, packaging tools and available verification reports/previews. Keep it
private; the signing key is not published to GitHub.

Snapshot: 2026-09-13T23:30:30.598183+00:00
