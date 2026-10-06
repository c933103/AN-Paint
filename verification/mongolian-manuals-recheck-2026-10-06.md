# Mongolian manuals: fresh source and clause recheck, 6 October 2026

This is a bounded new review after the September 28 reset. It does not reinstate
any withdrawn completion claim or close PR8, the central register, or native
language/runtime review. The starting original-branch and remote head was
`e2e79f905b1b66772ac3e343d1192261e46fd7d1`; the worktree was clean.

## Scope and exact resources

The old PR8 findings distinguish three subjects, not three interchangeable help
strings: the long main manual (including Tibetan/Dzongkha/Traditional Mongolian
locations), the Traditional Mongolian assembly manual, and Irasutoya conditions.
This pass reads both Mongolian scripts for each subject and also checks the
separate active main help and Catrobat attribution text:

- `ui_the_arrow_on_the_left_directly_below_the`: retained long main manual.
- `ui_add_up_to_20_images_with_android_s`: dedicated assembly manual, displayed by
  `AssemblyActivity.showHelp()`.
- `ui_irasutoya_help34`: Irasutoya instructions, selected through
  `IllustrationSource.IRASUTOYA` and displayed by `MediaGalleryActivity`.
- `ui_help23`: active main help, displayed by `ClassicPaintActivity.showHelp()`.
- `gallery_description`: Catrobat instructions and attribution.

The full English main and assembly resources are in `values/strings.xml`.
Irasutoya's English resource is in `values/editor34_strings.xml`, not
`values/strings.xml`. Checking the latter file alone would miss its source.
Tibetan and Dzongkha were inspected only for the specifically implicated opening
main-help clauses and Irasutoya clauses. Their catalogues were not edited.

Original findings used as leads:
[main manual](https://github.com/c933103/AN-Paint/pull/8#discussion_r4079390043),
[assembly](https://github.com/c933103/AN-Paint/pull/8#discussion_r4079390046),
[Irasutoya](https://github.com/c933103/AN-Paint/pull/8#discussion_r4079390051).
Their age and unresolved state do not establish the current contents.

## New changes, with meaning and application evidence

| Resource / locale | Newly observed problem | Change and source check |
| --- | --- | --- |
| Main manual, `mn-Cyrl-MN` | `баруун/дээд эсвэл доод/зүүн зэрэгцүүлэн` does not distinguish the attachment side from the aligned edge. | State that attaching on the right aligns the top edges, and attaching below aligns the left edges. `ImageAssembly.layout()` sets right attachment x to `parent.right` and y to `parent.top`; bottom attachment x to `parent.left` and y to `parent.bottom`. These are physical image coordinates, independent of writing direction. |
| Assembly manual, `mn-Cyrl-MN` | The ghost preview is called `Тунгалаг` (transparent), losing the partial-opacity distinction. | Use `Хагас тунгалаг` (partly transparent). `AssemblyCanvas.onDraw()` draws the ghost with alpha 180 out of 255. Traditional Mongolian already says `ᠬᠠᠭᠠᠰ ᠲᠤᠩᠭᠠᠯᠠᠭ`. |
| Main manual, `mn-Mong` | The Fit sentence names the function but omits the adjacent button. | Restore `ᠬᠠᠵᠠᠭᠤ ᠶᠢᠨ … ᠲᠣᠪᠴᠢ` (the adjacent … button). The `zoomRow` in `ClassicPaintActivity` includes the `zoom_fit_view` control alongside the slider. |
| Main manual, `mn-Mong` | The quoted Save and share label uses `ᠬᠠᠳᠠᠭᠠᠯᠠᠬᠤ ᠪᠠ …`, unlike the displayed menu label. | Use the `ui_save_and_share` caption `ᠬᠠᠳᠠᠭᠠᠯᠠᠵᠤ ᠬᠤᠪᠢᠶᠠᠯᠴᠠᠬᠤ`, without the menu ellipsis. Preserve the existing save-before-sharing clause. |
| Active main help, `mn-Mong` | Save only says it reuses the settings, omitting that it writes to the same location. | State that it saves again **with those settings at that location** (`ᠲᠡᠷᠡ ᠲᠣᠬᠢᠷᠠᠭ᠎ᠠ ᠪᠠᠷ ᠲᠡᠷᠡ ᠪᠠᠶᠢᠷᠢᠰᠢᠯ ᠳᠤ`). `requestSave()` copies `savedTarget.options` and calls `writeImage(savedTarget.uri)`. Save and share separately sets export mode and does not replace that saved target. |
| Catrobat gallery help, `mn-Mong` | Copy credit loses its publication purpose; the next sentence contracts separately named creators and other source notices to generic creator/copyright/source nouns. | Restore use when publishing one's work, separately named creators' names, copyright notices and other source notices. Preserve CC BY-SA 4.0, the compatible-licence alternative, describing edits, editing credits and the retained-source route. Compare the English `gallery_description`, `GalleryCredits.credit()` and the bundled `ASSET_CREDITS.txt`; no legal body or licence identifier is changed. |

These are direct canonical XML edits. No reference catalogue or generator was
used to replace reviewed text. Lexical checks include the Mongolian dictionary's
[right-side sense of баруун](https://www.mongoltoli.mn/search.php?opt=1&ug_id=12402)
and [тунгалаг](https://mongoltoli.mn/dictionary/detail/89712). Those dictionary
results support words, not the fluency of entire technical sentences. The
Traditional Mongolian wording is an editorial translation requiring independent
native review; this file does not invent such a review.

## Long main manual: paragraph-by-paragraph comparison

The following is a fresh semantic reading against the entire current English
resource, not a key-presence or length test. Each row was checked independently
in `mn-Cyrl-MN` and `mn-Mong`. “Present” means the listed English meaning can be
identified in those translations; it does not mean the English is up to date
with every current screen. The source-drift limits below still apply.

| Section | Clauses checked in both scripts | Finding |
| --- | --- | --- |
| Tool panels | Up/down collapse/expand; portrait strip and swipe; landscape left strip; Brush/Selection/Insert group contents; expansion below/right; second tap and reversed arrow; remembered tool; bounded-panel scrolling; first-launch expansion; later persistence; landscape row and centred filename; File/About route. | Present. The old omitted scrolling/start-state/persistence clauses are explicit now. In Traditional Mongolian, see `ᠬᠢᠵᠠᠭᠠᠷ ᠲᠠᠢ … ᠰᠠᠮᠪᠠᠷ᠎ᠠ ᠶᠢ ᠭᠦᠶᠦᠯᠭᠡᠨ᠎ᠡ`, `ᠠᠩᠬ᠎ᠠ … ᠬᠣᠶᠠᠷ ᠰᠠᠮᠪᠠᠷ᠎ᠠ`, and the following saved-choice sentence. |
| Palette | Fixed lower-left FG/BG; palette on its right on same row; arrow directions; extra swatches hidden without moving indicator; colour-box toggle; tap/hold foreground/background; Palette/Honeycomb/Advanced; spectrum/wheel/RGB/HSV/HSL/six-digit hex; four recent cells and gestures; four custom names/hex values; replace custom swatch; opaque editor; transparent imports on current BG; originals unchanged. | Present, sometimes reordered in Traditional Mongolian. Hex values remain exact. This describes the retained legacy source; current palette UI needs separate reconciliation. |
| Navigation | One-finger pan; two-finger zoom/pan; Navigate/Draw again exit; navigation in drawing tools without paint marks; bottom-right slider and 100% centre; buttons stop when crossing 100%, next press continues; adjacent Fit and centring; View 100%/pixel grid. | Present after the adjacent-Fit repair. Traditional Mongolian distributes two-finger pan and the second press across later sentences in the same paragraph. |
| Draft/save | Editing pause and leaving app; draft status/error; restore filename/settings/floating selection/unfinished geometry; private draft; PNG, JPEG/HEIC quality and JPEG XL/WebP/AVIF lossless/lossy; write before sharing; chosen export location/star; no autosave overwrite of source. | Listed meanings present; quoted Save and share caption repaired. **The English export/star account conflicts with current Save behavior; this row is not current-behavior approval.** |
| Selection | Rectangle/free outline; move inside; square corner/edge midpoint resize; round rotate; default aspect lock and independent axes; edge-side resize; retain shape after rotation/autosave; dimensions/angle sidebar; one undoable commit; unfinished transform; transformed Copy/Cut/Crop; Select all second row/Ctrl+A; two edit rows; mask shape/opaque document. | Present. The Traditional Mongolian paragraph first abbreviates handles, then explicitly distinguishes square and round handles later. |
| Bounds/size | Inward crop/outward expansion on any side; Apply bounds; new BG area; existing pixels not scaled; Cancel/Undo; Resize/Canvas size/New image; Pixels/Percent; optional aspect lock. | Present. |
| Tools/text/cursor | Curve line and two drags; polygon vertices/final double tap/Finish; open connected segments; radius control and half-short-side limit; text tap/font preview; size/bold/italic/underline/strike/alignment/line spacing/BG box; Watercolor location/strength; 100px sizes/1px pencil/remembered width/numeric entry; Heart/Star/Arrow outline/fill; cursor route/options/position/start/pan/stop; Draw/Drawing settings; adjustable magnifier; smoothing/antialiasing; bundled-font terms. | Present against English. Current font count and full typography/runtime behavior are not certified by this reading. |
| Import/credits | Load replaces canvas via Android picker; Draw/Insert/Other images; device/Catrobat/Irasutoya/Openclipart; online Use image; floating selection; retained source links/licence route; original resolution within memory budget; resize dimensions/pixel count/memory estimate; Pixels/Percent/aspect lock; original unchanged. | Present. Traditional Mongolian combines this paragraph with the next assembly paragraph; the boundary difference is not an omission. |
| Assembly summary | File-only route; separate workspace; up to 20; filename/time sorting; single/batch crop; all-input aspect-preserving normalization; right/top and bottom/left; selected unplace/gap closure; Show all view zoom; PNG; undoable Paint transfer; opaque main editor/separate arrangement workspace. | Present with the already-published capacity sentence and the new Cyrillic direction clarification. The capacity repair alone did not establish the other clauses. |
| Final credits | File/About route; original copyright; assets/fonts; full licences; this version's complete source; independently scrolling licence body and fixed Copy all/Other terms/Done controls. | Present. This checks the translation, not completeness of delivered corresponding source or actual legal-panel runtime behavior. |

## Dedicated assembly manual: separate checks

| Paragraph | Independently inspected meaning | Current result in both scripts |
| --- | --- | --- |
| 1 | Android picker, maximum 20, bottom thumbnails/name/crop dimensions/provider modification time, sort keys, sorting leaves placed layout unchanged. | Present. `ImageAssembly.MAX_IMAGES` is 20; `sorted()` returns an ordering without changing stored attachments. |
| 2 | Select thumbnail, individual/batch crop, pixel/percentage margins, drag/type, reset to original edges, non-destructive crop, undo. | Present, including the old reported reset/non-destructive/undo omissions. Crop is a retained `Rect`; history stores old states. |
| 3 | Long-press tray or drag placed image; highlighted edge; exact translucent ghost; right/top and bottom/left; thumbnail then +; origin; attached images move after parent crop; reject overlaps. | Present; Cyrillic translucency corrected. `layout()`, target rectangles, alpha 180 and overlap validation supply independent behavior evidence. |
| 4 | Same width/height for every input, own aspect ratio, pixels/percent/Smallest/Largest, restore originals removes normalization and keeps crops. | Present. `normalize()` changes normalization and `resetSizes()` clears it without changing crop rectangles. |
| 5 | Only selected image unplaced; following images fill gap and stay placed; Remove only that input; Undo/Redo; rearrange; empty pan; pinch zoom; Show all never changes output size. | Present, including the old reported output-size omission. `detached()`, `remove()`, history and `AssemblyCanvas.fit()` support the distinction. |
| 6 | Save PNG directly; Paint replacement undoable; smaller output if over memory; originals unchanged; locally stored assembly reopens. | Present, including the old reported memory/reopen omissions. `requestOutput()` uses the budget/size dialog; `ImageAssembly` writes and reads `project.json`. The source-memory-floor edge case remains a help-source issue, described below. |
| 7 | Same Catrobat/AGPL and asset credits, actual File/About panel. | Present. No licence ID was replaced or translated. |

## Active help, attribution and the other implicated locations

The separate `ui_help23` in both scripts was read for tabs, controls, navigation,
colour preview/confirm/cancel, saved-colour actions, Advanced position, pixel
rulers and x/y, Save as format/settings/location, repeat Save, non-saving export,
save-before-share and unchanged Save destination, insertion providers/floating
handles/Fit versus Original size, restoring both history stacks, File commands,
and horizontal/vertical text. The repeat-Save destination omission above was
found only in Traditional Mongolian. The remaining listed meanings are present;
this does not certify every referenced control's translation or runtime.

Both Mongolian Irasutoya resources currently contain all seven source elements:
artwork page and Use image; English/Japanese search; titles/site text remaining
Japanese; free use subject to terms; **commercial** use of **21 or more** items
requiring payment; possible special-collaboration conditions; retained source
pages/credits and the File/About/Image credits route. The last two elements are
also explicit in current Tibetan and Dzongkha. No Irasutoya string was changed.

The current Tibetan/Dzongkha long-manual opening also explicitly contains the
bounded options-panel scroll, initially expanded two panels, remembered later
choices, and the landscape top row/centred filename. These observations address
the named old omissions only; the rest of those languages remains outside this
pass. The removed generic Menu route was not restored.

The Catrobat resources retain immediate insertion, title/publisher/source/licence,
CC BY-SA 4.0, separately named creators, other notices, change description,
compatible licence, Edit credits and retained source route after the Traditional
Mongolian repair. This is instruction fidelity, not credit-lifecycle testing.

## Remaining limits requiring further work

- The retained English main manual has no direct reference in the searched
  `Paintroid/src/main/java` sources; current main help is `ui_help23`. Its
  export/star wording is stale: `writeImage()` updates `savedTarget` and calls
  `document.markSaved()` only when `!exporting`. Export/share preserves the old
  Save target. Its older palette/layout and numeric font-count wording also
  require shared-source reconciliation before the long manual can be called
  current. Both scripts inherit this issue; matching English does not close it.
- The dedicated English assembly help calls tray sizes crop dimensions, but
  `renderTray()` displays `placedSize` (including normalization). It also says to
  choose a smaller output when over budget, while `outputSizeDialog()` can show
  `ui_assembly_source_memory_floor` when no smaller output fits the source-memory
  floor. These are shared-source precision gaps; they were reported for shared
  reconciliation rather than silently changing only Mongolian meaning.
- A fresh independent legal-source check of Irasutoya's current terms did not
  complete: the official terms page failed to load in browsing (including a
  non-retryable Google challenge), and the execution-network request returned
  HTTP 403. The statements above compare the translation with the current
  repository English and bundled notices, not with a freshly fetched legal page.
- Independent native fluency, vertical shaping/layout, screen sizes, accessibility,
  API/device behavior, image-credit lifecycle and the rest of the PR8 catalogue
  are unverified here. Complete latest conversation transcripts are unavailable.
  None of these limits implies that unrelated 81 locales should be completed.
- The new changes must be published on the original PR8 branch and integration
  PR15, with remote trees and new CI outcomes checked separately. This local
  evidence is not proof of publication.

## Reproducibility and local checks

The English `values/strings.xml` used above has SHA-256
`4b13f6720333c78291095bfae6ef1ba770d834cf9ed5449d4139c3859786d33c`.
For the two modified XML files:

| Locale | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `mn-Cyrl-MN` | `e01f79b0635fffa647c367bd457f910a15cb2d096df41c09371e1de8ef887a7e` | `011f4b74cf0b2e25f7bf2ebdf644e5b39869d885b574c34ee6afbb41ec59597f` |
| `mn-Mong` | `3f1d6c922fece1c9060270bacc5a1fe8317efe7efb6eaa481bdca0fb3bc42823` | `a969e1de3735f67ddf958eff39eaa5ef6c824003c199a8faba34af93480104a8` |

Strict `aapt2 compile --dir Paintroid/src/main/res` passed without `--legacy`.
The resource comparison confirms unchanged resource-name sets, XML attributes,
percent tokens and escaped-newline counts. No plural resource or format argument
changed. These are structural/resource checks, not linguistic acceptance.

`python3 -m unittest discover -s tools -p 'test_*.py'` passed **91 tests** in
27.559 seconds. `git diff --check` passed. Android build and device results belong
to the published commit's CI and are not claimed here.
