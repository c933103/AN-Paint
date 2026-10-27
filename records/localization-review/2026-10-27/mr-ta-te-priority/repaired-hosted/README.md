# PR190: repaired-head CI and original artifact verification

Exact source head `0bbecc9eed1feeccdec6170af44076b408509b3a`, tree `05f16acf89258e5ca16d0bbae7fb2160dd96edd9`; [natural run 40504905089](https://github.com/c933103/AN-Paint/actions/runs/40504905089). All six hosted jobs passed. Its tested synthetic merge `4382c28ba83e333fc062fce3e5aba4dc5439342e` has the same tree and ordered parents `1126b650` + `0bbecc9e`.

- JVM: **1,438 tests, 157 suites, zero failures/errors/skips**. All eleven new MR/TA/TE methods and four SW/VI methods passed.
- Lint: zero issues. Exact-script generation passed.
- Hosted Python: 1,506 discovered, 1,504 passed and two optional Pillow-dependent tests skipped. Both repaired-head local aggregates passed all 1,506, ordinary and optimized.
- API35: all 47 source-eligible app tests and 74 native tests passed. Same-run core and position identities were recomposed locally against exact source. Mandatory dialog and vertical evidence collection succeeded; original app-owned archives, screenshot matrix and reachability validators all revalidated successfully.
- Original APK/source archive SHA256 `8fd17544f8cc24e7482a3601046c550b1b89bfeb94dcb02784221f1cae4e552e`. APK SHA256 `88515d70cf5e6060d9ff9b1a5b813c20bf03af655ae66be8c3840bbb23c80a57`; source ZIP SHA256 `225f720c4afcbc077773cd7d3aa2055c3dd018021975b6cdbafbb8361c2678a5`. APK signature verifies; embedded source equals delivery source. All 1,409 included repository blobs match, with only `.gitignore`, `.idea/codeStyles/Project.xml` and `colorpicker/.gitignore` omitted as repository metadata. Native dependency sources are additional entries.

The first run `40501474780` is preserved distinctly: 1,438 JVM tests had exactly one stale assertion (93 expected English fallbacks versus actual 90); all per-locale exact-value assertions and new methods passed. Its Core instrumentation also passed, but mandatory export collection failed with an offline ADB device. That run remains failed, not waived. The independently accepted one-line count successor preserves all 841 reviewed resource edits and frozen fixtures. No manual retry was used: the repaired source naturally triggered the successful run above.

`terminal-hosted-evidence.tar.xz` contains 1,461 regular files including a full member SHA256 manifest: selected original JUnit/lint/phase outputs, source-bound device receipts, independent repair review, first-run diagnostic evidence and repaired local host logs. The original downloaded artifacts remain immutable inputs; sanitized copies omit local private paths and credentials.

**Exact-head Codex rereview is still running at this checkpoint.** Older-head clean review does not satisfy that gate. This evidence does not claim merge/release readiness. The artifact uses the CI debug signing key, not upgrade signing. No release, native-speaker acceptance or universal device/locale layout certification is asserted.
