# PR114 composed-head verification

Source head: `93489b4138e84f73356302a1e75a5cb377954e88`.
Source tree: `2c61c517f00d800bd5cc0ff1bf8f783a9b687a56`.
Parents: concurrent `511f9607c7889a5acd2e6f79dc96e484cb37bf5a` and merged
PR111/develop `e414a4df64a56c2d8a2f374741b1f1b58fceea9b`.
The latter tree is identical to independently reviewed PR111 head `20437482`.

All 1,191 published files and executable modes were compared with the frozen
reviewed manifest, including all inherited files and both explicit overlapping
files. Publication used a non-force expected-head lease. The PR contains 35
changed files against merged PR111; this separate ref contains the larger evidence.

## Passed local gates

- Normal and optimized full host aggregates each passed **867 tests**, in
  201.673 and 198.713 seconds of unittest time respectively (202.053 and 199.622
  seconds including process setup). Initial runs each failed the stale sum of
  individual phase maxima. Those actual failures are retained. The reviewed
  correction adds explicit preparation 6 / JVM 12 / job 22 checks and preserves
  the original 38-minute sum for every other phase; no deadline was increased.
- Supplemental API35 compilation passed all 101 production source files and
  120 test files. One unrelated Mockito-dependent test was outside the available
  manual classpath; the actual hosted Gradle suite still includes it. All 18 pure
  formatter, caption-prefix and run-construction JUnit tests passed in 0.275s.
- The current XML inventory contains 48,970 rows. Its actual formatter comparison
  and 23,632 present-null samples have zero mismatches/Formatter errors.
- Fresh AAPT compile/link/dump contains 51,126 rows across 145 configurations.
  Its actual formatter comparison and 24,820 present-null samples have zero
  mismatches/errors. All 205 aliases resolve without a missing exact-config target.
  The nine canonical Commons messages are included in generated source fallback.
- Independent composition review preserves all reviewed Commons and PL/CS values.
  Japanese retains the nine Commons additions; its only difference from develop
  restores the percent symbol using valid `%%` encoding. The 18 Ainu/Manchu
  templates remain byte-for-byte intact. No PR113 corrections are included.
- The bounded caption/suffix composition review passed 6,000 Unicode comparisons,
  four long reconstruction controls, 45,600 modeled wrapping comparisons and 31
  incremental/whole-measurement controls. Mutations detect both missing suffix
  splitting and missing cross-token state. Model measurements are not native proof.
- Source-root repair and CI preparation changes have separately retained reviews,
  focused tests and negative controls. The actual Gradle producer/input graph is
  a hosted execution gate, not something the lexical host tests establish.

## Hosted state at publication

[Exact-head run 39021174915](https://github.com/c933103/AN-Paint/actions/runs/39021174915)
is running. The actual preparation graph, full JVM execution, native suffix and
caption tests together, lint, resource-generation probes, matching APK/source
build and API35 groups remain pending in this receipt. Exact-head code/security
reviews were requested; a request comment does not establish security execution.

Earlier failed deadline runs remain historical failures. In particular, run
39017556055 produced 1,099 passing JUnit cases but failed its unchanged 12-minute
JVM-step deadline. Its actual Test task took 9m32s, with roughly 149s of compilation,
resource preparation and setup inside the same step. The new required preparation
phase is separately bounded to six minutes; actual full tests remain bounded to
12 minutes and the aggregate job to 22 minutes, with unchanged assertions and
individual deadlines. Preparation failure still fails the job.

## Archive and reproduction

`combined-evidence.zip` preserves actual stdout/stderr, successful and failed host
logs, commands, source identities, the AAPT dump, generated fallback XML, independent
helper/model code and reviewed-patch receipts. The adjacent manifest records each
member and SHA256. Complete catalogue TSVs are reproducible from the exact source
and retained dump using the included scripts; their input hashes and comparison
summaries are retained without duplicating the full translated catalogues.

This establishes bounded runtime/resource compatibility, not linguistic acceptance,
invalid-XML recovery or a universal crash-proof guarantee. Caller/artwork text and
complete warnings remain intact. Native/font/layout/OS limits, very large caller
arguments, API21–27 cache-comparison execution and real-WebView/device coverage
remain separately scoped. Prior withdrawn localization conclusions stay withdrawn.
