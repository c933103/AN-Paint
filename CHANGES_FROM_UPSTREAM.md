# local.16 — 10 September 2026

- Consolidate standalone editing in the new workspace; delete the original editor,
  its layer/transparency/Smudge/project-format code, obsolete tests/resources and
  unused dependencies. Keep original Catrobat attribution and source history.
- Add Watercolor and Heart/Star/Arrow using four additional KDE Breeze icons;
  preserve all 33 original SVGs, licence notices and Android conversion details.
- Add cursor drawing, adjustable magnified preview, antialiasing and smoothing;
  Fit centres the canvas. Preserve connected lines with open-polygon drawing.
- Increase tool sizes to 100 px and provide tappable numbers for exact entry.
- Add four distinct recent colours at the far right of the palette.
- Rename File insertion to Insert image into canvas; place the optional online
  Catrobat gallery directly below it, with retained source/attribution links.
- Add adjustable-quality JPEG, JPEG XL import/crop/export via pinned libjxl 0.12.0,
  and Save and share after successful export. All document outputs are opaque.
- Extract interface text into Android string resources with stable routing and
  persistence IDs; add locale-aware decimal entry and translation instructions.
- Replace obsolete legacy-font tests with checks against the actual current font
  inventory. The Dubai/STC fallback explanation is in EDITOR_PARITY.md.
- Build and test in GitHub Actions, including real Android JPEG XL codec tests.
  Signing remains local with the existing private key; no key is uploaded.

Earlier change history follows; its feature counts and checks describe those
historical versions.

# Changes from the base repository

Base: [Catrobat/Paintroid](https://github.com/Catrobat/Paintroid), tag `v2.14.1`,
commit `853ce3c346910ea73aa4de5514f2a76ace1396fb`.

## First delivered build: 2.14.1-local.1

The brush, eraser, color palette, eyedropper, bucket fill, shapes, text, crop,
layers, undo/redo, and import/export features came from Pocket Paint. I did not
create those editing tools. The first build made these changes:

| Area | Exact changes | Files |
| --- | --- | --- |
| App identity | Use `Pocket Paint Local` and `app.paint.local`; set version name `2.14.1-local.1`. Version code remained 54. Sign the debug APK with the saved development key. | `app/build.gradle`, root `build.gradle`; signing key stored separately |
| Build setup | Remove `com.github.Catrobat:Gradle:1.6.2`, its JitPack repository, the `org.catrobat.gradle.androidemulators` plugin, emulator configuration, and the application of the legacy ADB/emulator task scripts. Pin the existing Gradle 8.13 distribution checksum. | Root `build.gradle`, `Paintroid/build.gradle`, `gradle/wrapper/gradle-wrapper.properties` |
| File sharing | Remove the duplicate app-level `FileProvider`; keep the library's `MyProvider` and its application-specific authority. | `app/src/main/AndroidManifest.xml` |
| Image scaling | Fix integer division in portrait aspect-ratio calculation, read image bounds before calculating scaling, and promote the first dimension to 64-bit before multiplying dimensions for the memory estimate. | `Paintroid/src/main/java/org/catrobat/paintroid/FileIO.kt` |
| Photo permission | Declare and handle Android 14 selected-photo access alongside full photo access, handle multiple permission results, and cap legacy read permission at API 32. | `Paintroid/src/main/AndroidManifest.xml`, `.../presenter/MainActivityPresenter.kt` |
| Menu | Hide the Rate Us and Feedback menu entries for the separate build. | `Paintroid/src/main/res/menu/menu_pocketpaint_more_options.xml` |
| Tests | Add 10 native graphics/activity tests and three permission-result regression tests; add Robolectric 4.14.1, include Android resources in unit tests, update JUnit to 4.13.2, and configure the test JVM. The remaining 257 tests were inherited. | `Paintroid/build.gradle`, `.../local/EditorBehaviorTest.kt`, `.../test/presenter/MainActivityPresenterTest.kt` |
| Documentation | Add the complete AGPL license text, local build instructions, provenance, and dated modification notices; retain upstream credits. | `LICENSE`, `LOCAL_BUILD.md`, `README.md`, comments in modified files |

The first build retained the upstream Android SDK levels, Android Gradle plugin
version and Kotlin version. It did not redesign the UI or add new drawing tools.

## Image-loading repair: 2.14.1-local.2

The user reported that images failed to load in both the official distribution
and the first local build. I reproduced a defect in the unchanged upstream
`LoadImage.kt` path using Android 13/API 33 runtime tests with a document provider:

| Input | Before the repair |
| --- | --- |
| PNG reported as `image/png` | Passed |
| JPEG reported as `image/jpeg` | Passed |
| PNG reported as `application/octet-stream` | Returned a load failure after being treated as a project/archive |
| JPEG reported as `application/octet-stream` | Uncaught `KryoBufferUnderflowException` from the project parser |
| WebP reported as `application/octet-stream` | Returned a load failure after being treated as a project/archive |
| Extensionless PNG with no reported MIME type | Passed |

This proves a shared code defect. It does not establish the MIME type, format,
or cause of failure for the user's particular image, which was not attached.

The repair changes:

- `.../iotasks/LoadImage.kt`: detect Catrobat and ZIP headers from actual bytes;
  otherwise use the image decoder. Provider MIME labels and filename extensions
  no longer select the project parser. Read a provider URI once into a private
  temporary file, delete it in `finally`, handle denied reads and malformed
  projects, and release the loading counter on all coroutine exit paths.
- `FileIO.kt`: return a scale request before allocating an oversized image;
  recycle an orientation input only when the transform returned a different
  bitmap.
- `.../local/ImageLoadingTest.kt`: add 14 import checks. Include a result from
  a document provider reaching the real activity's editor canvas, valid image
  decoding under generic MIME labels, saved-project/OpenRaster compatibility,
  single provider reads, failures and cleanup, and low-memory behavior.
- Root `build.gradle`: increment version code to 55 and version name to
  `2.14.1-local.2`. The application ID and signing key are retained, allowing
  installation as an update over the first local build.

All 14 targeted import checks pass after this repair. The final full-suite
results, signature checks and lint report are included in the build backup.
These are host-side Android runtime checks; a physical phone and the user's
failing image were not available for testing.

## Picker, classic workspace and credits: 2.14.1-local.3

The user clarified that pressing Load Image did not even invoke a picker. The
.2 decoder repair addressed a separate verified defect; it did not fix the
permission gate ahead of the picker. This version addresses that entry point.

| Area | Changes in this version |
| --- | --- |
| Open/Import in retained editor | Bypass broad media permission requests for user-selected files; preserve the save-before-replace dialogue. Launch ACTION_OPEN_DOCUMENT with CATEGORY_OPENABLE and a read grant. Remove FLAG_ACTIVITY_NEW_DOCUMENT. |
| Launcher | Open the new native ClassicPaintActivity. The original MainActivity remains accessible under View for layers, additional tools, Catrobat projects and OpenRaster. |
| Classic layout | Six named menus, permanent two-column toolbox, contextual options, white canvas, draggable scrollbars, FG/BG swatches, 28-colour two-row palette, status, Undo/Redo/Apply and a prominent Load image button. Toolbox and palette scroll on smaller screens. This version introduced locally drawn vector icons, replaced by KDE Breeze in local.12. |
| Raster editing | New PaintDocument and PaintCanvas implement the 16 pictured tools. They reuse Catrobat's JavaFillAlgorithm for the bucket. Other classic gestures, selection compositing, curve/polygon construction, shape drawing, viewport and raster history are new local code. |
| Selections | Rectangular/free-form masks, movement, cut/copy/paste, delete, select-all, crop and opaque/transparent modes. Clipboard is local to this workspace. |
| Tools/options | One-pixel pencil; round/square/calligraphy brushes; background-colour eraser; tolerance bucket; eyedropper; magnifier/pan/pinch/grid; airbrush; multiline text with size/family/bold/italic/background; line; two-control-point cubic curve; rectangle/polygon/ellipse/rounded rectangle with outline/fill/fill-and-outline. |
| Menus | New/open/import, PNG/JPEG save, edit actions, zoom, pixel grid, crop/resize/canvas size, flip/rotate/invert/clear, custom RGB/alpha/hex foreground/background colours, swap/reset and help. |
| Classic file flow | Direct document picker without broad storage/media access; GET_CONTENT fallback if no OPEN_DOCUMENT handler; explicit errors for missing picker, denied providers, unsupported/corrupt files and failed saves. Read a provider once, decode bytes, apply EXIF transforms, bound allocation, remove temporary files. Loading errors and cancellation preserve the current canvas. |
| Recovery and limits | Private recovery PNG on leaving; bounded 48 MiB undo snapshots. Classic images limited to 4,194,304 pixels / 8192 per side; larger imports downsample with a message. Classic and retained editor documents are separate. |
| Copyright/licensing | Help and retained About identify the modified distribution, date, original repository/tag/commit, Catrobat authorship, AGPL-3.0-or-later and no warranty. Full AGPL and notices for 59 resolved runtime components available offline. Third-party licence texts and packaged notices preserved. |
| Fonts | Remove the two upstream Dubai/STC font binaries: Dubai's embedded text restricts use, while STC/GE SS carries Boutros copyright without a redistribution grant. Replace both with Android system typefaces and rename their labels; retain enum identifiers for old project compatibility. Adjust the related instrumented-test expectations. |
| Corresponding source | A Gradle preBuild Zip task embeds the full current project source and build scripts in the APK, excluding keys and build output. Help exports this ZIP offline. The separately delivered source archive is that same asset. |
| Upgrade | Version 2.14.1-local.3, code 56. Keep app.paint.local and the existing signing certificate so it installs as an update to previous local builds. |

The custom workspace lives in `Paintroid/src/main/java/org/catrobat/paintroid/classic/`.
Other modified areas are the two manifests, presenter/navigator, AboutDialog,
font consumers and translated labels, Gradle build files, tests and documentation.
The backup contains the complete source diff for file-by-file review.

The pictured tools map directly to the left toolbox in this order:

| Row | Left | Right |
| --- | --- | --- |
| 1 | Free-form selection | Rectangular selection |
| 2 | Eraser | Bucket fill |
| 3 | Eyedropper | Magnifier |
| 4 | Pencil | Brush |
| 5 | Airbrush | Text |
| 6 | Line | Curve |
| 7 | Rectangle | Polygon |
| 8 | Ellipse | Rounded rectangle |

Validation includes actual Load button and File menu actions, outgoing Android
picker intents with denied media permissions, provider results reaching pixels,
PNG saving, save failure, cancellation, all tool controls and raster effects,
selection movement/transparency, text, curves, polygons, undo/redo, legal/source
assets and portrait/landscape view renders. Final totals and reports are in the
backup. Tests run in Robolectric's Android runtime; no physical device or full
system picker UI was available. The user's failing image was not supplied.

## Full resolution and toolbar update: 2.14.1-local.4

The user requested removal of the image limit, top-row Undo/Redo in place of
Load image, and Cut/Copy/Paste below How to use.

| Area | Changes in this version |
| --- | --- |
| Original resolution | Remove the classic workspace's 4,194,304-pixel, 8192-per-side and 256 MiB input-file limits. Decode with sample size 1 and scaling disabled. New canvases and image/canvas resizing also accept dimensions beyond the previous limits. No automatic reduction or reduction dialogue remains. |
| Undo memory | Replace RAM bitmap snapshots with lossless, compressed private disk snapshots in RasterHistory. Transfer pixels in small row segments and restore same-size edits into the existing bitmap. Validate the compressed snapshot before restoring. Keep a 256 MiB history budget with at least one complete step; this budget controls stored undo steps, not image dimensions. |
| Bucket memory | Replace the classic workspace's use of JavaFillAlgorithm with a new local scanline fill. Use a 256 KiB pixel cache, visited bitset and primitive scanline stack; run the operation on a worker while editing is locked. The retained original editor still includes Catrobat's JavaFillAlgorithm, which is credited accordingly. |
| Save/import/recovery | Stream PNG export and private recovery without another full canvas copy. File import transfers ownership of the decoded image to the selection. Show errors on memory/storage failure and avoid unlocking editing while another file operation is queued. JPEG flattening, transforms and selections can still require additional memory. |
| Header | Remove Load image from the top row. Put Undo, Redo and Save there, and remove the duplicate bottom Undo/Redo controls. Load image remains in File. |
| Left panel | Put Cut, Copy and Paste directly below How to use for every tool. These buttons use the same actions as Edit. Retain all 16 tools, their options, the palette, menus and Apply. |
| Credits/source | Preserve the Catrobat credits, AGPL text, third-party notices and offline corresponding-source export. Update bucket provenance and include this version's new source and change notes. |
| Upgrade | Version 2.14.1-local.4, code 57. Keep app.paint.local and the existing signing certificate. |

There is no artificial resolution ceiling in the classic workspace. The image
and requested operation must still fit the phone's memory and storage; a failed
allocation reports an error instead of silently reducing the image. Large
undo snapshots can take longer to write. The retained original editor remains
a separate workspace with its own upstream memory handling.

Eleven added regression checks cover the new controls, full-resolution
1644 × 3840 loading/drawing/undo/redo/PNG export with exact pixel assertions,
17 × 10000 loading, 12-megapixel fill with a protected enclosure, larger new/
resized canvases, lossless translucent-pixel snapshots, damaged/unwritable
history and scanline fill compared with an independent reference algorithm.
The backup records the final complete suite and APK/lint checks. These are
host-side Robolectric tests; no physical phone was available for validation.


## AN Paint controls, colours and safety policy: 2.14.1-local.5

The user requested the AN Paint name, icon edit controls, bottom-right zoom,
advanced colour selection and explicit visual-asset credits. They clarified that
extremely large images should have a sensible safety limit based on app design;
a billion-pixel tiled engine was not requested.

| Area | Changes in this version |
| --- | --- |
| Name/update | Rename the launcher label, classic workspace and About to AN Paint. Retain app.paint.local and the signing key. Version 2.14.1-local.5, code 58. Historical upstream/product names remain in credits and change history. |
| Actions | Use newly drawn, single vector icons for Undo, Redo, Cut, Copy and Paste. Preserve their existing actions, positions, accessible names and long-press labels. The icons do not use an icon font. |
| Apply/zoom | Replace the permanent bottom-right Apply with a logarithmic zoom slider and minus/plus controls. Synchronize it with pinch/Magnifier/menu zoom. Move selection commit, Finish polygon and Finish curve into the respective left tool options; all 16 tools retain their functionality. |
| Colour selection | Add 48 basic swatches, 16 persistent custom swatches, a classic hue/saturation spectrum with lightness bar, and an HSV wheel with value bar. Add linked RGB, HSV, HSL, alpha and hex input; validation/cancel/foreground/background support; preserve chosen hue/saturation at black for brightness adjustment. |
| Safety limit | Introduce ImageMemoryPolicy based on device memory, the current document/clipboard, three ARGB work buffers, headroom and Android allocation accounting. Check import headers before decoding and guard other bitmap allocations. Reject oversize with the current MP budget, without automatic downsizing. See LOCAL_BUILD.md for the exact policy. |
| Asset credits | Add an offline Icons, fonts & artwork credits page and inventory of 163 retained image/vector/widget resources. Identify the new AN Paint geometry, inherited Catrobat artwork, Android/Material Apache-2.0 assets, and generic device-supplied typefaces. No additional font binaries were bundled in this version. Keep full AGPL and dependency notices. |
| Source | Export AN-Paint-source.zip from Help; embed the corresponding source and current notices in the APK. The public source archive excludes signing keys. |

Tests cover the actual slider and controls, advanced colour input and touch
selection, custom-colour persistence, cancellation/validation, low-memory and
overflow/one-billion-pixel guards, retained image-loading and editing operations,
legal/source assets and native portrait/landscape/colour-dialog renders. Final
counts and signature/alignment/lint reports are in the build backup. Tests use
Robolectric Android runtimes, not a physical device.


## Honeycomb and explicit image downsizing: 2.14.1-local.6

The previous build omitted the requested honeycomb selector and only rejected
oversized imports. This update provides both missing controls.

| Area | Changes in this version |
| --- | --- |
| Colour progression | Palette → Honeycomb → Advanced. Add 127 original chromatic hexagons and a 13-step greyscale row, with per-swatch accessible names and keyboard focus. Keep the spectrum, wheel, saved swatches and RGB/HSV/HSL/hex controls. |
| Opacity | Label alpha as Opacity and display it only in Advanced, with its 0–255 scale explained. Transparency remains useful for PNG pixels/backgrounds on a single canvas; no layer system is implied or added. Basic and honeycomb choices are opaque. |
| Resize choice | Inspect import dimensions before decoding. If too large, show original oriented dimensions, exact pixel count, decoded RGBA bytes, estimated full-size editing memory and the current device budget. Offer an aspect-locked smaller copy with live estimates, Resize and load, and Cancel. |
| Loading | Read the provider once; retain the private copy across the choice. Sample before allocating the complete image, then resample and apply EXIF in one pass to the exact chosen dimensions. Account for decoder overhead, retain PNG alpha, recheck memory, and offer a smaller copy after allocation failure. Remove the cached file when finished or cancelled. |
| Existing image | Images that fit still load at full resolution. Cancelling keeps the canvas. Source files are never changed by import downsizing. The whole-bitmap architecture and dynamic safety policy remain; no gigapixel editing claim is made. |
| Credits/source | Credit the new honeycomb geometry alongside the existing icon/colour code; retain Catrobat, platform, font and dependency notices. Include this build's complete source in the APK and source archive. |
| Upgrade | Version 2.14.1-local.6, code 59. Keep app.paint.local and the existing signing certificate. |

Regression checks cover actual honeycomb taps, advanced-only opacity, resize
confirmation/cancellation/validation, reduced PNG/JPEG pixels and transparency,
orientation, thin and non-power-of-two sizes, changed memory budgets, a single
provider read, and unchanged source files. The one-billion-pixel check uses a
synthetic header to test the dialog before allocation. Final test/lint and APK
signature/alignment results are in the backup. No physical phone was available.


## Percentage sizing, touch trim and image assembly: 2.14.1-local.7

Local modifications dated 7 September 2026. This update adds the requested
sizing controls, touch equivalent of Select all and canvas trimming, and a
separate image assembly workflow.

| Area | Changes in this version |
| --- | --- |
| Dimensions | Shared Pixels/Percent controls with optional aspect lock in New, Resize image, Canvas size, oversized import and assembly output dialogs. Preserve exact dimensions when switching units; validate inputs and recalculate memory estimates. |
| Canvas trimming | Add a Select all vector icon beside Cut/Copy/Paste, retain Edit > Select all, and support external-keyboard Ctrl+A. Drag the selected image, then use Trim canvas with eight touch handles and Apply trim/Cancel. Applied trimming is undoable. |
| Pixel preservation | Canvas resizing copies existing alpha exactly and fills only newly exposed areas with the chosen background. Cropping retains exact source pixels. |
| Assembly entry | File and View > Image assembly open a separate native workspace for up to twenty images, with multiple document selection and bounded thumbnails. |
| Bottom tray | Show cropped thumbnails, filenames, crop dimensions and available modification timestamps. Sort by name or time in either direction; unknown timestamps stay last. |
| Cropping | Individual touch/numeric cropping and batch edge trimming in Pixels/Percent, image checkboxes, preview switching and Reset crop. Keep originals and store reversible crop metadata. |
| Arrangement | Hold and drag a thumbnail to snap to any placed image's right side/top alignment or bottom side/left alignment. Tap thumbnail then + target is also supported. Prevent overlap/cycles; reflow attachments when parent crops change. |
| Assembly state | Independent undo/redo and persistent current project. Keep source copies needed by current state or history; prune unused private copies. Unplacing a parent returns attached images to the tray. |
| Output | Save the placed composition directly as PNG or transfer it to Paint as an undoable replacement. Decode cropped source regions sequentially, preserve EXIF/alpha, and offer an explicit size choice when the full output exceeds the device budget. |
| Layout/help | Adapt the assembly controls and bottom tray for portrait and short landscape screens; update in-app usage instructions. |
| Attribution | Credit the new Select all icon, crop handles and assembly markers; retain Catrobat, inherited artwork, system-font explanations and dependency notices. Bundle this version's complete corresponding source. |
| Upgrade | Version 2.14.1-local.7, code 60. Keep app.paint.local and the existing signing certificate. |

Regression tests cover percentage/aspect-lock behavior, touch trimming and undo,
20-image import, timestamp/name sorting, drag snapping, individual/batch cropping,
project persistence, exact PNG pixels and transfer to the actual Paint activity.
See LOCAL_BUILD.md for the memory policy and the test-only region-decoder adapter
limitation. Final suite, lint, APK signature and alignment results are included
in the build backup. No physical phone was available for installation testing.


## Canvas expansion, edit grid and assembly refinement: 2.14.1-local.8

Local modifications dated 7 September 2026.

| Area | Changes in this version |
| --- | --- |
| Touch canvas size | Extend the existing eight handles beyond the original canvas on any side. Inward dragging still trims; outward dragging fills new space with BG. Apply bounds preserves exact original pixels and alpha, with no scaling. |
| Viewport | Fit reserves finger space around the handles and includes expanded bounds; zoom and scrollbar calculations support negative left/top bounds. |
| History | Undo turns grey when there is no committed history or pending geometry to cancel. Undo first cancels an unfinished canvas adjustment, curve or polygon. Opening an unchanged bounds tool adds no history. Edit menu availability follows the toolbar. |
| Edit icons | Place Cut/Copy on the first row and Paste/Select all on the second, below How to use for all sixteen tools. |
| Assembly normalization | Same width and Same height apply to all loaded inputs, preserving each cropped image's aspect ratio. Offer pixels, percent, smallest/largest presets and Restore original sizes. Persist reversible normalization metadata and render from original cropped sources. |
| Single-image unplace | Return only the chosen image to the tray; promote successors into the gap. Remove and moving a placed image also keep other images placed. Reattach colliding branches without overlap, with one undo step. |
| Direct drag | Drag an already placed image as well as a tray thumbnail. Preview the snapped image and gap closure before release; cancellation keeps the layout. Retain right/top and bottom/left alignment and tap-to-place targets. |
| Show all | Rename assembly Fit to Show all and explain that it changes the view zoom only, leaving output dimensions unchanged. |
| Allocation and crop safety | Check expanded dimensions and memory before allocation. Keep source-image crop dialogs bounded. Preserve the document when expansion is refused; make applied expansion and trim reversible with Undo/Redo. |
| Help and credits | Update instructions and retain all original Catrobat, AGPL, icon, artwork, font and dependency credits; include this exact version's source. |
| Build/upgrade | Version 2.14.1-local.8, code 61; preserve app.paint.local and its signing certificate. Accept an optional localDebugKeystore build property for the saved key. |

Host-side native-graphics regressions cover four-sided expansion, alpha and
PNG pixels, undo/redo/cancel/no-op behavior, bounded source cropping, overflow
and memory rejection, and the two-row action layout. Assembly checks cover
normalization, persisted dimensions, exact exported alpha/pixels, gap closing,
branched arrangements, moving the first image, direct touch dragging and
cancellation. No physical phone was available. The build backup records the
current test and APK checks.


## Autosave, compact workspace and fonts: 2.14.1-local.9

Local modifications dated 7 September 2026.

| Area | Changes in this version |
| --- | --- |
| Autosave | Save a private draft after an editing pause and on leaving. Store matching pixels/metadata atomically, retain the previous draft on failure, and restore filename, settings, viewport, floating selection and pending geometry. Display save/error status. Preserve an unreadable draft separately with File > Export recovery copy; pause autosave if preservation fails. Keep manual exports separate. |
| Colour controls | Pin a compact FG/BG colour indicator at the sidebar bottom. Clicking expands/collapses the full pinned palette. Preserve panel choices. |
| Sidebar | Add a top-level collapse/restore icon; keep it accessible when the sidebar is hidden. |
| Navigation | Replace Magnifier with Navigate. Support one-finger pan in that mode and two-finger pan/pinch in drawing modes. Cancel preliminary drawing without leaving a mark or destroying Redo. |
| Landscape | Merge both top bars into one row with a centred filename and a compact menu exposing all six menu groups. |
| Opaque main editor | Remove opacity controls and eight-digit colour entry. Make main-editor drawing colours opaque and composite transparent imports onto BG; preserve originals. Assembly and the retained layer editor keep their existing alpha handling. |
| Licences | Keep Copy all, Other terms and Done fixed outside scrolling text; copy the entire displayed term. Retain existing credits and add original notices for every bundled font. |
| Custom colours | Default to Pale Violet #5B67FF, Gold #FFD700, Silver #C0C0C0 and Copper #B87333, preserving existing user replacements. |
| Fonts/text | Add ten unmodified OFL fonts and six more system-family choices. Render dropdown names in their own font and provide a live preview, underline, strikethrough, alignment, line spacing and text-box controls alongside existing bold/italic/size. |
| Credits/source | Attribute the new local vector controls; bundle original font copyright/OFL texts, pinned upstream font URLs, hashes, and this exact app source. |
| Upgrade | Version 2.14.1-local.9, code 62. Preserve app.paint.local and the signing certificate. |

This update includes new native-graphics tests for persistence/failure recovery,
gestures, panel layouts, licence actions, fonts and opaque main-mode behaviour.
See LOCAL_BUILD.md and the build backup for test scope and final verification.

## Panel arrows and visible submenus: 2.14.1-local.10

Local modifications dated 7 September 2026.

- Replace the title-bar sidebar button with an arrow on the left below the toolbar. Up collapses the sidebar; down expands it. The control remains visible while the sidebar is hidden.
- Add a distinct arrow area to the right of the current FG/BG colour box. Left collapses the pinned palette; right expands it.
- Start both panels expanded on the first launch of this layout, including upgrades, then remember user choices.
- Use native Android submenus under each landscape Menu category, with visible submenu indicators and shared command/Undo/Redo state.
- Update help and vector-asset credits; retain all existing code, icon and font notices.
- Increment version to 2.14.1-local.10, code 63; keep the application ID and signing certificate.

## Palette expands to the right: 2.14.1-local.11

Local modifications dated 8 September 2026.

- Move the palette into the canvas column beside the pinned FG/BG indicator. It opens directly to the right on the same row, instead of creating a separate row beneath the indicator and workspace.
- Match both controls to an 80 dp height. Keep the indicator fixed when the palette opens or closes; the canvas uses the freed space when it closes.
- Preserve the expanded defaults, saved panel choices, sidebar arrow, colour actions and landscape submenus.
- Update help and existing native layout checks for portrait and landscape alignment and collapse/expand behaviour. Retain all existing copyright, icon and font notices; no new third-party assets are introduced.
- Increment version to 2.14.1-local.11, code 64; keep the application ID and signing certificate for upgrades.

## Copyleft icon replacement: 2.14.1-local.12 — 9 September 2026

- Replaced all 16 locally drawn tool glyphs, Undo/Redo, Cut/Copy/Paste,
  Select all, zoom-in/out, both sidebar states, both palette states and the
  assembly attachment glyph with 29 KDE Breeze Icons under LGPL-3.0-or-later.
- Removed the old glyph geometry from ToolButton.kt, ActionButton.kt,
  ColourStatusButton.kt and AssemblyCanvas.kt. CopyleftIcon.kt caches
  the replacement resources and applies normal/disabled/white display tints.
- Preserved button labels, hit areas, selection states, greyed-out Undo,
  panel directions and remembered expansion settings.
- Preserved exact upstream SVG bytes at revision
  `235730e69d90949621e4fee77fcc459772b7a8f0`. The source archive includes
  original artwork, source URLs, hashes, alias resolution, copyright and
  licences plus the PNG conversion script and generated Android resources.
- Added Help > Icon licences, including the complete upstream COPYING-ICONS
  (LGPL v3 and the artwork clarification) and the GPL v3 text it incorporates.
  Corrected About, asset credits and third-party notices to identify KDE
  artwork and its licence separately from AN Paint application code.
- Inherited Catrobat launcher/retained-editor assets, Android menu indicators,
  fonts and their notices are retained. Dynamic swatches, gradients, crop
  handles and image outlines remain state displays drawn by the app.
- Package ID `app.paint.local`; version code 65. Uses the existing signing key.

The icons are converted to small density-specific PNG resources; no SVG
renderer, icon font or other runtime dependency is added to the APK.
Verification results for this build are recorded in its build backup.

## Credit descriptions: 2.14.1-local.13 — 9 September 2026

- Removed reference-design and trademark disclaimers that did not describe
  included components from About and the asset-credits page.
- Described the drawing workspace and its two-column toolbox in neutral terms.
  Cleaned the corresponding source comments and build/change documentation.
- Retained the actual project attribution, all third-party copyright and licence
  texts, the KDE Breeze copyleft icons and their original SVG sources.
- This release changes descriptive text and version metadata only. Colour
  values, layouts and editing behaviour are unchanged from local.12.
- Package ID `app.paint.local`; version code 66. Uses the existing signing key.

## Drawing and selection controls: 2.14.1-local.14 — 9 September 2026

- Polygon: double-tap the final vertex to close and commit after at least three
  vertices. Keep Finish polygon as an alternative. Do not append a duplicate
  vertex on the finishing tap; reset recognition on cancellation/navigation.
- Rounded rectangle: add an image-pixel corner-radius slider, with each shape
  limiting its radius to half its shorter side. Preserve the value in autosave.
- Zoom: put a labelled 100% line at the slider centre. Zoom in/out buttons and
  menu actions stop at 100% when crossing that level. Add an adjacent Fit button.
- Selection: add four resize grips and a round rotation grip to rectangular,
  lasso, Select all and pasted selections. Lock proportions by default; offer
  independent width/height stretching when unlocked. Show dimensions and angle.
- Keep unscaled source selection pixels during handle adjustments, render them
  with the current scale/rotation, and preserve the opposite corner on resize.
  Copy, Cut and Crop to selection use the transformed result.
- Include floating transforms in Undo/Redo and autosave. Cancel the current
  transform on touch cancellation or two-finger navigation without losing the
  earlier selection. Preserve existing drafts with optional metadata fields.
- Update help and dynamic-control credits. Keep the existing KDE Breeze glyphs
  and all actual third-party copyright and licence texts.
- Package ID `app.paint.local`; version code 67. Uses the existing signing key.

Validation results and their scope are recorded in the build backup.

## Edge handles and app identity: 2.14.1-local.15 — 9 September 2026

- Add four edge-midpoint resize grips to the existing selection corner/rotation
  controls. Keep the opposite midpoint fixed in rotated coordinates; preserve
  proportions when locked and resize one axis when unlocked.
- Show the transformed free-form selection outline inside its bounding box,
  retaining the original masked pixels and unselected areas. Clip the display
  outline to the initial canvas bounds and preserve it with floating autosave.
- Change the application ID and app module namespace to `io.github.c933103.anpaint`.
  Provider authorities follow the new ID. Keep the app name AN Paint and the
  inherited library namespace. This installs separately from earlier local builds.
- Replace the installed launcher with an original AN monogram under
  AGPL-3.0-or-later, including legacy/round/adaptive/themed resources, editable
  SVG, conversion script and hashes. Update its in-app provenance and credits.
- Prepare a project-specific README, preserving the upstream README separately,
  and ignore private signing material for the source repository. Document image
  transfer via Save PNG in the old app and Open in the new installation.
- Version code 68. The existing private signing key is retained for future
  updates under this new package identity. Genuine third-party terms and font
  assets remain intact; only descriptive asset-provenance text changes.

Validation results and the GitHub publication status are recorded with the
build deliverables. A remote fork is not claimed until GitHub confirms it.

## Editor consolidation: 2.14.1-local.16 — 10–12 September 2026

Removed the original editor following the feature mapping in `EDITOR_PARITY.md`.
Ported Watercolor, shapes, cursor/magnifier, numeric brush settings, recent
colours, JPEG quality, sharing and gallery access into the new editor. Removed
layers/document transparency, Smudge, auto crop and native project formats as
requested; preserved internal selection masks. UI text moved into translation
resources. The intentionally unfinished delivery passed 154 unit checks but
failed one JPEG XL boundary test. Its exact status is preserved in
`verification/HANDOFF_LOCAL16.md`.

## Codec completion and audit: 2.14.1-local.17 — 12 September 2026

- Correct JPEG XL output streaming and valid source rectangles beyond 2048 px;
  use the Android API21-compatible large-file writer.
- Add native HEIC/AVIF still-image imports and saves, and true lossless or
  quality-adjustable WebP saves. Include all native dependency sources and terms
  in the offline corresponding-source archive and Help.
- Include native source/tile working memory in main-editor and assembly import,
  resizing and export admission checks. A smaller requested output cannot hide
  source-decoder memory requirements.
- Add format-dialog, source-memory and RTL regression checks plus installed-app
  emulator checks. Correct old launcher/backup lint findings without suppressing
  those warnings.
- Re-audit original-editor feature coverage; retain the requested removals and
  translation preparation. Record exact Dubai and former STC/GE SS identities,
  actual licence restrictions and the decision to keep those binaries excluded.
- Version code 70; retain `io.github.c933103.anpaint` and the AN Paint signing key.
- Isolate native codec CPU-feature settings so the generic AVIF build does not
  inherit another decoder's ARMv7 NEON detection.

See `HANDOFF.md` and the release verification report for executed checks and
physical-device limits; implementation entries alone are not test results.


## Responsive toolbox and colour imports: 2.14.1-local.18 — 12 September 2026

- Group drawing, selection and shape/text tools into expandable categories with
  remembered choices and reversible Breeze arrows. Use a top horizontal strip and
  downward options in portrait; retain a left strip and rightward options in landscape.
- Give Pencil an independent 1–100 px width, numeric input and draft persistence.
- Preserve input alpha until background compositing. Normalize working bitmaps to
  8-bit sRGB, including floating-point inputs, so memory/history assumptions remain valid.
- Add explicit ICC/CICP and HDR colour conversion with real high-depth and transparent
  fixtures. Exercise modern Ultra HDR inputs on Android 15 in addition to Android 11.
- Trace the original Dubai/STC additions and distinguish undocumented permission
  for AN Paint from any claim about upstream authorization.
