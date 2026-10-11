# PR34 immutable native-cache producer correction

Prepared 11 October 2026 UTC+08 on diagnostic head `9b62193455f3794192fe7e8b8ef6c3360d6e297f`, tree `d071e57d5774a639b7352f0cfa876b8922b4d899`.

## Evidence and scope

[Codex P1 discussion 4239016323](https://github.com/c933103/AN-Paint/pull/34#discussion_r4239016323) identifies a source-verifiable first-writer problem: checks compile only `-PnativeAbis=x86_64`, while universal assemble defaults to four ABIs, but both used exactly the same primary native compiler-cache key.

[GitHub's cache reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching) specifies that existing cache contents cannot be replaced, missing primary entries are saved after successful jobs, and restore prefixes are tried in order. Consequently, a successful x86-only checks producer can occupy the shared immutable entry before a universal producer can save its fuller cache. The host negative control reproduces that key collision; it does not measure the historical remote entry's actual contents.

## Change

- Separate primary save keys by build variant and producer: debug/release × checks-x86_64/universal.
- Shared first restore prefix matches exact source hashes and variant; retain previous compatible fallback prefixes.
- Preserve compiler-content checking, empty sloppiness, disabled direct/dependency modes, two GiB cache ceiling, pinned action/compiler-cache package and cache directory.
- No cache deletion, new persistent credentials, permissions, compiler output tree caching, run-ID key churn, ABI reduction, signing change, test removal or deadline change.
- Existing cache-safety test identifier is retained. Its former identical-step comparison now normalizes only the intentional producer suffix and still checks all other cache settings match.

A failed universal build still cannot save its cache. This fixes the distinct immutable-key race, not proof that a cold four-ABI build fits 22 minutes. Runtime diagnostics remain necessary to establish the actual slow phase and whether further bounded changes are justified. Running diagnostic CI is allowed to finish before the PR source ref is advanced, preserving its failure artifact.

## Validation

- 488 full host tests passed in 166.791s, no skips.
- 23 focused cache/build/check/budget contracts passed normal in 1.213s and `-O` in 1.169s.
- Both producer save orders retain the full universal entry under distinct keys; an old shared-key negative control loses it.
- Four primary keys are distinct across role/variant, ordered shared restoration is checked, forbidden compiled-output caching/run-ID churn is rejected, and existing compiler-safety contracts pass.
- Original application and direct-runner sources are unchanged. Host model checks are not a real GitHub cache-population or Android runtime result.

Fresh exact-head Codex/CI is still required after publication. All preceding build timeouts and skipped device tests remain in the record; merge/release remain held.
