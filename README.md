# AN Paint

> **Unfinished local.16 development snapshot.** The APK builds and all 154 regression tests pass, but one JPEG XL emulator test fails. See [HANDOFF.md](HANDOFF.md) for the known defect, completed work and next tasks, including the Dubai/STC font licence investigation.

AN Paint is an independently maintained Android image editor derived from
[Catrobat's Pocket Paint (Paintroid)](https://github.com/Catrobat/Paintroid),
based on tag `v2.14.1`, commit `853ce3c346910ea73aa4de5514f2a76ace1396fb`.
Original Catrobat copyright and licence notices are retained.

The application ID is **`io.github.c933103.anpaint`** and the launcher uses a
Pale Violet AN monogram. Android 5.0 (API 21) or newer is required.

## Editing

- Touch drawing, shapes, text, fill, free-form and rectangular selections.
- Corner and edge resize handles, a rotation handle and an aspect-ratio lock.
- Pinch zoom and pan, centred 100% zoom controls, and Fit view.
- Pixel/percentage sizing, touch canvas trimming and expansion, and disk-backed undo.
- Autosave and draft recovery, a compact collapsible toolbox, and advanced colour controls.
- A separate assembly workspace for up to 20 images, with cropping, normalization,
  alignment, direct PNG saving and transfer to the main editor.
- Watercolor, Heart/Star/Arrow, cursor drawing, magnified preview and sizes up to
  100 px with exact numeric entry.
- PNG, adjustable-quality JPEG, lossless/lossy JPEG XL, and Save and share.
- Four recent colours and an optional online Catrobat figures gallery.

The original editor, layers, transparency controls, Smudge, automatic crop and
native project formats have been removed. See [EDITOR_PARITY.md](EDITOR_PARITY.md)
for the audited feature mapping. The current UI uses Android translation
resources; see [TRANSLATING.md](TRANSLATING.md).

Both editing workspaces produce opaque images. Large imports receive a memory-based
size check and an explicit resize choice; files are not silently downsized.

## Installing this version

`2.14.1-local.16` updates local.15 using the same application ID and signing key.
Version local.15 introduced this package identity. It installs alongside both the
original Pocket Paint and earlier AN Paint builds (`app.paint.local`).
To transfer your current image, **save it as PNG in the old app, then open it in
the new app**. The image transfers; private autosave history, clipboard and
preferences remain in the old installation. Keep the old app until any work
you need has been saved. Later updates to this package must use the same
signing certificate and a higher version code.

## Building

Install JDK 17, Android SDK Platform 35, Build-Tools 35.0.0,
NDK 27.2.12479018 and CMake 3.22.1. Set `JAVA_HOME`
and `ANDROID_HOME`, then run:

```sh
./gradlew --no-daemon --max-workers=1 :app:assembleDebug
./gradlew --no-daemon --max-workers=1 :Paintroid:testDebugUnitTest :app:lintDebug
```

The APK is `app/build/outputs/apk/debug/app-debug.apk`. The first build requires
network access to Google Maven, Maven Central, the Gradle Plugin Portal and
GitHub for pinned JPEG XL/Brotli/Highway/skcms source revisions. The native codec
builds for arm64-v8a, armeabi-v7a, x86_64 and x86; `-PnativeAbis=x86_64` is available
for a faster emulator-only verification build. Android instrumentation tests run
the actual JPEG XL codec via `:Paintroid:connectedDebugAndroidTest`.
The APK includes its corresponding source, exportable from Help.

See [LOCAL_BUILD.md](LOCAL_BUILD.md) for detailed build and packaging instructions,
[CHANGES_FROM_UPSTREAM.md](CHANGES_FROM_UPSTREAM.md) for the changes, and
[UPSTREAM_README.md](UPSTREAM_README.md) for the unmodified upstream README.
The upstream issue tracker describes the original project; AN Paint changes
are independently maintained.

## Licences and artwork

- Application and new AN launcher: [GNU AGPL-3.0-or-later](LICENSE).
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
  preserve the upstream licences and patent grant. Gallery artwork retains its
  CC BY-SA 4.0 attribution and source links.

No signing keys or private build backups belong in the public repository.
