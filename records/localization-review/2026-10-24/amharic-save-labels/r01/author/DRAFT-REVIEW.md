# Amharic save/file-label draft dossier

Five new missing labels, separate from all prior 72 ready and 12 held proposals. All remain original drafts, not accepted or implemented. Production remains 12 present / 705 missing of 717 containers.

## string/ui_save

English: Save

Proposed XML: `<string name="ui_save">"አስቀምጥ"</string>`

Generic saving/persisting command, deliberately not image-only: File menu and quick icon reuse saved destination/options or open initial PNG Save as panel; palette replacement commits chosen colour into CustomColours preferences; credits editor saves current credit edits and remains open. No claim of success before validation/I/O.

Qualification: Save label must not mean Download/Export/Close or only save image. Image Save applies pending canvas work; successful non-export updates remembered destination and document saved state. Credit Save does not close the editor; palette Save also selects colour.

Evidence/adaptation: Exact Android action label.

Confidence: high lexical, draft only

## string/ui_save_a5d0d9

English: Save…

Proposed XML: `<string name="ui_save_a5d0d9">"አስቀምጥ…"</string>`

Positive Save… in confirmReplacement, before replacing dirty image. Stores requested continuation then requestSave(false); successful non-export write invokes it. Cancellation/failure clears continuation. Existing saved target can be written without another dialog; ellipsis is retained from English, not a promise every invocation opens one.

Qualification: Not immediate discard or replacement, not an unconditional success claim; unchanged source ellipsis not a proven defect.

Evidence/adaptation: Append canonical English U+2026 ellipsis to the exact Android Save action. This is not claimed as an exact source pair.

Confidence: high lexical plus explicit punctuation adaptation, draft only

## string/save20_title

English: Save as…

Proposed XML: `<string name="save20_title">"ማስቀመጫ እንደ…"</string>`

File menu Save as… command and ordinary save-options dialog title. Opens format/name/settings form then Android create-document location picker; not immediate saving. A successful ordinary save replaces remembered save destination/settings.

Qualification: Not rename-only, not Save a copy with unchanged destination, not Export as. Excludes share/export titles and complex explanations.

Evidence/adaptation: Remove LibreOffice ~ mnemonic and replace ASCII ... with canonical U+2026. Preserves sourced word order.

Confidence: medium-high lexical; title/register needs review

## string/save20_file_name

English: File name

Proposed XML: `<string name="save20_file_name">"የፋይል ስም"</string>`

Visible filename field label and its contentDescription, reused in horizontal and vertical forms. Editable basename with format extension: known extension replaced/appended on format change; validation forbids slashes/control characters and invalid blank/dot stems. Proposed name sent to Android document picker.

Qualification: File name, not full path/location; label does not translate typed user filenames or extensions. Same label is shared by save/export/share panels.

Evidence/adaptation: Exact non-fuzzy Save As dialog help label, preserving source spaces. Draft joins the bound prefix የ to ፋይል for consistency with reviewed project style; this is explicitly an editorial adaptation, not a verbatim pair.

Confidence: high lexical, draft only

## string/save20_file_format

English: File format

Proposed XML: `<string name="save20_file_format">"የፋይል አቀራረብ"</string>`

Visible format chooser label and contentDescription, reused in vertical form. Selects encoded output format and associated settings; ordinary save excludes derived formats, export filters derived formats, share can show all. Changes filename extension and applicable controls.

Qualification: Format/type of output file, not page layout, style, format-device action or filename extension alone. Format names and compression descriptions not translated in this group.

Evidence/adaptation: Extract exact phrase from non-fuzzy save-dialog prose and Default File Format and ODF Settings label. The standalone File format entry at help01 line 2680 has empty msgstr and is explicitly NOT positive evidence. Draft joins the bound prefix የ to ፋይል for consistency with reviewed project style; this is explicitly an editorial adaptation, not a verbatim pair.

Confidence: medium lexical; phrase extraction, draft only

## Review focus and evidence limits

Save is a generic command shared by image save, palette replacement and credit-text editing. It must not be expanded to Save image. Credit Save remains open; palette Save writes preferences and selects the colour. Image Save reuses an established target or opens initial Save as settings. Save… in replacement confirmation retains its English ellipsis, but an existing target may save without another dialog. Cancellation/failure clears the deferred replacement. No source defect is established by that convention alone.

Save as is supported by non-fuzzy LibreOffice nominal menu/title wording, rather than the imperative Android Save form. Preserve this register distinction for independent evaluation; no imperative alternative is invented. File name joins the bound prefix in an exactly attested label. File format joins the prefix and extracts the noun phrase from translated save-dialog prose and a compound settings label; the standalone File format entry is empty and excluded. These are explicit adaptations, not verbatim whole-label matches. Fuzzy GIMP variants are excluded. No exact-corpus-match requirement is imposed as a universal acceptance criterion.

Complete source copies: 20 current project files with exact Git blob and SHA-256 bindings; fresh develop commit/tree verification at 66be61df27c5359bffc32d56db21f3949899f873 / 870c5a584120d92710be516af0dc3b3847b183d9. Bounded direct-consumer audit finds 13 exact occurrences across five files. Initial discovery used historical source, then complete files were rebound to current blobs and rescanned. This is not an exhaustive fresh full-repository caller search. No tests were run. Encoding internals are outside label review; complete dispatch source supports format meaning, not codec-quality certification.

Seven complete reused primary lexical snapshots and 32 exact records preserve immutable URLs, contexts, flags and source hashes. Reuse is not fresh network retrieval or native-reader approval. AOSP products are not independent unrelated authorities. See lexical-evidence/README.md, sources.json and exact-records.json for primary locators and original alternatives. Full source files are supplied for independent checking, not merely manifests.

No format placeholders or units in this group. Exactly two ellipses remain U+2026. Neighbouring compression, error, share/export/recovery explanations and held Help remain outside scope. Previous held Done, Palette uncertainty, optional Horizontal change and all other holds are unchanged. No production edit, Work task, app build, CI, release, runtime/rendering/accessibility or whole-language acceptance.
