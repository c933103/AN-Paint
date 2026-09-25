# Recovered localization conversation handoffs

Resumed 25 September 2026 after the user identified that the earlier integration
had not actually finished the work left in the branched conversations.

This inventory uses retrieved conversation handoff records, original Git
snapshots, and the current source. The records are summaries and excerpts, not
complete transcripts or recovered unpublished workspaces. Earlier resource
counts, “ready” messages, resolved review flags, and successful builds are not
treated as proof of linguistic completion. The earlier blanket completion claim
is withdrawn. All edits are direct Android XML edits; no runtime translation or
character-transliteration generator is introduced.

## Eight branches and their shared base

Times below are UTC. Status refers to the recovered obligation, not independent
native-speaker certification of every sentence in a language.

| Conversation / PR | Last relevant recovered handoff | What the resumed review must establish | Source disposition |
| --- | --- | --- | --- |
| Tagalog, Cebuano, Malay, Indonesian / #3 | 22 Sep 06:54: reported ready after mechanical Cebuano corruption and Malay leakage into Indonesian had been repaired; CI remained pending. | Independently read the repaired Cebuano technical/manual prose and Indonesian/Malay clauses rather than accept the earlier claim. | Cebuano manuals and codec/memory warnings rewritten; independent reviewer found draft-versus-initial-work and positive-area crop ambiguities, now assigned back to the author. Indonesian zoom, assembly direction and actual-caption repairs integrated. See the branch audit when final corrections land. |
| Swahili, Finnish, Hungarian, Afrikaans, Dutch, Estonian, Latvian, Lithuanian / #4 | 23 Sep 00:40: 669-resource/structural completion reported; no CI for original `1711f55e6d`. | Check semantic consequences of substitutions and shared help defects, in addition to apostrophes and plurals. | Dutch airbrush/curve/assembly captions and decoder-memory conditions repaired. Actual Show all/Swap/Fit and attachment directions reviewed across this batch. Original two review findings remain globally guarded. |
| Spanish variants, French, German, Russian, Arabic, Esperanto / #5 | 23 Sep 03:12–03:23: Arabic six plurals, quote/terminology fixes, and Esperanto completion reported; CI pending. | Preserve grammar-specific plural meanings, inspect long-help control names and resolve the French substitution review. | Arabic zero/one/two now describe the affected count, not an invented subset. French star and shared Show all repairs apply to relevant tool/help entries. Active and legacy routes corrected. See `localization-mainstream-himalayan-handoff.md`. |
| Literary Chinese, Hakka scripts, Taiwanese scripts, Wu / #6 | 23 Sep 17:20: “picking up exactly at the Ministry Hakka dictionary inspection”; Sixian PFS generation/checking, dictionary-gap cleanup, validation and stacked PR still promised. Earlier Wu register/conversion cleanup also remained. | Finish the Ministry Sixian mapping and Han/PFS meaning comparison, then review Taiwanese pairs, Literary Chinese and Wu independently. | Hakka full paired-resource comparison and 47 contextual decisions recorded with Ministry entry IDs/hash; incorrect first readings, missing remembered-choice clause and stale routes repaired. Literary Chinese 29-entry and Wu 99-entry semantic batches integrated. Taiwanese review remains active until its paired audit lands. See `localization-sinitic-audit.md`. |
| English variants, Portuguese variants, Italian, Greek, Turkish / #7 | 23 Sep 03:02: default-English language note deliberately deferred; 05:21–05:24: twelve locales reported ready, duplicate pt-PT and CI base filter unresolved. | Close the explicitly deferred source-English obligation; preserve one Android pt-PT configuration and actual controls in all variants. | Source/default and translated language notes corrected; canonical pt-PT and global equivalent-qualifier gate retained. English and translated manuals now name actual import/assembly routes and controls. See the mainstream/Himalayan audit. |
| Tibetan, Dzongkha, Mongolian scripts / #8 | 23 Sep 00:54: Tibetan still at resource 123 before codec/export/gallery/cursor tail and Dzongkha. 05:30: Dzongkha Keep editing pending. 05:34: four complete catalogues claimed. | Read the actual long manual targeted by review, check operational clauses and original commit before calling an old task unfinished. | Keep editing was already fixed in original `6d591aa6f` at 05:31:43 and is not falsely credited as new. Resumed repairs cover save-before-sharing, retained source/credit instructions, active Draw versus Drawing captions, Save destination and dictionary-attested Dzongkha dithering. See the mainstream/Himalayan audit. |
| Jeju, Manchu, Ainu, Okinawan / #9 | 23 Sep 00:44: Jeju at resource 126 with grammar pass pending. 05:31: Manchu had 44 resources, plural and Unicode checks remaining. 08:53: publication claimed complete structural coverage. | Finish language-specific grammar and meanings; structural coverage cannot close these tasks. | Published Ainu/Manchu source-assisted audits retained. Resumed Jeju pass repairs 173 strings and the plural, separating commands from facts and removing Korean/Jeju inflection hybrids. Okinawan full-clause review remains active. Shared Manchu menu correction integrated. See the individual language audits. |
| Korean variants / Korean mixed script / Vietnamese / Nôm / #12 | 23 Sep 13:16–17:02: general-domain paired Hangul/Hanja prose and explicit image/colour/settings/save/select/edit/file/memory terminology still required. User corrected the tag to `ko-Kore-KR`. | Supply the promised general-domain evidence and contextual term decisions; a Bible-only corpus or Unicode script check does not fulfil it. Audit Nôm homonyms in actual compounds. | Korean evidence now has 91 exact NIKL-derived pairs, six explicitly editorial compositions and eight UI concept decisions. Repairs include the North Korean “too cursor” corruption of “too large”. Nôm catalogue-wide contextual review/font rebuild remains active. See `translations/KOREAN_SCRIPT_REVIEW.md`. |

The shared #2 base had a 22 September 03:16–03:18 instruction to edit direct
locale XML, use previous translations as references rather than authority, and
keep coverage JSON as a report. Japanese/Hong Kong/Taiwan Chinese were reported
complete at 04:19; Mainland Chinese and Cantonese scripts at 06:18. The resumed
pass fixes actual captions/import routes across these six catalogues and
context-dependent Jyutping readings. See `localization-base-caption-audit.md`.

## Review findings are a separate checklist

[`translations/PR_REVIEW_AUDIT.md`](../translations/PR_REVIEW_AUDIT.md) records all
15 inline findings, seven submitted review bodies, and eleven issue-discussion
records, with individual links. It identifies the actual long-help resource
targeted by #8; the shorter active `ui_help23` is an additional review target,
not a substitute for repairing the reviewed text.

Shared behavior lives in the integration, including script-aware vertical UI,
Literary Chinese and vertical English/emoji test locales, Taiwan Hakka tags,
licensed locale UI fonts, document/selection/clipboard/undo/draft image credits,
and the collapsed copyable Save as / Export as attribution panel. Reopened
language repairs preserve those features. Original PRs receive scoped updates
without importing unrelated locale directories or replacing their completion
tag lists.

## Recovery and publication

The resumed workspace initially restored an older snapshot. Unpublished audit
commits from the interrupted attempt were absent. Work restarted from the
published integration `7939f1292e706bd24dfd6596a8d3d51f3b202a84`, whose complete
Android workflow passed. The first reconstructed batch was preserved remotely
as `1c924c6178cef28b151ea644018ee772abf0c4da` on
`review/handoff-checkpoint-20260925`, with exact local/remote tree equality.
This is a checkpoint, not an assertion that the remaining language audits or a
new Android workflow have finished. No original PR has been merged.
