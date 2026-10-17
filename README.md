# Sampled-memory wording: bounded corrections and complete-value review

Application [PR #121](https://github.com/c933103/AN-Paint/pull/121), exact head
[`e45eb63a4539109a1270fc76f9ab73b0fb78b15e`](https://github.com/c933103/AN-Paint/commit/e45eb63a4539109a1270fc76f9ab73b0fb78b15e),
parent [`44ad5ce2156fef79baae3ef5650b9ac5eac06202`](https://github.com/c933103/AN-Paint/commit/44ad5ce2156fef79baae3ef5650b9ac5eac06202).
Tracker: [#71](https://github.com/c933103/AN-Paint/pull/71). This separate evidence ref is not an application change or tracker closure.

## Exact scope

The reviewed key is `ui_sampled_resize_memory_explanation`, consumed by the
sampled-memory branch of `ImageResizeDialog`. The fresh linguistic/static-context
review examined nine complete values on `f988a94d8e4fa300bfe181ba67bba7b546651ca1`.
All nine catalogue blobs and complete-value hashes remained identical on the
integration base above, including merged PR #120.

The application patch makes only these two one-span changes:

- `bo`: `འདྲ་བཤུས་ཆུང་བས་ཞིབ་ཆ་ཉམས་སྲིད།` becomes `འདྲ་བཤུས་ཆུང་བས་ཞིབ་ཆ་ཉམས།`.
- `jje`: `줄어들 수 이수다` becomes `줄어들어 이수다` in the smaller-copy detail-loss sentence.

Actual memory-use variability, all other clauses, resource attributes, quantities,
format arguments, routing and consumer code remain unchanged. Reversing each exact
span reconstructs its baseline catalogue blob. The key is a scalar string with no
quantity forms or format arguments. The patch adds a compact complete-value
fixture, four host methods and two real-dialog Robolectric methods; it does not
certify the complete Tibetan or Jeju messages.

## Current decisions

[Current exact values and dispositions](current-status.json) bind the post-edit
hashes to the application head. [Complete original review](review/complete-review.json)
preserves all original values, candidate values, reasoning summaries and source
links. The [historical inheritance-only receipt](https://github.com/c933103/AN-Paint/pull/80#issuecomment-6182923640)
remains unchanged.

- **One bounded complete-value semantic acceptance, confidence M:** unchanged
  `vi-Hani`, SHA-256 `c440148385de677afbe0d08d981c57a64267f53d1224c5effd502af513c1a270`.
  [Full review](review/vietnamese-hani-review.json) and
  [independent challenge receipt](review/vietnamese-hani-independent-review.json)
  support all four estimate components, variable usage, definite smaller-copy
  detail loss and unchanged original file. Contemporary technical-compound
  interpretation remains reviewer synthesis. Some primary PDF evidence was
  search-indexed only after the full PDF returned HTTP403; that limit is retained.
- **Eight complete-value holds:** `ain-Kana`, `ain-Latn`, `bo`, `dz`, `hak-Latn-TW`,
  `jje`, `mnc-Mong`, `ryu`. The two modality corrections resolve only that bounded
  mismatch; their technical-language and complete-message fluency holds remain.
  Other held values are unchanged. See the detailed Ainu/Manchu,
  Tibetan/Dzongkha and Hakka/Jeju/Ryukyuan review files.

No native-speaker, specialist, whole-catalogue, universal Nôm orthography, runtime,
layout, accessibility or release certification is implied. PR #56 is untouched.
No new dictionary alternative or absence of a phrase attestation is treated as
proof of error by itself.

## Verification

- Four focused host methods pass normally and optimized, including 27 malformed
  resource controls. Both original complete-value controls fail as expected.
- All 897 full host tests pass normally (210.522 seconds reported by unittest)
  and optimized (202.797 seconds); process timings are in `host-results.json`.
- Full current AAPT2 resource compile/link passes. Supplementary Kotlin 1.9.24/API35
  compilation of the new consumer test with fresh resource symbols passes.
- Real consumer coverage is authored for complete compiled bo/jje values, sampled
  dialog invalid/valid width changes, Cancel/reopen, and the unchanged native-floor
  branch that disables an impossible resize. It has **not executed locally**:
  Gradle wrapper download returned `Network is unreachable` after retrying with a
  writable Gradle cache. Supplementary compilation is not Robolectric execution.
- All 1,194 remote application leaves, blob hashes and modes match the reviewed
  candidate; its sole parent and tree were read back. The application diff is
  five files and removes no files.

[Exact-head hosted run 596](https://github.com/c933103/AN-Paint/actions/runs/39056963474)
is asynchronous. Its existence does not establish a pass. The parent review/merge
process owns exact-head CI and review gates.

## Packet

[`evidence.zip`](evidence.zip) includes full-value reviews, the independent challenge,
all local raw test logs, both original-value controls, complete source/resource
comparison, remote tree proof and supplementary check scripts. The scripts retain
the paths used for these runs; cached dependency paths are not portable setup
instructions. [`archive-record.json`](archive-record.json) gives ZIP size and SHA-256;
the ZIP contains its per-file hash manifest. Historical review statements describing
no mutations refer to the review stage; publication and the two bounded changes
are documented here separately.
