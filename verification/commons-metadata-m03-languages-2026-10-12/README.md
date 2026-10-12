# M03 three-language successor, 12 October 2026

The original reviewed, incomplete implementation remains immutable in PR #54 at
[`0c5073c7f55ba06657f79b8eb8a802d2cf0d7017`](https://github.com/c933103/AN-Paint/commit/0c5073c7f55ba06657f79b8eb8a802d2cf0d7017).
This separately identified successor adds the exact independently reviewed
Ainu Kana, Ainu Latin and Manchu Mongolian-script values. The implementation,
2 MiB threshold, default English and additive Nôm font are unchanged.

## Language decision

The [independent linguistic review](REVIEW.md) accepts the three exact strings as
source-assisted contextual UI paraphrases, with moderate confidence. It includes
independent backtranslations, grammar/attachment scrutiny, primary sources and
explicit semantic compression. No native-speaker approval or standardized modern
HTTP terminology is claimed, and no mandatory native-review gate is invented.
The Ainu pair is one linguistic translation in two checked writing systems.

[Exact decisions](decisions.json), [script checks](script-check.json), the two
translator JSON proposals and the Manchu explanatory report preserve the reviewed
wording and its limits. `artifact-provenance.json` records original and published
hashes; only incidental local paths/reviewer identifiers were made repository-
relative or descriptive for publication. Accepted values are unchanged.

The active all-140 disposition inventory now has 59 scoped values and exactly
81 out-of-scope default fallbacks. The original three unresolved rows remain
inspectable in the first commit above. Other language proposals retain their
individual review limits. The `linguistic_acceptance: not-established` inventory
field concerns competent/native certification; it does not erase the separately
recorded, bounded independent review of these three additions.

## Technical scope and validation

Three XML insertions, three API 30/35 expected-message rows, both Ainu tags added
to the normal/double-scale real-callback status checks, the exact M03 catalogue
fixture/pin, two host contracts, and the active disposition rows comprise the
successor delta. The old 57 fixture entries, historical oracles, production
mapping/cleanup, all existing glyphs and the font bytes remain unchanged.
The strict default-plus-59 and 81-fallback assertions are not weakened.

The original local runtime blocker remains: no Android SDK was available, so
local Kotlin compilation, Robolectric execution and device behavior have not
been established. Normal hosted API 35 CI must validate the actual published
successor head. New JVM declarations do not count as executed tests. Ainu uses
the existing system-font route; the Manchu script uses the existing bundled
font. Source/Unicode coverage is distinct from Android shaping/layout checks.

The Nôm U+8FD4 source/subset raster difference at 24 px remains explicitly open;
48/96 px masks match, and 2,202 existing-glyph samples remain preserved in the
initial evidence. This successor does not alter the font or establish universal
pixel equivalence. Security/device/archive and release holds are unchanged.
No readiness or merge approval is claimed.

## Author validation result

The frozen nine-path source/guard/disposition tree is
`db0735f6181c19be36c845a012ce541b61f1f64a`; its patch from the initial publication
is SHA-256 `b07c534abfc0ae4ff5fa2ff6494cc93eaa21cdbe0a58fd1064d47c13466ce52f`.
See `source-manifest.json` for every path and digest. New reports/logs are
additional evidence, so the full successor commit will have a different tree.

- Corrected focused host run: **82 methods, OK**, 5.644 seconds.
- Complete host aggregate: **568 methods, OK**, 184.901 seconds.
- The preceding focused command named a nonexistent F01 module; its invocation
  error is retained in `focused-host-invocation-error.log`. The corrected command
  used both actual TIFF description-wording modules. This was not a product defect.
- `integration-script-font-check.json` verifies exact reviewed values, NFC,
  no hidden controls, no newly introduced catalogue characters and complete
  existing Manchu font cmap coverage. This does not establish Android rendering.
- Mock instrumentation diagnostics in the aggregate log exercise host fixtures;
  they are not attempted or passed real-device tests.

The initial PR head's normal hosted run is
[38190123387](https://github.com/c933103/AN-Paint/actions/runs/38190123387).
Its resource-generation job passed; its host gate correctly failed the initial
three missing proposals. At this report checkpoint build/JVM work was still in
progress. These are initial-head observations, not successor runtime results.

## Independent technical review

The [independent technical review](technical-review/REVIEW.md) approves bounded
successor publication for the exact source tree and patch above. Its own focused
suite passed **98 methods** in 5.525 seconds; it inspected, but did not reexecute,
the author's passing 568-method aggregate. Exact resource injection, historical
fixture preservation, 59/81 dispositions, script/font coverage and evidence
provenance were checked. See [the indexed review summary](technical-review/review-summary.json).
The decision does not establish native-speaker certification, runtime behavior,
all-size font raster equivalence, readiness or merge approval.
