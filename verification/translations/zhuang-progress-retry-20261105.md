# Zhuang operation progress and retry notices

Base: `dfc9acb74a34666fd4b64ff8e8919093e381be1d` on `review/nv-bottom-2038-20261103`.

Adds six missing P1 resources: ongoing autosave, generic working status, wait and retry instructions, generic operation failure and an edit failure with diagnostic detail. All 130 previous typed resources and their attributes remain unchanged. Only the Zhuang catalogue and this report change.

## Wording and independent review

All six final entries received an independent linguistic and current-consumer review at moderate compositional confidence. The initial autosave wording merely named an automatically saved file. Review identified a possible ambiguity with ordinary document saving; the final wording explicitly says the ongoing automatic saving is for recovery. The purpose clause does not assert that recovery has happened or will succeed. The other five proposals were retained.

The progress notices describe ongoing work, not completed operations. The retry instruction asks the user to do the requested action again, without promising success. Failure wording is generic enough for editing, assembly placement, clipboard and credit export; it does not promise rollback or unchanged data. The edit diagnostic remains the original single `%1$s` argument, including when the caller substitutes the retry instruction.

Primary prose supports [ongoing action and repeated action](https://www.guangximinzubao.cn/zw/f_282584/646040.html), [waiting and the task/matter noun](https://www.guangximinzubao.cn/szbzw/html/2019-11/06/content_33679.htm), [negative ability with doing](https://www.guangximinzubao.cn/szbzw/html/2024-01/17/content_49035.htm) and [changing](https://www.guangximinzubao.cn/szbzw/html/2025-08/27/content_54391.htm). [Agency prose](https://www.guangximinzubao.cn/szbzw/page/21/2024-02/07/06/2024020706_pdf.pdf) also uses again + do + an action object. [Bilingual mechanical-action prose](https://www.guangximinzubao.cn/sy/mzwx/378147.html) supports automatic action. [Fronted purpose](https://www.guangximinzubao.cn/szbzw/html/2017-12/27/content_24066.htm) and [restoring a nonhuman condition](https://www.guangximinzubao.cn/szbzw/page/21/2023-11/29/03/2023112903_pdf.pdf) support the revised recovery-purpose construction. These sources were reread for this batch; PDF text was read, not raster-certified.

[MediaWiki's Zhuang resources](https://raw.githubusercontent.com/wikimedia/mediawiki/master/languages/i18n/za.json) corroborate technical editing and the digital save predicate. Its mixed English subject in the saved confirmation is not Zhuang sentence-structure evidence. The software clauses are authored compositions and semantic extensions, not attested complete quotations or native-speaker certification.

## Consumer and targeted verification

- `ClassicPaintActivity.updateStatus` selects autosaving only under busy + autosaving; otherwise it selects generic working. `saveDraftIfReady` sets autosaving before writing the recovery state, clears it afterward, and separately selects success or failure. The wait instruction also appears during startup and when busy actions are blocked.
- Startup failure and `editFailed` format the edit-failure message with the actual exception detail or retry fallback. Generic failure is also used by `AssemblyActivity`, `AssemblyPlacementDialog`, `LegacyImageCreditsActivity` and `GalleryCredits`; generic working is used during assembly work and legacy-credit export. These are static current-source checks, not executed Android flows.
- 77 affected Python host tests pass: current localization contracts, translations, translation boundaries, priority accounting, localized help and save/export help. All 171 offered catalogues and the priority manifest pass structural validation. This is a targeted subset, not the full suite.
- Twelve English/Zhuang Java template render checks pass, including exact diagnostic substitution with percent signs, angle brackets, ampersand and quotes. Missing-only additions preserve source attributes, ordered typed arguments, XML/Android escaping and all earlier resource values.
- The freshly fetched base tree matches all 1,252 materialized files' Git hashes and executable modes. Its 243 unmaterialized non-tree entries are retained. Publication uses the exact expected parent and a non-force lease, followed by complete remote-tree and changed-file verification.

Direct presence becomes P0 66/94, P1 70/249, P2 0/305 and P3 0/71: 136 typed resources. Across 171 offered options, P1 gaps decrease from 1,427 to 1,421; other tiers and the 46 options with all tracked resources are unchanged. Presence is not whole-catalogue linguistic acceptance or runtime fallback coverage.

No Android build, AAPT, installed rendering, device/accessibility execution, merge or release is claimed. Some non-scrolling status layouts allow two lines in 44dp; the longer working and recovery-saving labels therefore have a specific unresolved fit risk. No sentence mirror, permanent per-batch test package or runtime implementation change is added.
