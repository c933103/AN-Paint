# Caption successor: failed trial retained

Run [38118041931](https://github.com/c933103/AN-Paint/actions/runs/38118041931)
tested head `4750d62f1a45d74eb88e3d91a85512e0237e644c` through merge
`8d0dc77d69a3f67192f48deb0d733bdcc77d1885`; both have tree
`912a21a7d071e44fbe4499f5203ddd2b032281a3`.

## Results

- Build, source delivery, test-APK compilation and exact-script generation passed.
  All 487 production files match the delivered source; its ZIP exactly matches
  the APK-embedded source. The artifact/build hashes are in `source-binding.json`.
- All 814 JVM methods ran. Two failed on API 30/35 portrait Honeycomb complete
  bounds: an 88×51px view has only 88×48px visible. The other 812 methods passed;
  lint reported zero issues. Hungarian 1× landscape Add now has intrinsic text
  fit in the diagnostic report. Neither that image nor the model is installed
  acceptance. The unchanged strict whole-view assertion correctly catches the
  remaining portrait problem.
- All three installed colour cases failed at `Timed out: initial editor`, before
  any colour dialog opened. Their original receipts have empty observations;
  both original failure images remain inside each raw app-owned ZIP. The direct
  pre-restoration screenshots show a black activity with system bars.
- Ordinary 19/19 methods completed in 145.847s with three failures, not a phase
  timeout. The 74 native methods and 16 other ordinary methods passed. All three
  subsequent gallery-draft and all four vertical-locale cases failed; restart
  checks were withheld. There is no new colour, state, IME, Back or commit pass.

## Diagnosis and next controlled trial

The first colour activity was recorded RESUMED and Displayed before the timeout.
No app crash/ANR or visible overlay was found. Nearby AsyncRotation and
accessibility-window timeouts correlate with the earlier gallery/font transition,
but do not establish a root cause or identify the failed gate conjunct. A focused
original-line log excerpt is included; the full original device logcat remains
in the Actions artifact, not copied into this focused public archive.

The next harness adds read-only startup flags, nullable canvas/root geometry,
window focus/attachment and configuration at the existing gate boundaries before
cleanup. It does not alter the compound condition, force startup/focus, retry the
activity, or extend the 8s/45s/180s deadlines.

Separately, primary Android LinearLayout source explains how default baseline
alignment can move wrapped text buttons below their row. The narrow next
production correction disables baseline alignment on the two tab rows. Intrinsic
wrapping, minimum 44dp/48dp sizes, input handlers and all complete-bounds/caption
assertions remain. `tab-row-source-diagnosis.json` records the exact source and
hypothesis; re-execution is required. Large text 2× remains unaccepted.

## Archive inspection and reconstruction

`archive-inventory-inspection.json` records every original focused member/hash,
validated nested export manifest, UTF-8 report or synthetic PNG, and inspection
scope. No high-confidence credential indicator was found; no full-device logcat,
credentials or unrelated private data is included.

Concatenate the numbered parts in order, then compare the size and SHA-256 to
`source-binding.json` before unzipping:

```sh
cat caption-focused-evidence.zip.part* > caption-focused-evidence.zip
sha256sum caption-focused-evidence.zip
unzip -t caption-focused-evidence.zip
```

The archive includes all 87 JVM XML files, lint XML, eight model reports and 24
model PNGs, installed phase summaries/XML, three unchanged app-owned colour ZIPs,
public CI log, and source/build/startup diagnosis. Direct receipts/images are
convenience copies; the raw nested exports are the retained original evidence.
