# AN Paint ang/non — complete P0/P1 candidate inventory, unaccepted

**Deliverable:** 341 source-bound rows, each with an Old English candidate and an Old Norse candidate: **92 P0 + 249 P1 per locale (682 language-specific drafts)**. Every row includes exact English, target, intended backtranslation, rationale and draft confidence (column or batch-level declaration).

**This is not an accepted translation or source patch.** No native-speaker competence is claimed. Long warnings are low-confidence proposals. Independent review has already found substantive mistakes; its corrections are explicit in the secondcheck ledger. Merely filling the key inventory grants no implementation/release credit.

## Read order and current wording

1. `00-conventions.md` — proposed historical varieties, normalization, technical coinages, evidence limits.
2. `90-author-secondcheck.md` — **required superseding candidates**, exact full-string revisions and cited reasons. This overrides specified target cells or evidence status in version 1 batches; do not import version 1 blindly.
3. Batches 1–6 below — the complete original candidate inventory, retained visibly for review history.

| Batch | File | Rows | Scope |
|---|---|---:|---|
| 1 | `01-common-safety-controls.md` | 39 | 24 P0 + 15 P1: save, export, recovery controls; cancel/discard; menus |
| 2 | `02-p0-recovery-storage.md` | 38 | P0 storage, draft and error states |
| 3 | `03-p0-safety-explanations.md` | 30 | P0 explanations, memory, export, animation, rasterization and colour |
| 4 | `04-p1-editing-labels.md` | 141 | P1 drawing, colour, shapes, typography, resize and language labels |
| 5 | `05-p1-controls-instructions.md` | 64 | P1 gestures, accessibility, numeric constraints and canvas instructions |
| 6 | `06-p1-import-memory-failures.md` | 29 | P1 import/provider/memory/SVG/colour failure messages |

## Source identity

Supplied merged baseline: commit `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`. The local `.git` is an unborn index, so no local HEAD verification is claimed. These read-only Git blob digests bind the **actual input bytes read**:

| File relative to supplied checkout | Git blob SHA-1 |
|---|---|
| `Paintroid/src/main/res/values/strings.xml` | `b50c607aac54c6148e5ac4e44325cb6db3be3612` |
| `translations/string-importance.json` | `e76a3a440a8b169d31f5ab5d163a2695b0db93b1` |
| `Paintroid/src/main/res/values-b+ang/strings.xml` | `d98e760917dc9065143a682561b0fc603ae32abb` |
| `Paintroid/src/main/res/values-b+non/strings.xml` | `93034d518728f99ecf8d87705739e9cb440f51cc` |

The two target files were empty catalogues explicitly marked unstarted. This packet contains research records only; no application resources were edited.

## What was and was not checked

- Read-only name-set inventory against `string-importance.json`: **341 unique base rows, no missing P0/P1 keys, no duplicate base rows**. Revision-ledger repeats are intentional overrides, not additional scope.
- Candidate author manually retained numbered placeholders, `%` formatting specifications, `\n` escapes, JPEG/JPEG XL/PNG and other literal format identifiers. **No automated placeholder/parser/lint validation or Android tests were run.** Request a separate artifact validation before any future implementation.
- Primary dictionary/grammar checks were used for lexical/case ambiguities. Whole sentences are original research-assisted drafts, not source quotations or published UI matches. The exact review scope is the logged findings, not a full independent 682-string linguistic audit.
- `eptirrit` was exposed as a **modern/reconstructed compound**, not securely medieval, after reviewer correction. Its use as a technical convention is still proposed, not accepted. `Ellipsis`, pixel/metadata/cache/app/file terms and many compounds likewise need explicit terminology approval.
- No source-bound linguistic acceptance, runtime coverage, native-usage claim, or completed translation gate is asserted.

## Highest-priority remaining review decisions

1. Exact v2 long safety sentences in the secondcheck ledger; especially preservation of paused autosave, separate recovery ZIP, active-image save and output-only memory-floor distinctions.
2. Whether to accept or replace proposed historical-language technical conventions (copy, draft, pixel, file, format, source, metadata, encoding, buffers, colour profiles, clipboard).
3. Case/inflection and historical idiom across all 682 candidates, including dynamic placeholder agreement and abbreviations. Fixed-English placeholders can still insert unlocalized text.
4. Full source-English/placeholder integrity review and UI-length/accessibility checks **only in a separately authorized implementation/testing stage**.

## Current revision navigation

`91-latest-override-index.md` identifies the latest exact ledger revision for **24 ang + 16 non text overrides**, plus the three explicitly restated recovery-copy evidence-status cells and whole-convention caveats. It prevents older v2 wording from being mistaken for the latest v3 candidate. All listed overrides remain low-confidence and unaccepted.
