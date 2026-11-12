# Navigation language review, 12 November 2026

Source: AN Paint develop `0417bd8af2b411ff800ee27889a02276c0439bdc`.

This reviews all 50 language candidates left open by PR #437, using complete resource values, the actual menu/tool consumers, independent AI language review, and targeted published usage. It does not review entire catalogues or certify native fluency.

## Decisions

- Retain 46 Nigerian Pidgin labels as suitable shared vocabulary or technical terms under the catalogue's existing orthographic convention. English spelling equality alone is not a defect. These are contextual AI judgments, mostly medium confidence, not 46 new dictionary attestations.
- Retain Cebuano `Airbrush`. A genuine Cebuano artist interview published by Banat supports the borrowing; the actual tool sprays colour. An adapted alternative spelling does not make the retained form wrong.
- Clarify Nigerian Pidgin `Navigate` as `Move / zoom di view`.
- Localize Tok Pisin `Drawing` as `Droim` and `Navigate` as `Zum na muvim viw`.
- Update the two dependent canvas accessibility instructions so their named mode matches the caption. Two-finger zoom/pan and one-finger view movement remain distinct; no movement of image pixels is implied.

The complete 50-entry decisions, confidence and source limits are in `review-ledger.json`. The 47 retained entries remain visible to the generic English-match audit; no allowlist or audit suppression was added. The audit becomes 87 candidates across 24 locales. Review disposition is recorded here rather than encoded as a runtime wording mirror.

## Validation

Only five values in two existing XML files changed. All other XML nodes/attributes/order and all other 1,289 source leaves/modes remain unchanged. The existing 63 affected host tests pass. A first post-edit command ran from the wrong directory and could not import its four modules; the corrected repository-root invocation passed. The failure is not counted as a product-test pass.

All 171 offered choices retain all 71 direct navigation keys and zero unresolved navigation aliases. Direct P0/P1/P2/P3 coverage is unchanged at 92,105/122,949; 65 catalogues are key-complete and 106 partial. See `validation.json` for the exact counts and changed blob identities.

No permanent sentence fixtures or per-edit test package was added. Existing current-resource, source-derived navigation and actual consumer checks are reused. Hosted exact-head Android/JVM/lint/device CI and Codex review remain required before merge. No installed-layout, speech, physical-device, native-human or release acceptance is claimed.
