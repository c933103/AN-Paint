# Historical PR43/C023 preparation on the first PR34/PR41 partition

**Superseded source preparation. This records the earlier a9077243 candidate only. It is not the current PR43 base, current CI, merge acceptance or language sign-off.**

The [later current-source preparation](https://github.com/c933103/AN-Paint/pull/43#issuecomment-6103089119) supersedes this snapshot. Subsequent PR34 outer-budget and evidence-transport repairs are absent here and must not be overwritten by these patches.

## Frozen historical result

- Input PR34/PR41 tree: `6d6b90c1999d9e771970ab08e4c275e999c446ca`, later published at PR34 commit `739a3dcf1a59785d98a5f5a00f4b76a1b00e6472`.
- Original PR43: `4f9082aa687a5c36b559061bcc10d0e39331610f`; separate C023: `13edc0e81af1ca1561ee2dabedc17959cd85adc0`.
- Original PR43 overlay tree: `15211fc67f84ca09ec4647cc9eab7d6ead3a7146`.
- Original PR43 plus C023 tree: `a9077243b9d5d601c86b872b1a03cb78bcc36dea`.
- Both original deltas applied without conflicts or semantic edits: 1,485 paths, 55-path incremental delta, 1,430 input paths unchanged, no removals or mode changes.
- 483 host tests passed in 162.796 seconds, zero failures/errors/skips. The 26 focused TIFF/Copy-credit tests and actual-history replay passed in normal, -O and PYTHONOPTIMIZE=1 modes.
- Original 37-entry fixture and independent C023 pin, historical hashes, APK/resource assertions, and Android source union remained unchanged. API30 was 73 native + 22 app; API35 was 74 native + 25 app.

The inherited 930-second API35 inner ceilings versus 900-second outer step were explicitly unresolved in this snapshot. Later review/CI found that outer-budget defect and other gates; this earlier host pass does not cure them. No Android SDK was available locally, and this snapshot did not compile or execute the two new C023 Kotlin tests.

## Durable files

- `composition-summary.json`: exact input/output trees, path counts and four replay-patch hashes.
- `combined-on-partition.patch`: exact original 55-path overlay, intended only for the frozen partition tree.
- `historical-preparation-evidence.zip`: original detailed README, 1,485-path mode/blob/origin manifest, all original host and history receipts, source inventory, verification script and three original overlay patches.

For bounded archival, the ZIP omits only the redundant 2,095,044-byte `combined-from-original-pr43.patch`. Its exact Git source objects are already durable. `check_composition.py` reconstructs it with `git diff --binary 4f9082aa687a5c36b559061bcc10d0e39331610f a9077243b9d5d601c86b872b1a03cb78bcc36dea`; the combined target tree can first be reproduced by applying the included overlay to actual PR34 commit 739a3dcf. Expected patch SHA256: `8af7397c6cb91f7ce82f2020e35862d1ebd864ea576c1865c71719c622f8c35f`. Its fourth replay passed locally. The full earlier ZIP has not been published or claimed as delivered.

The embedded detailed README is an unchanged historical receipt written before the later fixes; its references to pending/current work describe that earlier time. This wrapper gives the present disposition.

Register totals remain 475 / 3 structural completed / 472 pending; the 12 probable and four uncertain language findings remain open. C023 remains separately attributable. No native-language, full-language, installed TIFF-dialog rendering/accessibility, release or merge acceptance is claimed.
