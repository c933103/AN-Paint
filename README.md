# AN Paint

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
- The original Pocket Paint editor, including layers, remains under View.

The main workspace uses an opaque canvas. Large imports receive a memory-based
size check and an explicit resize choice; files are not silently downsized.

## Installing this version

`2.14.1-local.15` starts a new package identity. It installs alongside both the
original Pocket Paint and earlier AN Paint builds (`app.paint.local`).
To transfer your current image, **save it as PNG in the old app, then open it in
the new app**. The image transfers; private autosave history, clipboard and
preferences remain in the old installation. Keep the old app until any work
you need has been saved. Later updates to this package must use the same
signing certificate and a higher version code.

## Building

Install JDK 17, Android SDK Platform 35 and Build-Tools 35.0.0. Set `JAVA_HOME`
and `ANDROID_HOME`, then run:

```sh
./gradlew --no-daemon --max-workers=1 :app:assembleDebug
./gradlew --no-daemon --max-workers=1 :Paintroid:testDebugUnitTest :app:lintDebug
```

The APK is `app/build/outputs/apk/debug/app-debug.apk`. The first build requires
network access to Google Maven, Maven Central and the Gradle Plugin Portal.
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
  identify inherited artwork and the packaged libraries.

No signing keys or private build backups belong in the public repository.
