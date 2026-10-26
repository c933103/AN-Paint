# Amharic actual-merge verification

PR #171 merged as d0e4a3868c376bb857be8ca9762e7ef5ed31cbd4. Develop readback and actual merge tree match the reviewed union tree 31217f00ef95a1da9a54a18d02031ba710e836cb, preserving Bulgarian/Bengali, crop work and approved documentation.

Natural push run 40261676133 passed all six checks on the exact merge, attempt 1. Python: 1,352 tests, two existing skips. JVM: 1,341 tests across 142 suites, zero failures/errors/skips. API35 device reports: 119 expected and completed tests across ten groups, all successful and none timed out. These are tested behavior results, not native linguistic certification.

All eight artifacts were downloaded and verified against GitHub SHA256, byte length and ZIP CRC. APK/source build-info binds the actual merge/run; both payload hashes match. The APK-embedded source is byte-identical to the separately delivered source. Source comparison finds 1,358 tracked files exact, zero changed; only three repository housekeeping/IDE files are packaging-omitted, listed in source-binding.json. No tracked production source, test, locale, fixture, documentation or licence content differs.

Raw bulky artifacts remain attached to the CI run, with identifiers and immutable digests recorded here; their CI retention is not indefinite. Compact verification records are durable on this evidence ref. No release, upgrade signing, user installation or new Work task is included. Original translation qualifications, frozen wording and held work remain unchanged.
