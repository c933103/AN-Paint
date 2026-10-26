# PR177 local implementation evidence

Pinned source: `06a2e4078efa1fe8ef8ea37b186ece0431633f08`, tree `949f87f736d4d12de2a92a1834ad35332ab01a1a`; [PR177](https://github.com/c933103/AN-Paint/pull/177).

The final ordinary and optimized host suites each pass 1,388 tests with zero skips. Both focused 14-test modules and their independent combined 28-test runs pass. All ten source-file identities were rechecked after both full runs. Local Android/JVM compilation or execution is **not** claimed.

The first full ordinary run genuinely failed with two stale tagged-colour-oracle errors. Its output and pre-fix manifests/audit remain here, separate from the passing final run and final independent audit. The repair adds exactly the two independently reviewed Catalan/Romanian full values to that current family (70 exact expectations /101 English fallbacks). Global 59/112 scope, P1, frozen history, inherited values and holds do not change.

The four artifact scripts are reproducible verification tools, not hosted results. Their four positives and 33 negatives in both Python modes are explicitly synthetic. The 33rd guard rejects overlap between the newly imported and prior Save key sets. Actual hosted artifacts and terminal results will be recorded separately.

Log transformation ledger records raw and published SHA-256 with only local/control path-prefix omissions. Printed unsuccessful synthetic runner receipts within successful host logs belong to deliberate negative tests; they are not failed device runs. Review qualifications remain in the separately preserved r02-reviewed packet. No native-human, physical-device, layout or whole-locale certification; no release or paused-scope change.
