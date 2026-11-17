# Round 4 independent Chamorro review

## Scope and limits
Screened 52 retained candidate strings selected by drawing/gesture/brush/cursor/crop/palette/colour/font key names against current canonical English. Exact key inventory: `round4-reviewed-keys.txt` (same draft directory). This is not a review of all 232 retained candidates. Deep lexical checks concentrated on `hit`, `brin`, `atyik`, `patcha`, `go'ti`, `rega`, and `tulaika` using the primary CNMI dictionary. No canonical or candidate JSON edits. No whole-string fluency approval. CNMI evidence does not by itself settle Guam orthographic preferences.

## New concrete finding

**Reject current `ui_drag_across_the_ellipse_s_bounding_box`.** Draft `Go'ti yan muebi gi kahon ni ha hit i elipse.` uses `hit` as though it were an enclosing/bounding verb. Primary H entry identifies `hit` as first-person inclusive pronoun (we/us), not a verb meaning bound/enclose. This is not an acceptable dictionary-grounded rendering of the ellipse's bounding box. Source R entry supplies `ridondeha` for surround/encompass, but a mechanical substitution would not establish a geometrical bounding rectangle. Correction requirement: explicitly describe the rectangle surrounding the ellipse and the drag across it; keep fallback until that complete wording is independently checked. Do not auto-replace `hit` with an unreviewed inflected verb.

## Newly sharpened semantic holds

- `ui_add_to_custom_colours`, `ui_custom_colour`, `ui_custom_colours_hold_a_swatch_to_replace_it`, `colour20_custom_selected_slot`: `ni un atyik` describes what the user chose. Primary `atyik` is choose/select/prefer, not customize. The palette has an important selected-vs-custom distinction. Proposed correction direction: explicitly describe user-defined/saved custom slots rather than merely selected colours. No verified ready-to-integrate replacement found.
- `ui_drag_to_erase_with_the_background_colour`: `kulot i brin` is canvas colour, narrower than the app's designated background colour used by eraser/fill. Primary `brin` denotes canvas material. Canonical background control already spells out canvas/eraser/interior-shape use, so using that established control wording is a guarded consistency correction; do not assume every canvas colour equals BG state.
- `ui_hold_a_thumbnail_and_drag_it_here_or`: generic `lugåt para un cho'gui` obscures the named workspace target. Gestures and alternative sequence are retained, but the user must know where the second tap lands. Prefer established workspace label from the actual screen, with separate language check.
- `ui_cursor_help31`: raw `Muebi` collapses drag and pan; this is a technical-instruction distinction to verify against actual gesture handling. Canonical `ui_drawing23=Dibuhu` explains one navigation label, but does not alone certify both `Draw → Drawing` destinations as `Dibuhu → Dibuhu`.
- Crop-selection descriptions (`ui_batch_crop`, `ui_batch_crop_images`, `ui_image_shown_in_crop_preview`) can read as selecting a part to use, rather than trimming with a visible crop preview. Previously held, now confirmed still needing task-specific terminology.
- Crisp-line/pencil wording retains clarity of edge rather than explicitly hard-edged/non-antialiased rendering. Do not treat this subtle technical equivalence as established.

## Correction to my earlier review

My earlier concern that `ui_tap_the_image_to_sample_the_foreground_colour` lost foreground specificity was too strong when considered in isolation. The draft uses `kulot para un fa'tinas pinenta`; canonical foreground/background controls consistently use this phrase for foreground. Thus this is a context-supported foreground reference, not a demonstrated semantic omission. Sampling verb/context still has not received full linguistic certification. This correction does not approve the whole sentence.

Likewise `Tulaika` in the stored-slot Replace instruction is not inherently a mistranslation: primary T entry includes exchange/replace/substitute. Verify that the actual button uses this label; do not reject simply because the same root also describes adjustment/change.

## Source-backed lexical observations, not whole-string approval

- `patcha`: touch/contact supports the tap metaphor, but does not by itself express brief tap duration.
- `go'ti`: hold/grasp supports holding metaphor, but does not independently distinguish long-press from ordinary drag.
- `rega`: sprinkle/scatter supports the spray-paint analogy; no primary software-specific usage was established.
- `brin`: canvas noun is attested. Physical-material sense does not automatically validate every UI compound.
- `atyik`: selection verb is attested, making the custom-versus-selected issue concrete.
- `tulaika`: replacement meaning is attested.

Sources:
- https://natibunmarianas.org/h/ (`hit`; useful button-press example under `honñu'`, but not an approved wholesale gesture replacement)
- https://natibunmarianas.org/b/ (`brin`)
- https://natibunmarianas.org/a-2/ (`atyik`)
- https://natibunmarianas.org/p/ (`patcha`)
- https://natibunmarianas.org/g/ (`go'ti`)
- https://natibunmarianas.org/r/ (`rega`, `ridondeha`)
- https://natibunmarianas.org/t/ (`tulaika`)

## Semantic structure retained in screened strings

The opposite-corner star instruction preserves five points; heart and basic outline/fill instructions retain their alternatives. Line-width instruction retains current English 1..100, not its obsolete one-pixel key name. Thumbnail placement descriptions generally retain hold/drag versus tap alternatives. Slot actions retain their numeric placeholders and save/replace distinction. Cursor marker instruction retains size independence from painted brush size. These are limited technical observations, not evidence of correct inflection, naturalness, or full instruction accuracy.

Previous holds on decode/extract wording, font/legal compounds, early curve commit, and specialist technical terminology remain. The other screened entries are not automatically accepted because no new concrete defect was isolated.

## Addendum: 17 new candidates and three correction hypotheses

After the initial report, screened all 17 `round4_drafts` entries plus the three invert/handle correction hypotheses. Scope now 69 distinct retained candidate keys plus three correction hypotheses (72 string versions screened, not 232). These are semantic screens with targeted dictionary checks, not full linguistic reviews.

- Light-coloured `chångnga`: exact finder entry verified. This corrects the earlier afraid/light lexical error in ASCII inversion. Whole inversion sentence remains unapproved.
- Handle `tokpung`: exact finder entry verified as physical handle. GUI-control metaphor remains unverified; removing `guinifi` is a real lexical improvement but not enough to certify the new instructions.
- Rotation `bira`: previously verified turning/rotation verb. It is substantially better grounded than the rejected prior term.
- `måhlus`: exact finder smooth entry verified, but freehand smoothing and pixel anti-aliasing are different algorithms. Shared ordinary adjective is not software terminology certification.
- Polygon instruction `hånggai` for close: no matching primary H entry found. Hold this pivotal verb and its open/closed derivatives. The tap-twice, last-vertex, alternative Finish, and switch-off structure is present; this does not rescue an unsupported close operation.
- Enclosed-area `masåhgi`: no matching primary S evidence found. Finder explicitly has `enclose = aridondeha`, but deriving a passive form and technical compound needs review. Do not silently replace.
- Opposite-corner `kinalañu`: no matching primary K evidence found. Finder `opposite = åtlibis (1)` is a research lead, not a certified spatial-corner substitution.
- Sideways `gi kilu'`: primary K entries near this spelling give kilogram/plant/last/cross/rotation forms, not this sideways expression. Hold both sideways and mixed-orientation entries. Absence of a match is not proof the expression cannot exist.
- Radius instruction preserves half-of-shorter-side concept, but finder distinguishes general short `kádada'` from length-short `ngisut`; verify intended geometric sense rather than assume the broad adjective is precise enough.
- Drop instruction preserves right/top versus below/left alignment alternatives; `mana'li'i'` appears to express made-visible rather than highlighted, so selection/highlight cue remains a technical hold.
- Polygon `vertex=eskina` is corner vocabulary and may be an explanatory choice; not established as general mathematical vertex terminology.
- Character-by-character uses `lettra` (letter), which may narrow the source's character concept, especially alongside CJK. Hold pending a deliberate character term.
- Four Commons attribution errors consistently use `rekognision`; recognition is not automatically attribution with creator/licence provenance. All remain held. `field` as generic part and `retain` as save likewise need context validation.
- Tagged-colour message keeps BMP/GIF, cannot-yet, sRGB PNG, pre-import conversion and colour-managed-editor requirement in approximate form. `colour profile` is openly unresolved English and the remaining colour-management phrase is not independently certified. Do not count this as completed localization.

Additional source evidence: local `/tmp/ch-finder.txt`, from the primary English–Chamorro Finders List; https://natibunmarianas.org/k/ ; https://natibunmarianas.org/h/ ; https://natibunmarianas.org/s/ .
