# Exact-head host verification

Implementation: `33ba9f34dfa39aa2780635818edb2a98dc9d4f8b`, tree `51a1e991e0125ba61384b1e35142dedf7f1569e5`.

Both full host suites ran after the final explicit-key test-inventory change and exited 0:

- Normal Python: 993 tests, 239.632 seconds. [Raw log](host-exact-head.log), [exit status](host-exact-head.exit).
- Optimized Python: 993 tests, 239.416 seconds. [Raw log](host-exact-head-optimized.log), [exit status](host-exact-head-optimized.exit).

[Source identity and log digests](exact-head-source-verification.json) record all 1,228 expected source leaves rechecked by Git blob SHA and mode after both runs. No source leaf differed from the published head. Generated untracked runtime files are not source changes.

This receipt supersedes only the earlier “exact-head full-suite runs in progress” status in the initial README. Earlier failed and repaired runs remain separately recorded; they are not relabelled. Expected synthetic failure-output fixtures printed after the unittest summary do not change the successful aggregate exit status.

At publication, hosted workflow [39241759777](https://github.com/c933103/AN-Paint/actions/runs/39241759777) and both Codex reviews are still running. Six new real-consumer JVM tests are authored but have not yet executed successfully. Local Gradle bootstrap remains network-blocked. No JVM, AAPT, APK, installed Swedish UI, TalkBack, native-speaker or release acceptance is inferred from these Python results.
