# Zhuang image-credit failure and retention notices

Base: `e4028a6f222941c618f45912c7bdfee7c41b30de` on `review/nv-bottom-2038-20261103`.

Adds two missing P0 notices: image credits that could not be saved or restored, and partially unreadable saved credit records whose stored copies are retained. All 121 previous typed resources and attributes remain unchanged. No implementation, default English, other locale or font changes.

## Meaning and independent review

Both complete values received independent linguistic and current-consumer review at moderate compositional confidence. Historical draft packets were treated as nominations, not approvals. The quoted category matches the current English fallback heading, `Image credits`; this is an explicit displayed-label reference, not a claimed Zhuang translation of attribution. A later translation of that heading must update these two references coherently.

The first notice reports a save/restore error, continued existence of previously stored credit data, and a retry instruction. Its diagnostic heading covers the current session-create/reopen, editor-construction, resource-refusal, draft-persistence and guarded returned-edit paths. It does not claim that both saving and restoration failed in every case, that a new save succeeded, that an unfinished field is durably saved, or that retry is guaranteed to succeed.

The second establishes saved credit data as its topic, says some cannot be read, and states that the data remains present. The bare-some construction has primary inanimate-predication evidence; the patient-negative construction preserves the unreadable records as the object of reading. Current `ImageCreditArchive.contents` counts unreadable snapshots without deleting original files, and `LegacyImageCreditsActivity` displays this warning only for a nonzero unreadable count. This is not a claim of universal corruption, complete recovery or creation of new copies.

Source evidence includes [official digital-data terminology](https://www.guangximinzubao.cn/sy/jxzw/412847.html), [temporal still-existence](https://www.guangximinzubao.cn/zw/y/377700.html), [bare inanimate some](https://www.guangximinzubao.cn/szbzw/html/2024-05/08/content_49809.htm), [nonhuman restoration](https://www.guangximinzubao.cn/szbzw/page/21/2023-11/29/03/2023112903_pdf.pdf), [textual reading](https://www.guangximinzubao.cn/szbzw/page/21/2025-10/01/05/2025100105_pdf.pdf) and [Zhuang patient-negative grammar, section 3.3.2](https://www.researchgate.net/publication/300848712_6_Zhuang_A_Tai_language_with_some_Sinitic_characteristics_Postverbal_'can'_in_Zhuang_Cantonese_Vietnamese_and_Lao). These support bounded authored digital compositions, not attested whole software sentences. Direct/indexed text was inspected; no PDF-raster or native-speaker certification is claimed.

`gallery_credit_too_large` remains English fallback. Its prospective restoration-size limit and preservation of the previous drawing must not be replaced with a generic oversized-image or already-damaged-file assertion. Other unsupported warnings also remain untranslated.

## Verification

- 78 affected host tests pass: current localization/formatting/legal boundaries, help and protected-draft routes, priority accounting and translation boundaries. This is an affected subset, not the full repository suite.
- All 171 offered language options and the priority manifest pass structural validation. Two unique missing-only additions preserve all source attributes, placeholder contracts, Android/XML escaping and old resources.
- Four English/Zhuang Java resource-template checks pass. The two exact reviewed values and quoted current heading were compared with the integrated XML.
- Current static checks confirm the editor error/success separation, session validation and durable write before in-memory acceptance, archive read-failure retention and nonzero unreadable-status condition. These are source checks, not executed Android credit-lifecycle tests.
- All 1,252 materialized base files match the freshly fetched remote tree's Git blob hashes and executable modes. Its 240 unmaterialized non-tree entries remain unchanged.
- Direct presence becomes P0 65/94, P1 58/249, P2 0/305 and P3 0/71: 123 typed resources total. P0 gaps decrease from 31 to 29. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, device/layout test, hosted CI, native-speaker certification, merge or release is claimed. Publication uses an exact expected parent and non-force lease, followed by full remote-tree and changed-file verification. Canonical XML owns current wording; no permanent sentence mirror or per-batch test package is added.
