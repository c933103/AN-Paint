# Independent M03 review

## Scoped verdict

Approved for publication as an incomplete technical draft only. The identified Hán/Nôm font-coverage defect is corrected and independently verified; no remaining blocking code-review defect was identified in the corrected snapshot. This is not merge, release, all-language, competent-language or runtime acceptance.

Reviewed baseline: `79b1f990a98eaf44c28351cd02c20157c70d8dff`.
Frozen source tree: `4f44f466eb9ed1f90790219b51d900a4a0603e95`.
Frozen 76-path source patch SHA-256: `96be917f8da57d3178637b92141de3448241ab9fc5ceb140aa2edfc6aab1ae27`.
Language-disposition JSON SHA-256: `f21dc67dabec758c5cd2972ce1640a4d8c8bb6be5481087c4118f17a6037b76b`.
The source tree/patch intentionally excludes the new verification documents and execution logs; the disposition hash binds the separate reviewed evidence input.

## Production review

The implementation matches M03 in the 12-message inventory at commit `c6fbbc7d23483a48bbef066313849129197398ce`, lines 59–77. A dedicated `ResponseLimitException : IOException` is raised only when the existing downloaded-byte accumulator plus the next read exceeds `2 * 1024 * 1024`. The comparator is still strict `>`, so exactly 2 MiB remains within the bound.

Both Copy credit and insertion map this type to `commons_metadata_response_too_large` inside an alive-activity main-thread callback. No string matching identifies the failure. Other exceptions retain their message, including whitespace, percent-looking content and null/blank behavior in the two existing wrappers. The separate SVG typed reasons remain mapped as before, now at callback time. I explicitly checked the replaced insertion `failure(message)` helper: it only enqueued `runOnUiThread` with the same alive guard and `showStatus`, and had no extra side effects. Both old and new paths enqueue once from the worker, then reach identical `finally` cleanup; neither waits for the UI callback. The relative callback/cleanup race is unchanged. Resource resolution is intentionally moved from the worker to the alive callback, including SVG messages.

Independent byte-for-byte reversal restored both production files to the real baseline. Apart from the declared mapping/type changes, the parser precondition, individual-field limit, image-byte limit, connection/stream cleanup, active connection clearing, credit cache/session handling, clipboard publication, result handling, temporary-file cleanup, retries, duplicate guard and destroyed-result handling are unchanged. This source observation does not substitute for executing the Android tests.

## Test and guard review

The new runtime tests use real WebView action routes with local fake connections. The exact-boundary fixture creates valid UTF-8 JSON, includes multibyte author text, then pads bytes to exactly 2 MiB or 2 MiB + 1. The test source checks typed rejection, stream closure/disconnect, active clearing, both action routes, exact-boundary retry, unaccepted draft/credit/clipboard/result/file preservation, late locale resolution, untyped detail preservation, duplicate attempts, destroyed late failures and already-queued success cleanup. Ordinary/RTL/vertical status-layout checks are declared for font scales 1 and 2; API 30/35 resource resolution is declared separately.

All 76 changed file bytes, SHA-256 digests and Git blob identities were independently checked against the source manifest. The source tree matches the complete frozen index including file modes. The 57 catalogue deltas and two production deltas reverse to the actual baseline bytes. Historical Copy-credit/F01/C023 hashes and fixtures, and the default-plus-59 completeness rule, remain unchanged. Focused mutation controls reject deletions, duplicates, changed additions, unrelated changes and fixture corruption.

An initial test command included a nonexistent module name, `test_tiff_size_wording`; that reviewer invocation was corrected to the repository's actual F01 modules. It is not a product failure. The final corrected focused frozen-source run executed 64 methods: 62 passed; two strict M03 completeness methods failed because only 56 of 59 scoped proposals exist. These are genuine, retained failures. The font coverage/preservation, input-safety, disclosures, Copy-credit, SVG and F01/C023 checks passed.

Superseded pre-font snapshot patch SHA-256: `bacae12c199a7d867e34b621eb7df010dcdb3e453735c8df9c8ec190d0b7ee46` (tree `503645568e3204082dd0b31721a8084b6e812d2a`). Its independent full host run: 561 methods completed in 219.395 seconds; six failure records. Five are expected missing-proposal completeness failures. The sixth is an actionable new defect: `test_every_nom_catalogue_ideograph_is_bundled` rejects U+8FD4 (返), used by the new Vietnamese Hán/Nôm proposal but absent from the bundled font. The author was notified and corrected it with the exact additive font extension reviewed below. This first snapshot is superseded. Original full log: `all-host-frozen.log`.

The corrected final full host aggregate executed 566 methods in 182.775 seconds, with five failure records: the two M03 default-plus-59/59-proposal assertions and the existing completeness subtests for `ain-Kana`, `ain-Latn`, and `mnc-Mong`. No unexpected failures remain. The aggregate is still FAILED; missing language proposals are not waived or marked green. Final full log: `all-host-final-corrected.log`. Its mock-instrumentation diagnostic JSON is output from host fixtures, not evidence of actual device runs.

The retained Gradle diagnostic reaches `SDK location not found`. Kotlin/Android test compilation, JVM runtime tests, lint, resource-generation execution, screenshots and installed-device behavior have not been established by this review. No runtime pass is inferred from host tests or source inspection.

## Corrected one-glyph font delta

The initial U+8FD4 coverage defect is corrected by appending only that glyph from the already-pinned Nom Na Tong v5.18 source (SHA-256 `37bd8506257d0905d499395e7f0bc2b6a2ae619dbb635a82ea0905b75b2ff5f3`). The new subset is 275,788 bytes, SHA-256 `4ae4cab599622f6c9d66b8a99074f2a291ffc32000a78ba69f241fc12eb64e05`.

I independently compared the actual Git baseline font, the corrected file and the pinned primary source using FontTools, then regenerated the corrected file into a separate reviewer path. The generation was byte-identical. All 734 old codepoints, 736 old glyph outlines/metrics, complete old cmap subtable identities/mappings and global/name/license data are preserved. The added outline hash is `e59decb99f22b2e26b7de68fde51dcfb622845ced7fed143fc67a0af87fe4dc3`; its source-identical advance/bearing are 1000/58. The full sfnt checksum is valid. The pinned binary reversal restores the actual baseline font byte-for-byte, so the historical SVG-font oracle is preserved rather than replaced. The original builder and notices remain byte-identical; the inventory changes only the corrected subset digest.

I independently repeated all 2,202 old-glyph raster comparisons using Pillow 12.3.0 / FreeType BASIC at 24/48/96 px; old masks, offsets and advances were identical. The new glyph is nonempty at all three sizes. Source/subset pixels match at 48/96 px with a common baseline, but mask size/pixels differ at 24 px despite exact vector outline/advance/bearing identity. This observation remains explicit and unresolved as an all-size source-pixel equivalence claim. It is not Android layout or rendering acceptance. I also inspected the supplied comparison PNG; the new subset shows the added glyph, while the prior subset has no rendered glyph in that position.

## Locale review and open holds

The default is exactly `Commons metadata exceeds the response limit`; all present messages retain literal `Commons` and have no format placeholders. No English filler was inserted into non-English catalogues. Individual disposition records match every one of the 140 offered tags: 56 proposals, three unresolved required catalogues (`ain-Kana`, `ain-Latn`, `mnc-Mong`), and 81 unchanged out-of-scope missing-key fallbacks. Actual missing-key fallback count is 84; the required target remains 81.

All rows explicitly retain `linguistic_acceptance: not-established`. Hakka Latin, traditional Mongolian and Vietnamese Hán/Nôm are source-assisted, low-confidence drafts with constituent-source and whole-sentence limitations stated. Other languages retain individual confidence/review limits, and `en-XV`/`qaa-Zsye-XV` are labeled synthetic layout fixtures. This review checked these records and structural consistency; it does not independently certify their linguistic accuracy or claim fluency.

Full acceptance remains held for the three missing required proposals, competent-language review of the proposals, and exact-source Android compilation/runtime/resource/layout verification. Existing security, device/archive and release holds are unchanged. No remote writes, Work-task actions, archive-producer retries, readiness changes or release operations were performed.

## Review evidence files

- `independent-manifest-final-check.json`: all final file identities and byte-for-byte reversals
- `independent-locale-check.json`: 140-tag structure and exact open dispositions
- `independent-font-check.json`: source identity, preservation, checksum and independent regeneration
- `independent-raster-check.json`: local raster comparisons and limits
- `focused-host-final-corrected.log`: 64 focused methods, two retained completeness failures
- `all-host-final-corrected.log`: 566-method final aggregate, five retained completeness failure records

Final source patch hash and language-disposition hash were rechecked after tests. No source changes were made by the reviewer.
