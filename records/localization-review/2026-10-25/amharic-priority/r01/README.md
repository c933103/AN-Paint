# Amharic priority review and integration evidence

Base: `ea1ec8c9433a022af62b82742312cd30420f0cf5`.

This packet preserves 255 independently reviewed P0/P1 string decisions:
249 additions, three replacements and three exact retains. The 86 previously
accepted priority carries and all 108 earlier additions remain untouched.
The original frozen pixel plural remains unchanged.

The independent linguistic review records 225 accepted and 30 accepted-qualified
strings. Qualifications remain applicable; this is not whole-language completion,
native-reader certification or runtime/layout/accessibility acceptance.

`candidates.json` contains exact reviewed values and bounded source contexts.
`independent-review.json` preserves the complete review with local filenames
replaced by portable artifact references. Original assignment and candidate
hashes remain recorded. `source-binding.json` identifies the immutable sources;
source files themselves are not duplicated in this packet.

`patch-manifest.json` binds the eight staged integration files. `static-checks.json`
records one-off preservation checks, not permanent historical source invariants.
The warning registry preserves all previous 118 successors, adds only the two
reviewed Amharic warnings, and requires Amharic historical values to remain null.
Historical fixtures and held languages remain unchanged.

The focused subset passed 40 tests normally and under Python optimization.
All six available snapshot modules passed 47 tests normally and under optimization,
with exact-base missing font and sampled-memory inputs restored before final runs.
This is not the full repository host suite. Hosted CI and Android build/device
checks remain pending. No install, release or deployment is included.
