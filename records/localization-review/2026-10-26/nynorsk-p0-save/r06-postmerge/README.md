# Nynorsk save messages: verified merged-source result

[PR #173](https://github.com/c933103/AN-Paint/pull/173) is merged as [`857a20103285a77846e340b326667c15a402ff9e`](https://github.com/c933103/AN-Paint/commit/857a20103285a77846e340b326667c15a402ff9e). The signed merge has the expected base/head parents and exactly the reviewed tree `6bb4fa11534149df7f8f58cb3d21faf2b802089f`; all 1,364 merged blobs/modes were checked. This receipt is for the **actual merged commit**, not relabelled PR-run evidence.

## Terminal postmerge checks

[Push run 40272570496](https://github.com/c933103/AN-Paint/actions/runs/40272570496) completed **success** on the merged commit: all six jobs passed (build/source, regression/lint, exact-script generation, API35 position, API35 core, API35 aggregate).

- **1,344 unique JVM cases passed**, zero failures/errors/skips. The two Nynorsk resource/dialog cases and real Nynorsk export filename/dirty-state case passed in this postmerge run.
- Hosted Python: **1,357 run, 1,355 passed, 2 skipped** (210.641 s); skipped identities are not named in the non-verbose receipt and are not guessed. Earlier local ordinary and optimized checks each passed all 1,357 with zero skips. These are distinct receipts.
- Lint: **zero issues**. All regression command phase exits are 0.
- API35: **74/74 native + 45/45 app** source-selected identities passed. The full nine-phase app union was independently recomputed from current source; native identities, uniqueness, source digest, final return/no-timeout status and missing/unexpected/error emptiness were checked. Composed device identity matches actual merged-source APK/build-info; both groups are attempt 1.
- All **13 exact-script probes** and their raw-log hashes/expected exit statuses were checked, including the intended rejected-variant negative probe.

## Exact development artifact

Artifact `12629321243`, archive SHA-256 `abb7afec6ed663ec509c7dade5825da70f6e67e5ec668907f1b72bdb32c1673d`.

- APK: `3f6cb024436af5d61c071008eefb3a5f1f2e60b4a29613ee9e97128363b0ee8b`.
- Corresponding source: `8dfe592ffb83c0ec97916eb8d5730c43e919a27d5b273ad5e3f0381b14400610`.
- All 1,361 packaged tracked files match the merged tree byte-for-byte; three normal packaging-excluded dotfiles are explicitly listed. APK-embedded source equals the external ZIP.
- All eight compiled Nynorsk display values equal the final independent review. APK v1/v2 signatures verify with the per-run CI debug certificate. **This is not upgrade-compatible/private release signing.**

## Coverage and preserved scope

The [merged 171-option CSV/JSON and reproducible delta](https://github.com/c933103/AN-Paint/tree/cde98d358f0035addae961490202b027b4a0e206/records/localization-review/2026-10-26/nynorsk-p0-save/r05-merged-coverage) show eight P0 gaps closed: Nynorsk **15/92 P0 present, 77 missing**; 118 containers present. All 110 inherited values/attributes and all other locales are unchanged. Global P0 missing is 9,278; P1 missing remains 22,557; English-identical leaves remain 7,051.

Exactly eight new disjoint whole values have bounded independent AI linguistic/static review. No prior author-only, historical, qualified, clause-only or synthetic scope is revoked or upgraded. Existing language-report snapshots stay immutable. First-head P2 review/fix/cancelled-run history remains in r03; terminal PR-head evidence remains in r04.

**No native-human, whole-Nynorsk, physical-device, Nynorsk installed-layout or release certification.** Existing 59 scoped / 112 fallback distinction, #56 never-merge, #159 freeze, #113 retarget/held-warning, Help callback/archive identity and release holds remain unchanged. No release occurred.
