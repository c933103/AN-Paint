# Current Swedish catalogue evidence

Current source baseline: `d7436b3df842b9be9aa12be622ebc88ed8e8e2b9`.

The original independent review is preserved unmodified in `README.md` and
`independent-review.json`. It accepted 373 new current-source entries and
preserved 340 earlier bounded entries without new linguistic review. It also
independently read and accepted the complete corrected assembly Help proposal
relative to its explicit proposed English source, while holding released-source
binding until that source was integrated.

PR #122 has now integrated that exact English source. The entire merged English
value equals the frozen reviewed proposal, and the unchanged reviewed Swedish
value is now applied. `assembly-current-source-rebind.json` records this
mechanical author-produced source rebinding, not a second independent review.
The original full table plus this explicit one-entry replacement is the complete
current source/target/context record; no earlier receipt has been rewritten.

Initial bounded result before the later Curve correction:
- 350 newly added resources, including the complete crop plural.
- 8 repaired existing labels, and 16 unchanged formerly unknown entries reviewed.
- 374 newly reviewed current-source entries: 334 direct production-call-context,
  40 source-semantics-only.
- 340 earlier entries retained exactly, not newly rereviewed.
- 715/717 typed resources present; 714/717 bounded current-source wording accepts.
- 3 holds: dormant Main label, ambiguous legacy palette argument, dormant full
  manual awaiting its explicit complete English correction.

`source-correction-proposals-reviewed.json` preserves both full manuals proposals.
Only assembly Help is now rebound; the legacy manual proposal remains held.

`verify_current_source_rebind.py` checks all current source entries, bounded
application targets and explicit holds against a supplied checkout. Its passing
result is in `current-source-binding.txt`. `validation-summary.md` distinguishes
host tests from unavailable local JVM/runtime checks. These counts and checks are
not native-speaker, installed-layout, TalkBack or whole-language certification.

## Subsequent Curve hint correction

Codex review of PR #151 found that `fästa` incorrectly suggested attachment rather
than committing the current curve. `curve-hint-author-correction.json` records the
complete original and corrected pair, actual call path and review finding. The
replacement explicitly says to finish the curve before both bends are set. The
original independent receipt is unchanged, but its acceptance of this superseded
target is not carried forward. Current source/target evidence comprises the
original full table plus the assembly rebind and this explicit author correction.

There are now 713 unchanged bounded accepts (373 newly reviewed plus 340 prior)
and one author-corrected target awaiting new-head review. Presence remains
715/717; three unrelated holds remain. Source-binding verification checks all
complete target values including this explicitly labelled pending correction,
without turning structural verification into linguistic acceptance.
