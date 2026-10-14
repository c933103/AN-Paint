# Translation importance tiers

AN Paint assigns each **translatable English resource identity** to exactly one
importance tier in [string-importance.json](string-importance.json). This is a
work-order aid for translators and reviewers, **not** a separate Android resource
catalogue. English and localized sources stay under
Paintroid/src/main/res/values*/strings.xml; Crowdin continues using those files.

## Priority definitions

| Tier | Purpose | Examples |
| --- | --- | --- |
| **P0 — Data safety and recovery** | Correctly understand destructive actions, unsaved work, saving/export distinctions, recovery and warnings about discarded content. Translate and validate first. | Save, Discard changes, Save destination failed, Autosave failed, recovery-copy instructions, animated-file flattening warnings. |
| **P1 — Essential editing** | Navigate the app and accomplish everyday drawing and editing tasks. | File/Edit/View menus, opening images, Pencil, Undo/Redo, selection, colour, canvas, zoom, language picker. |
| **P2 — Extended functions** | Specialized tools, formats and workflows, including their errors and controls. | Image assembly, TIFF/PDF/ICO options, galleries, advanced colour tools and compression settings. |
| **P3 — Reference and detailed help** | Secondary explanations, long tutorials, reference and licence/credit navigation. | Long editor guide, font/codec licence headings and tutorial hints. |

This ranks **UI localization effort**, not legal obligations. P3 is not
unnecessary: licence, copyright and creator-attribution obligations still apply
regardless of tier; existing legal bodies remain intact. Importance reflects
the consequence of misunderstanding, not length or translation difficulty.
Critical accessibility messages must not be downgraded.

P0 can include a specialist feature's warning when misunderstanding it could
silently change or destroy data. For example, importing an animation discards
other frames, so that warning is P0 even though the rest of the feature is P2.
A plural resource counts as **one key** across all quantity forms. Fixed
nontranslatable identifiers, file names and language-option arrays are excluded.

## Current source partition

Initial snapshot (14 October 2026):

| Tier | Source entries |
| --- | ---: |
| P0 | 83 |
| P1 | 249 |
| P2 | 288 |
| P3 | 78 |
| **Total** | **698** (697 strings and 1 plural) |

These are English source-entry counts, **not** completed translations or
accepted reviews. The validator recomputes totals and fails when an English
key is added, removed or made translatable without an explicit decision.
New keys have no default tier.

## Validation and language-level work

From the repository root:

~~~sh
python3 tools/string_importance.py
python3 tools/string_importance.py --locale ceb
python3 tools/string_importance.py --locale ceb --missing-keys
python3 tools/string_importance.py --all-locales --json
python3 -m unittest discover -s tools -p 'test_string_importance.py'
~~~

The locale report measures **direct presence in the exact canonical locale
file**, not Android's resolved fallback chain. English-identical values may be
valid proper names, legitimate translations or missing linguistic work.
Presence and string equality do not certify translation.

Priority and progress must remain separate dimensions:

- Priority: P0, P1, P2 or P3 for each translatable English key.
- Entry review: missing, present but unreviewed/unknown, evidence-backed bounded
  review, or needs re-review, tracked independently.

Structural tests cannot certify linguistic correctness. All withdrawn
historical localization conclusions remain withdrawn. The
[translation progress tracker](https://github.com/c933103/AN-Paint/pull/56)
can join the manifest to its exact-key review receipts and produce P0-first
queues without reviving any rejected review claims.

## Maintenance

1. On changing a source resource, deliberately assign its key to exactly one
   tier (remove obsolete keys); keep each tier list alphabetically sorted.
2. Reconsider importance when functionality changes, even if a key is unchanged.
3. Run the new validator, existing translation catalogue checks and host tests.
4. Translate and review in actual operation context, including placeholders,
   plurals, accessibility labels, RTL, and long-text layouts.
5. Never overwrite localized canonical XML or call a priority assignment an
   accepted linguistic review.

The manifest covers translatable string, plurals and string-array identities
in the default values XML directory. It never changes runtime UI or language
fallback behavior.
