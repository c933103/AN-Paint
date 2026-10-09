# AN-W05-C05 — Hungarian attribution terminology proposal

Status: evidence-only publication of diagnosis and a proposed patch. No application resource has been changed; the patch is proposed, not applied. Android/runtime checks for the proposal have not run.

## Result and bounded scope

The inherited Hungarian `gallery_copy_credit` is `Jóváírás másolása`. That names account crediting, while the actual action copies image-attribution text. Proposed wording: `Forrásmegjelölés másolása`.

The same false friend occurs in 17 directly related Hungarian resources. Correcting only the button would leave its literal instruction reference, Copy/Save confirmations and surrounding attribution panels inconsistent. The proposed coherent set enumerates every named resource and every exact replacement below. It is not a global substitution, does not alter legal bodies or provider content, and preserves all unrelated prose. No genuinely financial usage occurs in these 17 contexts. Irasutoya’s actual paid-use threshold and fee statements remain unchanged.

This is a focused semantic proposal, not a competent-language sign-off for the Hungarian catalogue or the other 59 scoped catalogues. The wider localization reset remains in force.

## Pinned source and semantics

- Analysis commit: [`43148951ac6bd23687e66685855909ac538ba004`](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/); tree `ab5ff7fe6d04d5e22348b979c9e0054eef9b1c0f`. The isolated native snapshot has exactly this tree. The local snapshot commit ID is synthetic and is not offered as upstream provenance.
- [English label and explanation](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values/strings.xml#L603-L614): attribution includes title, publisher, source and licence; creator/copyright notices and edits are discussed.
- [Clipboard implementation](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L15-L58) builds the attribution and publishes a plain-text clip. [Editor Copy](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L131-L145) saves its edited attribution first, then copies it. No behavior change is proposed.
- [Gallery action wiring](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L174-L195) passes `gallery_copy_credit` to injected page controls and dispatches the copy scheme to attribution copying. [Commons Copy](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L253-L263) fetches metadata and uses `record.text(imported=false)`; it does not register an insertion. No Gallery provider requests were made for this investigation.
- [About chooser](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L868-L882) shows that the other labels open image credits or bundled attribution/notices files, not payments.
- Existing Hungarian [size/save errors](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L692-L693) already use `forrásmegjelölések`. C04’s new, already-correct errors are excluded from this proposal and must be preserved when the base is updated.

## Public terminology evidence

- [Wiktionary’s Hungarian jóváírás entry](https://en.wiktionary.org/w/index.php?title=j%C3%B3v%C3%A1%C3%ADr%C3%A1s&oldid=63075365) explicitly gives the banking/account-crediting sense. This is lexical evidence, not language-wide review.
- The Hungarian Intellectual Property Office’s [2022/10 journal, page 174](https://sztnh.gov.hu/sw/static/file/202210-szemle.pdf) uses `forrásmegjelölés` in a discussion of identifying the source of reused audiovisual material. It supports the attribution/source-identification sense.
- [Creative Commons’ own Hungarian BY 4.0 summary](https://creativecommons.org/licenses/by/4.0/deed.hu) describes attribution as naming the author, linking the licence and identifying modifications. It confirms the operation’s semantic domain; it does not supply the exact proposed UI phrase.
- The exact Hungarian wording is a contextual translation proposal grounded in these sources and the app’s existing terminology. Dictionary mirrors at MEK/Arcanum could not be fetched; no claim relies on their unseen contents.

## Individually identified proposed subitems

### AN-W05-C05-HU-01: `gallery_copy_credit`

Purpose: Injected beside gallery artwork and on the attribution editor Copy button.

- `Jóváírás másolása` → `Forrásmegjelölés másolása` (1 occurrence(s))

### AN-W05-C05-HU-02: `gallery_description`

Purpose: Gallery instructions quoting the Copy, Edit, About and Image credits labels.

- `Jóváírás másolása` → `Forrásmegjelölés másolása` (1 occurrence(s))
- `Jóváírások szerkesztése` → `Forrásmegjelölések szerkesztése` (1 occurrence(s))
- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence(s))
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence(s))

### AN-W05-C05-HU-03: `gallery_edit_credits`

Purpose: Gallery action that opens the image-attribution editor.

- `Jóváírások szerkesztése` → `Forrásmegjelölések szerkesztése` (1 occurrence(s))

### AN-W05-C05-HU-04: `gallery_credit_copied`

Purpose: Clipboard-success notice after attribution text is copied.

- `Jóváírás másolva` → `Forrásmegjelölés másolva` (1 occurrence(s))

### AN-W05-C05-HU-05: `gallery_credit_saved`

Purpose: Confirmation after the attribution editor accepts Save.

- `Jóváírási szöveg mentve` → `A forrásmegjelölés szövege mentve` (1 occurrence(s))

### AN-W05-C05-HU-06: `ui_image_credits`

Purpose: Image-attribution panel/editor title, export-section label, clipboard clip label and Commons metadata-loading status.

- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence(s))

### AN-W05-C05-HU-07: `ui_about_credits23`

Purpose: File-menu entry and About/licences/attribution chooser title.

- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence(s))

### AN-W05-C05-HU-08: `ui_credits_terms`

Purpose: Gallery button opening the selected provider’s attribution/terms page.

- `Jóváírások és feltételek` → `Forrásmegjelölések és feltételek` (1 occurrence(s))

### AN-W05-C05-HU-09: `ui_icons_fonts_artwork_credits`

Purpose: About action/title displaying legal/ASSET_CREDITS.txt.

- `Ikonok, betűtípusok és alkotások jóváírásai` → `Ikonok, betűtípusok és alkotások forrásmegjelölései` (1 occurrence(s))

### AN-W05-C05-HU-10: `ui_open_source_credits_and_notices`

Purpose: Title displaying legal/THIRD_PARTY_NOTICES.txt.

- `Nyílt forráskódú jóváírások és közlemények` → `Nyílt forráskódú összetevők forrásmegjelölései és közleményei` (1 occurrence(s))

### AN-W05-C05-HU-11: `ui_gimp_translations31`

Purpose: About action/title displaying legal/GIMP_TRANSLATION_NOTICES.txt.

- `Fordítási jóváírások és licencek` → `Fordítások forrásmegjelölései és licencei` (1 occurrence(s))

### AN-W05-C05-HU-12: `ui_catrobat_s_own_artwork_uses_cc_by_sa`

Purpose: Catrobat guidance containing the exact About → Image credits path.

- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence(s))
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence(s))

### AN-W05-C05-HU-13: `ui_irasutoya_help34`

Purpose: Irasutoya guidance on retained source pages/attributions and the exact About → Image credits path.

- `A forrásoldalak és jóváírások` → `A forrásoldalak és forrásmegjelölések` (1 occurrence(s))
- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence(s))
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence(s))

### AN-W05-C05-HU-14: `ui_openclipart_help34`

Purpose: Openclipart guidance containing the exact About → Image credits path.

- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence(s))
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence(s))

### AN-W05-C05-HU-15: `ui_help23`

Purpose: Main Help summary quoting the About chooser label; Commons text and all other instructions retained.

- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence(s))

### AN-W05-C05-HU-16: `ui_add_up_to_20_images_with_android_s`

Purpose: Assembly Help final sentence referring to the shared Catrobat/AGPL and asset-attribution notices.

- `Ez a mód ugyanazokat a Catrobat/AGPL- és eszközjóváírásokat használja, amelyek a fő szerkesztő «Fájl > Névjegy, licencek és jóváírások» paneljén szerepelnek.` → `Ez a mód ugyanazokat a Catrobat/AGPL-re és a felhasznált elemekre vonatkozó forrásmegjelöléseket használja, amelyek a fő szerkesztő «Fájl > Névjegy, licencek és forrásmegjelölések» paneljén szerepelnek.` (1 occurrence(s))

### AN-W05-C05-HU-17: `ui_the_arrow_on_the_left_directly_below_the`

Purpose: Detailed Help: quoted Terms/About/Image credits labels, bundled-font attributions and the About panel’s asset/font-attribution content.

- `Jóváírások és feltételek` → `Forrásmegjelölések és feltételek` (1 occurrence(s))
- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (3 occurrence(s))
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence(s))
- `jóváírásaikat` → `forrásmegjelöléseiket` (1 occurrence(s))
- `eszköz-/betűtípus-jóváírásokat` → `a felhasznált elemek és betűtípusok forrásmegjelöléseit` (1 occurrence(s))

The complete old/proposed value, English source, source line and each replacement are retained in `proposal.json`. `proposed-hu.diff` is a review artifact only; it has not been applied. The proposal explicitly preserves resource keys, attributes, placeholders, escaped newlines and all non-replacement bytes.

## Same-label screen across the established scope

`label-scan.json` records every individual `gallery_copy_credit` value from the default source plus the 59 tags in `tools/test_translations.py:SCOPED_TAGS` (60 entries total). The other 81 offered locales are not part of this task.

- Hungarian is the only established financial false friend in this pass.
- The English AU/CA/GB and Portuguese PT values say only Copy/Copiar. Their omitted object is an independent clarity observation, not a financial-credit defect; they are left unchanged.
- Credit cognates are not automatically errors. For example, Afrikaans [publisher use of Fotokrediet](https://aanlyn.solidariteit.co.za/publieke/artikel/afrikaansdag-solidariteit-vier-100-jaar-van-afrikaans-as-amptelike-landstaal) and Finnish [film-study use of krediitti for creator information](https://www.theseus.fi/bitstream/10024/346720/2/Leino_Kati-Anne.pdf) provide counterexamples to assuming that every credit cognate is financial-only. This does not certify the app’s exact label naturalness.
- Uncertain attribution/acknowledgment wording and orthographic naturalness remain explicitly unaccepted; no speculative additional locale patch is proposed.

## Validation already performed

On the unchanged pinned snapshot:

- `python3 tools/translation_catalogues.py`: PASS, all catalogues structurally valid.
- `python3 -m unittest discover -s tools -p 'test_translations.py'`: PASS, 32 tests, including the existing 59-tag completeness assertions.
- Proposal construction checks: 17 explicit named-resource replacements only; all expected occurrences present; unchanged placeholder signatures and escaped-newline counts; proposed values pass Android quoting and format checks using each resource’s actual `formatted` attribute. The detailed Help already has `formatted="false"`; this attribute is preserved.
- Android compilation, instrumented or Robolectric runtime, screenshots and competent-language acceptance: NOT RUN / NOT ESTABLISHED for the proposed text.

## Proposed patch and test plan

1. Wait for the C04 integration base to be settled. Re-read the current Hungarian catalogue and reapply only these explicit replacements on an isolated C05 branch. Preserve C04’s new error resources, existing correct save/size errors and other workers’ changes.
2. Keep production changes confined to these 17 entries in `values-hu/strings.xml`; no Kotlin/Java logic changes, new resource keys, provider text or legal-body edits.
3. Add a narrow host regression for the proposed Hungarian attribution family, exact button references in instructions, and unchanged placeholder/newline contracts. Store the per-subitem decision and baseline/current evidence durably with C05 in GitHub.
4. Run canonical structural validation and the unchanged scoped completeness tests. Run the separate C04 resource contracts after integration. Do not present the known-out-of-scope 81-locale completeness gap as a new C05 failure or weaken that scope.
5. Compile the Hungarian resources with strict AAPT2 if the existing toolchain is available, then run current-platform Android regression/lint on the final head via the normal repository workflow. Do not launch an unrelated full matrix.
6. Because the replacement labels are longer, add Hungarian to the existing narrow/portrait/landscape/large-text gallery reachability coverage, and exercise the real attribution editor’s Copy/Save controls using local fixture data. Check About/notice titles and menu labels at large text. Preserve action behavior and clipboard content with the existing credit-flow tests; no live provider traffic is needed.
7. Publish C05 separately with an exact remote-tree check, source/evidence and precise test status after proposal review. The master tracker and merge are handled separately. This evidence-only publication is not an implementation PR.

## Follow-up refinement and C03 successor impact

HU-16 has been refined to keep the explicit Catrobat/AGPL attribution sense. See [test-impact-plan.md](test-impact-plan.md) for the strict successor plan for C05-HU-15, which intentionally changes the historical C03 Help hash. The review-only successor manifest and an in-memory 60-case/seven-negative-mutation proof are retained here. Historical C03 evidence and application resources remain unchanged.
