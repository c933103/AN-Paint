# Bounded prior-run equivalence: design only

No code, workflow, permissions, tests or CI runs changed. PR259 remains on its original full path.

## Claim and policy

This is reuse of a recent successful experiment on the identical source tree, **not** proof that running today's mutable runner/image would produce identical output. Current preparation uses `JAVA_HOME_17_X64`, `cmdline-tools/latest`, and unpinned emulator/system-image revisions. A runner label cannot bridge that gap.

Parent-approved initial policy (2026-11-01): only same-repository `pull_request` debug/current-API35 runs, attempt 1, completed successfully before merge, with final required job completion at most 24 hours before merge and verification at most 1 hour after merge. These explicit bounds are an acceptance policy, not cryptographic environmental equivalence. Only an immediate ordinary two-parent develop merge qualifies; squash/rebase/direct push, full/release label, dispatch, rerun, missing reviews, or source conflict fall back. No chains of reused receipts: the ancestor evidence must be an actually executed full PR workflow. No release/signing/publication reuse.

Record actual prior runner ImageOS/ImageVersion, Java runtime version, Android package revisions (platform/build-tools/NDK/CMake/emulator/system image), Gradle distribution checksum, resolved dependency inventory/checksums and existing native-source checksum inputs. Missing/inconsistent identity means full fallback. Record per-job environments: a shared label does not establish shared image. These facts are provenance under a trusted producer, not artifact-self-asserted proof. Do not require a new heavyweight toolchain installation solely to compare a new runner to a run whose environment is intentionally being reused.

For content-pinned inputs, require unchanged trusted pin definitions and verified observed digests. For version-only/mutable SDK, JDK, Maven inputs, explicitly apply the bounded prior-environment policy above and preserve observed versions/digests; do not call them immutable. If parent instead requires *current external-input equality*, this optimization must remain disabled until those inputs are actually pinned/independently resolved; a cosmetic runner fingerprint is not a substitute. No broad supply-chain retrofit is authorized by this design.

## Authority and independent association

1. Use GitHub push payload plus authenticated GitHub API metadata, not values supplied by downloaded receipts, to identify repository ID, actual develop M and immediate first parent B. Confirm develop still points at M at decision time; superseding push is not a new success for M.
2. Obtain associated merged PR from API: base is develop, head repository ID equals base repository ID, merged=true, merge_commit_sha=M, head=H. Require exactly one matching PR. Fetch commit objects independently: M has exactly parents B,H. Fetch exact terminal PR run R and attempt1; its event, repository ID, PR association, workflow ID/path and head H agree. No run-ID guessing from artifact content.
3. Treat the workflow definition and **all executable policy/validator/build inputs it invokes** as trusted only when their blobs equal the already-delivered first-parent B versions. Same M/S tree alone does not establish trust: a PR could edit its own evidence generator. On any workflow/selector/composer/runner/build-preparation identity change, force normal execution. The optimization's introducing PR therefore cannot reuse itself on its first merge. Do not run downloaded scripts.
4. Recover tested checkout S from original artifact identity, but independently fetch and hash its commit/tree objects; require the PR merge checkout parents B,H and tree(S)=tree(M). Also verify original embedded corresponding-source archive against that exact tree, excluding only existing explicit packaging exclusions. H alone is not the tested checkout. Missing transient merge commit object falls back, not inferred from a title/count.
5. GitHub review metadata/checks must identify successful exact-head required review using the integration's stable app identity, not comment text or display name. Existing repo required review/check policy must be enumerable with existing read access; if it cannot be established, fall back. Do not invent an approval from current PR state or authorize a new credential.
6. Fetch every required job and all metadata pages from GitHub; require completed/success for checks, exact-script, build, core35, position35 and union35, with exact workflow/head/run and no skipped required job. Use trusted workflow-derived variant/matrix policy, not a fixed case count or untrusted receipt's declared coverage. Attempt1 deliberately avoids partial-rerun attribution complexity in first scope.
7. Select artifacts by exact GitHub run/job intervals using the existing selector. Independently download exact IDs and hash ZIP bytes against GitHub digest; reject expired/missing/duplicate/foreign/ambiguous artifacts. Validate member paths/size bounds using existing archive controls. Independently validate APK/test APK/source hashes and test reports, then run the existing composition validator with ORIGINAL S/R/attempt environment. Regression and exact-script evidence must also be present and linked to their successful jobs; device union alone is not the full pipeline.
8. Re-fetch terminal run/job/artifact identities immediately before accepting to avoid changed attempts/expiry/races. Any API/network/rate-limit/permission/metadata failure yields normal pipeline, never 'equivalent'.

## Minimal existing-file changes, after policy approval

- `tools/select_device_artifacts.py`: bounded independent GitHub association/job/artifact selection entry point. Reuse pagination/timeouts/identity validation. Keep current selector behavior untouched. No new package, credentials or external service.
- `tools/compose_device_reports.py`: separate equivalence verification/receipt entry point. Existing compose remains exact original run identity; no rewriting its checks to accept M as S. Emit distinct linkage receipt M↔S/R plus policy version and actual executed jobs, verified artifact IDs/digests and environment provenance. This receipt is output, never trusted input sufficient for acceptance.
- Existing `tools/ci_prepare_build.sh` and existing workflow identity-recording blocks: only minimal observed input/version/digest recording necessary for the chosen policy, not a new build framework.
- `.github/workflows/android.yml`: one preflight decision before expensive work, default execute=true. PR/dispatch/release paths always full. If verified equivalent, original expensive job records remain honestly skipped; a clearly named equivalence-verification check and summary report prior executed evidence. Consumers must deliberately understand that semantic difference; do not manufacture six executed-success checks.
- **Approved narrow permission wiring:** add `actions: read` only to the preflight job alongside `contents: read`, using the existing same-repository GITHUB_TOKEN. Global permissions remain `contents: read`; device-union retains its existing read scope. No writes, secrets, new credential, external repository access or protected settings changes. Any implementation requiring a broader or persistent grant stops for review.


No changes to app/native source, resources, gate requirements, branch protection, release tools or actual test inventories. No duplicate new review request or benchmark runs.

## Focused existing-test matrix

Extend `test_select_device_artifacts.py` and `test_position_composition.py`; use current synthetic metadata/receipts and injected bounded fetch, no new fixture files/framework.

- Positive: same repo, unique PR, parents B/H, independent S/M equal trees, trusted old workflow inputs, exact-head app review, executed complete API35/debug run, original digests and provenance retained.
- Identity: foreign repo/fork/workflow/app; wrong PR/head/base/merge; ambiguous association; squash/rebase/direct push; S differs despite H match; changed validator/workflow; review on old head.
- Execution: missing/skipped/cancelled/timed-out/failed/running jobs, unsupported release/full/dispatch variant, attempt>1, inconsistent pages, latest API state changes, absent regression or exact-script evidence.
- Artifacts: foreign/expired/duplicate/out-of-interval/missing artifact; wrong ZIP/API digest; APK/source/test APK mismatch; source-tree mismatch; incomplete current discovered app/native inventory; path traversal/oversized archive; original identity rewritten to M; forged equivalence JSON without independent API proof.
- Freshness/environment: future timestamp, >24h evidence or >1h merge delay, missing per-job image/runtime/package identity, changed pins/checksums, unsupported mutable-input policy.
- Fallback: every API error or ineligible state selects normal full path without authorizing success; PR and release always full; no stale accepted receipt/output survives failed verification; source assertions cover graph semantics only where real shell/metadata simulation cannot.

Run affected existing modules once normal after implementation, then ordinary exact-head CI/Codex. No full normal+optimized local pair. Final delivery records whether actual jobs executed or prior run verified, never conflates them.

## Observed review transport (2026-11-01)

GitHub issue-comment API on PR259 exposes `performed_via_github_app.id=1144995`, slug `chatgpt-codex-connector`, and author Bot id `199175422` for summary6551655757. Reviews/check-runs were empty. Authenticate this API-provided stable app/author provenance before parsing the structured `codex-review-state:v1` marker; require exact H, completed code review, false findings/unresolved flags, and applicable security state. Display login or user-authored marker alone is insufficient. Missing metadata or malformed/ambiguous state falls back; no new grant. The introducing merge uses full fallback; no artificial PR is created to demonstrate reuse.
