# AN-W05-C05 — bounded Hungarian attribution wording review

Date: 9 October 2026. Status: review evidence only; proposal not applied.

## Result

All 17 explicitly enumerated replacements are supportable in their individual contexts. No required wording correction was identified. This is a contextual terminology and grammar review, not native-speaker acceptance, competent-language catalogue sign-off, Android/runtime approval or a legal-compliance assessment.

The [structured 17-item dispositions](wording-review-dispositions.json) retain each exact proposed value and replacement list. The reviewed [proposal](https://github.com/c933103/AN-Paint/blob/7bbb788b667b4b7fac22fc074e41267bd1fdfd0f/verification/attribution-terminology-2026-10-09/proposal.json) is unchanged.

## Provenance and boundaries

- Reviewed proposal commit: `7bbb788b667b4b7fac22fc074e41267bd1fdfd0f`; proposal blob: `f635b7c3ffa001406caceec4967bd70b998f712d`.
- Application baseline: `43148951ac6bd23687e66685855909ac538ba004`, tree `ab5ff7fe6d04d5e22348b979c9e0054eef9b1c0f`.
- The cached proposal exactly matched GitHub. The 11 inspected application/legal-notice file blobs also matched the pinned GitHub versions; their hashes are recorded in the structured dispositions.
- This publication adds review evidence and clarifies two README descriptions. It does not apply the proposed patch, change production or legal-body files, or alter the original proposal/proof artifacts. The original evidence commit remains the parent history.
- Implementation remains held until the C04 integration base is settled. Existing C04 errors and historical C03 evidence must be preserved at integration.

The attribution wording is supported because these panels identify reused material and its authors/sources. It is not a universal translation of English “credits”: a standalone contributor roll or acknowledgement needs its own contextual wording. No financial meaning occurs in the changed attribution phrases; Irasutoya's separate fee statement is preserved.

## Primary terminology evidence

- [Hungarian Intellectual Property Office journal, October 2022, printed page 174](https://sztnh.gov.hu/sw/static/file/202210-szemle.pdf#page=174): Observed use of forrásmegjelölés for identifying reused audiovisual material's source. Terminology-domain evidence; not an exact UI translation or catalogue acceptance.
- [Creative Commons BY-SA 4.0 Hungarian summary](https://creativecommons.org/licenses/by-sa/4.0/deed.hu): Attribution involves identifying the creator, linking the licence and indicating changes. The summary does not supply the exact proposed UI phrases. This is terminology evidence, not a legal-compliance assessment.
- [Hungarian National Bank: payment-account terminology list](https://mnb.hu/penzforgalom/fizetesi-szamla-iranyelv-pad): Observed use of jóváírás for funds credited to an account. Supports the financial distinction; does not prove that every conceivable use is exclusively financial.

These sources support the semantic distinction; none certifies the exact proposed UI phrases or the full Hungarian catalogue.

## Reachability qualifications

- **HU-12:** retained Catrobat guidance resource. The current [Catrobat provider mapping](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L8-L12) selects `gallery_description` instead. Live reachability of `ui_catrobat_s_own_artwork_uses_cc_by_sa` was not established.
- **HU-17:** retained detailed Help resource. Static repository search found catalogue/test references, but no direct production reference to `ui_the_arrow_on_the_left_directly_below_the`. The current [main Help action](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1576) selects `ui_help23`. Live reachability of the retained detailed resource was not established.

Both retained resources remain in the proposal for catalogue and literal-label consistency. Absence of a direct static reference is not a runtime proof that a resource can never be reached.

## Individual dispositions

### AN-W05-C05-HU-01 — `gallery_copy_credit`

**Supported contextual proposal.** The label names copying one attribution record. The selected editor record is saved before copying. Singular forrásmegjelölés fits the copied text; the action does not copy image pixels or account credit.

- `Jóváírás másolása` → `Forrásmegjelölés másolása` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L49); [Clipboard action](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L49-L58); [Editor actions](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L131-L145).

### AN-W05-C05-HU-02 — `gallery_description`

**Supported contextual proposal.** All four substitutions reproduce the corresponding proposed labels exactly. The sentence still explains title, publisher, source and licence; creator/copyright and modification guidance remains intact.

- `Jóváírás másolása` → `Forrásmegjelölés másolása` (1 occurrence).
- `Jóváírások szerkesztése` → `Forrásmegjelölések szerkesztése` (1 occurrence).
- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence).
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L609); [Provider description display](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L75-L83); [Provider description mapping](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L8-L12).

### AN-W05-C05-HU-03 — `gallery_edit_credits`

**Supported contextual proposal.** The plural Forrásmegjelölések fits an editor containing the document's collection of attribution entries, even though one entry is selected at a time.

- `Jóváírások szerkesztése` → `Forrásmegjelölések szerkesztése` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L610); [Gallery edit action](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L105-L111); [Entry collection and picker](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L88-L100).

### AN-W05-C05-HU-04 — `gallery_credit_copied`

**Supported contextual proposal.** Forrásmegjelölés másolva is a concise, grammatically coherent success notice following successful clipboard publication.

- `Jóváírás másolva` → `Forrásmegjelölés másolva` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L611); [Clipboard success/error sequence](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L49-L58).

### AN-W05-C05-HU-05 — `gallery_credit_saved`

**Supported contextual proposal.** A forrásmegjelölés szövege mentve explicitly identifies the saved text. The singular possessive construction fits Save for the selected entry.

- `Jóváírási szöveg mentve` → `A forrásmegjelölés szövege mentve` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L618); [Selected-entry Save action](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L142-L145).

### AN-W05-C05-HU-06 — `ui_image_credits`

**Supported contextual proposal.** Képek forrásmegjelölései is a coherent plural collection label for the About entry, editor title, clipboard label and export disclosure. It also remains meaningful as the Commons loading-status prefix.

- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L328); [About chooser](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L869-L882); [Clipboard label](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L49-L51); [Editor title](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/GalleryCredits.kt#L131-L135); [Export disclosure](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/SaveOptionsDialog.kt#L122-L139); [Commons loading status](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L253-L263).

### AN-W05-C05-HU-07 — `ui_about_credits23`

**Supported contextual proposal.** Névjegy, licencek és forrásmegjelölések covers the actual source/author acknowledgements alongside licences. This contextual result must not be generalized to an unrelated contributor-list screen.

- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L133); [About chooser destinations](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L868-L883).

### AN-W05-C05-HU-08 — `ui_credits_terms`

**Supported contextual proposal.** Forrásmegjelölések és feltételek fits the provider-specific attribution/terms destination and preserves the separate terms concept.

- `Jóváírások és feltételek` → `Forrásmegjelölések és feltételek` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L228); [Terms action](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/MediaGalleryActivity.kt#L110-L111); [Provider destinations](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L8-L12).

### AN-W05-C05-HU-09 — `ui_icons_fonts_artwork_credits`

**Supported contextual proposal.** Ikonok, betűtípusok és alkotások forrásmegjelölései names attribution for the actual materials. The plural possessive ending fits the coordinated list. The destination independently supports source/copyright acknowledgements beyond gallery images.

- `Ikonok, betűtípusok és alkotások jóváírásai` → `Ikonok, betűtípusok és alkotások forrásmegjelölései` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L325); [Asset attribution and notice content](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/assets/legal/ASSET_CREDITS.txt#L1-L80); [Asset-notice action](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L874).

### AN-W05-C05-HU-10 — `ui_open_source_credits_and_notices`

**Supported contextual proposal.** Nyílt forráskódú összetevők forrásmegjelölései és közleményei supplies the subject, components, and coordinates their attributions and notices. The actual file identifies components, publishers, contributors and licences.

- `Nyílt forráskódú jóváírások és közlemények` → `Nyílt forráskódú összetevők forrásmegjelölései és közleményei` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L364); [Component inventory and notices](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/assets/legal/THIRD_PARTY_NOTICES.txt#L95-L108); [Notice title wiring](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L872).

### AN-W05-C05-HU-11 — `ui_gimp_translations31`

**Supported contextual proposal.** Fordítások forrásmegjelölései és licencei is supported because the destination documents reused translations' source, revision, translator/copyright headers and licences. It is not merely a list thanking current app contributors. Both possessive forms are aligned. Original headers and legal text must remain unchanged.

- `Fordítási jóváírások és licencek` → `Fordítások forrásmegjelölései és licencei` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L649); [Translation provenance and preserved headers](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/assets/legal/GIMP_TRANSLATION_NOTICES.txt#L1-L24); [Translation-notice action](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L875).

### AN-W05-C05-HU-12 — `ui_catrobat_s_own_artwork_uses_cc_by_sa`

**Supported contextual proposal.** The two substitutions update the literal About → Image credits path and leave existing creator-credit wording intact. This is retained Catrobat guidance: current Catrobat provider routing selects gallery_description instead. Static inspection did not establish this retained resource's live reachability.

- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence).
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L191); [Current provider routing](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L8-L12).

### AN-W05-C05-HU-13 — `ui_irasutoya_help34`

**Supported contextual proposal.** A forrásoldalak és forrásmegjelölések distinguishes retained pages from attribution records and retains suitable plural agreement. Both embedded navigation labels match. The financial 21-or-more-items/fee statement is unchanged.

- `A forrásoldalak és jóváírások` → `A forrásoldalak és forrásmegjelölések` (1 occurrence).
- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence).
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L670); [Irasutoya description mapping](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L10).

### AN-W05-C05-HU-14 — `ui_openclipart_help34`

**Supported contextual proposal.** Only the two literal navigation labels change. Openclipart, CC0, Large PNG and the source-page/licence semantics are preserved.

- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence).
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L671); [Openclipart description mapping](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/IllustrationSource.kt#L11).

### AN-W05-C05-HU-15 — `ui_help23`

**Supported contextual proposal.** The single About-label substitution remains grammatical before részt, matches the proposed menu label, and preserves all Commons/provider instructions. This is the actual main Help resource.

- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L545); [Main Help action](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1576).

### AN-W05-C05-HU-16 — `ui_add_up_to_20_images_with_android_s`

**Supported contextual proposal.** The refined sentence explicitly retains Catrobat/AGPL and uses a felhasznált elemekre vonatkozó forrásmegjelöléseket for asset attribution. Catrobat/AGPL-re and elemekre are compatible with vonatkozó; ugyanazokat … forrásmegjelöléseket preserves plural agreement. The About label remains exact.

- `Ez a mód ugyanazokat a Catrobat/AGPL- és eszközjóváírásokat használja, amelyek a fő szerkesztő «Fájl > Névjegy, licencek és jóváírások» paneljén szerepelnek.` → `Ez a mód ugyanazokat a Catrobat/AGPL-re és a felhasznált elemekre vonatkozó forrásmegjelöléseket használja, amelyek a fő szerkesztő «Fájl > Névjegy, licencek és forrásmegjelölések» paneljén szerepelnek.` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L149); [Assembly Help action](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/AssemblyActivity.kt#L341).

### AN-W05-C05-HU-17 — `ui_the_arrow_on_the_left_directly_below_the`

**Supported contextual proposal.** All Terms/About/Image credits references match the proposed labels. Forrásmegjelöléseiket refers back to the bundled fonts. A felhasznált elemek és betűtípusok forrásmegjelöléseit identifies asset/font attributions and takes the accusative required by tartalmazza. Static inspection found catalogue/test references but no direct production reference to this retained resource key; live reachability is not established.

- `Jóváírások és feltételek` → `Forrásmegjelölések és feltételek` (1 occurrence).
- `Névjegy, licencek és jóváírások` → `Névjegy, licencek és forrásmegjelölések` (3 occurrences).
- `Képjóváírások` → `Képek forrásmegjelölései` (1 occurrence).
- `jóváírásaikat` → `forrásmegjelöléseiket` (1 occurrence).
- `eszköz-/betűtípus-jóváírásokat` → `a felhasznált elemek és betűtípusok forrásmegjelöléseit` (1 occurrence).

Evidence: [pinned Hungarian resource](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/res/values-hu/strings.xml#L443); [Current main Help selects ui_help23](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/java/org/catrobat/paintroid/classic/ClassicPaintActivity.kt#L1576); [Font notice content](https://github.com/c933103/AN-Paint/blob/43148951ac6bd23687e66685855909ac538ba004/Paintroid/src/main/assets/legal/ASSET_CREDITS.txt#L78-L80).

## Checks performed and remaining limits

A read-only, in-memory check confirmed all 17 current values against the pinned Hungarian catalogue; exact declared replacements and occurrence counts; unchanged placeholder signatures and escaped-newline counts; Android string quoting and format contracts using the original `formatted` attributes; unchanged provider/licence literals; and exact agreement between every changed embedded label and its proposed resource. These are structural checks, not proof of linguistic quality.

No production resources were changed or runtime tests executed by this review. Android compilation, screen-fit/reachability tests, accessibility rendering and competent-language acceptance remain unestablished. The planned narrow/portrait/landscape/large-text checks remain necessary after C04 integration; in particular, the HU-10 title grows from 42 to 61 characters. No implementation PR, merge or deployment is part of this evidence publication.
