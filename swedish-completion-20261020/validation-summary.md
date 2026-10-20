# Current Swedish validation

Latest application head: `994e448a7cf424ee33439662956fe46b221ba3f4`.
This changes only workflow budgets, their contract tests and CI documentation.
No production behavior, resource or translation value changed.

Current combined-source checks:
- Fresh develop: `4feab3d6a13ac8c8e049393498ecf059ebd2f9d7`.
- Exact synthetic merge: `d2785884f33e7171cc28cc6bd4487068da481d08`.
- All 1,263 merged leaf contents and modes match the locally checked composition.
- All 56 CI contract tests passed in 83.957 seconds.
- Complete normal host suite: 1,068 passed in 435.857 seconds.
- Complete optimized host suite: running; not counted passed here.
- Application tree: all 1,254 leaf entries verified, with four intended budget
  changes and 1,250 preserved entries/modes. Non-force expected-head lease and
  final ref/sole-parent/tree readback matched.
- Exact-head review request: PR151 comment 6292552617.
- Hosted run 39434720839 is running; no current-head JVM/device/CI pass claimed.

The preceding c8bf159 run proves both repaired JVM tests now pass, along with
all 1,186 JVM tests across 127 suites (zero failures/errors/skips) and the Curve
button regression. Python reported 1,066 tests OK with two skips. Its command
receipts exited zero, but explicit 4-minute Python and 12-minute JVM timeouts
still make their Actions steps fail. The job's aggregate conclusion was cancelled;
its separate cancellation source is not established by the available log. The
five other jobs passed, as did native/lint steps within the cancelled job.
See `hosted-jvm-repair-verification.json` for exact source/artifact/report binding.

The 8/20-minute phase caps now retain all assertions with measured headroom.
The 55-minute job cap covers 50 minutes of explicit phase maxima plus five of
checkout/cache/evidence allowance. These remain hard cancellation policies,
not universal runtime guarantees or permission to count a timeout as success.

Source binding is unchanged: all 717 current English identities/values/attributes;
713 unchanged bounded Swedish targets plus one explicit author-corrected Curve
target; 715 resources present and three genuine holds. The original independent
linguistic receipt is unmodified. c8bf159 had a clean exact-head Codex Code review,
but that is not a replacement independent linguistic or installed-layout review.

Local Android SDK/Gradle execution remains unavailable. Local JVM, lint, APK and
installed-device checks were not run. Host logs include intentional negative
instrumentation-parser fixtures; their printed mock failures are not device runs.
Native-speaker, installed Swedish layout and TalkBack certification are not claimed.
