# Translation runtime hardening: validation and compatibility

Source PR: https://github.com/c933103/AN-Paint/pull/114

Current source head: `e434c5e779183a017ca9153e688dc77a79a0fc39`.
Source tree: `a39746ee5b7bb4d51bcd66f88697e26a0adf05ce`.
Reconciled develop base: `38d4cbef9fff10bcb758f36b1908c4b87958d3d9` (merged PR112).
Independent v7 manifest SHA256: `d410b790dae9752966ccef9807706e24213d60e7426dc883506e67a1b0da841d`.

All 1,176 source blobs/modes match the reviewed local tree. All 182 values-resource XML blobs, including all catalogues, match develop byte-for-byte. In particular, the 18 existing Ainu Kana/Ainu Latin/Manchu values using escaped percent signs are unchanged: the code now accepts their valid literal `%%` formatting. No percent symbol was replaced with the word “percent,” and no translation was edited to accommodate the implementation. Polish/Czech resource/test additions are inherited from PR112.

This evidence is supplementary validation, not a substitute for exact-head hosted Gradle/JVM/lint/Android gates. The source PR contains code, behavior tests, generator and concise documentation only; bulky outputs are kept on this separate evidence ref.

## Executed current-head checks

- All production Kotlin/Java sources and both new boundary test classes compile with pinned Kotlin 1.9.24 dependencies and the API35 SDK. Eleven pure JUnit tests pass, including 2,500 seeded mutations and all 18 exact complete source/translation regression pairs.
- Independent bounded review passes all 22 frozen file hashes, 207 null/presence/wrong-type controls, 25 literal-token controls and 144 long malformed-template controls. The adjacent report lists every remaining raw formatting-containing line and explains XML/static/picker metadata exclusions.
- Current catalogue behavior sweep: 48,421 XML-inventory rows, 5,780 formatted and 42,641 plain; zero mismatches and zero Java formatter errors. No newly rejected values. A further 23,632 present-null comparisons also match existing Formatter behavior.
- AAPT-decoded behavior sweep: 50,550 rows across 145 resource configurations, including default and existing generated mirror resources; 6,071 formatted and 44,479 plain, zero mismatches and zero formatter errors. An additional 24,820 present-null comparisons pass. All 205 alias resolutions had exact-configuration targets. Each plural form was checked independently of platform plural selection.
- AAPT15 compile/link/dump succeeds. All 711 default string/plural entries retain their compiled values after reserved-ID/alias rebinding; all 711 explicit formatting contracts match generated XML. Source-generation tests cover aliases, plurals, source contracts and application/library/variant namespace rejection.
- Full combined-base normal host aggregate: 849 tests pass. The first optimized run finished 849 tests with one unchanged instrumentation-matrix negative-control subprocess exceeding its existing 10-second cap; the failed log is retained. The exact focused test and optimized aggregate are rerun unchanged, with terminal results in `host-v7-rerun-results.json`. See complete logs for all outcomes. Earlier combined-base v6 aggregates each passed 849 tests; those results are not acceptance of the final v7 code delta.

The local Java runtime is OpenJDK21 with no `--release` platform table. The initial `--release 17` failure is retained; successful supplemental Java compilation uses `-source 17 -target 17`, which does not establish exact hosted JDK17 compatibility.

## Hosted evidence and review

Current exact-head run: https://github.com/c933103/AN-Paint/actions/runs/39014409987

The hosted resource-graph gate passed. Its downloaded artifact has SHA256 eb42464ffb1cbe9043b933661e7cc7c5ac4097a6d3607bb5d654ca10e47a2d09; summary.json binds the synthetic merge commit db5bd30 to the exact reviewed tree a39746ee5b7bb4d51bcd66f88697e26a0adf05ce. The archive includes successful clean/incremental/source-change probes and the expected failed reserved-name overlay probe.

Exact-head code review completed with no findings in receipt6231323104 (requested by comment6231301537). Exact-head security review was requested by comment6231301895; at this snapshot its last completed receipt still refers to earlier head db076197 and is not counted. Final hosted/review status is recorded in the PR and follow-up evidence, not inferred from a request.

The earlier head `6ddc9eaf5baea9dc6f6c1eab1d1877e98bddff50` built successfully and passed the actual clean/incremental/release-first/resource-input mutation/stale-output/negative application debug overlay probe in run39012832234. Its regression log completed 1,084 tests with 12 failures before the job was superseded: three null-wrapper compatibility assertions, six hardcoded test-package lookups, and three dialog-looper assertions. The cancelled core emulator makes its roll-up fail; the position-dialog emulator passed. All job metadata/logs are retained separately. It is not acceptance of the current combined head.

## Retained failures and corrections

- Initial host aggregates each failed three source-route assertions requiring the old raw format/plural call sites. Updated assertions require guarded routes with the complete original argument lists and negative controls rejecting raw-call substitutions. No wording/full-text assertion or timeout was relaxed.
- An initial generator assertion compared XML attribute serialization order. It now compares canonical XML while retaining every source attribute, complete text and structure, except documented reserved names, rebound aliases and `translatable=false` metadata. The initial failure is retained.
- An initial AAPT equality harness assumed numeric alias IDs; this AAPT emits named references. The harness was corrected before the final derivation receipt.
- The catalogue sweep found 18 valid escaped-percent translations that the initial argument contract rejected. All 18 strings stayed byte-for-byte unchanged. Only non-argument literal tokens were removed from contract equality; token syntax/expansion bounds and argument types/indices/multiplicities remain enforced.
- Dialog tests gained deterministic main-looper drains after Cancel, reopen and Apply, preserving all assertions.
- Present-null values now retain Formatter behavior for all current conversions; omitted argument indices remain distinct and render only that missing source slot as `?`. Tests compare accepted translations and forced-source fallback against Formatter for null, without weakening wrong-type/missing-slot checks. Two test-only resource lookups derive the actual package owner instead of assuming a package name.

## Reproduction and limits

The archive contains source/test hashes, complete host/compiler/resource logs, generator outputs and reproducible commands. The independent report/helpers reproduce the actual production-boundary behavior sweeps from the exact source tree and AAPT dump. Large regenerated catalogue JSON/TSV is omitted because it is derived by those scripts from already-retained source/dump inputs.

Robolectric boundary tests compile locally and execute in hosted CI. Malformed-resource injections happen after Android resource decoding; they do not claim a deliberately invalid XML catalogue can package. Packaged Ainu/Manchu selection controls separately cover the 18 valid literal-percent translations. Real WebView/device/font/layout behavior, finite memory, unusually large caller arguments, native/OS errors, source-ID or package corruption, structural picker metadata and linguistic correctness retain separate limits. No universal crash-proof or linguistic-acceptance claim is made.
