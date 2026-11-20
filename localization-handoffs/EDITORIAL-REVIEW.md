# Editorial review checkpoint

Input: `a537ece7b363d7cb32014c3978c1db44ff1e2864` (the frozen 2,334-slot combined authoring handoff). No translations are changed by this review checkpoint.

## First pass: the long help text in Cherokee, Navajo and Tai Nüa

The assembly guide, compact help and editor guide in each of these three languages keep the expected 8, 1 and 10 paragraphs. A targeted comparison found the original technical names, controls' numeric anchors, color hex values, provider names and keystroke tokens in their corresponding paragraphs. This is not evidence of grammatical or semantic equivalence.

- Cherokee editor guide, paragraph 2: the label `Pale Violet` remains in English while the same handoff already has separate Cherokee wording for the swatch. Reconcile the label after its wording is validated; keep `#5B67FF` literal.
- Cherokee editor guide, paragraphs 3 and 7: the generic `slider` and trailing `stroke smoothing` are still in English. Decide on descriptive wording and check it against both actual control captions. Do not collapse brush-stroke smoothing into pixel anti-aliasing.
- Navajo editor guide, paragraph 7: the brush control is described generically; verify that a reader can identify the actual Strength control. Separately validate polygon completion and rotation captions.
- Tai Nüa editor guide, paragraphs 1 and 7: `Watercolor` remains English. Check the exact localized brush label before altering the guide. In paragraph 5, cross-check that `mask` refers to the shape of the selection, not hiding or deleting a layer.
- The compact Cherokee help and all three assembly guides still need a sentence-by-sentence semantic comparison, especially around crop undo, allowed overlap and RAM fallback. The paragraph/token screen alone does not show those relationships.

New linguistic acceptances: **0**. Retain all source-facing holds. No Android resources, PR, device test or integration changes.

## Second pass: generic typeface labels saved unchanged

Checked all nine localized name slots wired into [FontCatalog](https://github.com/c933103/AN-Paint/blob/597e644c31c450d45aa6962d89564581d4434758/Paintroid/src/main/java/org/catrobat/paintroid/classic/FontCatalog.kt#L20-L27) against the frozen handoff. **15 locale-key pairs need a terminology decision**, not automatic acceptance as invariants. These are visible chooser captions; Android family IDs and bundled proper names are separate and should stay unchanged.

- Tai Nüa (`tdd`): all nine captions: `ui_sans_serif`, `ui_serif`, `ui_monospace`, `ui_sans_light`, `ui_sans_thin`, `ui_sans_condensed`, `ui_sans_medium`, `ui_cursive`, `ui_casual`.
- Navajo (`nv`), Central Nahuatl (`nch`), and Western Huasteca Nahuatl (`nhw`): `ui_sans_serif` and `ui_serif` in each. A familiar borrow is a legitimate outcome only if it distinguishes the choices for the locale. Eastern Huasteca's descriptive pair is a comparison, not a term to copy between varieties.
- When drafting Tai Nüa captions, treat fixed character spacing, stroke weight, and letter width as separate attributes. Keep light, thin and medium distinct. Keep connected handwriting and informal lettering distinct. Consult [W3C font terminology](https://www.w3.org/TR/CSS22/fonts.html#generic-font-families) for the source-side concepts and Luo's [Dehong Tai dictionary](https://openresearch-repository.anu.edu.au/bitstreams/1b27afe2-adda-4fe2-95bf-5402206be010/download) for locale vocabulary. The dictionary did not establish a conventional typeface term in this pass. No borrowed or newly coined captions are accepted here.
- Later, test Tai Nüa and Cherokee glyph rendering in the default-font chooser and long help on a real Android build before deciding whether to bundle fonts. [AOSP Android 15's font inventory](https://android.googlesource.com/platform/frameworks/base/+/android-vts-15.0_r5/data/fonts/fonts.xml) includes Noto Sans Tai Le and Noto Sans Cherokee; that is not a device-rendering result.

New linguistic acceptances in this pass: **0**. Frozen authoring file unchanged; no Android XML, app coverage or integration changes.

## Third pass: numbered format arguments across the handoff

Compared typed source and candidate strings, including each plural quantity separately, for indexed Android/Java format tokens, `%%`, and `%n`. All **691 token occurrences across 392 text cells** match their source multisets; **0 missing, added, or altered tokens** in this defined class. Ordinary percent signs in prose were not treated as placeholders. This pass does not verify grammatical placement, rendering, or application behavior. No linguistic acceptances, integration, or resource changes.

## Fourth pass: Cherokee attribution action and feedback

`gallery_copy_credit` is a button command to copy the attribution text. `gallery_credit_copied` is shown after the clipboard action succeeds. The frozen Cherokee candidates use the same phrase for both. Each of the seven other draft locales with both keys has different wording for the two contexts. Hold the Cherokee pair pending wording that distinguishes the action from its result; review the pair together. No newly accepted wording or resource changes in this pass.

Provisional replacement pair, not accepted:

- `gallery_copy_credit`: `ᏧᏬᏪᎳᏅᎯ / ᏅᏓᏳᏓᎴᏅᎯ ᎠᎪᎵᏰᏗ — ᎤᏠᏱ ᎪᏢᏅᏗ`
- `gallery_credit_copied`: `ᏧᏬᏪᎳᏅᎯ / ᏅᏓᏳᏓᎴᏅᎯ ᎠᎪᎵᏰᏗ: ᏗᏟᎶᏍᏔᏅᎯ (ᎠᏍᏆᏛᎯ)`

Word choice follows existing Cherokee app keys `gallery_credit_could_not_save`, `ui_export_recovery_copy`, and `ui_full_text_copied` on the pinned source. This supports distinguishing action and result within the app, not the naturalness of the complete phrases. Check the idiomatic attribution term and whether the completion marker is redundant. Keep both on hold.

## Typeface follow-on authoring: 15 previously unchanged captions

Below are provisional alternatives for the 15 slots flagged in the second pass. Keep the original authoring snapshot intact; these are replacements for review, not acceptances. Validate stroke endings, fixed advance versus narrow glyphs, all three stroke weights, and handwriting versus casual style. Do not change Android family IDs.

```json
{
  "tdd": {
    "ui_sans_serif": "ᥘᥤᥐ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ ᥖᥤ ᥙᥣᥭ",
    "ui_serif": "ᥘᥤᥐ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ ᥖᥤ ᥙᥣᥭ",
    "ui_monospace": "ᥖᥨᥝ ᥘᥤᥐ ᥐᥧ ᥖᥨᥝ · ᥖᥣᥒᥰ ᥐᥣᥒᥲ ᥛᥫᥢᥴ ᥐᥢ",
    "ui_sans_light": "ᥘᥤᥐ ᥙᥣᥭ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ · ᥔᥥᥢᥲ ᥛᥣᥒ",
    "ui_sans_thin": "ᥘᥤᥐ ᥙᥣᥭ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ · ᥔᥥᥢᥲ ᥛᥣᥒ ᥖᥤ ᥔᥧᥖᥴ",
    "ui_sans_condensed": "ᥘᥤᥐ ᥙᥣᥭ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ · ᥖᥨᥝ ᥘᥤᥐ ᥞᥤᥙᥴ",
    "ui_sans_medium": "ᥘᥤᥐ ᥙᥣᥭ ᥟᥛᥱ ᥛᥤᥰ ᥔᥥᥢᥲ ᥟᥥᥱ · ᥔᥥᥢᥲ ᥐᥣᥒ",
    "ui_cursive": "ᥘᥤᥐ ᥖᥦᥛᥲ ᥘᥒᥱ ᥛᥪᥰ · ᥖᥨᥝ ᥘᥤᥐ ᥓᥙᥴ ᥐᥢ",
    "ui_casual": "ᥞᥣᥒᥲ ᥘᥤᥐ ᥓᥬᥳ ᥐᥧ ᥝᥢᥰ"
  },
  "nch": {
    "ui_serif": "Letras ica pilquentzi tlahuasantli campa tlami ininrayas",
    "ui_sans_serif": "Letras amo quipiyaj pilquentzi tlahuasantli campa tlami ininrayas"
  },
  "nhw": {
    "ui_serif": "Letras ica piltziquitetzi tlahuazantli campa tlami ininrayas",
    "ui_sans_serif": "Letras amo quipiyaj piltziquitetzi tlahuazantli campa tlami ininrayas"
  },
  "nv": {
    "ui_serif": "Saad: niníʼáhgi ídzoh yázhí hólǫ́",
    "ui_sans_serif": "Saad: niníʼáhgi ídzoh yázhí ádin"
  }
}
```

- Tai Nüa: [Dehong dictionary](https://openresearch-repository.anu.edu.au/bitstreams/1b27afe2-adda-4fe2-95bf-5402206be010/download) supports components for tip (p. 109), narrow (p. 28), thin (p. 88), middle (p. 39), and join (introduction). The [Tai Nüa script chart](https://arhiiv.eki.ee/knab/lat/kbltdd2.pdf) is a spelling reference. Review modern narrow/join spelling, caption length, and whether light versus thin reads naturally. The descriptive compounds are not attested typeface names.
- Central and Western Huasteca Nahuatl: compare each locale's pinned app keys `ui_line`, `ui_choose_a_smaller_size`, `ui_font`, and `ui_font_family`. The loan `rayas` is deliberate for the terminal stroke description. Validate idiom and chooser length separately for both locales.
- Navajo: the pinned app supplies text and line vocabulary; [Wall and Morgan](https://upload.wikimedia.org/wikipedia/commons/6/6c/Navajo-English_Dictionary.pdf) supports lexical components, and the [Swarthmore lexicon](https://talkingdictionary.swarthmore.edu/navajo_postposition/?introduction=&lang=nav) has speaker examples for the presence/absence construction. The adapted generic endpoint term is the weakest component. Do not assume the full compounds are attested.

No linguistic acceptance, Android integration, or device verification.

## Fifth pass: source names in UI messages and unchanged entries

Reviewed the canonical combined handoff at `027c199839d7e78cf0174841fcb5a9e82f990e2c` (blob `a8ff12aacf9bd675bfffb373e79eeaa0cb372dee`). Checked 238 non-invariant string entries with one or more defined literal product names, format names, colour codes, or shortcut tokens. Three entries omit a source literal; all three omit PDF. The other 235 retained every literal checked. This is an editorial screen, not a translation, grammar check, or Android test.

- Eastern and Western Huasteca Nahuatl, `formats22_pdf_page_index`: both tell the reader to choose a page from this document but omit the format name, while neighbouring errors retain PDF. Check whether the same error can appear without a visible PDF heading. If it can, restore the literal PDF to the error so users can identify the workflow. Compare each variant's wording separately.
- Western Huasteca Nahuatl, `formats22_pdf_crop`: the draft preserves the selected-page and non-empty-region instructions but omits PDF. Check its standalone error context before accepting its omission.
- All 114 records marked invariant are identical to the typed source values in the handoff. Eight cursor-help aliases preserve `@string/ui_cursor_help31` verbatim. Equality alone does not establish that a recorded invariant is linguistically appropriate or that the alias resolves on Android.

**New wording authored, accepted or integrated: 0.** No device verification. The combined file was not changed.

## Sixth pass: PDF error context and explicit numerical limits

Candidate file: `b05fb20235ea266b4265f4236c3fb7258d6c790a` (blob `4ec048d12a74dd312d9dfd99801b5fd0a403f053`), pinned app base `597e644c31c450d45aa6962d89564581d4434758`.

- **PDF error context:** In the pinned source, `ImportSelection.kt` closes the page chooser before the import handler revalidates the page index. Classic and Assembly error callbacks can show a generic dialog afterwards, so the page message should name PDF independently of the picker. `AssemblyRenderer.kt` also passes the placed item's crop back to the PDF renderer; an output failure can be shown outside the original picker. This supports preserving PDF in the three provisional replacements (Eastern and Western Huasteca page index; Western Huasteca crop). It does not establish normal-UI reproducibility, target-language idiom, or acceptance.
- **Numerical screen:** Of the strings with distinct source and draft wording, 70 entries across the nine locales contained an explicit source numeral followed by MiB, GiB, px/pixels, %, or ° (including both ends of dashed ranges). All 120 source value occurrences had a matching standalone numeral somewhere in that candidate. This limited test does not verify the unit, duplicate counts, upper/lower bound, scope of the limit, spelled-out numbers, or the sentence's meaning. For editorial review, check source bounds and qualifiers as a unit, especially `formats22_pdf_file_size` (>0 and ≤512 MiB), the pixel-grid threshold (≥800%), and the pencil default (1 px) versus max (100 px).
- **New review flag:** The Tai Nüa editor guide (`ui_the_arrow_on_the_left_directly_below_the`) adds `90°` twice in descriptions of rectangular selection, although the pinned source specifies no angle in either description. A right-angle description may be a legitimate explanation of the shape, but it should not sound like a limit on rotation. Hold both sentences for a language check and retain the separate Rotate instruction.

New translations, linguistic acceptances, Android integration, and device verification: **0**. The combined authoring file is unchanged.
