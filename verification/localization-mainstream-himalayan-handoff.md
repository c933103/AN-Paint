# Mainstream and Himalayan localization handoff repair

Reviewed against published integration `7939f1292`, 25 September 2026.
This records concrete follow-up to the recovered conversation handoffs. It does
not treat a previous assistant's completion statement, 669 resource entries, or a
passing build as proof of linguistic accuracy.

## Recovered obligations and findings

| Thread / obligation | Evidence in the published tree | Repair |
| --- | --- | --- |
| English variants, Portuguese, Italian, Greek, Turkish: the 23 September 03:02 handoff deliberately left the default language-information note unchanged | Default English still claimed to reuse Paintroid translations; Arabic, Spanish, French, German, Russian, Esperanto, Tibetan, Dzongkha, both Mongolian scripts and vertical test catalogues retained it too | Corrected the stale assertion in 14 catalogues; retained the accurate English-fallback information. Existing regional catalogue maintenance notes remain. |
| Both mainstream waves: review inherited instructions, not only resource coverage | The ambiguous source phrase “Show all changes zoom” became a nonexistent “Show all changes” button in 11 translations | Clarified both English help resources and their variants; aligned translated references with `ui_show_all`. Brazilian Portuguese already had the correct button name. |
| Arabic plural review | Zero, one and two described `%3$d` as an original total, although the argument is the number of affected images | Replaced those clauses with an explicit affected-image count; all six quantity forms and all three arguments remain. |
| Tibetan, Dzongkha, both Mongolian catalogues: complete meaning review | Legacy instructions still described a generic Menu and directed users to Help for copyright/source | Removed the obsolete Menu clauses; used the current File → About panel; retained bounded-panel scrolling, first-launch state and landscape layout clauses. |
| Dzongkha: independent terminology and omitted clauses | Wrong Draw/Drawing route, abbreviated or mismatched live captions, omitted location of Advanced, omitted Save destination, omitted save-before-sharing statement in the long manual | Corrected those instructions, kept Dzongkha wording distinct from Tibetan, and restored the missing clauses. The original Keep editing correction already existed; it was not counted as newly repaired. |
| Gallery credit instructions | Tibetan and Dzongkha omitted the retained-source route; traditional Mongolian also omitted editing credit details | Added those clauses to `gallery_description` with exact live captions. Existing licence/creator/edit-notice clauses remain. |
| Shared source and all owned manuals | Legacy manuals described insertion through an obsolete command and assembly under File or View | In 26 catalogues, documented Draw → Insert → Other images, device/Catrobat/Irasutoya/Openclipart selection and Use image, and File-only image assembly. Memory limits, original resolution, resizing and unchanged originals remain. |
| Active help consistency | Source English and translated `ui_help23` abbreviated Swap colors and Fit image to canvas; several also named different About or Other images captions | Aligned the live help with those actual captions. English variants and the vertical test catalogues use their own labels. |

## Source checks

The route/behaviour source is `ClassicPaintActivity.kt`: `menuActions("File")`
contains assembly and About; `menuActions("View")` does not contain assembly;
the Insert category opens `showOtherImages()`, which offers device files and the
three illustration sources. The real `ui_draw_again` button is still used by the
app, so its navigation references were retained. The independent fixed Copy all,
Other terms and Done buttons remain implemented in `LegalInfo.kt`.

The crop count was checked at the `getQuantityString(ui_crop_preview_images, …)`
call: the third format argument is affected count, not total input count.

Dzongkha `save20_dither` previously used the progressive phrase `སྤར་དོ།`.
The edited control uses `ཚོས་གཞི་སྤར་བ།`, a colour-specific nominal label. The
DzongkhaLinux team's *Dzongkha Computer Terms*, printed page 56 / PDF page 60,
gives `སྤར་བ།` for dithering. The page was rendered and visually checked because
text extraction omitted the stacked consonant. Search snippets also returned
conflicting corrupt OCR and were not accepted as the spelling source.

- Publisher distribution: https://download.savannah.gnu.org/releases/dzongkha-gnome/dzongkha_computer_terms.pdf
- PDF SHA-256: `b55983944fc94c0ada076947ba85bccfe4242728a531706ad92f894bf097005b`
- Primary project translation corroboration: https://sources.debian.org/src/gimp-gap/2.6.0%2Bdfsg-1/po/dz.po/ (`Floyd-Steinberg Color Dithering` uses the same technical root, with a progressive form in that sentence).

## Verification and scope

The 27 host translation tests pass after these repairs. Strict SDK 35 AAPT2
compilation of the entire `Paintroid/src/main/res` tree also passes. These changes
edit canonical Android XML directly. No translation generator or automatic
first-dictionary-reading conversion was introduced.

This pass reviewed the reported handoff gaps, active help, long manuals, assembly
instructions, language notes, Arabic crop counts and the identified Dzongkha term.
It is not an independent native-speaker certification of every entry in all
26 catalogues. Shared gallery-route repairs and global regression tests are
maintained separately in the integration change.
