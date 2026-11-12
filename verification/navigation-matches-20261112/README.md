# English-matching navigation review, 12 November 2026

Base: AN Paint develop `2b890631f5bc6e5da2c088a67b9cb3abe0931006`.

The 92 automated flags across 25 locales are review candidates, not 92 translation defects. All 92 have individual decisions in `review-ledger.json`:

- 40 retained shared terms have contextual catalogue or published lexical/usage support.
- Two Catalan/Valencian `El·lipse` entries are false positives caused by dropping the orthographic middle dot. Their resources remain unchanged.
- 50 entries remain unresolved: 47 Nigerian Pidgin, two Tok Pisin and one Cebuano technical term. No speculative replacement or native-speaker approval is claimed.

The proposed code correction preserves middle dots between letters while still ignoring surrounding punctuation and emoji decoration. The source-derived navigation inventory and fallback detection stay unchanged. The output becomes 90 flags across the same 25 locales. It does not hide valid shared words through a growing approval allowlist or add catalogue wording mirrors.

Validation: nine affected navigation tests and 19 priority-manifest tests pass; the old comparison fails the new letter-internal-dot negative control. A complete 171-locale navigation audit still finds all 71 keys present per locale, with zero unresolved aliases. Comparison of the two audit outputs shows exactly the two Catalan ellipse flags removed. All direct P0–P3 resource counts remain unchanged. Hosted exact-head CI and Codex review are required before merge.

No resource wording was edited. The 40 retained terms are an evidence-backed triage decision, not certification of entire languages. The unresolved English-lexified labels are not automatically defects. The separate fresh CI for #299 is development verification, not linguistic, exhaustive installed UI, speech, physical-device or release acceptance.

Supporting project catalogues and public sources are linked per entry. Dictionary/catalogue support establishes the relevant term, not every possible UI or spoken-language use.
