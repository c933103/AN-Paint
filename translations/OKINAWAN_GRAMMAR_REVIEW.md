# Okinawan handoff review — 25 September 2026

The previous completion count concealed substantial Japanese sentences in the
Okinawan catalogue: complete predicates such as `超えています`, `含まれています`,
and `描きます` remained beside isolated Okinawan endings. The review resumed from
the original Jeju/Manchu/Ainu/Okinawan handoff rather than treating the passing
resource gate as linguistic completion.

This pass read the 669 strings and plural against the current English meanings,
and changes 190 strings plus the plural. It rewrites the affected instructions
and explanatory clauses, especially codec/import limits, memory allocation,
recovery, selection geometry, and save/export effects. Bare technical nouns,
format names, and conventional UI terminology are retained; no claim is made
that borrowed technical vocabulary has an independently attested traditional
software meaning.

## Grammar evidence used

[Hanazono Satoru, 2014, an introductory Okinawan textbook proposal](https://www.tufs.ac.jp/icjs/images/publications/journal_004.pdf),
pp. 111–130, especially the sentence-pattern table on printed pp. 119–120
(PDF pages 122–123), provides the grammar checks used here:

- noun/state predicates, existential negation, and comparisons (lessons 1–7, 18);
- bare objects, `ぬ`/`や`, destination `んかい`, and instrumental `っし`;
- commands, connective forms, and completed versus continuing actions (12–13);
- capability versus circumstances and requirements (10, 16, 20);
- conditional and concessive clauses (16, 21–22).

The catalogue uses a Shuri/Naha-oriented written register with modern technical
loans, not a universal spelling for every Okinawan local variety. We do not
substitute another Ryukyuan language's forms for Okinawan. The grammar reference
informs the newly composed sentences; these are not copied example sentences.
The NINJAL dictionary catalogue was located, but its full downloadable dictionary
was not successfully retrieved in this resumed session. It is not listed as
completed evidence for these edits.

| Area | Repair and preserved distinction |
|---|---|
| User actions | Select, enter, tap, and drag are commands; subsequent automatic effects are statements. |
| Missing data | Existential negatives replace Japanese `見つかりません` and incorrect literal negation of “exists.” |
| Memory | Original-resolution working buffers, decoder floors, and smaller output copies remain distinct. All original-file preservation clauses remain. |
| Codec warnings | File size, page range, RGB/ICC conversion, poster image versus first frame, and animation loss remain explicit. |
| Geometry | Crop bounds, one-pixel minimum, reflow of attached images, aspect ratio, and half-short-edge radius limit remain. |
| Save/export | Save reuses the active target; exports do not mark the current drawing saved or change that target. |
| Vertical text | New columns, joined scripts including Mongolian, combining marks, and emoji sequences remain separate clauses. |
| Help captions | Paste uses the actual `ほかの画像` control; drawing guidance uses the actual `移動・拡大縮小` and `強さ（%）` controls. |
| Language note | Removed the inaccurate claim that the catalogue prioritizes Paintroid translations. |

The long editor, assembly, and legacy-help texts were read in full. Most had
already been substantially rewritten; this pass retains their substantive
instructions and fixes the navigation and remaining targeted wording. It does
not regenerate their text from Japanese by replacing particles or suffixes.

## Shared manual repair across the original branch

Jeju, Okinawan, Manchu, Latin Ainu, and Kana Ainu now all document:

1. File → Load image replaces the canvas.
2. Draw → Insert → Other images offers device files and Catrobat, Irasutoya,
   and Openclipart. Choose a device image or open an artwork page and use its
   actual Use image button. Insertion creates a floating selection.
3. File → Image assembly opens assembly; there is no second View route.

The Ainu and Manchu changes are limited to these route/insertion clauses and
exact active-help captions. Existing language work and the rest of the manuals
were preserved. Gallery source/license help routes are a separate shared patch.

Validation: all 27 translation tests pass; `git diff --check` is clean. The new
watercolor-caption reference has `formatted="false"` for its literal percent.
These checks protect resources, arguments, identifiers and limits. They do not
prove idiomatic language. This is a source-assisted editorial pass without an
independent native-speaker sign-off.

## Follow-up after independent review

The initial pass incorrectly wrote the required-item predicate as `要いびーん`.
Hanazono's lesson 26 (PDF page 123) supplies `イリヤビーン`; the memory and
password clauses now use `いりやびーん`. Related `要する`/`要いる` clauses
are rewritten as purpose phrases or a required-item noun with an existential
condition, preserving their actual requirement. The Irasutoya charge sentence
now also uses `料金ぬいりやびーん`, retaining the current File → About → Image
credits captions.

`formats22_pdf_invalid` had also presented two possible failure causes as facts.
It now explicitly scopes them with `可能性ぬ あいびーん`: the file may be damaged
or contain features unsupported by this Android version. `可能性` is a modern
technical noun, with Okinawan case and existential grammar. This preserves
uncertainty without presenting either cause as diagnosed.

The review did not normalize the existing variant `なやびーん` merely because
`ないびーん` occurs in the textbook. Regional variation needs evidence, not
blanket normalization. The independent reviewer checked the
[Okinawa language centre glossary](https://shimakutuba.jp/ctladmin/wp-content/uploads/2021/06/ca0632475bcb04913082a3fe272b8590.pdf)
entry `なりゆん／ないん` for that variant.

All 27 translation tests pass after the follow-up. This remains a source-assisted
editorial review with the language limits stated above.
