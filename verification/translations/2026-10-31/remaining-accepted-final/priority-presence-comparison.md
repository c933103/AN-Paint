# Direct P0/P1 presence on actual merged source

Commit a087bf6e609c86ac60110c0b782c62dc6c72a8d3; verified tree71c2c50b624a0f730aa28c00eca99c9768cb2227.
Method: unchanged tools/string_importance.py --all-locales --json, validated typed priority manifest and exact canonical same-tag resource presence. Strings, plurals and arrays count by typed identity; no inherited locale fallback is credited. All171 offered options retained. P0 denominator171*92=15732; P1 denominator171*249=42579.

| Measure | Before PR247 | Actual merged PR247 | Change |
|---|---:|---:|---:|
| P0 direct presence |14148/15732|14329/15732 (91.08%)|+181|
| P1 direct presence |38536/42579|39092/42579 (91.81%)|+556|
| Options with every P0 and P1 identity directly present |147|151|+4|

The same command on the preserved frozen base tree a05f9c3648f884470e2694006d64b68ace65f1a8 (actual c120 merge tree) reproduces all three prior figures exactly. The737 additional identities equal181+556; the two existing wording replacements do not increase presence. Newly P0/P1-presence-complete: br, sv, tt-Cyrl, tt-Latn. P0 alone complete153 options; P1 alone complete151.

The20 options with any P0/P1 absence remain: ang, ch, chr, fa-IR, nch, nhe, nhw, non, nv, qug, quh, quy, quz, rw, shn, tdd, yo, yua, za, zgh.

These are presence measures, not translated/reviewed/native-human/installed-layout certification. They do not restore withdrawn historical conclusions. They are distinct from all-tier canonical-catalogue presence:59 complete,106 partial,6 empty. Per-option full and priority ledgers preserve both methods explicitly.
