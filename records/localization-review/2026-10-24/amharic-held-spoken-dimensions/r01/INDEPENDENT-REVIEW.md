# Independent adjudication: Amharic spoken dimension labels

2026-10-24. This is a translation-readiness decision, not implementation, native certification, runtime testing, or release approval.

## Result

Release the two existing holds without changing their templates:

- ui_width_in: `ስፋት በ%1$s`
- ui_height_in: `ቁመት በ%1$s`

Separately accept the revision of the already-ready spoken dependency ui_pixels_6ec9c2 from `ፒክሰሎች` to `ፒክሰል`. Confidence in preferring the unmarked singular measure name is medium. The old plural is not wrong, and this review explicitly accepts both old complete plural phrases as admissible alternatives. This is a contextual editorial choice, not a correction of proven bad grammar.

The four selected complete phrases are:

- `ስፋት በፒክሰል`: accept, medium overall confidence, with medium-high meaning/construction confidence and medium singular-preference confidence.
- `ስፋት በፐርሰንት`: accept, medium-high contextual composition confidence.
- `ቁመት በፒክሰል`: accept, medium overall confidence, with medium-high meaning/construction confidence and medium singular-preference confidence.
- `ቁመት በፐርሰንት`: accept, medium-high contextual composition confidence.

The original `ስፋት በፒክሰሎች` and `ቁመት በፒክሰሎች` are explicitly admissible, unselected alternatives, with medium-high intelligibility/grammatical confidence. Keeping the old dependency is therefore not newly established mistranslation. Do not claim singular is the only grammatical way to clear the holds.

## What changed the earlier decision

The old review correctly distinguished intelligible components from an adequately supported complete short label. Its evidence consisted of image-dimension nouns, unit-bearing prose, and an imperative. The new textbook record is materially different: an actual nominal table heading.

I independently rendered PDF page 165 from the supplied complete, hash-verified Amhara National Regional State Education Bureau Grade 3 mathematics textbook. Its printed page 155 shows `ቁመት በሳ.ሜ` as the third table-column heading. The rendered pixels confirm a dimension-first short label with attached preposition and no copula or command. This is not OCR-only or an assertion based on the proposal's prose. The table concerns living things and centimetres, not software pixels or speech, so it supports the construction rather than the exact four proposed outputs. Width transfer is an explicit inference using the independently retained image-width noun.

[Official textbook, PDF page 165](https://anrseb.gov.et/wp-content/uploads/New_Text_Books/Grade3/Grade%203_Mathematics_Textbook.pdf#page=165)

The pinned Pluma PO record gives a short top-margin-in-pixels label with an unmarked singular pixel noun. I inspected the full PO context and the actual HTML tag definition, and recomputed both Git blob IDs. The record is nonempty, nonfuzzy and not obsolete. These are integrity facts, not proof of native authorship or impeccable translation quality. Its margin noun means line; the pixel spelling differs; the preposition is spaced. Accordingly, I transfer only the relevant unit-label construction and singular-measure precedent, with medium weight. I do not endorse the whole Pluma translation or silently normalize a quotation.

[Pinned Pluma record](https://github.com/mate-desktop/pluma/blob/b5e619eb833d44d52b9c6cb5677c89b9d7749a3e/po/am.po#L4793-L4795)

The retained pixel stem is independently supported by the AOSP megapixel form and the earlier plural family. The original plural also has positive evidence after the unit preposition. Evidence therefore supports two permissible realizations, not a categorical singular-versus-plural rule. With no number inserted in either consumer, an unmarked unit name is a reasonable preference. The singular does not say that width or height equals one pixel.

## Grammar and source meaning

Each complete phrase has a dimension head followed by a unit-denoting prepositional phrase. As a field label it need not contain a finite verb, copula, relative clause, definite article or imperative. The actual textbook heading supports this nominal-label register. The already-reviewed image nouns are retained, rather than switching the spoken height label to the alternative length/height noun and creating an unexplained visible/spoken mismatch.

Each template retains exactly one positional `%1$s`. Each inserted resource is a bare unit with no preposition. Every full phrase consequently has exactly one attached `በ`, no unresolved placeholder and no inserted numeral. The singular/plural decision affects only the spoken pixel key, not the generic visible Pixels selector. Percent keeps its already-reviewed bare noun unchanged.

The original LibreOffice percent record establishes the unit noun and prepositional meaning. Combining that evidence with the new short-label construction is productive grammar, not a falsely claimed exact corpus match. A supplemental web re-open also confirmed dimension-before-percent sequences in LibreOffice help, but they remain prose, use an alternate height noun, and come from a mutable crawled page. They are corroboration only. The failed EDRMC percent-report lead has no role in this decision.

[LibreOffice help corroboration](https://help.libreoffice.org/latest/am/text/swriter/01/05060100.html)

The source content descriptions identify a field's measurement scale. They do not append the unit resource to a numeric count. Source calculations take width as a percentage of original width and height as a percentage of original height. The translations introduce neither an image-area denominator, a fixed 100% value, a maximum range, nor an action. No English-source defect is established; this decision neither rewrites English nor triggers speculative cross-language source changes.

## Consumer scope and verification limits

The input seal matches SHA-256 `54fe607ce11507b94c397e81b33949018a619b448830913df2975c434b40afed`; all 66 payload hashes pass. I recomputed both Git blob IDs and SHA-256 for all 18 complete supplied project files. English values and hashes, XML fragments, placeholder contracts, four selected expansions and both plural alternatives also pass static checks.

The supplied current-main scan lists 104 Java/Kotlin files, no unavailable/changed files, and exactly two direct spoken-pixel references, DimensionControls lines 81 and 82. I inspected that scan and the actual full consumer. The three constructor contexts are new-image/resize/canvas-size, import-copy resize, and assembly output-copy sizing. ImageCropDialog is not misrepresented as a constructor caller.

[Bound consumer at the supplied production commit](https://github.com/c933103/AN-Paint/blob/66be61df27c5359bffc32d56db21f3949899f873/Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt#L76-L87)

The 104-file coverage is supplied sealed scan evidence. I did not freshly retrieve and independently rescan all 104 file bodies or requery remote HEAD. The 18 full file hashes are independently checked against their supplied bindings. Source evidence is not a proof about dynamic/reflection use, live TalkBack behavior, TTS pronunciation or Android rendering. No app tests, build, CI or release was run. This bounded linguistic acceptance does not certify any of those layers and does not reopen the longer help/result strings or aspect-ratio lock.

## History, counts and the pending batch

The full earlier decision record is copied byte for byte as preserved-original-reviewed-candidates-and-holds.json. Original acceptances, earlier hold rationale, dissent and alternatives are not overwritten. The original plural, alternate pixel spellings, native percent alternative and alternate height template remain recorded. Only the two existing template holds and the one explicitly separate dependency revision receive new decisions here. The previously resolved three proportion keys and Eyedropper are untouched.

If this adjudication is adopted into the project review inventory, the inventory moves from 94 ready / 14 held / 0 implemented to 96 ready / 12 held / 0 implemented. The dependency is already a ready unique key, so its value revision adds no new key and is not a third released hold. This review has not mutated the global inventory.

The pending 90-key implementation batch is unchanged. The spoken-pixel dependency is inside that old batch, so adopting singular requires an explicit versioned value amendment before implementation consumes it. Do not silently substitute the new value; do not pretend the old batch already contained it; do not add these two newly ready templates to that batch without a separate scope decision. Reviewed-values.xml is a three-entry review artifact, not a production patch or authorization to implement.

## Publication and stopping point

The explicit allowlist covers only the small review files, bounded excerpts/links and preserved project decision record. The 53 MB third-party textbook, full page images, extracted page text, complete PO/XML snapshots and transient render are excluded. The source packet's existing publication exclusions remain in force.

Review is complete with no action-time approval or permission denial pending. A supplemental web open of Pluma returned a cache miss, not an access denial; it did not invalidate the verified pinned snapshot. All production changes, batch adoption, implementation and later runtime validation remain outside this completed review.
