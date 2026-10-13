# PR60 font notice reference acceptance

[PR60](https://github.com/c933103/AN-Paint/pull/60) corrects ten asset-relative metadata pointers to the existing packaged font-notice aggregate. All font binaries, licence texts and attribution are unchanged. The three already-valid dedicated pointers are retained.

[verdict.json](verdict.json) records the exact source, all 13 resolved pointers, original full-notice checks, APK/embedded-source binding, the new installed AssetManager assertion, raw successful test events and artifact digests. All four jobs of [run 38328722360](https://github.com/c933103/AN-Paint/actions/runs/38328722360) passed on attempt 1: 942 JVM methods, 106 installed API35 methods, seven generation probes and zero lint issues. Local Python passed 666/666 in both modes; hosted Python passed 664 with two optional skips.

This compact evidence ref does not add application files, duplicate prior source inventories, retain full generated archives or establish a new CI gate. The complete current source and meaningful regressions remain on the linked PR head. Source notices with CRLF are compared using universal-newline text decoding; their original source bytes and the pre-existing packaged aggregate bytes were independently checked unchanged.

The ready-triggered review result and final merge disposition remain on PR60. No new API30, physical-device, licence-permission, upgrade-signing or release acceptance is claimed.
