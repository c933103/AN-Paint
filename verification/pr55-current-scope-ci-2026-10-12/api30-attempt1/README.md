# API30 setup failure preserved before targeted retry

Docs-only head 4a35933ff6b6d0013dac8743cc5eeac1c1033e05, tree b6bf7626c1d7c4aef669394970046ffc89a5c877; run 38303992927, attempt 1, job 114996862363.

The same-run prebuilt artifact downloads verified their expected SHA256 digests. sdkmanager then failed to prepare the Android Emulator package with "Archive is not a ZIP archive", exit 1. The source checkout and deadlines were unchanged. The underlying malformed-download mechanism is not established. Instrumentation did not start: all 95 selected API30 identities are UNRUN and no API30 artifact was uploaded. This is a setup failure, not an observed application-test failure.

The complete 25KB job log and exact phase/job metadata are retained. Independent review confirmed the phase and hash. A targeted job rerun was requested after diagnosis, but GitHub refused to start it while the overall workflow was still running. A later retry, if executed, must retain this attempt separately. No other job was cancelled or rerun.
