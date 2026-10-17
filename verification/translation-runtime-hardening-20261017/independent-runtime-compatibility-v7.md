# PR 114 independent v7 null-compatibility review

Date: 17 October 2026. Result: the frozen v7 bounded delta passes independent review and execution. Earlier review acceptance is retained for unchanged files; v7 supersedes v6 for present-null argument compatibility.

## Reviewed change

All 22 manifest entries match. Exactly four entries differ from v6: LocaleText.kt, LocaleTextTest.kt, LocaleTextBoundaryTest.kt and TRANSLATION_RUNTIME.md. There is no catalogue, generator, Gradle or consumer change in this delta.

LocaleText now distinguishes an omitted argument index from a present argument containing null, both before accepting a translated template and while rendering source fallback. Java Formatter supplies the existing null behavior for every conversion. For the current catalogue this includes s, d, grouped d, zero-padded uppercase hexadecimal and floating-point precision 0/1/2. Present null therefore can render as “null”, “NULL”, “n”, “nu” or an empty precision-zero value according to the original format. This preserves compatibility, rather than inventing replacement wording. Missing indices still render only that source slot as “?”, and incompatible non-null values remain guarded by IllegalFormatException fallback.

Two boundary-test resource lookups now derive their package from the compiled resource ID, matching the existing production UiText lookup. No production package-selection change was needed. The previously reviewed three dialog idle calls remain unchanged. Existing missing-slot and wrong-type assertions were retained; null expectations were corrected and expanded.

## Independent results on the exact v7 parser

- Fresh Kotlin/JUnit compilation and 11 pure tests: pass.
- 207 additional null/presence controls: pass. These compare accepted translation and forced-source fallback with direct Formatter under ROOT, Arabic and Turkish locales; include current conversions and additional general/date/character conversions; retain omitted-slot, wrong-type, reordered and relative-index controls.
- 25 additional literal-token controls: pass.
- 144 additional long malformed-template controls: complete fallback preserved.
- Current XML catalogue: 48,421 ordinary rows (5,780 formatted / 42,641 plain), plus 23,632 present-null comparisons: zero mismatches and zero Formatter errors.
- AAPT-decoded compiled catalogue: 50,550 ordinary rows (6,071 formatted / 44,479 plain), plus 24,820 present-null comparisons: zero mismatches and zero Formatter errors.

For each formatted row the nullable sweep tests an all-null array and, where there is more than one argument, each individual position set to null with other representative values retained. Each array is checked both with the valid translated template and with a deliberately rejected translation forcing canonical source rendering. Counts are comparison cases, not distinct strings. All-null and mixed-null comparisons retain the full output oracle. The v6 parser failed all 24,820 compiled null comparisons, confirming this extension detects the repaired behavior rather than merely re-running the previous non-null oracle.

The XML and AAPT inputs are unchanged from the v6 inventory. They include the newly merged Polish/Czech rows; compiled data also includes canonical defaults and both generated mirrors. Details and remaining-format-path inventory are in the accompanying v6 report, whose non-null results remain valid.

## Evidence

Fresh compile, JUnit, literal, adversarial, null-control and both sweep stdout/stderr files are in the adjacent independent-review directory under v7-*.log. The rendering comparison helper now fails with a nonzero process exit if any mismatch or invalid Java format is found. To repeat the nullable sweep, run CatalogueRenderAudit with the input TSV path followed by --null-samples. Helper sources are included; full generated TSV/JSON inputs need not be archived because the supplied extractor and exact AAPT dump reproduce them.

- v7 manifest: SHA256 d410b790dae9752966ccef9807706e24213d60e7426dc883506e67a1b0da841d
- production parser: SHA256 1f70b6536b3339b7ad3548b44012d76248757d45fe356da65f459256841b5381
- pure tests: SHA256 b4ba56ecb1b1e18006d8f37a9494c2cac503b57146ffe56482d09663f6f3691b
- XML input TSV: SHA256 0645058101e31bc3cb91ce3a8076e8890cee72c389cf0c55d158ad334e9f5616
- AAPT decoded dump: SHA256 fc5bec9ed16cd9b2ebd8772824f17c00f8fa2006889eb5808423cbfc169dc528

This is a local exact-source review result, not a claim that v7 hosted CI or installed Android tests passed. Final publication/head binding and those gates are separate. Invalid build resources, structural picker metadata, platform/native font/layout behavior, caller-controlled output size and linguistic accuracy retain the exclusions documented in the broader inventory.
