# Legacy Discard: later bounded disposition

Authoritative receipt: [PR56, comment6541291852](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6541291852).

+Discard wording review disposition — 31 October 2026. Independent linguistic review completed; this is bounded model review, not native-human or installed-UI certification.

1. eu-ES / ui_discard, English 'Discard': RETAIN AND ACCEPT UNCHANGED display value 'Baztertu aldaketak'. High confidence in the changes-discard action family. Immutable official GNOME simple-scan commit52d93f40443b7f155411320389f51b73ea5e0119, po/eu.po, explicitly maps 'Discard Changes' to this value in an unsaved-document abandonment dialog, while keeping-unchanged has separate wording. No source edit or presence credit.
https://github.com/GNOME/simple-scan/blob/52d93f40443b7f155411320389f51b73ea5e0119/po/eu.po

2. ps / ui_discard, English 'Discard': ACCEPT EXISTING-VALUE REFINEMENT from 'رد کړئ' to display value 'بدلونونه پرېږدئ'. Medium contextual-idiom confidence, strong grammatical plausibility. This is explicit-object harmonization with accepted ui_discard_changes23, NOT proof that the previous reject/turn-down wording was grammatically wrong or semantically reversed. OPED independently supports abandonment/cessation for پرېښودل and present پرېږدي; the changes plural and polite/plural imperative are supported by grammar sources. Leave/allow senses make context relevant; no deployed Pashto UI attestation or native-human review is claimed.
https://oped.univie.ac.at/oped.php?alph=2&dev=1&dir=1&entry=11477&how=1&let=&nons=1&what=0
https://oped.univie.ac.at/oped.php?alph=0&dev=1&dir=0&entry=23626&how=0&let=%D8%B1&nons=0&what=2
https://grammar.lingdocs.com/nouns/nouns-plural/
https://grammar.lingdocs.com/verbs/imperative-verbs/

Scope: current production caller found uses ui_discard_changes23, not legacy ui_discard; dynamic-resource resolver and Java/Kotlin/XML references were checked. Do not claim an active-dialog bug fix. Original held fixtures contain no recovered rejected alternative/rationale; preserve them historically and record these as later dispositions. Unreadable ERIC table was NOT treated as visually verified evidence.

Implementation accounting: zero new missing entries; one newly accepted existing replacement, plus one unchanged acceptance. These are separate from PR247's frozen737-addition/2-replacement packet. Preserve its active validation unchanged; apply the Pashto refinement in the next bounded native integration after that base settles, with exact predecessor/source/placeholder tests. Do not call this a user approval hold, a merged change, or a release.

## Regression boundary

This change is separate from PR247's frozen acceptance packet. Its historical
fixtures and residual ledger remain byte-for-byte unchanged. The finite later
binding checks the Pashto identity, exact historical predecessor, source text,
attributes, resource shape and placeholder-free value. The historical cohort
checks use that binding only for `ps/ui_discard`; other holds retain their guards.
Compiled tests cover the refined Pashto and unchanged Basque displays under the
selected locale and reject a wrong successor identity or predecessor. These are
not installed-UI, native-human or whole-language certification.

Accounting: zero new missing entries; one existing refinement; one unchanged
acceptance. No release is part of this change.
