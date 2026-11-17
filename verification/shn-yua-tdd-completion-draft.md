# Shan / Yucatec Maya / Tai Nüa completion workstream

This is a work-in-progress translation proposal, not linguistic acceptance or release approval. It resumes full-language completion rather than creating separate 18–34-entry PRs. English remains the explicit fallback for keys not yet translated.

Baseline: `428f9f2a203116c4d11a279ea2c1cfb3093059c0` (`develop`). On the 718 translatable-string definition used by this pass, baseline gaps are Shan 288, Yucatec Maya 322, Tai Nüa 329. This denominator is deliberately not conflated with the tracker's 719-entry inventory.

Current proposal adds 288 Shan values and 322 Yucatec Maya values (including one reference alias and format-only controls), plus two Tai Nüa references to existing resources with identical English source three dictionary-informed colour names, two filename-sort labels and two acronym licence headings. It leaves zero Shan, zero Yucatec Maya and 320 Tai Nüa gaps. Both structurally complete catalogues remain unaccepted linguistic drafts. Missing long guides and specialized terminology have not been replaced with English copies to manufacture completeness. Tai Nüa prose remains blocked on reliable linguistic coverage.

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
- The same dictionary p. 67 and the pinned [MediaWiki Yucatec catalogue](https://raw.githubusercontent.com/wikimedia/mediawiki/377002822b34077904f4e83c21faaf69d1bfea9a/languages/i18n/yua.json), `savechanges`, support **taʼak** for saving. The inherited catalogue instead uses **Táabsaj** and inflections extensively. This terminology inconsistency initially blocked extending the three long guides; the subsequent paradigm correction below resolves the root evidence, not general fluency. A fluent reviewer must still settle nominal save constructions, tap/pinch vocabulary, direction/geometry wording and connected sentence grammar. No claim is made that a dictionary alone can settle these. At that stage save wording was not blanket-replaced with unreviewed inflections.
- Shan: a second **author** pass corrected seven existing draft values to bind the actual Pencil, Radius, Fit, Finish polygon, Paste, Drawing settings and Watercolor Strength labels. Legal obligation/exception language was rechecked without an identified concrete modality error. This is not independent native-speaker or legal certification.
- Tai Nüa: obtained [Luo Yongxian, *A dictionary of Dehong, Southwest China* (1999), Pacific Linguistics C-145, ANU](https://openresearch-repository.anu.edu.au/bitstreams/1b27afe2-adda-4fe2-95bf-5402206be010/download), and visually checked printed pp. 107, 179 and 224. Added dictionary-informed colour-name drafts for silver, copper and gold. The lookup used the lexical entries, not OCR glyph substitutions or automated conversion from Shan. These three labels do not establish proficiency for the remaining 324 strings. The downloaded online edition identifies CC BY-SA 4.0, ©1999 Pacific Linguistics and/or the author(s); no dictionary pages or prose are reproduced in the app.

At the source-correction stage, the three Yucatec guides were still absent. They were subsequently drafted as documented below. Full-language scope remains the objective, but structural presence is not a substitute for the unresolved qualified-language review.


## Save paradigm review and correction

[Shigeto Yoshida (2009), *Diccionario de la conjugación de verbos en el maya yucateco actual*](https://www.academia.edu/3381085/Diccionario_de_la_conjugaci%C3%B3n_de_verbos_en_el_maya_yucateco_actual), T entries, supplies the previously missing grammatical evidence: **táabs** concerns deception, whereas **taʼak** concerns keeping/storing. The active **taʼakik**, passive **taʼakaʼal** and resultative **taʼakaʼan** are explicitly documented. Corrected 94 resources using these forms, including inherited baseline strings and quoted button labels. An independent model source/context pass checked all 94 against their English uses and identified four publishing contexts, which must not be treated as storage. These were separately changed using the pinned MediaWiki `publishpage` phrase for making public, with active/passive adaptation. This is still not native grammar certification: nominal constructions and adapted publication sentences remain review items. At this correction stage, no long-form guide completion was claimed.

The publication exceptions are `gallery_credit_publisher`, `gallery_description`, `gallery_credit_edit_hint` and `ui_openclipart_help34`. Their former root was already inappropriate, so the correction did not revert it. The technical saved-state and export-destination distinction remains unchanged.

Tai Nüa filename-order controls now reuse the existing `save20_file_name` wording, itself matching pinned MediaWiki `filename`, followed by the source's literal A–Z / Z–A sort indicators. This adds no new grammatical composition; 322 Tai Nüa gaps remain. Presence counts are not linguistic approval.


## Full Yucatec guide draft

Added all three remaining full values: assembly (8 paragraphs), main guide (10), quick help (1). Every paragraph was written as a draft using the corrected save/drag vocabulary and existing UI labels, not English fallback copies. An independent model source-semantic pass read all 18 assembly/main paragraphs against the English clauses. It identified and corrected rotation versus restoration wording, stroke smoothing versus softening, actual control-label references, downward landscape ordering and memory-budget versus total-device-memory wording. The quick guide received an author clause audit. Separate checks confirmed the 8/10/1 paragraph structure and numeric, colour-code, format and product tokens.

This is **structural draft completion only**, not a fluent or accepted translation. Technical loans, grammatical naturalness, embedded long labels, history-stack terminology, legal phrasing and the previously noted nominal/publication adaptations still need qualified review. The full-language scope is preserved; zero gaps must not be reported as native-speaker approval or a release gate passing.


## Further Tai Nüa source boundary

Added two bounded licence headings using pinned MediaWiki `license-header` and the unchanged identifiers AGPL / GNU AGPL. This translates the heading only, not licence obligations. No unsupported legal sentence was composed. Luo (1999), section 2.3.1.2 (printed p. xxi), was also consulted for head–modifier structure; a compound pattern does not establish that arbitrary technical phrases are idiomatic. The remaining 320 gaps therefore still need qualified language work. No other Tai Nüa prose was added in this pass.


## Cherokee feasibility research (no catalogue edits)

The additional Cherokee lane is reserved for source-based work, not bulk generation. Consulted the [official Microsoft Cherokee localization styleguide](https://download.microsoft.com/download/4/a/3/4a372197-0042-4cb0-a13b-7decf7132c26/chr-chr-styleguide.pdf) and [Cherokee Nation technology-localization materials](https://language.cherokee.gov/technology-localization/), including links to paired interface screenshots and Office/Windows tutorials. These are useful terminology and usage references, not proof of the application's full custom sentences.

The [pinned MediaWiki Cherokee catalogue](https://github.com/wikimedia/mediawiki/blob/ea83228d5fe2b1f9559196a2716c8580cdb2407d/languages/i18n/chr.json) has 255 entries. It does not supply exact full values for the application's substantial missing technical/legal guidance. Some legacy messages contain unexplained Latin prefixes, so source origin alone cannot justify blanket copying. A concrete concern needs contextual verification: current `ui_remove` equals MediaWiki's `move` value, whereas its `remove` and `delete` values differ. Do not carry that inherited Remove wording into new guides without resolving it. Similarly, existing Save-as frames are not automatically certified merely because three additional format names could be substituted.

The official [92-page Windows 8 paired-screenshot PDF](https://language.cherokee.gov/media/3ukaiatf/windows8screenshots.pdf) was surveyed and likely device/language-setting pairs inspected at full size. No visible Remove/Delete command was found in those inspected pairs. This does not prove it is absent everywhere; it means the source pass did not resolve the mismatch. No Cherokee values were changed, and the Save-as format-substitution candidates were withheld.
