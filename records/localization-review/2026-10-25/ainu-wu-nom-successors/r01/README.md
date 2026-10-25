# Reviewed Ainu, Wu and Nôm translation successors, 25 October 2026

This record covers 16 existing resource values in four catalogues. It is a successor to PR #169, not an amendment of that PR's reviewed head. English, application behavior, warning values integrated by #169, unrelated locales, and historical review comments remain unchanged.

## Exact acceptance scope

- **ain-Latn assembly Help:** five additional corrections on the #169 value: contingent crop movement, retained placements and possible gap filling after Unplace, snap-only overlap rejection, quantitative common dimension, and exact preview versus committed result. Candidate value SHA-256 `5b515a6d18c078c830233ed304aff876ab5cde61f2ec87e693d2ef115b5d48c3`.
- **ain-Kana assembly Help:** seven additional corrections on the #169 value: the corresponding tray/provider and conditional memory branches, plus the same five completion components. Candidate value SHA-256 `11f8f37dc212310740cd73a4bac8710ce8139f77894e342ad54cf9d3f916e551`.
- **wuu-Hans assembly Help:** the complete eight-paragraph successor resolves the eleven previously identified semantic defects, including the numeric-position paragraph and current control captions. Candidate value SHA-256 `a898bdda8993642d70449d3b31d5e99a5fc55b0ba3fdbf5ddcbfcd934236d53f`.

For each of those three exact Help values, the complete 34-sentence English source was independently compared and no remaining concrete source-semantic gap was found. Their common English source SHA-256 is `6ae12f86846110a7573a5c608b8561b0c03b037454f1905d3b5bf8342fb26aac`. The existing per-image equal-percentage Ainu aspect-ratio sentence is positively retained, not held. Medium idiom confidence, contemporary terminology and Shanghai-based written Wu are qualifications, not grounds to retain a whole-key semantic hold. This is not native-speaker certification or rendered/runtime acceptance.

- **Six estimate contexts in each Ainu script:** the changed clauses now state expected memory use rather than lack of knowledge. Acceptance is limited to the documented estimate deltas, not all inherited prose or the complete legacy Help value. See `estimate-values.json` and final `estimate-review.json`; the latter supersedes the review-time pending status in the former without changing candidate bytes.

The six keys are:

1. `ui_assembly_decoded_output_estimated_editing_render_memory_at`
2. `ui_copy_decoded_image_at_this_size_estimated_loading`
3. `ui_original_decoded_image_rgba_4_bytes_pixel_estimated`
4. `ui_sampled_resize_memory_explanation`
5. `ui_estimates_include_the_current_canvas_and_clipboard_sampled`
6. `ui_the_arrow_on_the_left_directly_below_the`

The last two have no literal references in the inspected 104 main Kotlin/Java source files; current editor Help uses `ui_help23`. They are retained-resource corrections, not identified live UI blockers. The retained technical sampled-decoding list has not been newly certified.

## Nôm assembly-Help successor

The separate `vi-Hani` assembly Help candidate has eight paragraphs and no remaining concrete linguistic correction identified by its independent bounded review. The final exact value SHA-256 is `d33cbe183658d2e8d71924a6ebbabf1f04792fa8a76d5c0eb26db33f41775232`. It preserves the complete historical PR12 tray/output paragraphs and uses the current PR67 numeric-position clauses and captions. Earlier acceptance of PR12 remains narrow; it is not enlarged retroactively.

The previously accepted `612852fa…` variant is preserved separately. Its U+25A28 𥨨 failed the existing actual bundled-font coverage contract. The final candidate replaces exactly two occurrences with U+259EA 𥧪, independently supported for the Vietnamese empty sense by dictionary readings `trống` and `rỗng`, not chosen merely for glyph convenience. The unchanged current font maps U+259EA and the final complete Nôm catalogue passes the normal all-glyph guard. No font asset, font inventory or font-routing change is made.

Only `ui_add_up_to_20_images_with_android_s` changes in Nôm. PR113 is not retargeted; its `commons_blank_maps` and `ui_help23` keys and all Nôm warning terms remain untouched. Native-reader and runtime rendering qualifications remain, without a language-wide acceptance gate.

The final two-character variant received a fresh independent focused review on 25 October 2026 at 13:54 UTC, recorded in `nom-variant-independent-review-20261025.json`. This is new verification, not recovery of an earlier missing reviewer receipt. Its exact candidate identity and contextual empty-space senses were independently checked against the dictionary source. The proposal's original pending status remains historical and is superseded by that focused acceptance only.

## History and evidence

`exact-changed-values.json` preserves the complete old and accepted new values. The separate receipts, sentence maps, independent reviews and source/consumer bindings explain their scope. `packet-origins.json` binds the original review packets to these project records; only temporary artifact paths and internal reviewer identifiers were replaced with project-relative references and review roles.

The historical Ainu PR #56 comments [Kana](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6327485786) and [Latin](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6327665535), and the [Wu hold](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6349315226), remain unchanged. This is an additive exact-source/value successor assessment, not retroactive acceptance of the old wording or the whole catalogues. The earlier five-component packets and #169 partial successor remain historical evidence.

## Focused static and contract validation

- Exact source and predecessor hashes matched the #169 repaired head before local composition. Every replacement occurred once. Sixteen values changed; all other keys, all resource attributes and English stayed unchanged.
- All four catalogues passed Android string/placeholder/XML structural checks.
- The Wu PR6 test reproduced three expected paragraph-structure failures before its guard update. The successor adds the eighth paragraph; the guard now identifies paragraph 6 as the memory paragraph. Its three original dimension/conditional-choice/tiny-output-warning spans and the other five locale cases remain unchanged. Additional bounded clauses guard the repaired distinctions.
- The Nôm PR12 guard reproduced four expected old seven-paragraph failures. Only its paragraph/output index expectations changed; original Vietnamese/Nôm tray and conditional-memory spans remain exact, with additive bounded successor clauses.
- Fifty-seven focused tests passed normally and with `python3 -O`, including the original memory-warning corruption/inventory contracts, Nôm context guards, the actual Nôm all-glyph contract and the existing Wu supplementary-font coverage contract. This is not a full CI result.
- New Wu Han character **U+62E2 拢** is a BMP character handled by the ordinary platform font. The unchanged bundled Wu fallback intentionally covers only supplementary U+20C8E and passed its existing actual-cmap check. The new BMP character was included in the static character inventory; this does not establish device rendering for it. No font asset or routing change is proposed and no new native-review gate is introduced.

The application branch must be rebound to the fresh post-#169 merge base, reviewed and tested as one accumulated batch before merge. Natural postmerge checks remain separate from linguistic acceptance. No release is part of this work.
