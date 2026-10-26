# Nynorsk: eight P0 save/export/share messages — bounded review

The independent review accepted five candidates unchanged and supplied three clarity revisions. Exactly eight final whole values are approved for the stated AI linguistic/static scope. This is not native-human, complete-language, physical-device, layout or release certification.

The candidate packet and its source-context windows remain unchanged at [r01](https://github.com/c933103/AN-Paint/tree/bbc98e13d30f8b0137ee6b6f4715b5c61a32eded/records/localization-review/2026-10-26/nynorsk-p0-save/r01). Candidate SHA-256: `deb1f64fdcba57228004ace4f402cffd5ae3269494e7a71ba1eeb7acc03903c2`. Source: AN-Paint `develop` commit `d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4` (not the separate `main` branch).

`independent-review.json` preserves all eight decisions, exact text/hashes and qualifications. Its review-time statements (no implementation, no tests and no coverage increment) describe the review stage, not the later implementation. The public export removes only an internal reviewer identifier and operational bookkeeping; the original review SHA-256 is retained.

## Consumer check and proposed implementation

The reviewed export warning now starts “Eksportfila er oppretta.” The export and share explanations refer to “kva fil «Lagra» lagrar til”: the full saved file destination, not merely a directory. Source inspection confirms that a successful export writes a file without updating `savedTarget` or marking the current drawing saved. The success status names the written file; it must not be interpreted as clearing unsaved drawing state. Share uses the export path. The failure prefix has no final punctuation because the caller adds punctuation and an exception/fallback detail.

`implementation-bindings.json` identifies the minimal proposed resource/test payload. All 110 prior Nynorsk values and their attributes are preserved; only eight missing P0 values are added (118 present containers). Nynorsk P0 presence would change from 7/92 to 15/92 after application; 77 remain missing. The separate 59 scoped / 112 fallback-locale distinction is unchanged. Neighbouring fallbacks and inherited action wording are not newly accepted.

Five focused host tests passed in ordinary and optimized Python, including exact values, resource attributes, `%1$s`, missing/duplicate/truncated/markup/wrong-type negatives and untouched neighbours. The aggregate host suite is still pending when this review record is prepared. Compiled Android/Robolectric tests are authored but unrun locally because the Android SDK/toolchain is unavailable; exact-head hosted CI is required before merge. No runtime, layout or native-language acceptance is inferred from source-only checks.

PR56 remains never-merge; PR159 stays frozen; PR113 retarget/held-warning, Help callback/archive identity and release holds remain unchanged. This packet makes no release or application-logic change.
