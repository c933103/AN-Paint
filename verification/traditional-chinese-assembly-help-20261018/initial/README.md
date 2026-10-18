# Traditional Chinese assembly Help: bounded complete-entry correction

PR: https://github.com/c933103/AN-Paint/pull/134
Application head: `50307966ebad759e0e66e13fd18706e1b129305e`
Application tree: `f7fd3b473e09ec91a8f06cea1e54ec88b0b47da8`
Base develop: `702f0d8afa5bd5c950ec22ae14f29aecf4140482`
Hosted run: https://github.com/c933103/AN-Paint/actions/runs/39120393383

## Complete-entry source and meaning review

This corrects `ui_add_up_to_20_images_with_android_s` in `values-zh-rHK` and
`values-zh-rTW` only. The accompanying JSON contains both complete original
Android-escaped values, the complete reviewed replacements, displayed values,
and exact base/final blob identities. Each replacement has eight paragraphs.
The corrected English meaning reference is PR #122 at
`0d56dd970c22398f7fa032d1baee4a1b74c83f2b`; the old English Help on develop was
not treated as the corrected authority.

1. Import/tray/sorting: keep the 20-image limit, thumbnails, filenames, effective
   dimensions after cropping and Same width/height, both sort options, and the
   fact that sorting does not rearrange placements. HK is unchanged. TW confines
   the provider-data condition to modification time, which is optional.
2. Selection/cropping: unchanged complete paragraph in each locale. Preserve
   actual Crop image/Batch crop/Reset crop names, selected images, pixels or
   percentages, handles or numbers, restoration of edges, nondestructive
   originals, and Undo.
3. Snapping: retain hold/drag, highlighted edge, exact translucent preview,
   top alignment on the right and left alignment below, and thumbnail/+ route.
   Qualify origin and overlap rejection as snapping behavior. HK already says
   attached images may move after parent cropping. Correct TW to that meaning.
4. Exact position: add the actual 精確位置 label, the selected image's top-left
   X/Y, integer pixels starting at zero, unchanged other-image positions, and
   permitted overlap. HK uses 由零開始; TW uses 從零開始, matching their dialogs.
5. Common dimensions: unchanged complete paragraph in each locale. Retain
   all-input common size, per-image aspect ratio, pixels/percentage/smallest/
   largest options, and reset while preserving crops.
6. Unplace/navigation: replace guaranteed gap filling with preservation of
   other placed images and possible movement of attached images. Keep one-image
   removal, Undo/Redo, drag rearrangement, empty-area panning, pinch zoom, and
   Show all changing view zoom only.
7. Output/memory/persistence: unchanged complete paragraph in each locale.
   Preserve PNG/editor actions, undoable replacement, conditional smaller-copy
   chooser, warning when even tiny output exceeds memory, unchanged originals,
   and locally reopened assembly.
8. Credits: unchanged complete paragraph in each locale. The actual routes are
   HK 檔案 > 關於、授權及鳴謝 and TW 檔案 > 關於、授權與致謝; retain Catrobat/AGPL and asset credits.

Source review used the exact base versions of AssemblyActivity.kt (toolbar,
metadata, output and Help consumers), ImageAssembly.kt (sizes, sorting,
detachment/removal, crop, absolute position, snap alignment and collisions),
AssemblyPlacementDialog.kt (nonnegative whole X/Y), NormalizeImagesDialog.kt,
ImageCropDialog.kt, AssemblyCanvas.kt and AssemblyRenderer.kt. These are under
`Paintroid/src/main/java/org/catrobat/paintroid/classic/` at the immutable base.

Canonical resources are direct Android XML, as TRANSLATING.md explains.
No copy of this Help key exists in the provenance translation JSON. The separate
six exact-position-string fixture remains unchanged. No other Chinese variants,
English fallbacks, locale routes or generated mirrors are in this patch.

## Test-oracle inventory and coverage

The exact-base AssemblyActivityTest and all source/test/resource fixture files
were searched for this Help key and complete HK/TW paragraphs. No pre-existing
HK/TW exact complete-value oracle needed changing. Existing exact French,
Japanese, Hungarian, Korean and crop-counterpart expectations are unchanged.
Prior HK/TW crop-normalized-dimension and memory-warning clause guards remain.
The two new complete fixtures are independently fixed expected text, shared by
host and Android tests rather than derived from production at runtime.

Host tests enforce complete XML/value equality, eight paragraphs, Android
escaping/placeholders, all actual referenced captions, snap-only origin/overlap
rules, conditional dates/movement and prior memory/dimension clauses. Mutations
remove every paragraph, the whole entry, or a final character; duplicate or
re-mark the entry; add markup; and swap locale texts. All must fail.

Five new native-graphics Robolectric methods cover complete compiled resources;
real Help toolbar/dialog open, dismissal and reopening; complete accessibility
text; native line coverage, no ellipsis or horizontal/vertical clipping, and
scrolling every line in normal portrait and 2× short landscape; and actual HK/TW
Exact position/Unplace controls. Locale and global UI resources are bound before
Activity startup. Behavior checks include whole/nonnegative input, invalid and
Cancel preserving the saved bytes, zero, nonorigin first placement, selected-only
movement, deliberate overlap, nonmoving Unplace, snap collision rejection,
conditional gap closing and Undo. Assertions and deadlines are not weakened.

## Validation and limits

The 56 focused host tests, all 942 ordinary-Python host tests, and all 942
optimized-Python host tests passed. Exact-head hosted checks are still pending
in this initial record. Raw local logs preserve the results and both local JVM setup attempts.
The first attempt lacked a writable cached Gradle home; with a writable home,
the uncached Gradle distribution download failed because the network was
unreachable. No local JVM, APK or installed execution pass is claimed.

The complete final remote tree was compared with the reviewed checkout: six
changed/added files, no removals, all 1,213 source blobs and executable modes
accounted for, and every retained base blob outside the two Help values
unchanged. This evidence is additive to that exact application tree on a
separate ref; generated reports are not added to the application PR.

Codex Code and Security review were requested for the exact application head.
Only actual exact-head terminal results and their artifacts can establish the
remaining gates. This is bounded full-Help verification, not whole-language
acceptance, native-speaker certification, installed Chinese glyph/TalkBack or
physical-device verification.

## Separate open warning

TW `plurals/ui_crop_preview_images/other` still unconditionally says that
connected images' positions will be rearranged after cropping. A separate
reviewed correction would say that images attached to the cropped images may
move, preserving the `other` quantity, `%1$d`, `%2$d`, `%3$d`, and newline.
That warning is explicitly outside this Help-only correction and is unchanged.
PR #56, processing labels, French work and broader localization obligations
remain outside this patch. No release or merge is performed by this record.
