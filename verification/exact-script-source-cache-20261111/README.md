# Exact-script source cache qualification

PR #424 merged as fa617108ca987d458ec2ac445f8fa0ae7fc375ac after exact-head Codex and all seven required PR jobs passed. The actual merge has the identical tested tree and ordered parents. The full natural develop run 42909226180 was still active at this receipt; no final-develop pass is claimed here.

qualification.json contains the exact source, run, review, cache-hit excerpts, artifact digests and independent verification boundaries. exact.zip preserves the complete original resource-probe archive, including all 13 hashed probe logs and observed inputs (SHA-256 06349364c7e38922f2a1900398b7e2afb3539069aa60eab5d6305f94c1f15cd1).

The original source/dependency cache was actually restored, but its creating ref is not reported by the logs. This is not sibling-PR evidence reuse or a cold-download fix. Downloader code, hashes, source URLs, notice checks, source markers, tests and deadlines remain unchanged. #422/#423 old failed checkouts remain unqualified; #395 was not integrated. No release or exhaustive language/device/security claim.

Original full CI artifacts: https://github.com/c933103/AN-Paint/actions/runs/42904324996 . Regression and composition archives were independently downloaded and hashed, as recorded; this compact receipt does not duplicate all unrelated capture/build bytes.
