# Danish, Icelandic and Norwegian priority review — 29 October 2026

Reviewed source: `0070c5816ad31911d227fab50ea193e2a39b13ab`.
Prior-author candidates: `7fc5492da0e78474bb828b5276e0b703989c7b67`,
`verification/da-is-no-priority-20261027/candidates`.

This completes the **inventory review**, not whole-language acceptance, for
Danish `da`, Icelandic `is` and the actual offered Norwegian `no` option.
`nn` remains separately offered and outside this delivery; `nb` is not offered.
Each inventory has **92 P0 + 249 P1 = 341 typed identities**.
The complete English/current/candidate pairs and attributes all matched the
current base before editing; no later translation was overwritten.

| Locale | Priority edits | Retained priority | Absent holds | Additional changed companions |
|---|---:|---:|---:|---:|
| da | 164 | 171 | 6 | 4 |
| is | 246 | 89 | 6 | 5 |
| no | 174 | 161 | 6 | 5 |

**598 resource edits: 570 additions and 28 replacements.** The additions close
exact catalogue gaps; they do not imply complete locale coverage. Replacements
include inherited English labels, Icelandic filename spelling, contextual unit
case, Norwegian Redo semantics, and atomic matching menu references. Fuller Fit,
Keep editing and dithering terminology are explicitly contextual refinements,
not claims of severe bugs. Optional standalone pixel-label lowercasing in da/no
was rejected. Icelandic standalone dative candidates were rejected; the existing
standalone names remain, while dative suffixes serve the separate composed
accessibility descriptions.

The two da/no inventories each carry **76 exact previously accepted priority
pairs**, without new review credit. Their two other prior reviewed messages are
updated only to match newly localized command/field labels. Icelandic carries
**83 previously independently reviewed priority candidates plus two companions**;
those earlier candidates were not previously in production. The independent
current model review covers the remaining prior-author candidates and inherited
values. Its uncertainty is retained: medium AI linguistic judgment, not
native-human certification. The parent's separate exact Icelandic unit check is
preserved alongside this report. Two unchanged Top edge companions (da/is) are
also reviewed for the new complete crop descriptions.

All locales retain these six absent holds: `formats22_derived_exported`,
`ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, `ui_save_as_png`,
`ui_foreground_background_colour_palette`. Each has **24 additional dormant
wording-only priority values**, with no runtime-context acceptance. Fit rendering,
TalkBack, physical devices and native-human linguistic acceptance remain untested.
The post-change exact catalogues contain da 363, is 355 and no 360 typed resources;
this is presence, not broader P2 acceptance. No global 171-language total is
recomputed and no withdrawn review conclusion is revived.

## Tests and publication

New host tests cover full source/target/attribute/placeholder bindings, the exact
priority partitions, old/missing/truncated/duplicate/markup/attribute negative
controls, finite previous-value guards, every composed unit output, command
references, GIF frame count and shared warning/SVG preconditions. New Robolectric
tests exercise compiled strings, DimensionControls changes, crop selection and
Cancel, category accessibility, actual animated import cancellation and memory
admission. Historical fixtures stay unchanged; finite forward projections retain
all prior assertions and unrelated values. The shared colour-profile and memory
warning contracts explicitly include the new scope without rewriting history.

Initial focused Nordic host suite: 7 tests passed. Updated historical da/no
suite: 10 tests passed. Full normal/optimized aggregate outcomes and exact-head
hosted Android outcomes are pending and must be recorded separately. Earlier
focused shared failure was a missing Icelandic tagged-colour projection; diagnosed
and fixed before publication, with rerun pending. No Android SDK is installed in
the local environment: compilation, JVM, lint and device checks are unrun locally.

This work makes no release, signing, access, provider, PR113 or stopped bulk-archive
change. Parent coordinates merge only after exact-head review and required CI.
Suggested next genuinely unresolved ordinary trio: Nynorsk `nn`, Croatian `hr`,
Bosnian `bs`, subject to avoiding overlap with another active assignment. They
must first reconcile their existing P0 receipts rather than repeat them.
