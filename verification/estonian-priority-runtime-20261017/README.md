# Estonian priority runtime follow-up

Application head: `e2f0e6a7c1c232767fe2aa641ebb60aa8424b5f0`; tree `22c5db5148d0fb750b2d30946f1516ee70956f59`.

The original complete 341-entry review and independent challenge remain in the unchanged five-file packet under `verification/estonian-priority-review-20261017`, also independently reachable at commit `723cfa571399e300b860ce32d169b16a18e70423`. Seven resource values are unchanged since that review.

Initial hosted run 39070963804 executed 1,113 JVM tests with one failure and zero skips. The new picker cancellation test asserted `isShowing` before the Android dismissal message ran. The raw JUnit diagnostic explicitly reports unexecuted main-looper runnables. Full picker wording and the other three Estonian runtime tests passed. The follow-up adds main-looper draining after the actual Cancel click, retaining all full-text, callback, selection and dismissal assertions; no production behavior or text changed. The initial test failure is preserved rather than relabelled as a pass.

`initial-runtime-packet.zip` retains all 118 JUnit suites, the complete regression log, precise diagnosis and artifact identity/digest, the follow-up source patch, current focused host/compile checks and full remote-source validation. Artifact download URLs and credentials are excluded. Initial local evidence remains in the original review packet.

Fresh exact-head run 39072564370 is pending/running when this packet is first published. Later terminal results will be added without altering any retained source/evidence. The PR remains draft until hosted checks stabilize; parent handles Codex/ready/merge/postmerge. Existing linguistic uncertainties and all holds remain unchanged. Runtime results do not provide native-speaker, TalkBack or installed Estonian layout acceptance.
