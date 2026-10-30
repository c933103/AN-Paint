# Shan batch C and brush reassessment

Same source binding as review.md: source-bound merged develop `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`, read-only materialized selected files. Batch A and B bytes remain frozen during their independent review.

## Concrete additional work

- `batch-c.tsv`: 30 missing-key candidates, **5 P0 + 25 P1**. These are actual source-bound translations, not source-finding placeholders. Two revise earlier unaccepted work (Pencil and Save explanation); the other 28 are new.
- `brush-reassessment.tsv`: exact proposed replacement `ယူႈယွမ်ႉသီ` for existing-unreviewed `ui_brush`. Positive lexical evidence supersedes the earlier lack-of-confidence hold; it does not prove the old term is wrong. No production mutation.
- `format-invariant-review.tsv`: seven missing P1 values with no English lexical text. Exact source-format preservation is appropriate and separately labelled, not inflated into seven newly authored linguistic translations.

## Independently inspected primary references

[CLDR49 Shan summary](https://unicode.org/cldr/charts/49/summary/shn.html), read 2026-10-30, gives paintbrush at rows7412–7413, pencil at7404–7405, percent at4703–4704, rectangle at8680–8685, palette at7084–7085. These are direct term mappings. The paintbrush entry's distinct noun and painting keywords establish the implement sense; the app BRUSH tool uses a selected tip and width. PENCIL produces a crisp line, rectangle selection selects a rectangle rather than paints it, and the palette panel selects available colours. The term mappings do not independently certify every constructed sentence.

[CLDR primary Shan annotation XML](https://raw.githubusercontent.com/unicode-org/cldr/main/common/annotations/shn.xml) was opened, but the web renderer's find returned unrelated ranges for those exact terms; the directly inspectable CLDR49 summary is the evidence actually relied upon, not a claimed successful extraction from the raw file.

[MediaWiki primary Shan catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/shn.json) corroborates collapse/expand UI vocabulary. Cache is intentionally paraphrased as temporary data storage for Undo rather than importing an unassessed loan. Existing accepted full-image memory warning already supplies the buffer paraphrase and working-memory vocabulary used here.

## Proposition review

- Undo-cache creation failure directs freeing device storage, not RAM; damaged and unexpected cache data remain distinct diagnoses and never claim source-image corruption.
- Export memory budget includes both image and encoding buffers; no financial meaning.
- Save explanation preserves reuse of filename, destination, format and settings. Compression is proposed as settings for making the file smaller; reviewer should ensure it does not suggest geometric resizing.
- Palette tap versus sustained press retain foreground/background roles. Scroll is distinct from tap/hold.
- Tool-category accessibility strings retain category then currently-selected tool and their distinct action to expand/collapse.
- Show/hide controls change visibility, not editing authorization or image content.
- Canvas zoom/magnification explicitly concern viewing, not output-image dimensions.

All new material still requires independent review. No implementation, native-human certification or aggregate completion credit is asserted. Work continues on feasible still-unaddressed residual keys; the existing 14 draft-object holds remain separately scoped.
