# Shan priority review — frozen research record

**Final source-bound linguistic decisions; no application implementation, runtime validation or native-human certification.**

Baseline: [`96681f687671a1fdffe134a325843919c1543401`](https://github.com/c933103/AN-Paint/commit/96681f687671a1fdffe134a325843919c1543401), tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`. Snapshot completed **2026-10-30 22:02:46.021652 UTC**, after the reviewer confirmed the final records were stable.

## Final accounting

| Missing-resource outcome | P0 | P1 | Total |
|---|---:|---:|---:|
| Accepted lexical values | 26 | 114 | **140** |
| Accepted notation-only templates | 0 | 7 | **7** |
| Held; excluded from additions | 27 | 9 | **36** |
| Entire missing-resource scope | **53** | **130** | **183** |

**147 missing values accepted = 140 lexical + 7 notation-only.** The seven templates have zero lexical-progress credit; dynamically inserted text is not thereby localized. The 36 held keys retain English fallback. This is not a completed-language claim or evidence that any value has been integrated.

### Read first

1. [Authoritative final publication ledger](independent-review/shan-review-publication-ledger-20261030.md): complete scope, exact-value precedence, confidence, source qualifications and every hold. Original SHA-256: `db80d17e4dcade2bd926cae2ebbdf57cd6c9853288358cce4296a7d42fd31ee0`; this file is published byte-identically.
2. [Accepted missing-value ledger](accepted-missing-ledger.tsv): a mechanically assembled 147-row convenience table applying that precedence, with exact source/target representations, attributes, confidence and decision-record references. [Held index](held-index.tsv): 36 excluded keys with item-specific reasons and provenance.
3. [Original author packet](author/) and [independent decision records](independent-review/): retain the original candidates, their historical decisions, exact successors and evidence. The convenience ledger introduces no new linguistic decision.

These TSVs preserve their original text representations, including literal backslashes and Android serialization quotes. They are review records, **not an import-ready resource patch**. No escaping normalization, placeholder transformation or target-wording correction is performed by publication.

## Palette resolution and separate P2 scope

The final [palette decision](independent-review/shan-review-palette-resolution-independent-20261030.tsv) supersedes **only** batch E's historical hold on `ui_foreground_background_colour_palette`, using the exact new em-dash topic/instruction target. Its [historical-contract report](independent-review/shan-review-palette-resolution-independent-20261030.md) binds the recovered caller at commit `f47d9ee9458f2f9207eae5e3514f211baecdfa51`: the third argument is the complete left-collapse/right-expand instruction, not a state, name or count. Hex arguments already supply `#`.

[Four exact compositions](independent-review/shan-review-palette-compositions-independent-20261030.tsv) preserve two full-Shan examples and two conditional English-fallback examples. Both arrow fragments are absent from the frozen production Shan catalogue; the left P1 wording is independently accepted but not implemented. The [right-arrow P2 wording](ancillary-p2-wording.tsv) is **ancillary linguistic evidence only, with zero P0/P1 credit and no source-integration authorization**. Current code no longer invokes this historical composite. The English-fallback examples remain mixed-language, not observed runtime or TalkBack results.

The reviewer separately preserved this exact delta in [PR 56's palette review comment](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6534460471). The complete tables are archived here; that comment alone is not their archive.

## Existing values and review history

[Existing-value decisions](existing-value-decisions.tsv) are separate from the 147 additions: **Undo accepted unchanged**, including its exact Android outer quotes; **Brush accepted as a replacement** after second-check. The Brush decision supports the new wording, not a proven-defect allegation against the previous unreviewed compound. Prior PR 237 acceptances and six earlier unchanged Shan decisions earn no duplicate credit.

Historical receipts retain the conclusions of their recorded stages:

- `shan-review-final-receipt-independent-20261030.md` is the earlier **A/B/C 95-missing-accept snapshot**, despite its historical filename.
- `shan-review-batches-def-independent-20261030.md` is the **pre-palette 146-accept snapshot**.
- Original A/B/C held/corrected proposals and E's palette hold remain visible. The final publication ledger, resolution TSV, exact F successors and palette decision establish current precedence; do not revive superseded candidates.

This separate Shan directory does not overwrite the previously preserved Yucatec/historical-language snapshot. In particular, that earlier historical rev9 packet remains a dated snapshot, not a claim about the latest historical-language revision.

## Integrity, provenance and limits

- [Snapshot manifest](snapshot-manifest.tsv): **45 input files**, their original snapshot and published SHA-256 hashes, byte sizes, Git blob identities and sanitization status. Fourteen files have metadata-only changes removing temporary paths or internal operational coordination; one of these is a rationale-only TSV edit. **Exact source, target, key, attribute and decision values are unchanged.** Embedded historical hashes still identify original input bytes; use this manifest to map sanitized copies.
- [Source bindings](source-bindings.tsv): exact English resource, Shan resource, priority map and existing review manifest. Computed Git blob identities and byte sizes match the remote frozen-baseline tree. Original reviewers' narrower local-checkout attestations remain distinguishable from this publication verification.
- [Source URL index](source-urls.tsv): cited source URLs and their evidence records. Source titles, attribution, historical/current distinctions, contextual lexical limits and confidence remain in the reports.
- [SHA256SUMS](SHA256SUMS): checksums for all published files except the checksum file itself, whose bytes are bound by the immutable Git tree. Document inventory/hash checks establish the stated counts; they are not project parser, build, UI or runtime tests.

Only authored translation/review work is published: no raw third-party PDF/TMX corpus, credentials or unrelated private data. Public repository visibility and the [existing repository license](https://github.com/c933103/AN-Paint/blob/96681f687671a1fdffe134a325843919c1543401/LICENSE) remain unchanged; cited external works retain their own rights and attribution. No external corpus is relicensed by this record.

No application, resource, test or workflow file is changed. Integration, font rendering, compact-control fit, installed UI and TalkBack behavior remain unverified and outside this publication.
