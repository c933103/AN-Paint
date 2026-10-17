# Complete English assembly Help review

Base: develop 44ad5ce2156fef79baae3ef5650b9ac5eac06202. Application candidate: fcdb417dddd5cba516eea661e917f0183ed61d46.
Key: string/ui_add_up_to_20_images_with_android_s. Priority remains P3.

## Exact inventory

Ten values: default English; International English en-001; six regional variants en-AU, en-CA, en-GB, en-IN, en-SG, en-US; plain-English vertical-test en-XV; and separate emoji-English qaa-Zsye-XV. The emoji-English canonical XML is mirrored by the existing build to en-Zsye-XV-anpaint, while the user-facing preference stays qaa-Zsye-XV. The en-XV test locale is not the emoji locale.

Every complete old/new value is retained in complete-value-comparison.json. Each complete candidate also has a runtime fixture. en-US preserves its existing licenses spelling; other ordinary English variants use licences. No other-language resource is changed.

## Full-entry review, eight paragraphs

1. Import/tray: at most 20 inputs; provider filenames/times; displayed dimensions include crop and normalization. AssemblyActivity.renderTray uses placedSize; ImageAssembly.placedSize preserves individual aspect ratio. Sorting does not mutate layout. Both vertical English variants still said only crop dimensions, so this same-entry omission is repaired.
2. Crop: individual and selected batch crop, pixel/percentage margins, dragging or typed values, reset, non-destructive operations and undo. ImageCropDialog and ImageAssembly.crop retain the original input files. This paragraph remains unchanged except complete emoji button-label references.
3. Snap placement: hold/drag and highlighted edge targets; the ghost reflects the prospective layout; RIGHT aligns top edges and BOTTOM aligns left edges. The origin and overlap statements are now explicitly limited to snapping: “When snapping, the first image starts at the origin.” and “Overlaps are rejected when snapping.” Qualified crop movement remains “Attached images may move when their parent is cropped.” ImageAssembly.place, targets, layout and validateSnapPlacement establish this behavior.
4. Exact position: selected image; current Exact position toolbar label; top-left X/Y, whole pixels, zero-based coordinates; other images preserve their positions and overlaps are allowed. AssemblyActivity.exactPosition launches AssemblyPositionDialog; its inputs reject negative/fractional/out-of-range coordinates. ImageAssembly.position freezes direct children at their current coordinates and only moves the selected image. This paragraph is new.
5. Common size: Same width/Same height preserve each image's own aspect ratio; Pixels/Percent/Smallest/Largest; Restore original sizes retains crops. The current control names are checked in every variant. Ordinary English pixels/percent are prose forms of the title-case unit controls. Emoji-English now retains the full decorated labels in these references.
6. Unplace/remove/history/view: Unplace retains the selected input in the tray; other images remain placed. Attached images may fill a removed snap-parent gap, while explicit-parent removal preserves their coordinates. The old guarantee is replaced by “Other images stay placed; attached images may move to fill the gap.” Remove deletes only the selected input; undo/redo, drag rearrangement, empty-area pan, pinch and Show all retain their meanings. Show all adjusts viewing zoom, not output dimensions.
7. Output/memory/persistence: Save PNG exports directly; Edit in Paint performs an undoable main-editor replacement. Smaller-copy choice is conditional on being offered; a source-memory floor can warn without a chooser. The two vertical English variants still implied that a chooser is always available and omitted the warning-only branch; both same-entry omissions are corrected. Source bytes stay unchanged and the locally saved assembly reopens.
8. Credits: the main File > About, licences/licenses & credits route and Catrobat/AGPL/asset-credit reference remain unchanged. Emoji-English retains its existing full decorated route labels.

## Actual label review

The main controls are Crop image, Batch crop, Reset crop, Same width, Same height, Smallest, Largest, Restore original sizes, Unplace, Remove, Show all, Save PNG, Edit in Paint, and Exact position. Every ordinary English variant uses the same labels. Emoji-English uses the actual decorated equivalents, including “📍 Exact position”, “🖼️ Crop image”, “🧪 Batch crop”, “↔️ Same width”, “↕️ Same height” and “📏 Restore original sizes”. The new host contract checks the complete labels against canonical resources. No label resources changed.

## Evidence boundaries

- Source review and whole-value comparisons are complete for these ten English values only.
- New host guards enforce whole values, inventory, eight paragraphs, actual control labels, qualified crop/removal behavior, dimension and memory clauses, and P3. The oracle has 120 malformed/old-claim controls plus ten separately restored old-full-value controls.
- New Robolectric methods use actual Help/toolbar consumers. They check native Help and both vertical shells, current full messages/labels, explicit first placement, overlap with unchanged other images, exact-parent Unplace/Remove, snap origin/collision rejection and gap filling, Undo/Redo and unchanged source bytes. Existing cancellation, validation, reopening, crop and model tests remain intact.
- These are whole-message/interaction regressions, not a proof of glyph shape, full visible extent, physical-device layout, TalkBack, or whole-language acceptance.
- Fifty other-language Help overrides need full-entry/source-binding re-review; 112 other public locales use English fallback and need routing rechecks. This source change does not carry historical full-Help acceptance forward. Separately bounded unchanged crop-warning/plural and unrelated-key evidence is not silently invalidated or enlarged. PR56 is untouched.
