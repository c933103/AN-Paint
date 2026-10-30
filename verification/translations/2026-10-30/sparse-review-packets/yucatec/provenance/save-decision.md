# Yucatec save lexical decision — 30 October 2026

Declared baseline: merged develop `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`.
Source read: `Paintroid/src/main/res/values/strings.xml`, current YUA catalogue, `translations/string-importance.json`, `tools/fixtures/current_localization/reviewed_priority_batches.json`, and original ZA/NV/YUA candidate/review evidence. Current 49 accepted YUA values remain untouched.

## Decision

**Propose a source-backed alternative, not acceptance of the old ten drafts: Táabsaj as the Save action label, táabsik in the dependent verb, táabsaʼal in the passive.** Exact candidates/backtranslations and confidence are in `save-ten.tsv`. These are AI linguistic candidates, not native-human approval or production acceptance.

The old `Líikʼs` family remains **uncertain**, not categorically wrong. The Universidad de Quintana Roo dictionary places storing together with raising for related liʼis. A lift sense does not disprove a technical storage extension. This investigation did not establish the exact Líikʼs software use. Rather than continuing that ambiguity, it found positive evidence for a different lexical family in actual Yucatec software and non-software digital-recording prose.

## Primary, inspected evidence

1. Mozilla Pontoon Yucatec team: https://pontoon.mozilla.org/yua/ . Downloaded actual current translation-memory export: https://pontoon.mozilla.org/translation-memory/yua.all-projects.tmx . Frozen translation-memory export (header creation timestamp 2026-10-30T20:53:00.965044). Exact paired entries inspected:
   - `focus-for-android:mozilla-mobile/focus-android/app/src/main/res/values/strings.xml:action_save` (lines 5517–5524): Save → Táabsaj.
   - Same project `search_add_manually_save` (5509–5516), same Save label.
   - `firefox-for-android:...:mozac_feature_prompt_save_confirmation` (2598–2605), same Save label.
   - `focus-for-android-po:app.po:save-imagecontextmenu_image_save` (6830–6837): Save image → Táabsa’ak oochelil.
   - Legacy saved-image warning (6822–6829) uses the same táabs- family for saved images. No warning sentence is imported into AN Paint.
2. La Jornada Maya's own Yucatec digital-media prose: https://www.lajornadamaya.mx/k%27iintsil/29769/el-chivo-lubezkie-ku-k-a-aytik-tuumben-nu-ukul-ku-t-absik-koom-cha-an-yeetel-tuumben-iphone-12 . In the title, táabsik is the verb for recording a short film on iPhone. This independently supports the modern digital-recording sense and active form; it alone would not establish file Save.
3. La Jornada Maya: https://www.lajornadamaya.mx/k%27iintsil/226886/yaax-junteen-uuchik-ch-a-abal-u-yoochel-juntuul-u-neene-il-xok-taant-u-siijile . Passive táabsaʼal is used for capturing digital footage. This supports the passive form in the failure message; the file-Save extension comes from software evidence, not from an assumed filming = saving equivalence.
4. Javier Abelardo Gómez Navarrete, Universidad de Quintana Roo, 2009 dictionary: https://www.uqroo.mx/libros/maya/diccionario.pdf pp.67/149/170. Guardar is paired with liʼis/taʼak, and related raising/storing senses coexist. This limits negative conclusions about the old Líikʼs proposal; it is not evidence that the exact old form is natural software Save.

## Important source-quality distinction

Mozilla export is evidence of actual software usage, not automatic linguistic truth. It contains heterogeneous translations: some recent rows are mixed Spanish/Yucatec and another replaces a full English sentence with a period. Therefore no wholesale import, no claim all Mozilla rows are fluent/native, and no such rows are used to certify AN Paint. The Save decision relies on repeated short action labels, an explicit image-saving context, and independent native digital-recording usage. `Táabsaj` is retained as an attested nominal action label; no unattested bare imperative is silently substituted. `bey` constructions are authored combinations, not published exact matches, and appropriately have lower confidence.

Orthography: all Yucatec glottal/apostrophe characters in candidates are U+02BC, matching the existing AN Paint catalogue. Source typography U+2019 is normalized only for that character; vowel length, accents and stem consonants are not mechanically changed. JPEG, JPEG XL, PNG, `%1$s` and ellipses are retained. No application resources were edited; no build or test result is asserted.

## Further language work

`further-candidates.tsv` contains separately authored source-bound proposals. Confidence is per item; none has production-accepted status. `neutral-format-rows.tsv` records seven non-language format templates separately with **zero linguistic-progress credit**. They are not a cheap way to inflate translation counts.

Targeted references for further candidates:
- UQROO dictionary above: height is a noun distinct from high; pencil, brush, eraser and line entries select the right object category. The generic cutting entry differs from knife-cutting. This resolves a lexical distinction, but does **not** automatically validate prior whole crop/trim sentences; their action nominal/verb morphology still needs resolution. I have not promoted that family from the earlier draft.
- INALI orthographic/grammatical norm: https://site.inali.gob.mx/Micrositios/normas/pdf/Norma_Maya.pdf pp.305–309 (PDF indices304–308). It describes transitive imperative -ej and its omission before following constituents; this supports correcting bare standalone Il to Ilej and the complement-bearing Jeʼeb construction. Targeted section read; the entire grammar was not reviewed.
- Primary concrete use/gloss of Ilej by the organization using the name: https://tm.org.mx/2024/03/11/yucatan-se-suma-a-3de3-con-observatorio-ilej-observalo-en-maya/ . No Kʼicheʼ/Qʼeqchiʼ/Itzaj generic-Maya substitution is used.
- Actual kʼaʼabéetkuns spelling in native prose: https://www.lajornadamaya.mx/kiintsil/264208/sats-juntuul-ba-alche-ku-ye-esik-u-leelem-u-boonil-ti-al-ma-u-jaanta-al and the iPhone article above. The spelling is not mechanically changed to a superficially regular long-vowel form.
- Actual quantitative borrowing por siento in native prose: https://www.lajornadamaya.mx/kiintsil/219363/seeba-an-u-bin-ch-a-ak-bej-u-meyaj-u-kuuchil-aeropuerto-internacional-manuel-crescencio-rejon-tu-kaajil-jo . Borrowings are not inherently invalid, but an unverified technical term is not invented merely to fill a row.

Share-family addition: the inspected Mozilla export has `focus-for-android-po:app.po:share-imagecontextmenu_image_share` at lines6846–6853 using túuxt- for Share image, and current Focus `menu_share` at5749–5756 for Share…. This licenses a bounded proposed sending/sharing metaphor, not a claim the chosen image is automatically sent without a chooser. Save-and-share paired action nouns and saved-image morphology remain medium-confidence authored combinations.
