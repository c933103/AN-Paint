# 171-option language coverage — current results, partial evidence publication

**Source pinned to merged `develop` commit [`d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4`](https://github.com/c933103/AN-Paint/commit/d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4).** The complete [previous r01 report](https://github.com/c933103/AN-Paint/tree/0d47f7df077836f2d0d4eb2394485dc19e262f75/records/localization-review/2026-10-25/current-language-coverage/r01) is preserved.

**This revision publishes the complete current 171-option CSV/JSON and source-bound findings, but not the compressed source/evidence archive set.** The calculations and receipt matching are verified; publication of the full offline reproduction packet is incomplete. `publication-status.json` explicitly lists omitted files. `full-package-manifest.json` identifies the original complete staged packet; it is **not a claim that all listed files are present here**. `manifest.json` lists only files actually included in this partial revision.

## Current result

| Metric | Previous `393f2804` | Merged `d0e4a386` | Change |
|---|---:|---:|---:|
| Typed containers present | 49,726 | **50,469** | +743 |
| Typed containers missing | 72,881 | **72,138** | −743 |
| P0 gaps | 9,536 | **9,286** | −250 |
| P1 gaps | 23,050 | **22,557** | −493 |
| Canonical leaves present | 49,760 | **50,503** | +743 |
| English-identical leaves | 7,039 | **7,051** | +12 |
| Source-different leaves | 42,721 | **43,452** | +731 |

Denominators remain **171 options × 717 typed containers**, and **171 × 718 canonical leaves**. All three priority locales now have **92/92 P0 and 249/249 P1 containers present**:

- Amharic: 369 containers present, 348 missing; 249 added and 3 replaced.
- Bulgarian: 365 present, 352 missing; 238 added and 14 replaced.
- Bengali: 359 present, 358 missing; 256 added and 27 replaced.

The three crop `other`-leaf wording changes do not change presence. All 790 added/changed container identities and exact hashes are in `source-delta.json`. **59** options have full container presence and **31** zero container presence, unchanged. Presence, English identity and source difference are not authorship or acceptance judgments. Plural-container presence does not imply all canonical leaves are present; only canonical leaves enter the leaf denominator.

## Evidence categories and preserved limits

All **13,898 prior evidence-union source/target pairs are exact and unchanged**. None of their original scopes is revoked. The inventory retains **4,754 prior independent bounded whole-value scopes**, including 29 synthetic fixture scopes; **8,181 author-only** scopes; and **963 historical scoped** records whose individual accepted, comparison, partial, proposal and context/provenance limits remain as in r01.

The immutable [BG/BN/crop receipt](https://github.com/c933103/AN-Paint/blob/d6f6640ae3d36d53c1986d0b1ceccf1f58be80a8/verification/translations/bg-bn-crop-20261026/reviewed-wording.json) and [Amharic receipt](https://github.com/c933103/AN-Paint/blob/f0df28ca2e449c2cdc946e6136f9c96dd866fd0f/records/localization-review/2026-10-25/amharic-priority/r01/independent-review.json) match **937 new scalar whole-value scopes**: **847 bounded static-context** and **90 explicitly source-only-qualified**, with **zero overlap** with the earlier identity union. **Three further qualified crop scopes cover only the complete `other` value, not all plural leaves.** Their idiom/orthographic qualifications remain.

Five explicitly accepted Amharic carries absent from r01's independent inventory—`ui_category_selection`, `ui_eraser`, `ui_pencil`, `ui_preview`, `ui_text`—are retained as **prior accepted-carry attestations, not new independent reviews**. All 86 accepted priority carries remain excluded from the new 255-entry review. The resulting **14,843-identity mixed inventory is not an acceptance or completion total**. Fourteen current-exact clause-only scopes remain separately visible and non-additive; fragments do not become complete Help acceptance.

All **4,754 prior independent hashes** and **940 new receipt bindings** matched. Across the complete earlier union, 13,083 identities match a selected published pair digest; 815 author-only rows lack a pair digest in the selected published object and retain their exact source/value continuity and prior status. The original 9,465 mixed historical identities remain preserved, including 44 synthetic conventions; no new historical reconstruction or blanket re-review requirement is imposed.

## Verification and available files

All **176 counting inputs** (174 catalogues, option list, priority map) were raw-byte verified. The complete `f942` → `d0e` tree delta has 13 blobs; only the Amharic catalogue changes among those inputs. **175 inputs reuse exact `f942` bytes.** Canonical English, the option list and the tier map match the earlier snapshot. Independent DOM-based calculation agrees with all totals; full Git-tree reconstruction and five malformed-input guards pass. These are data-only report checks, not application tests or linguistic judgments.

- `per-locale-final.csv` / `.json`: all 171 options and exact evidence categories.
- `summary.json`: complete metrics, explicitly marked partial publication.
- `source-provenance.json`, `source-delta.json`: source/review identities, all input hashes and exact changes.
- `accepted-carry-reconciliation.json`, `clause-current-binding.json`, `clause-only-receipts.json`: narrowly preserved scopes.
- `verification.json`, `independent-verification.json`: checks actually completed against the full staged source/evidence inputs, not a claim that those inputs are all included here.
- `publication-status.json`, `manifest.json`, `full-package-manifest.json`: clear separation between published files and omitted complete-packet files.

Amharic postmerge CI is outside this report's pass claims and is handled separately. **#56 remains never-merge; #159 frozen; #113 retarget/held-warning scoped.** Help/archive, Hakka PFS/crop, synthetic and release limits remain. No whole-language, native-reader, physical-device, layout, rendering, accessibility-output or release certification. No application, `develop` or `main` changes.
