# PR85: gallery external-link handler evidence

This compact, separate-ref evidence accompanies [PR85](https://github.com/c933103/AN-Paint/pull/85). It contains review conclusions and exact statements, not a whole-source copy or raw test logs.

## Source binding

- Base commit: `0aa6c89c9d3a4d133a8b231e7002783b60ead46d`
- Expected application tree: `faa0cf1d9976061ca970c92a8625e11febbc3929`
- Prior PR85 head: `67ef4516c6359e613688af6830ec129c30536ad3`
- 68 changed/new files; 1136 target files; no removals or mode changes

The tree hash is immutable content identity. The publisher must verify that the published application commit resolves to this tree; these preparation records do not invent or certify a commit not yet read back. `source-binding.json` contains principal source blob/SHA-256 hashes and all 59 statement-to-resource bindings.

## Contents

- `complete-statement-review.json`: all 59 exact final statements, full independent model-assisted review conclusions, individual limits, primary lexical evidence, and corrections. These are full-message reviews rather than placeholder/script checks.
- `source-binding.json`: the reviewed text matches the final canonical XML and fixture for all 59 scoped tags, with immutable application-tree and principal-file binding.
- `code-test-review.json`: independent bounded code/test review and verified host aggregates (717 normal, 717 optimized; independently 35 focused checks in each mode), including corrected earlier attempts and local Android blocker.
- `manifest.json`: SHA-256, Git blob identity and byte count for these compact evidence files.

## Limits that remain open

The 59 scoped catalogue entries comprise 50 non-English statements, 7 ordinary English variants and 2 synthetic options, plus the separate default English resource. All 112 outside-scope catalogues continue explicit English fallback. This review does not restore withdrawn audit conclusions or credit any pre-existing catalogue entry. The merged-source denominator stays 706 until PR85 merges, when the new key makes it 707.

Whole-sentence idiom/attestation remains unresolved for `ain-Kana`, `ain-Latn`, `hak-Latn-TW`, `mnc-Mong` and `ryu`. Other individual medium-confidence language/script limits, including Cebuano, are retained in the full reviews. No reviewer claims human/native-speaker certification or whole-catalogue completion.

Local Android compilation, lint and the six new Robolectric methods were not run: the wrapper distribution download failed before compilation with network unreachable. Hosted exact-head results must be linked separately. Host tests and a future Robolectric pass do not prove installed browser/device/provider-network behavior.

The previous PR85 tracker remains in the application tree with its original evidence and a current-status link. Existing processing-label holds and the separately recorded inherited Hakka file-picker wording issue are outside this correction and receive no completion credit here.
