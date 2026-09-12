# AN Paint local.18

Updated 12 September 2026. Package `io.github.c933103.anpaint`, version
`2.14.1-local.18`, version code `71`. This updates local.17 with the same signing identity.

## Changes

- Pencil has its own adjustable 1–100 px width and exact numeric input; hard edges
  and the one-pixel default remain. Draft recovery retains the chosen width.
- Brush, Selection and Insert categories remember their selected tool and expand
  beside the main strip. Landscape keeps the strip left and opens options to its
  right. Portrait puts a horizontal strip below the header with options below it.
- Colour-managed imports convert supported ICC/CICP/PNG colour information and
  high-bit-depth/HDR input to the opaque 8-bit SDR sRGB working canvas. Alpha is
  preserved until opening onto the chosen background, inserting onto existing
  canvas pixels, or compositing an assembly onto white.
  HDR input support does not add HDR or transparent document output.
- The upstream font-introduction history is recorded in FONT-LICENCE-REVIEW.md.
  Public PRs show that the fonts were added for Arabic text, but do not establish
  the permission upstream relied on. No sufficient redistribution grant for
  AN Paint has been established; that is not a finding that Catrobat lacked permission.

## Verification status

The signed local.18 APK passed 177 unit/regression tests. Android 15/API35 passed 35 native tests and 8 installed-app tests; Android 11/API30 passed 34 native tests and 8 app tests. The Ultra HDR test requires API34+ and is explicitly filtered only from API30. No executed tests failed or skipped. Lint reported zero errors and 0 warnings. All four CPU architectures, the matching source/fonts/licences, 16 KB alignment and the local.17 upgrade signature were verified.

Build: [`6b5acc7b56ca5685e1b148bbf173522a6b218244`](https://github.com/c933103/AN-Paint/commit/6b5acc7b56ca5685e1b148bbf173522a6b218244). [Android workflow](https://github.com/c933103/AN-Paint/actions/runs/34692671218); [detailed verification](https://github.com/c933103/AN-Paint/blob/develop/verification/local18.json). The downloadable and in-app source ZIPs are the exact build snapshot; this final status was recorded afterward.

## Remaining boundaries

No physical phone is attached. ARM runtime performance, installation/update on a
phone, sharing to third-party apps and live gallery downloading remain unverified.
Android emulator checks are reported separately from physical-device use.

The editor's working canvas and exports remain opaque 8-bit SDR sRGB. Import
conversion cannot retain HDR brightness or colours beyond that output gamut.
Unsupported or malformed colour metadata produces a visible error instead of an
unmarked colour fallback. CODEC_SUPPORT.md records supported conversions and limits.

Historical local.17 results remain in verification/HANDOFF_LOCAL17.md and
verification/local17.json. Those counts do not describe this new build.
