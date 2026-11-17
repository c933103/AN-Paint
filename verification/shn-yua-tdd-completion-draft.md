# Shan / Yucatec Maya / Tai Nüa completion and Cherokee source workstream

This is a work-in-progress translation proposal, not linguistic acceptance or release approval. It resumes full-language completion rather than creating separate 18–34-entry PRs. English remains the explicit fallback for keys not yet translated.

Baseline: `428f9f2a203116c4d11a279ea2c1cfb3093059c0` (`develop`). On the 718 translatable-string definition used by this pass, baseline gaps are Shan 288, Yucatec Maya 322, Tai Nüa 329. This denominator is deliberately not conflated with the tracker's 719-entry inventory.

Current proposal adds 288 Shan values and 322 Yucatec Maya values (including one reference alias and format-only controls), plus two Tai Nüa references to existing resources with identical English source, three dictionary-informed colour names, two filename-sort labels and two acronym licence headings. It leaves zero Shan, zero Yucatec Maya and 320 Tai Nüa gaps. Both structurally complete catalogues remain unaccepted linguistic drafts. Missing long guides and specialized terminology have not been replaced with English copies to manufacture completeness. Tai Nüa prose remains blocked on reliable linguistic coverage.

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

## Deeper source-semantic quality pass

This pass reviewed the 381 changed nonguide Yucatec source/target pairs; the three long guides had their separate full-value review above. Eight Yucatec values were corrected: the CC BY-SA exception was accidentally expressed as an only-if condition and now explicitly applies when the source does **not** identify separate terms; two selection tooltips now distinguish rotation from restoration; three pinch instructions use the existing two-finger-distance explanation; Watercolor uses the actual control label; and open-source retains the explicit technical term instead of equating open licensing with merely visible source code. An independent model source-semantic pass checked all eight repairs. The selection tooltip's shape/path wording and general native phrasing remain unresolved review items.

The Shan author rechecked all 288 additions (285 short/medium values and three guides), including format/memory, normalization, licensing and the full 19 guide paragraphs. Seven values were corrected: rectangle versus generic quadrilateral, square resize handles, the canonical radius term, explicitly rapid consecutive polygon taps, and the actual Image assembly recovery control. This was an author source-semantic pass, not independent native-speaker approval. These checks cover later-priority content and existing translated quality, not merely P0/P1 presence.


## Inherited Yucatec catalogue review

Extended the source-semantic author review to the 334 inherited values unchanged by the preceding draft, including memory/recovery errors, colour conversion, canvas/crop behaviour, gesture accessibility and geometry labels. This is an inspection for concrete errors, not a no-defect certificate. Together with the previous changed-value and guide passes, review now reaches the full 718-string Yucatec catalogue rather than only newly added or high-priority values.

The university-hosted [Gómez Navarrete dictionary](https://www.uqroo.mx/libros/maya/diccionario.pdf), printed pp. 64, 118, 134 and 137, resolves the previously recorded shape/path concern: `patul` denotes form/figure, while `beel` denotes a path. The selection aspect-lock tooltip now says it preserves shape using the existing canonical geometry noun. An inherited crop-preview instruction also used `jutsʼ` (bringing near), not the dictionary-supported dragging root `jíil`; both drag occurrences in that value now use the same reviewed drag root as the other gestures. Existing scroll instructions using `jutsʼ` were not blanket-changed: the UI-scroll adaptation still needs qualified terminology review. The two corrections do not certify general sentence grammar.

The same source supports retaining the existing left-direction spelling, Main label and Arrow noun rather than speculative substitutions based on their other senses. No additional Tai Nüa or Cherokee sentences were composed without stronger evidence. Their unresolved qualified-language requirements remain unchanged. Exact-head review and CI are still merge gates.


## Cherokee lexical expansion and further Tai Nüa research

The official Cherokee Nation [2024 consortium vocabulary](https://language.cherokee.gov/media/vdiic5hr/2024consortium.pdf) provides direct lexical evidence for three previously missing labels: Honeycomb (entry 1), Horizontal and Spectrum. Visually checked PDF pages 43 and 84 (zero-based 42/83) against their English and transliterated columns. Added these three bounded label drafts to `values-b+chr`; 329 of the 718-string denominator remain missing. Honeycomb is used as the palette-layout metaphor; Spectrum names the colour-spectrum control. No novel sentences or verb paradigms were extrapolated. These lexical facts do not establish the naturalness of the UI metaphors or native acceptance. The document itself is linked, not reproduced.

The same new source's Save entry differs from the inherited application's imperative frame. It does not by itself settle that command; no bulk Save substitution or Save-as expansion was made. Cherokee Nation's [Cherokee Reader](https://cherokee.gov/media/ti2etezo/cherokee_reader.pdf) and the Durbin Feeling dictionary entry indexed as 72393 reinforce that inherited Remove wording is used for moving objects, but selecting the correct UI Remove imperative still needs contextual evidence. No unsupported replacement was made.

Further Tai Nüa searches covered potential Wikimedia UI extension sources and Luo's wheel/honeycomb/colour entries. The queried UploadWizard, MultimediaViewer and extension VisualEditor Tai Nüa paths were absent; dictionary senses and historical-script OCR do not safely establish modern UI words. No new Tai Nüa text was added; 320 gaps remain. This bounded negative result is not evidence that no other qualified source exists.

## Inherited Shan catalogue review

The Shan author read the remaining 430 inherited unchanged source/target pairs, including safety, recovery, rendering and typography strings. Combined with the prior 288-addition pass, this reaches the full 718-string catalogue. It is author source-semantic review, not independent native acceptance or a no-defect certificate.

Corrected the Italic control and its main-guide reference to the same source-attested term. [Pinned Wikimedia VisualEditor Shan](https://github.com/wikimedia/VisualEditor/blob/8ad5e6ac6ec3e079d0fe7595f683959a95cabef8/i18n/shn.json), `visualeditor-annotationbutton-italic-tooltip`, supplies the term, credited to Saimawnkham and Saosukham. This is identical to the previously attributed source content (MIT) already covered by the packaged translation notices; the control and guide are now consistent. No other grammar was extrapolated from that word. The apparent Percent concern was rejected after checking [Unicode CLDR's percent unit data](https://unicode.org/cldr/charts/50/by_type/units.other_units_metric_per.html); the existing term is supported. Strikethrough is also supported by VisualEditor and was retained. Differing upstream Invert terms were not treated as permission for a speculative rewrite.


## Cherokee colour-name follow-up and remaining feasibility limit

The Cherokee Nation-hosted [English–Cherokee dictionary](https://language.cherokee.gov/media/ykahxw4v/oudictionaryeuglutan.pdf), PDF pages 282 and 642 (zero-based 281/641), supplies paired syllabary/transliteration entries for Gold and Silver. Both pages were downloaded and rendered for visual inspection. Added the explicitly glossed metal-name variants, not the alternative yellow-only or silver/shiner senses. Like Copper and the source's English names, these are palette colour-name metaphors; native UI naturalness remains unaccepted. Cherokee has five newly drafted lexical labels in this proposal and 327 remaining missing strings.

These bounded words do not establish the sentence grammar needed for the remaining legal notices, image assembly, P2/P3 tool guidance or full inherited-catalogue certification. Searches for cursive/monospace/strikethrough in the consulted dictionary found no entries. Existing Remove and Save concerns remain unresolved. Full Cherokee and Tai Nüa completion requires qualified language work beyond these source lookups; structural tests and model inspections cannot substitute for it. No format-only copies or extrapolated technical sentences were added to inflate completion.
