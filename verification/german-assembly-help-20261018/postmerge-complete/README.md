# German assembly Help: postmerge verification complete

Merged PR: https://github.com/c933103/AN-Paint/pull/129
Merge: `ec4d74eb222c58d51e4a339e43ca83cc7aa16ec3`
Reviewed PR head: `2686f35c1c43910f659fdfe48944a61516bd473e`
Shared tree: `05f725b3a5c64acdace799cfb8cb5d5768ce8f63`
Natural develop run: https://github.com/c933103/AN-Paint/actions/runs/39087387993/attempts/2

## Terminal result

The postmerge workflow is **completed / success**, with all six gates passing. Attempt 1 passed every instrumentation method but failed when its emulator went offline before required screenshot pulls. After inspecting the exact logs/artifact, one rerun of failed jobs completed the core and dependent combined gates, without source, assertion, deadline or workflow changes. The final composed device receipt explicitly binds core attempt 2 and position attempt 1 to the same APK/source/test hashes. The already-passing build, resources and regression stages were not rerun.

[Attempt 1's actual failure, full core artifact/log and passing JVM results remain preserved](https://github.com/c933103/AN-Paint/blob/233cb683fe11324a100c6a8342ab9753e54f1bc7/verification/german-assembly-help-20261018/postmerge-attempt-1/README.md). Missing capture evidence was never converted into a pass. The earlier original German toolbar fixture failure and repaired PR success also remain in the [prior immutable evidence](https://github.com/c933103/AN-Paint/blob/dab89c939d761b6b649899f6daa2562df8bd4e20/verification/german-assembly-help-20261018/repaired-runtime/README.md).

## Actual artifact verification

- The exact postmerge regression artifact contains **1,124 JVM tests**, zero failures/errors/skips, across 120 suites. All four complete Help/crop consumer methods pass, including the German toolbar/Exact position/conditional Unplace method (0.216 seconds). Every JUnit XML is retained in the packet.
- The final composed API35 artifact verifies **74 native and 45 app methods**, with no missing, unexpected, errored or timed-out methods. Its source-bound inventory is complete. It retains the successful first-attempt 7 position methods and fresh second-attempt core methods.
- The actual recovered capture exports were downloaded and independently run through the unchanged repository transport/inventory validators: all **12 dialog cases**, **104 vertical export data files**, and the **32-image vertical matrix** passed validation. Capture transport is now verified; this does not replace independent visual review or add German-specific installed acceptance.
- Artifact digests match GitHub, and APK/source payload hashes match build-info. The APK embeds exactly the companion source ZIP. All 1,206 included tracked payload files match reviewed Git blobs and executable modes; packaging omits two .gitignore files and .idea/codeStyles/Project.xml. The build uses a CI debug key, not the private upgrade key.
- Exact-script resources passed all nine clean/incremental probes. The merge tree is byte/mode identical to the PR head that received clean Code and Security reviews and six passing premerge gates.

`checks.json` records exact run/job/artifact IDs, hashes, outcomes and method durations. The compact packet retains terminal snapshots, every JVM and device JUnit XML, complete device identity/coverage/capture receipts, source binding and independently rerun transport receipts. Bulk APKs and screenshots remain in the referenced Actions artifacts; this compact record makes no independent visual-acceptance claim.

## Scope

The bounded complete German Help correction and unchanged behavioral assertions are exercised. No full German catalogue, native-speaker, installed German glyph/layout, TalkBack, universal large-font or physical-device acceptance is inferred. PR75's broader obligations remain open; PR56 and explicit holds are unchanged. Evidence is additive on a dedicated ref, outside the application tree.
