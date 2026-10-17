# PR 114 independent runtime-compatibility acceptance audit

This v6 record covers the representative non-null samples described below. A later hosted test found present-null compatibility outside those samples; v7 repairs and independently checks it. The v7 addendum supersedes v6 as the current acceptance result.

Date: 17 October 2026. Scope: frozen v6 translation-runtime patch, composed with the updated Polish/Czech catalogue base. This is an ordinary robustness and compatibility report, not a linguistic acceptance or an installed-device result.

## Result

No concrete defect remains in the reviewed v6 delta. All 22 manifest entries match; exactly LocaleText.kt, LocaleTextTest.kt, LocaleTextBoundaryTest.kt and TRANSLATION_RUNTIME.md differ from v5. Prior review of unchanged files is retained. The earlier v5 scheduling delta was independently verified to consist solely of three main-looper idle calls after Cancel, final reopen and Apply; no assertions were removed or changed.

The repaired comparison ignores non-argument formatter tokens in the contract multiset. Argument indices, conversion types, multiplicities, flags, widths and precision still have to match. Literal tokens are still parsed and included in the token-count and numeric bounds; Java Formatter validates their legal combinations before output is accepted. Both added and removed escaped percent/newline literals are allowed when the argument contract is unchanged.

## Independently executed checks

- Freshly compiled production LocaleText and its 10 pure JUnit tests: pass.
- Additional 25 literal-token controls: pass, including the token-count boundary, allowed bounded padding, rejected illegal padding/flags/newline forms, unchanged argument contracts, and formatted=false preservation.
- Additional 144 long malformed-template cases: complete fallback preserved; no timing assertion substituted for behavioral assertions.
- Current XML catalogue inventory: all 48,421 non-default string/plural-form rows match the supplied sweep identities exactly, with no missing or extra row. Actual LocaleText.resolve versus direct Formatter output: 5,780 formatted and 42,641 plain rows, zero mismatches and zero Formatter errors.
- Fresh AAPT15-decoded resource dump, independently parsed: 50,550 rows across 145 resource configurations, including 712 canonical default rows and 1,417 rows in the two generated mirrors. Actual resolve versus direct Formatter output: 6,071 formatted and 44,479 plain rows, zero mismatches and zero Formatter errors. All 205 alias-resolution operations had the exact requested resource configuration available.
- The pre-repair production boundary independently produced exactly 18 output mismatches on the old 47,955-row catalogue. The repaired boundary preserves all 18 complete existing Ainu Kana, Ainu Latin and Manchu strings. These are runtime compatibility checks, not a new judgment about their wording.

Representative arguments were derived from each source token's type and included percent-containing Unicode string data. Plain resources were compared without interpolation. Each plural form was checked; this does not simulate the platform's locale-selection or plural-selection algorithm on a device. The AAPT dump is decoded compiled resource data, not a screenshot or installed-app execution.

## Remaining resource and static paths

Main-source search covered both application/library modules, all Kotlin/Java/C/C++ sources, and XML manifests/resources. There are 21 formatting-containing source lines: 3 in the guarded boundary, 15 using fixed literal numeric/hash templates, 2 platform date-format calls, and 1 native libtiff diagnostic. A source line can contain more than one call. The full inventory follows below.

- Raw Android string/plural resource retrieval is confined to UiText's canonical source/metadata lookup and candidate lookup. No remaining translation-derived String.format, Kotlin .format, MessageFormat, getString-with-arguments or getQuantityString-with-arguments bypass was found.
- Resource IDs held in enums, category tables and when branches reach ui() before display. PaintTool label/hint, ToolCategory, AssemblySort, EditIcon, colour field labels, save-format descriptions, bitmap error descriptions, gallery error reasons and IllustrationSource descriptions were checked.
- AppLanguage reads four canonical translatable=false arrays: app_language_tags, app_language_names, app_language_aliases and app_language_alias_targets. They have no localized overrides. These are build-owned picker metadata, rather than formatting templates; changing array structure is excluded from arbitrary translation text.
- Neither module has XML view/manifest @string or @plurals display references. The launcher label is the appName Gradle placeholder. Other XML resources are locale configuration, provider paths, styles, IDs, drawables and launcher assets. The editor33/editor34 string migration files contain no entries.
- The only Kotlin main source outside the classic package is MyProvider, a bare FileProvider subclass; the app module has no separate main Kotlin/Java formatting code.
- GalleryPage and all IllustrationPage provider branches JSON-quote labels and assign textContent. Action schemes/provider identities are independently chosen and do not depend on translated captions. This source inspection complements the existing bounded DOM/JSON tests; it does not claim all WebView versions were exercised.
- There are 173 non-default catalogue files: 142 contain rows and 31 are explicitly empty fallback catalogues. The three default non-translatable filename strings have no translated entries. Generated fallback/contract entries are excluded from the translated inventory, while compiled mirror rows are included in the compiled sweep.

## Exact formatting-containing source lines

- Paintroid/src/main/cpp/tiff_bridge.cpp:75 — native diagnostic
  `if (!state.failed) vsnprintf(state.message, sizeof(state.message), format, args);`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt:66 — fixed literal template
  `return "$name: ${String.format(Locale.ROOT,"#%06X",colour and 0xffffff)}"`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt:128 — fixed literal template
  `tag = tagName; contentDescription = ui(R.string.ui_colour, String.format(Locale.ROOT, "#%06X", colour and 0xffffff))`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/AdvancedColourDialog.kt:370 — fixed literal template
  `field.setText(if (key == "hex") String.format(Locale.ROOT, "#%06X", c and 0xffffff) else String.format(Locale.getDefault(), if (key in listOf("r","g","b")) "%.0f" else "%.2f", numbers[key]))`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt:156 — date formatting
  `card.addView(text(item.timestamp?.let { DateFormat.getDateTimeInstance(DateFormat.SHORT,DateFormat.SHORT).format(Date(it)) } ?: ui(R.string.ui_time_unavailable),10f).apply { maxLines = 1; ellipsize = TextUtils.TruncateAt.END })`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt:972 — fixed literal template
  `cell.contentDescription=cell.colour?.let {ui(R.string.ui_colour,String.format(java.util.Locale.ROOT,"#%06X",it and 0xffffff))}`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt:982 — fixed literal template
  `.setItems(entries.map {String.format(java.util.Locale.ROOT,"#%06X",it.second and 0xffffff)}.toTypedArray()) {_,which ->addColour(entries[which].first)}`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt:997 — fixed literal template
  `EditorDialogBuilder(this).setTitle(String.format(java.util.Locale.ROOT,"#%06X",store.colour(index) and 0xffffff))`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt:1152 — date formatting
  `.setTitle(ui(R.string.ui_export_recovery_copy_144b8a)).setItems(copies.map { java.text.DateFormat.getDateTimeInstance().format(java.util.Date(it.lastModified())) }.toTypedArray()) { _,i -> choose(copies[i]) }`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/ColourStatusButton.kt:39 — fixed literal template
  `private fun hex(c: Int)=String.format(Locale.ROOT,"#%06X",c and 0xffffff)`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/DimensionControls.kt:59 — fixed literal template
  `private fun format(value: Double) = String.format(Locale.ROOT,"%.4f",value).trimEnd('0').trimEnd('.')`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/HistoryArchive.kt:36 — fixed literal template
  `private fun hex(bytes: ByteArray)=bytes.joinToString("") {"%02x".format(it.toInt() and 255)}`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCreditArchive.kt:88 — fixed literal template
  `return digest.digest().joinToString("") {"%02x".format(it.toInt() and 255)}`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/ImageCropDialog.kt:82 — fixed literal template
  `field.setText(String.format(Locale.ROOT,"%.4f",n).trimEnd('0').trimEnd('.'))`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/LegacyImageCredits.kt:41 — fixed literal template
  `.digest(source.toByteArray(Charsets.UTF_8)).joinToString("") {"%02x".format(it.toInt() and 255)}`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleText.kt:107 — guarded boundary
  `try { return String.format(locale, candidate, *values) }`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleText.kt:118 — guarded boundary
  `if (token.index == null) String.format(locale, token.standalone())`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/LocaleText.kt:120 — guarded boundary
  `else String.format(locale, token.standalone(), value)`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/NormalizeImagesDialog.kt:35 — fixed literal template
  `input.setText(if (percent) String.format(Locale.ROOT,"%.4f",pixels*100.0/largest).trimEnd('0').trimEnd('.') else pixels.toString())`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/PaintCanvas.kt:217 — fixed literal template
  `fun zoomLabel(): String = if (zoom >= .1f) "${(zoom * 100).roundToInt()}%" else String.format(java.util.Locale.ROOT, "%.2f%%", zoom * 100)`
- Paintroid/src/main/java/org/catrobat/paintroid/classic/RasterHistory.kt:59 — fixed literal template
  `val actual=digest.digest().joinToString("") {"%02x".format(it.toInt() and 255)}`

## Evidence identity and limits

- v6 manifest: SHA256 4bb257b58596e05c759402ad66f9160c5c058496d7b3ff2bc69fecdcaab7abff
- production parser: SHA256 aa34edd212dfe6cd4b740819a8a6e72313b117d02190ad27a77d53461bde2899
- pure tests: SHA256 cccec1387ca2d0eb06757cc7be7e1885c7e5c07ec766df993f1022b83caa685e
- XML sweep TSV: SHA256 0645058101e31bc3cb91ce3a8076e8890cee72c389cf0c55d158ad334e9f5616
- AAPT decoded dump: SHA256 fc5bec9ed16cd9b2ebd8772824f17c00f8fa2006889eb5808423cbfc169dc528

This review does not replace exact-head hosted Gradle ordering/invalidation, lint, unit/instrumentation or emulator gates. The full main/test compile and hosted results are reported separately by their owner. Invalid XML, missing/corrupted canonical resources, structural metadata changes, native/platform layout/font behavior, unbounded caller-supplied argument size and linguistic correctness remain explicit exclusions. No universal “arbitrary text can never cause an error” claim is made.

## Reproduction helpers

The adjacent independent-review directory contains the independent JVM rendering comparison, compiled-dump input extractor, literal controls and long-template controls. They use the unchanged production Kotlin class. Compile LocaleText.kt and LocaleTextTest.kt with the repository Kotlin/JUnit dependencies, then compile the Java helpers into that same temporary classes directory. Run the pure JUnit class, LiteralControls and Adversarial with kotlin-stdlib on the classpath.

For the decoded sweep, run compiled_sweep_input.py with the exact AAPT dump path and an output prefix. It writes JSON/TSV input plus a summary that includes the dump hash. Run CatalogueRenderAudit against that TSV with the production classes and kotlin-stdlib. The summary must report zero mismatches and zero invalid Java formats; the expected full counts above bind the result to this snapshot. The helper is an audit reader for this observed AAPT dump profile, not a generic untrusted-resource parser.
