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
| **P3 — Reference and detailed help** | Secondary explanations, optional tutorials, reference and licence/credit navigation. | Editor and assembly help, cursor how-to guidance, lossless format reference and font/codec licence headings. |

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

### Explanations versus active instructions

Classify text by where it is used and the consequence of misunderstanding it,
not a character-count threshold or a `help`/`description` name. In particular:

- Optional how-to dialogs and supplementary reference belong in P3. The
  seven-paragraph assembly guide, `string/ui_add_up_to_20_images_with_android_s`,
  was already P3 in the original typed manifest. It remains P3, alongside the
  editor guides, even though it also summarizes saving and recovery behavior.
  Dedicated warnings and instructions at the point of action retain their
  higher priority; the guide is not their replacement.
- The optional cursor how-to alias `string/ui_cursor_help29` belongs with its
  P3 target `string/ui_cursor_help31`. The separate
  `string/ui_cursor_tap_hint37` stays P2: it also appears when cursor mode is
  enabled and explains how to start or stop drawing.
- `string/formats22_tiff_description` is P3 lossless format reference, like the
  BMP/DIB descriptions. Its compression choice preserves pixels. TIFF controls
  remain P2; lossy quality, GIF palette/frame loss, PDF rasterization and
  non-reopenable ASCII output explanations remain P0.
- An accessibility description is an operational label when it identifies an
  interactive surface. `string/ui_image_assembly_workspace_drag_placed_images_or_drop`
  therefore belongs in P2 with the assembly controls, even though it is a full
  sentence. It is the canvas content description, not the optional Help dialog.
- Crop previews, normalization dimensions/reflow notices and input guidance stay
  P2. Data-loss, unsaved-work, destructive-confirmation and recovery messages stay
  P0 regardless of length, including `string/ui_sampled_resize_memory_explanation`
  and `string/ui_a_separate_recovery_copy_has_been_kept_use`.

The 15 October explanatory-text audit changes only three assignments: cursor
how-to alias and TIFF reference P2 → P3; assembly accessibility description
P3 → P2. It preserves all 700 typed identities, canonical resource text,
language-level coverage and review statuses. P3 is still part of the eventual
translation/support scope. A priority change cannot close a wording defect or
revalidate an entry-review receipt; the independent corrections in
[PR #90](https://github.com/c933103/AN-Paint/pull/90) remain separate.

## Current source partition

Current partition (15 October 2026):

| Tier | Source entries |
| --- | ---: |
| P0 | 92 |
| P1 | 246 |
| P2 | 285 |
| P3 | 77 |
| **Total** | **700** (699 strings and 1 plural) |

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


Manifest schema 2 and missing-key reports use explicit `type/name` keys, for
example `string/ui_save`, `plurals/ui_crop_preview_images` and
`string-array/choices`. The type is the canonical XML resource tag. Different
types may share a name and are classified independently; a duplicate of the
same type and name is rejected. Consumers joining review receipts must retain
both type and name. Bare-name schema 1 manifests are rejected, not guessed.
