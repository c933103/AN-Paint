# Slovak / Slovenian P0 — frozen local evidence

Source head `0824180c14ae979dc253f03d0fe628fbe9cf9b34`, tree `98b89d126533df3c0dbaeb729c74e4bcb44a3a8a`, PR179. All1,382 final paths/modes match the remote Git tree; all15 changed contents read back exactly.

Final ordinary and optimized host runs each pass1,408 tests, no skips. Focused10 tests pass. Source hashes/modes frozen before final runs and checked again afterward. The preliminary full ordinary1,408-pass run is retained separately: a Kotlin-only numeric oracle was corrected during it, so it is not relabelled as final frozen evidence.

Independent source audit verifies156 exact approved additions,254 inherited pairs, missing-only scope and P087/92 each. It caught the sk/sl zoom comma-decimal test expectation before hosted execution; the exact test-only fix is retained. No production semantics changed.

Artifact verifiers include four positive and45 negative synthetic controls, ordinary/optimized receipts matching. They are prepared verification tools, not actual hosted results. The Java decimal probe was not run because jshell was absent; actual Android SDK/compiler/Gradle caches are also unavailable locally. Source-static conclusions are not presented as runtime execution.

The reproducible implementation audit expects source/, base-source/, packet/, review/, and approved-manifest.json as named by its script; use the immutable source commits and r01/r02 records for those inputs. Artifact scripts document their parameterized inputs and publication limits.

Required CI40362410752 and exact-head Codex review remain pending at this record. Actual PR artifacts and later actual-postmerge checks are separate. All five no-consumer holds per locale, mixed-English inherited context, P1/frozen history, paired120/60 and global59/112 stay unchanged. No native-human/whole-language/layout/private-upgrade-signing/release claim.
