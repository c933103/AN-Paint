# Three existing Amharic holds: independent review output

Read `REVIEW.md` and `adjudicated-values.json` for the substantive decisions. The result is two releases with revision and one release unchanged; no implementation was performed.

- `adjudicated-values.json`: exact accepted values and hashes, decisions, reasoning, original hold decisions, alternatives, and scope boundaries.
- `adjudicated-values.xml`: three exact reviewed resource elements, solely as a review artifact.
- `prior-held-records.json`: unchanged copy of the entire original three-row history supplied for review.
- `input-MANIFEST.json`: unchanged input manifest whose SHA-256 is the task's input seal.
- `input-verification.json`: independent integrity checks and explicit execution/retrieval limits.
- `sources.json`: immutable primary-source links and byte hashes, including bounded excerpts. Complete source bytes remain in the unchanged sibling input dossier `amharic-held-proportions-resolution-20261024`.
- `verify_review.py`: reproducible integrity checks for the review and its exact sealed input. It does not run the app or alter files.
- `MANIFEST.json` and `SHA256SUMS`: output seal and file inventory.

No input file was modified. This output does not add these values, or the separate Eyedropper result, to the pending 90-value implementation batch. The parent must preserve the original evidence and resolve scope explicitly before adding them to implementation work.

This directory contains a source-backed review deliverable, not private assistant memory. It has not been published remotely by this reviewer. Do not bulk-publish complete third-party corpus snapshots or grammar extraction solely because they were retained for local verification.
