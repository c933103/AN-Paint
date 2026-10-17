# Four-language crop guidance and same-entry Help corrections

Project: c933103/AN-Paint. Tracker: [PR75](https://github.com/c933103/AN-Paint/pull/75).
Application head: `667ea44539f33a1406a19e65120eeaed60e03bd1`.
Final base: `f988a94d8e4fa300bfe181ba67bba7b546651ca1`; final application tree: `0925675f6618d06cad25177c3da9d4bc7dd3e653`.

## Bounded correction

German, Spanish (Spain), Italian and Portuguese (Portugal) have one complete assembly Help value and both crop-preview quantity forms corrected. All warnings now name attached images and qualify movement as possible. No attachment, geometry, crop or undo implementation changed.

Complete-entry review also corrected demonstrated differences within those same Help values:
- German: the ghost preview is semitransparent.
- Spanish: Crop and Remove references match current labels; pinch supports zooming out too.
- Italian: tray dimensions include normalization; current normalization-unit labels are retained; pinch is bidirectional; smaller-copy selection is conditional and an impossible minimum output gives a memory warning.
- Portuguese: the same dimension/output/zoom guidance, plus the current Desfazer/Refazer label.

This changes exactly two keys per locale (four Help values and eight plural forms), with complete reviewed values retained in a compact test fixture. Help remains P3 and crop previews remain P2. Other resource entries, accepted EN/FR/JA/HK/LT/AR/RU/KO subsets, priority files, prior receipts and untranslated/unreviewed obligations remain unchanged. This is not whole-language or native-speaker approval.

## Full-value and consumer evidence

The four language reports include entire English/old/new values, all quantity categories, concrete consumers, model behavior, source hashes and limits. Initial review was against develop `8c08554995f4d07be1b47736746ab2d0771e810e`. The final composition incorporates merged #117/#119 at `f988a94d`; all four localized source inputs, English guidance, AssemblyActivity, AssemblyCanvas, ImageAssembly, ImageCropDialog, normalization and locale routing remain identical. Three ancillary image-size/budget helpers changed numeric formatting only; their final comparison is recorded.

Five focused host contracts check complete values, seven Help paragraphs, every plural form, exact argument types and newline structure, 48 malformed-resource mutations, current control labels, conditional image movement, and preserved P3/P2 priority. Twelve separate old-value controls prove that restoring any former complete Help/plural value is rejected.

Three new Robolectric methods exercise compiled complete Help/quantity resources and the actual Help button plus batch-crop toolbar. The latter checks placed/attached synthetic images; counts 0/1/2; trim, reset, cancel and reopen; and unchanged image bytes, geometry, attachment metadata and persisted state on cancellation. These are authored and supplementary-compiled tests, not locally executed Android results. Existing RIGHT/BOTTOM moving/stationary, relationship, Undo/Redo and no-attached-image model coverage is unchanged and remains part of the hosted suite.

## Checks and truthful limits

- Final composition: all 893 host tests passed normally and optimized. Exact commands, timings and logs are in `final/`.
- Five focused tests passed in both modes; 12 old-value rejection controls passed.
- Canonical translation structural validation passed.
- AAPT2 compiled and linked the full final resources.
- The new test and existing pixel-decoder helper compiled with Kotlin 1.9.24/API35, fresh resource symbols and previously compiled dependency classes. This is supplementary API/source compilation, not a clean Gradle build.
- Full Gradle/Robolectric execution was attempted and blocked at the wrapper download by `Network is unreachable`; no lint/APK/device execution is claimed locally. Hosted exact-head gates remain necessary.
- The two earlier 8c host runs failed because a JVM perf-data file lock warning appeared on stdout in an unrelated caption-tile numeric probe. Those logs are preserved. The unchanged focused caption tests passed with `JAVA_TOOL_OPTIONS=-XX:-UsePerfData`; the final regular host runs also passed. Both additional no-perf full runs passed all 893 tests (normal 222.833 s; optimized 220.700 s), separately recorded rather than overwriting the failure.
- An initial supplementary compile omitted an existing test helper from its source list; its preserved failure was resolved by including that helper. No production or test assertion was weakened.

All 1,188 final-base blobs were matched by content/mode. All 1,191 resulting remote leaves, modes and hashes match the reviewed candidate; the seven intended paths are the entire diff. The commit has the expected f988a94d parent. No bulk evidence is added to the application tree.

## Remaining boundary

The shared English Help's snapping/origin/overlap/gap-filling statements have a broader applicability question when Exact position is used. Spanish and Portuguese reviewers explicitly identify this source-wide issue. It is preserved rather than silently changing four translations ahead of the source contract. Keep PR75 open pending reconciliation of its full recorded counterpart scope; this bounded patch does not close that tracker. Separate untranslated/unreviewed language and layout/accessibility obligations remain open.
