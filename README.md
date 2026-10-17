# Brazilian Portuguese priority review, 17 October 2026

Reviewed all **341 P0/P1 entries** together: P0 92, P1 249. The complete English and existing pt-BR values, individual linguistic judgments and immutable production consumer context are in `brazilian-portuguese-p0-p1-341-review.json`. The 717-entry canonical catalogue comprises 716 strings and one plural family; the other 376 entries are outside this review.

- Source: `75d56c8c9597f135799d2a3aac84c1e8aa3ee2a4`.
- Application candidate: `76807df744b990159fa62c2a68cfe7f4558b967b`.
- Candidate tree: `170487fc82abd4f5ef68533aecd02325925d77f1`; all 1,183 final blobs and modes verified against the complete 1,180-file baseline plus four intended files.
- Language selection: recent Spanish/German/European-Portuguese batches were already covered by PR109/110. Brazilian Portuguese is distinct. Current open-PR and branch checks found no new overlapping pt-BR implementation. Earlier broad PR7 conclusions remain withdrawn.

## Findings and adoption

The baseline ledger preserves 300 accepted static-context judgments, 29 accepted catalogue-meaning-only judgments, one prior exact receipt, eight proposed corrections and three open holds. Thirty entries have no direct current production reference; no live-use acceptance is inferred for them.

A separate full-pair/context assessment accepted all eight candidates, recorded in `candidate-adoption.json`, without rewriting baseline proposal dispositions or minting aggregate PR56 credit:

1. Recovery instruction names the actual `Arquivo > Abrir imagem` command.
2. Language note restores new-or-untranslated English fallback scope.
3. Collapsed tool-category caption uses fixed feminine `Ferramenta selecionada`.
4. Expanded tool-category caption uses the same grammatical construction.
5. Pixel count uses a count label that remains grammatical for one pixel.
6. Canvas guidance distinguishes spreading/pinching for zoom from two-finger movement for panning.
7. `Nenhuma` agrees with the crop dialog's image checklist.
8. Lowercase `pixels` composes correctly in width/height accessibility captions; standalone `Pixels` is unchanged.

The `FG`, `BG` and unused three-part palette-template holds remain open. Prior exact sampled-resize memory receipt and bounded colour-profile/SVG review references remain preserved. PR56 and its upload hold are unchanged. `supplemental-consumer-context.json` includes the actual span ratio, focus movement and single-finger navigation implementation, not just its accessibility string reference.

## Evidence and limitations

`final-test-summary.json` records complete host, focused, mutation and AAPT2 results. The four new JVM consumer tests are authored and independently source/API reviewed; Android build/JVM/lint/device execution awaits exact-head hosted CI. Neither host source assertions nor AAPT2 XML compilation establishes rendered fit, TalkBack behavior or installed interactions.

This is bounded AI-assisted linguistic/context review, not native-speaker certification, whole-language acceptance or completion of P2/P3. It does not borrow unmerged PR114 runtime-hardening changes.

The ZIP contains source/target review data, prior receipt ledger, the four candidate files, complete reviewed consumer source files, exact contexts, hashes and raw test outputs. For the one-time validator, materialize the complete source checkout at the pinned baseline under source, copy it to worktree and apply application-candidate; the archive intentionally does not duplicate every unrelated application file. Its member manifest and archive receipt are verified. Historical validators are one-time evidence only and are not installed as permanent source-hash CI gates.
