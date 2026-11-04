# Remaining P3 help: Old English and Old Norse

Base: `a6b04bf3f38a8845d546279899aca3a4ac7e00c7` on `review/nv-bottom-2038-20261103`.

## Scope and review

Six retained resources are added to each of `ang` and `non`: the complete ten-paragraph editor guide, paste hint, sampled-memory explanation including the selected opaque background, conditional Catrobat attribution notice, adjustable-width crisp-pencil hint, and toolbox/options accessibility description. The paste and pencil counterparts reuse identical-source wording already present in each catalogue. Existing resources and runtime routing are unchanged.

Independent text/context review accepted all twelve additions after separating PNG from the adjustable-quality JPEG/HEIC clause in both guides, correcting the Old English pencil pronoun, and making Old Norse image insertion explicit. A reviewed Old English infinitive refinement is also included. The complete current strings remain solely in canonical Android XML, not a permanent approval mirror.

The retained long guide is distinct from the active `ui_help23` call in `ClassicPaintActivity.showHelp`. Direct consumers of the equivalent paste and pencil hints, current resize explanation, category/panel state, and source/fallback generation were inspected. Absence of a direct static call does not establish that a retained resource is unused; nothing was deleted.

## Checks

- 78 existing host tests passed: translation catalogues, localized help, translation boundaries, current localization contracts, language translation note, string importance, ordinary-priority follow-through, and open-review recovery.
- All 171 offered options pass existing structural validation.
- Each locale preserves all 713 previous typed resources and adds exactly six strings, reaching 719 typed resources (718 strings and one plural).
- Per-locale priority presence: P0 94/94, P1 249/249, P2 305/305, P3 71/71 (previously 65/71). No missing priority keys remain in these two catalogues.
- Source attributes, XML/Android escaping, placeholder contracts, all quoted localized captions/routes, nine double-newline guide separators, trailing attribution double newline, four hexadecimal colour values and all three literal `100%` tokens are preserved. The long guide retains `formatted="false"`.
- The temporary source snapshot was reconstructed from repository content with hash/mode verification; unmaterialized files remain in the original Git base tree. Publication uses an exact-parent non-force lease and compares every remote non-tree path, type, mode and object hash, followed by changed-file readback.

## Limits

These are bounded independent AI language/context and host structural checks. Historical-language computing compounds are functional adaptations. Presence is not whole-catalogue linguistic acceptance or native-speaker certification. No Android build, AAPT, installed rendering, device, accessibility, runtime or CI acceptance is claimed. No release, merge, source removal or issue-tracker update is included.
