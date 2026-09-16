# AN Paint 0.0.33 — grouped Edit commands and uniform tool tiles

Release candidate version code 87 (development build: 86). Edit expands Selection, Canvas, Flip / Rotate and Colours
groups. All twelve actions retain their behaviour and stable internal action IDs.
Tool tiles use one square size per writing mode and font setting; caption length
does not change an individual tile. Side tabs and vertical File commands share
a uniform row height. View uses short Pixel grid, Magnifier and Full screen
labels. Pixel-grid threshold/ruler help is available through How to use and by
holding Pixel grid. Its selected state indicates whether the grid is enabled.

Cursor drawing uses an Enable/Disable push button rather than a checkbox. The
on-canvas Start/Stop control, independent cursor outline and shared Drawing
brush settings remain. All 30 requested menu catalogues include the seven new
labels/help entries. README now describes the current editor and Save/Export
behaviour without obsolete release or language-coverage claims.

Verification of development source d65ee237aa341d91c655a6b59be0bb6b3b9dcb6e:
81 host checks passed; all 134 generated translation files match regeneration;
Android aapt2 compiled the complete resource tree; whitespace checks passed.
Workflow 35031011913 passed all three jobs: 270 regression tests, zero lint
issues and 79 Android API 35 instrumentation tests, without failures or skips.
Rendered previews were reviewed for grouped Edit actions, square View tiles,
vertical Chinese/Mongolian layouts, Armenian and Latin Cantonese captions, and
the cursor push button. The development APK uses version code 86.

The initial run (35001403001) built the APK and passed API 35, but unit-test
compilation failed on an ambiguous View/ViewParent property. Explicit nullable
View traversal fixed it. Both workflows now use pinned Node 24 actions, keeping
the existing ZIP artifact layout. The corrected run above passed regression.

This commit prepares the non-debuggable release variant and full API 30/35
verification. Version code 87 permits an upgrade from the development APK.
The release build, release regression/lint and both emulator results are pending;
the successful debug results do not substitute for these checks. Exact-source
verification and private upgrade signing remain required before release delivery.
Follow CI.md: finish useful work and report the asynchronous run without waiting
for GitHub as the sole remaining activity. Keep the signing key and private
backup outside GitHub.

Development build and checks:
https://github.com/c933103/AN-Paint/actions/runs/35031011913

---

# AN Paint 0.0.32 — unified tool tiles, cursor drawer and menu translations

Version code 85. Edit and View use the same scrolling tool tiles as Draw.
View > Cursor drawing expands the enable switch, independent round/square cursor
outline, magnifier and marker-size controls directly in its panel. Brush choice,
width and tip remain under Draw > Drawing. Enabling cursor mode preserves the
brush settings and starts with positioning only. The floating on-canvas drawing
button changes its selected state and Start/Stop caption, with a non-modal toast
explaining pan to draw / tap again to stop. Active crosshairs change colour.
Opening the cursor drawer or restoring a draft pauses drawing. Cursor shape is
saved separately from the brush shape; the marker still has its original size.

The system-default language row resolves against the device language even when
the app uses another language. Armenian (hy) is added. All five main tabs and
first-level commands, including FG/BG and cursor controls, have explicit text for
ja, zh-TW, zh-HK, zh-CN, yue-Hant, yue-Latn, lzh-Hant, ar, de, pl, ru, es-419,
es-ES, pt-PT, pt-BR, it, fr, he, ko-KR, ko-KP, id, ms, vi, tl, th, el, sr-Cyrl,
sr-Latn and tr, plus hy. Deeper dialogs retain their existing partial vocabulary.
Cantonese Latin uses Jyutping; Korean regional commands and Serbian scripts are
separate resources. Existing pinned translator sources and notices are retained.

The release passed workflow 34992890074: 81 local host checks; 267 release
regression tests; zero app lint issues; 78 instrumentation tests on API 30 and
79 on API 35. All passed. Visual checks cover matching View/Edit tool tiles,
Armenian, Arabic and Latin Cantonese captions, and the cursor drawer.

The non-debuggable universal APK uses the existing upgrade signing certificate,
contains four ABIs and passes 16 KB ZIP alignment. Embedded and separate source
archives match every one of 830 exported repository blobs.

Source: https://github.com/c933103/AN-Paint/commit/964b82f9a2b157a867e361845cdaa0adde0439d5
Build: https://github.com/c933103/AN-Paint/actions/runs/34992890074
Release: https://github.com/c933103/AN-Paint/releases/tag/v0.0.32

APK SHA-256: `864630a4001bb9542aaf32c191012dbc7ea7da6c52a708581316b74c30ea29f5`
Source SHA-256: `86d8039ced245c3e269162670a6ec26e83ab8ea9c574989916845587aa4a6f10`

The release request publishes this exact verified APK and matching source. The
private signing key and build backup remain outside GitHub. Results below are
historical and belong to their stated versions.

---

# AN Paint 0.0.31 — explicit cursor control and image save settings

Version code 84. Cursor mode starts with positioning only; Start drawing / Stop
 drawing below the canvas controls ink. Dedicated cursor settings under View and
beside that control expose brush, size, shape, magnifier and marker visibility.
Opening settings, switching tools and reopening drafts pause ink. Original
Paintroid geometry remains; the marker now stays visible at fitted zoom without
changing the painted brush width. Main canvas bitmap filtering remains off.

Save as offers all ordinary images and real compression controls. Export as is
restricted to ICO, ASCII art and Base64 text. Save retains the successful Save as
name, URI, format, quality, lossless mode, GIF dithering and TIFF compression,
including draft recovery. JPEG XL lossless still uses the verified native codec.

GIMP supplies context-matched common vocabulary across 81 language bases; original
translator notices, full GPL text, source revision/hashes and selected original
PO entries are bundled. Local regional/action corrections retain precedence.
Coverage is partial; see translations/README.md and coverage.json.
Twenty GIMP languages are added, along with explicit tt-Cyrl and tt-Latn choices;
Latin Tatar is generated from the sourced Cyrillic starter catalogue.

The release passed workflow 34979038050: 80 local host checks; 261 release regression tests; zero app lint issues; 78 instrumentation tests on API 30 and 79 on API 35. All passed.

Real Android input verifies positioning without ink followed by the visible
Start drawing control, strokes, Stop drawing and cursor settings. JPEG XL Save as
with lossless enabled and subsequent Save preserve all 49,601 canvas pixels;
lossy JPEG XL and AVIF quality controls change the actual encoded image files.
The release APK is non-debuggable, uses the existing upgrade signing certificate,
contains four ABIs and passes 16 KB ZIP alignment. Embedded and separate source
archives match every one of 821 exported repository blobs.

Source: https://github.com/c933103/AN-Paint/commit/b18fdb6cfb94230fc7d16a89fe0c03674c23b16b
Build: https://github.com/c933103/AN-Paint/actions/runs/34979038050
Release: https://github.com/c933103/AN-Paint/releases/tag/v0.0.31

APK SHA-256: `680cfd1d4eb9cc212299db3986865f10dd4911b1f2e84016d38bf716434ff6df`
Source SHA-256: `b1592ba5f212033172579e2cae6ffbb51b271a4aa6cbe8ac315006b728bfd246`

The release request publishes this exact signed APK and source. The private key
and backup remain outside GitHub. Historical results below belong to 0.0.30.

---

# AN Paint 0.0.30 — cursor input and sharp canvas display

Package `paint.anpaint.android`; version code 83. Cursor drawing now enables ink
immediately, with an explicit Draw with cursor checkbox for moving without ink.
Short strokes are retained instead of being cancelled as taps. Circle/square
markers, magnification, cancellation and undo remain supported. Draw/move mode
persists in drafts. Main canvas, selection previews and magnifier use unfiltered
pixel display; drawing antialiasing still defaults off.

The new installed-app tests verify a real input-dispatcher swipe paints a line
and Save as JPEG XL followed by Save preserves every canvas pixel. Native JPEG
XL lossless tests already passed for 0.0.29. See docs/CURSOR_UPSTREAM.md and
docs/JPEG_XL_LOSSLESS.md. The corrected release passed workflow 34945326732:
80 local host checks, 257 release regression tests, zero app lint issues, 77 instrumentation tests on API 30 and 78 on API 35. All passed.
The actual input-dispatcher cursor swipe, explicit move-only mode, unfiltered
canvas pixel comparison, and JPEG XL Save as/Save checks all passed. The universal
APK uses the existing upgrade certificate, is non-debuggable, includes four ABIs
and passes 16 KB ZIP alignment. Its embedded source ZIP matches the separate
archive and all 791 exported repository blobs.

Source: https://github.com/c933103/AN-Paint/commit/31526a42ced7d6eae6c8c9a756ae6c2e8b23d162
Build: https://github.com/c933103/AN-Paint/actions/runs/34945326732
Release: https://github.com/c933103/AN-Paint/releases/tag/v0.0.30

APK SHA-256: `7064b86171764da83d6531ac985e4a71d78f9105add761d79d54a1d0162f27d4`
Source ZIP SHA-256: `8093a01979acfa1e6b953d0e30fc4150929b390bddbb9fd480303dd232773c81`

The checked-in release request publishes this exact verified APK and corresponding
source. The private key and backup remain outside GitHub. Earlier results below
belong to 0.0.29.

The first 0.0.30 run (34944021765) compiled and passed the new app JPEG XL save
case on API 30 and 35. Its pixel-display test exposed Android's implicit bitmap
filter constructor flag; the display paint now explicitly clears it. The cursor
swipe painted correctly, but the test helper incorrectly required a checkbox's
performClick return value to be true. Checkbox checks now verify state or use
actual UI input. The corrected run above passed both checks and the complete release matrix.

---

# AN Paint 0.0.29 — language and cursor corrections

Package `paint.anpaint.android`; version code 82. The user clarified Tai Nüa
(`tdd`): its native name and five sourced action labels replace the mistaken
`tai` collection choice, with saved-preference migration. See the translation
audit in `translations/README.md`: regional Spanish and Korean still share base
catalogues, and all non-English editor translations remain partial.

Mongolian language radio alignment now retains the native CheckedTextView
padding. Both Ainu scripts are selectable: `ain-Latn` and `ain-Kana`, with
sourced Brush/Save/Done terms and migration of the old `ain` preference.
Cursor drawing directly adapts Paintroid's brush-sized circle/square overlay,
alternating crosshairs, activation dot and cumulative travel detection. Its
circular magnifier samples the cursor and defaults on, with adjustable zoom.
See `translations/README.md` and `docs/CURSOR_UPSTREAM.md` for provenance.

The final source, including Tai Nüa, passed release workflow 34914389654:
75 host checks, 255 release regression tests, zero app lint issues, 76 Android
API 30 tests and 77 API 35 tests. All passed. The universal release APK is signed
with the existing upgrade certificate; package, version, non-debuggable manifest,
four ABIs and 16 KB ZIP alignment are verified. Its embedded source ZIP matches
the separate source archive and all 788 exported repository blobs.

Source commit: https://github.com/c933103/AN-Paint/commit/01681570c448824a32039473bede5ae9591795c9
Build and checks: https://github.com/c933103/AN-Paint/actions/runs/34914389654
Release: https://github.com/c933103/AN-Paint/releases/tag/v0.0.29

APK SHA-256: `97de3f95832c560b20fe39b46e78e2f15658a8ba73d0a7c2a5c76871c905d940`
Source ZIP SHA-256: `0ed0526a5c91fdb3ceb0629743f5925431bf47e3e765e36a93dfa20ef16b64df`

The checked-in release request publishes this exact signed APK with corresponding
source, checksums and verification evidence. The private signing key and build
backup remain outside GitHub. Earlier results below describe 0.0.28 only.

---

# AN Paint 0.0.28

Package `paint.anpaint.android`; version code 81. Universal, non-debuggable release
APK, signed with the existing certificate to update 0.0.27 and earlier compatible
installations. Minimum Android API 21; target API 35.

## Changes and review

PR #1's one-catalogue translation consolidation preserves all 4,867 existing
strings. Its merged build, lint, regression and Android 35 checks passed.
The review found and fixed missing starter coverage, a Save label that fell back
to English in the unsaved prompt, and inaccurate starter vocabulary. Ainu and the
Tai collection remain offered with English fallback. Partial starter translations
still require native-speaker review; automated tests do not certify their quality.

The Mongolian language option now contains only its native name and `[mn-Mong]`.
The two joined words occupy adjacent vertical columns. The complete name and code
fit the actual menu row in portrait, landscape and at enlarged text size.

The release build also corrects Kvazaar's C dialect and HEIF file-offset flags on 32-bit Android.
Existing image formats, editing features and earlier colour/zoom fixes remain.

## Completed verification

- 75 host checks passed, including generation, release gating and exact APK signing-patch round trips.
- 10 local language/layout tests passed; local release lint has zero issues.
- Release APK and both instrumentation APKs compiled locally for x86_64.
- CI release regression: 251 passed; release lint: 0 issues.
- Android 30: 76 instrumentation tests passed.
- Android 35: 77 instrumentation tests passed.
- Universal ABIs: arm64-v8a, armeabi-v7a, x86_64 and x86.
- The remote tree matched before building. All 781 exported repository blobs
  match their Git objects; four pinned native source trees are also included.
- The APK embeds the identical corresponding-source ZIP. Signature, package,
  version, non-debuggable manifest and 16 KB ZIP alignment verified after signing.

Source commit: https://github.com/c933103/AN-Paint/commit/30968c60299d05cf4dd2335e8e1b887c4cf66209
Build and checks: https://github.com/c933103/AN-Paint/actions/runs/34794257334
Release: https://github.com/c933103/AN-Paint/releases/tag/v0.0.28

APK SHA-256: `f154728854af0be1c8bb62d4908fde75f4b082a9c7e2bc1aab217ce2819e5c1c`
Source ZIP SHA-256: `0c7481d566eb35a6daefaceaef4d35c72cb5f1061f901b9f394f768bbd8157f2`
Signing certificate SHA-256: `f6220f4f21dd5af98d01983f2dbbf37893adfe93aa0de19868ac93b48b0b7791`

The private backup contains the APK, source, original signing key and final
verification reports. Keep that backup private; GitHub receives only public
release assets and public signature/alignment bytes, never the key.

Snapshot: 2026-09-14T01:25:39.390893+00:00
