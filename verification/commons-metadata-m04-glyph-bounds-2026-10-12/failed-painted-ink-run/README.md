# Independent PR55 painted-ink hosted artifact review

## Result: current acceptance FAILED

The exact-source run compiled and executed all **892 JVM identities**: **890 passed, two failed**, with no skipped, missing, extra or duplicate JVM identities. Both failures are confined to enlarged Arabic (font scale 2, 640×320 dp):

1. `shortLandscapeM04RetainsFullAccessibleTextAtDoubleScale`: COPY and INSERT each fail strict painted-ink containment by two pixels.
2. `paintedInkOracleRejectsNativeOverflowAndClippedEdgeGlyphsAtDoubleScale`: the Arabic **intact** baseline fails the same assertion before its mutants execute.

This is a real observed difference between the full native text raster and the clipped TextView raster. The zero-tolerance oracle remains failed. No alpha masking, tolerance increase, wording change, production repair or successful-control claim is substituted for the failure.

## Exact binding

- PR55 head: `e7855e04a1a4647a1fae3a14937df0c17c3f4d79`
- Base: `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- Synthetic merge: `9af58e46c6a7196ef90c60e345bcd7a5194ffacf`
- Reviewed published tree: `8752ed99c9350235da46fac1b4a188ca89296889`, 2,008 leaves
- [Run 38250189049](https://github.com/c933103/AN-Paint/actions/runs/38250189049)
- Regression artifact 11748136511, SHA-256 `68d730c96a2fe3e3144d5ce2e31a8eb3c3c76c80ee23fd4d43aa2c79bcd39e82`

Parent verified remote merge parents and the entire publication tree. This reviewer independently matched all eight reviewed source/inventory/provenance hashes to the immutable local tree, fetched official artifact/job metadata, downloaded the regression ZIP and verified its published digest. All **2,509 extracted regression files** exactly match the ZIP. Prior d802/4ff7 source, checker and failed-run reports remain frozen; no earlier result has been rebound.

## Exact pixel finding

For Arabic COPY, INSERT and the intact control, the content width is 1232 pixels and reference ink extends to x=1232 (right-exclusive 1233). The complete raster contains:

- Layout (1232,29), view (1256,29): reference RGBA `[0,0,36,7]`; actual RGBA `[0,0,0,0]`
- Layout (1232,30), view (1256,30): reference RGBA `[0,0,0,1]`; actual RGBA `[0,0,0,0]`

All three frames independently recompute to exactly two overflow, missing and differing pixels, zero reference-allocation edge contact, and zero ink outside the overall view. Thus the loss occurs at the content clip, not because the complete reference ran off its finite canvas. The complete glyph bounds reach x=1233, and the expanded reference includes them. COPY/control reference ink count is 13,885; INSERT is 14,370.

`inspect_arabic_overflow.py` and `arabic-overflow-pixels.json` reproduce every coordinate, RGBA value and hash. The original actual/reference images and JSON are copied byte-for-byte under `observed-ink/`; the exact failing JUnit XML is under `observed-junit/`. `selected-raw-evidence.json` maps each copy to its original artifact path. Both actual/reference COPY and INSERT PNGs were directly inspected; low-alpha pixel loss is established numerically, not by claiming conspicuous visible truncation.

## Complete inventory and partial controls

- Ordinary captures: **110/112** valid PNG+JSON pairs. Only enlarged Arabic COPY and INSERT success pairs are missing, as expected after their assertions fail.
- Normal-landscape diagnostics: **28/28**, with source/schema/UTF-16 coverage, line metrics, alpha statistics and finite-canvas edge flags independently checked. Their current normal-scale outcome is successful.
- The original Ainu normal COPY advance still reads 1233.043 against width 1232; the historical width-plus-one proxy is still false, while its observed ink overflow remains zero. That failed proxy is explicitly diagnostic, not silently declared passed.
- Painted-ink evidence: **100/120 complete triplets** exist, all 100 numerically recomputed; **97 satisfy their expected positive/negative classification**, and the three Arabic positive frames fail. Twenty triplets plus the double-scale summary are missing after the intact Arabic failure stops that method.
- Available frames comprise 36 live frames, ten intact control frames and 54 mutants. Of the planned 48 positive frames, 46 exist and 43 pass; of 72 mutants, 54 exist.
- The normal-scale receipt records all six intact profiles and 36 rejected mutants. At double scale, English, Ainu Kana and Tibetan emit their intact plus 18 mutants before Arabic fails. Arabic mutants and the subsequent Japanese/Nôm profiles do not execute.
- `audit_available_controls.py` independently matches all **54 emitted mutant pairs** to genuine integer translation or first/last spatial-column clipping, preserves every complete-reference glyph pixel, and proves nonzero affected ink. This partial evidence does not replace the absent double-scale completion receipt.

The fresh checker uses the exact 892-identity inventory and current schema. Eight synthetic checker tests exercise exact inventory, missing/duplicate cases, one-alpha/one-color-level pixels, wholly displaced ink, dishonest counts and a falsely reported but unapplied translation. These are checker tests, not native execution evidence.

## Other checked outcomes

- Exact-script resource generation: **PASS**, all seven probes, commands, exits, log hashes, task ordering and generated-resource bytes; ZIP and all eight extracted files independently verified.
- APK/source binding: **PASS**, artifact 11746749156, SHA-256 `7f2741e84e22682ce3e0b0b627ea93f6c262e2871bc29862953d052f1e49dc8c`. All 2,005 included tracked blobs are exact. Only the established `.gitignore`, `colorpicker/.gitignore`, `.idea/codeStyles/Project.xml` omissions occur. Additional source is confined to the four declared native-source roots. Embedded source matches the separate ZIP.
- All 14 font-directory assets, including licences and the unchanged Nôm font, match source exactly. Font SHA remains `6b70d3c5c146c9d11503e5dff7ade5e7ccb3ae5a70c511f71902d4a75f7a3006`.
- Actual APK aapt2 dump: **PASS**, default + exact 59 values + Korean alias = 61 configurations. Manchu U+180E remains at indices 7/18/27; Mongolian U+202F at 7/17/30. Compiled values do not themselves prove runtime shaping.
- Hosted Python: exit 0, 673 methods, **two skips**. Compact output positions map to the two optional Pillow ICO decoder tests; this mapping is explicitly an inference from exact-source discovery order, not a named skip-reason receipt. Local source review had separately run all 673 without skips.
- Native dependency phase: exit 0, 76.733 seconds. Lint: exit 0, 114.238 seconds. JVM: exit 1, 524.2 seconds.
- Official API35 emulator job summary is success. This review has not independently audited that job's installed-test identities/receipts; a successful job label is not reproduction of the enlarged Arabic clipping scenario.

## Limits before any repair

The evidence is native **Robolectric** clipping. It is not an installed-device clipping claim. The helper reached an explicit `layout.useBoundsForWidth == false` precondition. The app targets API35; [TextView's documented default](https://developer.android.com/reference/android/widget/TextView#setUseBoundsForWidth(boolean)) depends on target SDK and can reserve glyph-bound space. Actual installed TextView and Layout flags, compatibility behavior, fonts and geometry should therefore be inspected before a production geometry change. The source of any test/device difference is unproven.

The strict oracle should remain unchanged while that distinction is investigated. Linguistic correctness, universal shaping, hardware rendering, signing/upgradeability and full cross-version release verification are outside this bounded artifact conclusion. No source-publication or merge-readiness claim follows from the passing auxiliary jobs.

## Portable commands

All checkers use only immutable source reads and downloaded artifacts. Substitute paths without changing bindings:

```
python3 audit_ink_artifacts.py --repo CHECKOUT --artifact REGRESSION.zip --extracted REGRESSION --binding actual-binding.json --output artifact-result.json
python3 inspect_arabic_overflow.py observed-ink --output arabic-overflow-pixels.json
python3 audit_available_controls.py REGRESSION/Paintroid/build/reports/commons-metadata-m04-painted-ink --output available-native-controls.json
python3 -m unittest -v test_painted_ink_checker test_artifact_inventory
```

The aggregate artifact checker must exit nonzero for this run. Its diagnostic-integrity pass, partial-control consistency and APK success must not be confused with acceptance.
