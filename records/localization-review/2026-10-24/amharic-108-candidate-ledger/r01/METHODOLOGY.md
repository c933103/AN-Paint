# Methodology and accounting

This is a read-only consolidation of existing reviewed records, not new language review or an implementation payload.

## Source and boundary

- Canonical English and Amharic presence were parsed from the supplied source snapshot at [66be61df27c5359bffc32d56db21f3949899f873](https://github.com/c933103/AN-Paint/commit/66be61df27c5359bffc32d56db21f3949899f873). The exact source-file integrity checks are retained outside this public artifact.
- The records are bound to [c9f5d54ccaee4ed7e7799febb66c560ba3116ef6](https://github.com/c933103/AN-Paint/blob/c9f5d54ccaee4ed7e7799febb66c560ba3116ef6/records/localization-review/index.json); initial and successor links use immutable publication commits.
- No separate 90-key consolidated packet was found among the inspected Amharic candidate artifacts. The original 90 was reconstructed from the accepted arrays in the following eighteen dated packets, in index order. Rejected drafts and held rows are excluded.

| Group | Accepted keys | Immutable decision |
|---|---:|---|
| amharic-missing-drawing | 7 | [record](https://github.com/c933103/AN-Paint/blob/6f9c3d7deecafcd6a8fbffc5f1e15b584abea1b1/records/localization-review/2026-10-23/amharic-missing-drawing/r01/reviewed-candidates.json) |
| amharic-missing-editing | 6 | [record](https://github.com/c933103/AN-Paint/blob/97f2be09aebf45c5f020fda5805ffd45dc2b20a3/records/localization-review/2026-10-23/amharic-missing-editing/r01/reviewed-candidates.json) |
| amharic-text-style | 6 | [record](https://github.com/c933103/AN-Paint/blob/2b678f98e9ff8d627c4c8177dc39211132959737/records/localization-review/2026-10-24/amharic-text-style/r01/reviewed-candidates-and-reconciliation.json) |
| amharic-file-actions | 5 | [record](https://github.com/c933103/AN-Paint/blob/01e394ecd4b5b983109d0b924aab4223e073f1f0/records/localization-review/2026-10-24/amharic-file-actions/r01/reviewed-candidates-and-reconciliation.json) |
| amharic-tabs | 5 | [record](https://github.com/c933103/AN-Paint/blob/366fd3bc9de5ee801ba7b5a88ef6bcac8e78fe80/records/localization-review/2026-10-24/amharic-tabs/r01/reviewed-candidates-and-reconciliation.json) |
| amharic-edit-transforms | 7 | [record](https://github.com/c933103/AN-Paint/blob/581e032955f034e88958efaca9db6405c3579379/records/localization-review/2026-10-24/amharic-edit-transforms/r01/reviewed-candidates-and-hold.json) |
| amharic-view-controls | 6 | [record](https://github.com/c933103/AN-Paint/blob/fe0657e03789ca58d9cf786d1da6093296612fda/records/localization-review/2026-10-24/amharic-view-controls/r01/reviewed-candidates-and-hold.json) |
| amharic-brush-shape | 5 | [record](https://github.com/c933103/AN-Paint/blob/fe51d699eed5b068444c46168339b41b6cd1010a/records/localization-review/2026-10-24/amharic-brush-shape/r01/reviewed-candidates-and-holds.json) |
| amharic-size-controls | 5 | [record](https://github.com/c933103/AN-Paint/blob/0ccbec849aefa83b1fe4e4129fead677699fe9cf/records/localization-review/2026-10-24/amharic-size-controls/r01/reviewed-candidates-and-holds.json) |
| amharic-text-geometry | 8 | [record](https://github.com/c933103/AN-Paint/blob/c9d8c74a73784f4ed02a40cea50a4b711d78c62b/records/localization-review/2026-10-24/amharic-text-geometry/r01/reviewed-candidates-and-holds.json) |
| amharic-dimensions | 6 | [record](https://github.com/c933103/AN-Paint/blob/e0b380665a037a0cb8ab8e8c71785a96fe1b73a9/records/localization-review/2026-10-24/amharic-dimensions/r01/reviewed-candidates-and-holds.json) |
| amharic-normalization | 3 | [record](https://github.com/c933103/AN-Paint/blob/1aa7f8d363c29a3f7c63a6c857603e17a24c62fe/records/localization-review/2026-10-24/amharic-normalization/r01/reviewed-candidates-and-holds.json) |
| amharic-dialog-controls | 3 | [record](https://github.com/c933103/AN-Paint/blob/b808034de4d1f3081b02176f5b5a355ac1057d38/records/localization-review/2026-10-24/amharic-dialog-controls/r01/reviewed-candidates-and-holds.json) |
| amharic-save-labels | 5 | [record](https://github.com/c933103/AN-Paint/blob/f9e075d33f417ae67a5810fadbb2995e2ccf2623/records/localization-review/2026-10-24/amharic-save-labels/r01/reviewed-candidates-and-holds.json) |
| amharic-navigation | 4 | [record](https://github.com/c933103/AN-Paint/blob/0dbfee447be055614d11db76862a1b6352e46bd8/records/localization-review/2026-10-24/amharic-navigation/r01/reviewed-candidates-and-holds.json) |
| amharic-colour-actions | 5 | [record](https://github.com/c933103/AN-Paint/blob/44007be2530d28a9565dee696341b611a0bc025a/records/localization-review/2026-10-24/amharic-colour-actions/r01/reviewed-candidates-and-holds.json) |
| amharic-colour-roles | 2 | [record](https://github.com/c933103/AN-Paint/blob/f31a22cdcae565d422f1c9f701c1dca4a3bfdfa7/records/localization-review/2026-10-24/amharic-colour-roles/r01/reviewed-candidates-and-holds.json) |
| amharic-shape-names | 2 | [record](https://github.com/c933103/AN-Paint/blob/15b0fdc15cb46ef237bc9c26a3a4d32e64605db8/records/localization-review/2026-10-24/amharic-shape-names/r01/reviewed-candidates-and-holds.json) |

The counts sum to exactly 90 unique keys. Selection-tools follows that boundary and adds Eyedropper, not an amendment to the original 90. The remaining 17 additions are all original held keys subsequently released by named, per-key adjudications. The fourteen pre-selection holds plus three selection-tool holds are therefore accounted for exactly once.

## Value lineage

- Accepted/reconciled output fields take precedence over draft fields. For example, joined spelling and reviewed wording changes already made before the 90-key freeze are part of that frozen batch.
- Every original-90 row stores its exact frozen value. ui_pixels_6ec9c2 additionally stores the later singular preference, with the dated successor decision. Its original plural remains admissible; this consolidation does not amend it.
- Every formerly held row retains a link and value from the original hold and an immutable successor release. Eyedropper has an original ready decision without a prior hold.
- The 108 rows are keyed by canonical resource identity, not translated text; equal display values on distinct keys are not deduplicated. No inherited-nine key is admitted to the addition cohort.

## Checks completed

- 108 row identities, 108 unique keys, 90 original keys, 18 additional keys, 17 superseded holds, no duplicate keys.
- All 108 exist in translatable canonical English; each reviewed English value matches that source and each exact Amharic target key is absent.
- Format placeholders match between canonical English and current reviewed values. The original frozen pixel value has no placeholders and differs only as explicitly recorded.
- The separate nine-key review is disjoint from the 108. Its original five retain, two provisional, one unresolved and one optional classification is preserved.
- All counted readiness comes from explicit accepted records, not mere evidence availability, lexical matches or inferred implementation.

## Qualifications

- This consolidates existing decisions only; no new translation review or uplift in confidence.
- Ready means bounded source/textual review readiness, not authorization to implement or expand an existing batch.
- No native-reader certification, app build, tests, CI, runtime, rendering, accessibility, deployment or release was performed by this consolidation.
- A zero held count applies only to these 108 additions, not to inherited labels, full Help or other language-review scopes.
- Linked historical records preserve their original judgments and limitations; latest per-key decisions control only the identified successor.

## Remaining implementation checks

- Reconfirm the implementation baseline and explicit batch key/value version before editing.
- Preserve placeholders, Android string quoting, punctuation and required resource attributes.
- Check actual Ethiopic glyphs, truncation and wrapping at supported font scales; review full accessible labels and composed strings in their actual consumers.
- Run the authorized application and repository validation only in a separately authorized implementation task; none is claimed here.

## Compact-public representation

- Immutable record locators, confidence values and qualifications are stored once in shared dictionaries and referenced by per-row IDs. Every distinct qualification is retained verbatim with its row association.
- Common source checks apply to all 108 rows. Only nonempty placeholder-token lists are repeated per row; omitted lists mean both source and candidate have no format placeholders.
- Repeated supporting source/consumer URL arrays are omitted from the compact JSON. The exact immutable decision locators retain these underlying sources. No evidence decision, reviewed value, confidence judgment, qualification, supersession event or specific implementation check is dropped.
- The original full local artifact is preserved unchanged. Compact rows were expanded and checked against it field by field.
- The table resolves short evidence IDs through shared anchors rather than repeating long immutable URLs in every row.
