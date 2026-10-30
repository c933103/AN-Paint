# Three regional candidate catalogues — incomplete, not accepted

Base checked against remote `develop`: `420cb76fb1fc02a53a5b6296505be193eaa3bb2f`.
Scope: qug Chimborazo Highland Kichwa, quh South Bolivian Quechua,
quz Cusco Quechua. Paused quy excluded. No production XML changed.

These are independently editable draft strings, not linguistic certification.
Each XML contains only actual proposed translations. `scope.tsv` inventories **all 92 P0 + 249 P1 keys** and their English meanings,
distinguishing proposed text from unresolved entries. The three review JSON
files list missing keys separately. Missing text is not English fallback claimed
as translation. `regional-comparison.tsv` explicitly lists every proposed key
as all-identical, Southern-identical, or regionally different. Shared words
are independently reviewable candidates, not mechanical acceptance transfer.
The TSV is the authored bilingual working record; its backtranslation describes
proposed meaning, not a second independent review. No acceptance is transferred
between varieties, even where candidates coincide.

## Regional choices and actual uncertainties

- **qug**: Ecuadorian forms `shimi`, `killka`, `shuyu`, `tullpu`, `mushuk`,
  `yurak`, `-shka`, `-pak`, `-na` action labels, rather than Southern Quechua
  suffixes and aspirated/ejective inventory. This is a Chimborazo-targeted
  candidate, **not proof of specifically Chimborazo idiomatic usage**. Local
  review is necessary for infinitive-style action labels, `kipu` as computer
  file (not established here), `ruray` as application, `ñawpa shuyu` for draft,
  `ñawpak/washa` for foreground/background, and `allishka` for ready.
- **quh**: `jallch'ay` for Save, `juk`, `jatun`, `juch'uy`, `jina`,
  `llimphi`, `khuchuy`, and `llankhay` for touch are candidate regional choices.
  Review `siq'i` for a raster image versus drawing, `kipu` for file,
  `kikinchay` for Copy, `wakjinayachiy` for modification, `ñawpaq siq'i`
  for draft, and whether `jallch'ay` is preferable to `waqaychay` in this UI.
- **quz**: `waqaychay`, `huk`, `hatun`, `huch'uy`, `hina`, `llimp'i`,
  `kuchuy`, `llamiy`, and `llapan` are candidate Cusco-oriented choices.
  Review `siq'i` versus a broader image term, `kipu`, `kikinchay`,
  `hukmanyachiy`, and `ñawpaq siq'i` as above independently of quh.
- The paired **Draw again / Redo** wording currently shares “do/draw again”
  semantics; reviewers must ensure the history action is unambiguous in the UI.
  **Cancel / Discard / Clear** must not be collapsed: unresolved discard
  strings have deliberately not been guessed from Cancel.
- `Piksel` is an explicit technical loan, not a claim about an established
  regional standard. FG/BG are expanded to front/back rather than English
  initialisms; review available width before production use.
- Long memory-budget, autosave/recovery, colour-profile and destructive-crop
  warnings remain unresolved wherever a fully faithful regional rendering
  could not responsibly be supplied. A misleading warning is worse than an
  honestly identified missing draft. These gaps are a linguistic-competence
  limitation, not an unavailable API, a permission denial, or a requirement
  that exact published UI phrases must already exist.

## Narrow reference check

These references informed narrow terminology/orthography questions only; they
are not evidence that the full proposed UI has been published or reviewed.

- Bolivia: ILLA dictionary catalogue identifies the Instituto de Lengua y
  Cultura de la Nación Quechua / CENAQ dictionary separately from Cusco and
  Chanka material: https://www.illaa.org/index.php/diccionarios/
- Bolivia educational language guidance lists `Jallch’ay` and `waqaychay`
  as guardar synonyms: https://educacioninterculturalbolivia.org.bo/wp-content/uploads/educacion-en-lengua-Ind%C3%ADgena/LINEAMIENTOS%20BASE%20EDUCACI%C3%93N%20LENGUA%20QUECHUA%20EN%20INICIAL%20Y%20PRIMARIA.pdf
- Ecuador university Kichwa curriculum supports `tullpu` as colour, but its
  Napo programme is **not Chimborazo regional validation**:
  https://www.ikiam.edu.ec/index.php/curso-de-kichwa/
- Peru Ministry of Culture distinguishes Quechua Collao/Cusco geographic scope:
  https://bdpi.cultura.gob.pe/lenguas/quechua

## Checks

XML serialization/parse and positional-format-token parity are checked for
proposed entries. Apostrophes are Android-escaped, including ejectives.
Literal format identifiers and numbers remain intact. `validation.json`
reports exact counts; presence is not acceptance. No full test/build runs,
merge, native-speaker review, screen fit, or production acceptance performed.

### Additional review targets in the second partial batch

`shuyuna pampa` / `siq'ina pampa` explicitly mean drawing surface (canvas),
not the image itself. The crop constraints distinguish staying within this
surface from staying within the image. `illak` / `ch'usaq` denote zero in
the positive-dimension messages. Confirm these usages independently.
`kodifikador` is an unvalidated technical loan, not silently presented as an
established local encoder term. Automatic saving is rendered compositionally
(“saving by itself”); verify `kikinmanta` / `kikillanmanta` idiom and the
failed/paused distinction. Clockwise explicitly means in the clock direction.

Examples of legitimate overlap needing independent review: `pichana`
(eraser), `yanapay` (help), and the Southern forms `qillqa` (text), `paña`
(right), `qhaway` (view). The mathematical layout strings and Hex #RRGGBB
are invariant notation, not evidence of translated prose. Identical values
are not generated by adapting one catalogue with a global replacement rule:
the authored TSV records three proposed strings per key. This still does
not establish native fluency or regional acceptance.

## Final partial coverage at this handoff

Each locale: **32/92 P0 + 166/249 P1 = 198 candidate entries**. This
includes **8 invariant mathematical/technical notation entries**, so the
proposed translated prose is **190 entries per locale**, not 198. Each
locale has **143 unresolved keys** (60 P0 + 83 P1). The assigned full
translation job is **not complete**. Independent regional review is needed
for proposed text as well as expert translation of the remaining warnings.

All 594 XML entries were parsed and checked using the repository's
`android_string_errors` and `FORMAT_TOKEN` functions. `git diff --check`
passed. The builder now reproduces these checks; no full test suite ran.
Publication uses a dedicated evidence branch and changes no application
catalogue. The 198-row comparison identifies 81 regionally differing rows,
102 rows with identical Southern candidates, and 15 all-identical rows
(including the 8 invariant notation rows).
