# Earlier-request completion audit — local.19

This audit rechecks the actual source and regression coverage against the user's
requests, rather than treating the prior release notes as proof of completion.
The detailed original-editor mapping remains in EDITOR_PARITY.md. The signed
build's actual verification status belongs in HANDOFF.md and its verification
report; implementation coverage does not imply physical-phone verification.

| Requested area | Completion / location |
|---|---|
| Copyleft icons; distinct app identity | KDE Breeze LGPL icons with original SVGs and generated hashes; independent AGPL AN launcher; `io.github.c933103.anpaint`; credits in Help. |
| Material Design 3 colour scheme | Local.19 replaces the remaining old cream/blue UI chrome with shared Material 3 colour roles. Image pixels, brush colours and palette swatches keep their actual values. |
| Pencil and brush widths | Pencil has independent 1–100 px width. Brush, Watercolor, Airbrush and Eraser have adjustable sizes and exact numeric entry. |
| Tool grouping and orientation | Brush, Selection and Insert categories remember their chosen tool. Landscape keeps tools left and opens options right; portrait places tools below the toolbar and opens options downward. |
| Requested drawing/selection additions | Watercolor; Heart/Star/Arrow; polygon double-tap completion; rounded-corner radius; corner/edge resize and rotation for rectangle and free-form masks; Select all and two-column clipboard controls. |
| Navigation | Pinch/pan, cursor drawing, magnified preview, 100% zoom tick/step stop and centred Fit. Local.19 also autosaves a magnification-only setting change while the editor stays open. |
| Canvas size and assembly | Pixel/percent controls and aspect locks; touch trim/expand on all sides; up to 20 assembly inputs, name/time sorting, individual/batch crop, normalization, single-image Unplace with gap closing, drag/snap preview and PNG/save-to-Paint transfer. |
| Colours | Collapsible palette beside the colour indicator, four recent cells, Palette/Honeycomb/Advanced, presets and custom colours. RGB/HSV/HSL numeric labels and decimal entry are fully resource/locale based in local.19. |
| Import and memory | File picker opens without broad photo permission; explicit oversized-image choice with dimensions, pixel count and memory estimates; source files unchanged. Supported ICC/high-bit-depth/HDR input converts to SDR sRGB before compositing alpha. |
| Formats and export | PNG, JPEG, JPEG XL, WebP, HEIC and AVIF; applicable quality/lossless options; corrected thin/large JPEG XL encoding; Save and share exports before sharing. See CODEC_SUPPORT.md for format and colour-model boundaries. |
| Existing-image insertion and gallery | File > Insert image into canvas; Catrobat sticker gallery directly below. Local.19 completes cancellation/result ownership for downloads and adds download-to-insertion regression coverage, including source attribution and transparent pixels. |
| Recovery and editing history | Atomic autosave/recovery, recoverable pending geometry, disk-backed undo/redo and unavailable-action states. |
| Font and licence UI | Actual-font previews, 19 named choices, ten bundled OFL fonts, complete credits and fixed licence footer with Copy all. Dubai/STC review examines exact binaries, public terms and upstream introduction history; their redistribution rights for AN Paint remain unestablished. |
| Translation readiness | Android resources, positional formats, plurals and stable identifiers cover the editor. Local.19 closes remaining advanced-colour and assembly-status text gaps. No particular new human translation was requested. |
| Original editor removal | Original activity, layers, document transparency controls, Smudge, automatic crop and public project formats removed. Retained editing commands are mapped to the new view in EDITOR_PARITY.md. Internal selection masks and transparent input compositing remain necessary image operations. |

## Boundaries that cannot be labelled complete by a source change

- The working document and exports are opaque 8-bit SDR sRGB, as requested.
  HDR import produces an SDR rendition, not HDR editing/output. Unsupported
  colour models are rejected visibly; they are listed in CODEC_SUPPORT.md.
- Physical-phone installation, manufacturer-specific picker behaviour and ARM
  runtime performance require an attached device. No such device is available.
- The live Catrobat gallery is an external service. The source page and an image
  URL can be checked independently; this is distinct from a physical-phone live
  download. Deterministic end-to-end download/insertion tests are identified as
  such, not presented as a physical-device/network test.
- Public history does not establish what font permissions Catrobat relied on.
  No rights holder was contacted or additional font licence obtained. Excluding
  the two files is a decision about rights established for AN Paint; it is not
  an accusation about the upstream distributor.

Long device testing is asynchronous under CI.md. Pending/failed checks remain
visible in the release report and do not disappear merely because an APK exists.
