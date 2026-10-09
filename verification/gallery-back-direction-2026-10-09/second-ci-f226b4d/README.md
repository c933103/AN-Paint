# Second run: production-view checks pass; auxiliary identity assertion fails

[Run 37959961028](https://github.com/c933103/AN-Paint/actions/runs/37959961028)
tested `f226b4da19a73bebdf3c0176914aa1e9377a8579` through merge
`26667d7b7000e6007be5f5bd5edc40754fbf7376`, with identical tree
`44fd58106bf22800073272e33ac41e59e200ba16`. This includes accepted Help work.

The SHA256-verified regression ZIP contains 731 JVM tests: 729 pass, two fail,
zero errors/skips. All six production-view configurations in
`GalleryBackDirectionTest.xml` pass, including explicit repeated locale-switch
save/restore and the independent 140-tag direction/history/accessibility matrix on
both API30 and API35. Each matrix JSON records 140 completed tags and exactly the
ten expected RTL tags. Lint XML contains zero issues.

Only the two auxiliary `syntheticResourceMutationKeepsTheOldLocaleCacheKey` cases
fail. The exact assertion was object identity: `Host reuses Resources under the
original English override key expected same:<android.content.res.Resources@...>
was not:<android.content.res.Resources@...>`. The unedited XML preserves complete
values/stacks. This disproves that control's particular same-object assumption.
It is not a failure of the production arrow, history or accessibility assertions.

The auxiliary test is removed instead of relaxing its identity check into a pass.
All six production-view configurations and every arrow/accessibility/history
assertion remain. No production change accompanies this removal.

## Correct the earlier explanation

The first run's retrieved XML confirms both failures expected `←` and observed
`→` when the synthetic configuration helper returned to LTR. The explicit
save/destroy/create tests now pass. Robolectric's documented resource-management
caveats provide background, but a specific cached-Resources identity mechanism
was not proven and is contradicted by the auxiliary control above. Do not report
that hypothesis as the established cause. The host recreation tests do not
independently establish delivery of a real framework-triggered locale recreation.

## Retrieval and visual review

The earlier direct/materializer HTTP403 responses did not classify the backing
or establish an owner denial. The returned `sdmnt…oaiusercontent.com` artifact
reference is Sediment-backed. The documented tool-owned download route succeeded
for both exact file references. Both complete ZIP SHA256 values match GitHub's
artifact digests; safe extraction rejected absolute/parent traversal paths.
The earlier JUnit/capture retrieval blocker is resolved. Raw-log Git blob upload
remains separately paused and its missing file remains absent.

The four included PNGs were inspected at original capture scale: Arabic's Back
points right on API30 and API35, while English and Classical Chinese vertical
columns retain a horizontal left arrow. All are Robolectric NATIVE production-view
captures, not installed-device screenshots. The blank browser area is the offline
ShadowWebView, not proof of a loaded Chromium page.

`artifact-manifest.json` records both source ZIP identities and which evidence was
retained in this repository. `junit-inventory.json` records the complete suite.
The original ZIPs remain available through their official Actions artifact records
until expiry; the complete ZIP bytes are not claimed as published here.

Removing the invalid diagnostic test still requires new exact-head CI and review.
The two failed runs remain failed historical results.
