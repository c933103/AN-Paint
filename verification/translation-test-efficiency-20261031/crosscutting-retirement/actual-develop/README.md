# Final actual-develop verification — PR254

Actual develop `25f678d2a784ffe096a0eeaf92494c02637e6cc7`, tree `b9b3c557c64d4c0c3e70892bc2fc1527e9945d28`, remained current at18:46 UTC on31 October2026. Its tree equals the qualified source/tested merge. Natural push run41228315594 passed all six jobs; no manual duplicate verification run or release.

Actual artifacts were downloaded and checked against GitHub SHA256 digests:
- Regression13052849296: `bd6df8b90655f89a4af501860f50bb5f7d3cf1b48381048bcacad228ca079e68`. Python1,464 passes (two pre-existing skips); JVM1,501 cases, zero failure/error/skip. All25 preserved script-family consumers plus the21-option identity/platform method are present; the latter runs on both SDKs. Generic all-offered real selection/wrap boundary passes.
- Emulator aggregate13053124725: `3c7b6ee7d05fa70b6c23853e83f67673b1dd175dd787f21b0d8b12917a201bd5`. Native74/74 and app49/49 complete and passed, with exact actual-commit/run/source/APK identity. Attached receipts preserve the precise device/UI scope.

## Actual timing, including the slower final run

| Metric | Prior actual develop0ae/run41222010049 | Qualified PR/run41226217743 | Final actual develop25f/run41228315594 |
|---|---:|---:|---:|
| Python cases |1529|1464|1464|
| Python test seconds |391.007|247.291|327.912|
| JVM cases |1521|1501|1501|
| JVM summed case seconds |732.504|653.540|976.322|
| JVM Gradle step seconds |922.645|799.541|1194.552|
| Regression/lint job log span seconds |1629.088|1330.873|1918.164|

**The final whole job was slower**, 31m58.2s versus the prior actual27m09.1s, despite fewer test executions; Python was faster but JVM slower. The faster qualified-PR22m10.9s is not substituted for this result. VMs/regions differ (centralus, westus, eastus); runner image and restored cache keys match but runtime/cache conditions are not controlled. Reduced active data and test work is established; a reliable overall wall-clock speedup is not. No extra benchmark runs were launched.

## Cumulative source reduction since today's pre-cleanup develop

Original `f3d617d0ec83dcab20d9fd5287272207c17c8d51` remote tree verified as `b72698ab8937bad21431e5c9a8124e2122d0d205`. Git-tree blob inventories, including the subsequent Swedish manual addition:
- All tools/fixtures JSON:148 files /21,886,679 bytes →86 /2,090,207; **19,796,472 bytes (90.45%) net removed**.
- current_localization JSON:137 /19,250,531 →81 /2,066,409.
- Existing unchanged-helper baseline run41198859959:2,086 host /1,962 JVM cases; final actual now1,464 /1,501. Counts include new meaningful manual checks added meanwhile.

This does not certify linguistic acceptance or completion of all project-wide cleanup. The current171-option direct-key inventory and finite remaining-scope plan are preserved in this evidence ref. Remaining priority/AssemblyHelp approval copies and bounded legal/provider/privacy/Unicode/font obligations need mapped treatment, not blind deletion or a new framework.

Original PR254 run41225956381 remains cancelled, not passed; Codex's late-import finding and focused correction remain in prior receipts. Production wording/resources and workflows are unchanged.
