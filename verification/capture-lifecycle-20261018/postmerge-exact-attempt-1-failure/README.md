# PR138 postmerge exact-script setup failure, attempt 1

Observed on 2026-10-18 at 15:33 UTC. The workflow was still running; this packet records a terminal failed job, not a terminal workflow.

- Source: merge commit `248d5d41e4114f9252c858c3ac08f2bb124746dc`, tree `f2870b51aba6c8290e929c7fa176c4d14c802d52`, identical to reviewed PR138 head `81404c63c54b47a7cc3f55bacaee93e14d98eb9b`.
- [Workflow 39140653627, attempt 1](https://github.com/c933103/AN-Paint/actions/runs/39140653627/attempts/1); [exact-script job 117714218072](https://github.com/c933103/AN-Paint/actions/runs/39140653627/job/117714218072).
- Job execution: 15:28:45–15:29:13 UTC. Prepare build tools and notices failed while installing NDK 27.2.12479018, reporting “Archive is not a ZIP archive”.
- All nine resource-generation probes were skipped. No exact-script test result is claimed. Upload found no files at `build/reports/exact-script-generation/`; no artifact was uploaded. The observed run artifact list was empty.
- The SDK installer did not retain the downloaded archive in an uploaded artifact. The underlying malformed-download cause is unknown. This failure precedes application tests and is distinct from historical emulator collection failures.
- No retry had been requested at the time of this snapshot. Subsequent work must preserve this failure and inspect the terminal workflow before targeted recovery.

`failure-packet.zip` contains the full job log and observed raw workflow/job/artifact metadata with per-file SHA256 manifest. It is 8,620 bytes; SHA256 `d91998c0e338aed050f9d7fdc3663fce9d48da6f9c24275796df6806266ef1c3`.

This additive evidence commit preserves all integrated source files, prior premerge acceptance evidence, and all historical failure refs. The accepted premerge source-bound checks remain in [the premerge report](../premerge-integrated/README.md). This snapshot does not establish postmerge acceptance.
