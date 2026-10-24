# Independent review: Amharic colour roles

## Outcome

**2 RETAIN, 0 REVISE, 1 HOLD.** Retain the two proposed colour-role noun labels unchanged for the reviewed-candidate ledger. Keep the composed swap command on HOLD. This is an independent source-and-language assessment, not native-reader approval, implementation or runtime certification. Prior 86 ready / 12 held decisions are separate and unchanged by this packet.

Input seal: `bedd1144d33e9e54b4edb3e915877ec515f3dd355be7339c29ed203a26667842` (SHA-256 of `input/MANIFEST.json`). All 32 input payload hashes and all 12 source Git blobs match. The copied input is unchanged. Source commit: `66be61df27c5359bffc32d56db21f3949899f873`; tree: `870c5a584120d92710be516af0dc3b3847b183d9`.

## 1. ui_foreground_colour: RETAIN

English: Foreground colour

Retained text: **የፊት ለፊት ቀለም**

Confidence: medium-high for lexical equivalence and orthographic form; medium for complete AN-Paint idiomatic fit. No human native-speaker judgment is claimed.

The phrase remains a noun label for the current foreground colour. It does not add an instruction to bring a layer forward, select a visually nearer object, or recolour existing pixels. It is suitable both as a colour-editor title and as one component of the status description. A rewrite as only “brush colour” would wrongly narrow its uses, which include fill, shapes and text.

The input's non-fuzzy LibreOffice pattern-colour record directly supplies the whole role phrase, `የ ፊት ለ ፊት ቀለም:`. Joining the genitive prefix to its following word, joining `ለ` to `ፊት`, and dropping the English label's absent terminal colon are disclosed orthographic/punctuation adaptations, not an exact-byte quotation. The input GIMP RGB status supports `ፊት ለፊት` as an actual colour role, not layer stacking.

Additional independently retrieved GTK evidence reinforces this judgment: non-fuzzy “Foreground color name” is `የፊት ለፊት ቀለም ስም` (lines 1103–1105). That attests the proposal's exact noun-phrase sequence within a longer colour-property label. GTK also has “Foreground color” as `የፊት ለፊቱ ቀለም` (1111–1113), with a definiteness suffix. This is useful corroboration, not an exact standalone match and not a reason to silently add that suffix. These related GNOME-family sources should not be treated as multiple independent native-reader votes.

Sources: input lexical IDs `lo_pattern_foreground`, `gimp_foreground_rgb`; [GTK immutable source](https://github.com/GNOME/gtk/blob/13b9cf841947711e8b28eb464aa6e32434309d80/po-properties/am.po#L1103-L1113).

## 2. ui_background_colour: RETAIN

English: Background colour

Retained text: **የመደብ ቀለም**

Confidence: medium-high for lexical equivalence; medium for complete AN-Paint idiomatic fit. No human native-speaker judgment is claimed.

The phrase denotes the background colour property, rather than a background image layer, application theme or OS wallpaper. It preserves the source noun-label register in all three uses: editor title, status-description component, and the custom-swatch menu entry assigning that colour to the background property. Do not add a “set” imperative in only this language to make the shared menu entry more explicit.

Two non-fuzzy LibreOffice colour-control records supply `የ መደብ ቀለም` (with and without a colon). Joining the genitive prefix and omitting the colon where English has none are defensible disclosed adaptations. The non-fuzzy GIMP background RGB record supports the same noun. Newly retrieved GTK “Background color” is `የመደቡ ቀለም` (1095–1097), a definite variant, and “Background color name” has the same attached-prefix pattern. This corroborates the colour-property interpretation without making the definite variant mandatory.

The inherited AN-Paint `ui_edit_background` translation is not an acceptance precedent. It is not necessary to support this decision and has not been re-approved here.

Sources: input lexical IDs `lo_pattern_background`, `lo_background_colour`, `gimp_background_rgb`; [GTK immutable source](https://github.com/GNOME/gtk/blob/13b9cf841947711e8b28eb464aa6e32434309d80/po-properties/am.po#L1087-L1097).

## 3. ui_swap23: HOLD

English: Swap colors

Held candidate, unchanged: **ቀለሞችን ያለዋውጡ**

Confidence: high about the required operation; medium about the components and role-exchange analogy; insufficient to accept the complete command's idiomatic fit/register.

The source callback exchanges foreground and background values through a temporary variable. It does not invert RGB channels, reverse every pixel, reset black/white, exchange image layers, or rearrange palette slots. The exact AOSP verb is paired with swapping left and right mouse-button roles, a genuinely useful two-role exchange analogue. It is materially better evidence than character substitution or the excluded fuzzy GIMP “Exchange foreground and background colors” record.

The composition is transparent: LibreOffice's `ቀለሞች` plus the object ending `ን`, followed by the exact AOSP command verb. The alternate plural `ቀለማት` in AOSP establishes another source usage, not an error in `ቀለሞች`. However, neither the complete phrase nor its reader interpretation has been independently validated here. Do not present AOSP as full-phrase attestation or treat upstream presence as native approval. The command uses the AOSP polite/plural imperative pattern; the inherited singular `ለውጥ` elsewhere is not a sound basis for enforcing a different global register.

This HOLD is not a finding that the candidate is grammatically wrong. Lack of an exact corpus match is not, by itself, grounds to reject a legitimate composition. The remaining issue is whether the whole command naturally communicates the reciprocal exchange of the two current colour values, rather than merely changing or cycling colours, in the intended UI register. This review cannot confidently settle that question. No speculative replacement is promoted. A proficient Amharic review of this specific command in the two-swatch context is the appropriate next evidence.

Sources: input lexical IDs `aosp_swap_buttons`, `lo_colours`, `aosp_colours`. The excluded fuzzy GIMP exchange record and LibreOffice similarity-search character-substitution record are not affirmative support for this command.

## Exact source use and semantic checks

The bounded scan reproduces exactly six references across the supplied complete caller files:

- `AdvancedColourDialog.kt:304`: foreground and background labels are conditional editor titles. Validation/commit and preview restoration are visible at 305–325.
- `ColourStatusButton.kt:36`: the two labels are joined by an external slash. Separate hex-specific edit templates and FG/BG captions are not these keys.
- `ClassicPaintActivity.kt:1007–1008`: the background menu item calls `setColour` with `background=true` for the selected custom swatch.
- `ClassicPaintActivity.kt:422`: the live swap key is `ui_swap23`, and its callback exchanges the values. `updateColours` at 727–730 refreshes the status, invalidates the canvas and schedules autosave.

`PaintDocument.kt:44–47` stores two opaque colour properties. The property setters alone do not paint pixels. Foreground is used by ordinary painting, flood fill, shape outlines/most fills and text; background is used by erasing, background-filled shapes, clearing/new canvas, selection deletion and opaque text backgrounds. Canvas invalidation can update pending previews, so “nothing visible changes” would be too strong.

The longer `ui_swap_foreground_background` and `ui_edit_foreground` have no direct references in the supplied bounded Kotlin corpus and remain excluded. This is not a fresh exhaustive repository search or a global dead-code finding. No English source defect was established and no English rewrite is proposed.

## Evidence, scope and limits

- Input verification: five lexical snapshots, ten positive records, 27 excluded/history records, 39 exact blocks, all matching source slices and recorded hashes. Positive PO evidence is not fuzzy or obsolete.
- New evidence: one complete immutable GTK PO snapshot, 103,834 bytes, Git blob `a056ddf20d6af1ad71264d9cae4afda264914671`, SHA-256 `a11defff11e503da50835f072d20f79794e33ae4d4bbe5860cae661ad5db7fa6`, with four extracted non-fuzzy records. Its historical translation date is not represented as recent native review.
- The GTK web fetch returned a cache miss; the connected GitHub read subsequently returned the complete pinned file. Its locally recomputed Git blob matches the tool. The search excerpt alone was not used as final evidence.
- Other public search hits were exploratory and are not affirmative evidence. No exhaustive Amharic corpus claim is made, and no new complete swap-phrase attestation was established.
- Production remains 12 present / 705 missing of 717 translatable containers. All three target keys are missing in the source Amharic resource file.
- No Work task, production changes, build, CI, release or remote publication. The sealed input, earlier 86 ready / 12 held decisions, inherited strings and unrelated holds remain untouched.
- No runtime rendering, TalkBack pronunciation, whole combined-description acceptance, whole-language acceptance, or native-reader approval. Android quotes are resource syntax; no ellipsis, unit or placeholder has been added to these three labels.

Machine-readable decisions are in `decisions.json`; reproducible identity/count results are in `verification.json`; original input is in `input/`; the new snapshot and exact records are in `additional-evidence/`.
