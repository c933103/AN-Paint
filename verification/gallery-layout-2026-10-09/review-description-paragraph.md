# Vertical description: avoid repeated paragraph painting

Manual inspection of the first candidate's native-rendered evidence found that
its vertical provider description was painted twice. This was a candidate defect
within the separately tracked AN-W04 vertical-prose repair, not a passed result.

Exact source: `0a2d19db6805016f17b860f8d9964677cfc7880c`, tested tree
`de0742cdd47a55e84ed2773f4808ddd7e3575d29`, run
[37927180323](https://github.com/c933103/AN-Paint/actions/runs/37927180323).
A clear repro is `gallery-vertical-status/api35-en-XV-font2.0-commons_svg_original_size_unavailable.png`:
the whole provider/help caption appears as two identical vertically stacked runs.
The same duplication is visible in the API35 2× Mongolian, Manchu, Literary Chinese
and emoji pseudo-profile captures. Their exact hashes are retained in the
[first-run manifest](first-ci-0a2d19d/artifact-manifest.json).

The gallery concatenated provider label + newline + help, then installed the
accepted shared `VerticalUi.caption`, whose atomic ReplacementSpan covers the
whole source string. A literal newline creates two native TextView paragraphs;
each draws that same whole span. Existing status tests did not check this separate
description, so their passing results did not establish description acceptance.

The bounded gallery-only correction uses a space for that inserted separator in
vertical profiles. It preserves every existing label/help word and uses the same
shared shaping/column renderer. Horizontal layouts retain their original newline.
No translation key/value, text size, provider logic or shared renderer changes.
Resource inspection found no embedded paragraph separators in the six provider
label/help resources in the offered vertical catalogues. The generic direction
branch applies equally to every provider and every shared vertical profile.

The native regression now checks the actual gallery description's exact wording,
full accessible text, one complete replacement span, one native paragraph, full
character layout and unclipped measured ink at APIs30/35, 1×/2×, all five vertical
profiles. One native paragraph prevents this repeated-whole-span defect. The
real-Activity diagnostics also record the description's actual bounds, node text
and native line count. Existing status/action/reachability assertions remain.

Fresh exact-head CI and visual comparison are required; this record does not
claim that the corrected native tests have already run. No physical-device,
TalkBack or fluent-language acceptance is implied.

Local combined Python validation after the complete correction: 326 tests passed
in 49.961 seconds, zero failures/errors/skips. Raw output is
`logs/host-python-description.log`; this does not replace pending Android CI.
