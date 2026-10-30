# Yucatec Maya: author second-check of two reviewer corrections

Date: 2026-10-30 UTC. Scope: two P1 targets only. This is a model-authored second-check against primary references, not native-human approval and not a replacement for the final acceptance review. No implementation or original packet mutation.

## Dispositions

| Key | Exact English source | Frozen original target | Exact corrected full target | Decision | Backtranslation | Confidence |
|---|---|---|---|---|---|---|
| ui_underline | Underline | Tʼoʼol yaanal le tsʼíiboʼ | Tʼoʼol yáanal le tsʼíiboʼ | Accept correction; no further revision | A line under the text | High for the orthographic correction; medium-high for the complete checkbox label |
| ui_centred | Centred | Tu chumuk | Tu chúumuk | Accept correction; no further revision | In the middle / at the centre | High for the orthographic correction; medium-high for the complete alignment-option label |

### ui_underline

The intended relation is spatial **under/below**, not other/different. UQROO's dictionary, printed p.51, gives **yáanal** for both the preposition and spatial adverb meaning below. Its p.86 separately assigns the unaccented **yaanal** to other/different. Thus the acute accent here is a meaningful lexical distinction, not optional typographic decoration. INALI's writing norm, printed p.215, table 3.3, independently prints **tu yáanal** as a locative adverb (local extracted lines 7237–7238 include the relevant rows).

The whole phrase remains a nominal description of the underline checkbox: line + below + the text. UQROO's preposition entry supports retaining **yáanal** before the text noun phrase; the INALI adverbial example does not require inserting an extra **tu** into this particular full target. **Tʼoʼol**, **le tsʼíiboʼ**, and U+02BC apostrophes remain unchanged. The app's TextStyleDialog.kt:50 uses this key for the underlining property, not subscript or a separate text-placement instruction. Accept **Tʼoʼol yáanal le tsʼíiboʼ** exactly.

### ui_centred

UQROO's dictionary printed p.43 gives **chúumuk** for centre; p.59 explicitly includes the locative expression **tu chúumuk** under in-the-middle (the extraction splits the stem across a printed line break). INALI's table 3.3, printed p.215, independently gives **chúumuk**. Both the second vowel and the acute accent are needed in the chosen orthography; the original short, unaccented **chumuk** is not the supported form.

The complete locative label expresses the middle alignment setting. It does not suggest issuing a command to recenter a view. TextStyleDialog.kt:54,81–82 places this option between left/right for horizontal text and top/bottom for vertical text; the non-axis-specific phrase works for both. Retain capitalized **Tu** and accept **Tu chúumuk** exactly.

## Primary references actually rechecked

- Javier Abelardo Gómez Navarrete, UQROO, *Diccionario introductorio español–maya, maya–español* (2009): https://www.uqroo.mx/libros/maya/diccionario.pdf . Reviewed text extraction: below entries lines1747–1748; centre lines1377–1378; in-the-middle lines2088–2089; other/different lines3156–3157. Line and writing/text entries were also checked (2734,2128,6744).
- INALI, *Normas de escritura para la lengua maya*, printed p.215, table3.3: https://site.inali.gob.mx/Micrositios/normas/pdf/Norma_Maya.pdf . Reviewed text extraction, lines7237–7238.
- App semantic context: `Paintroid/src/main/java/org/catrobat/paintroid/classic/TextStyleDialog.kt`, lines50,54,81–82. Baseline develop96681f687671a1fdffe134a325843919c1543401, tree39bb7351fa5532194e2c0430432b2f0cc6358a86.

## Frozen-packet preservation

The final acceptance ledger may bind these two exact corrected strings as overrides. The original53 candidates,7 separate invariant-template rows,232 residual records/limits and49 accepted production entries remain unchanged. No new candidate credit is claimed for these corrections.

SHA-256 of the unchanged original packet files at this check:

- `save-ten.tsv`: `7a50a12564025a1fe594e36fbde4b1f7bba4ee53487959f2bca89714f3559ff8`
- `further-candidates.tsv`: `864afc08eeff27a091c3abab74a81f7ba76622fae7a3fe331a94073554fcff31`
- `neutral-format-rows.tsv`: `c6810d7fe5d5aef9fb0a34ed14cd80062e47aeff8fa781b5986dcd444cec1919`
- `residual-source.tsv`: `ea57853596c4759024df2f495ca2755e83ee7e84ba545b7eef500bb48390f79f`
- `residual-limits.md`: `3dc6e96fe3f686bfa094873aba1988278e048d1a6ca6a7aed406065354c22e48`
