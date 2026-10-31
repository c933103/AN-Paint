# Memory-warning source semantics and outstanding review

Canonical Android XML is the current wording authority. The two-term linguistic
review remains outstanding where its evidence did not establish acceptance.
Removing copied approval queues from CI grants **no new linguistic acceptance,
whole-language completion, or restoration of withdrawn review conclusions**.
Historical counts below are snapshots, not current progress or current coverage.

## Distinct consumer predicates and remedies

- `ui_no_resize_fits_decoder_memory`: the import dialog warns for valid entered
  dimensions when the plan fails and `hasNativeWork && !accepts(minimumPlan,
  residentPixels)`. The minimum plan is 1×1; admission combines editing/resident,
  native-or-decoded-plus-metadata work, further buffers and allocation guards.
  This is failure within current editing-memory limits, **not a decoder-only
  diagnosis**. The remedy remains cancelling and using a smaller source image.
- `ui_assembly_source_memory_floor`: the assembly path warns when `suggested`
  returns null on `!fits(1×1)` and creates no output. Its combined estimated peak
  is the maximum of output/resident memory and each placed source's combined
  import estimate; it is not a sum of all source decoders and does not share the
  import `hasNativeWork` predicate. Reducing output dimensions alone is not enough:
  close other documents or prepare a smaller source image. The assembly is unchanged.

The [original source finding](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6314782623)
and [complete original explanation](https://github.com/c933103/AN-Paint/blob/25f678d2/translations/source-review/README.md)
retain the formulas, counterexamples and review qualifications. Existing source
modality tests and actual memory/decoder/admission consumers remain active;
the fixed memory-modality regression fixture is not retired.

## Recoverable review history—not active test oracles

The original queue and every successor packet remain in immutable source history:

- [Initial 171-option/two-term queue](https://github.com/c933103/AN-Paint/blob/25f678d2/translations/source-review/memory-warnings-20261021.json)
- [23 October successors](https://github.com/c933103/AN-Paint/blob/25f678d2/translations/source-review/memory-warning-successors-20261023.json)
- [25 October successors](https://github.com/c933103/AN-Paint/blob/25f678d2/translations/source-review/memory-warning-successors-20261025.json)
- [Amharic successor packet](https://github.com/c933103/AN-Paint/blob/25f678d2/translations/source-review/memory-warning-successors-amharic-20261025.json)

[Bounded review receipts](https://github.com/c933103/AN-Paint/blob/4590c20ca8a8f159f63afa3294bc908f8ed62394/verification/translations/memory-warning-successors-20261023/receipt-exports.json)
remain preserved with their original qualifications. Reviewing a future wording
change should compare current text and the relevant consumer predicate, not
update a second complete catalogue or reconstruct predecessor snapshots in CI.
