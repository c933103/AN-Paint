# Final actual-develop verification — PR253

Actual develop `0ae074295045aaa794c755b5ff548067ccbfdfa5`, tree `879586bacd6091e830a558b3eaad7c744037e0d4`, remained current when read at 2026-10-31 17:29 UTC. Its tree equals the qualified PR source and tested merge tree. Natural push run 41222010049 completed successfully in all six jobs; no manual verification run was launched. PR exact-head automatic Codex review and required CI qualified before merge.

Hashed actual-run artifacts:
- regression 13051210869: SHA256 `996d37ea525aa93698cda5bd988f9cc77c0a98c449f3c00fec9d1184b1fcf730`; 1,521 JVM cases, zero failure/error/skip; all 63 distinct mapped/representative survivor identities present, including all 46 retained representative methods. Generic real AppLanguage selection/wrap boundary case passes.
- emulator aggregate 13050749340: SHA256 `40fec54f010363307f420fbae33c25c66a5ed0e8f82d6898da3e21158aba1cb2`; exact actual-commit/run identity; native 74/74 and app 49/49 pass.
- Python: 1,529 tests pass, two pre-existing skips. Android lint, exact-script generation and APK/source build pass.

## Observed ongoing work, not a controlled benchmark

| Observation | Baseline develop5367, run41212775008 | Qualified PR, run41219486029 | Final develop0ae, run41222010049 |
|---|---:|---:|---:|
| Python cases | 2006 | 1529 | 1529 |
| Python test seconds | 879.896 | 393.027 | 391.007 |
| JVM cases | 1862 | 1521 | 1521 |
| JVM summed case seconds | 537.964 | 712.628 | 732.504 |
| JVM Gradle step seconds | 666.864 | 896.026 | 922.645 |
| Regression/lint job log span seconds | 1790.762 | 1601.396 | 1629.088 |

The final whole job was 161.674 seconds (9.03%) shorter than baseline, and Python was faster, but JVM execution was slower despite fewer cases. Different VMs/regions (westus2, westcentralus, centralus), source states and runtime/cache conditions prevent causal or guaranteed speed claims; restored cache keys and runner image versions matched. These are existing required-run observations, not extra benchmarks. Raw phase/runner/cache receipts are attached.

This batch retires 47 catalogue mirrors totaling 12,484,429 bytes; active current_localization fixtures fall from 131/15,124,016 bytes to 84/2,639,587 bytes. Host cases decrease by 477 and hosted JVM cases by 341. Unique product consumers, formatting/selection/state boundaries survive; approval-history literal freezes intentionally do not. All 147 deleted paths remain recoverable at immutable baseline5367, with blob identities in removed-paths.json. No production resources or workflows changed. CI.md no longer recommends default duplicate full normal/optimized local aggregates.

The original failed/cancelled hosted run and its narrow correction remain recorded separately; neither is relabelled success. No release was created. Remaining cross-cutting provenance, exact-script/Latin-Sinitic approval payloads and bounded feature fixtures still require obligation-based review; this is not completion of the entire project-wide repair.
