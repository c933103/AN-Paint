# Independent PR55 diagnostic successor source review

## Conclusion

PASS for the narrowly scoped diagnostic source change. No blocking source-review finding. This is not a fix or an Android/runtime acceptance: the first exact-source hosted run remains failed, and this successor has not yet compiled or executed under Android/Robolectric.

Reviewed checkout: `/workspace/shared/anpaint-pr55-landscape-diagnostic-20261012`. Immutable base tree: `d80218496e45bbefcaa378d40e5cd9846b7988ee` (failed PR55 head `b95c9a682c77f5dfa9b9a1f4eacabd9d9a03265a`, tested synthetic merge `14b1fdf8e02ebe6f765d63906f05c7e808524b76`, run 38239121942). The source manifest here binds exactly seven changed/new source/test/fixture files; it does not claim the later publication/evidence tree.

Final flow SHA256: `4624896010fa18484e64f60f97d7e56a81c520f1b4c8b6c14e2335468f207111`.

New pinned inverse fixture SHA256: `b41ec5e2d53ea0cb8cc64f9cef5d6cd8800e3c2b9e8a07828d647eef7a895356`.

## Exact scope and preserved checks

Independent `audit_diagnostic.py` compared every one of the 1,947 actual immutable Git-tree blobs with this checkout. Exactly 1,943 remain byte-identical. Four modified files restore byte-for-byte to the actual original Git blobs through the new explicit pinned inverse fixture:

1. `CommonsMetadataQueryFailureFlowTest.kt`: pre-assertion diagnostics, contextual assertion message, bounded per-profile failure collection, completed reading-start layout for vertical success captures.
2. `tools/commons_metadata_m04_composition_scope.py`: apply exact diagnostic inverse before old projections.
3. `tools/test_commons_metadata_m04_composition.py`: narrowly projected checks retaining historical pins and corruption controls.
4. `tools/test_localized_dialog_composition.py`: apply the exact diagnostic inverse to the M04 added-test source pin.

Three new source paths are the diagnostic inverse helper, its fixture and six host contract tests. Every historical fixture, manifest, evidence file and old expected-890 inventory remains byte-identical. Production/UI/HTTP behavior, all 59 translations, font/inventory/licence, limits, timing and all other source files are unchanged. No PR51 or stopped PR53 import is present.

The historical composition corruption tests still validate their historical endpoint, after reversing only the fully hash-pinned diagnostic delta. The new six contracts reject original/missing/duplicated/altered/unrelated successor content and fixture corruption, including under Python optimization. The same 16 M04 flow identities are retained, and a new evidence-only inventory binds the unchanged exact 890 identities to the changed flow source without repinning the old inventory.

## Diagnostic behavior reviewed

- The exact `getLineLeft >= -1f && getLineRight <= layout.width + 1f` assertion remains. The same condition is additionally reported as a diagnostic boolean; no extra pixel allowance is introduced.
- Normal-landscape profiles save the real root raster and the same native Layout drawn on a finite expanded transparent canvas before the line-width check. They retain resource/text locales, configured scale/density, view/content/layout/window geometry, line start/end/text/advance/ellipsis and per-line painted bounds.
- Four expanded-canvas edge-contact flags make potential probe clipping visible. The report explicitly limits ink measurements to native line boxes and a finite margin. These pixels cannot establish installed-device behavior or global font shaping correctness.
- Post-fetch profile AssertionErrors are collected after normal `withGallery` cleanup, and an aggregate assertion still fails the JUnit method. Startup/in-flight failures rethrow immediately. No failed action is retried and no failure becomes a pass. Non-AssertionError exceptions are not swallowed.
- Existing success captures are retained. Vertical endpoint-reachability checks remain, followed by actual measure/layout and an assertion of the correct reading-start scroll. Success JSON now records status-parent scrollX, correcting the earlier unverified deferred-reset capture position.

## Executable evidence

Reviewer ran the three relevant contract modules normally: six diagnostic + nine M04 composition + seven localized-dialog composition methods, all 22 PASS. Reviewer also ran the same 22 under Python `-O`, PASS. Source inverse audit and `git diff --check` PASS. Logs are included; no full aggregate was rerun by this reviewer.

Writer logs independently read: clean ordinary full aggregate, 666 tests in 182.529s, OK, with writer-confirmed forwarded command exit0; separate fail-fast full aggregate, 666 in 185.243s, OK (its raw Python exit status was not separately retained); optimized focused32, PASS. `observed-writer-checks.json` binds raw logs and summary line numbers. Later `success:false` JSON in successful logs belongs to deliberate negative fixtures, not an overridden test result. The initial 262-failure log invalidated by the writer's mid-run source changes is preserved and receives no acceptance credit.

## Remaining gates

Kotlin compilation, actual generated diagnostic artifacts, source-bound JVM rerun, lint/build and relevant installed checks for the successor remain UNRUN here. Preserve first-run failure and its 85/112 renders separately. The initial failure is localized by source/capture order to ain-Kana copy at 640x320 DP/font1.0, but actual clipping versus line-metric/fixture semantics remains unresolved until the failed layout's new metrics and pixels are inspected. Do not relax its threshold or describe the diagnostic successor as repaired.

A later run must bind its actual tested merge/commit/tree and downloaded artifact hashes. Keep the first-run checker frozen to d802 and its original JSON schema; create a separate successor checker for the new scroll field and diagnostic directory once the publisher supplies final bindings.

## Reproduce

```sh
python3 audit_diagnostic.py --repo CHECKOUT --output source-scope-result.json
cd CHECKOUT/tools
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_commons_metadata_m04_diagnostic test_commons_metadata_m04_composition test_localized_dialog_composition
PYTHONDONTWRITEBYTECODE=1 python3 -O -m unittest -v test_commons_metadata_m04_diagnostic test_commons_metadata_m04_composition test_localized_dialog_composition
```

The audit requires the immutable d802 tree to be available in the checkout's Git object database. No source/publication changes were made by the reviewer.
