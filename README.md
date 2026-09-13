# AN Paint

> Version 0.0.27 fixes clipping of the Mongolian language option, turns the Swap arrows to match the foreground/background arrangement, and removes the zoom slider's fixed 100% text label. All earlier format and editing support remains included. Package `paint.anpaint.android`, version code 80. See [HANDOFF.md](HANDOFF.md) for verification status.

AN Paint is an independently maintained Android image editor derived from
[Catrobat's Pocket Paint (Paintroid)](https://github.com/Catrobat/Paintroid),
based on tag `v2.14.1`, commit `853ce3c346910ea73aa4de5514f2a76ace1396fb`.
Original Catrobat copyright and licence notices are retained.

The application ID is **`paint.anpaint.android`**. Its launcher shows an original
paintbrush with a coloured stroke. Android 5.0 (API 21) or newer is required.

## Editing

- View, Draw, File, Edit and Color tabs with a collapsible panel above the canvas in portrait and a vertical side ribbon in landscape. Navigate is first in View and the initial tool; Draw holds Drawing, Selection and Insert categories that remember their tool. All panel tools have visible labels. Cut/Copy/Paste sit beside Undo/Redo on the first title row, with the filename and AN Paint subtitle.
- Touch drawing, shapes, text, fill, free-form and rectangular selections.
- Adjustable hard-edged Pencil width from 1 to 100 px.
- Corner and edge resize handles, a rotation handle and an aspect-ratio lock.
- Pinch zoom and pan, centred 100% zoom controls, and Fit view. Pixel grid enables top/left rulers in image pixels. Cursor drawing shows live x/y next to the zoom percentage. Anti-aliasing defaults off, while explicitly saved settings are retained.
- Pixel/percentage sizing, touch canvas trimming and expansion, and disk-backed undo.
- Autosave and draft recovery, a compact collapsible toolbox, and advanced colour controls.
- A separate assembly workspace for up to 20 images, with cropping, normalization,
  alignment, direct PNG saving and transfer to the main editor.
- Watercolor, Heart/Star/Arrow, cursor drawing, magnified preview and sizes up to
  100 px with exact numeric entry.
- Save as preserves canvas pixels in PNG, lossless JPEG XL/WebP/AVIF, BMP, DIB, TIFF or Base64 PNG text. Save writes the last successful Save as destination directly. Export as offers JPEG, lossy JPEG XL/WebP/AVIF, HEIC, GIF, ICO and ASCII art with their relevant quality, dithering, icon-size or text options. Export never clears unsaved changes or changes the Save destination. Save and share offers all formats.
- PDF and TIFF page previews/selection, plus warnings when animated GIF/APNG/WebP imports become still images.
- Live FG/BG colour previews with Use colour / Cancel, four recent colours and sixteen shared saved slots, including visible empty slots. Add colour or tap an empty slot to choose and save a colour directly; hold a saved slot to edit, use as background or remove it. Advanced is beside Swap and Black / white. The optional Catrobat gallery supplies copyable/editable credits.
- View > Languages, reviewed destructive-action and clipboard translations, and initial Literary Chinese (`lzh-Hant`) and traditional-script Mongolian (`mn-Mong`) catalogues. Text supports horizontal and both vertical column orders, with mixed, sideways or upright letters; Noto Sans Mongolian preserves joined text.

The original editor, layers, transparency controls, Smudge, automatic crop and
native project formats have been removed. See [EDITOR_PARITY.md](EDITOR_PARITY.md)
for the audited feature mapping. The current UI uses Android translation
resources; see [TRANSLATING.md](TRANSLATING.md).

Both editing workspaces produce opaque images. Large imports receive a memory-based
size check and an explicit resize choice; files are not silently downsized.

## Installing this version

`0.0.27` uses version code `80` and updates `0.0.26`, `0.0.25`, `0.0.24`, `0.0.23`, `0.0.22` and local.20–local.22 in place when signed with the existing key. The package change introduced in local.20 means it **installs alongside local.15 through
local.19** (`io.github.c933103.anpaint`), earlier AN Paint (`app.paint.local`) and
the original Pocket Paint. Keeping the signing key does not make different
package names an in-place update.

To transfer your current image, **save it as PNG in the old app, then open it in
the new app**. Private autosaves, undo history, clipboard and preferences stay in
the old installation. Keep the old app until needed images have been exported.
Later updates to `paint.anpaint.android` must use the same signing certificate
and a higher version code.

Choose **View > Languages** to override the device language.
Existing Paintroid translations supply common tool names and commands; new or
untranslated text appears in English. This is partial translation coverage,
not a claim that every selectable language has a fully translated interface.
English (International) is directly below device language; the other choices
are sorted by language code. Thirty requested language/script names are offered
without translations yet. See [the language catalogue notes](translations/README.md).

## Building

GitHub publishes the APK/source artifact before emulator checks finish.
Regression/lint results are independent; routine runs test API 35 and the full
API 30/35 matrix is selectable manually. See [CI.md](CI.md) for the workflow,
timeouts and development-build versus verified-release status.

Install JDK 17, Android SDK Platform 35, Build-Tools 35.0.0,
NDK 27.2.12479018 and CMake 3.22.1. Set `JAVA_HOME`
and `ANDROID_HOME`, then run:

```sh
./gradlew --no-daemon --max-workers=1 :app:assembleDebug
./gradlew --no-daemon --max-workers=1 :Paintroid:testDebugUnitTest :app:lintDebug
```

The APK is `app/build/outputs/apk/debug/app-debug.apk`. The first build requires
network access to Google Maven, Maven Central, the Gradle Plugin Portal and
GitHub and download.osgeo.org for pinned native codec sources (JPEG XL, WebP,
HEIF/HEVC, AV1 and TIFF/JPEG dependencies). Exported corresponding source also includes those native sources
offline. The native codecs
build for arm64-v8a, armeabi-v7a, x86_64 and x86; `-PnativeAbis=x86_64` is available
for a faster emulator-only verification build. Android instrumentation tests run
the actual codecs via `:Paintroid:connectedDebugAndroidTest`; installed-app tests
run via `:app:connectedDebugAndroidTest`.
The APK includes its corresponding source, exportable from File > About / licences / credits.

See [LOCAL_BUILD.md](LOCAL_BUILD.md) for detailed build and packaging instructions,
[CHANGES_FROM_UPSTREAM.md](CHANGES_FROM_UPSTREAM.md) for the changes, and
[UPSTREAM_README.md](UPSTREAM_README.md) for the unmodified upstream README.
The upstream issue tracker describes the original project; AN Paint changes
are independently maintained.

## Licences and artwork

- Application and original paintbrush launcher: [GNU AGPL-3.0-or-later](LICENSE).
  Original code: Copyright © 2010–2022 The Catrobat Team and contributors;
  AN Paint modifications and launcher: Copyright © 2026 AN Paint contributors.
- Tool/action icons: KDE Breeze, LGPL-3.0-or-later. Original SVGs, revision,
  notices and generation details are in [artwork/breeze](artwork/breeze).
- The launcher source is [artwork/an-paint/launcher.svg](artwork/an-paint/launcher.svg).
- Bundled fonts: SIL Open Font License 1.1, with individual authors and full
  terms in [font notices](Paintroid/src/main/assets/legal/FONT_NOTICES.txt).
- [Asset credits](Paintroid/src/main/assets/legal/ASSET_CREDITS.txt) and
  [third-party notices](Paintroid/src/main/assets/legal/THIRD_PARTY_NOTICES.txt)
  identify the artwork and packaged libraries.
- [JPEG XL codec notices](Paintroid/src/main/assets/legal/JPEG_XL_NOTICES.txt)
  and [WebP](Paintroid/src/main/assets/legal/WEBP_NOTICES.txt) /
  [HEIC–AVIF](Paintroid/src/main/assets/legal/HEIF_AVIF_NOTICES.txt) /
  [TIFF](Paintroid/src/main/assets/legal/TIFF_NOTICES.txt) notices preserve
  the upstream licences and patent grants. Gallery artwork retains its
  CC BY-SA 4.0 attribution and source links; the gallery provides copyable credit
  text and editing controls for accurately describing later modifications.

No signing keys or private build backups belong in the public repository.
