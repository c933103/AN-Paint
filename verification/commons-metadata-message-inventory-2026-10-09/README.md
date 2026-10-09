# Remaining application-authored Commons/import messages: inventory and implementation plan

## Result and scope

At develop **7e8a0d2377693a35cd9392f2082ef88548a6f67f** (tree **7d4245411d699a3cf59018ce8c6d4cb87940dc60**), all **12 previously tracked English literals remain**:

- **Nine** metadata/cache reasons can be displayed during either metadata-only **Copy credit** or Commons image insertion.
- **One** non-file-page reason is a **defensive precondition with a conditional insertion route**. Copy credit validates the same page first; insertion subsequently truncates the page, which can make the precondition fail.
- **One** original-download identity reason is insertion-only.
- **One** PNG-encoding reason is Commons SVG insertion-only.

This is an evidence-only source audit and plan, dated **9 October 2026**. No production code, resource value, held PR34 branch, proposed Hungarian correction, provider setting or workflow was changed. No PR was opened and no Wikimedia/provider request was made. Reachability below is established by source tracing, **not newly executed Android tests**. This does not close the broader localization reset, all-language completion, native-language review or device-acceptance work.

The audit resolves the older redirect inventory's line 324 to **line 321 on this pinned develop commit**; its text is unchanged. The other eleven source lines still match the tracked inventory.

## Exact inventory

The machine-readable [inventory](inventory.json) records exact literals, source links, conditions, exception classes, proposed keys, placeholders and a deterministic test for each item. The proposed names and defaults are a design, not existing resources.

| ID | Exact application literal | Pinned source | Proposed resource key |
|---|---|---|---|
| M01 | `Not a Commons file page` | [CommonsAttribution.kt:44](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L44) | `commons_metadata_not_file_page` |
| M02 | `Commons metadata: HTTP $status` | [CommonsAttribution.kt:69](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L69) | `commons_metadata_http_error` |
| M03 | `Commons metadata exceeds the response limit` | [CommonsAttribution.kt:76](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L76) | `commons_metadata_response_too_large` |
| M04 | `Commons metadata query failed` | [CommonsAttribution.kt:88](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L88) | `commons_metadata_query_failed` |
| M05 | `Commons metadata returned an ambiguous file` | [CommonsAttribution.kt:90](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L90) | `commons_metadata_ambiguous_file` |
| M06 | `Commons file metadata is unavailable` | [CommonsAttribution.kt:92](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L92) | `commons_metadata_unavailable` |
| M07 | `Commons attribution does not match the selected original file` | [CommonsAttribution.kt:95](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L95) | `commons_metadata_original_mismatch` |
| M08 | `Invalid Commons attribution page` | [CommonsAttribution.kt:97](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L97) | `commons_metadata_invalid_page` |
| M09 | `Commons attribution field exceeds the text limit` | [CommonsAttribution.kt:116](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L116) | `commons_metadata_field_too_large` |
| M10 | `Could not retain Commons attribution` | [CommonsAttribution.kt:137](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L137) | `commons_metadata_cache_failed` |
| M11 | `The Commons download redirected to a different original file.` | [MediaGalleryActivity.kt:321](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L321) | `commons_download_original_mismatch` |
| M12 | `Could not encode blank map as PNG` | [BlankMapSvg.kt:47](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/BlankMapSvg.kt#L47) | `commons_svg_png_encode_failed` |

All defaults preserve the current wording. Only M02 needs a substitution: `Commons metadata: HTTP %1$s`, with `status.toString()` as the single argument. `%1$s` deliberately preserves the ASCII HTTP code produced by the current interpolation; locale-sensitive `%d` could change its digits. `HTTP` and `PNG` remain recognizable technical identifiers. `Commons` remains an identifiable proper name; its surrounding prose is translated. The other eleven reasons need no placeholders or plurals. Do not add numeric limits or parameter names to the visible prose as part of this slice.

## Actual routes and display boundaries

### Commons metadata and cache (M01–M10)

The [gallery action handler](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L175-L189) accepts the generated Copy credit or Use image action only after checking the source and artwork page. `copyCommonsCredit` calls `commonsCredit`, which calls `CommonsAttribution.fetch` and then `cache` ([lines 248–273](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L248-L273)). The current develop exception callback displays `ui_could_not_load_gallery_image` with `error.message`; thus a localized outer sentence can still contain one of these English reasons.

Insertion can begin through Use image, an allowed image navigation/download, or an image long-press. It additionally validates the artwork page in `insert`. After a successful original download and validation/render, [download line 350](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L286-L364) calls the same `commonsCredit`. Its catch uses the same outer gallery-image resource. A metadata/cache failure therefore also prevents returning an otherwise successfully downloaded image.

M01 needs a more precise disposition than the earlier “guarded defensive” label: `requestUrl` checks the same Commons artwork predicate already checked by both action-entry routes. Copy credit retains the page unchanged. Insertion, however, validates the full page and then calls `download(uri, page.take(4096), ...)` at line 290. A valid `/w/index.php` artwork URL with `title=File:...` after that boundary loses its title parameter when truncated; after a successful fake original download, `requestUrl` rejects it and the insertion wrapper can display M01 before opening the metadata connection. This is a source-traced conditional route, not an Android execution claim or a proposal to change the existing validation/truncation behavior. The verifier includes a local URL/query model of that transition and exact Kotlin source anchors. Normal invalid-page entry should still be tested for rejection with zero requests. The later title shape/length/pipe precondition has no custom message and is outside the twelve-item inventory.

Important semantic boundaries:

- M02 rejects every status other than exactly 200, including a metadata redirect. It is not an image-download status failure.
- M03 is the **2 MiB response byte** limit during streaming. The separate `require(json.length <= MAX_RESPONSE)` is a message-less defensive Kotlin precondition, not another application-authored English literal.
- M05 means **zero or multiple** pages; a translation that only says “multiple matches” narrows its actual condition.
- M06 includes a missing page, a non-file namespace and an absent namespace.
- M09 tests the raw HTML field's Kotlin String length: **64 Ki UTF-16 code units**, before HTML-to-text conversion. This is not a byte limit or a rendered-text limit.
- M10 means the metadata snapshot could not be retained because `commit()` returned false. It does not mean the drawing, edited credit or clipboard failed to save.
- `cached()` catches invalid cached-data exceptions and returns null ([lines 140–149](https://github.com/c933103/AN-Paint/blob/7e8a0d2377693a35cd9392f2082ef88548a6f67f/Paintroid/src/main/java/org/catrobat/paintroid/classic/CommonsAttribution.kt#L140-L149)); it is not an additional visible source for these reasons.

### Image-only reasons (M11–M12)

M11 is tested after the redirect loop has selected a successful image response and before reading its body. A different allowed Commons original can reach this reason; an unsupported destination reaches the already-localized supported-host check instead. Metadata-only Copy credit does not download an image and cannot reach M11.

M12 occurs only if `Bitmap.compress(PNG, 100, out)` returns false after original-size SVG rendering. A thrown output-stream exception or AndroidSVG parse failure is a separate library/OS exception, not this reason. The bitmap is recycled in `finally`; the caller cleans up temporary files. Copy credit and raster insertion cannot reach M12.

## What must and must not be localized

All twelve inventory rows are application-authored text: their exact literals are in application Kotlin code. HTTP status is runtime protocol data embedded in the app's own sentence. A JSON response with `error` causes M04's fixed app-authored sentence; the remote object's message/code are not currently displayed by that branch.

Do not perform string matching on exception messages or attempt to translate arbitrary exception text. JSON parsing failures, network/stream/OS exceptions, AndroidSVG exceptions and message-less Kotlin preconditions can also reach existing wrappers. Those are outside this bounded application-literal slice. Preserve their current detail/fallback behavior, including literal `%` sequences and newlines; never feed a provider/exception value back through a second formatting pass.

The provider fields `ObjectName`, `Artist`, `Credit`, `Attribution`, `LicenseShortName`, `LicenseUrl`, `UsageTerms`, `Permission`, `Copyrighted`, `AttributionRequired` and `Restrictions`, along with their values, attribution links, licence versions and source/page URLs, are retained provider data. They are not twelve more UI strings. Preserve the existing decoded-text/link handling rather than changing its policy. The metadata request currently specifies `iiextmetadatalanguage=en`; changing that request parameter is a different behavior change and is not needed to localize application reasons. This audit does not send such a request.

Previously resource-based SVG size failures, the two import-change notes, Help text and existing copy/credit labels are distinct work. Do not duplicate their keys or reopen them merely because they appear next to these call sites.

## All-language applicability

[All-language dispositions](all-language-dispositions.json) list **every one of the 140 exact offered tags** and its canonical resource path, including the existing 59-tag scoped batch and the other 81 tags. Every locale shares these conditional paths, so no locale is functionally non-applicable. Device default uses the same mechanisms through the resolved device locale.

The current reasons are hard-coded English for **all** tags. This is not evidence of resource fallback: the proposed keys do not exist even in the default catalogue. English variants need resource externalization and English wording review; their legitimate English text must not be counted as an untranslated-language defect. The `en-XV` and `qaa-Zsye-XV` conventions need intentional pseudo/variant handling. Other locales need actual target-language/script translations and review.

The first implementation may use the established default-plus-59 complete batch as a bounded increment, with **12 × 59 = 708 exact localized/variant entries plus 12 defaults** if all reasons land together. That does not satisfy the all-language acceptance condition: **81 × 12 = 972** additional offered-tag entries would remain explicitly open. A full twelve-message applicability inventory covers **140 × 12 = 1,680 tag/message pairs**. Do not fill untranslated locales with English just to claim key completeness or substitute a neighboring language/script. Preserve each locale's independent acceptance status.

## PR34 and Hungarian dependencies

The read-only PR34 comparison is pinned to head **1cd0eeac6bc4a30cb331f3b27cdfa30ff62b97df**, an open draft based originally on **43148951ac6bd23687e66685855909ac538ba004**. [Exact overlap evidence](pr34-overlap.json) includes its three-message Copy credit catch patch and affected paths.

- PR34 changes the **outer** Copy credit wrapper, absent/blank detail behavior, out-of-memory text and linkage fallback. It does not edit `CommonsAttribution.kt` or `BlankMapSvg.kt` and explicitly leaves these twelve reasons unchanged.
- There is a direct integration overlap in `MediaGalleryActivity.copyCommonsCredit` and in default plus 59 localized resource files, **61 production paths total**. Distinct new keys do not remove the need to reconcile the same catch block and catalogue append locations.
- PR34's `CommonsCopyCreditErrorTest` deliberately asserts the old English metadata reasons. Its HTTP/query/validation/oversize expectations must become localized **only for typed application failures**. Its verbatim untyped/provider/framework-detail, blank, OOM, linkage, clipboard rejection, duplicate tap and destroyed-activity cases must keep their existing purpose.
- PR34 also has a source-contract assertion that confines that prior patch to three resource additions and an otherwise unchanged source. Preserve its historical evidence; add a versioned successor contract or narrowly revise the live assertion for the combined implementation. Do not silently rewrite historical results to make a later patch appear identical.
- This inventory can be published independently. Implementation should use the settled PR34 integration head and re-read its actual tests, rather than modifying/retrying the held branch or copying an unverified prepared tree. If the base changes, rerun the audit/overlap checks before applying changes.
- The separate Hungarian attribution terminology proposal is not applied here. New Hungarian reason wording should eventually use reviewed attribution-context terminology, while the 17 proposed existing-string changes remain in their own integration slice. Shared catalogue editing is an integration dependency, not authorization to apply that proposal now.

## Bounded implementation plan

1. Freeze the actual settled base, preserve a clean separate implementation branch and recheck the twelve source conditions. Do not alter provider permissions, requests, thresholds, image-size behavior, cached record schema, editing/clipboard semantics, redirect identity checks or lifecycle guards.
2. Introduce typed application failure reasons with optional HTTP-status data. Follow the existing `SvgOriginalSize.SizeException` principle: helper code reports a reason; UI code selects a resource. Preserve the existing `IOException` versus `IllegalArgumentException` distinction, for example through a common marker implemented by appropriately typed exception subclasses. Avoid classifying arbitrary errors by English text.
3. Add complete translatable resources in canonical `values/strings.xml`, with translator comments that explain the two-route metadata context, the zero-or-many ambiguity condition, cache retention and PNG encoding. Add reviewed translations directly to the chosen exact catalogues, with per-tag provenance/review/fallback dispositions. Do not regenerate from historical reference snapshots.
4. Replace only the twelve application literals with typed reasons. Resolve them once at each relevant guarded UI error boundary, including both Copy credit and insertion. Compose with the settled PR34 outer Copy credit wrapper; keep the current insertion wrapper and existing typed SVG-size mappings. Put new resource lookup inside the existing alive-activity callback rather than localizing on a worker or after destruction. Preserve untyped detail and the Copy credit blank-reason behavior.
5. Separate tests and evidence by reason. A practical sequence is the ten metadata/precondition reasons, followed by the two image-only reasons, on the settled base. Each slice must name its remaining keys/locales rather than marking all twelve complete early.
6. Run the prescribed host checks, focused Android tests, full applicable regression/lint/build checks, representative rendered checks and exact-head review. Reconcile a changed integration base and verify the actual merged head afterwards. Do not treat a source inventory or passing structural checks as Android/native-language acceptance.

## Deterministic implementation/test acceptance

The `planned_test` field in [inventory.json](inventory.json) is the trigger-specific test specification for each row. All provider responses must use fake `HttpURLConnection` instances and local fixture streams; no real provider/network dependency is needed.

Required coverage:

- **Direct producers:** exercise all twelve conditions, exact response/field boundaries, zero and multiple page entries, invalid metadata namespace/page/source, cache-commit false and compress false. For cache/PNG failure, use a test-only shadow or context wrapper so production has no new failure hook. Also prove accepted boundary cases still pass.
- **Real gallery routes:** drive the existing WebView action callback. Show every reachable metadata reason through both Copy credit and image insertion; show redirect/PNG reasons through the image path. For M01, prove normal invalid-page rejection and the conditional post-validation truncation route on insertion, in addition to direct producer/mapping coverage. Do not classify M01 as a normal Copy credit failure.
- **Side effects:** Copy credit failure leaves existing clipboard content, document ledger/edited credit and activity result unchanged, opens no image request and creates no gallery image. Insertion failure returns no successful image, adds no credit, cleans temporary files and releases connections/bitmap/streams as applicable. Preserve a pre-existing edited-credit fixture.
- **Recovery/lifecycle:** retry success after each failure category, suppress duplicate requests, do not render after Close/Done/Back-driven destruction, disconnect an in-flight fake request, and retain already-supported rotation behavior. A discarded late result must not create a success or stale failure message.
- **Untyped controls:** malformed JSON, a library/network exception, null/empty/whitespace messages, literal percent/newline detail, OOM and linkage must retain the relevant settled wrapper behavior. Provider metadata fields and existing imported/edited credit text must remain unchanged.
- **Catalogue resolution:** verify exact resources/placeholder counts for every implemented tag, plus explicit unresolved/fallback dispositions for all other offered tags. Select/wrap through the actual `AppLanguage` path, with API30 and API35 host resource checks for relevant qualifier differences. In particular, retain an exact `ko-Kore-KR` versus `ko-KR` diagnostic; do not explain away a wrong resolution as fluency or silently accept a neighboring catalogue.
- **Readability:** representative English/French expansion, Arabic RTL, Japanese, Mongolian/Manchu vertical and Nôm text, 1×/2× font scales, short/portrait/landscape surfaces. Assert complete underlying status text, accessible live-region text and reading-start reset; inspect renders. Host captures are not installed/physical screenshots or TalkBack speech proof.
- **Final gates:** `python3 tools/translation_catalogues.py`, the existing translation and relevant source/fixture contracts, new focused tests, then the repository's Android unit/lint/build/current-platform checks. Run a broader installed matrix only for release or a concrete cross-version risk under `CI.md`. Record failed, blocked, unrun and passed stages separately, tied to the final exact head.

## Verification performed for this report

- The [source manifest](source-manifest.json) records **199** relevant source/resource/test/document byte hashes. Local source bytes were checked against the GitHub recursive tree at the pinned develop commit, without modifying a working branch.
- [verify_inventory.py](verify_inventory.py) checks those exact bytes, all twelve literal positions, the source-route partition/anchors, all 140 tag dispositions, proposed-key non-collision, the single placeholder contract, PR34's 61-production-path overlap and current render/provider boundaries and a labelled URL/query model of the conditional M01 insertion path.
- [Inventory verification](inventory-verification.log): **9 offline audit checks passed**. This is source/manifest verification only. No Android JVM, AAPT, lint, APK, emulator, device or linguistic test was run for this evidence-only report; no translation was supplied.
- The checks intentionally require the pinned input. A later implementation should produce a new source manifest and successor results rather than altering this historical audit.

Reproduce against the pinned source checkout:

```sh
python3 verification/commons-metadata-message-inventory-2026-10-09/verify_inventory.py --source-root . -v
```

The publication receipt is established separately by byte/tree/ref readback. The evidence branch adds only this report directory and leaves every inherited source and test blob unchanged.
