# Shared typography resource-context repair: independent authoring review

## Current result

No remaining source-review blocker on staged tree `cf1ffdb16e4e8401edce81a50b16ad6f21cdcaa8`, compared with accepted tree `b6bf7626c1d7c4aef669394970046ffc89a5c877`. This is a source/host-contract review. Android/Kotlin compilation and fresh native/installed behavior have not run locally; their hosted result remains required.

The ready-triggered P2 is source-supported: a resource-context UI locale and a different process default could select correct direction but omit the bundled UI face. The prior accepted runtime evidence remains bound to its own source and does not establish this newly controlled mismatch case.

## Reviewed scope and semantics

- Four production files only: VerticalText, LocaleTypography, LocaleTooltip and FontCatalog. Existing API21/API24 resource-locale selection is extracted without changing its branch semantics. Default UI typeface and context direction now share that lookup.
- Notification/tooltip vertical exclusions use the same context as the selected UI face. The notification host, lifecycle, duration and fallback implementation are unchanged.
- FontCatalog passes its already-selected process locale explicitly, preserving drawing-model semantics. Explicit picker-row locale overrides, font-preview exclusions, asset mapping and caches are unchanged.
- GalleryTypography's actual MediaGalleryActivity call already supplies AppLanguage.locale(activity) explicitly. Its separate defaults are not a necessary dependency of this repair and remain unchanged.
- Existing resources, fonts, legal notices, installed tests, workflow, deadlines, script controls and documentation are unchanged. This preservation check is a one-time review, not a new permanent CI source gate.

## Tests and resolved authoring findings

The new controls cover each offered Mongolian-script tag plus Nôm and Wu, fresh widgets created after a process-default reset, later installed children/spinner rows, known bundled assets, explicit drawing/preview preservation, explicit locale overrides, inverse English resources, and tooltip direction/font agreement. Native API30/35 additionally check sample glyph availability; API21/24 establish binding using Robolectric's legacy graphics path and do not prove real glyph geometry. Existing direction lifecycle tests additionally exercise Nôm/Wu and construct font-bound controls after callbacks/default resets.

Six older fixtures now configure their own resource context consistently with the locale they intend to test. Existing rendering, native popup, lifecycle and timeout assertions remain. They do not substitute process-locale alignment for the new mismatch controls.

Three issues were addressed before the final freeze:

1. The first new fixture called createAccessibilityNodeInfo on detached API21 views. Exact Robolectric 4.14.1 selects Android 5.0.2_r3, whose View implementation dereferences mAttachInfo on this path. The final fixture removes only that invalid detached-node assertion and expressly relies on the separately attached notification/dialog coverage. Logical text and independent font/glyph assertions remain.
2. The changed notification branch originally had only matched-locale fixtures. A new attached-host test now checks Nôm/Wu resources versus a Mongolian process default, full accessible text, known bundled face and existing timeout; Mongolian/English resources versus Nôm process default retain their appropriate toast path.
3. The first full host run exposed one further source-wiring expectation for the old no-argument vertical guard. That expectation now requires the context argument; the surrounding characterization and negative controls remain unchanged.

Primary sources for the API21 fixture finding:
- https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/robolectric/src/main/java/org/robolectric/plugins/DefaultSdkProvider.java
- https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-5.0.2_r3/core/java/android/view/View.java (onInitializeAccessibilityNodeInfoInternal, lines 5275–5276)
- https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/ShadowView.java
- https://raw.githubusercontent.com/robolectric/robolectric/robolectric-4.14.1/shadows/framework/src/main/java/org/robolectric/shadows/GraphicsShadowPicker.java

## Executable checks and binding

Independent focused host checks passed 102/102 ordinary in 11.688s and 102/102 optimized in 11.087s against the initial e44ab250 draft. Those logs retain their pre-correction attribution. On the final cf1ffdb1 tree, the expanded independent set passed **108/108 ordinary in 11.583s and 108/108 optimized in 11.135s**, both exit 0.

The final one-time scope/inventory check passes: **15 changed paths**, all **910** prior expanded JVM identities retained, **22** additions, **932 expected executions**. The additions are five font-control methods on API21/24/30/35 and one notification method on API30/35. Source hashes and complete current-source inventory are in `final-source-scope.json`; the portable scope checker is included.

The first full host attempt on 9dfe21eb ran 650 methods and failed one stale source-wiring spelling check (exit 1, 127.623s). The original failed log/receipt remain preserved in the writer packet's `pre-guard-correction` directory; `preserved-failed-attempt-binding.json` independently binds the exact bytes and failed identity. No failure is relabeled as a pass.

Final writer aggregates independently reconcile against all **650 current source-discovered host identities**: ordinary **126.357s** and optimized **125.394s**, both exit 0, zero skips/failures/errors/missing/unexpected identities, unchanged **240-second cap**. The warning-wrapped method with a separate `ok` line is included. Deliberate negative-control JSON failures after the unittest summary are not actual failed methods. `writer-host-log-audit.json` binds both complete logs and receipts; `audit_host_aggregates.py` replays this check using the separately retained writer directory. No local Android run is claimed.

## Fresh hosted acceptance scope

Bind source, head, synthetic merge, tree, job and artifact receipts for the final published candidate. Require all 932 current-source JVM identities, including the 22 new executions and the extended lifecycle bodies. Retain real compiler/API errors as failures. Verify the selected installed API30 and API35 source/protocol/identity unions and current APK/corresponding source, including fonts and locale resources. API21/24 JVM legacy binding must not be described as installed legacy rendering.

The unchanged M04/notice pixel requirements still need current-source diagnostics and complete captures. Previous images may be reused only after exact equality; any changed font/layout capture requires fresh inspection, and the previously reviewed mixed-Arabic fringe remains an explicit source/run-bound disposition. Do not infer unchanged visual behavior from the small production diff. Physical-device, TalkBack, linguistic and release acceptance remain separate.
