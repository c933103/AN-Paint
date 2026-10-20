# Current Swedish validation

Latest application head: `cafb244e8bd8342926d5696ce63a67860cb9b9ad`.
This corrects only the Curve hint and its tests/documentation over the original
Swedish PR head. The complete original independent receipt is unchanged.

Current checks after the Curve correction:
- Swedish wording suites: 23 passed in 3.836 seconds.
- Complete normal host suite: 1,056 passed in 223.709 seconds.
- Translation catalogue structural validation: passed.
- Source binding: all 717 complete current English identities/values/attributes;
  713 unchanged bounded Swedish targets plus the explicitly author-corrected
  pending target, 715 resources present and three unrelated holds.
- Remote application tree: all 1,254 leaf entries verified against the expected
  parent, including five intended changed files and 1,249 retained entries with
  original modes. Same branch updated non-force with expected-head lease.
- Exact-head hosted run 39412001502 has started. Current-head Codex code review
  is running. Neither is counted passed here.
- Optimized host suite started on this correction; pending at this receipt.

Earlier head `6cfe2e924bb733366599d89d93ead11dff7dd689` passed both normal and
optimized host suites with 1,055 tests. Its earlier APK/build and position-dialog
checks passed, but they do not verify the new correction/test head.

Local Gradle distribution download was unavailable due network unreachable, so
local JVM, lint, APK and installed-device checks remain unrun. The new real-button
curve regression covers zero/one bends, repeated activation and undo/redo; it
must run in hosted JVM CI before a behavioral pass is claimed.
