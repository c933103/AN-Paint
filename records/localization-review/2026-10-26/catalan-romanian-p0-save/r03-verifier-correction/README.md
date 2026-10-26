# Packet verifier metadata correction

An independent audit found two metadata-integrity gaps in the frozen r01 packet verifier: a candidate priority changed to P3, or a fabricated consumer-context ID, could pass. **The actual 20 candidate values, priorities and context bindings were independently verified correct.** This was not a translation or privacy defect. Original r01 bytes and the counterexamples are retained; r01 was staged as Git blobs but no records branch advanced before this correction.

The corrected verifier requires every candidate priority to be P0 and its context IDs to equal the corresponding source entry. It also checks that source context IDs are unique, match the actual ordered context records and agree with the declared context count. These checks close the forged-source-plus-candidate-chain case, not only the two original counterexamples.

The original 39 controls remain, with six additional refreshed-hash controls: two locale priority mutations, two candidate-context mutations, a forged source/candidate context chain and a wrong source-context count. **One positive packet and all 45 negative controls pass** in ordinary and optimized Python; control receipts are byte-identical. Existing full-format guards continue to reject added unindexed/nonargument/malformed tokens even under formatted=false.

Use this corrected verifier and test file against the frozen r01 candidate packet. Neither script changes source or confers linguistic acceptance; the full independent value receipts are in r02. The original verifier's exact SHA-256 is recorded in verifier-extra-controls.json. No scope or review verdict is widened.

```sh
python3 verify_candidates.py --source-root PINNED_CHECKOUT --packet ../r01-candidates --out CHECKS
python3 test_verifier.py --source-root PINNED_CHECKOUT --packet ../r01-candidates --out CHECKS
python3 -O test_verifier.py --source-root PINNED_CHECKOUT --packet ../r01-candidates --out OPTIMIZED_CHECKS
```
