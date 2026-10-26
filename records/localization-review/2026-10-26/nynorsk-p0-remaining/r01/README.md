# Nynorsk: remaining 77 absent P0 values — candidate packet r01

Pinned source: **857a20103285a77846e340b326667c15a402ff9e** on `develop`, tree `6bb4fa11534149df7f8f58cb3d21faf2b802089f`.

**72 author proposals, 5 explicit holds; pre-review candidate snapshot.** Subsequent independent decisions are separate receipts; this immutable candidate packet is not updated into acceptance. Absence is a structural observation, not a defect verdict. None of the existing 118 values is replaced. The earlier eight reviewed whole values retain their bounded qualifications; the other existing 110 are terminology context, not newly accepted by this packet.

| Group | Proposed values | Review file |
|---|---:|---|
| Import and format explanations | 14 | `group-01-import-format-candidates.json` |
| Autosave, recovery and undo | 28 | `group-02-recovery-candidates.json` |
| Assembly, memory and destructive actions | 16 | `group-03-assembly-memory-candidates.json` |
| Save/share errors and credit preservation | 14 | `group-04-save-credit-candidates.json` |

`scope-and-holds.json` lists all 77 absent identities. Five remain held with no candidate: `formats22_derived_exported`, `ui_save_as`, `ui_save_as_jpeg`, `ui_save_as_jpeg_xl`, `ui_save_as_png`. No current production reference or resource alias was found; this is not proof of permanent unreachability and not a linguistic rejection.

## Review boundaries

Review each complete source/target pair with its exact consumer windows. Return accept, revise (exact full final string), or hold per identity; include uncertainties and the candidate-file hash. Do not infer approval from author confidence, extraction, dictionary words, or another language. No native-human, device, layout, whole-language, or runtime certification is claimed.

Important compositions are explicit in the groups:
- Animation count `%2$s` may include the unchanged English `at least %1$d`; this remains mixed-language and outside scope.
- Recovery instructions use the actual `Fil > Load image…` menu path, not an invented Nynorsk translation of an absent P1 action. Other quoted commands must match final reviewed proposed labels.
- Autosave draft status is not explicit Save; exporting or sharing a copy need not change the Save destination or clear unsaved drawing state.
- The assembly warning is the corrected estimated combined-peak warning, not a decoder-only impossibility claim. Its missing P1 companion is **not** proposed or accepted here. Paired-warning test accounting needs a narrow, truthful implementation design.
- Recovery-copy, assembly, floating-selection and attribution terminology are proposals requiring judgment. Exception placeholders may contain untranslated details.

`canvas.png`, ZIP, PNG, JPEG, sRGB, PDF, AN Paint, Android, format tokens, numeric precision and `formatted=false` remain product contracts. The draft-recovery ZIP instruction is not the separately paused Help callback/archive-identity work.

PR56 never-merge, PR159 freeze, PR113 retarget/held work, Help callback/archive identity and release pause remain unchanged. No archive upload retry or application change is part of this record.

## Inspect and reproduce

Every group contains full source and candidate values, attributes, SHA-256 value hashes, production consumer windows, and all untouched Nynorsk terminology. `source-provenance.json` binds exact source files by Git blob and SHA-256. The source tree has 171 picker options, 717 containers and 718 leaves; Nynorsk has 118 present values and 77 absent P0 values before any proposal.

Run `python verify_candidates.py --source-root CHECKOUT --packet .` against the pinned source checkout. The validator separately parses XML with DOM, derives the missing P0 set, recomputes every current consumer and context, checks placeholders and hashes, verifies all bound files with `git hash-object --stdin`, and guards manifest/privacy assertions. It does not decide linguistic correctness. See `validation.json` for actual validation results and `implementation-test-plan.md` for gated next steps.

## Narrow lexical background, not sentence acceptance

- [Nynorskordboka: utkast](https://ordbokene.no/nn/86134) supports the noun used for draft.
- [Nynorskordboka: montasje](https://ordbokene.no/nno/nn/montasje) supports assembly/combined-image terminology; the proposed UI compound still needs contextual review.
- [GIMP Nynorsk dashboard](https://docs.gimp.org/nn/gimp-dashboard-dialog.html) uses `mellomlager` for a cache. It does not establish this app’s behavior or approve these complete strings.

No dictionary or external documentation supplies whole-value acceptance. Historical GIMP terminology and earlier accepted values must not be silently promoted to a new native review.
