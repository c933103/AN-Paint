# Independent principal-variety and language-option review

## Result

No blocking source or tracker finding remains in the revised **167-option** candidate reviewed on 12 October 2026. The 42 reviewed source/test/document paths are bound by `reviewed-source-sha256.json`, SHA-256 `519996573b43b7795416e9c13dc49c547a9100c2fe0dc0f64fd80787f8191c8b`.

The baseline is merged PR #57, commit `1011233a89a3cac98f56fc2d46a902a9476a1e08`, tree `bbf2766504e1b743cc9a580a429f0a2179a10b2d`. GitHub independently confirmed this tree equals the reviewed PR source `be60964a5b62c73f6517ec2fa8f58b101ab05c99`.

This review supersedes the earlier 162-option acceptance for the clarified request. That candidate's unchanged evidence is explicitly archived as historical, not reused as current acceptance.

## Verified source

- 167 unique offered options; all prior 146 identities and their relative order remain unchanged.
- Exactly 21 new options have matching picker names/tags, Android locale inventory, metadata and exact empty canonical catalogues. No new translated entries were supplied.
- The clarified seven choices are `nch`, `nhe`, `nhw`, `quz`, `quy`, `quh`, `qug`. Generic `nah` and `qu` no longer appear as offered choices or canonical catalogues.
- Source-backed name bases and explicit regional qualifiers match the agreed labels. The scope notes avoid claiming all Nahuatl, all Southern Quechua, all Bolivian Quechua or all Ecuadorian Kichwa. Provincial Kichwa population evidence is explicitly not an exact `qug` census. The companion `principal-variety-decision.md` records primary sources and selection limits.
- Sanskrit `sa` remains the sole macrolanguage among the new 21. The other 20 use individual-language tags. This is a bounded principal set, not an exhaustive language-family classification.
- Source coverage remains 0/695 strings and 0/1 plural resource for each new catalogue; translation and linguistic review are not started.
- Current fallback checks use 108 remaining partial/empty catalogues and compose the 27 additions. Historical 140-choice/81-fallback evidence and the first six-option fixture remain byte-identical.
- No production Kotlin code changed. The API30/35 app-language method now exercises every new identity, label and default-resource fallback, with platform language-switch checks where applicable. This review inspected that method; it did not execute Android tests.
- `git diff HEAD --check` passed.

One concrete fixture defect was found during revision: `nch` was initially assigned to the Quechua requested group. It was corrected to Nahuatl before freeze, and both the exact group-set test and an independent mutation control now reject that mistake.

## Independent host results

64 focused Python tests passed in **7.802 seconds**:

`PYTHONPATH=tools python3 -m unittest -v test_language_option_additions test_language_option_additions_second test_translations test_help_commons_provider test_commons_import_change_translations test_commons_copy_credit_errors test_commons_metadata_m03`

Ten negative controls were correctly rejected: duplicate tag; wrong autonym; English-filled catalogue misrepresented as untranslated; Chimborazo misclassified as a macrolanguage; omitted second extension; changed prior identity at constant inventory size; altered first-extension fixture; reintroduced broad Quechua option; reintroduced broad Nahuatl catalogue; and Central Huasteca assigned to the Quechua group. Results are in `independent-review.json`; raw focused output is in `focused-tests.log`.

## Tracker checks

The refreshed tracker generator passed isolated dummy-candidate tests in both first-PR merge-state branches. Both outputs have 167 unique rows, preserve the original 140 rows verbatim, and bind all 21 new catalogue Git blobs correctly. The merged branch retains the first six accepted identity/fallback checks while explicitly leaving full UI acceptance open. Every new row remains 0/696 with translation/review unstarted and UI verification not established.

The current remote tracker parent `1318691` was fetched independently. All 146 of its existing rows are retained verbatim in the merged-branch output. The new selection decision and primary sources propagate unchanged into the 21-option JSON. Dummy outputs were not published; real publication must use the verified candidate PR and full source commit, preserving the existing merged-six snapshot.

Generator SHA-256: `9e033c675a41224d5069f0281a9f10bd82338578961499936526d153b60ef581`. Detailed branch results are in `tracker-branch-review.json`.

## Limits

This establishes source/host contracts and tracker claims only. No new Android compilation, emulator run, glyph-coverage check, installed picker/UI test, translation, linguistic acceptance or whole-UI acceptance is claimed. The final hosted results must be bound to the exact revised published source separately.
