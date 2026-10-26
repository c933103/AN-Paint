# Danish and existing Norwegian catalogue: missing-only P0 candidates

**Author-candidate snapshot frozen at 07:47 UTC — no acceptance is conferred by this packet.** This is one shared source-context packet with separate locale judgments. Independent reviews are arriving separately after the freeze and will be published in their own version; the pending flags here describe the original proposals, not a live review-status dashboard. Application source is unchanged.

Pinned source: [`df9bc04b848ab5e99457bc67265d771bb839ec9d`](https://github.com/c933103/AN-Paint/commit/df9bc04b848ab5e99457bc67265d771bb839ec9d), tree `8ca5fc4f3989cf8c9307432d5e5c28ceef698251`. A fresh explicit `branches/develop` read matched that commit at 07:36 UTC on 26 October 2026; no completed CI monitor was reopened. The [171-option structural report](https://github.com/c933103/AN-Paint/tree/708bbaf18874b97815882adacadf4b7a73513a9e/records/localization-review/2026-10-26/nynorsk-p0-remaining/r06-merged-coverage) supplied the gaps; the [prior current-value review ledger](https://github.com/c933103/AN-Paint/tree/cdc469f0005ebbfeecfded45722f360119425a20/records/localization-review/2026-10-26/current-language-coverage/r02) supplied existing evidence classifications.

## Why these two catalogues

Danish (`da`) and the existing Norwegian catalogue (`no`, unchanged identity) each have **83 missing P0 values out of 92** and an established catalogue foundation: 127 Danish and 115 Norwegian values. Existing Save/Cancel/menu/image/canvas/selection terminology supports bounded, source-first candidate drafting with independent review. Selection is based on substantial gaps, relevant terminology and reusable verified consumer context—not popularity or an assumption that English-identical strings are wrong.

The current-value ledger documents no independent whole-value P0 scopes for either locale. Existing text is consistency context, not proof of linguistic acceptance. Every existing value and attribute remains untouched, including both Save confirmations and the actual `Image format` value. No locale-code retagging is proposed.

## Concrete scope

| Group | Per locale | Both locales |
|---|---:|---:|
| 01 Import and format explanations | 13 | 26 |
| 02 Recovery and autosave | 28 | 56 |
| 03 Assembly and memory | 16 | 32 |
| 04 Save/share and image credits | 21 | 42 |
| **Total** | **78** | **156** |

The same 78 source identities are missing in both catalogues. Five more missing P0 identities per locale stay held: `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, `ui_save_as_png`. A source-bound scan of all 322 tracked production Kotlin/Java/XML files found no direct `R.string` reference or XML alias for those identities. This is a bounded static observation, not proof that they can never be used or that absence is defective.

All five Nynorsk holds, prior accepted/qualified/author-only/historical/clause-only/unmatched/synthetic evidence, PR56 never-merge, PR159 freeze, PR113 held/retarget scope, Help callback/archive identity, interrupted report archive and release pauses remain unchanged.

## Review the actual compositions

Each locale/group file includes complete source/target pairs, XML attributes, numbered placeholders, display and encoded-text hashes, context IDs, source-semantic notes, author uncertainties and pending status. `shared-source-context.json` binds 323 source inputs and 140 exact consumer windows; every reused line window and source hash was revalidated at the current pin. It contains no inherited translation acceptance. `terminology-foundations.json` includes every existing value and attribute for consistency/preservation checks.

Important boundaries:

- Animation counts can contain the unchanged English `at least %1$d` qualifier. This mixed composition must not be called fully localized.
- Recovery instructions must use the actual `Filer`/`Fil`, `Gem som…`/`Lagre som…`, `Image format`, and untouched `Load image…` labels. A proposed recovery action is a within-group dependency, not prior acceptance.
- `canvas.png`, ZIP, PNG / JPEG and one optional floating selection are literal/model constraints. This recovery archive is not the paused Help callback/archive work.
- Export can successfully create a file while retaining the drawing's dirty state and Save destination. Save, export, sharing, autosave draft and assembly output outcomes must remain distinct.
- The P0 assembly-memory warning is a single-key proposal. Its P1 companion remains missing/unreviewed; the 120-entry/60-tag paired-warning oracle and frozen history must remain unchanged.
- Technical terms for frames, recovery copies, undo cache, assembly, sampled decoding and credit attribution are explicitly open to full-value independent revision or hold. No dictionary or related-locale acceptance substitutes for that judgment.

## Verification and next steps

Run the data-only verifier against the pinned source checkout:

```sh
python3 verify_candidates.py --source-root CHECKOUT --packet PACKET_DIRECTORY
```

It independently checks DOM resource values/attributes, Git/SHA-256 identities, exact source windows, complete missing-only identity sets, held absences, placeholders, candidate Android encoding, current command-label compositions and preservation of all 242 existing locale values. `verification.json` records the actual checks. This validates structure and selected composition tokens, **not full linguistic acceptance**.

Independent reviewers must give a separate full-value verdict for each locale/identity, retaining all qualifications. Only final reviewed values can proceed to an implementation manifest. A later combined reviewed source/test PR can share CI while keeping locale-specific resource/behavior checks, exact-head review and postmerge evidence separate. No application mutation, build, runtime execution, native-human, physical-device, layout or whole-language certification is performed by this packet.
