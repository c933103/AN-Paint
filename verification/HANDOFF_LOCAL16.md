# AN Paint local.16 — unfinished development snapshot

Status recorded 12 September 2026. This is a handoff of the latest build, not a completed or fully verified release. Development and verification are paused at the user's request so the current APK and source can be delivered promptly.

- APK version: `2.14.1-local.16`, version code `69`.
- Package: `io.github.c933103.anpaint`; the existing AN Paint signing key is retained for updating local.15.
- Built source: commit `71b4bc76ce42d4c443babcc9e8032aa0e87d60e3`.
- Build/report: https://github.com/c933103/AN-Paint/actions/runs/34496438712
- Four native architectures: arm64-v8a, armeabi-v7a, x86_64 and x86.
- The APK carries the exact corresponding source ZIP. Later documentation-only commits record this handoff; they do not change the compiled application.

## Implemented

- Removed the original editor after a source-based feature audit. `EDITOR_PARITY.md` records the retained, moved and deliberately removed capabilities; it is a coverage audit, not proof of complete behavioral equivalence.
- Removed layers, document transparency, Smudge, automatic crop and native project formats. Imports flatten onto the background colour; assembly output is opaque white. Internal geometric masks preserve free-form and rotated selections.
- Added Watercolor beside Brush/Airbrush, plus Heart, Star and Arrow tools.
- Added sizes up to 100 px with sliders and numeric entry; Watercolor strength and Spray radius have their own controls.
- Added cursor drawing, magnified preview, smoothing/antialiasing controls and hide-controls mode under View. Fit also centres the canvas. Polygon can draw connected open segments with Close polygon disabled.
- Added four recent-colour cells at the far right of the palette.
- Renamed File insertion to **Insert image into canvas…**. Added the optional online Catrobat sticker gallery directly below it and retained source links in Image credits. Gallery media are not bundled offline.
- Added JPEG quality selection, lossless/lossy JPEG XL code paths, and Save and share.
- Moved UI text into Android resources, with plural handling, stable control identifiers and translation guidance. Human translations have not been supplied.
- Preserved the prior selection transforms, touch canvas expansion/trimming, autosave, assembly, zoom controls, copyleft icons, app identity and licensed font catalogue.

## What verification actually completed

- Android APK build succeeded for all four architectures.
- **154/154 regression tests passed.** This is the current consolidated-editor suite; obsolete tests for the deleted original editor are no longer run.
- Android lint completed with **0 errors and 5 warnings**.
- **5/6 Android 11 x86_64 emulator tests passed.** Passing checks cover small-image lossless JPEG XL pixel equality, lossy output and reduced decoding, region decoding/scaling, invalid-input/memory-budget handling and loading all advertised fonts.

## Known failure — correction still required

`NativeCodecTest.losslessEncodingPreservesPixelsAcrossThe2048PixelChunkBoundary` fails while encoding a **2057 × 17** image with `IOException: Cannot encode JPEG XL pixels.`

Small-image codec tests passing does not establish reliable JPEG XL support for larger images. Use PNG or JPEG for dependable export in this snapshot. The exact range affected by the encoder defect has not been established. The CI run is correctly marked failed; this handoff does not waive or hide the failure.

## Next tasks, in order

1. **Correct JPEG XL chunked encoding.** Reproduce the saved failing fixture, check libjxl's buffered/streaming-input contract, implement the correction and rerun the failed test and relevant round trips. Include larger portrait/landscape images and memory-pressure behavior before considering the codec complete.
2. **Finish device verification.** Install/update on a physical ARM Android phone. Exercise the document picker, Save and share, gallery import and credits, cursor/magnifier, Watercolor, shapes, numeric controls, selection masks, autosave and assembly. Only x86_64 codec/font execution has been checked on an emulator; compiling ARM libraries is not an ARM runtime test.
3. **Review the five lint warnings.** Two vector `fillType` warnings concern API 21–23; one concerns Android backup/data-extraction rules; two concern monochrome adaptive icons. Existing v33 monochrome resources need checking against lint's warning before deciding the appropriate change.
4. **Investigate the actual Dubai and STC font licences.** Retrieve the exact `dubai` and `stc_regular` files from the original Paintroid revision; identify their full family/version, author and source. Find authoritative licence/EULA terms from the rights holders and original distribution, specifically covering redistribution and embedding in an Android app. Record the evidence, attribution requirements and any modification limits. Decide whether either font can be restored. **Their permission status is unresolved here; absence of permission in the bundled metadata alone is not a conclusion that redistribution is prohibited.**
5. **Complete translation and release review.** Add and review requested languages, including plurals, numeric entry, accessibility and right-to-left layout where applicable. Recheck the parity audit against device behavior, correct any remaining gaps, then publish a fully verified release with a fresh APK/source match.

## Why the old font test used sans-serif

The earlier build removed the Dubai and STC files while their redistribution terms were unresolved, and the old selector used system-font fallbacks. The test consequently compared those fallbacks. Keeping variables named `dubaiFontFace` and `stcFontFace` was misleading: the values no longer represented those fonts.

The original selector and its tests have now been deleted with the original editor. Current tests load the actual ten bundled OFL font files and nine system-font choices. Investigation of Dubai and STC is explicitly outstanding above; those names must not be presented as actual fonts while backed only by a sans-serif fallback.
