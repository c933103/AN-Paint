# Independent bounded review: round 3 zgh / za

Scope: 30 zgh and 21 za proposed entries in locale-second-drafts. Compared with canonical English and pinned MediaWiki catalogues at 377002822b34077904f4e83c21faaf69d1bfea9a. No canonical edits. This is a technical/semantic screening record, NOT linguistic acceptance or native fluency certification. None of this round's prose is approved for integration by this review.

## Mechanical facts

All 51 strings preserve checked printf placeholder multisets and literal newline counts. Numerals match English, with the correct intentional spelling-to-digit conversion of `zero` to `0` in zgh coordinates. ICO lists retain all seven sizes: 16, 24, 32, 48, 64, 128, 256. Both GIF messages retain 65,535. zgh PDF retains 512 MiB and page bounds 1 to %1$d; assembly messages retain 20 and %1$s/20. za crisp-line instruction correctly follows current English 1..100 pixels, NOT the obsolete one-pixel key name.

## Semantics retained, with linguistic review still required

- zgh PDF file-size candidate visibly includes separate negative clauses for empty-file and exceeding 512 MiB. Do not confuse this with approval of the verbs or negative morphology.
- zgh page-count and coordinate messages retain both numeric endpoints. `whole numbers` terminology remains unverified, but is not simply omitted.
- za GIF candidate explicitly says width AND height cannot exceed 65,535; that preserves per-axis rather than total-area restriction on a semantic reading.
- Missing attachment and not-placed attachment remain different expressions in both locales, not a single conflated error. zgh uses `ur tlli` versus `ur ttusrs`; za uses `mbouj miz` versus `lij mbouj cuengq`.
- zgh long assembly-limit candidate includes remove-one/add-another action, while short candidate omits it as English does.
- za place-at-least-one candidate expresses one OR more than one, retaining lower bound.
- za credit-copy failure variants preserve distinct generic failure, reason placeholder, and insufficient-memory cases. Credit terminology remains held.

## Explicit holds / potential defects

1. zgh GIF: `ur qqant ... ad zrin...` negates an obligation construction. It risks expressing 'not required to exceed' rather than 'cannot/must not exceed'. Require a qualified language check of negation scope; do not accept merely because the number is correct.
2. zgh restore-original-sizes uses `tisalanin`, not established canonical original-size terminology `tinasliyin`. No pinned MediaWiki match supports the new adjective. Hold rather than infer synonymy.
3. zgh assembly now uses `tusmunt`, whereas existing canonical assembly uses `tagrumma`. A deliberate terminology decision is needed; this pass does not establish interchangeability.
4. zgh unknown-image says image is not in assembly; the explicit temporal nuance 'no longer' is not clearly retained. Hold if the product requires this distinction.
5. zgh cropped-thumbnail and attachment modifiers need gender/agreement review. Source noun fragments do not validate the entire compounds.
6. zgh metadata `awttas` (limit), query-failure verb, and publisher noun are not substantiated as technical terms by the inspected source. Hold.
7. za `ui_could_not_load_gallery_image`: MediaWiki `skin-view-view=Doeg` supports a read/view action, not software image loading. Using `doeg` here needs technical-context review.
8. za `Cwmh ... mbouj cwngzgoeng` uses source-supported search for machine metadata query. The UI-error meaning may be understandable, but technical query-vs-user-search equivalence is not verified.
9. za attachment `fu dwk`, gallery phrase, artwork/credit `vihsuz`, response-limit `dajsiuj dauqdap`, font `sawyangh`, memory `neicun`, and copy `fugci` remain unsupported specialist vocabulary in this source review. Do not promote by absence of other findings.
10. za crisp-line `cingcuj` may describe clarity, not hard pixel edges; source does not establish rendering sense.

## Guarded corrections requested

- zgh `ui_same`: do not replace with another unsourced word. `yan %1$s` is not demonstrated to mean 'same %1$s', and the generic placeholder can introduce agreement problems. Keep this key absent from canonical so English fallback supplies correct semantics until a qualified translation/source exists. Same-width and same-height require independent contextual checking, not propagation of this generic construction.
- za processed label: remove `Dozsiengq caeuq liz` from acceptance consideration. Source `and=caeuq` is not a processing verb; no sourced replacement was found. Keep canonical English fallback rather than invent a correction.

Previously source-supported zgh About/copyright labels should use the agreed punctuation-separated exact-source versions, not this round's newly composed conjunction wording. Prior bounded short-label acceptance is unchanged.
