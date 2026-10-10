# Proposed non-destructive continuation of existing PR19

Status: preparation only. Final source diff and parent refs require review before the existing PR branch or base changes.

1. Re-read `develop` and PR19 immediately before publication. Initial inspected refs are develop `4b615ce2d9e27814df84812b90858b5f676ce51a` and PR19 `dc518e7663ee3173f81ee6a931e15fb4ab9c467f`.
2. Prepare the accepted develop tree plus only the reviewed gallery routing tests, necessary test-only local-network containment, strict runner accounting if required, and focused documentation/evidence. Do not transplant old production or CI files wholesale.
3. Create one merge commit with the existing PR19 head as first parent and the then-current accepted develop as second parent. Its tree must equal the inspected develop-plus-allowlisted-delta snapshot.
4. Verify all original PR19 commits remain reachable through the first parent. Their experimental source trees remain recoverable without another archive branch or a duplicate PR.
5. After review, fast-forward `test/combined-gallery-autosave-20261007` to this commit with an expected-head check and no force option. Retarget the same PR19 to develop. Re-read both refs, verify the complete remote tree and inspect the resulting diff before evaluating CI.
6. Retain draft status until the new exact head passes applicable checks and obtains acceptable review. Historical old-tree passes do not satisfy these gates.

## Explicit exclusions

- No production gallery/credit implementation changes unless a newly reproduced defect is separately reviewed within scope.
- No #18 vertical-locale test/prototype adoption, Arrow test repair, vertical notice UI or unrelated language work.
- No PR29 resource, font, SVG-reason or translation-test edits. Its current `MediaGalleryActivity` change is avoided because this continuation does not edit that production file.
- No replacement of the accepted ordinary/seed/verify force-stop workflow with PR19's obsolete partition.
- No native/physical-device, live-provider, API30 or broad language acceptance inference.

## Test boundary to resolve before execution

All data fixtures are local. The real gallery must still be launched and recreated by Android, and its result must return through the actual task stack. Only external document destinations may be substituted. The gallery result itself must never be synthesized.

Contain initial WebView traffic before launching the gallery, fail closed if the boundary cannot be established, and prove the boundary with a local observed probe. A block applied at CREATED is insufficient. This is a test-only containment mechanism, not a production network behavior change.
