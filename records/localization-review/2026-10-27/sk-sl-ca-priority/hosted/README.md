# Terminal exact-head CI: Slovak, Slovenian and Catalan

[PR187](https://github.com/c933103/AN-Paint/pull/187), head `941e4a15b1ebf0fd0242cae7765ab75e94922818`, passed [run40466523033](https://github.com/c933103/AN-Paint/actions/runs/40466523033), attempt 1. All six jobs completed successfully: regression/lint, build/corresponding source, exact-script generation, core API35, position API35, and composed API35. No source repair or rerun was needed.

The hosted merge commit `b5542dabdaf38ce0f1f4c79299ef9eedd869acd9` has exactly the reviewed head tree `d06833e6d8cd1ec700fd03f61858433290808ab7`. Its parents are develop `0c4f732e7c959bb0829bc537b8e1d34e474e4258` and the PR head. The source head carries PR186 final `728ddd062b4fef9e9440978959d85c199da6dccc`; earlier acceptance and integration evidence remain unchanged.

## Verified results

- Hosted Python aggregate: **1,481 passed**, 227.629 seconds. Earlier local ordinary and optimized aggregates also passed 1,481 each and are preserved in the preceding final evidence record.
- JVM XML: **1,417 tests across 154 suites**, zero failures, errors or skips. All **seven new actual-consumer methods** passed, including complete compiled values, crop/dimension controls, tool descriptions, exact/lower-bound animation import with Cancel/file ownership, decoder-memory floor and preallocation failure text.
- Android lint: **zero issues** in its XML report.
- Current API35: **47/47 app identities and 74/74 native identities** match the exact source inventory, with no omitted, unexpected, duplicated, skipped, failed or excluded methods. Core and position reports were independently recomposed locally using the source validator and matching APK/source/test-APK identities. This is regression coverage, not whole-device linguistic acceptance for all strings.
- Exact-script clean/incremental resource graph checks passed. APK, corresponding source and test APK compilation passed in the build job.
- Exact-head [Codex review](https://github.com/c933103/AN-Paint/pull/187#issuecomment-6436229184) found no major issues; the code and security summary reports completed with no findings for this head.

The prebuilt API35 identity reports bind APK SHA256 `1275afe4f7765ec93d52bf1df674c1de23ade0cee63b554855879fa032cfb63d`, corresponding-source SHA256 `4c8305acfbfa0bcf84444ada3661486451910acf2b96a2fae6feead599e3bdb2`, and app test APK SHA256 `e7c2c0136ac1023830401a67afe33393377acc26d0baa7fb0c0d23fb24245ae8`. The APK is a CI debug artifact, not a release or a claim of private upgrade signing.

## Durable records

[Terminal hosted evidence](terminal-hosted-evidence.zip) preserves the complete JVM XML results, phase logs, lint report, exact-script reports, source-bound instrumentation summaries/full protocol logs, composition receipts and sanitized terminal GitHub metadata. [Archive receipt](archive-receipt.json) and the internal manifest bind exact bytes. The original downloadable GitHub artifacts are identified with SHA256 digests; this compact archive intentionally omits large binary APKs, unrelated captures, raw logcat and cache files. No signed download URLs or credentials are included.

The earlier source-bound author, independent linguistic review, all-171 structural accounting and final local-check archives remain immutable. No new translation/review credit is claimed here. Merge remains subject to reconciliation with PR186's actual merged tree and the normal exact-head gate; no release is requested.
