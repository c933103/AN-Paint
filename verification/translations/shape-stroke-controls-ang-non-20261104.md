# Shape tools and stroke controls: Old English and Old Norse

Base commit: 30589063918889bfb056cdb8f25348ce7f2a21db.

Adds 17 previously absent P2 strings to each offered `ang` (Ænglisc) and `non` (Norrœna) catalogue. Independent semantic review accepted all 34 after clarifying that the rounded-rectangle labels round the corners while retaining rectangular geometry.

The batch covers arrow, curve, heart, star and rounded rectangle; curve/polygon completion and polygon closure; fill-plus-outline mode; round, square and calligraphy tips; radius, spray radius and watercolour strength; freehand stroke smoothing and anti-aliasing. PaintDocument tool definitions and ClassicPaintActivity consumers were inspected. Close polygon remains a checkbox, distinct from the finish action that commits pending work. Round/square labels remain suitable for their shared brush, eraser, line and cursor consumers. Tool-specific help outside this P2 block is not included.

Radius is described as centre-to-edge distance, retaining pixels; strength retains percent. Freehand stroke smoothing remains distinct from pixel-edge smoothing. Filled-plus-line mode includes both fill and outline. No application behavior or dynamic argument handling changes.

Validation passed:
- Exact English and target base Git identities; offered picker entries; XML parsing and duplicate-name checks; exactly 17 additions per locale; all 373 previous entries, attributes and surrounding bytes unchanged.
- Android escaping/formatting, source attributes and placeholder/newline parity. These strings have no substitution arguments. Literal units, the additive plus sign and parenthetical anti-aliasing identifier are retained. Strength preserves the source `formatted="false"` attribute for its literal percent sign.
- 78 host tests: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery.
- Structural catalogue validation passed for all 171 offered options. All 1,276 materialized tracked base files matched their Git blob identities and executable modes. The 158 unmaterialized research/verification documents are retained unchanged in the publication tree and were not needed by these checks.

Each locale changes from P2 30/305 to 47/305, leaving 258 P2 keys absent. P0 remains 94/94, P1 249/249 and P3 0/71. These are direct-key-presence counts, not whole-catalogue quality ratings. The priority manifest is unchanged.

Vocabulary follows the current line, polygon, rectangle, outline, drawing and spray terms. [Bosworth-Toller](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/b0281.html) attests feowerscyte in the square sense; [Zoëga](https://norroen.info/dct/zoega/f.html) gives ferskeyttr as square. Modern geometric/UI adaptations and descriptive compounds are not claimed historical computing terms or full-sentence attestations.

Limits: no historical-language specialist certification, whole-catalogue linguistic acceptance, Android build, device/rendering check or CI result is claimed. Canonical Android resources own current wording; this evidence is not a wording freeze.
