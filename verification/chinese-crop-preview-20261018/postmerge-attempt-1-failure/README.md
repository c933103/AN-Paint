# Natural postmerge attempt 1: position-dialog deadline failure

Run 39126110768, merge 614f28f9f8edd489e5d13cffbe481d3b49c99d7f, failed job 117673010551.

The raw report records 6/7 position methods passing. `manchuPositionColumnsAndNativeEditing` exceeded the unchanged 45-second interaction budget while waiting for `Back dismisses the reopened dialog`. Its protocol completed with a failure, so the gate correctly failed; the source-bound method was not skipped. The shared process cap did not time out. Logcat records this test from 12:19:59.138 to 12:20:46.689 and system frame delays, but these observations do not establish a production root cause. No crash or ANR was found in the retained relevant excerpt.

The exact same source passed the premerge run. Only TW/CN plural text and two new host/JVM test files changed in PR135; the installed Manchu test, resources, code, assertions and time budgets are unchanged. After inspecting the complete original artifact and job log, a retry of only the failed position job is appropriate, without changing assertions/deadlines or discarding this failure. If it repeats, investigate further rather than repeatedly retrying.

The first retry request returned HTTP403 because the workflow was still running, explicitly “The workflow run containing this job is already running”. It did not start a retry and is not a user refusal or authorization denial. Retry remains pending until the existing run ends.

This packet preserves the original failed artifact metadata and digest; complete job log; unmodified XML, summaries, instrumentation/install/startup logs and device identity; and a clearly labelled relevant logcat excerpt. The complete downloaded artifact was inspected and its digest verified. Large general emulator/logcat logs remain in the original Actions artifact rather than being represented as complete inside this packet.
