# Natural postmerge core setup failure, retained

Natural integrated develop [run 39131791712](https://github.com/c933103/AN-Paint/actions/runs/39131791712), commit `8700ca4d921875bdc9f3cf824290cfb83cda2037`, attempt 1. Core job `117689541968` started 2026-10-18 13:35:37 UTC and completed failed at 13:36:11 UTC.

The `Install emulator image` step failed after sdkmanager downloaded `x86_64-35_r09.zip` and reported: `Archive is not a ZIP archive.` The package was `Google APIs Intel x86_64 Atom System Image`. The downloaded package bytes are not available in the job artifact, so the underlying cause is not established. This is an SDK-image setup failure, not an app instrumentation failure or a composer-selection failure. **Core instrumentation did not run.** Its run step was skipped, and no core test inventory is accepted from this attempt.

Artifact `12138303007`, name `emulator-core-api-35-8700ca4d921875bdc9f3cf824290cfb83cda2037`, was created/updated at 13:36:09 UTC. Its original 469-byte ZIP SHA-256 is `8d538b15952eae98701accaa03807ffca0beca61a82143013c10071afed86c7b`, verified after download. It contains only `device-identity.json`, which binds this source, run and attempt to the prebuilt APK/source/test-APK hashes; it contains no successful execution evidence.

`failure-packet.zip` is 12,109 bytes, SHA-256 `604ca64757619ce0f83883b757dbc14bbc56f3998a0d6859b108629781111830`. It preserves the complete original job log, raw job/artifact metadata, the observed in-progress workflow record, original artifact ZIP and extracted identity. Each packet member was verified against its manifest. The observed workflow record is explicitly a snapshot, not its later terminal state.

Build and all nine exact-script probes passed. Position subsequently passed; JVM/lint and the aggregate were still pending/running when this record was prepared. The intended recovery is a targeted retry of this core job after the workflow reaches terminal state, preserving successful jobs and all original evidence. No source edit, deadline relaxation, skipped-test acceptance or full-suite restart is used for that recovery. A later successful retry must remain distinct from this failed setup attempt.

The previously preserved original crop postmerge interaction timeout and stale-artifact composer failure remain intact on their earlier refs. Integrated #123/#133/#135 application changes and scope limits are unchanged; no release or broader language/device acceptance is claimed.
