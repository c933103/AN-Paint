# JVM source blocker identified after publication

Binding: head d5fb31f6cb1562eecba51e5ccff9b118a7e71714, tree 8f9f0d5399f88d173a508e0ce5c96682ca173ed4, merge b750c54f6411412ee3f1bc1f51815db205212c35, run 38263619232.

The writer reported the failed hosted JVM step, then flagged a possible shadowed assignment. Independent source/specification review confirms the issue in `Paintroid/src/test/java/org/catrobat/paintroid/local/CommonsMetadataQueryFailureFlowTest.kt` (SHA256 a93f18f38bbea4691cb82de6753b4d9909c9637d98f0871bfec6a9c6b18ced97):

- Line 634 declares local `val text=view.text.toString()`.
- The nested `TextView(activity).apply` block at line 648 assigns unqualified `text=view.text.toString()`.
- Kotlin resolves the local property before implicit-receiver properties. A read-only property remains an assignment-resolution candidate and then causes a compilation error. The intended new TextView property therefore requires an explicit receiver (`this.text`) or setter call.

Primary specification: [Call without an explicit receiver](https://kotlinlang.org/spec/overload-resolution.html#call-without-an-explicit-receiver), [Resolving property access](https://kotlinlang.org/spec/overload-resolution.html#resolving-property-access), read 2026-10-12.

Status at creation: source-level compile blocker confirmed; actual hosted compiler error text and whether this is the only error remain pending. No local Kotlin compiler/Android execution was performed. APK and instrumentation-test compilation do not compile this JVM-test source. The earlier frozen independent source review missed this lexical-resolution defect; its host-test passes and byte-scope conclusions remain limited to their original stated scope and cannot stand in for Kotlin compilation.

This report does not change production, test thresholds, translations, source hashes or prior evidence. A successor must preserve this failed checkpoint, use a narrow reversible source projection, and run fresh exact-source Android/JVM evidence. A compiler repair alone cannot establish that the geometry fix works.

## Confirmed hosted receipt

The later official regression ZIP (artifact 11754635554, SHA256 8c2f3a8be6bc85412ce748c8b155a5b840445ab279394ba5252dce5cad7bbeec) confirms exactly one Kotlin error at line 648:86: `Val cannot be reassigned`. `:Paintroid:compileDebugUnitTestKotlin` failed, phase exit 1. There are no JVM XML files or M04 render directories. All 892 JVM identities and all planned render/control images therefore remain UNRUN. `phase-result.json` and `artifact-result.json` retain exact source-bound checks; an absent inventory causes the checker to fail and is not evidence of a new painted-ink failure. Production APK and test-APK compilation do not establish JVM-test compilation.
