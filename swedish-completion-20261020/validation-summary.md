# Current Swedish validation

Latest application head: `c8bf159e06cacf351407a0ac7cdd28a2a3e16b3f`.
It repairs two JVM test fixtures over `cafb244e8bd8342926d5696ce63a67860cb9b9ad`.
No production source, resource or accepted translation value changed.
The complete original independent receipt is unchanged.

Current local checks:
- Swedish wording suites: 23 passed in 5.976 seconds.
- Empty-credit wording suite: 5 passed in 0.363 seconds.
- Complete normal host suite: 1,056 passed in 287.129 seconds.
- Complete optimized host suite: 1,056 passed in 331.65 seconds.
- Source binding: all 717 complete current English identities/values/attributes;
  713 unchanged bounded Swedish targets plus the explicitly author-corrected
  Curve target, 715 resources present and three unrelated language holds.
- Remote application tree: all 1,254 leaf entries verified against the expected
  parent, including two intended changed files and 1,252 retained entries/modes.
  The same branch was updated non-force with an expected-head lease; final ref,
  sole parent and tree readback matched.
- Current-head hosted run 39427728235 and Codex code review have started.
  Neither is counted passed by this receipt.

The prior hosted run 39412001502 on `cafb244` had 1,186 JVM tests in 127 suites,
with two failures, zero errors and zero skipped. The other five CI jobs passed.
The new real-button Curve test passed in that run, and its exact-head Codex code
review reported no major issues, but these are not current-head acceptance.
`jvm-fixture-repair.json` preserves the exact failures and diagnosis limits.

The empty-credit failure was a stale English fallback oracle for Swedish.
The Exact position fixture omitted the queued OnShow callback and selected only
Swedish resources, not the production app/process locale. The repair adds those
setup requirements and strengthens both-axis syntax, localized error, open-dialog,
layout and persisted-byte checks. The host Java parser probe is not an Android
reproduction; the original assertion report did not identify the invalid input.

The host logs include expected negative-case fixture output from tests of the
instrumentation-result parser. Their overall unittest results are passing;
those emitted mock results do not constitute installed-device execution.

Local Android SDK/Gradle execution is unavailable, so local JVM, lint, APK and
installed-device checks remain unrun. Hosted CI must verify the new exact head.
The original linguistic receipt is not silently rewritten by these author test
corrections; native-speaker, installed-layout and TalkBack certification is not
claimed.
