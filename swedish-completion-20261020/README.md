# Independent Swedish completion review

Baseline: released AN Paint `e50de18d`. Frozen author packet SHA-256:
`21e47cf1ec14f2e0efe85b5f04993c379a42a49adaabde5a157f27d200773f39`.

## Outcome

Every complete proposal was read: all 352 missing typed entries, including the
complete one/other plural, all 24 previously present unknown entries, and the
held Main label. All long Help/manual paragraphs were read. The final corrected
wording was reread; structural checks are additional evidence, not linguistic
acceptance criteria.

- 373 newly reviewed current-source accepts: 349 missing entries and 24 formerly
  unknown entries. Of these, 333 have direct production Kotlin call-site context;
  40 are source-semantic-only.
- 340 earlier bounded accepts preserved with exact full English/Swedish values
  and resource attributes. They were not newly linguistically rereviewed.
- 713 current-source bounded accepts in total, with four explicit holds below.
- Application snapshot: 714/717 typed entries present. Presence includes the
  unaccepted existing Main label; it is not the count of accepted translations.

This is bounded model-based wording review, not native-speaker certification,
whole-Swedish fluency/completeness, installed layout, TalkBack, runtime, build,
release or merge approval. Dormant lexical holds must not block unrelated
accepted reachable workflows.

## Explicit holds

1. `string/ui_main23`: existing `Huvud` remains present and unaccepted. No current
   production caller establishes what Main names.
2. `string/ui_foreground_background_colour_palette`: retain English fallback.
   The role of `%3$s` is unknown. The neutral-colon Swedish proposal is not
   accepted merely because it preserves placeholders.
3. `string/ui_add_up_to_20_images_with_android_s`: the complete corrected
   Swedish/English proposal is linguistically acceptable, including separate
   snapping/Exact position and qualified gap-closing behavior. It is not bound
   to the released English source. Rebind to the exact final PR #122 source
   after its gate resolves.
4. `string/ui_the_arrow_on_the_left_directly_below_the`: the complete corrected
   legacy-manual proposal is linguistically acceptable against its proposed
   English source, but that source adds Commons, exact-position behavior and
   qualified unplacing. Keep the source-binding hold. No direct production
   Kotlin caller was found, so this is not an active-workflow fallback blocker.

## Corrections made during review

The final source-target receipt records all accepted changes. Review fixed full
creator/artwork credit being narrowed to a creator name, made the greyscale row
explicit, replaced misleading assembly attachment nouns, corrected the
painted-brush phrasing, refined early curve commit, aligned the exact
`Lås proportionerna` control name, aligned corrected assembly Help with the
short PR #122 source paragraph, and clarified its credits sentence.

Eight previously present values were repaired: fixed-width font name, freehand
stroke smoothing, pixel-edge antialiasing, Use image, Copy credit, circular
brush/cursor shape, top crop edge and colour wheel. The other 16 present unknown
values receive bounded acceptance; the dormant Edit palette label is
source-semantic-only.

The quick-Help swap reference is correctly `Byt plats på färgerna`, because the
actual control uses `ui_swap23`. The review initially referenced a different,
dormant swap string; this was corrected before acceptance.

## Cross-language follow-through lead

The retained GIMP `Wheel` source is explicitly a mouse/input-device wheel.
AN Paint consumes `ui_wheel` in `AdvancedColourDialog.kt:118` as a colour wheel.
Swedish `Mushjul` was therefore corrected to `Färghjul`. This source-context
mismatch merits a later applicability check across other locales. It does not
prove other translations are wrong and must not be generalized into locale
acceptance or defect counts.

## Artifacts and checks

- `independent-review.json`: all 717 typed identities with complete source and
  target values, hashes, individual decisions, reasons and current contexts.
- `author-proposals-reviewed.json`: immutable local snapshot of the reviewed
  author packet.
- `source-correction-proposals-reviewed.json`: complete proposed English/Swedish
  pairs for the two held Help/manual entries.
- `verify_receipt.py`: checks all source bindings, non-held application targets,
  prior preservation, new attributes, format arguments, plural quantities,
  escaped newlines and resource aliases. It passed against the recorded
  application snapshot.

No application files were edited and no GitHub changes were published by this
independent reviewer. Local files are temporary evidence for the authorized
project record, not a substitute for its designated durable repository.
