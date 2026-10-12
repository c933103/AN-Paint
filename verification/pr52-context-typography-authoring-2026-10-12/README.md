# Context-bound UI typography candidate

This successor addresses [PR52's ready-review P2](https://github.com/c933103/AN-Paint/pull/52#discussion_r4252897501). The accepted predecessor is `eb7451d320ba56e1ece6b1b55797da653966051d`, tree `b6bf7626c1d7c4aef669394970046ffc89a5c877`.

UI direction and bundled UI font selection now resolve the same rendering-context resource locale. Pure explicit-locale mappings, language-picker overrides and the drawing font fallback retain their prior semantics. The fifteen-path delta changes only four production files; no wording, resource, font asset, installed test, workflow or timeout changes.

Five new cross-version binding tests and one attached notification test cover newly constructed Nôm, Wu and every offered Mongolian-script profile after an opposite process-default reset, inverse English behavior, explicit overrides, later children/spinner rows, tooltip routing and full accessible attached notifications. Existing rotation/recreation checks additionally cover fresh Nôm/Wu/Mongolian-script font binding. API21/24 establish binding and logical text; actual native glyph checks run only where Robolectric supports them. Real accessibility-node checks use attached windows, avoiding an independently identified API21 detached-fixture dereference.

Existing process-only typography fixtures now configure their rendering resources explicitly. Every prior JVM identity is retained. Current discovery derives 932 JVM executions (910 retained plus 22 added), rather than freezing that count in application CI. The host inventory remains 650.

The source review and host receipts below are bounded authoring evidence. Kotlin compilation, native behavior and installed API30/API35 acceptance require the fresh hosted run. Previous accepted runs retain their original source attribution. No default-branch merge or release is established here.

The first ordinary host attempt on tree `9dfe21eb` executed all 650 methods and failed one structural expectation that still named the old no-context vertical guard. Its raw log and exit-1 receipt are preserved under `pre-guard-correction/`. Updating that expectation to the approved context-bound guard changes no production code or runtime assertion. Final candidate tree: `cf1ffdb16e4e8401edce81a50b16ad6f21cdcaa8`.

## Published successor and authoring results

Published head [`ff8553d29a4c135c16b00beadf9cabba1e8d6fae`](https://github.com/c933103/AN-Paint/commit/ff8553d29a4c135c16b00beadf9cabba1e8d6fae) has parent `eb7451d3`; every one of its 1,095 tree leaves/modes was compared with the reviewed checkout before the leased branch update. The synthetic merge `a73e9482` has ordered parents develop `484d1b31`, then `ff8553d2`, and the same reviewed tree. [Run 38319915849](https://github.com/c933103/AN-Paint/actions/runs/38319915849) requests API30/API35. [Exact-head Codex review](https://github.com/c933103/AN-Paint/pull/52#issuecomment-6134269653) was requested and read back.

Final ordinary host run passed 650/650 in 126.357s; optimized passed 650/650 in 125.394s, no skips, exits 0, unchanged 240s cap. Independent final focused checks passed 108/108 in each mode and independently reconciled both complete host logs. The previous one-failure attempt stays failed in its separate directory. These results do not claim fresh hosted Android acceptance.
