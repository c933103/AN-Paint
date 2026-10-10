# F01 TIFF size wording: bounded correction and evidence

10 October 2026. [Draft PR43](https://github.com/c933103/AN-Paint/pull/43) publishes exactly the independently reviewed 37 catalogue substitutions and four new test files. This evidence-only supplement does not modify that source tree.

## Current stack publication

Draft PR43 now has head `4f9082aa687a5c36b559061bcc10d0e39331610f`, tree `04a84df1535297f13a314c521b55647f6d15a678`, on the exact unmerged PR34 dependency. The [43-path stack evidence and independent review](stacked-evidence/README.md) records 412 host passes and the narrow historical-guard composition repair. [Release-configured run 38049772357](https://github.com/c933103/AN-Paint/actions/runs/38049772357) is pending at this checkpoint. Earlier failures remain retained below; they are not replaced with successful results.

## First-head CI update

The first run completed with two strict mixed-Korean JVM failures; all seven initial F01 dialog methods, build/lint and API35 passed. Read the [retained failure and dependency diagnosis](first-ci-evidence/README.md) and [proposed exact stack](integration-proposal/README.md). The source-head history below remains the initial publication snapshot. The evidence-files.json manifest pins the original packet at commit3981b84e; later additions and this updated index have their own commits/manifests.

## Published source and verification

- Source head: `d3ada3e55fb60a6926e7f6c8eede242f3c1f140e`; parent/develop: `80c14372b0504bc44f9f2809ad477247fdc8100b`.
- Accepted source tree: `bde13ca4bbd9a45198ab4da9cadd85d900aaa594`.
- Preserved eleven-entry tree: `89e43725c5b7c2f01827cfa06510c21f5268314c`; isolated 26-resource tree: `b81391fb46dd9ee1bdb86c3faf693462e1316232`.
- All 1,294 remote file identities/modes and the contents of all 41 changed/added files were read back and matched before publication. There are 1,253 unchanged base files and no removals.
- PR43 is draft and unmerged. Existing automatic [CI run 38047199955](https://github.com/c933103/AN-Paint/actions/runs/38047199955), attempt 1, is in progress at this initial publication snapshot. No successful Android result is inferred here. Its PR merge commit `a8825ce33460372fb2888f9d49830f80df38d9cd` has the same accepted source tree and parents develop plus the source head.

## Read the evidence

1. [Final combined scope, patch and test limits](combined-evidence/README.md), [exact manifest](combined-evidence/candidate-manifest.json), [all-language inventory](combined-evidence/all-language-inventory.json).
2. [Independent source/test review](independent-review/source-test-review.md), [structured review and nine test names](independent-review/source-test-review.json).
3. [26 individual linguistic proposals](evidence/linguistic-proposals-26.json), including exact originals/proposals, minimal replacement pairs, confidence, sources and limitations. [Independent map check](independent-review/expansion-map-review.json) and [combined inventory check](independent-review/combined-inventory-review.json).
4. [Final independent host log](combined-evidence/independent-final-host.log): 374 passed, no skips. [41 assertion-rejected negative controls](combined-evidence/independent-final-negative-controls.json), with positive runs before and after.
5. [Initial eleven-entry review stage](evidence/README.md), including its separate patch, full inventory and historical checks. Superseded before-checkbox-review snapshots are explicitly retained as history.

The stage READMEs and reviews describe their prepublication state. This root page records later publication; earlier local Gradle failure logs remain tied to their actual attempted pre-repair trees. Their uncached Gradle8.13 download failed with Network is unreachable before tasks or Kotlin compilation. Nine new Robolectric methods were therefore uncompiled/unrun locally. The independent reviewer corrected two invalid assertions about CompoundButton.performClick()'s return value before accepting the source. That was a source/API-contract finding, not an executed Android failure. Actual state, description and callback assertions remain. Deliberately rejected mocked instrumentation summaries in Python host logs are not device failures.

The two independent verification scripts are preserved exactly. They expect sibling `candidate`, `expansion-candidate` and `combined-candidate` Git snapshots, rather than an evidence-only checkout. Reconstruct those snapshots from develop and the respective retained patches/manifest identities when reproducing that layout.

## Scope and unresolved obligations

Only `formats22_tiff_description` changes. English now says **may reduce** and pt-BR **pode reduzir**; the other 26 use individually reviewed modal constructions. The [encoder](https://github.com/c933103/AN-Paint/blob/80c14372b0504bc44f9f2809ad477247fdc8100b/Paintroid/src/main/cpp/tiff_bridge.cpp#L480-L518) does not compare compressed/uncompressed outputs and select the smaller. [RFC1951 §1.1](https://www.rfc-editor.org/rfc/rfc1951.html#section-1.1) and [zlib's technical bounds](https://zlib.net/zlib_tech.html) support qualifying size reduction. No stream-bound percentage is promised for a complete TIFF.

The RGB-page/pixel-preservation and unchecking instructions, emoji prefix, Korean Hanja, qualifiers, routing, generation/canonical-source policy and all other text remain unchanged. No encoder or application-code change is made. Model linguistic review and cited grammatical usage do not constitute native-speaker, complete-string or full-language acceptance; per-entry confidence and regional/terminology limits remain explicit.

The inventory records all 60 explicit descriptions plus 81 offered missing-key locales. Thirty-seven clear cases are qualified. Twelve probable cases remain individually open and unchanged: bo, ceb, dz, hak-Hant-TW, hak-Latn-TW, jje, mn-Cyrl-MN, mn-Mong, mnc-Mong, nan-Hant-TW, nan-Latn-TW, wuu-Hans. Four uncertain cases remain open and unchanged: ain-Kana, ain-Latn, ryu, vi-Hani. Seven already-qualified entries remain unchanged without broader acceptance: ja, lzh-Hant, yue-Hant, yue-Latn, zh-CN, zh-HK, zh-TW. The 81 missing-key locales receive no new translations; their default fallback is source-predicted, not runtime-proved individually. The new Welsh fallback test supplies one bounded case only when execution is verified.

Broader F01 and P07-007 remain pending. The authoritative register stays **475 total / 3 structural completed / 472 pending**. Original owner scope is partially recovered; term-specific original-thread reconciliation and applicable runtime/rendering/language requirements remain open. A01 is a separate change and is not included in this develop-based PR. No clean Codex review is claimed at this initial evidence publication.
