# PR246 explicit synthetic IME setup evidence

Final source head: 03efdfe82823ad52b08a2e9e87dcde6404c31671.
Final source tree: 0ebdc84449c7c9b6a2f011a54a11580cf3af59bc.
PR: https://github.com/c933103/AN-Paint/pull/246

## Separate runs
- Actual failed push: c000194d3f96b89896d679214d2a43889a27356a, run41173526887, core124457749666, artifact13032339137 SHA256b9159743a8a4fcbf00105c5d7e64eb7ce25e8c6adedc65a2b7dcc9b7376e07b4. English/Hungarian synthetic SHOW_IMPLICIT request returned true but IME logcat rejected PHASE_IME_ON_SHOW_SOFT_INPUT_TRUE. Native screenshots/receipts show absent keyboard. Native74, ordinary19, gallery3, vertical4 passed; dialog12/14; restart seed/verify NOT RUN because dialog failed; composed failed. Pulls and logcat exit0; transport_complete=true. No original rerun; no claim of translation causation or transport flake.
- Premerge passing: source764744060fba578a8e2c2eddefc4e8da5062d88a, tested merge bb7692841b1986578b65f2c3dbc9ade90c2c02de, run41170013217, artifact13031475140 SHA256a6bb24218a13d45885b523ca614c8aeab0e07a2921cb5b32493b98a9db443579. Same fingerprint/geometry, implicit request did render fullscreen IME. This does not clear actual push failure.
- PR246 passing device run41175482973, tested merge4cb8e778eaf768a0fb77807c6ccef2b4641d244a, source03efdfe82823ad52b08a2e9e87dcde6404c31671. Core artifact13033306661 SHA2564f2c504bad642be53d5829fe8605bb53fc194e3074f86d83dadeb4bdce206314; composed artifact13033781550 SHA256ae01d0fdec7f9ab2d95f3b8cedf9696c08b4f59b9722800c716888e7e7290c00. Native explicit showSoftInput(0), fullscreen show/hide, Back/footer lifecycle pass: English19.159s/Hungarian22.043s. Restart1+1 and complete composed49/49 pass. Host JVM/lint still running when this snapshot was written; not an aggregate completion claim.

## Local host checks
Frozen final source: normal2072 tests pass1640.195s; optimized2072 pass1574.457s; both exit0. Git tree checked before/after with clean worktree. Focused62 also pass normal/optimized.
`postmerge-ime-full-normal.log` is SUPERSEDED MUTABLE SOURCE DIAGNOSTIC ONLY: initial source changed while this run was in progress; explicit source-digest mismatch appears; safely interrupted with tool-confirmed exit130. Partial F/E remain unclassified beyond the emitted mismatch; no completion credit. The final-normal/final-optimized logs are authoritative frozen-source runs. Failure messages within successful suites are exercised negative fixtures, not test failures.

## Scope
Only synthetic 2x lifecycle precondition changed to explicit0, not forced. Production code/input modes, timeouts, retries, native show/hide/Back/footer assertions, selection, callbacks, and exact composed inventory unchanged. Receipts keep initial native activation not-tested, full-field visibility and simultaneous IME/field/footer fit not-accepted. Do not infer universal 2x layout acceptance.
