<!-- ang-non-metadata-M1-adoption-20261030-98c30f3db074 -->
## ANG / NON metadata M1 — separate bounded adoption delta

After inspection of the complete independent M1 report, these **six unchanged lexical values are adopted at moderate confidence**. They add **4 P0 + 2 P1**, with **no notation-only entries**. Historical wording totals become **455 adopted / 227 held** (ANG 222 / 119; NON 233 / 108). The prior 449-value packet remains unchanged; this is a later, disjoint adoption delta.

| Locale | Key | Tier | Exact adopted target |
|---|---|---|---|
| ang | colour_truncated_metadata | P1 | Þæt anlicnesgewrit endaþ innan his hiwsidegewrita. |
| ang | ui_autosave_metadata_is_missing | P0 | Sidegewritu þære sylfhealdunge wana sind. |
| ang | ui_invalid_autosave_metadata | P0 | Unrihte sidegewritu þære sylfhealdunge. |
| non | colour_invalid_metadata | P1 | Myndin hefir ógild viðbótarrit um liti eða slík er verkfærit tekr eigi við. |
| non | ui_autosave_metadata_is_missing | P0 | Viðbótarrit sjálfvarðveizlu vantar. |
| non | ui_invalid_autosave_metadata | P0 | Ógild viðbótarrit sjálfvarðveizlu. |

**Limited M1 convention:** metadata means structured descriptive/control records associated with an image or editing state, textual or binary, embedded or archive-associated. The terms do not imply prose, external/sidecar or appended storage, optionality, disposability, or raw pixel content. Historical components support formation/morphology; no historical software attestation or native-human certification is claimed. This does not adopt unrelated terminology.

**Retain HOLD:** ANG `colour_invalid_metadata` (exact relative-clause force) and NON `colour_truncated_metadata` (exact historical ending construction), plus every unrelated hold. No automatic whole-screen, runtime/UI or source-integration acceptance. The 14 notation-only entries remain included in the earlier packet, not added again.

**Bindings:**
- Supplied source: develop `96681f687671a1fdffe134a325843919c1543401`, tree `39bb7351fa5532194e2c0430432b2f0cc6358a86`; no independently resolved local HEAD claimed.
- Author M1 SHA256: `b65ea2e11e612efb1f981b801e562eef25c236edcd60313371c533c0ccca69de`.
- Independent eight-row M1 delta SHA256: `98c30f3db074f272b8e8110f6301222d45cde73bb15d6899c275e4785ecf49df`; all six targets are byte-identical to that reviewed proposal.
- Exact six-row adoption overlay SHA256: `b5605b31b884c78604f0715151613a63e149445c0324a965e019b507d5d34a2d`.
- Separate M1 adoption receipt JSON SHA256: `e3ede12d9f94aa6bd68b01d98bd770555060611b7da3a857e9099b88f9e01062`.
- [Prior 449-value adoption receipt](https://github.com/c933103/AN-Paint/pull/56#issuecomment-6534700034); its immutable JSON SHA256 remains `ac66e6bb17d405b4eb948c7fb445cc6c773b47db8a729c0ccffdd78c2295d06f`.

Documentation only. No application/source/Work/project-test changes, release or merge action; PR56 remains the never-merge tracking draft.