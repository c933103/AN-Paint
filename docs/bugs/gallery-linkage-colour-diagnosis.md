# Gallery reports every native linkage failure as the colour converter

**Status:** Open shared source-context diagnostic bug; documentation-only tracking PR. No fix is applied. **Baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`. Independently reviewed static paths and complete English/French/Japanese values; no runtime/provider/native incident, outage or security vulnerability is claimed. Faithful translations share the source mismatch. [Board](https://github.com/c933103/AN-Paint/pull/39) · [French review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182795516) · [Japanese review](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182776352).

## Expected and actual

Expected: gallery import identifies the failed component only when known, or gives a truthful generic image-component/decoder failure explanation.

Actual: the gallery's broad `LinkageError` catch always uses `colour_converter_unavailable`: “The image colour converter could not start. The image was not imported.” Its validation path can instead initialize another native decoder, such as `anpaint_jxl`, without calling the platform colour converter.

Impact: if a different native component fails to load/link, the user is told the colour converter failed. This is a condition-specific diagnostic mismatch, not evidence that the shipped JXL library or converter is currently missing or broken.

## Static path and evidence

- [MediaGalleryActivity.kt L358–359,L378–381](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L358-L381) validates a downloaded image through `ImportedImage` and catches any `LinkageError` with the colour-converter-specific message.
- [IllustrationSource.kt L22–35,L46](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L22-L46) permits raster extensions including JXL subject to the full provider URL policy.
- [ImageImport.kt L116–128](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageImport.kt#L116-L128) detects JXL, skips `PlatformImageColour` for it, and obtains dimensions through `JxlCodec`.
- [JxlCodec.kt L10–21](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/JxlCodec.kt#L10-L21) initializes `anpaint_jxl` for `Native.info`; native library load/linkage can raise a different component's error.
- Current resource: [EN L554](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L554), [FR L580](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L580), [JA L628](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L628). Retain the specific resource where actual colour-converter startup is the established failure.

## Bounded fix and acceptance

- Give the broad gallery catch a generic truthful component/decoder message, or preserve typed component-specific provenance. Do not label every `LinkageError` as colour conversion.
- Exercise controlled JXL native-initialization failure on the real gallery-validation path and verify the generic/component-accurate diagnostic with no imported result. Use a supported test seam, not altered production libraries or system security.
- Separately test genuine converter startup on editor decode or an end-to-end gallery insertion after handback: [ImageImport.kt L124,L128–141](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageImport.kt#L124-L141) only reads platform colour metadata during construction; [decode L160–165](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageImport.kt#L160-L165) calls `colour.convert`, whose [PlatformImageColour.kt L45–59](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PlatformImageColour.kt#L45-L59) catches actual converter linkage errors precisely. The editor invokes decode at [ClassicPaintActivity.kt L1300–1307](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1300-L1307). Do not inject a converter failure into gallery validation, where the converter has not started.
- Keep successful JXL/platform-colour import controls, policy checks, failure cleanup and no-document-mutation behavior.
- Enumerate emitters and affected localized values; preserve precise converter wording at actual converter-specific sites. Review all new/changed complete values and run focused current-source codec/error-routing tests.

## Next action

Implement bounded failure classification/message selection and prove the actual conditional paths under test before closing. This independent cause does not assert a live native incident and does not authorize changes to package/security configuration. Tracker changes documentation only; no application/resource/test edits, runtime pass or release.
