# Croatian/Bosnian bounded P0 artifact verifier

Separate adaptation of the PR182 Serbian successor verifier; no prior source,
verifier, failure or acceptance record is overwritten. Current source identity
and publication state are recorded in preparation/source-expectations.json and
manifest.json. Synthetic controls do not establish any actual hosted pass.

## Accounting

78 new reviewed values per hr/bs =156. Preserve98 Croatian and117 Bosnian
existing values, disjoint from the new key set. Complete locale/key/English
source/target/attributes pair list is canonicalized in hr,bs order with sorted
keys and bound to independently pinned SHA256 ecf526badf05941ed1a11be43af7e6192fda51828861fce34b385c991e2011dc.

Prior Serbian current reviewed149 (147 unchanged plus2 previously corrected
values) and preserved337 remain unchanged. Other prior reviewed548 plus prior
SK/SL preservation254 are retained. Total reviewed853 = new156 + prior697;
preservation806 = new-family215 + prior591; combined1659 distinct locale/key
entries. hr176,bs195,Serbian244/242,SK/SL205 each,CA/RO/DA/NO78 each,NN80.
Receipt preserves prior producer fields: prior_reviewed_entries548 is the older
non-Serbian subtotal; prior_reviewed_total697 includes Serbian149. These must
not be added twice. New reviewed_entries156 is distinct from the retained
current_Serbian_reviewed_entries149.

Exact BCP47 Serbian qualifiers and symbolic references remain validated.
Generic sr cannot substitute for either script. Existing inherited values are
preservation-only, not newly reviewed or whole-language acceptance.

## Source/JVM expectations

Derive tracked source tree including the3 new files, expected1388 tracked and
1385 packaged after unchanged3 exclusions. Full source bytes/modes must match
remote Git tree before artifact acceptance. Focused inventory14 classes/81
methods includes CroatianBosnianP0WordingTest8 and ProtectedDraftWarningTest8;
all other focused suites retained. NumericDisplayLocaleTest remains6 methods,
but all11 explicit locale tags must have distinct matching literal caption map
entries. Missing hr/bs or prior captions are negative controls. Actual full JVM
and Python totals come from hosted receipts, not these estimates. API35 source
expectations45app+74native remain separate from execution results.

## Verification controls

Run test_artifact_verifiers.py under ordinary Python and python -O, binding
--source-root, --source-head (once available), --tree-file, --expected-tree and
separate --out directories. Archives, APK output and run identifiers are
synthetic; API source validators are stubbed only in the synthetic runner.
Controls retain exact-script generation, signature, packaged source, script
swaps, symbolic aliases, complete reviewed pairs and producer-selection checks.
New controls reject altered Croatian/Bosnian text/source/attributes/review
binding, inherited text corruption, reviewed omission/overlap, every missing
new JVM method, whole new suite omission and all8 protected runtime omissions.

API35 --core-attempt/--position-attempt/--composed-attempt default1; actual
attempts must match the artifact. --expected-selection is mandatory and must
be independently reconstructed from complete remote artifacts/jobs metadata.
Do not copy the archive's selection into that expected file. Replayed job
record attempts remain distinguished from original group execution attempts.

All actual artifact families require fresh final-head/tested-commit/tree/run
and artifact digest binding. No previous PR artifact is a successor pass.
No release, native-human, physical-device, layout or whole-language claim.
