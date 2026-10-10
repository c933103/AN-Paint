# PR18 current-develop integration: accepted bounded evidence

Source head `66c6fd8411dd799c2d2ceb9250c1de500346f3f5`, accepted tree `2ca29f84ce77e8d3be1aa2b7602fa6cca0ca6c31`. This is an evidence-only branch; none of its added files changes the tested source head. All original 1,344 source paths are preserved byte/mode-identically.

## Exact integration and merge

Original PR18 `66c39ca345ef7bc8c5fe1da8ce64cb872c3a0e88` and accepted develop `699f3cb0d3e0fe932fbf39779f852c2b5e9dbf3c` share real merge base `ff2db040272fa522226da60744316bfeb8695cf0`. PR18's 44 changed paths and develop's seven later changed paths are disjoint. The conflict-free 1,344-path union is recorded in `composition.json`, independently recomputed and checked against every remote blob/mode/type before the non-force continuation. PR37 optimized evidence validation and PR42's warning title are preserved.

PR18 merged as `8b9ce13a4d011abadedb8069f81800f156886846`. Readback verified that exact accepted tree and parents `699f3cb0` and `66c6fd84`. This archival branch does not change develop or perform another merge.

## Exact premerge run and source bytes

[Run 38067267565](https://github.com/c933103/AN-Paint/actions/runs/38067267565), attempt1, passed all three jobs. Artifact/build-info identity proves the actual executed merge was `5c791111d6b29035a59267125d0a6e02e4603e0b`, captured against former PR37 head `dbd4d22e` while retargeting completed. That merge has exactly tree `2ca29f84`; new PR18 head already includes accepted develop `699f3cb0`. The post-retarget synthetic ref `c60c1b79503cebeb4e28bd0b9d9b381aad455fa2` has the same tree and current develop/head parents, but was not the ref executed by this run.

- Build artifact11676230206: SHA256 `da34ecfc6fe0d73744f8a7b6d94d90f3c3aaf9eef1c20153207498f5596a9dc1`.
- Regression artifact11675312130: SHA256 `ea1c0b355fbc89dafa805d6fe25a6b33e723e39ab8644b86279c1d030656fa91`.
- API35 artifact11675547516: 3,255,413 bytes; SHA256 `edd6706eb5851cf90a5503c75b1b2794846d8a0e25f8e1a1146f1a90280637b9`.

Production and instrumentation APK compilation passed. Delivered APK/source digests match build-info; APK-embedded and delivered source ZIPs are identical. All1,341 included tracked blobs match the accepted tree. Only two gitignores and one IDEA code-style file are omitted. Four declared native dependency source trees are additionally bundled; this tracked-source comparison does not recertify each upstream blob. See `build-receipt.json`.

## Host and runtime checks

Local command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'`. Result:390 passed, zero failures/errors/skips,143.318s; complete output is `host-tests.log`. Bash syntax and staged/unstaged whitespace checks passed. Actual historical verifier replay in normal Python, `-O`, and `PYTHONOPTIMIZE=1` is byte-identical to accepted source-results.json; the identical retained copy is `replay-normal.json`. The preserved mode suite covers23 invalid prerequisites in all three modes plus valid controls and receipt regressions.

CI Python discovered390, passed388 with two optional Pillow decoder skips,92.660s, within the unchanged120s step deadline. JVM XML:746 cases in78 suites, zero failures/errors/skips. Lint:zero issues. See `regression-receipt.json`.

API35 raw instrumentation was reparsed against exact source inventories and cross-checked with JSON/XML. All98 installed cases passed:74 native,18 ordinary,4 vertical,1 seed,1 verify. Exact24-method app union and the complete live-PID/Gallery/external-force-stop/verified-absence/fresh-verify sequence passed. Phase seconds:82.912 native,160.731 ordinary,122.538 vertical,6.899 seed,8.399 verify. The runner completed at+428s. Existing180s/60s phase ceilings and15-minute outer cap were unchanged.

## Fresh reviews and actual images

The [verified Codex summary6050354262](https://github.com/c933103/AN-Paint/pull/18#issuecomment-6050354262) names exact head66c6fd84 and completed Code/Security reviews. Separately, Codex added PR reaction558844329 (+1) at16:30:33Z after completion. No inline threads or review findings existed at acceptance. See `codex-review-receipt.json`; the reaction is distinct evidence from the summary badge.

All32 original PNGs are retained individually under `screenshots/`. Each matched the downloaded ZIP/receipt hash, fully decoded, and was individually viewed. All eight native format popups visibly show the open list, including the previously stale English-landscape state. Workspace, initial Save, open-popup and JPEG-quality captures are distinct; no duplicate file or decoded-pixel content remains. The parent separately viewed eight originals, recorded unchanged in `parent-visual-sample.json`.

Acceptance is limited to the API35 capture-state matrix. Manchu landscape slider thumb and several portrait labels/neighboring columns remain clipped. The five questioned dialog regions are pixel-identical to prior accepted66c39ca captures; see `prior-visual-comparison.json`. PR18's visible-center/minimum32dp oracle does not establish whole controls or full-range native gestures. PR41 separately demonstrated ancestor interception and corrected slider ownership and vertical-text redraw; its [prior exact-source evidence](https://github.com/c933103/AN-Paint/pull/41#issuecomment-6095226895) does not retroactively make those fixes present in PR18. No broad usability, linguistic/all-glyph, API30, physical-device, alternate-route or release acceptance is claimed.

## Archive status and later verification

The original API35 ZIP was fully downloaded and digest-checked before acceptance. Its small binary archival parts and the regression-essential ZIP are being added to this same evidence branch; until their manifest is published, only the individual PNGs and the receipts above are claimed durable here. This explicit archival status does not change the completed checks or source.

The independently completed postmerge verification is preserved separately in [postmerge evidence9ec5c371](https://github.com/c933103/AN-Paint/tree/9ec5c3718b3ed0e5359f9a2adf2b44618cae91b7) and [receipt6100769642](https://github.com/c933103/AN-Paint/pull/18#issuecomment-6100769642). This premerge archival continuation does not duplicate that work.
