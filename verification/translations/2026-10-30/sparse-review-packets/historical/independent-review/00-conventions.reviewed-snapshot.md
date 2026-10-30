# AN Paint — historical-language candidate drafts, not accepted strings

## Source and authority

- Declared baseline: commit `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`.
- Read source: `Paintroid/src/main/res/values/strings.xml` and `translations/string-importance.json`.
- The local Git directory is an unborn index, not a checkout with a resolvable HEAD. The baseline identity above is supplied provenance, not an independently verified local commit. English in each row was read from the supplied source. XML entities are decoded in English columns; Android `\n` and backslash escapes are shown literally when present.
- Target resources: `values-b+ang/strings.xml` and `values-b+non/strings.xml`, both empty and explicitly unstarted when read. **Research only; no application resource has been changed.**
- Scope requested: 92 P0 + 249 P1 keys for each language. Batches are drafts only. Presence in a batch is NOT linguistic acceptance or implementation permission.
- I am producing research-assisted candidates, not claiming to be a native speaker of either historical language or to reproduce historical software usage. All complete sentences and all UI senses require independent specialist review. Technical compounds are particularly uncertain.

## Proposed normalization — not an accepted project policy

**ang:** normalized late West Saxon prose orientation, approximately tenth–eleventh centuries. Latin script; `æ`, `þ`, `ð`, `w`; no runes, no dotted c/g, no length marks. Thorn is generally initial, eth medial; this is an editorial convention, not an asserted medieval rule. Infinitives label actions, singular imperatives address the user in instructions. Avoid pseudo-Shakespearean modern English. Modern punctuation and Arabic numerals serve the UI.

**non:** normalized Old West Norse prose orientation, approximately thirteenth-century Icelandic/Norwegian literary language, not a claim to cover every Old Norse variety. Latin script with accents, `þ`, `ð`, `ǫ`, `ø/œ` where appropriate; `ok`, `at`, `eigi`, `aptr`, and historical inflection. No modern-Icelandic replacement text, modern `og/að` syntax, or decorative runes. Infinitives label actions; singular imperatives address users. Modern punctuation/numerals are an explicit interface adaptation.

## Confidence and rationale codes

- **M:** moderate confidence in a short candidate's basic lexical/grammatical meaning, but the UI application is still a modern proposal. Not approved.
- **L:** low confidence: novel terminology, complex inflection/syntax, or semantic ambiguity needs specialist correction before use. Not approved. Every long safety string should be treated as L even if its backtranslation preserves all safety clauses.
- No H/native/accepted rating is used. A backtranslation is my own intended reading, not independent validation.
- **A**: ordinary attested lexical base applied to a modern action; **N**: explicit new compound or new technical sense; **S**: safety distinction intentionally retained; **P**: placeholder/format literal retained; **G**: grammar/case or idiom needs particular review.

## Proposed terminology ledger

| Concept | ang proposal | non proposal | Status / intended distinction |
|---|---|---|---|
| save | healdan | varðveita | Historical verbs, new disk-save sense. `varðveita` has medieval accusative as well as earlier dative constructions; the draft uses accusative consistently. |
| export | utberan | fœra út | Literal carry/bring out, new technical sense; never claims the current document was saved. |
| cancel | ablinnan | hætta við | Cease the pending action, not destroy current work. Review `hætta við` as a complete historical idiom. |
| discard | forlætan | kasta brott | Abandon/cast away, not save. Explicit changes object where source gives it. |
| erase / clear | adilegian | má brott | Erase; not the cancel action. |
| image | anlicnes (f.) | mynd (f.) | Attested likeness/image words extended to raster data. |
| file | gewrit (n.) | rit (n.) | Written item, modern file sense; does not mean specifically a text-only file. |
| draft | weorcgewrit (n.) | vinnurit (n.) | **New compounds** “work-writing”; working draft, not final saved output. |
| copy | efenwyrht (f., provisional) | eptirrit (n., technical extension) | **Uncertain ang coinage**, “equal-made thing”; non “after-writing”. Applies also to image/archive data. Review morphology and suitability. |
| recovery copy | efenwyrht to eftstaþelunge | eptirrit til viðgerðar | **New technical phrases**: copy for restoration. No claim that export itself restores the editor. |
| assembly | samnung (f.) | samsetning (f.) | Gathering/putting together, extended to multi-image assembly. |
| editing | awending (f.) / awendan | breyting (f.) / breyta | Alteration/change, not necessarily correction of a mistake. |
| canvas | metingbord (n.) | myndborð (n.) | **New compounds** “drawing-board/image-board”; not a claim to an attested electronic canvas. |
| pixel | anlicnesprica (m., weak) | myndhlutr (m.) | **New compounds** “image-dot/image-part”, defined to mean one raster pixel; technical review needed. Keep the international unit `px` where the source uses it. |
| memory | gemynd (f.) | minni (n.) | **New machine-memory senses**, distinct from persistent file storage. |
| device | searu (n.) | tæki (n.) | Existing instrument/device vocabulary applied to hardware. |
| app | weorctol (n.) | verkfæri (n.) | **New application senses** “work-tool”. Android and other product names remain literal. |
| format | hiw (n.) | háttr (m.) | **New data-format senses** form/manner. |
| setting | gesetnes (f.) | skipan (f.) | Arrangement, new software-setting sense. |

Long strings sometimes use a phrase instead of the short ledger noun to make a distinction explicit. Do not treat these choices as settled terminology. Save and recovery are especially dependent on a consistent glossary and independent semantic review.

## Primary references actually consulted

1. Bosworth–Toller, *An Anglo-Saxon Dictionary*, Charles University digital edition: [healdan search/result](https://bosworthtoller.com/search?q=healdan), [ā-blinnan](https://bosworthtoller.com/37362). Supports lexical bases, not UI meanings.
2. Bosworth–Toller, [an-lícnes, p. 44](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/b0044.html). Historical likeness/image senses; new raster use is ours.
3. Cleasby–Vigfusson, [varð-veita, p. 680](https://www.germanic-lexicon-project.org/html/oi_cleasbyvigfusson/b0680.html). The accusative use is medieval, not merely a modern-Icelandic assumption.
4. Cleasby–Vigfusson, [geyma transcription](https://oldnorsedictionary.com/home/word/geyma). Its older genitive government and notes on later accusative use informed choosing `varðveita` instead for this draft.
5. Cleasby–Vigfusson, [mynd transcription](https://oldnorsedictionary.com/home/word/mynd). Image/figure is attested; photographs and raster images are not historical meanings.
6. University of Texas Linguistics Research Center, Jonathan Slocum and Winfred Lehmann, [Old English introduction](https://lrc.la.utexas.edu/eieol/engol/0). Editorial spelling and inflection guidance, not an exact UI precedent.
7. University of Texas Linguistics Research Center, Todd Krause and Jonathan Slocum, [Old Norse grammar contents](https://lrc.la.utexas.edu/eieol_toc/norol), [Lesson 2](https://lrc.la.utexas.edu/eieol/norol/20). Historical prose and weak-verb paradigms.

The live ONP homepage timed out; no ONP verification is claimed. Several Bosworth–Toller direct search opens also failed; only returned entries above support the listed decisions. Published exact UI equivalents are not a gate: these are modern proposals on historical linguistic bases. Neither glossary nor sentences have undergone independent review.
