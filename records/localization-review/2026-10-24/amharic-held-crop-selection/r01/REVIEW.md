# Independent adjudication: Amharic Crop to selection

24 October 2026. Scope: `string/ui_crop_to_selection` only.

## Decision: release the semantic hold with the revision

Accept **የተመረጠው ክፍል ብቻ እንዲቀር ከርክም** as the reviewed candidate, replacing **በምርጫው መጠን ከርክም**.

Meaning: **Crop so that only the selected part remains.**

This resolves the specific translation-precision hold. It does not implement the string, approve a production release, certify native usage, or claim rendered fit. The [English source](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/res/values/strings.xml#L123) remains **Crop to selection**. No English-source defect was established, so no cross-language source-change pass is triggered by this adjudication.

## Why the revision is supported

The old size phrase left open whether the command merely used selected dimensions. The revision instead places the selected part in a positive purpose clause as what remains. It retains an explicit crop command, rather than substituting Keep, Resize, Delete selection, or Deselect. The definite selected modifier, explicit part noun, restrictive word, and remain clause work together; this is not a judgment based on isolated dictionary substitutions.

- The image-editing imperative **ከርክም** directly corresponds to Crop in Android Gallery2's [Amharic resource](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#94) and [English resource](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values/strings.xml#191). That supports the operation verb, not the complete new sentence.
- Gallery2's [selected-item construction](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#54) and [Images only label](https://android.googlesource.com/platform/packages/apps/Gallery2/+/c0712a1daee50e52cd6f3e8e7698ddb8da3e1bcb/res/values-am/strings.xml#110) support the modifier and restrictive-word patterns. Item deletion is not treated as equivalent to region cropping.
- The inspected dictionary entries support **ክፍል** for part, **ቀረ** for remain in the be-left sense, and **ብቻ** for only: Leslau, *Concise Amharic Dictionary*, [printed page 429 / PDF page 428](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf#page=428), [printed page 456 / PDF page 455](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf#page=455), and [printed page 423 / PDF page 422](https://lojs.org/wp-content/uploads/2019/11/Concise-Amharic-Dictionary-Amharic-to-English-English-to-Amharic.pdf#page=422).
- Leslau's *An Amharic Reference Grammar*, section 94.3, explains the conjunction forms at [printed page 443 / PDF page 425](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=425) and the positive-simple-imperfect purpose construction at [printed page 445 / PDF page 427](https://e-learning.tsu.ge/pluginfile.php/6774/mod_resource/content/0/amharic_rg.pdf#page=427). Main and subordinate subjects may differ. Applying that productive grammar gives **እንዲቀር**, so that it remains, with the selected part as subject and crop as the main command. This is grammatical composition, not a claim that the book quotes the proposed label.
- Adafre's [noun-phrase analysis, printed pages 45–46](https://aclanthology.org/2004.eamt-1.6.pdf#page=3) supports prenominal modifiers and distinguishes direct-object marking. The selected part is the subject of remain here; adding accusative **ን** would change that analysis.

My independent full-phrase judgment is that the revised clause is semantically precise and grammatically supported in this context. Requiring an identical pre-existing software sentence would add no demonstrated protection against the original error. Conversely, the availability of lexical pieces alone would not suffice without this clause-level analysis.

## Agreement with the actual operation

The [Edit command](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L848-L860) acts on a selection. [Extraction](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L289-L311) carries selected pixels and any mask, not merely dimensions. The [rendering path](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L348-L364) uses the selected image with its current transform inside the [axis-aligned enclosing bounds](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/SelectionGeometry.kt#L8-L24). [Cropping](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L461-L465) replaces the canvas with that rendered result. Floating content outside the old canvas may therefore survive.

“Only the selected part” accurately describes which artwork is retained. It does not promise an irregularly shaped canvas or preservation of transparency. [Replacement](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L197-L218) flattens transparent mask, rotation, or import margins against the current background and clears the selection. Generated background margins do not turn this into retention of unselected artwork. The wording also makes no promise that undo restores an editable floating selection; [history restoration](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintDocument.kt#L230-L244) is raster-state restoration after the crop's preceding floating-content commit.

## Alternatives, confidence, and the remaining check

Keep the explicit **ክፍል** rather than removing it solely to shorten the caption. The shorter purpose-clause alternative is plausible, but no observed fit failure justifies trading away that clarity now. The according-to-selected alternative leaves the retained-versus-removed relation less explicit. A direct crop-selected-part object construction could instead suggest trimming the selection itself. Bare Crop loses selection scope.

Confidence: source semantics high; grammatical construction high; full-phrase semantic fit medium-high; modern UI idiom medium; rendered fit unassessed. No native-reader judgment is claimed. The dictionary and grammar are by the same author and are not counted as independent authors.

The candidate has 24 Unicode characters including spaces, versus 14 in the held text. The [compact command tile](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/RibbonWidgets.kt#L60-L124) normally provides a 64dp square with at most two horizontal caption lines. During implementation, inspect actual Amharic rendering at supported font scales and confirm the visible caption remains useful and the full accessible name and tooltip are correct. The main verb is at the end, so truncation deserves particular attention. No clipping or accessibility failure was observed or measured in this review. This is an implementation verification item, not a continuing semantic hold.

## Verification and disposition

- Independently verified all 682 supplied manifest entries and all 591 supplied source-file bindings against the complete supplied Git tree, with no mismatches or missing files in the audited extensions. This establishes input consistency, not an independent live-branch freshness check.
- Confirmed one direct production reference to the key, the exact English text, and absence of the key from the current Amharic resource. The proposed value is NFC, parses in an XML fragment, and adds no formatting placeholders.
- Visually inspected the cited grammar and dictionary pages. Inspected the supplied Gallery2 XML and the GIMP record. The [exact-looking GIMP label](https://github.com/GNOME/gimp/blob/7d518c7971e80719ce30f70ec44b55e49ab2aeb7/po/am.po#L3274-L3283) remains excluded because it is fuzzy and the accompanying description is untranslated.
- The adjudication moves this one candidate from held to ready when incorporated into the review ledger: the supplied 103 ready / 5 held / 0 implemented would become **104 ready / 4 held / 0 implemented**. The pending 90 remain unchanged. This report itself does not edit that ledger.
- No production resource change, Work task, application execution, build, application test, CI, publication, deployment, or release occurred. Artifact integrity/XML checks are not application tests.

