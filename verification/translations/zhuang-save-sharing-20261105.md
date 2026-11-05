# Zhuang saving and sharing

Base: `cdfce6b35785fdbeb85a3bfd555942de31629552` on `review/nv-bottom-2038-20261103`.

Adds two missing P0 strings: the Save and share menu caption and its dialog title. All 105 previous typed resources and attributes remain unchanged. No other locale, English text or implementation changes.

## Scope and review

Zhuang had the largest remaining direct P0 gap at this source checkpoint. Existing accepted Zhuang packets were reconciled against the current catalogue and were already present. Earlier save/share research was a nomination, not prior approval. This batch receives a new bounded linguistic and current-consumer review; it does not relabel other drafts or historical localization conclusions as accepted.

Independent review accepts the two captions at moderate compositional confidence. They coordinate saving and sharing with an explicit image object and preserve the menu ellipsis. Primary Zhuang prose supports the sharing lexeme and its digital use; a primary software description independently supports coordinated verbs with a common final object. Extending the sharing verb to Android ACTION_SEND is an authored functional use, not a claim of an attested complete software caption or public-posting-only meaning.

The accompanying saved-but-sharing-failed warning remains untranslated. Its proposed failed-inception/event-nominal clause was not established clearly enough by independent review. That is a narrow clause hold, not rejection of the sharing verb or a whole-language pause. The draft warning is excluded from the source; existing English fallback remains.

Current consumers were checked in `ClassicPaintActivity.kt` and `SaveOptionsDialog.kt`. The menu opens export-and-share options, the dialog uses its share title, output writing precedes sharing, and the exception handler surrounds FileProvider/intent/chooser setup. The export route does not mark the working document saved or change its normal save destination. These are static source checks, not executed Android behavior.

Linguistic sources: [sharing terminology](https://www.guangximinzubao.cn/szbzw/html/2024-07/17/content_50661.htm), [digital sharing context](https://www.guangximinzubao.cn/szbzw/page/21/2023-11/08/08/2023110808_pdf.pdf), [coordinated software actions](https://www.guangximinzubao.cn/szbzw/html/2024-11/06/content_51822.htm) and [Zhuang software saving vocabulary](https://github.com/wikimedia/mediawiki/blob/master/languages/i18n/za.json). Direct/indexed textual evidence was checked; no PDF-raster or native-speaker certification is claimed.

## Verification

- 78 affected host tests pass, covering current localization structure, formatting/legal boundaries, help routes, source recovery and priority accounting. This is an affected subset, not the entire repository suite.
- Structural validation passes for all 171 offered language options and the priority manifest.
- Four English/Zhuang Java resource-template checks pass; the two new keys are unique and missing-only, with exact source attributes, format slots, literals and valid Android/XML escaping. The caption pair differs only by its ellipsis.
- All 1,252 materialized base files match the freshly fetched remote tree's Git blob hashes and executable modes. Its 236 unmaterialized non-tree entries are retained unchanged.
- Direct presence becomes P0 51/94, P1 56/249, P2 0/305 and P3 0/71: 107 typed resources total. P0 gaps decrease from 45 to 43. Presence is not whole-catalogue linguistic acceptance.

No Android build, AAPT, device/layout test, hosted CI, native-speaker certification, merge or release is claimed. Publication uses the exact expected parent and a non-force branch lease, with final remote tree and changed-file verification. Canonical Android resources own the wording; no permanent sentence mirror or per-batch test package is introduced.
