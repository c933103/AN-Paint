# Amharic text geometry: lexical author drafts

2026-10-24. Eight original, unaccepted review drafts. This packet is lexical evidence, not implementation or acceptance. No build, CI, Work task, remote publication, native-speaker review, rendering, visual-fit, or accessibility test was performed.

## Candidates

- Size (pixels): መጠን (ፒክሰሎች)
- Line spacing (%): የ መስመር ክፍተት (%)
- Text alignment: ጽሑፍ ማሰለፊያ
- Left aligned: በ ግራ ማሰለፊያ
- Centred: መሀከል
- Right aligned: በ ቀኝ ማሰለፊያ
- Top aligned: ከ ላይ ማሰለፊያ
- Bottom aligned: ከ ታች ማሰለፊያ

All eight have author_status=review. This means available lexical evidence supports presenting an original candidate for independent review, not that the wording is cleared. A reviewer may hold, reject, or revise any row. Source-backed components do not force acceptance of a composition or transferred grammatical form.

## Important distinctions

1. The Size (pixels) phrase is composed, not an exact whole-label quotation. AOSP Gallery2 directly attests the plural token ፒክሰሎች in 13M pixels and 4M pixels, so the selected plural is not merely an invented derivation. Its spelling family is consistent with the prior Pixel grid draft. LibreOffice's standalone Pixels → ፒክስሎች and UI _Pixels → _ፒክስልስ are retained as explicit variants. Only the English parentheses are structural here; unlike the other Size (px) key, there is no literal px to preserve.
2. Line spacing preserves both (%) and formatted="false". The exact LibreOffice wording/spacing is retained; normalized የመስመር is listed only as an editorial alternative. AN-Paint scales paint.fontSpacing by the 50..300% value for horizontal row or vertical column steps. It is not letter spacing, arbitrary extra pixels, or a promise about paragraph margins.
3. Text alignment adapts the exact LibreOffice phrase ጽሁፍ ማሰለፊያ with an explicitly disclosed ሁ→ሑ spelling normalization to the current project ui_text value ጽሑፍ. This is not the exact PO byte sequence. It neither discredits the attested alternate nor authorizes unrelated spelling edits.
4. Left/Right function-label evidence comes from paragraph and Fontwork text alignment, rather than physical object-motion commands. Top/Bottom function-label evidence comes from content alignment to cell edges and is corroborated by vertical text-adjustment values. Transferring Align Left/Right/Top/Bottom into the source Left/Right/Top/Bottom aligned spinner is an original function-label adaptation. Reviewers must assess whether a passive state form would read more naturally; no exact state-label attestation is claimed.
5. Centred uses the exact paragraph Centered → መሀከል value, supported in both horizontal and vertical text-adjustment contexts. It deliberately has no axis qualifier. A longer exact Align Center counterpart is retained as an alternative if review favors parallel function-label forms across the group.
6. Alignment concerns shorter rows/columns inside the text block and block anchoring at the chosen canvas point. It does not name writing direction, glyph orientation, movement of an existing image/canvas, or centering on the whole screen. Top/bottom stay physical edges regardless of column progression direction.

## Evidence files

- draft-candidates.json: eight objects with key, english, draft, source_attributes, rationale, confidence, evidence_record_ids, limitations, author_status, status, and alternatives.
- sources.json: eleven full snapshots, each with file, local_source_path, immutable URL, SHA-256, byte count, reuse provenance, and pin. The nine external sources are five LibreOffice files plus paired AOSP Settings and Gallery2 XML. Two project XML copies establish English identity and current Text orthography, not external authority.
- exact-records.json: 34 curated records. PO records contain full raw records, line ranges, context, msgid/msgstr, fuzzy/flags, and the pinned URL. Android records retain paired English/Amharic keys, source lines, raw XML, Android message ID attributes, and quote-wrapper-aware display values. Negative evidence is labeled explicitly.
- english-source-records.json: exact canonical English text and attributes for the eight keys.
- search-limits.json: bounded corpus, exclusions, spelling and transfer limitations, and the unsuccessful fresh-network diagnostic.
- validation.json: packet-integrity checks only, not linguistic or app acceptance.
- SHA256SUMS: hashes for all package files except this checksum file itself.

## Provenance and limits

All source snapshots were reused from earlier same-day packets or the parent's canonical source dossier. Their complete bytes were copied and their SHA-256 values recomputed and matched to the prior provenance. No successful fresh fetch is claimed. A web-open attempt at the pinned LibreOffice cui URL returned cache miss; it supplied no bytes and was not an access denial.

Every retained raw PO record is verified against its full-source line range. Positive PO evidence is nonempty and nonfuzzy, but nonfuzzy is not a quality guarantee. A LibreOffice object-bottom-alignment paragraph with apparent top/center drift is explicitly excluded. Empty translations are excluded. AOSP Settings font-size and device/audio left/right records were inspected but not promoted to alignment evidence. No claim of exhaustive dictionaries, all upstream files, or current-web coverage is made.

Full source snapshots retain original license/copyright headers. Reuse of terminology does not imply endorsement by LibreOffice, Android, or a native-language reviewer.
