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
