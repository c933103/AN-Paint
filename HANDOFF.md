# Current project handoff

- Build, test and delivery rules: [CI.md](CI.md).
- Current localization regression data: `tools/fixtures/current_localization/`.
  Exact wording coverage is not native-speaker acceptance. The picker offers
  171 locales: 59 scoped catalogues and 112 other offered locales outside the
  bounded work, with explicit English fallback.
- PR55's typed Commons query failures, full accessible localized status text,
  and native/installed lifecycle and rendering regressions are integrated through
  PR52. Use the project board and current child receipts for remaining work.
- Verification history and failures: [archive index](verification/README.md).
- Active release publication inputs remain in `verification/releases/`;
  migrating audit history does not publish or sign a release.

Use the exact commit's CI/review results for completion claims. Earlier passed
runs, incomplete runs and reviewed diagnostics remain separately labelled.
