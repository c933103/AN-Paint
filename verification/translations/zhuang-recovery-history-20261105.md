# Zhuang draft preservation and history recovery

Base: `c0eccc5165bf0e967eea9e7821257274f13b579b` on `review/nv-bottom-2038-20261103`.

Adds four missing P0 notices: failure to move the previous draft aside, failure to preserve it separately, damaged Undo data, and restored canvas with unreadable history and a retained recovery copy. All 117 previous typed resources and attributes remain unchanged. No implementation, English resource, other locale or font changes.

## Meaning and independent review

The complete values received independent linguistic and current-consumer review at moderate compositional confidence. Earlier research packets were nominations, not approvals. The damaged-cache nomination was corrected from a generic error to explicit damaged-data wording. The damage predicate has primary bilingual technical-hardware usage; applying it to stored data is a disclosed semantic extension, not an attested full software sentence.

The two preservation failures remain distinct. `AutosaveStore` reports the move notice when the source is missing or a same-directory rename fails; the contextual translation describes the unsuccessful filename change. Separate preservation copies raw bytes into a new `AtomicFile`; its failure notice describes inability to store the old file's data in a new file. Neither clause claims source deletion, restored pixels, verified recoverability or a successful backup.

The partial-history notice separates completed canvas restoration, inability to read saved Undo data, and completed storage of the previous draft's data in a separate recovery file. `EditorDraftRecovery` emits it only after the preservation call returns. It does not claim the history was repaired or that every recovered state is intact. It remains distinct from the newer unverified-recovery notices, which this batch does not translate.

Quoted Undo references match the actual Android-decoded Zhuang command, `siu`. Damage errors in `RasterHistory` cover hash, header and dimension checks. The optional trailing-data draft remains excluded: merely saying too much data could be mistaken for a storage/memory-capacity limit rather than unexpected extra payload. Other unsupported warnings retain English fallback.

Source evidence includes [the damaged-network-card predicate](https://www.guangximinzubao.cn/szbzw/page/21/2024-10/23/03/2024102303_pdf.pdf), [official digital-data terminology](https://www.guangximinzubao.cn/sy/jxzw/412847.html), [active change-failure grammar](https://www.guangximinzubao.cn/szbzw/html/2025-08/27/content_54391.htm), [storage-location ordering](https://www.guangximinzubao.cn/zw/l/381421.html) and [restoration of a nonhuman state](https://www.guangximinzubao.cn/szbzw/page/21/2023-11/29/03/2023112903_pdf.pdf). Direct/indexed textual support and authored technical extensions are distinguished; no PDF-raster or native-speaker certification is claimed.

## Verification

- 78 affected host tests pass: localization structure, current formatting/legal boundaries, help and protected-draft routes, priority accounting and translation boundaries. This is an affected subset, not the full repository suite.
- All 171 offered language options and the priority manifest pass structural validation.
- Eight English/Zhuang Java resource-template checks pass. Four unique missing-only additions preserve source attributes, formatting and Android/XML escaping; the partial-history notice retains `formatted="false"`. Exact reviewed values and quoted command references were checked.
- Current source checks confirm the missing-source/rename versus raw-copy branches, canvas-before-history recovery order, notice-after-copy ordering and all three damaged-data callers. These are static checks, not executed Android recovery tests.
- All 1,252 materialized base files match the freshly fetched remote tree's Git blob hashes and executable modes. Its 239 unmaterialized non-tree entries remain unchanged.
- Direct presence becomes P0 63/94, P1 58/249, P2 0/305 and P3 0/71: 121 typed resources total. P0 gaps decrease from 35 to 31. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, device/layout test, hosted CI, native-speaker certification, merge or release is claimed. Publication uses an exact expected parent and non-force lease, followed by full remote-tree and changed-file verification. Canonical Android XML owns current wording; no permanent sentence mirror or per-batch test package is added.
