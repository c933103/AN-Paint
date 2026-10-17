# Japanese assembly Help: independent correction

## Scope and source binding

This is a complete review and correction of the single Japanese resource `string/ui_add_up_to_20_images_with_android_s`, on develop **5dba779c904a25bde2ec6d6f8f48eb3cad901a1e** (tree `2f15510fa46894e9a372ee58f2bf2b1ffeb4f691`). All 1,194 base files and executable modes were verified against GitHub before applying the four-file change. Merged PR121 is fully retained.

The proposed corrected English Help at **fcdb417dddd5cba516eea661e917f0183ed61d46** (PR122) provides an explicit editorial reference for distinguishing snapping from Exact position. It is **not** an implementation or merge dependency. The actual production implementation on develop already provides the behavior described by this Japanese correction. This branch does not import PR122's English resources, fixtures, tests or other files. Current develop's English Help remains unchanged and its correction is tracked separately.

Exactly one Japanese resource value changes. The other three files are the complete-value fixture, six standalone host regression tests and one added actual-Help consumer test. The host test has no import or runtime dependency on PR122. No production Kotlin/model code changes. P3, all other resource keys/catalogues, current repository visibility, and held PR56 remain unchanged.

This is a bounded complete-value linguistic/source review, not whole-Japanese-catalogue acceptance, restoration of withdrawn conclusions, independent native-speaker certification, or installed-device rendering/accessibility evidence.

## Complete-value assessment

1. Import/tray: preserved the 20-image cap, cropped/normalized display dimensions, optional provider modification time, and tray-only sorting. The whole paragraph remains unchanged.
2. Crop: corrected the ambiguous “margin specification” to the amount trimmed from each edge; uses パーセント to match the current unit control. Reset now explicitly restores the crop region to the whole original image. Selection, handles/numeric entry, non-destructive operation and undo remain intact.
3. Snap: preserved long-press/drag/drop, exact translucent preview, right/top and bottom/left alignment, + target and conditional movement on cropping an anchor. Origin placement and overlap rejection are now explicitly limited to snapping.
4. Exact position: added a separate paragraph using the exact ［正確な位置］ label. It identifies the image’s top-left X/Y coordinates, pixel units, nonnegative integers, preservation of other image positions and allowed overlaps.
5. Normalization: clarified that all inputs share the selected width or height while retaining individual aspect ratios; neither both dimensions nor aspect ratios are made identical. Pixel/percent/smallest/largest references now match the live control labels. Reset continues to retain crops.
6. Removal/navigation: distinguishes returning only the selected image to the tray from removing that input. Other images remain placed; connected images may move into the gap. Corrected ［やり直し］ to the actual ［やり直す］ control and explains undo/redo directly. Rearrangement is described as changing placement, avoiding confusion with tray sorting. Pan, pinch and zoom-only Show all remain intact.
7. Output/memory/persistence: made the undoable main-editor replacement explicit in natural Japanese. Retained direct PNG save, conditional smaller-copy offer, warning when even a tiny output does not fit, unchanged original files and local assembly reopening.
8. Credits: preserved the exact About/credits label and the Catrobat/AGPL/asset-credit claim. The whole paragraph remains unchanged.

## Implementation evidence

The inspected files are byte-identical between the proposed English reference and current develop: `ImageAssembly.kt`, `AssemblyActivity.kt`, `AssemblyCanvas.kt`, `AssemblyPlacementDialog.kt`, `ImageCropDialog.kt`, `NormalizeImagesDialog.kt`, `AssemblyRenderer.kt`, `ClassicPaintActivity.kt` and `ActionButton.kt`.

- `position()` sets nonnegative absolute top-left coordinates, preserves other positions, and permits overlaps. `validateSnapPlacement()` rejects overlapping snap drops; `targets()` starts an empty snapped assembly at (0,0).
- `detached()` preserves coordinates for children of an explicitly positioned anchor, while attachment-tree promotion can close gaps. The Help therefore makes gap filling conditional.
- Crop margins trim each original edge; Reset selects full original bounds. Normalization adjusts the selected dimension and preserves crops/individual aspect ratios.
- The actual toolbar labels match the Help, including 正確な位置, パーセント and やり直す. The main editor receives assembly output as an undoable replacement (`asEdit = true`). Memory handling has both an optional smaller-copy chooser and a no-size-fits warning path.

See source/comparison manifests in the evidence packet for exact file binding. The complete old/new values and paragraph diff follow below.

Application commit: [f1aae6ebd453bac18ddabf7c63e629b4291e4d59](https://github.com/c933103/AN-Paint/commit/f1aae6ebd453bac18ddabf7c63e629b4291e4d59). The complete remote application tree was verified against all 1,196 candidate files and modes before publication.

## Verification

- PASS: 67 assembly-Help host tests normally and 67 with optimized Python, including the six Japanese tests and 25 synthetic omission/semantic/resource-corruption mutations.
- PASS: the actual original Japanese value is rejected by the complete-value oracle.
- PASS: canonical catalogue structure and placeholders.
- PASS: complete resource compilation/linking with aapt2/API35, including both exact-script mirrors.
- PASS: supplementary Kotlin 1.9.24/API35 compilation of the changed activity-test source and helper sources with freshly compiled resource symbols and previously compiled dependency classes. This is not full Gradle compilation or runtime execution.
- PASS: all unchanged file content/modes and the four-file-only diff; whitespace checks.
- PASS: 903 complete host tests normally (227.725 s) and 903 with optimized Python (227.907 s), on this independent source.
- BLOCKED/UNRUN: Gradle 8.13 download fails with `Network is unreachable`; the new Robolectric consumer has compiled but has not run. Full Gradle unit/lint/APK and installed-device checks are not claimed. Exact-head hosted CI must supply fresh Android evidence.

The actual Japanese consumer selects Japanese, opens the production Help via its toolbar, compares the complete eight-paragraph message, verifies the current Exact position button label, dismisses the dialog and checks that assembly contents remain unchanged.

## Full old value

Android のファイル選択画面から最大20枚の画像を追加できます。下部のトレイには、サムネイル、ファイル名、トリミングと［同じ幅］または［同じ高さ］の調整を反映した画像寸法が表示されます。提供元からファイル更新日時を取得できる場合は、その日時も表示されます。ファイル名または更新日時で並べ替えられますが、並べ替えても配置済み画像の位置は変わりません。

サムネイルをタップして選択します。［画像をトリミング］はその画像をトリミングし、［一括トリミング］は選択した画像にピクセルまたは百分率の余白指定を適用します。トリミングハンドルをドラッグするか、数値を入力してください。［トリミングをリセット］で元の端に戻せます。トリミングは非破壊で、元に戻すこともできます。

サムネイルを長押しするか、作業領域に配置済みの画像をドラッグし、強調表示された辺へドロップします。半透明のプレビューにはスナップ後の正確な結果が表示されます。右側への接続では上端がそろい、下側への接続では左端がそろいます。サムネイルをタップしてから「+」のターゲットをタップすることもできます。最初の画像は原点に配置されます。親画像をトリミングすると、そこに接続した画像も移動する場合があります。重なりは許可されません。

［同じ幅］と［同じ高さ］では、各画像固有の縦横比を維持したまま、すべての入力画像の寸法をそろえます。ピクセル、百分率、最小、最大から選択してください。［元のサイズに戻す］では寸法の統一だけを解除し、トリミングは保持します。

［配置解除］は選択した画像だけをトレイへ戻します。後続の画像は隙間を詰めますが、配置済みのままです。［削除］はその入力画像だけを削除します。［元に戻す］／［やり直し］でこれらの変更を復元できます。配置済み画像をドラッグすると並べ替えられ、空白部分をドラッグすると表示を移動できます。ピンチでズームできます。［すべて表示］は結合画像全体が見える倍率に変更するだけで、出力寸法は変更しません。

［PNG を保存］は結合済み画像を直接保存します。［Paintで編集］はメインエディターへ転送し、元に戻せる画像置換として扱います。出力がメモリ上限を超える場合は、選択画面が表示されたときに小さい出力コピーを選択してください。ごく小さい出力でもメモリ上限を超える場合は、サイズの選択画面の代わりにメモリ警告が表示されます。元の画像ファイルは変更されません。現在の結合状態は端末内に保存され、戻ってきたときに再度開かれます。

このモードには、メインエディターの［ファイル］→［このアプリについて・ライセンス・クレジット］メニューに記載されているものと同じ Catrobat/AGPL および素材クレジットが適用されます。

## Full new value

Android のファイル選択画面から最大20枚の画像を追加できます。下部のトレイには、サムネイル、ファイル名、トリミングと［同じ幅］または［同じ高さ］の調整を反映した画像寸法が表示されます。提供元からファイル更新日時を取得できる場合は、その日時も表示されます。ファイル名または更新日時で並べ替えられますが、並べ替えても配置済み画像の位置は変わりません。

サムネイルをタップして選択します。［画像をトリミング］はその画像をトリミングし、［一括トリミング］では選択した画像の各辺から切り取る量を、ピクセル数またはパーセントで指定します。トリミングハンドルをドラッグするか、数値を入力してください。［トリミングをリセット］でトリミング範囲を元画像全体に戻せます。トリミングは非破壊で、元に戻すこともできます。

サムネイルを長押しするか、作業領域に配置済みの画像をドラッグし、強調表示された辺へドロップします。半透明のプレビューにはスナップ後の正確な結果が表示されます。右側への接続では上端がそろい、下側への接続では左端がそろいます。サムネイルをタップしてから「+」のターゲットをタップすることもできます。スナップで配置する場合、最初の画像は原点に配置されます。親画像をトリミングすると、そこに接続した画像も移動する場合があります。スナップで配置する場合は、画像の重なりは許可されません。

画像を選択し、［正確な位置］でその左上隅の X 座標と Y 座標をピクセル単位で指定します。座標には 0 以上の整数を指定してください。他の画像の位置は変わらず、画像を重ねることもできます。

［同じ幅］と［同じ高さ］では、各画像固有の縦横比を維持したまま、すべての入力画像の幅または高さをそろえます。［ピクセル］、［パーセント］、［最小］、［最大］から選択してください。［元のサイズに戻す］では寸法の統一だけを解除し、トリミングは保持します。

［配置解除］は選択した画像だけをトレイへ戻します。他の画像は配置済みのままで、接続された画像が隙間を埋めるように移動する場合があります。［削除］はその入力画像だけを削除します。［元に戻す］／［やり直す］でこれらの変更を取り消したり、やり直したりできます。配置済み画像をドラッグすると配置を変更でき、空白部分をドラッグすると表示を移動できます。ピンチでズームできます。［すべて表示］は結合画像全体が見える倍率に変更するだけで、出力寸法は変更しません。

［PNG を保存］は結合済み画像を直接保存します。［Paintで編集］では、結合画像でメインエディターの画像を置き換えます。この置き換えは元に戻せます。出力がメモリ上限を超える場合は、選択画面が表示されたときに小さい出力コピーを選択してください。ごく小さい出力でもメモリ上限を超える場合は、サイズの選択画面の代わりにメモリ警告が表示されます。元の画像ファイルは変更されません。現在の結合状態は端末内に保存され、戻ってきたときに再度開かれます。

このモードには、メインエディターの［ファイル］→［このアプリについて・ライセンス・クレジット］メニューに記載されているものと同じ Catrobat/AGPL および素材クレジットが適用されます。

## Paragraph diff

```diff
--- Japanese Help before
+++ Japanese Help after
@@ -1,13 +1,15 @@
 Android のファイル選択画面から最大20枚の画像を追加できます。下部のトレイには、サムネイル、ファイル名、トリミングと［同じ幅］または［同じ高さ］の調整を反映した画像寸法が表示されます。提供元からファイル更新日時を取得できる場合は、その日時も表示されます。ファイル名または更新日時で並べ替えられますが、並べ替えても配置済み画像の位置は変わりません。
 
-サムネイルをタップして選択します。［画像をトリミング］はその画像をトリミングし、［一括トリミング］は選択した画像にピクセルまたは百分率の余白指定を適用します。トリミングハンドルをドラッグするか、数値を入力してください。［トリミングをリセット］で元の端に戻せます。トリミングは非破壊で、元に戻すこともできます。
+サムネイルをタップして選択します。［画像をトリミング］はその画像をトリミングし、［一括トリミング］では選択した画像の各辺から切り取る量を、ピクセル数またはパーセントで指定します。トリミングハンドルをドラッグするか、数値を入力してください。［トリミングをリセット］でトリミング範囲を元画像全体に戻せます。トリミングは非破壊で、元に戻すこともできます。
 
-サムネイルを長押しするか、作業領域に配置済みの画像をドラッグし、強調表示された辺へドロップします。半透明のプレビューにはスナップ後の正確な結果が表示されます。右側への接続では上端がそろい、下側への接続では左端がそろいます。サムネイルをタップしてから「+」のターゲットをタップすることもできます。最初の画像は原点に配置されます。親画像をトリミングすると、そこに接続した画像も移動する場合があります。重なりは許可されません。
+サムネイルを長押しするか、作業領域に配置済みの画像をドラッグし、強調表示された辺へドロップします。半透明のプレビューにはスナップ後の正確な結果が表示されます。右側への接続では上端がそろい、下側への接続では左端がそろいます。サムネイルをタップしてから「+」のターゲットをタップすることもできます。スナップで配置する場合、最初の画像は原点に配置されます。親画像をトリミングすると、そこに接続した画像も移動する場合があります。スナップで配置する場合は、画像の重なりは許可されません。
 
-［同じ幅］と［同じ高さ］では、各画像固有の縦横比を維持したまま、すべての入力画像の寸法をそろえます。ピクセル、百分率、最小、最大から選択してください。［元のサイズに戻す］では寸法の統一だけを解除し、トリミングは保持します。
+画像を選択し、［正確な位置］でその左上隅の X 座標と Y 座標をピクセル単位で指定します。座標には 0 以上の整数を指定してください。他の画像の位置は変わらず、画像を重ねることもできます。
 
-［配置解除］は選択した画像だけをトレイへ戻します。後続の画像は隙間を詰めますが、配置済みのままです。［削除］はその入力画像だけを削除します。［元に戻す］／［やり直し］でこれらの変更を復元できます。配置済み画像をドラッグすると並べ替えられ、空白部分をドラッグすると表示を移動できます。ピンチでズームできます。［すべて表示］は結合画像全体が見える倍率に変更するだけで、出力寸法は変更しません。
+［同じ幅］と［同じ高さ］では、各画像固有の縦横比を維持したまま、すべての入力画像の幅または高さをそろえます。［ピクセル］、［パーセント］、［最小］、［最大］から選択してください。［元のサイズに戻す］では寸法の統一だけを解除し、トリミングは保持します。
 
-［PNG を保存］は結合済み画像を直接保存します。［Paintで編集］はメインエディターへ転送し、元に戻せる画像置換として扱います。出力がメモリ上限を超える場合は、選択画面が表示されたときに小さい出力コピーを選択してください。ごく小さい出力でもメモリ上限を超える場合は、サイズの選択画面の代わりにメモリ警告が表示されます。元の画像ファイルは変更されません。現在の結合状態は端末内に保存され、戻ってきたときに再度開かれます。
+［配置解除］は選択した画像だけをトレイへ戻します。他の画像は配置済みのままで、接続された画像が隙間を埋めるように移動する場合があります。［削除］はその入力画像だけを削除します。［元に戻す］／［やり直す］でこれらの変更を取り消したり、やり直したりできます。配置済み画像をドラッグすると配置を変更でき、空白部分をドラッグすると表示を移動できます。ピンチでズームできます。［すべて表示］は結合画像全体が見える倍率に変更するだけで、出力寸法は変更しません。
+
+［PNG を保存］は結合済み画像を直接保存します。［Paintで編集］では、結合画像でメインエディターの画像を置き換えます。この置き換えは元に戻せます。出力がメモリ上限を超える場合は、選択画面が表示されたときに小さい出力コピーを選択してください。ごく小さい出力でもメモリ上限を超える場合は、サイズの選択画面の代わりにメモリ警告が表示されます。元の画像ファイルは変更されません。現在の結合状態は端末内に保存され、戻ってきたときに再度開かれます。
 
 このモードには、メインエディターの［ファイル］→［このアプリについて・ライセンス・クレジット］メニューに記載されているものと同じ Catrobat/AGPL および素材クレジットが適用されます。
```
