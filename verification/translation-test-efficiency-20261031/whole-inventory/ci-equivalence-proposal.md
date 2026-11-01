# Proposed equivalent-source post-merge verification (not implemented)

Purpose: avoid repeating the entire already-qualified PR pipeline on the immediate develop merge when it represents exactly the same source. This is a separate policy/implementation review, not a waiver in PR259. Current triggers and gates remain unchanged.

## Narrow eligibility

Use only the immediately merged, reviewed PR in this same repository. Establish actual develop commit M, its merged PR/head H and the exact successful workflow run/attempt R. Obtain tested checkout S from artifact identity, not merely the API's head H. Prove Git tree(S) = Git tree(M), and that M actually includes H. A conflict, changed combined tree, direct push, missing review, different workflow or unverified parent/source association takes the ordinary pipeline.

R must be terminal successful for every currently required job, with the required current-platform/matrix and build variant. Never reinterpret a cancelled, timed-out, missing, skipped-required, partial or superseded run as passed. A release or concrete cross-version requirement continues its prescribed full path. Different label/event-derived variants or missing matrix coverage are ineligible.

Bind the actual workflow/configuration, dependency/toolchain inputs and recorded APK/test-APK/corresponding-source bytes. The same `ubuntu-22.04` label is not proof of identical image/toolchain inputs. Missing required identity metadata fails closed to the normal run. Any proposed freshness/input policy must be explicit; no guessed equivalence from a matching PR title or coincident test counts.

## Evidence must retain its original identity

Current `compose_device_reports` requires exact commit/run/variant/test-source identity and matching APK/source/test-APK digests across core and position. Do not alter old receipts to say they ran on M. Keep their original S/R/attempt identity and issue a separate, narrowly scoped source-equivalence receipt linking S to M with the verified tree and qualifying checks. The app49/native74 inventories are source-discovered, not counts to freeze in the new path.

If a development APK is reused, label it as the already-tested artifact built from S whose reviewed source tree equals M, not a newly built M APK. Its embedded corresponding source and original byte hashes remain intact. Do not rewrite ZIPs or build-info records just to make old identity checks pass. Release/upgrade signing remains a separate policy; no release reuse is proposed here.

## Minimal integration, not another framework

Prefer a bounded extension of existing workflow/identity selection and composition code. Preserve the normal path as fallback; do not replace existing corruption/identity validators with trust in a new summary. The post-merge result should explicitly say 'verified equivalent-source prior run', not report six newly executed successes. Required-check policy and consumers must accept this semantic distinction deliberately before any trigger or gate changes.

Existing relevant tests should exercise correct association plus tree/base/workflow/variant/SDK mismatch, foreign repository or run, incomplete/cancelled/failed checks, stale/missing/changed artifacts, mismatched attempts, current test-source inventory drift and forged/partial source-equivalence receipts. Reuse existing test modules and synthetic fixtures; do not introduce per-language packages, another approval catalogue, or a full duplicate benchmark matrix. One required exact-head qualification tests the implementation; final delivery preserves original and current provenance honestly.

## Other architecture questions, not automatic deletions

Some position/vertical evidence modules mix real receipt corruption, shell fault and native-input safeguards with source-spelling inventories. Evaluate those within this same evidence-path design; preserve genuine false-pass prevention rather than discarding all tests-of-evidence. Successful JVM capture volume also warrants separating needed pixel computations/assertions from writing every successful diagnostic image. Neither reduction is implemented or claimed by this proposal.

Existing observations: #256 PR42m04s + actual-push22m19s were separate workflow elapsed durations, not CPU time. PR258 actual regression ZIP was84.6MB; removed colour capture contributed32files/1.34MB raw/1.14MB compressed. Large retained UI image groups support mixed real assertions and evidence, so size alone does not justify removing them. No extra benchmark or full-suite run was launched for this plan.
