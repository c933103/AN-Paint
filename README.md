# Legacy Discard final local verification

Candidate c72aafced5ac713db436cb98aa1d279981f06449, tree b72698ab8937bad21431e5c9a8124e2122d0d205.
PR248; authoritative disposition PR56 comment6541291852.

local-final-verification.zip contains final frozen-source SHA256 manifest, complete normal and optimized Python logs and exit receipts, and focused logs. Both final full modes passed2086 tests, no skips, exit0; normal1751.379s, optimized1737.076s. All1643 source files unchanged after runs. Focused36 tests passed both modes. Source branch holds code; this evidence-only branch holds bulky logs, not a release or whole-language certification.

Hosted run41189271133 and exact-head Codex receipt6541797058 provide separate hosted/review gates. At evidence creation hosted JVM/lint remains pending; do not infer a pass from this archive.
