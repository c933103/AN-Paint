# PR9 documentation conflict repair

The 6 October source check found a README conflict between PR9 head
`d60178949819a8fac8977ced0ba6497c84c7a90e` and its actual base
`41ac05dba279ca52ad86f952edeada2d772ff4b4`. Both branches had independently
wrapped withdrawn historical claims in a disclosure and `<details>` block.

The repair keeps the base's `8cf4ed2e5` archive link at the shared location and
moves the PR9-specific `97e511dc6` archive link beside the preserved PR9 history.
Both referenced README objects exist. The PR9 section moves before the older
vocabulary history so the common closing `</details>` no longer competes with
the branch-specific tail addition. Its historical prose is preserved verbatim;
the reset and non-acceptance warnings remain.

Validation: `git diff --check` passes, and `git merge-tree --write-tree --name-only`
with the exact base above returns success with no conflicted paths. This only
computes a proposed merge tree; no branch merge, PR merge or deployment was done.
Only Markdown documentation changes, so Android checks are not rerun for this
edit under the repository's documented workflow. Locale source and all pending
semantic rechecks remain unchanged.
