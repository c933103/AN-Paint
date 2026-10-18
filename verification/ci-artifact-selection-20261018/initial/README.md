# Partial-rerun artifact-selection diagnosis

PR [136](https://github.com/c933103/AN-Paint/pull/136), patch head `2477633f0a1eab2dc4ea4fd090d4ced697ab3467`, tree `3ae2315d7e682da67f879fb39ca1825253dbcff1`. This evidence ref adds records to that exact complete source tree; it is not a new application patch or release.

## Observed failure and recovered evidence

The TW/CN warning fix in [PR135](https://github.com/c933103/AN-Paint/pull/135) merged as `614f28f9f8edd489e5d13cffbe481d3b49c99d7f`. Its [natural postmerge run 39126110768](https://github.com/c933103/AN-Paint/actions/runs/39126110768) remains **failed**, including its attempt-2 composer. No failed record was deleted or turned into a pass.

All timestamps below are 2026-10-18 UTC. Both position artifacts have the exact same name `emulator-position-api-35-614f28f9f8edd489e5d13cffbe481d3b49c99d7f`.

| Artifact | Source execution | Created/updated | Job interval and result |
| --- | --- | --- | --- |
| `12136188934` | Position attempt 1 | 12:22:38Z | Job `117673010551`, 12:16:53–12:22:40Z, failure |
| `12136049338` | Position attempt 2 | 12:37:26Z | Job `117676195214`, 12:32:24–12:37:29Z, success |
| `12136657509` | Core attempt 1 | 12:31:14Z | Job `117673010494`, 12:16:53–12:31:17Z, success; carried into attempt-2 metadata as job `117676217327` with original interval |

The later successful position artifact has the **lower** numeric ID. The attempt-2 composer job `117677253699` ran 12:37:31–12:37:38Z; its log explicitly downloads failed artifact `12136188934` and correctly rejects `position-ainu-manchu` inventory. The successful position retry completed all seven methods. The original failure was the unchanged 45-second Manchu interaction budget while waiting for Back dismissal; observed frame delays do not establish a root cause. Its original raw evidence is separately [preserved](https://github.com/c933103/AN-Paint/blob/8b839faf25214fa0a60d25ffd5f5b79924d339a7/verification/chinese-crop-preview-20261018/postmerge-attempt-1-failure/README.md).

`artifact-identities.json` retains both position artifact metadata records, the core metadata, all matching job records, creation/update times, ZIP SHA-256 digests and each downloaded artifact's exact source/run/attempt/APK/test-APK/source hashes. All three original ZIP downloads were checked against those digests. Every receipt identifies run `39126110768`, commit `614f28f9f8edd489e5d13cffbe481d3b49c99d7f`, SDK35, debug, the same source-test digest and identical prebuilt inputs. The successful core receipt says attempt 1, and the successful position receipt says attempt 2. The carried core job's API `run_attempt: 2` is metadata, not evidence of rerunning core.

## Proposed and tested repair

The selector paginates current-run artifacts and `filter=all` jobs. It requires the latest matching job to have succeeded, then requires exactly one nonexpired artifact with the exact checkout/SDK name and workflow run/head created and updated inside that job's execution interval. It downloads the validated IDs, never the first name match or highest numeric ID. PR source head and synthetic merge checkout are checked separately. Incomplete, ambiguous, wrong-source, future-attempt or expired evidence fails closed. Its read-only Actions permission is scoped to the composition job, with a one-minute step inside the unchanged eight-minute job cap.

The actual observed-metadata test selects core `12136657509` and position `12136049338`. Applying the **unchanged** source-bound inventory/hash composer locally to those downloaded successful original bytes passes all 45 API35 app identities with core attempt 1 and position attempt 2. This is a local recovery verification, **not** a successful hosted composer or a release claim. All existing content gates, tests and deadlines remain unchanged.

The five-file patch passed all 957 Python tests normally (167.503 seconds) and optimized (166.140 seconds), including 11 new selection regressions and the eight existing composition tests. The remote tree was checked against all 1,217 tracked local blobs/modes, with exactly five intended changed/added files and no removals. Codex exact-head review and [hosted run 39129078042](https://github.com/c933103/AN-Paint/actions/runs/39129078042) were pending when this packet was made. Do not infer their later status from this snapshot.

## Packet

`diagnosis-packet.zip` SHA-256: `2cab2ea8a2dff602da74f01a875c6763296898953291b6a9f620f60609a47708` (264,359 bytes, 107 manifest entries). It retains original failed-composer log/terminal run/job/artifact records; all three artifacts' selected raw JSON/XML, instrumentation/install/startup logs; observed selector metadata and output; local complete-union receipt; host test logs; and the packaging script. `manifest.json` provides per-member hashes verified after creation. Large emulator/logcat captures and screenshot binary payloads remain in the original Actions archives; this packet does not pretend to preserve every archive byte. Original archive IDs/digests are retained. No credentials or unrelated private data are included.

The application crop wording, JVM real-consumer checks, existing language-scope limits and separate unreviewed CN Help/Sinitic follow-ups in tracker [75](https://github.com/c933103/AN-Paint/pull/75#issuecomment-6249510704) remain unchanged. No whole-language, physical-device, appearance, TalkBack or release acceptance is claimed.
