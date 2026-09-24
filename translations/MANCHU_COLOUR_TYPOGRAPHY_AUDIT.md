# Manchu colour and typography repair — 24 September 2026

Scope: 56 changed values in `values-b+mnc+Mong/strings.xml`, covering the
colour selectors, palette slots, colour-profile errors, font controls, drawing
tool labels and vertical-text help. The existing Wheel label was also checked
and retained. No application code or other language catalogue changes.

This is source-assisted translation, not independent native-speaker approval.
The modern software descriptions below are authored Manchu constructions; they
are not presented as terminology from an established Manchu software standard.
English words and neighbouring-language translations were not respelled to
create the new wording.

## Lexical checks

The primary reference is H. Kuribayashi and Hurelbator,
[the Manchu index to the 1780 triglot dictionary](https://gerel.net/articles/roncho/A47All.pdf).
Page references below are PDF pages, counting the first page as 1.
Jerry Norman's lexicon was also consulted through its
[searchable transcription](https://www.studylib.net/doc/7052336/21-826-entries);
ambiguous OCR spellings were checked against the primary index.

| UI concept | Manchu wording / basis | Review decision |
| --- | --- | --- |
| Honeycomb | `kiya`, PDF p329 | An attested word replaces the untranslated English label. The help describes its colour cells and the black-to-white row. |
| Cursive | `lasihire hergen`, PDF p348 | Uses the attested script description. |
| Airbrush | `sisara fi` | A short description of the tool's sprinkling action; the verb is indexed on PDF p450. |
| Pencil | `tarcan fi` | A description of the writing tool using the material term indexed on PDF pp495–496. Both help strings retain crisp edges at every selected width. |
| Ellipse / radius | `golmin muheliyen` / `dulin onco` | Short descriptive labels. Radius help explicitly defines the distance from a circle's centre to its edge, and retains the half-shorter-side limit. |
| Pale Violet | `biyahūn šušu boco`, PDF pp64,486 | Uses the colour senses of these words, replacing respelled English. |
| Dither | `boco i tongki be kamcibure` | Describes combining colour dots. The dot term is indexed on PDF p510. The full GIF explanation is maintained with the accompanying general-prose repair. |
| Font styles | Stroke ends, thickness, width | Serif and sans-serif describe the presence or absence of terminal ornament; thin/light/medium and condensed remain distinct. The unsupported inherited `itomka` is removed. |

## Meaning retained in longer descriptions

- The spectrum selects `HSL H` and `HSL S`, with the right-hand control changing
  `HSL L` across the black-to-white range. The wheel selects `HSV H` and `HSV S`,
  with the right-hand control changing `HSV V`. These identifiers refer to the
  actual implementations in `AdvancedColourDialog.kt`; lightness and value are
  not conflated into a single translated setting.
- Palette instructions retain tap for foreground, hold for background, scrolling
  for further colours, explicit slot selection and replacement of stored colours.
- Colour metadata is described as a record explaining the colours. A colour-aware
  editor is described as a tool that adjusts colours according to that record.
  The ICC warning still requires exporting an RGB copy first; the BMP/GIF warning
  still requires conversion to sRGB PNG before import. Converter failure explicitly
  says the image was not imported. Truncation and unsupported metadata remain
  separate errors.
- Vertical help explains that a new line starts a new vertical column, that joined
  writing such as Mongolian stays joined in sideways mode, and that upright mode
  keeps attached marks and character sequences forming one pictorial symbol
  together. The explicit column-order labels are retained.
- Literal format/model identifiers, `px`, `%`, `#RRGGBB` and Android format
  placeholders are preserved. New Manchu text uses canonical letters, without
  inserting Sibe IY or arbitrary variation selectors.

Validation: XML parsing and placeholder preservation, all 25 translation tests,
all three bundled-font coverage tests, complete Android resource compilation
with AAPT2, and `git diff --check`. These checks establish resource integrity and
glyph availability; they do not establish native idiom or replace device review.
