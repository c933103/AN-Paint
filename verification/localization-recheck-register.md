# Localization recheck register

**All previous scoped work is open. Accepted progress: zero. Every item below is pending full recheck.**

The user rejected the entire previous delivery and instructed that each part become additional work requiring an individual full recheck. This register implements that reset; creating the register does not advance the original reconciliation or translation work. No source revalidation is claimed here.

The scope remains the latest summary PR, the latest discussions and conclusions in all eight other threads, their original PRs and shared base, and related integration findings, including findings outside PR reviews. Completing the other 81 locales is excluded. Checking a specifically implicated shared defect in another locale does not expand that scope to completing that locale.

## Rules for the reset

- The rejected [reconciliation report](localization-reconciliation-2026-09-28.md), including its version in [commit e51ab25c0](https://github.com/c933103/AN-Paint/blob/e51ab25c0/verification/localization-reconciliation-2026-09-28.md), contains **claims to recheck, not accepted evidence or accepted progress**.
- The same applies to every earlier handoff, review, semantic audit, evidence ledger, PR conclusion, assistant summary, checked box and completion statement within this scope. No conclusion inherits acceptance from another document.
- Existing code, translations, historical artifacts, commits and CI records are retained. They are neither erased nor assumed broken. Historical CI records are not rewritten to show failure; their relevance and claimed evidentiary value remain pending recheck.
- A previous positive, negative, partial, no-defect, coverage or evidence-gap assertion receives the same pending status. A previous resolved GitHub flag, passing test or document title grants no acceptance.
- Each item requires the original instruction/finding, relevant latest discussion, primary source or source behavior, and independent new validation as applicable. A claim about test coverage requires checking the assertion and actual execution, not merely finding the test name.
- If a row names several individual entries or cases, each must receive a separate recorded result during the recheck. Parent rows stay pending until all required cases have been independently checked. Individual locale and source-evidence rows are further expanded in [localization-evidence-rechecks.md](localization-evidence-rechecks.md); that companion does not inherit acceptance either.
- **Unlisted-claim rule:** every prior scoped claim not explicitly listed here is also pending full recheck. Before relying on it, add a stable individual item. Silence, omission, repetition and a previous report's bounded wording never carry progress forward.
- No item becomes accepted merely because a document was changed, a status reset was published or this register was counted. Any eventual status change needs its own new evidence and must respect the user's actual instruction.

This file lists **475 individually identified pending recheck rows**. These are reset entries, not completed checks. The companion register supplies additional granular locale/evidence rows.

## Scope, provenance and history

Prior claim location: Rejected report: opening; Evidence and limits. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| BASE-001 | Reconstruct the user-authorized task and every correction without inheriting the rejected delivery's interpretation. | Pending full recheck |
| BASE-002 | Map the eight other discussion threads to their original PRs and distinguish the shared base and integration discussion. | Pending full recheck |
| BASE-003 | Recheck the asserted application snapshot 50395ad05be90d9b19ef7223289760fa448bb581 and what was actually inspected. | Pending full recheck |
| BASE-004 | Recheck the asserted tree 4f9bc377504a76f43d128041a2f1794815940832 against the inspected application snapshot. | Pending full recheck |
| BASE-005 | Establish which original PR and integration heads are current at the time of the new recheck. | Pending full recheck |
| BASE-006 | Recover the latest summary PR's full conclusion, review bodies, comments and subsequent updates. | Pending full recheck |
| BASE-007 | Recover and read the latest relevant messages of each original thread; do not substitute retrospective summaries. | Pending full recheck |
| BASE-008 | Trace every reported conversation timestamp to its original message and timezone. | Pending full recheck |
| BASE-009 | Distinguish actual latest messages from merely latest retrieved excerpts. | Pending full recheck |
| BASE-010 | Distinguish user requirements and corrections from assistant claims or plans in recovered history. | Pending full recheck |
| BASE-011 | Recheck the assertion that targeted retrieval did not obtain complete latest transcripts. | Pending full recheck |
| BASE-012 | Recheck the assertion that matching conversation exports could not be located. | Pending full recheck |
| BASE-013 | Recheck the claim that the rejected report inventoried all obligations recoverable in its audit. | Pending full recheck |
| BASE-014 | Recheck the completeness of findings and updates outside GitHub inline comments. | Pending full recheck |
| BASE-015 | Recheck the negative claim that unseen later messages do not affect any particular disposition. | Pending full recheck |
| BASE-016 | Identify every inherited completion assertion in earlier audits; none is admissible as proof of itself. | Pending full recheck |
| BASE-017 | Independently derive the unfinished-work inventory; the earlier limit of two concrete defects is withdrawn. | Pending full recheck |
| BASE-018 | Recheck every claim that a historical pending task was implemented later. | Pending full recheck |
| BASE-019 | Recheck every assertion that existing substantive review establishes completion of an obligation. | Pending full recheck |
| BASE-020 | Keep source presence, semantic adequacy, test coverage, test execution and publication as separate requirements. | Pending full recheck |
| BASE-021 | Recheck whether the previous inspection covered actual source or only documents describing source. | Pending full recheck |
| BASE-022 | Record native-speaker certification and exhaustive corpus attestation only if an actual user requirement supports them. | Pending full recheck |
| BASE-023 | Recheck whether shared application changes belong only in integration or also in a particular original PR. | Pending full recheck |
| BASE-024 | Verify the final inventory against the original command and corrections before making any completion claim. | Pending full recheck |

## Earlier R1–R6 backlog, reopened

Prior claim location: Rejected report: Work still to be done. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| R-001 | R1: fully reconcile the latest conclusions of all eight other threads with the summary PR and actual work. | Pending full recheck |
| R-002 | R1: reconcile each additional correction, unfinished instruction and later conclusion individually. | Pending full recheck |
| R-003 | R2: recheck the diagnosis and wording of Malay ui_smooth_freehand_strokes. | Pending full recheck |
| R-004 | R2: recheck the diagnosis and wording of Malay ui_smooth_pixel_edges_anti_aliasing. | Pending full recheck |
| R-005 | R2: recheck the distinction between stroke smoothing and pixel-edge antialiasing. | Pending full recheck |
| R-006 | R2: establish and repair every affected original-PR and integration copy if the finding is confirmed. | Pending full recheck |
| R-007 | R3: compare the complete English legacy assembly paragraph with the Traditional Mongolian counterpart. | Pending full recheck |
| R-008 | R3: recheck the asserted omission of the up-to-20-images capacity clause. | Pending full recheck |
| R-009 | R3: recheck companion omissions or changed meanings in that same legacy paragraph. | Pending full recheck |
| R-010 | R3: independently check the separate assembly help; its result cannot close the legacy resource. | Pending full recheck |
| R-011 | R3: independently check active ui_help23 and the asserted distinction from the legacy resource. | Pending full recheck |
| R-012 | R3: establish every affected branch and publication requirement for any confirmed repair. | Pending full recheck |
| R-013 | R4: establish the original semantic-review obligation for each scoped language. | Pending full recheck |
| R-014 | R4: recheck the reported longer-than-100-characters cutoff for Malay and Indonesian non-manual review. | Pending full recheck |
| R-015 | R4: recheck the reported 62 Malay and 66 Indonesian reviewed-entry counts and snapshot. | Pending full recheck |
| R-016 | R4: enumerate and review every excluded Malay short control or message. | Pending full recheck |
| R-017 | R4: enumerate and review every excluded Indonesian short control or message. | Pending full recheck |
| R-018 | R4: establish and complete remaining review coverage separately for every PR4 language. | Pending full recheck |
| R-019 | R4: recheck rather than inherit claims of full Ainu, Manchu, Jeju and Okinawan review. | Pending full recheck |
| R-020 | R5: assess each newly confirmed shared defect across affected locales and script pairs. | Pending full recheck |
| R-021 | R5: assess each newly confirmed shared defect across active manuals, legacy manuals and duplicate hints. | Pending full recheck |
| R-022 | R5: assess each newly confirmed shared defect across labels, plurals, source defaults and app behavior. | Pending full recheck |
| R-023 | R5: distinguish a shared defect from a language-specific error before propagating a repair. | Pending full recheck |
| R-024 | R6: establish each needed source repair without assuming the rejected backlog is exhaustive. | Pending full recheck |
| R-025 | R6: validate and publish each confirmed repair to the required original and integration branches. | Pending full recheck |
| R-026 | R6: check intended and published trees, including removals, before claiming publication. | Pending full recheck |
| R-027 | R6: select and execute relevant structural, semantic, resource and Android checks for the repaired source. | Pending full recheck |
| R-028 | R6: replace conclusions only with independently established, bounded results. | Pending full recheck |
| R-029 | Recheck the earlier classification of R1 as only access, R4 as only review coverage and R5–R6 as only future acceptance work. | Pending full recheck |

## Shared base and PR2

Prior claim location: Rejected report: shared-base row and related non-PR rows. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| P02-001 | Recover all original direct-XML, upstream-reference and generator instructions. | Pending full recheck |
| P02-002 | Recheck that direct Android locale XML is canonical in the actual workflow. | Pending full recheck |
| P02-003 | Recheck Crowdin's per-locale XML mapping. | Pending full recheck |
| P02-004 | Recheck that validation reads XML rather than regenerating live translations. | Pending full recheck |
| P02-005 | Recheck absence of the old live translation generator and any equivalent generation route. | Pending full recheck |
| P02-006 | Recheck the assertion that historical JSON serves only as provenance. | Pending full recheck |
| P02-007 | Recheck whether upstream translations are treated as references rather than assumed authority. | Pending full recheck |
| P02-008 | Recheck coverage and required locale identities for the six claimed catalogues. | Pending full recheck |
| P02-009 | Recheck Japanese flip-control meanings against the actual controls. | Pending full recheck |
| P02-010 | Recheck Cantonese Fit wording and readings. | Pending full recheck |
| P02-011 | Recheck Cantonese italic wording and readings. | Pending full recheck |
| P02-012 | Recheck Cantonese line-spacing wording and readings. | Pending full recheck |
| P02-013 | Recheck contextual Cantonese row-versus-walking readings in every affected entry. | Pending full recheck |
| P02-014 | Recheck actual menu routes and captions cited by the base-caption audit. | Pending full recheck |
| P02-015 | Recheck the no-new-PR2-defect conclusion through the full required review. | Pending full recheck |

## PR3: Tagalog, Cebuano, Malay and Indonesian

Prior claim location: Rejected report: PR3 row and related non-PR rows. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| P03-001 | Recover the mechanical Cebuano corruption finding and the full scope of the required rewrite. | Pending full recheck |
| P03-002 | Recheck the claim that all 669 Cebuano entries were rewritten from English. | Pending full recheck |
| P03-003 | Recheck Cebuano word-level corruption beyond the specific examples previously identified. | Pending full recheck |
| P03-004 | Recheck Indonesian nyahaktif absence and every intended replacement's meaning. | Pending full recheck |
| P03-005 | Recheck broader Malay leakage in Indonesian; one removed token does not prove completion. | Pending full recheck |
| P03-006 | Recheck substantive Indonesian terminology changes including clipboard. | Pending full recheck |
| P03-007 | Recheck the claimed Cebuano draft-versus-initial-work repair. | Pending full recheck |
| P03-008 | Recheck Cebuano PDF crop's positive-width condition. | Pending full recheck |
| P03-009 | Recheck Cebuano PDF crop's positive-height condition. | Pending full recheck |
| P03-010 | Recheck Cebuano File borrowing against the actual context and required language register. | Pending full recheck |
| P03-011 | Recheck the change to the test that rejected legitimate technical borrowing. | Pending full recheck |
| P03-012 | Recheck each later help-route repair in all four languages. | Pending full recheck |
| P03-013 | Recheck each later navigation repair in all four languages. | Pending full recheck |
| P03-014 | Recheck each later zoom repair in all four languages. | Pending full recheck |
| P03-015 | Recheck structural and semantic coverage separately for Tagalog. | Pending full recheck |
| P03-016 | Recheck structural and semantic coverage separately for Cebuano. | Pending full recheck |
| P03-017 | Recheck structural and semantic coverage separately for Malay. | Pending full recheck |
| P03-018 | Recheck structural and semantic coverage separately for Indonesian. | Pending full recheck |
| P03-019 | Recheck the assertion that specific later repairs are implemented and preserved. | Pending full recheck |

## PR4: eight additional languages

Prior claim location: Rejected report: PR4 row and related non-PR rows. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| P04-001 | Recover the latest conclusions and original review obligations for all eight languages. | Pending full recheck |
| P04-002 | Recheck full required semantic coverage for Swahili. | Pending full recheck |
| P04-003 | Recheck full required semantic coverage for Finnish. | Pending full recheck |
| P04-004 | Recheck full required semantic coverage for Hungarian. | Pending full recheck |
| P04-005 | Recheck full required semantic coverage for Afrikaans. | Pending full recheck |
| P04-006 | Recheck full required semantic coverage for Dutch. | Pending full recheck |
| P04-007 | Recheck full required semantic coverage for Estonian. | Pending full recheck |
| P04-008 | Recheck full required semantic coverage for Latvian. | Pending full recheck |
| P04-009 | Recheck full required semantic coverage for Lithuanian. | Pending full recheck |
| P04-010 | Recheck Dutch tool captions individually against actual controls. | Pending full recheck |
| P04-011 | Recheck the Dutch decoder-memory condition and its error semantics. | Pending full recheck |
| P04-012 | Recheck Show all wording and routes across the affected languages. | Pending full recheck |
| P04-013 | Recheck Fit wording and routes across the affected languages. | Pending full recheck |
| P04-014 | Recheck Swap wording and routes across the affected languages. | Pending full recheck |
| P04-015 | Recheck placement clauses across the affected languages. | Pending full recheck |
| P04-016 | Recheck zoom clauses across the affected languages. | Pending full recheck |
| P04-017 | Recheck Lithuanian few plural form, selection behavior and meaning. | Pending full recheck |
| P04-018 | Recheck every Android apostrophe finding, including Dutch and Swahili. | Pending full recheck |
| P04-019 | Recheck Dutch Menu, Pixels and Canvas separately as deliberately retained appropriate terms. | Pending full recheck |
| P04-020 | Recheck Afrikaans Radius as a deliberately retained appropriate term. | Pending full recheck |
| P04-021 | Recheck the conclusion that historical lack of CI has been closed at the relevant current head. | Pending full recheck |
| P04-022 | Recheck the conclusion that all named PR4 findings are implemented. | Pending full recheck |

## PR5: Spanish variants, French, German, Russian, Arabic and Esperanto

Prior claim location: Rejected report: PR5 row and related non-PR rows. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| P05-001 | Recover the latest language-tail and terminology obligations rather than inheriting the final-ready claim. | Pending full recheck |
| P05-002 | Recheck both Spanish variants' required scope and remaining work separately. | Pending full recheck |
| P05-003 | Recheck the French tail and corrupted Star repair. | Pending full recheck |
| P05-004 | Recheck the German remaining-tail completion. | Pending full recheck |
| P05-005 | Recheck Russian one, few, many and other categories and their meanings individually. | Pending full recheck |
| P05-006 | Recheck Arabic zero, one, two, few, many and other categories and their meanings individually. | Pending full recheck |
| P05-007 | Recheck Arabic affected-count semantics. | Pending full recheck |
| P05-008 | Recheck Esperanto Fit meaning. | Pending full recheck |
| P05-009 | Recheck Esperanto foreground meaning. | Pending full recheck |
| P05-010 | Recheck Esperanto background meaning. | Pending full recheck |
| P05-011 | Recheck Esperanto cursor wording and actual behavior. | Pending full recheck |
| P05-012 | Recheck all claimed shared actual-caption and menu-route repairs. | Pending full recheck |
| P05-013 | Recheck the assertion that every concrete recovered PR5 task is implemented. | Pending full recheck |
| P05-014 | Recheck the no-additional-current-PR5-defect conclusion. | Pending full recheck |

## PR6: Literary Chinese, Hakka, Taiwanese and Wu

Prior claim location: Rejected report: PR6 row and related non-PR rows. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| P06-001 | Recover the latest Hakka regional-reading, script-pair and dictionary-gap instructions. | Pending full recheck |
| P06-002 | Recheck the Save Han/PFS synonym pairing itself. | Pending full recheck |
| P06-003 | Recheck all claimed 58 matching Save occurrences rather than a sample. | Pending full recheck |
| P06-004 | Recheck the remembered-choice clause in the Han catalogue. | Pending full recheck |
| P06-005 | Recheck the remembered-choice clause in the Latin catalogue. | Pending full recheck |
| P06-006 | Recheck contextual system terminology and PFS rendering. | Pending full recheck |
| P06-007 | Recheck Ministry Sixian entry identities and regional relevance. | Pending full recheck |
| P06-008 | Recheck dictionary-source hashes and provenance. | Pending full recheck |
| P06-009 | Recheck the mapping from official pronunciations to PFS. | Pending full recheck |
| P06-010 | Recheck every recorded dictionary decision and gap treatment; none inherits acceptance. | Pending full recheck |
| P06-011 | Recheck the asserted count of 47 dictionary decisions. | Pending full recheck |
| P06-012 | Recheck all Literary Chinese semantic substitutions covered by the original obligation. | Pending full recheck |
| P06-013 | Recheck all Taiwanese Han semantic substitutions covered by the original obligation. | Pending full recheck |
| P06-014 | Recheck all Taiwanese Latin/POJ pairings covered by the original obligation. | Pending full recheck |
| P06-015 | Recheck Wu conversion and language register. | Pending full recheck |
| P06-016 | Recheck Wu strikethrough wording. | Pending full recheck |
| P06-017 | Recheck Wu PDF error prose. | Pending full recheck |
| P06-018 | Recheck six-catalogue structural-check coverage and actual outcomes. | Pending full recheck |
| P06-019 | Recheck the statement that raw dictionary evidence was not replayed. | Pending full recheck |
| P06-020 | Recheck whether any original obligation remains unmet because dictionary evidence was not replayed. | Pending full recheck |
| P06-021 | Recheck the substantive-implementation-confirmed conclusion. | Pending full recheck |

## PR7: English variants, Portuguese variants, Italian, Greek and Turkish

Prior claim location: Rejected report: PR7 row and related non-PR rows. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| P07-001 | Recover the original default-English language-note deferral and later instruction. | Pending full recheck |
| P07-002 | Recheck the current default-English language note against the app's actual resource workflow. | Pending full recheck |
| P07-003 | Recheck the precise scope and identities of the seven English variants. | Pending full recheck |
| P07-004 | Recheck European Portuguese configuration identity. | Pending full recheck |
| P07-005 | Recheck duplicate Portuguese configuration removal. | Pending full recheck |
| P07-006 | Recheck the equivalent-qualifier guard and its relevant cases. | Pending full recheck |
| P07-007 | Recheck Brazilian Portuguese substantive semantic changes. | Pending full recheck |
| P07-008 | Recheck Brazilian Portuguese clipboard terminology. | Pending full recheck |
| P07-009 | Recheck the assertion that the entire Brazilian Portuguese rewrite is preserved. | Pending full recheck |
| P07-010 | Recheck Italian full required scope and unresolved obligations. | Pending full recheck |
| P07-011 | Recheck Greek full required scope and unresolved obligations. | Pending full recheck |
| P07-012 | Recheck Turkish full required scope and unresolved obligations. | Pending full recheck |
| P07-013 | Recheck every source and translated menu-route repair claimed for this PR. | Pending full recheck |
| P07-014 | Recheck twelve-catalogue coverage and whether it meets the actual instruction. | Pending full recheck |
| P07-015 | Recheck the deferred-tasks-implemented conclusion. | Pending full recheck |
| P07-016 | Recheck the no-additional-current-PR7-defect conclusion. | Pending full recheck |

## PR8: Tibetan, Dzongkha and both Mongolian scripts

Prior claim location: Rejected report: PR8 row and related non-PR rows. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| P08-001 | Recover the Tibetan remaining-tail status without confusing remaining entries with completed entries. | Pending full recheck |
| P08-002 | Recheck Tibetan codec and export tail. | Pending full recheck |
| P08-003 | Recheck Tibetan gallery and cursor tail. | Pending full recheck |
| P08-004 | Recheck Dzongkha Keep editing meaning against the actual action. | Pending full recheck |
| P08-005 | Recheck the asserted Keep editing repair commit 6d591aa6f and timestamp. | Pending full recheck |
| P08-006 | Recheck Dzongkha format and gallery tail. | Pending full recheck |
| P08-007 | Recheck Dzongkha save and import tail. | Pending full recheck |
| P08-008 | Recheck independent Dzongkha wording rather than inherited Tibetan substitutions. | Pending full recheck |
| P08-009 | Recheck complete required scope for Cyrillic Mongolian. | Pending full recheck |
| P08-010 | Recheck complete required scope for Traditional Mongolian. | Pending full recheck |
| P08-011 | Recheck later source and credit wording in every affected catalogue. | Pending full recheck |
| P08-012 | Recheck later save-before-sharing wording in every affected catalogue. | Pending full recheck |
| P08-013 | Recheck later destination wording in every affected catalogue. | Pending full recheck |
| P08-014 | Recheck later menu-caption repairs in every affected catalogue. | Pending full recheck |
| P08-015 | Recheck later dithering wording in every affected catalogue. | Pending full recheck |
| P08-016 | Recheck all separate assembly operational clauses. | Pending full recheck |
| P08-017 | Recheck Irasutoya licensing conditions. | Pending full recheck |
| P08-018 | Recheck the assertion that all four historical tails are structurally present. | Pending full recheck |
| P08-019 | Recheck the conclusion that historical tail and Keep editing obligations are closed. | Pending full recheck |
| P08-020 | Recheck the conclusion that the known legacy capacity clause is the only residual manual issue. | Pending full recheck |

## PR9: Jeju, Manchu, Ainu and Okinawan

Prior claim location: Rejected report: PR9 row and related non-PR rows. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| P09-001 | Recover the latest original Jeju, Manchu, Ainu and Okinawan instructions separately. | Pending full recheck |
| P09-002 | Recheck the Manchu progress correction of 625 complete and 44 remaining against original history. | Pending full recheck |
| P09-003 | Recheck all five catalogue identities and complete required scope. | Pending full recheck |
| P09-004 | Recheck jje registration. | Pending full recheck |
| P09-005 | Recheck cju migration without unintended current registration. | Pending full recheck |
| P09-006 | Recheck the stale cju test repair. | Pending full recheck |
| P09-007 | Recheck Jeju whole-clause grammar review and actual language adequacy. | Pending full recheck |
| P09-008 | Recheck Jeju finite-predicate review and repairs. | Pending full recheck |
| P09-009 | Recheck Jeju memory-wording repairs. | Pending full recheck |
| P09-010 | Recheck the claimed full source-assisted Ainu Latin review. | Pending full recheck |
| P09-011 | Recheck the claimed full source-assisted Ainu Kana review. | Pending full recheck |
| P09-012 | Recheck Ainu file-count versus file-size meaning. | Pending full recheck |
| P09-013 | Recheck Ainu Select all instruction placement. | Pending full recheck |
| P09-014 | Recheck Manchu lexical review and actual repairs. | Pending full recheck |
| P09-015 | Recheck Manchu Unicode conversion. | Pending full recheck |
| P09-016 | Recheck Manchu newline-corruption repair. | Pending full recheck |
| P09-017 | Recheck Manchu partial-transliteration repair. | Pending full recheck |
| P09-018 | Recheck Manchu glyph checks and the exact text covered. | Pending full recheck |
| P09-019 | Recheck the claimed full Okinawan grammar review. | Pending full recheck |
| P09-020 | Recheck Okinawan short-action grammar. | Pending full recheck |
| P09-021 | Recheck Okinawan connected-polygon-segment meaning. | Pending full recheck |
| P09-022 | Recheck Okinawan selection/aspect-ratio control caption. | Pending full recheck |
| P09-023 | Recheck the no-new-current-PR9-defect conclusion. | Pending full recheck |

## PR12: Korean variants, mixed-script Korean, Vietnamese and Nôm

Prior claim location: Rejected report: PR12 row and related non-PR rows. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| P12-001 | Recover the user's mixed-script correction and latest evidence requirements. | Pending full recheck |
| P12-002 | Recheck ko-Kore-KR registration and actual mixed-script behavior. | Pending full recheck |
| P12-003 | Recheck complete required scope for South Korean. | Pending full recheck |
| P12-004 | Recheck complete required scope for North Korean. | Pending full recheck |
| P12-005 | Recheck complete required scope for mixed-script Korean. | Pending full recheck |
| P12-006 | Recheck complete required scope for Vietnamese. | Pending full recheck |
| P12-007 | Recheck complete required scope for Nôm. | Pending full recheck |
| P12-008 | Recheck every inventory example against current XML, including plural resources; use the companion evidence register. | Pending full recheck |
| P12-009 | Recheck the asserted total of 97 inventory entries. | Pending full recheck |
| P12-010 | Recheck the asserted 91 exact dictionary-evidence decisions. | Pending full recheck |
| P12-011 | Recheck the asserted six editorial-evidence decisions. | Pending full recheck |
| P12-012 | Recheck general-domain evidence breadth against the original requirement. | Pending full recheck |
| P12-013 | Recheck whether reliance on Bible-only evidence was actually remedied. | Pending full recheck |
| P12-014 | Recheck literary corpus provenance, source identities and hashes. | Pending full recheck |
| P12-015 | Recheck literary occurrence offsets and exact source text. | Pending full recheck |
| P12-016 | Recheck each literary occurrence's accepted or rejected status. | Pending full recheck |
| P12-017 | Recheck the claimed 42 literary occurrences, 41 accepted and one rejected. | Pending full recheck |
| P12-018 | Recheck civic-source provenance and the actual Gazette or other primary records. | Pending full recheck |
| P12-019 | Recheck all 12 claimed civic spans against primary sources. | Pending full recheck |
| P12-020 | Recheck the accepted-pair union and claimed 47 distinct app pairs. | Pending full recheck |
| P12-021 | Recheck source-verifier behavior and whether it was actually executed on available raw data. | Pending full recheck |
| P12-022 | Recheck the assertion that 254 MB of raw corpus was absent locally. | Pending full recheck |
| P12-023 | Recheck the assertion that raw corpus and Gazette sources were not freshly replayed. | Pending full recheck |
| P12-024 | Recheck the remaining inventory pairs without assuming absence of corpus evidence proves correctness or error. | Pending full recheck |
| P12-025 | Recheck the image concept decision and its actual uses. | Pending full recheck |
| P12-026 | Recheck the colour concept decision and its actual uses. | Pending full recheck |
| P12-027 | Recheck the settings concept decision and its actual uses. | Pending full recheck |
| P12-028 | Recheck the save concept decision and its actual uses. | Pending full recheck |
| P12-029 | Recheck the select concept decision and its actual uses. | Pending full recheck |
| P12-030 | Recheck the edit concept decision and its actual uses. | Pending full recheck |
| P12-031 | Recheck the file concept decision and its actual uses. | Pending full recheck |
| P12-032 | Recheck the memory concept decision and its actual uses. | Pending full recheck |
| P12-033 | Recheck the North Korean PDF dimensions warning and the alleged too-cursor corruption repair. | Pending full recheck |
| P12-034 | Recheck every Nôm contextual homophone decision in the companion evidence register. | Pending full recheck |
| P12-035 | Recheck the claimed 404-string Nôm semantic batch. | Pending full recheck |
| P12-036 | Recheck the claimed 405 changed values against the stated older baseline. | Pending full recheck |
| P12-037 | Recheck the explanation of the 404-versus-405 difference. | Pending full recheck |
| P12-038 | Recheck whether final Nôm source edits were included in the font rebuild. | Pending full recheck |
| P12-039 | Recheck coverage of all claimed 622 used Nôm ideographs. | Pending full recheck |
| P12-040 | Recheck coverage of all claimed 157 supplementary Nôm ideographs. | Pending full recheck |
| P12-041 | Recheck the no-new-current-PR12-defect conclusion. | Pending full recheck |
| P12-042 | Recheck the inventory, corpus, script-registration and named-repairs-implemented conclusions separately. | Pending full recheck |

## Shared credits behavior

Prior claim location: Rejected report: non-PR credit discoveries. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| CR-001 | Recheck document-specific ownership of credits. | Pending full recheck |
| CR-002 | Recheck that insertion starts do not commit credits prematurely. | Pending full recheck |
| CR-003 | Recheck that committed insertion adds the intended credits. | Pending full recheck |
| CR-004 | Recheck cancelled insertion leaves no unwanted credits. | Pending full recheck |
| CR-005 | Recheck undo restores the intended credit state. | Pending full recheck |
| CR-006 | Recheck redo restores the intended credit state. | Pending full recheck |
| CR-007 | Recheck clipboard credit ownership and transfer. | Pending full recheck |
| CR-008 | Recheck repeated insertion behavior. | Pending full recheck |
| CR-009 | Recheck clearing a document clears the intended credits. | Pending full recheck |
| CR-010 | Recheck a new document starts with the intended credit state. | Pending full recheck |
| CR-011 | Recheck draft restoration restores matching credits. | Pending full recheck |
| CR-012 | Recheck history restoration restores matching credits. | Pending full recheck |
| CR-013 | Recheck credit editing interactions with document history. | Pending full recheck |
| CR-014 | Recheck gallery edited-credit results survive activity recreation. | Pending full recheck |
| CR-015 | Recheck gallery unchanged-credit exits preserve the intended result. | Pending full recheck |
| CR-016 | Recheck Save dialog credits start collapsed. | Pending full recheck |
| CR-017 | Recheck Export dialog credits start collapsed. | Pending full recheck |
| CR-018 | Recheck Save dialog credit text is selectable. | Pending full recheck |
| CR-019 | Recheck Export dialog credit text is selectable. | Pending full recheck |
| CR-020 | Recheck Save dialog Copy all behavior. | Pending full recheck |
| CR-021 | Recheck Export dialog Copy all behavior. | Pending full recheck |
| CR-022 | Recheck copying credits does not start a save or export. | Pending full recheck |
| CR-023 | Recheck preservation of original credit language. | Pending full recheck |
| CR-024 | Recheck each credit regression test's existence, assertions, covered paths and execution independently. | Pending full recheck |

## Vertical UI, emoji, fonts and locale migrations

Prior claim location: Rejected report: non-PR typography discoveries. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| TY-001 | Recheck Mongolian vertical layout and left-to-right column progression. | Pending full recheck |
| TY-002 | Recheck Manchu vertical layout and left-to-right column progression. | Pending full recheck |
| TY-003 | Recheck Literary Chinese vertical layout and right-to-left column progression. | Pending full recheck |
| TY-004 | Recheck en-XV registration and selection. | Pending full recheck |
| TY-005 | Recheck en-XV persistence and round-trip. | Pending full recheck |
| TY-006 | Recheck qaa-Zsye-XV registration and selection. | Pending full recheck |
| TY-007 | Recheck qaa-Zsye-XV persistence and round-trip. | Pending full recheck |
| TY-008 | Recheck BMP checkmark upright rendering. | Pending full recheck |
| TY-009 | Recheck BMP gear upright rendering. | Pending full recheck |
| TY-010 | Recheck variation-selector clustering and orientation. | Pending full recheck |
| TY-011 | Recheck keycap clustering and orientation. | Pending full recheck |
| TY-012 | Recheck subdivision-flag tag clustering. | Pending full recheck |
| TY-013 | Recheck emoji cluster measurement. | Pending full recheck |
| TY-014 | Recheck emoji cluster wrapping. | Pending full recheck |
| TY-015 | Recheck web-gallery AN Paint controls use the intended embedded fonts. | Pending full recheck |
| TY-016 | Recheck web-gallery styles are scoped to the intended controls. | Pending full recheck |
| TY-017 | Recheck web-gallery vertical direction and layout. | Pending full recheck |
| TY-018 | Recheck gallery font bytes and source-asset association. | Pending full recheck |
| TY-019 | Recheck font application on untagged controls. | Pending full recheck |
| TY-020 | Recheck font application on newly added controls. | Pending full recheck |
| TY-021 | Recheck UI-only font exclusion from drawing-font choices. | Pending full recheck |
| TY-022 | Recheck preservation of the user's selected drawing font. | Pending full recheck |
| TY-023 | Recheck loading of every advertised bundled font's actual file. | Pending full recheck |
| TY-024 | Recheck per-font asset/hash assertions and absence of weakened test coverage. | Pending full recheck |
| TY-025 | Recheck Wu UI fallback behavior. | Pending full recheck |
| TY-026 | Recheck Nôm UI fallback behavior independently of drawing fonts. | Pending full recheck |
| TY-027 | Recheck Hakka Taiwan locale tags. | Pending full recheck |
| TY-028 | Recheck Hakka preference migration on the pre-platform-locale path. | Pending full recheck |
| TY-029 | Recheck Hakka preference migration on the platform-locale path. | Pending full recheck |
| TY-030 | Recheck the assertion that the relevant font and gallery changes are present in PR12 and integration. | Pending full recheck |
| TY-031 | Recheck the historical-font-crash-closed conclusion. | Pending full recheck |
| TY-032 | Recheck each named typography, locale and native-font test's actual assertions and execution. | Pending full recheck |

## Shared help, routes and formatting

Prior claim location: Rejected report: non-PR help and validator discoveries. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| HELP-001 | Recheck static literal-percent handling with formatted=false. | Pending full recheck |
| HELP-002 | Recheck runtime formatting and escaped-percent handling. | Pending full recheck |
| HELP-003 | Recheck percent-regression test coverage against actual failure cases. | Pending full recheck |
| HELP-004 | Recheck the local Kotlin/Maven access diagnosis and its relationship to source failures. | Pending full recheck |
| HELP-005 | Recheck gallery routes in the first active help resource. | Pending full recheck |
| HELP-006 | Recheck gallery routes in the second active help resource. | Pending full recheck |
| HELP-007 | Recheck gallery routes in the third active help resource. | Pending full recheck |
| HELP-008 | Recheck the final copyright paragraph separately from gallery routes. | Pending full recheck |
| HELP-009 | Recheck relevant legacy gallery help resources separately from active help. | Pending full recheck |
| HELP-010 | Recheck the asserted initial 54 failing subchecks and each claimed repair. | Pending full recheck |
| HELP-011 | Recheck any later residual subchecks and each claimed repair. | Pending full recheck |
| HELP-012 | Recheck nonexistent Show all changes caption replacements. | Pending full recheck |
| HELP-013 | Recheck Fit captions and help references. | Pending full recheck |
| HELP-014 | Recheck Swap captions and help references. | Pending full recheck |
| HELP-015 | Recheck Navigate captions and help references. | Pending full recheck |
| HELP-016 | Recheck obsolete File routes. | Pending full recheck |
| HELP-017 | Recheck obsolete Draw routes. | Pending full recheck |
| HELP-018 | Recheck Armenian cursor-settings help. | Pending full recheck |
| HELP-019 | Recheck Serbian Cyrillic cursor-settings help. | Pending full recheck |
| HELP-020 | Recheck Serbian Latin cursor-settings help. | Pending full recheck |
| HELP-021 | Recheck Hebrew cursor-settings help. | Pending full recheck |
| HELP-022 | Recheck Polish cursor-settings help. | Pending full recheck |
| HELP-023 | Recheck Thai cursor-settings help. | Pending full recheck |
| HELP-024 | Recheck alias-aware cursor-help validation. | Pending full recheck |
| HELP-025 | Recheck active copy/paste hint routing. | Pending full recheck |
| HELP-026 | Recheck retained duplicate copy/paste hint routing. | Pending full recheck |
| HELP-027 | Recheck every affected locale for obsolete File-to-Insert-image hint wording. | Pending full recheck |
| HELP-028 | Recheck the actual Lock proportions control caption and selection-tooltip meaning. | Pending full recheck |
| HELP-029 | Recheck Japanese selection-tooltip repair. | Pending full recheck |
| HELP-030 | Recheck Russian selection-tooltip repair. | Pending full recheck |
| HELP-031 | Recheck Swahili selection-tooltip repair. | Pending full recheck |
| HELP-032 | Recheck other affected locales for the same wrong-caption substitution. | Pending full recheck |
| HELP-033 | Recheck validator acceptance of valid native paraphrases. | Pending full recheck |
| HELP-034 | Recheck each global help check's actual locale/resource reach and blind spots. | Pending full recheck |

## Inline findings and discussion inventory

Prior claim location: Rejected report: Inline PR findings and current publication. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| GH-001 | Recheck the total of 15 inline findings against complete GitHub retrieval. | Pending full recheck |
| GH-002 | Recheck the total of seven submitted review bodies. | Pending full recheck |
| GH-003 | Recheck the total of eleven issue-discussion records. | Pending full recheck |
| GH-004 | Recheck the negative claim that review bodies contain no additional substantive findings. | Pending full recheck |
| GH-005 | Recheck the assertion that PR2 received only quota notices rather than a submitted code review. | Pending full recheck |
| GH-006 | Recheck the assertion that PR3 received only quota notices rather than a submitted code review. | Pending full recheck |
| GH-007 | Recheck the assertion that PR15 had no submitted review at the cited retrieval. | Pending full recheck |
| GH-008 | Recheck the asserted resolved state of every inline thread; resolved is not accepted completion. | Pending full recheck |
| GH-009 | Recheck the relationship between old review commits and each current repaired head. | Pending full recheck |
| GH-010 | Recheck whether any later review, issue comment or discussion adds a requirement. | Pending full recheck |
| GH-011 | Inline finding 01: PR4 Android apostrophe handling, including every locale implicated by the original comment. | Pending full recheck |
| GH-012 | Inline finding 02: PR4 Lithuanian few plural category and semantics. | Pending full recheck |
| GH-013 | Inline finding 03: PR5 French Star corruption. | Pending full recheck |
| GH-014 | Inline finding 04: PR6 protected Base64 prefix. | Pending full recheck |
| GH-015 | Inline finding 05: PR6 CC BY-SA identifier. | Pending full recheck |
| GH-016 | Inline finding 06: PR6 GIF numeric limit. | Pending full recheck |
| GH-017 | Inline finding 07: PR6 Literary Chinese image-replacement versus foreground meaning. | Pending full recheck |
| GH-018 | Inline finding 08: PR7 duplicate European Portuguese configuration. | Pending full recheck |
| GH-019 | Inline finding 09: PR8 truncated legacy manual, including every omitted clause. | Pending full recheck |
| GH-020 | Inline finding 10: PR8 Traditional Mongolian assembly operational omissions. | Pending full recheck |
| GH-021 | Inline finding 11: PR8 Irasutoya licensing conditions. | Pending full recheck |
| GH-022 | Inline finding 12: PR9 stale cju test assertion. | Pending full recheck |
| GH-023 | Inline finding 13: PR9 Manchu vertical UI. | Pending full recheck |
| GH-024 | Inline finding 14: PR12 Nôm font coverage. | Pending full recheck |
| GH-025 | Inline finding 15: PR12 Korean regex escaping. | Pending full recheck |
| GH-026 | Reconcile the provisional numbered inline-finding mapping above against original comment IDs; split or correct it without dropping an obligation. | Pending full recheck |
| GH-027 | Recheck all relevant guards associated with the inline findings; presence alone is not proof of adequacy. | Pending full recheck |
| GH-028 | Recheck the conclusion that only the residual PR8 finding remains open. | Pending full recheck |

## Recovery, publication and validation claims

Prior claim location: Rejected report: recovery row and publication section. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| REC-001 | Recheck the old-workspace-snapshot incident and exactly what unpublished work was missing. | Pending full recheck |
| REC-002 | Recheck recovery checkpoint 1c924c6178 and what it actually restores. | Pending full recheck |
| REC-003 | Recheck recovery checkpoint 7309e1b1b and what it actually restores. | Pending full recheck |
| REC-004 | Recheck recovery checkpoint 0c8ac3fe6 and what it actually restores. | Pending full recheck |
| REC-005 | Recheck the claim that all recovered published work is preserved. | Pending full recheck |
| REC-006 | Recheck the total of 57 owned locale XML files and the ownership mapping. | Pending full recheck |
| REC-007 | Recheck 669-string coverage separately for every claimed locale in the companion evidence register. | Pending full recheck |
| REC-008 | Recheck the required plural resource separately for every claimed locale in the companion evidence register. | Pending full recheck |
| REC-009 | Recheck every owned XML's byte parity in the companion evidence register. | Pending full recheck |
| REC-010 | Recheck missing owned-locale paths. | Pending full recheck |
| REC-011 | Recheck duplicate owned-locale paths. | Pending full recheck |
| REC-012 | Recheck the assertion that each original head is included in integration. | Pending full recheck |
| REC-013 | Recheck the placement and completeness of shared application changes omitted from original language branches. | Pending full recheck |
| REC-014 | Recheck the earlier 109 host-check count and exact set of checks. | Pending full recheck |
| REC-015 | Recheck the execution and outcomes of those host checks at the cited snapshot. | Pending full recheck |
| REC-016 | Recheck strict resource-compilation execution and outcome at the cited snapshot. | Pending full recheck |
| REC-017 | Recheck the claim that current CI is green as a whole. | Pending full recheck |
| REC-018 | Recheck the assertion that no PR has been merged. | Pending full recheck |
| REC-019 | Recheck that the previous delivery changed documentation only. | Pending full recheck |
| REC-020 | Recheck that the previous delivery did not rerun Android tests. | Pending full recheck |
| REC-021 | Recheck CI.md's documentation-only treatment. | Pending full recheck |
| REC-022 | Recheck the actual workflow's Markdown and historical-verification path exclusions. | Pending full recheck |
| REC-023 | Recheck whether any previous result was incorrectly presented as validating new source repairs. | Pending full recheck |
| REC-024 | Recheck every published tree against the intended tree, including deletions. | Pending full recheck |

## Rejected delivery's documentation and communicated progress

Prior claim location: Rejected report, altered audit documents, PR15 body and delivery message. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| DOC-001 | Recheck every paragraph added or changed in the rejected reconciliation report. | Pending full recheck |
| DOC-002 | Recheck every status edit to localization-thread-handoffs.md. | Pending full recheck |
| DOC-003 | Recheck every status edit to translations/PR_REVIEW_AUDIT.md. | Pending full recheck |
| DOC-004 | Recheck every status edit to localization-integration-review.md. | Pending full recheck |
| DOC-005 | Recheck any other document changed as part of the rejected delivery. | Pending full recheck |
| DOC-006 | Recheck the documentation's Manchu progress correction. | Pending full recheck |
| DOC-007 | Recheck the documentation's residual PR8 reopening. | Pending full recheck |
| DOC-008 | Recheck replacements of broad completion claims and whether they still carry unsupported progress. | Pending full recheck |
| DOC-009 | Recheck every statement in the previous PR15 body update. | Pending full recheck |
| DOC-010 | Recheck every previous checked task box or completion marker associated with the scoped work. | Pending full recheck |
| DOC-011 | Recheck every previous thread-resolution or finding-closure action associated with the scoped work. | Pending full recheck |
| DOC-012 | Recheck every plan item previously marked complete or progressed. | Pending full recheck |
| DOC-013 | Recheck every final-answer statement presenting the delivery as completed reconciliation. | Pending full recheck |
| DOC-014 | Recheck the claim that the documentation corrections are already done. | Pending full recheck |
| DOC-015 | Recheck whether the delivered local file matches the published report. | Pending full recheck |
| DOC-016 | Recheck publication identity and contents of commit e51ab25c0. | Pending full recheck |
| DOC-017 | Recheck the register's own coverage against every claim in the rejected delivery. | Pending full recheck |
| DOC-018 | Capture every unlisted prior claim as a new pending item before using it; omission grants no acceptance. | Pending full recheck |

## PR02: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB02-001 | Recheck PR02's authorized scope, actual current head and the earlier assertion that 8cf4ed2e5 was inspected. | Pending full recheck |
| PUB02-002 | Recheck PR02's claimed 6 owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB02-003 | Recheck PR02's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB02-004 | Recheck PR02's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB02-005 | Recheck run 36175227320's association with PR02, exact source commit and workflow. | Pending full recheck |
| PUB02-006 | Recheck run 36175227320's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB02-007 | Recheck whether any later PR02 change invalidates the cited run's relevance. | Pending full recheck |

## PR03: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB03-001 | Recheck PR03's authorized scope, actual current head and the earlier assertion that 8a3a17ca1 was inspected. | Pending full recheck |
| PUB03-002 | Recheck PR03's claimed 4 owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB03-003 | Recheck PR03's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB03-004 | Recheck PR03's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB03-005 | Recheck run 36175252567's association with PR03, exact source commit and workflow. | Pending full recheck |
| PUB03-006 | Recheck run 36175252567's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB03-007 | Recheck whether any later PR03 change invalidates the cited run's relevance. | Pending full recheck |

## PR04: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB04-001 | Recheck PR04's authorized scope, actual current head and the earlier assertion that c07dfb366 was inspected. | Pending full recheck |
| PUB04-002 | Recheck PR04's claimed 8 owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB04-003 | Recheck PR04's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB04-004 | Recheck PR04's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB04-005 | Recheck run 36175278920's association with PR04, exact source commit and workflow. | Pending full recheck |
| PUB04-006 | Recheck run 36175278920's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB04-007 | Recheck whether any later PR04 change invalidates the cited run's relevance. | Pending full recheck |

## PR05: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB05-001 | Recheck PR05's authorized scope, actual current head and the earlier assertion that aeec0d053 was inspected. | Pending full recheck |
| PUB05-002 | Recheck PR05's claimed 7 owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB05-003 | Recheck PR05's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB05-004 | Recheck PR05's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB05-005 | Recheck run 36175302649's association with PR05, exact source commit and workflow. | Pending full recheck |
| PUB05-006 | Recheck run 36175302649's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB05-007 | Recheck whether any later PR05 change invalidates the cited run's relevance. | Pending full recheck |

## PR06: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB06-001 | Recheck PR06's authorized scope, actual current head and the earlier assertion that d7de53e33 was inspected. | Pending full recheck |
| PUB06-002 | Recheck PR06's claimed 6 owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB06-003 | Recheck PR06's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB06-004 | Recheck PR06's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB06-005 | Recheck run 36175454796's association with PR06, exact source commit and workflow. | Pending full recheck |
| PUB06-006 | Recheck run 36175454796's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB06-007 | Recheck whether any later PR06 change invalidates the cited run's relevance. | Pending full recheck |

## PR07: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB07-001 | Recheck PR07's authorized scope, actual current head and the earlier assertion that b528c9d2a was inspected. | Pending full recheck |
| PUB07-002 | Recheck PR07's claimed 12 owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB07-003 | Recheck PR07's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB07-004 | Recheck PR07's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB07-005 | Recheck run 36175478621's association with PR07, exact source commit and workflow. | Pending full recheck |
| PUB07-006 | Recheck run 36175478621's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB07-007 | Recheck whether any later PR07 change invalidates the cited run's relevance. | Pending full recheck |

## PR08: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB08-001 | Recheck PR08's authorized scope, actual current head and the earlier assertion that 72aa3bd2c was inspected. | Pending full recheck |
| PUB08-002 | Recheck PR08's claimed 4 owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB08-003 | Recheck PR08's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB08-004 | Recheck PR08's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB08-005 | Recheck run 36175503191's association with PR08, exact source commit and workflow. | Pending full recheck |
| PUB08-006 | Recheck run 36175503191's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB08-007 | Recheck whether any later PR08 change invalidates the cited run's relevance. | Pending full recheck |

## PR09: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB09-001 | Recheck PR09's authorized scope, actual current head and the earlier assertion that 97e511dc6 was inspected. | Pending full recheck |
| PUB09-002 | Recheck PR09's claimed 5 owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB09-003 | Recheck PR09's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB09-004 | Recheck PR09's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB09-005 | Recheck run 36175529316's association with PR09, exact source commit and workflow. | Pending full recheck |
| PUB09-006 | Recheck run 36175529316's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB09-007 | Recheck whether any later PR09 change invalidates the cited run's relevance. | Pending full recheck |

## PR12: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB12-001 | Recheck PR12's authorized scope, actual current head and the earlier assertion that 3d674096f was inspected. | Pending full recheck |
| PUB12-002 | Recheck PR12's claimed 5 owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB12-003 | Recheck PR12's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB12-004 | Recheck PR12's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB12-005 | Recheck run 36175559899's association with PR12, exact source commit and workflow. | Pending full recheck |
| PUB12-006 | Recheck run 36175559899's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB12-007 | Recheck whether any later PR12 change invalidates the cited run's relevance. | Pending full recheck |

## PR15: independent scope, parity and CI rechecks

Prior claim location: Rejected report: publication table. This location identifies a rejected assertion; it does not verify it.

| ID | Individual full-recheck requirement | Status |
| --- | --- | --- |
| PUB15-001 | Recheck PR15's authorized scope, actual current head and the earlier assertion that 50395ad05 was inspected. | Pending full recheck |
| PUB15-002 | Recheck PR15's claimed combined owned-locale coverage against the user's requirements and exact paths. | Pending full recheck |
| PUB15-003 | Recheck PR15's claimed original/integration parity individually for every owned locale or combined scope. | Pending full recheck |
| PUB15-004 | Recheck PR15's publication and incorporation into the intended integration source. | Pending full recheck |
| PUB15-005 | Recheck run 36175711603's association with PR15, exact source commit and workflow. | Pending full recheck |
| PUB15-006 | Recheck run 36175711603's actual conclusion and the precise tests/build steps it covered. | Pending full recheck |
| PUB15-007 | Recheck whether any later PR15 change invalidates the cited run's relevance. | Pending full recheck |
