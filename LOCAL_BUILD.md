# AN Paint

An installable Android image editor built from Catrobat's Pocket Paint
(Paintroid), release tag `v2.14.1`, with a separate application identity and
a new classic workspace, build changes and image-import fixes. Earlier local versions were named Pocket Paint Local. This is a local derivative, not an official
Catrobat release.

## Use

The launcher opens the main Paint workspace. An arrow on the left directly
below the toolbar hides or restores the entire sidebar: up collapses it, down
expands it. The arrow remains accessible when the sidebar is hidden. Its
tools/options scroll independently of the compact FG/BG colour indicator
pinned at the bottom. The indicator has an arrow on its right edge: left
collapses the full pinned palette, right expands it. The palette opens directly
to the indicator's right, with matching top and bottom edges. Closing it gives
the canvas more height while the indicator stays fixed. Tapping the box also
toggles the palette. Both panels start expanded on first launch of this layout
(including upgrades); subsequent choices persist. Hiding the sidebar also hides an expanded
palette; restoring it restores the chosen palette state.

Portrait has the title/actions and six menu buttons. Landscape uses one 48 dp
header with the filename centred, a Menu button for File/Edit/View/Image/Colors/
Help, and Undo/Redo/Save. All six groups are native submenus with visible
submenu indicators. Rotation preserves the document, selection, tool and
pending geometry. Undo grays out when there is nothing to undo. Cut/Copy and
Paste/Select all remain two rows below How to use.

The 16 tool positions are free-form selection, rectangular selection, eraser,
bucket, eyedropper, Navigate, pencil, brush, airbrush, text, line, curve,
rectangle, polygon, ellipse and rounded rectangle. Navigate replaces Magnifier:
one finger pans without drawing; two fingers pan and pinch to zoom. Tap Navigate
again or Draw again to return to the previous drawing tool. Two-finger navigation
also works in drawing tools; cancelling the first finger's stroke preserves
pixels and existing Redo. The bottom-right slider and View's Fit/100% commands
also control zoom.

Tap palette colours for foreground; hold for background. FG/BG opens Palette,
Honeycomb and Advanced, with Spectrum/Wheel, RGB/HSV/HSL and #RRGGBB fields.
Opacity controls and eight-digit colour input are removed from the main editor.
Drawing colours and its canvas are opaque. Transparent imported pixels are
composited onto the selected BG colour; original provider files are unchanged.
The separate assembly/retained layer editors keep their own image handling.
Custom slots default to Pale Violet #5B67FF, Gold #FFD700, Silver #C0C0C0 and
Copper #B87333. Existing user colours are preserved. Long-press a slot to replace
it; Add to custom colours starts after the four defaults for a new installation.

Autosave writes a private draft after 1.5 seconds without another editing or
viewport action, and when leaving the app. It streams PNG pixels plus matching
metadata into one atomic file; a failed/interrupted replacement keeps the last
complete draft. Editing is briefly locked during encoding so a draft cannot
contain mixed generations of pixels. Busy edits are followed by a queued save.
The status reports Draft saved or an autosave error. Reopening restores pixels,
filename/dirty state, drawing settings, viewport, floating selection and pending
polygon/curve/canvas-bound geometry. Autosave does not commit unfinished shapes.
A non-floating selection outline and undo history are session state. The older
recovery PNG is migrated after a successful draft write. Save/Save as still
exports to a user-chosen file; a filename star tracks changes to that export.
If a draft cannot reopen, it is preserved separately before a new draft can be
saved. File > Export recovery copy saves its ZIP; extract canvas.png to load it
with the normal resize choices. If preservation fails, autosave pauses to
protect the old draft and manual Save remains available.

Text offers nine Android system-family choices and ten unmodified bundled fonts:
Lato, Alegreya Sans, Bree Serif, Anton, Bangers, Patrick Hand, Sacramento,
Sawarabi Gothic, Sawarabi Mincho and Anonymous Pro. Each dropdown name uses its
own typeface. A live preview follows font, size, bold, italic, underline,
strikethrough, alignment, 50–300% line spacing and the optional BG text box.
Font size is 1–1024 pixels; a large preview is scaled to fit the dialog. The
system families and script fallbacks depend on the device. Original copyright
notices and complete OFL-1.1 terms are in Help > Font licences, the source and
third-party notices; source URLs and hashes are in fonts/inventory.json.

Select all, also available as Ctrl+A on a keyboard, selects the full image for
touch movement. Canvas bounds provides eight handles: drag inward to trim or
outward to expand on any side, then Apply bounds. BG fills new areas without
scaling existing pixels. Cancel and Undo remain available. New, Resize image,
Canvas size and oversized-image dialogs support Pixels/Percent and aspect lock.

File > Load image uses Android's document picker. Images within the dynamic
memory budget load at original resolution. Larger inputs show dimensions,
exact pixel count and decoded/working memory estimates before an explicit
resize choice. Source files are never overwritten or automatically downsized.
File also supports Paste from image, PNG/JPEG export and the separate assembly
workspace described below. View opens the retained Pocket Paint layer editor.

Every licence viewer has fixed Copy all, Other terms and Done buttons outside
the scrolling terms. Copy all copies the entire displayed document. Help retains
Catrobat/derivative identification, original notices, icon/artwork credits,
font licences and export of this exact build's complete corresponding source.
No icon font is bundled.

## Identity and source

- App name: AN Paint (formerly Pocket Paint Local)
- Application ID: `io.github.c933103.anpaint`
- Version: `2.14.1-local.15`, code `68`
- Minimum Android API: 21 (Android 5.0); target/compile API: 35
- Upstream: https://github.com/Catrobat/Paintroid
- Upstream tag: `v2.14.1`
- Upstream commit: `853ce3c346910ea73aa4de5514f2a76ace1396fb`
- Download: https://codeload.github.com/Catrobat/Paintroid/zip/refs/tags/v2.14.1
- Download SHA-256: `6b252464a23c7b3803587473b72c79fefd32f3ec55a3590cee1d4b491cf4c762`

Original authorship, credits and notices are retained. The project is licensed
under GNU AGPL version 3 or, at your option, a later version; see `LICENSE`
and individual file notices. The accompanying source archive contains the
corresponding application source and build scripts.

## Local changes — 2026-09-07

See `CHANGES_FROM_UPSTREAM.md` for each version's changes, including the current
AN Paint sizing, touch trimming, image assembly, colour picker, size policy and credits updates. The earlier retained-editor fixes
include the following:

- Give the app a distinct name, package ID and version.
- Remove the old Catrobat emulator Gradle plugin and its JitPack buildscript
  dependency. Keep the upstream emulator task files for reference; ordinary
  Android builds and tests do not need this plugin.
- Pin the Gradle 8.13 distribution checksum.
- Remove the duplicate app-level file provider. The library's `MyProvider`
  remains registered once with the local application ID's authority.
- Fix portrait image aspect-ratio calculation, read image bounds before
  allocating a decoded image, and use 64-bit arithmetic for import memory
  estimation in `FileIO.kt`.
- Hide the store-rating and upstream feedback menu actions for this derivative.
- Handle Android 14+ selected-photo permission grants as well as full photo
  library access, including callbacks with multiple permission results.
  Add regression tests for partial, full and denied photo access.
  Reference: https://developer.android.com/about/versions/14/changes/partial-photo-video-access
- Add host-side Android tests with Robolectric native graphics for bucket
  fill, drawing/erasing, transparency, image import, PNG encoding, undo/redo,
  activity startup and the pipette tool. Update JUnit to 4.13.2 for this suite.
- Identify imported raster images, OpenRaster archives and Catrobat projects
  from their bytes. The previous MIME-based loader incorrectly sent ordinary
  images labeled `application/octet-stream` to project/archive parsers.
- Read each selected provider file into a temporary private copy once and
  remove it after loading. Handle unreadable files and broken saved projects
  without leaving the loader busy or leaking a parsing exception.
- Request scaling before allocating an image that exceeds the memory budget.
  Keep identity-rotated bitmaps valid when Android returns the input bitmap.

## Build

Install JDK 17 and Android SDK Platform 35 / Build-Tools 35.0.0. Set `JAVA_HOME`
and `ANDROID_HOME` to their locations. Dependencies download from the Gradle
Plugin Portal, Google Maven and Maven Central on the first build.

```sh
chmod +x gradlew
./gradlew --no-daemon --max-workers=1 :app:assembleDebug
./gradlew --no-daemon --max-workers=1 :Paintroid:testDebugUnitTest :app:lintDebug
```

The APK is written to `app/build/outputs/apk/debug/app-debug.apk`.
This is a debug-signed build for direct installation. To update an existing
installation of the same application ID without uninstalling it, reuse the same signing key and increment
the version code. This build accepts `-PlocalDebugKeystore=/absolute/path/debug.keystore`
to use the saved key without replacing another project's default debug key. The build backup contains the key used for the delivered APK.
Do not publish that key with the public source archive.

The source archive excludes generated build directories, local SDK paths,
downloaded toolchains and private signing keys. The Gradle wrapper and all
three application modules are included.

The first build passed 270 tests, but did not exercise the full picker-result
loading path. The loading update adds 14 Android API 33 import checks. They
cover real content-provider URIs, generic and unknown MIME types, PNG/JPEG/WebP,
saved projects, OpenRaster archives, read-access errors, low-memory scaling,
temporary-file cleanup, and a picker result reaching the editor canvas.

Before the fix, three of the first six new checks failed. All 14 targeted
import checks pass after the fix. See the delivered build backup's verification
report for the final full-suite count and APK/lint checks. No physical phone or
full Android emulator was available, and the user's failing image was not
provided for reproduction.

## Current validation and source packaging

ClassicWorkspaceTest exercises actual view clicks and outgoing picker intents
with denied media permission on APIs 28 and 33, provider results, save/cancel/
error handling, all pictured tool controls, rendered pixels, selections, text,
curves, polygon closure, undo/redo and offline licences/source. PickerLaunchTest
checks the retained editor's Open menu without photo permission. Portrait and
landscape renders are generated from the actual Android view hierarchy.

The full-resolution checks load and export a 1644 × 3840 image without losing
one-pixel detail, exercise drawing and same-bitmap undo/redo, fill a 4000 × 3000
canvas with a protected enclosed region, and open a 17 × 10000 image. They also
exercise the top Undo/Redo controls, the Cut/Copy/Paste buttons and their order
below How to use for all 16 tools, plus canvas creation and resizing beyond the
previous caps. FullResolutionStorageTest checks exact translucent-pixel history,
damaged/unwritable undo storage and flood fill against an independent reference.

These are Robolectric host-side Android runtime tests. They do not constitute
installation on a physical phone or exercise a manufacturer's system picker UI.
The earlier .2 tests only injected a picker result; they did not test the button
that should open the picker. The current checks cover that missing entry point.

The Gradle preBuild task bundles the corresponding project source in the APK,
excluding build output, local.properties, downloaded toolchains and keys. It
includes the wrapper, all modules, legal notices, change report and build scripts.
Help > Export this version's source code saves the bundled ZIP with Android's
Create Document picker. The separately delivered source ZIP is byte-identical
to that APK asset.

If dependency versions change, regenerate the checked-in notice inventory:

```sh
./gradlew :app:writeDependencyInventory
python3 tools/generate_legal_notices.py
```

This reads publisher POMs from the local Gradle cache and preserves the vendor
licence files under legal/vendor plus LICENSE/NOTICE from shipped archives.
The upstream Dubai and STC/GE SS font binaries have been removed because their
embedded copyright/licence metadata did not grant clear app redistribution.
Their legacy serialized font identifiers remain readable using Android system
font substitutes, labelled System sans / System Arabic in the retained editor.

## Whole-bitmap safety policy and resize choices (local.6)

The user selected a sensible architecture-based upper safety limit, rather than
a disk-tiled billion-pixel editor. The old fixed 4 MP limit and silent import
reduction are not restored. No fixed one-billion-pixel cutoff is used.

ImageMemoryPolicy reserves three 4-byte ARGB work buffers per requested pixel
for decode/orientation, transforms and selection compositing, plus the existing
canvas, selection and clipboard, with 32 MiB headroom for UI and other objects.
On Android 8+ its working budget is the smaller of one third of currently
available system memory above Android's low-memory threshold and twice the
app's maximum Java heap allowance, after the headroom reserve. On older Android,
remaining Java heap space is the process budget because bitmap pixels live there.
If platform memory statistics are unavailable, it uses remaining heap headroom.
An individual bitmap is also kept within signed 32-bit allocation accounting.
Exact pixel counts use 64-bit arithmetic. Byte estimates use floating-point
arithmetic so even maximum integer dimensions cannot wrap into negative memory. This is a conservative
admission check, not a guarantee against later OS/native allocation failure.

Import headers are inspected before decoding; creation/resizing, selections,
transforms and other full-bitmap allocations are checked too. Small startup
canvas allocation is retained so an app can open and report a low-memory state.
New/Resize canvas dialogs show the current budget and reject allocations that
do not fit. Oversized file imports, including headers above one billion pixels,
get the explicit resize-choice dialog. A power-of-two sampled decode keeps at
least the requested detail where the format decoder supports it; a single
resampling/orientation pass produces the exact chosen dimensions. The import
estimate is the larger of three final-size ARGB buffers and the sampled decode
plus two final-size buffers, plus the resident canvas/selection/clipboard.
Both the sampled decode and final bitmap must fit Android allocation accounting.
The suggested copy leaves 10% of the calculated working budget free; its size
varies with the source aspect ratio, decoder sampling and device memory. The
user can choose a different size that fits. EXIF rotation/flip and PNG alpha are
preserved; the cached provider copy is removed on success, error, cancellation
or activity destruction. Extremely large or unsupported format decoders may
still fail; the app does not implement full billion-pixel or tiled editing.

ANPaintControlsTest covers the icon actions, slider touch and synchronization,
RGB/HSV/HSL/hex/alpha input, invalid input, cancellation, persistent custom
swatches, honeycomb touch selection, both advanced graphical selectors (including starting at black), asset credits,
oversized-canvas refusal and native UI previews. ImageMemoryPolicyTest checks
variable device budgets, Java-heap versus native-bitmap budgets, zero headroom,
one-billion-pixel and overflow-sized dimensions, and achromatic colour handling.

Platform references for the memory policy:
- [Android bitmap memory](https://developer.android.com/topic/performance/graphics/manage-memory)
  documents the move from Java-heap pixel storage to native-heap pixels at API 26.
- [ActivityManager.MemoryInfo](https://developer.android.com/reference/android/app/ActivityManager.MemoryInfo)
  defines the available-memory and low-memory-threshold fields used by the check.

ImageResizeFlowTest exercises real PNG/JPEG imports under constrained memory,
user-approved exact resizing, original-file preservation and a single provider
read, PNG transparent/semitransparent pixels, rotated photos, non-power-of-two
sizes, thin images, import into a selection on Android 9, invalid dimensions,
changed memory while the dialog is open, and cancellation. The billion-pixel
case tests preflight with a synthetic header, not a successfully edited gigapixel
image. Native view previews include the honeycomb and resize-choice dialog.


## Image assembly and sizing (local.7, updated in local.8)

File > Image assembly or View > Image assembly opens a separate workspace for
up to 20 images. Add images accepts multiple files from Android's document
picker. Each thumbnail in the bottom tray includes its filename, crop dimensions
and available modification time. Sorting supports filename A–Z/Z–A or modified
oldest/newest; unknown times appear last. Modification time is provider metadata,
not an inferred photo capture time. Sorting changes the tray order only.

Tap a thumbnail, then Crop image to adjust its crop by touch or by four edge
amounts in Pixels or Percent. Batch crop applies edge amounts to checked images,
with a preview selector and All/None controls. Percentages are measured separately
against each original image. Reset crop restores the full original. Crops are
reversible metadata and the cached original stays unchanged. A batch that would
remove an entire image or make placed images overlap is rejected as a whole.

Hold and drag a thumbnail onto the workspace. The first image starts at the
origin; later images snap to any placed image's right side, top aligned, or
bottom side, left aligned. Highlighted targets preview valid placements. Tap a
thumbnail and then a + target as an alternative to dragging. Drag an already
placed image directly to move it, with a preview of the snapped position before
release. Empty-space dragging pans and pinching zooms. Show all (formerly Fit)
adjusts zoom to show the composition and available targets; output dimensions
stay unchanged. Overlapping placements and attachment cycles are disallowed.
Cropping a placed image reflows its attached images. Unplace returns only the
selected image to the tray. Images behind it advance into the gap, including
when the first image is unplaced. Remove discards only that input; the remaining
placed images stay in the composition. Undo restores either action.

Same width and Same height normalize all currently loaded images to a common
dimension, keeping each crop's aspect ratio. Choose Pixels or Percent, or use
Smallest/Largest presets. Percent is relative to the largest current dimension
on the chosen axis; the dialog shows that base and the resulting dimensions.
Restore original sizes removes normalization and keeps crops. Scaling remains
reversible metadata: output reads original cropped pixels rather than enlarged
thumbnails. Normalization persists with the assembly project. Placed images
reflow to avoid overlap after a size change.

Assembly has independent Undo/Redo, retaining up to 50 metadata steps for the
session. Its current project and private original copies persist across closing
and reopening. Files needed by the current state or undo/redo stay available;
unused private copies are pruned. The original provider files are never edited.
The assembly and Paint canvas remain separate until Edit in Paint is chosen.

Save PNG exports placed images directly through Android's save picker. Edit in
Paint imports that same composite into the main canvas as an undoable edit;
Undo there restores the previous image. Empty parts of the composition stay
transparent. Export reads the original cropped regions one image at a time,
preserves EXIF orientation and alpha, and never enlarges a thumbnail as output.

The composition preview uses bounded thumbnails, so adding large sources does
not allocate twenty full-resolution bitmaps. Final output is still a whole
bitmap. Its conservative preflight estimate reserves 28 bytes per output pixel
plus resident main-canvas and thumbnail pixels. If it cannot fit the dynamic
memory budget or Android's bitmap accounting, a size-choice dialog displays the
original dimensions, exact pixel count, decoded and estimated working memory,
plus live Pixels/Percent controls and an optional aspect lock. Allocation failure
also offers a smaller output. Cancel does not flatten or replace the canvas.
Region-capable codecs decode only each requested source crop; other codecs use
a guarded sampled full-source fallback. Format and device decoder limitations
still apply. This is not a tiled gigapixel export engine.

SizingAndTrimTest covers pixel/percent conversion, optional aspect locks, invalid
input, exact unit switching, actual touch selection/movement/crop handles,
canvas transparency and undo. AssemblyModelTest covers geometry, parent reflow,
invalid atomic batches, undo, persistence, sorting, the twenty-image cap, and
exact composite/EXIF pixels. AssemblyActivityTest covers the real multi-picker
intent and provider result path, twenty inputs on API 28, thumbnail sorting,
Android drag events, individual/batch crop dialogs, repeated crop handle motion,
PNG saving, cancellation, persistence, and an undoable transfer to Paint.
Portrait/landscape and sizing/crop dialog previews come from Android view renders.

Validation uses Robolectric native graphics on the build host, not a physical
phone or full emulator. Robolectric's stock BitmapRegionDecoder shadow returns
blank buffers. PixelRegionDecoderShadow is a test-only adapter that decodes the
small fixtures with native BitmapFactory and independently copies/samples the
requested raw region; production code performs orientation and composition.
These pixel tests validate the composition and crop logic but do not exercise a
physical Android device's native region decoder or manufacturer picker UI.

Platform references:
- [Multiple document selection](https://developer.android.com/reference/android/content/Intent#EXTRA_ALLOW_MULTIPLE)
- [Document modification timestamps](https://developer.android.com/reference/android/provider/DocumentsContract.Document#COLUMN_LAST_MODIFIED)
- [Bitmap region decoding](https://developer.android.com/reference/android/graphics/BitmapRegionDecoder)


## Canvas expansion, action layout and assembly refinement (local.8)

The existing touch crop handles now also expand the main canvas beyond any
original edge. Newly exposed space uses the background colour, including its
alpha, and original pixels are copied without resampling. Source-image crop
previews in assembly stay bounded to their original images. Canvas bounds use
64-bit intermediate arithmetic; invalid/overflow dimensions and allocations
above the existing device budget are rejected before changing the document.
A no-op bounds confirmation adds no undo step.

Undo is enabled only when committed history or cancellable pending geometry
exists. Cancelling a pending curve, polygon or changed canvas boundary does not
consume committed history. Merely opening the bounds tool or selecting an area
does not enable Undo on an untouched image. Undo/Redo in Edit use the same
availability as the toolbar. Cut/Copy and Paste/Select all form two rows of
original vector icons below How to use for each of the sixteen tools.

This update adds native Android host checks for expansion on every side,
source and new-area alpha, exact PNG round-trip pixels, cancellation, no-op
history, memory rejection, integer overflow and Undo availability across
history, new documents and unfinished shapes. The toolbox layout regression
checks both rows and action order for all sixteen tools. New previews show
expanded bounds and the two-column edit controls.

Assembly regression checks cover common width/height in pixels and percent,
aspect ratios, normalized PNG/alpha pixels, unchanged source files, project
persistence and Undo. They also cover unplacing/removing one image in straight
and branched layouts, filling the gap, moving the first image after its former
successors, direct touch dragging, a visible snap preview and gesture cancellation.
The Show all button is checked to leave output dimensions unchanged. Two new
native view renders show the normalization dialog and direct-drag preview.


## Autosave, compact controls and fonts (local.9)

WorkspaceRefinementTest exercises autosave without leaving the activity,
restart recovery of pixels/settings and unfinished work, atomic failure,
pre-decode memory checks, leaving during background edits, gesture cancellation
with preserved Redo, panel geometry, landscape menu access/filename centring,
fixed licence actions and exact clipboard text, each bundled font, native font
preview/formatting, named colour defaults and opaque main-editor imports.
Earlier image loading, resizing, assembly, drawing, licence and storage tests
remain part of the full suite. Final counts, lint, APK signing/alignment and
source/runtime consistency checks are in the build backup. Tests use native
Robolectric graphics on the build host; no physical device is claimed.

## Panel arrows and landscape submenus (local.10)

Move the sidebar toggle out of the title bar to a 48 dp control at the left
under the toolbar. It reverses between up/collapse and down/expand. Keep it
accessible after hiding the entire sidebar, without adding a full-width row
above the canvas. Add a distinct left/right arrow area to the right of the
current colour box. Both panels default to expanded once for the new layout,
then preserve user choices. Use native Android submenus for all six landscape
Menu categories; commands and Undo/Redo availability use the same definitions
as the portrait menus. Existing layout regressions check these behaviours.

## Palette opens beside the indicator (local.11)

Place the palette at the bottom of the canvas column, directly to the right of
the pinned FG/BG indicator. Both occupy the same 80 dp row. The palette no
longer adds a second row below the sidebar. Toggling it leaves the indicator
fixed and gives the canvas back the released height. The entire sidebar and
palette still hide together, and remembered panel choices remain in effect.

The existing native layout checks now assert matching top/bottom edges,
right-edge adjacency and a stationary indicator through collapse/expand in
portrait and landscape. Native view previews show the resulting layout.

## Copyleft icons (local.12)

The complete set of 29 added tool/action/navigation/panel/assembly glyphs now
uses KDE Breeze Icons (LGPL-3.0-or-later), replacing the earlier drawn icons.
Original SVG files, copyright, exact revision, aliases and hashes are in
`artwork/breeze`; full licence texts are also under Help > Icon licences.
The application code remains AGPL-3.0-or-later. The inherited Catrobat launcher
and retained editor assets keep their existing notices.

To regenerate the checked-in Android PNG resources from the unchanged SVGs:

```sh
python3 -m pip install CairoSVG==2.8.2
python3 tools/generate_breeze_icons.py
```

CairoSVG is used only on the build computer for optional asset regeneration;
it is not included in the APK. Normal Gradle builds need no additional library.
Density-specific PNGs preserve SVG dashed strokes and avoid runtime SVG parsing.
To use modified artwork, replace the corresponding SVG, update its manifest hash,
regenerate the PNGs, then rebuild as above. You can sign that APK with your own
key and install it; to update an existing install, use its original signing key.

## Credit descriptions (local.13)

About and the asset-credits page identify the projects and assets included in
AN Paint. Reference-design and trademark disclaimers unrelated to bundled
components have been removed, with neutral descriptions of the workspace in
source comments and documentation. All actual licence texts and copyright
notices remain intact. This release changes descriptive text and version
metadata only; colours, layouts and editing behaviour are unchanged.

## Drawing and selection controls (local.14)

Polygon closes on a double-tap of its final vertex after at least three vertices;
Finish polygon remains available. A repeated slow tap adds a vertex. Navigation
and cancelled touch gestures reset double-tap recognition.

Rounded rectangle uses the Radius (px) slider. The selected value is an image-pixel
radius, limited by half the shorter side of the shape being drawn. The slider
range follows the canvas dimensions; the setting is included in autosave.

ZoomSeekBar marks 100% at its centre. Each half uses logarithmic scaling. Zoom
in/out buttons and menu commands stop at 100% when a step would cross it, and a
subsequent press continues. The adjacent Fit button fits the canvas in the view.
Pinch zoom remains continuous.

Rectangle, lasso, Select all and pasted selections expose four corner grips for
resizing and a round grip for rotation. Lock proportions is on by default and
can be switched off. The opposite corner stays fixed during resizing, including
after rotation. The sidebar shows image-pixel dimensions and angle. A floating
selection retains its original bitmap until rendering, avoiding repeated
resampling as its handles move. Commit combines the selection transaction into
an undoable canvas edit. Undo before Commit captures the visible transformed
result for Redo. Copy/Cut and Crop to selection render the transformed bounds,
subject to the existing device memory check.

Cancelling a touch gesture or starting two-finger navigation restores the
selection bounds, angle and source pixels from before that gesture. Autosave
retains floating selection scale/position/rotation and the aspect-lock choice;
older drafts default to zero rotation and locked proportions. All control code
is AGPL-3.0-or-later; KDE Breeze artwork remains under LGPL-3.0-or-later.

## Edge transforms and separate identity (local.15)

Selections now expose four edge-midpoint grips in addition to the corner and
rotation grips. With Lock proportions off, an edge changes only its own axis;
with it on, both dimensions follow the original ratio. The opposite midpoint
stays fixed, including when the selection is rotated. Free-form selections
retain their masked shape and visible outline within the transform box. The
source bitmap remains unchanged during adjustments, and autosave preserves
both the exact floating pixels and a compact display outline.

The application and app-module namespace are `io.github.c933103.anpaint`.
Provider authorities follow the application ID. The retained library's source
namespace remains `org.catrobat.paintroid` to preserve upstream structure.
The installed launcher uses original AN Paint geometric artwork, with legacy,
round, adaptive and themed variants and AGPL-3.0-or-later credit in Help.

This identity installs separately from builds through local.14. Save current
work as PNG in the old app, then load it in the new app. PNG transfers the
image; the old app retains its autosave, clipboard and preferences. The new
identity's future updates must use its signing key. Never publish private
signing material or the build backup to GitHub.
