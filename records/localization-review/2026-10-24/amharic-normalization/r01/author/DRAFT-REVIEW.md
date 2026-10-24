# Amharic assembly normalization: original draft dossier

Production 66be61df27c5359bffc32d56db21f3949899f873; tree 870c5a584120d92710be516af0dc3b3847b183d9. Twelve complete source copies are supplied, exact Git blobs checked against freshly retrieved production tree.

No independent acceptance or implementation. Prior66 ready/eight held remain separate.

## string/ui_same_width

English: Same width

Proposed XML: `<string name="ui_same_width">"ተመሳሳይ ስፋት"</string>`

Status: review

Confidence: medium-high lexical components; medium whole-label idiom; unaccepted

Original concise Same + image Width composition. AOSP pairs Width with ስፋት, and LO attests ተመሳሳይ for Same, including a heights context. The complete two-word phrase is not an exact source match. It labels the shared-width dialog/action without promising identical whole-image size.

Toolbar button opens normalization dialog for WIDTH and same key is dialog title. Gives all inputs common target width; each other dimension derives proportionally from its own current crop with integer rounding. Does not mean identical total sizes, same heights, equal file sizes or identical aspect ratios. Includes unplaced inputs in tray.

['Must mean one common width for every input, while each height follows its own cropped aspect ratio; not approximate similarity, equal file size, equal height or frozen scale.', 'Native contextual review must confirm that ተመሳሳይ reads as same/equal rather than merely similar in this short title.', 'Keep adjective/noun construction suitable both for toolbar button and dialog title.', 'Original AI-authored draft, unaccepted and not implemented. No native-speaker, visual-fit, accessibility or runtime acceptance is claimed.', 'No Work task, production edit, app build, CI, release or remote write was performed.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L97-L98, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L268-L271, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L17-L38, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L19-L32, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L123-L124

## string/ui_same_height

English: Same height

Proposed XML: `<string name="ui_same_height">"ተመሳሳይ ቁመት"</string>`

Status: review

Confidence: medium-high lexical components; medium whole-label idiom; unaccepted

Original Same + image Height composition. Select the directly attested AOSP image noun ቁመት, consistent with the prior reviewed dimension noun; retain rather than erase LO እርዝመት variation. Prior singular/dimension acceptance does not accept this label.

Toolbar button opens HEIGHT normalization dialog and same key is title. Sets all inputs common target height, computes each width from own crop aspect ratio with integer rounding. Not width, file size, alignment position or guaranteed identical shape.

['Must mean one common height for all inputs, preserving each crop ratio; not vertical alignment, same width or identical image shape.', 'The source Fontwork Same Letter Heights uses እርዝመት; replacing it with the AOSP image noun is an explicit original adaptation.', 'Native review must check same-versus-similar reading and shared button/title fit.', 'Original AI-authored draft, unaccepted and not implemented. No native-speaker, visual-fit, accessibility or runtime acceptance is claimed.', 'No Work task, production edit, app build, CI, release or remote write was performed.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L97-L98, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L268-L271, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L17-L38, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L19-L32, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L123-L124

## string/ui_smallest

English: Smallest

Proposed XML: `<string name="ui_smallest">"ትንሹ"</string>`

Status: review

Confidence: high lexical; medium-high contextual short-label confidence; unaccepted

Exact nonfuzzy LO Smallest → ትንሹ, corroborated by Fit to smallest width/height. Reuse the short superlative, not the external numeric-filter or layout behavior.

Preset button fills target field with minimum current placedSize selected-axis value among all inputs at dialog creation. It is smallest width in WIDTH mode, smallest height in HEIGHT mode, including current crop/normalization. Does not mean area, file size or smallest memory-safe copy. Button updates field/preview only; Apply to all commits.

['The omitted noun is the current selected-axis dimension: minimum placedSize width or height, not area, file bytes, resolution total or memory-safe size.', 'The button only fills the target/preview; it does not apply resizing until Apply to all.', 'AOSP alternative አነስተኛ is preserved separately; exclude contradictory neighboring LO smallest-percent prose.', 'Original AI-authored draft, unaccepted and not implemented. No native-speaker, visual-fit, accessibility or runtime acceptance is claimed.', 'No Work task, production edit, app build, CI, release or remote write was performed.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L19-L21, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L34-L36, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L63-L66, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L78-L85

## string/ui_largest

English: Largest

Proposed XML: `<string name="ui_largest">"ትልቁ"</string>`

Status: review

Confidence: high lexical; medium-high contextual short-label confidence; unaccepted

Exact nonfuzzy LO Largest → ትልቁ, independently corroborated by greatest-width/height labels. Matches the comparative preset without adding area, file-size or apply-action semantics.

Preset button fills target field with maximum current placedSize selected-axis value among all inputs at dialog creation. Largest width or height depending mode, not total area/file size. Updates field/preview only; subsequent Apply commits. This largest value is also percent baseline.

['Means maximum current placedSize selected-axis dimension among all inputs at dialog creation. It is also the percent baseline, not a guaranteed upper bound on custom input.', 'The button updates target/preview only; applying remains a separate action.', 'The short adjective omits width/height as the English does; inspect both dialogs in contextual review.', 'Original AI-authored draft, unaccepted and not implemented. No native-speaker, visual-fit, accessibility or runtime acceptance is claimed.', 'No Work task, production edit, app build, CI, release or remote write was performed.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L19-L35, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L63-L66, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L78-L85

## string/ui_apply_to_all

English: Apply to all

Proposed XML: `<string name="ui_apply_to_all">"ለሁሉም ተግብር"</string>`

Status: review

Confidence: medium-high component evidence; medium whole-command idiom; unaccepted

Original command joining attested to/for all ለሁሉም with exact AOSP Apply → ተግብር. The exact LO Apply to All record has an empty translation and is explicitly excluded. Preserves all-input scope, not selected-image scope.

Positive dialog button validates target then normalizes entire assembly.images/state list, including unplaced inputs, not selected thumbnails only. Sets same selected-axis dimension preserving each crop aspect ratio; writes project metadata/history, not source image pixel files. May reflow attached placement.

['No eligible whole-phrase attestation was found in the bounded corpus; the full phrase is original composition.', 'Applies normalization to every assembly input, including unplaced images, not only selected thumbnails and not every image on the device.', 'Native review should check imperative register against the retained LO noun-label alternative; no automatic register preference is claimed.', 'Original AI-authored draft, unaccepted and not implemented. No native-speaker, visual-fit, accessibility or runtime acceptance is claimed.', 'No Work task, production edit, app build, CI, release or remote write was performed.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L37-L48, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L78-L85, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L123-L151, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L233-L248

## string/ui_restore_original_sizes

English: Restore original sizes

Proposed XML: `<string name="ui_restore_original_sizes">"ዋናዎቹን መጠኖች መልስ"</string>`

Status: hold

Confidence: medium lexical components; low-to-medium plural-command idiom; HOLD

Original plural restoration command built from singular Original Size → ዋናው መጠን, attested plural sizes መጠኖች, and AOSP restore verb መልስ. The plural adjective/object inflection and complete command are original, not covered by prior singular acceptance. Retains current English wording rather than silently changing it to Remove normalization.

Immediate button removes every normalization record (sets null), then closes dialog. Retains crops, source dimensions/files and other image records; effective size becomes croppedSize, not necessarily uncropped file dimensions. reflow may relocate attachments to fit. This is not resetting crop, restoring file contents, restoring previous arbitrary size or global undo. Existing English explanation states normalization removal and crop preservation.

['IDIOM HOLD: no exact plural restoration command was established. Independent review must confirm that ዋናዎቹን መጠኖች naturally means the original sizes rather than main sizes, and confirm object/adjective grammar.', 'This button acts immediately, removes normalization on all inputs and closes the dialog; it does not merely stage a preset.', 'Effective sizes return to each retained crop size. Crops, source files and original source-dimension metadata remain; attached placement may reflow. Do not imply uncropping, file rollback, prior arbitrary size or global Undo.', 'No English defect is established: canonical English help explicitly states normalization removal and crop preservation. Keep that contextual qualification in review; do not rewrite the Amharic label into a different operation.', 'Alternative ዋነኛው is an actual source variant only in the singular. Neither its plural nor the draft plural gets inherited acceptance.', 'Original AI-authored draft, unaccepted and not implemented. No native-speaker, visual-fit, accessibility or runtime acceptance is claimed.', 'No Work task, production edit, app build, CI, release or remote write was performed.']

Consumers: https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt#L68-L71, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L19-L32, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L123-L151, https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageAssembly.kt#L233-L248

## Shared scope and evidence limits

AssemblyActivity opens NormalizeImagesDialog, which derives current placed dimensions, offers unit/preset targets and invokes ImageAssembly.normalize/resetSizes. ImageAssembly computes proportional other dimension from crop, reflows attachment metadata and records state/history. All source copies complete. No rendering, native naturalness or exhaustive repository-wide search claim.

No English defect established in this bounded scope. Restore original sizes is contextual to normalization and keeps crops, supported by current canonical explanatory help. Preserve that distinction; if English wording is separately judged defective, correct source first and flag all affected languages rather than silently changing Amharic alone.

Six plain labels have no placeholders or explicit units. Related percentage/numeric result templates and full Help remain outside translation scope.

Full lexical reasoning, exact records, source snapshots and retrieval/reuse limitations are in lexical-evidence/. Nonfuzzy is a record flag, not proof of correctness. Component and cross-context evidence does not establish exact full-phrase native acceptance.

Original drafts only; independent checking required.

No transfer of prior singular Original size acceptance to plural restoration command.

No whole Help acceptance or amendment; English help used only as contextual evidence.

No Work, production edit, app build, CI, release or runtime/native validation.

Production remains12 present/705 missing of717. No production changes, builds, CI, release or Work task.
