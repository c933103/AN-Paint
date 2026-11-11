# PR 430 qualification

Source head `79cbd92fa338b6c82e61f6aa083ff8e6f0e1b7be`, base `e2ed367a9459907effcfb5f877c7dd86ef56a8f7`, source tree `a275820307774369d0796d4ab1c03d35cbd82494`. The tested merge checkout `5e231000d3291bafcf7eba0c27f4c57bf574ffa2` has that tree and ordered base/head parents.

[Original required PR run 42964894448](https://github.com/c933103/AN-Paint/actions/runs/42964894448), attempt 1, completed successfully. All seven normal jobs passed. [Codex exact-head code/security review completed](https://github.com/c933103/AN-Paint/pull/430#issuecomment-6787764017), code review with no findings.

Downloaded artifact ZIP digests were checked against GitHub metadata. Reports establish 865 passing Python tests plus two explicit skips, 1,392 JVM passes with zero failures/errors/skips, 13 exact-script probes, 74 native API35 and 50 app API35 methods. Fresh source discovery and the existing app report validator reproduce the complete app union. Build, standalone/embedded corresponding source and instrumentation hashes match the composed device identity. All 1,280 bundled tracked blobs match the remote tree; the three existing VCS/IDE omissions remain explicit. The seven position methods are part of the 50-method app union, not additional tests.

`qualified-results.zip`: 408,335 bytes, 250 members, SHA-256 `17ed4764517d264b83575a947f7694659ee6284fef308985bc7c8aa7f22447b1`, Git blob `f9b4c6ac522eb29f091f70d26ace2eee6bb9dc76`. Contains compact source-bound metadata, current review, validators and test reports. Full bulky artifacts stay in the original workflow; this evidence ref does not alter application source.

Limits: independent archive/report verification is not a new device execution, native-human review or exhaustive layout/glyph/speech certification. CI debug key only, no upgrade-signed release. Post-merge actual-develop verification is recorded separately after merge. Older holds and withdrawn acceptance are unchanged.
