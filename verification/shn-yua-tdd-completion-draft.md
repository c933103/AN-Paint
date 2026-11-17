# Shan / Yucatec Maya / Tai Nüa completion workstream

This is a work-in-progress translation proposal, not linguistic acceptance or release approval. It resumes full-language completion rather than creating separate 18–34-entry PRs. English remains the explicit fallback for keys not yet translated.

Baseline: `428f9f2a203116c4d11a279ea2c1cfb3093059c0` (`develop`). On the 718 translatable-string definition used by this pass, baseline gaps are Shan 288, Yucatec Maya 322, Tai Nüa 329. This denominator is deliberately not conflated with the tracker's 719-entry inventory.

Current proposal adds 288 Shan values and 319 Yucatec Maya values (including one reference alias and format-only controls), plus two Tai Nüa references to existing resources with identical English source and three dictionary-informed colour names. It leaves zero Shan, three Yucatec Maya and 324 Tai Nüa gaps. The three Yucatec gaps are the assembly, main and quick-start guides. Missing long guides and specialized terminology have not been replaced with English copies to manufacture completeness. Tai Nüa prose remains blocked on reliable linguistic coverage.

The Shan author checked source/placeholder alignment. An independent model source/semantic review of Yucatec identified and corrected “fewer files” and transparent-versus-bright ICO backing ambiguities, horizontal-versus-left-to-right direction, explicit two-drag instructions, and smooth-versus-small wording. This is not native-fluency acceptance; full independent linguistic review, especially of licensing, typography and technical instructions, is still required. Presence and structural checks are not proof of naturalness.

The shared catalogue validation, translation-boundary checks, translation catalogue tests and current legal/protocol/format contracts must be run on the final proposal. Hosted exact-head Codex review and required CI remain merge gates. No merge or release is authorized by this record.

## Tai Nüa follow-up investigation

The full Tai Nüa MediaWiki catalogue (1,144 message keys excluding `@metadata`) was compared with the English messages from the same pinned revision and the 329 missing application strings. Comparison ignored terminal punctuation, case, surrounding whitespace and literal newline escapes. No exact normalized source-text matches were found. This is a bounded negative result, not a claim that no reusable terminology exists anywhere.

Sources inspected:
- [MediaWiki Tai Nüa](https://raw.githubusercontent.com/wikimedia/mediawiki/377002822b34077904f4e83c21faaf69d1bfea9a/languages/i18n/tdd.json) and [matching English](https://raw.githubusercontent.com/wikimedia/mediawiki/377002822b34077904f4e83c21faaf69d1bfea9a/languages/i18n/en.json).
- [VisualEditor Tai Nüa](https://raw.githubusercontent.com/wikimedia/VisualEditor/4d12cd4ed69480fcf0ebc7aa0627716e39ab93af/i18n/tdd.json).
- Existing application source mappings in `translations/SOURCE-SUPPORTED-UI.json` and the packaged source-supported translation licence notice.

Useful terminology leads include MediaWiki `filename` (filename), `filehist-dimensions` (dimensions), `filehist-datetime` (date/time), `show-big-image` (original file), and `license-header` (licensing). These are **not** sufficient evidence for composing the application's longer instructions, technical distinctions or legal obligations. Reusing words does not establish sentence grammar or legal meaning. No synthetic long-form Tai Nüa prose was added on that basis.

Two missing controls have exactly the same English source as existing app controls. They now reference those resources: `ui_copy_an_area_or_use_file_insert_image` → `ui_paste_hint34`; `ui_disable_cursor_drawing` → `ui_disable_cursor_drawing33`. These reduce structural fallback by two; they are not two newly translated or independently verified sentences. Existing target wording still requires linguistic review. That alias-only step left 327 gaps; the dictionary follow-up below reduces that to 324. A fluent Tai Nüa contributor must resolve the prose/terminology gap before full-language completion can be claimed.

The follow-up Yucatec controls were checked against their English clauses and the existing translated UI labels; exact button labels were aligned. Literal `%` in the quoted strength label is marked `formatted="false"`. Catalogue validation plus 44 boundary/catalogue/current-contract tests are rerun on the combined final proposal before publication. These are structural/source-alignment checks only.

All 68 remaining Shan entries were drafted, including the three complete guides. Author review checked source clauses and aligned existing UI labels. An independent nonlinguistic check confirmed 8/10/1 paragraph counts and retained the source numeric/format/product tokens; this does not establish semantic equivalence or native fluency. Zero missing Shan keys is structural completion of the draft only, not accepted language completion.

Independent model source-semantic review of the follow-up Yucatec controls identified four further clarifications: square resize handles, outward canvas expansion, explicit consecutive double-taps, and current-canvas memory accounting. These were corrected before final checks. This review still does not certify fluent Yucatec.


## Source-led correction pass

- Yucatec: [Javier Abelardo Gómez Navarrete, *Diccionario introductorio español–maya, maya–español*, Universidad de Quintana Roo (2009)](https://www.ordensincronico.com/wp-content/uploads/2021/07/Diccionario-Espanol-Maya-_-Maya-Espanol.pdf), printed pp. 34 and 134, distinguishes the dragging verb **jíil / jíilt** from **jiitʼ** (weaving/braiding). Corrected the draft dragging root in 24 resources. Dictionary evidence establishes this lexical distinction, not complete sentence grammar or UI naturalness.
- The same dictionary p. 67 and the pinned [MediaWiki Yucatec catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/377002822b34077904f4e83c21faaf69d1bfea9a/languages/i18n/yua.json), `savechanges`, support **taʼak** for saving. The inherited catalogue instead uses **Táabsaj** and inflections extensively. This unresolved terminology inconsistency blocks responsibly extending the three long guides. A fluent reviewer must settle the save paradigm, tap/pinch vocabulary, direction/geometry wording and connected sentence grammar. No claim is made that a dictionary alone can settle these. Existing save wording was not blanket-replaced with unreviewed inflections.
- Shan: a second **author** pass corrected seven existing draft values to bind the actual Pencil, Radius, Fit, Finish polygon, Paste, Drawing settings and Watercolor Strength labels. Legal obligation/exception language was rechecked without an identified concrete modality error. This is not independent native-speaker or legal certification.
- Tai Nüa: obtained [Luo Yongxian, *A dictionary of Dehong, Southwest China* (1999), Pacific Linguistics C-145, ANU](https://openresearch-repository.anu.edu.au/bitstreams/1b27afe2-adda-4fe2-95bf-5402206be010/download), and visually checked printed pp. 107, 179 and 224. Added dictionary-informed colour-name drafts for silver, copper and gold. The lookup used the lexical entries, not OCR glyph substitutions or automated conversion from Shan. These three labels do not establish proficiency for the remaining 324 strings. The downloaded online edition identifies CC BY-SA 4.0, ©1999 Pacific Linguistics and/or the author(s); no dictionary pages or prose are reproduced in the app.

The three Yucatec guides are still absent, not represented by English copies or synthetic full-length text. Full-language scope remains the objective, but structural presence is not a substitute for the unresolved qualified-language review.
