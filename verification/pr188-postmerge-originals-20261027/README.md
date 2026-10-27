# PR188 actual merge-push verification

Source commit `1126b650216478c422997dcd1236ca6cc780e4e3`, tree `8e2b7586b62e65bc8afaf007751b9cb3d2d91c92`. Actual push [run 40485214055](https://github.com/c933103/AN-Paint/actions/runs/40485214055), not the earlier PR cohort.

Independent original-artifact verification passed: all six terminal jobs; seven ZIP digests/sizes; 1,423 JVM tests across 155 suites including all six new Portuguese/Spanish methods, zero failures/errors/skips; lint zero; API 35 exact-source test inventories 74 Paintroid + 47 app with all ten raw protocols reparsed and the complete union revalidated; all 13 probe outcomes/log hashes; APK/source/test APK identities; 1,402 included Git blobs match the merged source tree. The three source-archive omissions are repository metadata explicitly listed in the receipt.

The archive contains complete source/test inventories and Git-blob bindings, original bounded JVM/lint/instrumentation/probe reports, metadata IDs/digests, the verifier and terminal receipt. Large APK binaries and screenshots are not duplicated. Original artifacts remain identified by workflow and artifact IDs. To rerun, download those original artifacts, restore the verifier’s expected relative working layout, extract the source ZIP from the APK/source artifact and execute the verifier. `MANIFEST.json` binds every archived member.

A truncated first APK/source download was rejected before any pass claim. `download-recovery.json` records its exact partial size/digest and the successful retry of the same original artifact. Transport URLs and credentials are excluded.

This evidence does not certify native fluency, TalkBack usability, all locale layouts or all devices. Existing colour scope stays preview-rail reachability and Cancel for API 35 en-US/hu at 2× 640×320 mdpi, with separate IME/Back/footer lifecycle, not universal 2× or simultaneous whole-dialog/IME fit. Release 0.0.41 remains paused; other explicit project holds remain unchanged. Evidence only: no application source changes.
