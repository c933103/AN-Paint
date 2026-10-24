# Independent Amharic normalization-label review

Result: 3 RETAIN, 0 REVISE, 3 HOLD. No production changes.

Input seal: `e89ed5d8ab634f777cabe9bac2c52ec3a2ea27332a13749772e555a9edd0c27a`. Production snapshot: `66be61df27c5359bffc32d56db21f3949899f873`.

RETAIN is independent textual-review support for the exact draft, not native-speaker, visual-fit, runtime or production acceptance. HOLD is unresolved full-phrase assurance, not a finding that a draft is wrong. Prior 66 ready/eight held remain separate.

## Verified evidence

- All 37 manifest files match the supplied seal; all 12 complete source files reproduce their bound Git blobs.
- All 10 retained lexical snapshots match their hashes/byte counts; all 27 exact records match their stated source lines.
- The six canonical English values/attributes match; all six are still absent from production Amharic. Coverage remains 12 present / 705 missing of 717 translatable containers.
- Freshness of the supplied commit/tree is dossier provenance, not a new remote query by this reviewer.

## Per-key decisions

### string/ui_same_width — HOLD

English: Same width

Exact draft: ተመሳሳይ ስፋት

Confidence: Medium lexical/structural plausibility; insufficient full-label semantic/idiomatic assurance for release.

The draft is a plausible adjective-plus-dimension noun phrase, but this review cannot sufficiently establish that the complete short label unambiguously means one equal/common width rather than similar width. The LO Fontwork and locale records plus the AOSP dimension noun are not full-label validation. No mistranslation is established; the hold is evidentiary, not an instruction to rewrite.

Consumer check: The toolbar opens the WIDTH dialog; it does not immediately normalize. Apply later gives all assembly inputs the same selected-axis pixel target. Other dimensions follow each crop ratio, subject to integer rounding. No equal file size, area, whole-image shape, or equal height claim.

What remains: A competent contextual Amharic review must assess the complete phrase as both the toolbar opener and dialog title, with exact shared width and independently proportional cropped heights. An exact corpus match is not a universal requirement, but component lookup alone is not enough.

Variants: እኩል ስፋት remains an unaccepted alternative. Do not substitute it solely to remove an English ambiguity without complete-label review.

Evidence IDs: width_aosp_image, same_height_lo_fontwork, same_lo_locale, equalize_width_variant

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L97-L98, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L268-L271, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L17-L38, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L19-L32, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L123-L124

### string/ui_same_height — HOLD

English: Same height

Exact draft: ተመሳሳይ ቁመት

Confidence: Medium lexical/structural plausibility; insufficient full-label semantic/idiomatic assurance for release.

AOSP supports ቁመት for image height, while the actual LO Same Letter Heights record uses እርዝመት. The proposed shortened/substituted phrase is new. Its exact common-height reading, rather than similarity or vertical alignment, is not sufficiently independently established by the retained evidence.

Consumer check: The toolbar opens the HEIGHT dialog, not immediate resizing. Apply normalizes selected-axis height for every input and computes each width separately from that image crop, subject to integer rounding. No matching shape, equal width or aligned-position claim.

What remains: Review the complete phrase in both toolbar/title uses with common height, crop-proportional widths and all-input scope. Prior acceptance of the dimension noun cannot stand in for this check.

Variants: Preserve the real LO እርዝመት variation and both supplied alternatives without silently accepting or flattening them.

Evidence IDs: height_aosp_image, same_height_lo_fontwork, equalize_height_variant

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L97-L98, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L268-L271, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L17-L38, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L19-L32, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L123-L124

### string/ui_smallest — RETAIN

English: Smallest

Exact draft: ትንሹ

Confidence: High lexical confidence; medium-high source-context confidence. No native-reader or UI-fit claim.

The exact complete short label ትንሹ is present in the nonfuzzy LO Smallest entry, and the separately retained smallest-width and smallest-height records corroborate the dimension sense. In this dialog it is a noun-omitting preset just as the English is, not an imperative or a whole-image selection. No evidence-backed revision is needed.

Consumer check: Preset derives the minimum current placedSize value on the chosen axis across all inputs at dialog opening, including tray inputs. It updates input/preview only. It is not minimum file bytes, area, original uncropped dimensions or an immediate resize. Existing percentage display/rounding is not a translation promise.

What remains: Retain the exact draft for this independent textual review; rendering/accessibility/native-reader acceptance and implementation remain separate.

Variants: Keep AOSP አነስተኛ as a genuine cross-context variant, not automatically preferable. Exclude the contradictory smallest-percent sentence containing largest wording.

Evidence IDs: smallest_exact, smallest_width_context, smallest_height_context, smallest_aosp_variant, smallest_percent_bad_prose

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L19-L21, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L34-L36, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L63-L66, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L78-L85

### string/ui_largest — RETAIN

English: Largest

Exact draft: ትልቁ

Confidence: High lexical confidence; medium-high source-context confidence. No native-reader or UI-fit claim.

The complete ትልቁ label has an exact nonfuzzy LO Largest record plus greatest-width and greatest-height corroboration. The short definite superlative preserves the English noun omission without adding an operation or a different measurement.

Consumer check: Preset derives the maximum current placedSize chosen-axis value across all inputs at dialog opening and stages input/preview only. The maximum is also the percent baseline, not a bound on custom targets. It is not area or file size.

What remains: Retain the exact draft for this independent textual review; rendering/accessibility/native-reader acceptance and implementation remain separate.

Variants: No evidence-backed wording change proposed.

Evidence IDs: largest_exact, greatest_width_context, greatest_height_context

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L19-L35, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L63-L66, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L78-L85

### string/ui_apply_to_all — RETAIN

English: Apply to all

Exact draft: ለሁሉም ተግብር

Confidence: Medium-high whole-command and context confidence, strengthened by new complete-phrase evidence; no native-reader/UI-fit claim.

New independent evidence supplies the exact full command: ICT Development Office/ELRC glossary entry 152, page 12, pairs Apply to All with ለሁሉም ተግብር and defines all-item application. The full Amharic column was visually checked against extracted text. This closes the dossier component-only gap. The target-before-imperative construction preserves both operation and all-item scope; no noun-label or selected-only substitution is justified.

Consumer check: The positive dialog button validates the target then applies normalization to the complete assembly state, including unplaced tray images. It changes project metadata/history, not source-file pixel content. Reflow may adjust attachments. All is bounded by this assembly, not every device image.

What remains: Retain this exact draft under the augmented evidence, not solely on Apply + for-all components. Preserve the mirror/source-age and non-native-review limitations.

Variants: The LO exact-English Apply to All record remains excluded because its msgstr is empty; new evidence does not retroactively make that record translated. LO መፈጸሚያ remains a real generic Apply variant, not an instruction to change the command.

Evidence IDs: apply_aosp, for_all_aosp, to_all_lo, apply_lo_variant, apply_all_untranslated, elrc_apply_to_all_152

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L37-L48, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L78-L85, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L123-L151, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L233-L248

### string/ui_restore_original_sizes — HOLD

English: Restore original sizes

Exact draft: ዋናዎቹን መጠኖች መልስ

Confidence: Medium component evidence; low-to-medium confidence in complete plural restoration command and original-versus-main reading.

Maintain the author idiom hold. Singular ዋናው መጠን, plural መጠኖች and restoration verbs do not establish the plural adjective/object command ዋናዎቹን መጠኖች መልስ. This review cannot confidently resolve original rather than main sizes or the complete object/adjective idiom. No alternative is approved.

Consumer check: Unlike the presets, this button immediately calls resetSizes and dismisses on success. It sets normalization to null for every input, retains crop/source-dimension/file data, and returns effective dimensions to each retained croppedSize. Attached placement can reflow. This is not global Undo, previous arbitrary sizing, source-file restoration, or resetting crops.

What remains: A competent contextual Amharic reviewer must assess the full plural command and the intended original-size reading, without promising uncropping, file rollback or global Undo. Any English-source defect established later must be fixed in English and tracked across affected languages, not patched silently in Amharic.

Variants: Do not inherit the prior singular Original size acceptance. Keep singular ዋነኛው evidence separate. Do not silently translate a different English operation such as Remove normalization.

Evidence IDs: original_size_ui, original_size_help_variant, original_size_return_context, original_size_restore_context, sizes_plural_component, restore_aosp, reset_lo_variant, restart_reset_exclusion

Source: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L68-L71, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L19-L32, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L123-L151, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L233-L248

## New full-command evidence

The [ICT Development Office/ELRC glossary, page 12, entry 152](https://oromianeconomist.com/wp-content/uploads/2017/08/ict-glossary-in-afaan-oromoo-amharic-and-tigarinya.pdf#page=12) gives the complete pair “Apply to All” → “ለሁሉም ተግብር”. Its meaning is application to every item. The downloaded 240-page PDF was extracted and page 12 visually inspected to confirm the correct language column.

The PDF attributes itself to those institutions, but the retrieval host is a public mirror rather than an authenticated institutional endpoint. SHA-256: `6eddbd874ac0710ac02cb959fd073d2501dc88404d88d29ee6ce20bc1941eab2`. Its metadata dates from 2011; no immutable publisher revision, institutional authentication, native-reader validation or rights to republish the complete PDF is asserted. The public review should cite the link and bounded exact record, not republish the whole glossary or page screenshot.

This strengthens only Apply to all. The previously empty LO exact-English record remains excluded. The phrase was not accepted merely by concatenating dictionary components.

## Source fidelity and scope

- Same width/height open dialogs. They are not immediate normalizations. Each selected-axis target is shared across all inputs; each other dimension is computed separately from that input’s crop with integer rounding.
- Smallest/Largest are current selected-axis dimension presets across all inputs, not area or bytes. They stage the field/preview; Apply commits. Percent uses the current largest dimension as baseline and has existing display/rounding behavior.
- Apply covers the entire assembly list, including unplaced tray inputs, not selected thumbnails alone.
- Restore acts immediately on success, removes all normalization metadata, retains crop rectangles and source file/dimension data, and can reflow attachments. It does not reset crops, roll back files, restore previous arbitrary sizes or invoke global Undo.

No English-source defect was established. The canonical help explicitly qualifies restoration as normalization removal with crop preservation. If English is later judged defective, correct it first and flag affected terms across languages, as instructed; do not silently change only the Amharic operation.

## Limits and stopping point

No Work task, production edit, remote publication, build, CI or release occurred. This review is complete at the static textual/evidence level. Three held compositions need contextual linguistic assurance before acceptance; no replacement is approved. This pass does not claim a native reader, UI rendering, accessibility or runtime validation. The supplied original dossier was not modified.
