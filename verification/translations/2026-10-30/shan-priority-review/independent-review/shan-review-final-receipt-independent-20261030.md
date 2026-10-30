# Final source-bound independent review receipt — Shan A/B/C

## Final accepted scope

After exact-wording revision review and independent author second-checks:

| Category | P0 | P1 | Total |
|---|---:|---:|---:|
| Missing lexical target values, batches A/B/C | 19 | 69 | **88** |
| Missing notation-only values, separately classified | 0 | 7 | **7** |
| Existing values newly reviewed here: Undo unchanged, Brush replaced | 0 | 2 | **2** |

**95 missing resource values** are accepted (**19 P0 + 76 P1**), of which **88 contain lexical translations** and **7 are unchanged notation/templates**. Two existing-value reviews are additional and must not be represented as missing translations. This is acceptance scope, not a claim that production was modified or official residual counts have already changed.

All six initial A/C lexical holds have now been resolved by **new exact wording**, not by silently upgrading the old phrases. Two B trim proposals have an exact second-check receipt. Existing Brush replacement has the recorded independent author acceptance and supporting brush reassessment.

The **14 separately recorded draft-object holds** remain unresolved and excluded. Previously accepted PR237 additions and the six prior unchanged SHN decisions remain untouched and receive no duplicate credit.

## Integration precedence — do not integrate superseded targets

1. Use exact accepted originals from the A, B and C reviewer TSVs for rows marked `accept`.
2. For the six original held keys and the two B corrected keys, use **only** exact values in `shan-review-resolutions-independent-20261030.tsv`. This overrides the corresponding historical hold/correction rows.
3. For existing `ui_brush`, use the exact replacement in that resolution TSV, not the old unreviewed compound. Existing `ui_undo` remains exactly serialized as `"ၶိုၼ်ၶိုၼ်း"`.
4. For seven nonlexical templates, use `shan-review-format-invariants-independent-20261030.tsv`, preserving their separate credit classification.
5. Do not introduce any value from `draft-term-holds.tsv` or any other unreviewed prior candidate.

No source file, accepted manifest or official count was modified by this reviewer.

## Why the revised wording clears the holds

### Encoding family

Five revised clauses replace ambiguous code-entry calques with an explicit **convert image/selected content into file data** construction. Independently reviewed as full sentences:

- PNG failure preserves PNG and inability to encode.
- Encoder non-completion names the converting component and says its work did not finish.
- Autosave full-image and selected-content failures remain different operations.
- Encoding-budget warning retains image plus temporary conversion buffers and an export working-memory limit.

The paraphrase does not assert successful writing to a final destination, does not imply user-entered program code and does not claim earlier autosave data was deleted. `ImageExporter.kt:23–25`, `IcoCodec.kt:98–100`, `TextImageCodec.kt:30–33`, `AssemblyActivity.kt:324` and `AutosaveStore.kt:132–134` support the precise output-conversion contexts. Longer wording is not claimed to have passed UI-fit checks.

### Clockwise rotation

Exact revised **ပၼ်ႇလိဝ်ၶႂႃ 90°** combines rotation with clockwise/rightward direction. [Unicode CLDR49 Shan summary](https://unicode.org/cldr/charts/49/summary/shn.html) contrasts clockwise **လိဝ်ၶႂႃ** in circular-arrow names with anticlockwise **လိဝ်သၢႆႉ**. With the rotational verb, this is not mere rightward translation or mirroring. Accepted at moderate idiomatic confidence; the previous clock-hand compound is not accepted.

### Trim and Brush second-checks

I read `trim-secondcheck-receipt.tsv`; both exact corrected targets match the independent reviewer proposals without alteration, and author acceptance explicitly preserves amount/every-edge/all-four semantics. The original attribution of **ၸမ်းတတ်း** to accepted vocabulary is corrected.

The review records independent author acceptance of **ယူႈယွမ်ႉသီ** for existing Brush; `brush-reassessment.tsv` supplies the exact word, [CLDR paintbrush mapping](https://unicode.org/cldr/charts/49/summary/shn.html), and actual tool context. This establishes a suitable reviewed replacement, not that the old word was proven defective.

## Canonical baseline and frozen input hashes

Declared source binding: merged develop **96681f687671a1fdffe134a325843919c1543401**, tree **39bb7351fa5532194e2c0430432b2f0cc6358a86**, selected English/SHN/importance/manifest files unchanged in materialized checkout `baseline resource snapshot`. No independently resolvable local Git HEAD is claimed.

Read-only SHA-256 inspection of the reviewed temporary inputs, 2026-10-30 21:10 UTC:

| File under `../author/` | SHA-256 |
|---|---|
| `batch-a.tsv` | `d30ba3b7332f135a39dd1e73c24f2f82fa6b589c1246fd890b07082fb16da2f7` |
| `batch-b.tsv` | `b032bf1d857fc977bc95edab01620756ca6868f76521b5d75c431b32835e22bb` |
| `batch-c.tsv` | `9d0bfa49e8a678cc99260cbf4208f701da10c957a5999809ceba233d873ec954` |
| `encoding-revisions.tsv` | `b4258ecba9bfe76bb594c50997a670ccdcc300f6ed8a49ab3c2b7ab83e1a3595` |
| `rotation-revision.tsv` | `f2a3303fa197868e37ff79f629b387c0bf2660cd5b43fe6900161c0b76547b89` |
| `trim-secondcheck-receipt.tsv` | `06b33d3e631d856d3dae41470dac7919ee7ad7f12f3ae660d49859e5114db30e` |
| `brush-reassessment.tsv` | `ebfba1de293fcdb82aa9b9ec69c6d210fdd79282729b94db6d4c04decfe1236c` |
| `format-invariant-review.tsv` | `d0c274d9e4b9ea0de8aa33c8b5756671f6c3c0a4e7dca14c49a6cbe9579679e4` |

Batch C's updated Pencil rationale was inspected. Exact candidate **ၵမ်ၸိုၼ်း** remains unchanged; current rationale now correctly says crisp edges at any selected width. The hash above is the corrected-rationale file, not its older pre-correction bytes. Hash inspection is source binding, not a technical test or proof of integration.

## Reviewer artifacts

- `shan-review-batch-a-independent-20261030.tsv` and `.md` — 37 original missing candidates plus two existing values, with historical decisions.
- `shan-review-batch-b-independent-20261030.tsv` and `.md` — 21 original missing candidates, with historical correction proposals.
- `shan-review-batch-c-independent-20261030.tsv` and `.md` — 30 original missing candidates, with historical encoding hold.
- `shan-review-format-invariants-independent-20261030.tsv` — seven separately classified templates.
- `shan-review-resolutions-independent-20261030.tsv` — exact final replacements and hold resolutions; takes precedence.
- This final receipt records current scope and frozen input hashes.

## Review limits

Independent **AI/model** linguistic/semantic review, not native-human certification, renderer/device proof, UI-fit verification, automated parser tests or a claim of complete locale coverage. All 97 scoped target values have exact per-item decisions, backtranslations/meanings, reasons and confidence across the reviewer tables. Sources, callsites, attributes and formatting were read and manually compared; no scripts/tests or source edits were run. This artifact records linguistic review only.
