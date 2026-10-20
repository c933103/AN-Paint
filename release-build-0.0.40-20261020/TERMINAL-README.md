# Exact 0.0.40 release gates

Natural push run [39452992495](https://github.com/c933103/AN-Paint/actions/runs/39452992495), source `d664b3e72ea3261dba662119a429b0bb3914c04a`, tree `409a41191173f98d10155b8058b232efa1a527fc`, completed successfully at 2026-10-20T16:20:45Z. All nine jobs passed.

The read-only independent artifact verification reproduced exact SDK-aware app inventories and Paintroid source inventories, checked JUnit counts and zero failures/errors/skips, reconciled the composed artifact/job/run identities, and revalidated vertical and dialog export contents using the source-bound validators.

- 1,250 JVM tests across 131 XML reports; release lint has zero issues.
- API 30: 103 selected tests, comprising 73 Paintroid and 30 app cases. Thirteen app SDK suppressions, two restart exclusions, and one Paintroid SDK suppression remain explicit.
- API 35: 119 selected tests, comprising 74 Paintroid and 45 app cases.
- Each API: 32 baseline screenshots, 64 reachability screenshots, eight reachability JSON traces, and 104 vertical export files. API 35 additionally has 12 source-bound dialog exports, retaining the scope limits in the original receipt.
- Exact-script resource graph: nine probes, all zero exits, with all log hashes verified. See the separately preserved exact-script archive.

`terminal-report-receipts.zip` preserves JSON receipts/traces and JUnit/lint XML from the exact downloaded report artifacts. It does not duplicate raw screenshot PNGs, export ZIPs or full CI logs; their archive identities and per-file digests remain in the original manifests. This ZIP is evidence, not an application source-tree change.

`final-report-verification.json` records computed inventory counts and acceptance limits. `natural-release-gates.json` preserves the terminal run/jobs/artifact metadata. `ci-artifact-verification.json` separately records the release-variant APK/source hash, byte equality, version, non-debuggable package, four ABIs and alignment checks.

The CI gate records do not establish private upgrade signing or publication. The CI APK still uses the CI debug signer. The separate `signing-verification.json` and `signature-verification.txt` record subsequent local upgrade signing of a separate 0.0.40 output, unchanged payload/source, and the public patch's exact reconstruction through the unmodified publisher apply routine. The standard generator's exit-137 attempt and the successful memory-bounded construction remain distinguished. No publication has occurred. Existing Swedish, Afrikaans and other holds remain unchanged; no native-speaker, whole-locale, physical-device or universal UI claim is made. Newer unpublished Czech work is excluded.
