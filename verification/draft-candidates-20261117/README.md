# Continued draft review: 314 distinct source keys

**UNAPPROVED DRAFT EVIDENCE, NOT AN APPLICATION MERGE BRANCH.**

Pinned base remains 428f9f2a203116c4d11a279ea2c1cfb3093059c0. Continued authoring now covers 241 distinct Chamorro keys, 33 Zhuang keys and 40 Standard Moroccan Tamazight keys: 314 distinct source-key candidates. These are incomplete draft hypotheses against 875 missing keys, not 314 completed translations.

Chamorro has 232 retained candidate values and 10 historical rejects; one rejected spelling (Back) was subsequently corrected and has lexical acceptance, so these categories overlap by one key. Three further correction hypotheses remain separate and unapproved. The newest 57 candidate keys cover memory diagnostics, format behavior, assembly dimensions and licence/help terminology. All uncertain prose remains outside canonical resources.

Independent review found further invalid or unverified extraction-versus-decoding terminology; ambiguity between memory capacity and application budget; TIFF byte size versus dimensions; panning versus drawing movement; early curve commit; and legal/codec compounds. Exact holds are retained in ch.json. Semantic-only review of numeric conditions and source clauses is not linguistic acceptance.

## Combined integration proposal

Use `accepted.patch` (supersedes the earlier `ch-accepted.patch`) only as input to a larger combined batch. It adds 7 Chamorro short labels (Quality, Top, Tool option, Wheel, Back, AGPL licence, GNU AGPL licence) and 2 Standard Moroccan Tamazight licence labels. It also corrects a zgh provenance entry that incorrectly referred to Wolof capitalization. No separate micro-PR was created.

The two zgh licence labels use the exact pinned MediaWiki licence term plus unchanged identifiers; existing source notices remain intact and two provenance mappings were added. Chamorro lisensia is attested in the primary dictionary. These bounded lexical compositions do not certify any long technical/legal prose.

Zhuang image/width/height and Tamazight width candidates were adjusted toward current catalogue terminology, but these are still unresolved hypotheses: the existing catalogue is not independent linguistic authority. Do not integrate them.

Six translation-boundary and 34 translation tests passed for the preceding 7-label patch; the final 9-label patch is rechecked separately in checks.json. No Android/AAPT/runtime or hosted-CI result is claimed. Required exact-head Codex/CI gates remain unchanged.

Sources remain those in the initial evidence README/history: official Guam technology list and orthography; https://natibunmarianas.org/l/ for lisensia; pinned MediaWiki 377002822b34077904f4e83c21faaf69d1bfea9a za/zgh terminology references, with GPL-2.0-or-later notices. Individual lexical evidence is not whole-phrase attestation. Full source/callsite/linguistic review is still needed before production integration.
