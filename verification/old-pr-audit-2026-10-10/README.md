# Older PR current-source audit, 10 October 2026

Scope: PR7, PR9, PR16 and PR18 against develop7e8a0d2377693a35cd9392f2082ef88548a6f67f. Source presence, test execution, linguistic review and original-discussion reconciliation remain separate.

## AN16 supersession proof

Replacement commit `4e11cb42374f2aee0557cbdda1da938ff4902106` explicitly adapts PR16 and is an ancestor of current develop. The local checkout was deepened before final ancestry conclusions, because its initial shallow boundary obscured this relationship.

The following three method bodies are byte-identical between original aa3412a45 and current develop:

- unfinishedCreditDraftSurvivesRecreationWithoutBecomingASavedEdit
- restoredCreditDraftKeepsSelectedSourceAndAnEmptyDraftWithoutSavingIt
- dismissedCreditDraftIsNotSavedOrReopenedByActivityRecreation

The current production code retains EditorDraft/source restoration, explicit Save/Copy/Done semantics, and cancellation/discard, with newer credit-session persistence, error handling and notification behavior. Old-file transplantation produces conflicts in GalleryCredits.kt and MediaGalleryActivity.kt.

Current develop run https://github.com/c933103/AN-Paint/actions/runs/37978574286 is successful. Downloaded current-head artifact11641121530 XML was inspected: GalleryImportTest11/11, no failures/errors/skips, including all three named cases. Existing downloaded-artifact receipt agrees with live artifact metadata/digest `cf5cbd6a6f0c25963540695008283dd9ed7aa4f6cf1cc71bfed50b07d3cf197f`.

## AN18 current-source gap and bounded continuation

Head040d64f is an ancestor of develop. It has zero commits unique to develop, but that does not prove retention.

`a1f9d6d8cf4062c4f764c3436a73ecec21a59d9a` reconciled PR19 onto accepted develop. Its message explicitly avoids old vertical prototypes; `verification/gallery-routing-reconciliation-2026-10-09/reconciliation-plan.md` explicitly excludes '#18 vertical-locale test/prototype adoption' and the Arrow repair. The old VerticalLocaleDeviceTest (488 lines after the later b6c560d32 autosave correction) and separate vertical runner/capture partition were removed in that reconciliation. The current runner has exclude-class selection and ordinary/seed/verify accounting; it does not retain PR18's include-class option or app-vertical invocation.

Current installed successors include `insertedCreditsRemainOriginalAndCopyableAfterChoosingVerticalEnglish` and `deviceLanguageRowKeepsTheSystemLabelAcrossRealAppLanguageSwitches`. Current API35 XML has74 native/import +18 ordinary app +1 seed +1 verify successes. It contains no four-locale portrait/landscape tab/tool/Save/JPEG matrix. Host DeviceLanguagePickerTest and vertical-notice characterization are useful different coverage, not substitutes for the omitted installed matrix.

Next implementation should preserve current develop production and runner architecture, adapt the four matrix cases and real-input oracles, use current startupReady and scheduled-autosave readiness, preserve both sentinel pixels and external-destination rejection, and collect32 expected PNGs. Consider the later b6c560d32 source evidence: Line schedules a1500ms autosave that can cross Arrow reveal; its proposed fix waits for the actual write and records passive input, rather than retries or longer deadlines.

Use a distinct bounded vertical invocation rather than adding roughly108 historical seconds to the current18-case ordinary invocation. Extend strict accounting to the disjoint union of ordinary/vertical/seed/verify; retain both accepted-credit process-stop phases and existing deadlines. Fresh exact-head API35 compilation/runtime/XML/screenshot evidence is required. No production vertical-notice experiment, broad language certification or old CI transplant is implied.

Proposed bounded PR18 disposition:

Current develop7e8a0d2 includes this PR's head in its history, but its four installed matrix tests are absent from the current tree. PR19 reconciliation a1f9d6d8 explicitly excluded adoption of the old vertical-locale prototype and preserved the newer ordinary/accepted-credit restart runner. Current exact-head API35 results cover the retained en-XV credit and language-row tests; they do not execute this PR's four-locale/two-orientation navigation and Save matrix. The next bounded step is a current-base adaptation of those four real-input tests with startup/autosave readiness, separate bounded execution, complete method accounting, and32 expected screenshots, while preserving the accepted-credit restart phases. This PR therefore needs a tested continuation; its historical green run is retained as old-head evidence only.

## AN7/9 actionable remaining work

Fresh element-level comparison of each merge-base-to-head resource delta against current develop found:

- PR7:135 changed string/plural elements across19 XML files, all135 equal to current develop; no removed resource keys.
- PR9:97 changed elements across12 XML files, all97 equal to current develop; no removed resource keys.

Comparisons use the full serialized XML element, not just the key. The current NormalizeImagesDialog also uses the proposed localized intro/info/content-description resources while preserving newer LocaleNumberInput behavior. Do not resolve conflicts by restoring old numeric-input implementation or replacing current catalogues.

Missing guard files are `tools/test_normalization_scope_pr7.py` and `tools/test_normalization_scope_pr9.py`. Each original guard was executed from memory against current develop: both pass, covering the six normalization resources for the12 PR7 tags and5 PR9 tags. Adding these unchanged guards is a minimal useful test delta; it grants no language acceptance.

Fresh current-source structural evidence:32 translation tests passed, including equivalent locale configuration checks. Current exact-head AppLanguageTest XML is19/19 with no failure/error/skip, including `regionalLabelsLegacyMigrationsAndStarterChoicesUseTheirCatalogues` and `manchuPickerUsesItsOwnJoinedVerticalAutonym`. Current source registers jje, keeps cju as a migration alias, uses script==Mong direction, shared typography, and uniform VerticalUi.languageChoice for picker rows. This evidence can inform the individual reopened engineering obligations, but review/reset flags were not changed.

After preserving those results in the same PR histories, work through P07-001..016 and P09-001..023 plus their companion granular rows. Specifically recover latest original instructions, reconcile non-review findings, verify seven English variant identities/default language note and pt-BR/Italian/Greek/Turkish semantic scope; independently recheck Jeju clause/predicate/memory terms, both Ainu source-assisted reviews/count-size/select-all meanings, Manchu lexical/Unicode/newline/transliteration/glyph cases, and Okinawan grammar/action/polygon/aspect-ratio cases. Retain withdrawn records as historical input and preserve current recheck register/history links. No row closes merely because its old source is present or tests pass.


## Reproduction and limits

Run `python verification/old-pr-audit-2026-10-10/verify_source.py` from a checkout with the exact named commit objects. The verifier performs read-only Git source comparisons, emits machine-readable evidence, checks the retained PR16 test identities and archived current-head XML, and confirms the missing PR18 test/guard files. It does not run Android or certify language quality.

Current structural translation suite:32 tests passed. Current runner/emulator/gallery host subset:33 tests passed. Original PR7/9 normalization guards executed against current catalogues:2 passed; the guards were not added to production/test directories.

Original latest discussion completeness and remaining language semantics are still unverified. Repository ancestry and historical tests cannot close the reset obligations.
