# Single-page PDF/TIFF description says “1 pages” in English and French

**Status:** Open bug; documentation-only issue-style tracking PR, not an applied fix. Keep open/draft pending separately reviewed implementation and acceptance evidence.

**Source baseline:** develop `647a4b5647cabf3e51cb6dcf20d41ae08143ccdb`, checked 15 October 2026. **Evidence boundary:** independently confirmed linguistic/static-source finding only; no runtime/device reproduction, CI or whole-language acceptance. [Project board](https://github.com/c933103/AN-Paint/pull/39) and [translation review](https://github.com/c933103/AN-Paint/pull/56) track related work. Issues remain disabled; visibility/settings are unchanged.

## Expected and actual

Expected: the page chooser describes valid one-page and multi-page PDF/TIFF inputs using grammatical count wording.

Actual: the English and French `formats22_page_description` strings contain the unconditional phrase `%3$d pages`. The chooser accepts count 1 and formats that string, producing “1 pages”. This is a shared count/message design defect; Japanese `全%3$dページ` does not share the grammatical problem.

Impact: visibly incorrect count agreement for a valid one-page input. No incorrect page count, lost page, import failure or runtime reproduction is claimed by this static finding.

## Static path and evidence

- [English L570](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values/strings.xml#L570): `%1$s · %2$s\n%3$d pages. Choose one page to edit as an image.`
- [French L595](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-fr/strings.xml#L595): `%1$s · %2$s\n%3$d pages. Choisissez une page à modifier comme image.`
- [Japanese control L139](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/res/values-ja/strings.xml#L139) uses the count-invariant expression `全%3$dページ`.
- [ImportSelection.kt L55–60](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L55-L60) calls `showPages` for PDF/TIFF without excluding one-page inputs. [L98–101](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/ImportSelection.kt#L98-L101) accepts every positive count and formats this string with kind, name and count.
- [PdfCodec.kt L110–112](https://github.com/c933103/AN-Paint/blob/647a4b5647cabf3e51cb6dcf20d41ae08143ccdb/Paintroid/src/main/java/org/catrobat/paintroid/classic/PdfCodec.kt#L110-L112) explicitly permits a page count of 1.

Independent review receipt: [French priority batch 03](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6182504034).

## Bounded fix and acceptance

A count-invariant wording can preserve the existing string API and placeholders:

- EN candidate: `%1$s · %2$s\nNumber of pages: %3$d. Choose one page to edit as an image.`
- FR candidate: `%1$s · %2$s\nNombre de pages : %3$d. Choisissez une page à modifier comme image.`

Alternatively, introduce genuine plural resources and update the call site with correct locale-specific quantities. The candidates are proposed, not applied.

- Verify actual PDF/TIFF chooser descriptions for one-page and multi-page fixtures, preserving the true count, filename/type, page selection and cancellation behavior.
- Keep placeholder types/indexes `%1$s`, `%2$s`, `%3$d` and newline handling correct; test complete rendered messages rather than only counting keys.
- Audit every affected localized count expression for singular/multiple cases. Correct confirmed affected values; do not rewrite already valid Japanese/count-invariant forms merely for uniformity.
- If using plurals, cover each relevant locale's quantity rules and preserve existing import bounds and page-index behavior.
- Perform independent full-value/context review and applicable current-source structural/UI tests before crediting the corrected entries.

## Next action and dependencies

Choose the smallest grammatical message design, enumerate affected locales, implement it with real one-/multi-page chooser regressions, and complete current-source review/test gates. Coordinate receipt replacement in PR56 without double-counting old rejected values. Independent of the Japanese PDF error-cause bug and other trackers. This PR adds only this documentation.
