# PDF import and preview diagnostics: Old English and Old Norse

Base: `62b2131be57243af94cd8ac93d65b24cc63b5465` on `review/nv-bottom-2038-20261103`.

Added eight P2 strings per locale in `values-b+ang` and `values-b+non`, covering PDF import validation and preview-memory failure. Canonical wording remains in the Android resources, without duplicated approval-text fixtures.

## Context and review

Source consumers checked: `PdfCodec.kt` and the page-preview path in `ImportSelection.kt`.

- A read failure remains uncertain: the file may be damaged or contain features unsupported by the current Android version. It does not assert confirmed damage.
- The password-required and unsupported-encryption alternatives remain separate. The proposed remedy is saving an unprotected copy before import, without asking the user to disclose a password or promising successful decryption.
- A PDF must be nonempty and no larger than 512 MiB. The page count retains the inclusive 1 through `%1$d` bound.
- Invalid dimensions and dimensions too large for import remain alternatives. A crop must be a rectangle inside the selected page with positive width and height, preserving the source's nonempty-region requirement.
- Rendering is constrained by the available image-memory budget. Failed-preview guidance offers smaller dimensions only when possible, without guaranteeing that resizing will always make the file importable.

Independent semantic and linguistic review accepted all 16 strings unchanged. Existing page, preview, rectangle and memory terminology is reused. Password/encryption and software-version expressions are transparent modern computing adaptations within these historical-language catalogues, not claims of ancient technical attestations.

## Validation and coverage

- All 78 repository host tests passed against the accepted candidate.
- All 171 offered-language structural checks passed.
- XML parsing, unique typed keys, Android escaping, source attributes, ordered typed placeholders and exact newline escapes passed. PDF/Android identifiers and numeric bounds were checked.
- All 493 previous resources and their original bytes per locale remain unchanged. Each resulting catalogue has 501 typed resources: 500 strings and one plural resource.
- All direct resource references in `PdfCodec.kt` are now present in each catalogue. The shared import chooser's separate animated-frame lower-bound caption remains outside this PDF batch; the whole shared chooser is not claimed complete.
- Per locale, P2 direct coverage increases from 146 to 154 of 305. P0 remains 94/94, P1 249/249 and P3 4/71.
- All 1,276 materialized base files match remote Git identities/modes. The 165 unmaterialized research/verification records are preserved through the base tree. Only the two catalogues and this evidence record are intended publication changes.

These results do not certify an Android build, device rendering, screen-reader execution, runtime plural routing, external CI or historical-language specialist quality. No issue1 action was attempted.
