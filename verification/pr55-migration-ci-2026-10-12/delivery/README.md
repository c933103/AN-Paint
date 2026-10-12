# PR55 reviewability-migration delivery: independent retained-artifact audit

## Result

PASS within the bounded delivery/probe/compiled-resource scope below. No migration-created discrepancy was found in these checks. This is not an overall CI, installed-device, rendering, upgrade-signing, release, or linguistic-acceptance conclusion. The supplied run metadata records API30 failure and API35 success; those device results belong to the separate parent review.

- Public head: `43ab6622cdf6aac957a8d31cf2c5c20009e71d6e`
- Current source tree: `592a60877524c5c118695cb45a4d0d5cd257b25a`
- PR52 base: `71f4d288669858e7975ec4c094b7f47a9a1ff145`
- Merge tested by CI: `e191c4660ef8709450df213cb75bd4bcf0810cb2`
- Run: [38279470164](https://github.com/c933103/AN-Paint/actions/runs/38279470164)
- Source/merge/publication relation: parent-verified GitHub provenance retained in `source-publication.json`; this offline review independently rechecked the actual ZIPs, extractions, source objects and compiled APK resources. It did not independently query GitHub.

## Actual artifacts

| Artifact | ID | ZIP SHA-256 |
|---|---:|---|
| APK and corresponding source | 11760314237 | `a9134a6575b8e61a1b90cf63309b455da1dabeaaa68f6b55faa7bcec63cdf1a8` |
| Exact-script generation | 11760916005 | `dcde889303bb63f0dbdc10006df2148d03e0725d9e7115b019052d5b7ed86d73` |

The metadata run/head, merge-derived artifact names, sizes, archive digests and every extracted file agree. The retained metadata SHA-256 is `6603606fcd84d51e7ea99d55e432d1ab4984d28cf630b85b8360393252d7565d`.

- APK SHA-256: `445b9b6e393e63490c7054ef44e0aefb1fefd5b56954fa8736e9974dee06f588`
- Separate and APK-embedded source ZIP SHA-256: `7beaf27696c948d94dec39b58cb0678a6a6315d2b3b89b43c74d582f1daf20b4`
- Probe summary SHA-256: `305bc404d8d78146bc1f2da4e2658c51ed6d6197c1eff0472b272353f413553b`
- aapt2 SHA-256: `d1096e11aba9c974644369ee3c50d239acac3f3428ffa928e5b9c14dfb7a57de`
- Complete aapt2 resource dump SHA-256: `6e0cadda96f4e7ed41f0594c8a30ef2237d97ba0cde4faa12f325a74ecce9f9e`

## Delivery and notices

Tracked inventory is derived from the current source tree, not the previous delivery or a historical file-count oracle: 1,061 current tracked leaves. The corresponding-source ZIP contains 1,058 byte-exact Git blobs with exact executable modes. Its only tracked omissions are the predeclared `.gitignore`, `colorpicker/.gitignore`, and `.idea/codeStyles/Project.xml`. The other 6,258 files lie exclusively under the four native-source roots declared by the current bundling script: jxl-source, webp-source, heif-source, and tiff-source. Upstream native-source contents were not independently reaudited.

The source embedded in the actual APK is identical to the separately delivered ZIP. All 14 packaged font/inventory files and all 21 legal assets match the current tree byte-for-byte and have exact path-set equality. All 13 font binaries match their inventory digests. Nôm UI-only identity, current name/licence metadata, original input attribution, five MIT paragraphs and 21 OFL paragraphs are retained in the appropriate actual notice assets; its complete combined notice is present in both displayed aggregates. This verifies asset/notice preservation, not an independent legal determination.

One pre-existing metadata observation is retained separately: ten ordinary-font `licence_file` entries point to missing individual files. Their attributions and licence text remain in the packaged `FONT_NOTICES.txt` / `THIRD_PARTY_NOTICES.txt` aggregates. The paths were already absent before migration, and the inventory plus aggregates are unchanged from the prior reviewed tree. This is an existing unresolved reference inconsistency, not evidence that this migration removed licence text. See `preexisting-inventory-observation.json` for exact paths and the one-time comparison; it is not a normal CI gate.

## Seven exact-script probes

All seven retained pinned-Gradle probe receipts pass source identity, success status, command/task inventory, original log SHA-256, source wrapper/build hashes and producer-before-consumer validation:

1. Clean
2. Clean debug and release resource merges
3. Unchanged generation is UP-TO-DATE
4. Input change regenerates while stale output is removed
5. Restored input precedes release merge
6. Second clean
7. Release-first generation after clean

The four applicable generated-resource hash dictionaries exactly match the current canonical XML or its declared temporary comment mutation; missing receipts and extra stale members are rejected. The retained probe implementation checks complete generated-file equality and stale-output removal before success. Only the unrelated corresponding-source bundle task is excluded. This audit verifies the real retained toolchain receipts; it does not rerun Gradle.

## Compiled M04 and Arabic

The actual source-bound APK contains exactly 61 M04 configurations: default, the current compact fixture's 59 scoped locales, and generated mixed-script Korean alias. Every compiled value matches the current fixture, including decoded Android escapes. No unexpected M04 locale is present.

- Manchu U+180E zero-based positions: 7, 18, 27
- Mongolian U+202F zero-based positions: 7, 17, 30
- The compiled Arabic M04 value and both copy/insert wrapper values also match current source. `compiled-arabic-result.json` supplies the two composed route texts for the parent's independent installed-record comparison.

This proves compiled value/configuration/control retention. It does not prove all runtime locale fallback selections, shaping, clipping, pixel equality, accessibility, route execution, linguistic fluency or completion of the 81 open fallback locales.

## Portable checks

From any directory, pass a repository containing the current tree object, the retained CI root (two ZIPs, extractions and supplied metadata), an existing matching aapt2, and a new output directory:

```sh
bash run_audit.sh SOURCE_REPO CI_ARTIFACT_ROOT AAPT2 NEW_OUTPUT_DIRECTORY
```

The runner requires a new output directory and does not modify source, existing evidence or downloaded archive contents. Standard-library Python, Git, Bash and the hash-pinned aapt2 are sufficient. The standalone review scripts bind this particular delivery's identities; none were installed as application CI or added to the source tree.

Five audit stages passed. Eight checker tests also passed under normal Python and `python3 -O`, including corrupt/missing/stale generated receipts, altered command/log hash, missing probe and a fully rehashed producer-after-consumer mutation. A complete portable-run rerun produced byte-identical five JSON results (`portable-result-equality.json`). `git diff --exit-code` against the current tree passed, confirming the source worktree remained exact.

## Limits and handoff

No source edits, public writes, user-computer/Work tasks, historical receipt modifications, Gradle rerun, JVM audit or installed audit were performed. APK signature/upgrade key, alignment, ABIs, native-source authenticity, installation and visual acceptance are outside this review. Build metadata explicitly identifies a CI debug key and separate test status. Preserve this audit with the parent's final evidence; do not use its source hashes as a new permanent historical CI dependency.
