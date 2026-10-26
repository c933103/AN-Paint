# Serbian format-label successor artifact-verifier preparation

Source: isolated durable successor awaiting merge integration; no successor PR
or hosted CI is asserted by this package.
Published branch commit: `998dcfccbe3f54fc61b2deaa3579a08bbaa2da06`.
Exact tree: `0c606e5dfaf497d59fdcadf85d453afb96b4ed6b`.
Parent source: `6b7cbfceefe66f7a78a46e792f57b49455384e18`.

This separate directory adapts the PR180 verifier bundle without modifying it.
The immutable PR180 source, review, historical snapshots and acceptance receipts
remain distinct. No prior hosted pass transfers to this successor.

## Scope and review lineage

Current Serbian reviewed family comprises 147 unchanged reviewed values, one
replacement Cyrillic warning, and one newly reviewed Cyrillic format label:
149 unique current reviewed values, NOT 150 or 149 newly reviewed changes.
The separately pinned complete two-value canonical pair digest and review record
are checked, including locale, key and attributes. The added label must be
disjoint from the 74-key family and preserved map.

Compiled scope: Serbian149 + other prior reviewed548 =697 reviewed;
Serbian337 + SK/SL254 =591 preservation-only; combined1288 unchanged.
Cyrillic75 reviewed+169 preserved=244; Latin74+168=242. Both explicit BCP47
script configurations and symbolic aliases remain checked; generic sr does
not substitute for either script. Preservation does not imply linguistic review.

Focused JVM scope is source-derived:13 classes,71 methods, including all6
ProtectedDraftWarningTest methods (4 preexisting plus2 Serbian). The existing
SerbianP0WordingTest remains8 methods. Actual aggregate totals must come from
hosted XML, not this focused inventory. API35 source expectations remain45app
and74native;1385 tracked files imply1382 packaged after3 explicit exclusions.

## Controls and invocation

Run test_artifact_verifiers.py in ordinary Python and python -O with the exact
source-root, source-head, tree-file, expected-tree and separate --out directories.
Controls fabricate archives/outcomes and stub API35 source validators only
inside the synthetic test runner; they are not hosted execution evidence.
New negatives cover both compiled pair values and omissions, altered successor
review metadata/locale/key/values, overlapping preservation, every missing
protected-runtime method and the missing entire class. Existing alias, script,
source/archive/signature, exact-script and attempt-selection controls are retained.

API35 supports --core-attempt/--position-attempt/--composed-attempt (default1)
and --artifact-file (default api35-composed.zip). --expected-selection is
mandatory and must be reconstructed independently from remote artifact/job
metadata, not copied from the archive. Exact receipt equality, producer/source
identity and bounded original-versus-replayed attempts remain mandatory.
Do not assume this successor's attempts match PR180's2/1/2 retry.

Parent read-only review found no blocking issue in the APK adapter. Two initial
synthetic harness construction errors (tuple subscript and helper scope) were
repaired before successful controls; they were not production failures.

No actual successor APK/JVM/API35/exact-script artifact was verified here.
No release, physical-device, layout, native-human or whole-language claim.
