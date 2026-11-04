# Saved colours and palette slots: Old English and Old Norse

Base commit: c7b87f447a2ff501c11562944aa0bbeab16b1106.

Adds 18 previously absent P2 strings to each offered `ang` (Ænglisc) and `non` (Norrœna) catalogue. Independent semantic review accepted all 36 after two Old Norse word-order corrections that clarify the colour being added. The batch covers saved/custom-colour labels, add/edit/remove actions, full-palette replacement, numbered empty/selected/stored slots and save feedback.

The translations preserve add versus replace versus remove, the current active colour versus a stored colour, tap/use versus hold/replace, choosing the save location versus saving, and the sequence of using a stored colour, adjusting it and explicitly saving changes. Dynamic slot-number and colour-description arguments retain their exact roles. The replacement instruction matches the beginning of its translated dynamic button caption. Status strings do not turn pending actions into completed saves.

The current AdvancedColourDialog and ClassicPaintActivity palette consumers were inspected for context. Some retained source resources have no current production callsite; this is catalogue coverage, not a claim that every label is currently displayed. Application behavior is unchanged.

Validation passed:
- Exact English and target base Git identities; offered picker entries; XML parsing and duplicate-name checks; exactly 18 additions per locale; all 355 previous entries, attributes and surrounding bytes unchanged.
- Android escaping and formatting, typed placeholder sequences, escaped-newline parity and source attributes.
- 78 host tests: test_translations, test_localized_help, test_translation_boundaries, test_current_localization_contracts, test_language_translation_note, test_string_importance, test_ordinary_priority_followthrough and test_open_review_recovery.
- Structural catalogue validation passed for all 171 offered options. All 1,276 materialized tracked base files matched their Git blob identities and executable modes. The 157 unmaterialized research/verification documents are retained unchanged in the publication tree and were not needed by these checks.

Each locale changes from P2 12/305 to 30/305, leaving 275 P2 keys absent. P0 remains 94/94, P1 249/249 and P3 0/71. These are direct-key-presence counts, not whole-catalogue quality ratings. The priority manifest is unchanged.

Vocabulary follows the current colour, palette, save, edit, remove, replacement and touch-gesture resources. Custom colours are expressed as the user's colours. Slots use Old English stow and Old Norse reitr. [Bosworth-Toller, ecan](https://www.germanic-lexicon-project.org/html/oe_bosworthtoller/b0238.html) supports the added-status participle; [Zoëga, reitr](https://norroen.info/dct/zoega/r.html) gives a marked-out space or board square. Technical compounds and UI adaptations are not claimed historical computing terms or full-sentence attestations.

Limits: no historical-language specialist certification, whole-catalogue linguistic acceptance, Android build, device/rendering check or CI result is claimed. Canonical Android resources own current wording; this evidence is not a wording freeze.
