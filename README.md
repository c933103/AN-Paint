# AN Paint

AN Paint is an independently maintained Android image editor derived from
[Catrobat's Pocket Paint (Paintroid)](https://github.com/Catrobat/Paintroid).
It is based on tag `v2.14.1`, commit `853ce3c346910ea73aa4de5514f2a76ace1396fb`;
original copyright and licence notices are retained.

[Download the latest published release](https://github.com/c933103/AN-Paint/releases/latest).
The `develop` branch can contain changes that are still being built or tested.
Check [GitHub Actions](https://github.com/c933103/AN-Paint/actions/workflows/android.yml)
for their actual status and [HANDOFF.md](HANDOFF.md) for version-specific evidence.

The application ID is **`paint.anpaint.android`**. Android 5.0 (API 21) or newer
is required. Published APKs contain all four supported ABIs: arm64-v8a,
armeabi-v7a, x86_64 and x86.

## Editing

- View, Draw, File, Edit and Color tabs. Portrait uses a panel above the canvas;
  landscape uses a side ribbon. Tool tiles share a square size, including vertical
  scripts, and scale together with the system font setting.
- Draw groups tools into Drawing, Selection and Insert. Edit groups its commands
  into Selection, Canvas, Flip / Rotate and Colours. Expand a group to reach its
  commands; collapse it to recover canvas space.
- Pencil, brush, watercolor, spray, eraser, fill, colour picker, shapes and text.
  Pencil and brush widths have independent numeric controls up to 100 px.
- Rectangular and free-form selections, resize/rotation handles, an aspect-ratio
  lock, canvas trimming/expansion, image resizing and disk-backed undo/redo.
- Navigate supports pinch zoom and pan, actual-size and Fit view. Pixel grid is a
  short, selected-state toggle; its 800% threshold and pixel rulers are explained
  under View > How to use and by holding the grid button.
- View > Cursor drawing expands cursor options, with an Enable/Disable button,
  independent round/square outline, magnifier and marker size. Brush controls stay
  under Draw > Drawing. Enabling cursor mode starts with positioning only; the
  on-canvas Start/Stop button controls ink, displays guidance and changes the
  cursor's visible state. Reopening cursor options or a draft pauses drawing.
- Autosave and draft recovery, foreground/background previews, recent colours,
  sixteen saved colour slots and an advanced colour picker.
- A separate assembly workspace for up to 20 images, with cropping, normalization,
  alignment, direct PNG saving and transfer to the editor.

Both editing workspaces produce opaque images. Layers, transparency controls,
Smudge, automatic crop and native project formats are absent. Large imports
receive a memory-based size check and an explicit resize choice. See
[EDITOR_PARITY.md](EDITOR_PARITY.md) for the feature mapping.

## Files and image formats

**Save as** offers PNG, JPEG, JPEG XL, WebP, HEIC, AVIF, BMP, GIF, DIB and TIFF in
one filename/format panel. It exposes applicable quality, lossless, dithering and
TIFF compression controls. JPEG XL supports actual lossless encoding.
**Save** reuses the last successful Save as destination and encoding settings,
including after draft recovery.

**Export as** offers ICO, ASCII art and Base64 text with their relevant options.
Export does not replace the Save destination or clear unsaved changes.
**Save and share** offers all output formats.

PDF and TIFF imports provide page previews and selection. Animated GIF, APNG and
WebP imports warn when opening a still frame. The optional Catrobat gallery
provides copyable, editable attribution for inserted artwork.

## Languages and text

Choose **View > Languages** to override the device language. The system-default
choice is labelled in the device's language, independently of the selected app
language. Android 13 and newer also expose the setting in system App languages.

The main tabs, first-level commands and Edit groups have explicit translations
for `ja`, `zh-TW`, `zh-HK`, `zh-CN`, `yue-Hant`, `yue-Latn`, `lzh-Hant`, `ar`,
`de`, `pl`, `ru`, `es-419`, `es-ES`, `pt-PT`, `pt-BR`, `it`, `fr`, `he`, `ko-KR`,
`ko-KP`, `id`, `ms`, `vi`, `tl`, `th`, `el`, `sr-Cyrl`, `sr-Latn`, `tr` and `hy`.
Other languages and deeper dialogs have varying partial coverage, with English
fallback. Translation completeness is not a claim of independent native review.

Existing Paintroid, Android and GIMP vocabulary retains its provenance and
translator credits. Armenian, both Tatar scripts and both Ainu scripts are
available. See [translation notes](translations/README.md) and
[TRANSLATING.md](TRANSLATING.md) for catalogues, coverage and regeneration.

Inserted text supports horizontal writing and both vertical column orders, with
mixed, sideways or upright letters. Literary Chinese and traditional Mongolian
also use vertical interface captions; the bundled Mongolian font preserves joined
words.

## Installation and updates

Install the signed APK from a published release. Updates to `paint.anpaint.android`
require the same signing certificate and a higher version code. Earlier builds
with different package IDs and the original Pocket Paint remain separate apps.
To move an image between separate installations, save it as PNG and open it in
the other app; private drafts and preferences do not transfer automatically.

CI artifacts are development outputs. Their availability does not mean all checks
passed, and their temporary CI signing key does not replace the existing upgrade
key used for published releases.

## Building and checking

Install JDK 17, Android SDK Platform 35, Build-Tools 35.0.0,
NDK 27.2.12479018 and CMake 3.22.1. Set `JAVA_HOME` and `ANDROID_HOME`, then run:

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew --no-daemon --max-workers=1 :app:assembleDebug
./gradlew --no-daemon --max-workers=1 :Paintroid:testDebugUnitTest :app:lintDebug
```

The APK is `app/build/outputs/apk/debug/app-debug.apk`. The first build needs
Google Maven, Maven Central, the Gradle Plugin Portal, GitHub and
download.osgeo.org for dependencies and pinned native codec sources.
Use `-PnativeAbis=x86_64` for an emulator-only build. Instrumentation tests use
`:Paintroid:connectedDebugAndroidTest` and `:app:connectedDebugAndroidTest`.

GitHub uploads the APK and matching source before emulator tests finish.
Regression/lint runs independently. Routine runs test API 35; release verification
uses both API 30 and 35. See [CI.md](CI.md) for triggers, deadlines and the
separation between development artifacts and verified releases.

The APK includes corresponding source, including pinned native codec sources,
exportable from File > About / licences / credits. Published releases also include
a separate source archive, verification evidence and checksums. See
[LOCAL_BUILD.md](LOCAL_BUILD.md), [CHANGES_FROM_UPSTREAM.md](CHANGES_FROM_UPSTREAM.md)
and the preserved [upstream README](UPSTREAM_README.md).

## Licences and artwork

- Application and original paintbrush launcher: [GNU AGPL-3.0-or-later](LICENSE).
  Original code: Copyright © 2010–2022 The Catrobat Team and contributors;
  AN Paint modifications and launcher: Copyright © 2026 AN Paint contributors.
- Tool/action icons: KDE Breeze, LGPL-3.0-or-later. Sources, revision and notices
  are in [artwork/breeze](artwork/breeze). Standard Android controls use platform
  artwork. The launcher source is [artwork/an-paint/launcher.svg](artwork/an-paint/launcher.svg).
- Bundled fonts: SIL Open Font License 1.1, with authors and full terms in
  [font notices](Paintroid/src/main/assets/legal/FONT_NOTICES.txt).
- [Asset credits](Paintroid/src/main/assets/legal/ASSET_CREDITS.txt) and
  [third-party notices](Paintroid/src/main/assets/legal/THIRD_PARTY_NOTICES.txt)
  identify packaged artwork, libraries and translation sources.
- Native codec licences and grants are retained in the
  [JPEG XL](Paintroid/src/main/assets/legal/JPEG_XL_NOTICES.txt),
  [WebP](Paintroid/src/main/assets/legal/WEBP_NOTICES.txt),
  [HEIC–AVIF](Paintroid/src/main/assets/legal/HEIF_AVIF_NOTICES.txt) and
  [TIFF](Paintroid/src/main/assets/legal/TIFF_NOTICES.txt) notices.
  Gallery artwork retains its CC BY-SA 4.0 attribution and source links.

The upstream issue tracker covers Pocket Paint; AN Paint is independently
maintained. Signing keys and private build backups are never published here.
