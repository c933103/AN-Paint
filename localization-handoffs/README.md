# AN Paint translation handoffs

1. **Translation authors new wording.** Work in non-overlapping portions of the existing locale assignments, using the exact English source and the locale's current terminology. Return keyed wording and flag uncertainty; a worker does not write files or change the app. The coordinator saves the wording handoff and pins the source revision. Don't delay authoring while review or CI is pending.
2. **Editorial review assesses existing drafts.** Check meaning, natural language, spelling, and consistency with the actual controls. Record acceptance and unresolved items explicitly. Review is not new translation; editorial acceptance is not native-speaker or device verification.
3. **Integration applies accepted wording.** Check for drift, preserve the accepted wording and Android resource contracts, and handle XML, tests, PRs, merges, and releases. Return wording problems to editorial review rather than rewriting them silently.

Track fresh drafts, reviewed or accepted wording, merged coverage, and runtime checks separately. Invariant notation, aliases, and unchanged English do not count as new translations. CI and code review cannot confer linguistic acceptance. This evidence branch is not meant to merge into the app.
