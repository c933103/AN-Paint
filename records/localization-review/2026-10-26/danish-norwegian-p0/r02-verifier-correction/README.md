# Candidate verifier correction — original candidate bytes unchanged

The independent data audit found a real defect in the [r01 candidate verifier](https://github.com/c933103/AN-Paint/tree/8eeb848c00b0dd5e23d2ac003b6dff99bf7be74e/records/localization-review/2026-10-26/danish-norwegian-p0/r01-candidates): its indexed-only placeholder regex ignored an injected extra unindexed `%s` if candidate hashes were refreshed. The historical verifier and receipt remain intact. **No defect was found in the 156 actual candidate values**; they independently passed the repository's fuller placeholder/Android-string checks.

This version corrects the checker, not the candidate text. It recognizes indexed and unindexed format tokens, rejects malformed or stray percent syntax, and compares the entire ordered token inventory even for `formatted=false`. It writes verification output outside the immutable input packet. All eight candidate files retain their exact r01 bytes, SHA-256 and Git identities.

The corrected checker passes all 156 actual values, 323 source bindings and 140 consumer windows. Reproducible controls pass one positive case and reject eight mutations, including refreshed-hash `%s`, extra numbered tokens, invalid `%q`, bare percent, missing argument, duplicate identity/JSON key and missing group. A separate independent check additionally rejects malformed `%1$q`, incomplete `%1$`, extra `%%`, and extra `%s` in `formatted=false`; no failed control emitted a verification receipt.

```sh
python3 verify_candidates.py --source-root CHECKOUT --packet R01_PACKET --out OUTPUT
python3 test_verifier.py --source-root CHECKOUT --packet R01_PACKET --verifier verify_candidates.py --out TEST_OUTPUT
```

This is data/source validation, not linguistic acceptance. Final locale reviews are separate records. Application source, current catalogue values, all ten held absences, Nynorsk holds, paired/P1 boundaries and explicit pauses remain unchanged. No CI or release was launched.
