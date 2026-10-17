# Latvian P0 + P1 review, 17 October 2026

Application source: [`d72b43478c020f55faae9e358f57ff88b3254b0d`](https://github.com/c933103/AN-Paint/commit/d72b43478c020f55faae9e358f57ff88b3254b0d); tree `ff1b183c1449a10f55d43489ef8d41541f11ff5c`. Parent: `7745432c266f62f3b57a4f4fdca08adf46004eb0`.

This dedicated evidence ref is additive to that complete application source tree. It is not a production PR and does not remove or rewrite retained source. All 1,209 application leaves were verified by exact Git blob, path and executable mode before branch publication and CI.

## Scope and outcome

All 341 English/Latvian P0/P1 pairs (92 P0, 249 P1) were reviewed individually with actual consumer context where present, then independently challenged. Author ledger: **285 accepted within bounded static context, 28 wording-only without a direct current consumer, 10 corrected, 18 uncertain and unchanged**. These are review dispositions, not native-speaker certification or tracker acceptance. The independent review's narrower five terminology-held keys are reconciled explicitly with the author's more conservative source/context holds.

Eleven XML values change: ten priority entries and the P2 width-template companion required for the same four width/height-by-unit compositions. [Complete English/old/new values](corrections.json) are readable separately. Other 331 priority values and all other resource values/attributes remain unchanged.

The corrections cover animation/pixel counts, the language-picker's missing English-fallback guidance, all four dimension accessibility compositions, selected-tool agreement, and palette tap/hold instructions. Six Kotlin tests exercise real consumer behavior; seven host tests validate full wording/structure and reject old or damaged values. Category tests cover every tool and expanded/collapsed state, animation tests cover exact and lower-bound counts, and palette tests preserve the canvas while exercising tap and hold.

## Prior evidence and retained uncertainty

The current PR search returned only withdrawn historical PR4 for Latvian. PR56 head `cc1d2718b88b9f08e25b3013ccdbc10770e7f332`, receipt blob `004a38a070bc4ea215a82fdd41028aac5e341f3b`, contained nine Latvian records across the catalogue. **Only one overlaps these priority keys**: `ui_sampled_resize_memory_explanation`. Its complete source and translation hashes still match. The other **340 have no prior tracker receipt**. Nothing receives double review credit; PR56 is read-only and no counters/receipts were changed.

Uncertain technical terminology and source-context compositions remain explicitly recorded. This includes dithering, sampled decoding, source tiles and colour management; author holds also preserve unresolved attribution/compact-label/grammar/context points. The P2 crop-side template observation remains outside this patch. P3 remains deferred; Swedish expansion and paused processing-label locales remain untouched.

## Verification

- Final-source host suite: **931 passed normally and 931 passed with Python optimization**.
- Focused wording contracts: **7 passed normally and 7 optimized**; independent reviewer also ran the seven host checks.
- Complete AAPT2 resources, both exact-script mirrors and resource link: passed.
- Supplementary changed Kotlin/test-helper compilation with fresh resource symbols: passed. Previously compiled dependencies were used only for this explicitly limited local compile check, never a claim of a clean build.
- Full local Gradle/Robolectric: blocked at wrapper download by unavailable network after a writable cache retry. Raw first failure and retry are preserved. Hosted build, JVM and device checks are pending at packet creation.
- No installed Latvian layout, native fluency or TalkBack acceptance is claimed.

## Full evidence

[Full review packet](full-review-packet.zip), SHA-256 `5c691dfc9ce5edbfd9798b332c20e20eb981cea6dd78ab7b41e43135cfb70c7b`, contains the complete paired ledger, independent per-entry review and exact-final addenda, source consumer excerpts, prior receipt proof, source inventory/validation, and raw successful, failed and superseded local attempts. [Manifest](packet-manifest.json) hashes every enclosed file. Fixture-generated diagnostic failures inside passing aggregate logs are retained verbatim; aggregate status comes from the runner summary and exit file.

No prior report is replaced. Followup hosted-CI evidence may be appended on a descendant evidence commit; cite immutable commit links for each result.
