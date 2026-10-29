# Danish, Icelandic and Norwegian priority scope

All **92 P0 + 249 P1** identities have a bounded disposition for each of
`da`, `is` and actual offered `no` (`nn` remains separate; `nb` is not offered).
This is not whole-language, native-human, installed-layout or TalkBack acceptance.

[Complete review and prior-source bindings](https://github.com/c933103/AN-Paint/tree/9087639f5c9fc7869e75b1226367164a6ff92bc3/verification/nordic-priority-20261029)
retain prior acceptance rather than crediting repeated review. The former author
candidates are at `7fc5492da0e78474bb828b5276e0b703989c7b67`; the current review
binds to `0070c5816ad31911d227fab50ea193e2a39b13ab`.

| Locale | Priority edits | Retained priority | Absent holds | Changed companions |
|---|---:|---:|---:|---:|
| da | 164 | 171 | 6 | 4 |
| is | 246 | 89 | 6 | 5 |
| no | 174 | 161 | 6 | 5 |

598 resource edits comprise 570 additions and 28 replacements. Six absent holds
and 24 wording-only dormant entries per locale remain explicit. The 152 prior
da/no priority pairs and 85 earlier Icelandic candidate receipts are carries,
not newly earned reviews. Icelandic standalone selectors retain `Mynddílar` /
`prósent`; separate suffixes use dative in the complete width/height descriptions.
The two da/no standalone pixel-label capitalization suggestions were not applied.

Current resource fixtures and meaningful consumer/negative-control tests live in
`nordic_priority_wording.json`, `test_nordic_priority_wording.py` and
`NordicPriorityWordingTest.kt`. The existing da/no P0 and shared warning/profile
checks use finite forward bindings; their historical fixtures remain unchanged.
Local host and exact-head hosted outcomes belong in the PR, not assumed here.
No release, signing, access, provider, PR113 or stopped archive change is included.
