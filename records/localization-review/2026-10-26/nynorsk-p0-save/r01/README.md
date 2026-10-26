# Nynorsk P0 save/export guard — eight author candidates

**Status: candidate-only; independent whole-value review pending.** No application changes or current coverage increments are supplied. Source is pinned to [`d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4`](https://github.com/c933103/AN-Paint/commit/d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4).

## Why this bounded batch

The verified current report gives `nn` **7/92 P0 present, 85 missing**, with 110 containers present overall. These eight truly absent resources form one data-loss-critical save/export/replace workflow and have exact direct consumers. Existing `Lagra`, `Lagra som…`, `Bilete`, `Fil`, and `Eksporter som…` provide terminology context. This is a workflow-priority decision, not a global ranking of languages or a judgment that English-identical values are wrong.

| Missing P0 identity | Proposed display text |
|---|---|
| `ui_save_your_changes` | Vil du lagra endringane? |
| `ui_your_current_image_has_unsaved_changes` | Biletet du arbeider med, har endringar som ikkje er lagra. |
| `ui_export_did_not_save23` | Eksporten er oppretta. Bruk «Lagra» eller «Lagra som…» til å lagra biletet du arbeider med, før du held fram. |
| `ui_could_not_save_image` | Kunne ikkje lagra biletet |
| `ui_saved` | %1$s er lagra |
| `ui_export_explanation23` | Eksporter eit ikon, Base64-tekst eller ASCII-kunst. Eksportering endrar korkje biletet du arbeider med, eller lagringsmålet for «Lagra». |
| `ui_save_explanation23` | Vel eit biletformat og innstillingane for komprimering. «Lagra» vil bruka dette filnamnet, denne plasseringa, formatet og innstillingane om att. |
| `ui_share_explanation34` | Lagra ein kopi på staden du vel, og vel deretter ein app til å dela kopien. Lagringsmålet for «Lagra» er uendra. |

The JSON records exact Android-quoted candidate values, source attributes and raw UTF-8 hashes, not merely these display strings.

## Behavioral distinctions the review must preserve

- The replacement guard is shown only after applying pending edits when the document is dirty. Save arranges a continuation; Discard runs the replacement; Keep editing dismisses the dialog.
- The File menu calls Share with **both `share=true` and `export=true`**. Ordinary Save reuses the remembered target/options.
- Only **`!exporting`** updates `savedTarget` and marks the document saved. Export and Share write an output without changing that state.
- The **`ui_saved` toast follows every successful write**, including export/share. Its filename placeholder must describe the written output, not assert that every current drawing change is saved.
- If a pending continuation exists during an exporting write, the app shows `ui_export_did_not_save23` instead of running that continuation.
- Failure composition appends **a full stop and an error/fallback message**. The candidate error prefix therefore adds no trailing punctuation or new placeholder.

The exact complete method windows, menu caller and horizontal/vertical consumer sites are in `source-context.json`; immutable source links and byte hashes are in `source-bindings.json`.

## Independent-review questions and limits

Review all eight complete values, not only changed words. In particular:

1. Is **`lagringsmålet`** clear natural Nynorsk for the remembered Save destination, rather than a goal, just a directory, or image position? This compound is an author proposal, not established by the local glossary or dictionary checks.
2. Are **`biletet du arbeider med`**, relative-clause commas and the **`korkje … eller`** construction idiomatic without losing current-image and unchanged-destination meaning?
3. Does **`Eksporten er oppretta`** clearly convey a successfully produced output, not an export setting or export failure?
4. Does **`%1$s er lagra`** stay limited to the named output-file write? Is the filename-first passive preferable to an ambiguous imperative/status `Lagra %1$s`?
5. Do Save and Share instructions retain all source distinctions and all four reused Save items (name, location, format, settings)?

Untouched adjacent labels are included in `candidates.json`, including `ui_save_a5d0d9`'s alias, `ui_discard_changes23` = `Avslutt utan lagring`, and `ui_keep_editing23` = `Avbryt`. Their existing context is visible; this packet neither edits nor independently re-approves them. Missing adjacent labels continue their existing fallback. Nothing in this packet requires broad label normalization.

The official [Nynorsk image entry](https://ordbokene.no/nn/bilete) and [Nynorsk section of the save/store verb entry](https://ordbokene.no/bm,nn/lagre) support only limited lexical choices. `lexical-references.json` distinguishes successful direct page reads from search-index-only evidence. Dictionaries and previously reviewed Bulgarian/Bengali/Amharic counterparts **do not establish Nynorsk sentence acceptance**.

No native-reader, whole-locale, runtime, physical-device, layout, accessibility-output or release certification. The global 59-scoped / 112-outside-scope fixture distinction is unchanged. #56 remains never-merge, #159 frozen, #113 retarget/held-warning scoped; Help callback/archive identity and release pauses are excluded.

## Files and verification

- `candidates.json`: all eight proposed exact values, semantic contracts, uncertainties, peer-review locators and untouched neighbours.
- `source-context.json`: current exact direct-consumer and state-transition excerpts.
- `source-bindings.json`: all eight inspected source files match pinned Git blobs; old ZIP bytes were checked against the current tree before reuse.
- `lexical-references.json`: primary lexical references and their narrow evidential limits.
- `static-bookkeeping.json`: absence, P0 identity, XML round-trip, attribute/hash and placeholder checks only. No application tests ran.
- `manifest.json`: exact bytes, SHA-256 and Git-blob identities.

All eight would increase P0 presence from 7 to 15 **only if independently accepted and later implemented**. That hypothetical is not credited as current progress.
