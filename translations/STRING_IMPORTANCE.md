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
| **P1 — Essential editing** | Navigate the app and use its active main-editor menus, tool choices and inline controls, including accessible names. | Top-level tabs, second-level File/Edit/View commands, every drawing-tool label, colour-panel actions, cursor controls, inline tool options, opening images, Undo/Redo and language picker. |
| **P2 — Extended functions** | Deeper specialized workflow contents, formats and controls, including their errors; not their main-editor entry points. | Assembly workspace/dialog contents, TIFF/PDF/ICO options, galleries, advanced colour-dialog fields and compression settings. |
| **P3 — Reference and detailed help** | Secondary explanations, optional tutorial bodies, reference and deeper licence/credit navigation; not main-editor launchers. | Editor and assembly help bodies, cursor how-to guidance, lossless format reference and font/codec licence headings. |

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

### Main-editor menu and control floor

All active top-level tabs and second-level command/tool labels are **at least
P1**, in every offered language. The same floor covers directly rendered inline
tool/cursor options, colour/palette controls and their accessible names, including
dynamic selected choices, start/stop labels and expand/collapse states. Existing
P0 safety commands remain P0. A feature being advanced or optional does not make
its visible entry point lower priority: Image assembly, Advanced colour,
How to use and About/credits are P1 launchers.

This does not promote all text reachable through those launchers. Long help
bodies, deeper dialog fields, assembly-workspace contents and licence documents
retain their separately assigned priorities. Nor does an identifier containing
`menu` prove an active menu: `ui_menu_help` is an unused title fallback and
`ui_menu_image` is a filename fallback in the current editor.

The source-binding host regression checks the current menu producers, tool and
action enums, inline options and adjacent accessibility bindings. It excludes
explicit help/toast/callback bodies rather than selecting by text length or
locale. It is a bounded static guard, not a Kotlin parser, installed UI test or
proof that every future binding will be discovered. Revisit its boundaries when
adding or moving controls. Canonical XML, held wording and review receipts are
unchanged by a priority decision; newly exposed P1 gaps are not new translations.

Navigation captions are also checked from the shared `EditorNavigation.kt`
command/tab/group definitions that build the UI. Tool and header definitions
join that audit; new navigation captions must remain P0/P1. The navigation
coverage report separately identifies missing entries, aliases falling back to
English and English matches needing review. Presence alone is not acceptance.

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
- Accessibility descriptions that identify interactive surfaces or controls are
  operational labels. The main drawing canvas and Fit action belong in P1;
  assembly canvas, crop-image selector and thumbnail tray belong in P2. Their
  prose-like wording does not make them optional Help.
- `string/ui_paste_hint34` is a failed-Paste prerequisite/recovery message (P1).
  `string/ui_px_drag_an_image_to_move_hold_a` combines current assembly dimensions
  with teaching text (P2). Mixed identities take the operational role's priority.
- Inline teaching can still be P3 when separate controls/feedback carry the
  operation: selection handles, Navigate gestures, canvas-bounds gestures,
  vertical-text behavior and assembly empty-state reminders are examples.
- Crop previews, normalization dimensions/reflow notices and input guidance stay
  P2. Data-loss, unsaved-work, destructive-confirmation and recovery messages stay
  P0 regardless of length, including `string/ui_sampled_resize_memory_explanation`
  and `string/ui_a_separate_recovery_copy_has_been_kept_use`.
- Unreferenced legacy descriptions retain their existing priority conservatively;
  their wording alone does not establish a current UI role. The live language
  picker note is a mixed heading/explanation (P1), and Commons credit-record
  guidance is operational P2 despite its explanatory wording.

The 15 October catalogue-wide source-role audit read all 700 identities. Broad
name/sentence/word-count screening selected 275; manual/reference-role checks
added 88, for 363 detailed dispositions. The other 337 ordinary entries were
included in the full read. Of the detailed set, 285 originally higher-tier
entries stay at their assigned tier, two move P2 → P3, 69 original P3 entries
stay P3, and seven move higher (three P1, four P2). The grouped exact-key sets,
source call sites, screening reproduction and legacy-use limits are recorded in
[PR #91's audit](https://github.com/c933103/AN-Paint/pull/91#issuecomment-6185966530).

These nine changes preserve all 700 typed identities, canonical resource text,
language-level coverage and review statuses. P3 remains part of the eventual
translation/support scope. A priority change cannot close a wording defect or
revalidate an entry-review receipt; the independent corrections in
[PR #90](https://github.com/c933103/AN-Paint/pull/90) remain separate.

## Earlier source partitions

Current partition (17 October 2026), including the six exact-position controls
added by PR #67. Before the source-role audit the counts were
P0/P1/P2/P3 = 92/246/286/76; the audit produced 92/249/288/71.
The six new labels, active coordinate instructions and validation messages are
P2 because they operate the specialized assembly dialog. The inline
`ui_assembly_position_help` is required position guidance, not the optional
general assembly how-to guide. No existing identity changes tier.

The prior implemented partition contains 708 identities, including the P2
external-link and native-image-component diagnostics. This slice externalizes
nine previously literal Commons/import reasons as P2, matching the existing
Commons HTTP, response-limit and API-query failure messages. These are active
specialist-operation failures, not optional long-form reference. No existing
key changes tier, including the detailed explanations and guides assigned P3.

The source denominator therefore increases from 708 to 717 and P2 from 296 to
305. P0 + P1 remains exactly 341; a prior 341-key language review does not cover
any of these nine new P2 keys. Applicability and translation/review progress for
the new keys remain separate; see [the bounded implementation plan](../verification/commons-import-failures.md).

## Current source partition

The 9 November 2026 main-editor scope correction moves 34 existing identities
to P1: 32 from P2 and two help/about launchers from P3. It includes 20 main
menu/tool/adjacent-control labels and 14 directly rendered inline-option labels.
The preceding 719-key partition was 94/249/305/71. No key is added or removed,
no P0 key moves, and no localized value or hold changes.

| Tier | Source entries |
| --- | ---: |
| P0 | 94 |
| P1 | 283 |
| P2 | 273 |
| P3 | 69 |
| **Total** | **719** (718 strings and 1 plural) |

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
   Active main-editor menu and inline control bindings have a P1 floor; keep
   existing P0 safety roles higher. Apply the same source-key policy to all locales.
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
