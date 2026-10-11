# AN-W05-METADATA-M02: localize the metadata HTTP failure reason

## Selected obligation and frozen base

This is one independently tracked increment of **AN-W05-METADATA**, item **M02** in the [twelve-message inventory](https://github.com/c933103/AN-Paint/blob/c6fbbc7d23483a48bbef066313849129197398ce/verification/commons-metadata-message-inventory-2026-10-09/README.md). The [repository kanban](https://github.com/c933103/AN-Paint/blob/docs/project-kanban-2026-10-10/docs/PROJECT_KANBAN.md) requests implementation after PR34 settles. This source uses develop **2c1bd8622eb6c57444eee8f816194b309fff136e**, with PR34 and PR43/C023 already integrated. Existing PRs 44/45 are separate release-publisher work; no release or workflow file is edited here.

Before editing, the inventory and current source were compared and all repository PR titles/scopes searched. Repository Issues are disabled. M02 remains the exact application literal `Commons metadata: HTTP $status` in `CommonsAttribution.fetch`, reachable through both Copy credit and image insertion. No other open PR implements it. The selected scope was reported before editing.

## Change and preserved boundaries

- `CommonsAttribution.HttpException(status)` remains an `IOException` and carries only the numeric application-owned status, with no worker-localized prose. **Exactly 200** remains success; all other statuses, including redirects, retain the failure behavior. Response bodies are not read for this failure and connection cleanup is unchanged.
- The guarded, alive-activity callback resolves the new `commons_metadata_http_error` resource separately for Copy credit and insertion. `status.toString()` plus `%1$s` keeps protocol digits ASCII even in Arabic. No arbitrary exception is classified by its English text.
- Preserve the existing outer wrappers, Copy credit's blank/absent-detail fallback, insertion's untyped detail behavior, literal percent/newline provider details, and existing typed SVG-size mappings. The shared marker only applies to the metadata fetch; an image-download HTTP failure is still its original separate reason.
- Provider URLs, request parameters (including `iiextmetadatalanguage=en`), response/field limits, metadata content, cache schema, credit ledger/editing, clipboard, redirect policy, SVG rendering and lifecycle guards are unchanged. The other **11 inventory reasons remain open and hard-coded**.
- No fonts, language routing, release code, CI budgets, catalogue policy or repository settings change.

## Language dispositions and acceptance limits

[All 140 exact offered-tag dispositions](all-language-dispositions.json) record this message individually. The canonical default and existing 59-tag complete-check scope receive one new key each; the other **81 offered tags retain their missing-key English fallback**. They are not populated with English copies or neighboring languages/scripts.

The 59 entries comprise eight English variants, the established symbolic variant and 50 model-proposed target-language/script labels. Proposed terminology follows existing catalogue metadata vocabulary where available; those historic words do not regain withdrawn acceptance through reuse. English variants intentionally retain English. The symbolic convention keeps its existing warning prefix. Mixed Korean retains its private exact-script resource route and public tag; Mongolian/Manchu/Nôm scripts remain distinct.

**No new translation has competent/native-speaker acceptance.** High-uncertainty entries are individually marked, notably Ainu, Tibetan, Dzongkha, Hakka, Literary Chinese, vertical Mongolian/Manchu, Hokkien, Jeju, Okinawan, Nôm, Wu and romanized Cantonese. Structural or resource-resolution success is not fluency. All-language completion, native linguistic review and physical-device/TalkBack acceptance remain open. The reset register remains **475 total / 3 structural completed / 472 pending**. M02 does not close any reset row or any whole-language obligation.

## Test design

- The six new host contracts cover the exact 60-resource delta, placeholders, 140 dispositions/81 untouched fallbacks, exact two-production-file changes, both guarded UI boundaries and runtime test inventory. Missing/duplicated/modified resource entries are rejected for every one of 60 catalogues, and unrelated edits fail the original full-file hashes. Corrupted fixtures and untyped producer mutations are rejected.
- The existing PR34 source guard now reverses only this independently pinned M02 increment before performing the original unchanged hashes. Its historical evidence and original F01/C023 pins remain untouched. The two C023 whole-catalogue guards similarly strip only the pinned M02 line before checking their original hashes; the SVG source contract still requires its exact typed mappings and now follows the guarded callback plus metadata-only helper. The old mixed-Korean HTTP test changes only its inner reason oracle to the new exact Korean resource; the independent Hanja-bearing outer oracle remains.
- `CommonsMetadataHttpTranslationTest`: API30/35 real AppLanguage selection/wrapping across **all 140 tags**, literal per-tag resource oracles, explicit 81 fallback checks, exact persisted/private resource tags and nine ASCII status controls. The M02 wording is legitimately identical for ordinary/mixed Korean, so the existing independent Hanja-bearing gallery wrapper test remains the discriminating routing oracle.
- `CommonsMetadataHttpFlowTest`: direct non-200 producers/200 boundary, actual WebView Copy credit and insertion, file/connection cleanup, clipboard/edited-credit/result preservation, successful retries, untyped HTTP-looking/percent/newline/null/blank detail, duplicate actions, destroyed-activity late typed failure suppression, and accessible full-text readability for ten representative profiles at 1×/2×. Forty native host PNG/JSON pairs are requested. These would be Robolectric captures, not installed-device evidence.

## Current verification status

- Canonical catalogue structural validation passes.
- Focused host checks pass normally and under `python -O`; the first test expected the wrong Python representation of the placeholder counter, failed, and was corrected without changing the production code or placeholder requirement. [Original failure](initial-host-fixture-failure.log) is retained.
- The first aggregate run executed 516 cases with three source-contract failures: the new M02 key crossed the two frozen Mongolian full-file guards, and the SVG guard expected the old direct untyped-detail fallback/callback spelling. The precisely scoped successor guards above address those failures without altering production or historical hashes. [Initial failed run](initial-aggregate-scope-failures.log) remains evidence.
- **All 516 host tests pass, zero skips**, in 144.423 seconds on the corrected source/guard tree: [all-host.log](all-host.log). Its negative-control fixtures deliberately print `success: false` diagnostics; the unittest summary is the aggregate result.
- **Local Android compilation/execution was blocked before compilation.** An initial wrapper call could not create its lock under the unavailable default Gradle directory. A bounded retry with a writable temporary Gradle home reached the pinned Gradle 8.13 download and failed with `Network is unreachable`; [exact bootstrap output](gradle-bootstrap-blocked.log). No local Gradle/JVM/lint/AAPT/APK/emulator test or capture is claimed as passed.
- The draft PR's normal exact-head Android CI and distinct Code/Security review requests are the next gates. No full-matrix release run is requested for this routine increment. API30/35 resource checks are included in JVM tests; ordinary installed coverage remains the normal API35 workflow.

Publication is verified by full remote-tree/readback against the intended snapshot before PR creation. The PR discussion will carry exact head, run IDs and later results. No merge or release is included.
