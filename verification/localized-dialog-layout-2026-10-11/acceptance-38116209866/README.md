# Bounded PR49 acceptance: run 38116209866

[Draft PR49](https://github.com/c933103/AN-Paint/pull/49) fixes shared About-heading
and legal-notice heading/footer truncation without changing translations or legal
bodies. C05 and M02 remain separate until parent-managed composition.

## Exact identities

- Source: `d7f1a95835704d2b263866895babaffa9a16b49e`
- Tree: `32957329aef7dc966d4a138c24c1a9292deb1de5`
- Tested merge: `ec952b34919725b67e698b4df34e988e4433bc42`
- Develop parent: `691f8870649a1d21d1441f4e3d0e795660b23e9a`
- [All four CI jobs passed](https://github.com/c933103/AN-Paint/actions/runs/38116209866)
- [Exact-head Code review found no major issues](https://github.com/c933103/AN-Paint/pull/49#issuecomment-6106027171)

The intended and remote source trees match across all 1,589 leaf paths, modes and
Git blobs. The debug APK and corresponding-source ZIP match build-info hashes;
the embedded source ZIP equals the sidecar. All 1,586 delivered tracked files
match this tree. The three omissions are packaging metadata: two `.gitignore`
files and `.idea/codeStyles/Project.xml`. This is a CI-debug build, not an
original-signer upgrade or release acceptance.

## Verified results

- 587 host checks pass; 50 selected checks also pass under Python `-O`.
- Original XML: 836 JVM passes across 87 suites, no failures/errors/skips;
  all 28 shared-dialog cases pass on API30/35 Robolectric NATIVE.
- All 380 localized model report files are byte-identical to the previous run:
  170 PNGs, 170 JSON records and 40 pointer traces.
- Original installed protocol replay: 104 passes, comprising 74 native and
  the exact 30-method API35 app union, including both restart phases.
- Five source-bound installed dialog exports pass independent collection;
  all ten original PNGs were inspected by the implementer and reviewer.
- All seven native Back actions establish specific-window detachment and
  the required focus/callback outcomes before cleanup. Credit retains its draft
  and selection through live rotation, with four saves and two dismissals.

App source-test digest:
`aaaeee9481ac0d47a8724e29b82fc3adbe7d6d8f3b5597be85ed591d213e75e9`.

| Installed phase | Passed | Seconds | Cap |
| --- | ---: | ---: | ---: |
| Native | 74 | 61.414 | 180 |
| Ordinary | 16 | 126.674 | 180 |
| Gallery | 3 | 46.178 | 90 |
| Dialog | 5 | 103.192 | 300 |
| Vertical English/Manchu | 2 | 114.997 | 180 |
| Vertical literary Chinese/emoji | 2 | 109.226 | 180 |
| Restart seed | 1 | 6.091 | 60 |
| Restart verify | 1 | 7.893 | 60 |

Each complete dialog interaction passed its unchanged 45-second bound:
third-party notices 25.693s, artwork 18.016s, GIMP 22.337s, credit 13.434s,
colour diagnostic 1.843s. Receipt metadata separates setup and teardown from
interaction time. The phase includes all five fixtures and export work.

## Actual image and reachability interpretation

The three real French About-to-notice flows at 2× exercise heading lines, menu
rows, exact bundled bodies, Copy/clipboard, Other terms, nested Back, Done,
reopening and closing Back. The first also retains actual About and notice
instances through rotation. The Hungarian credit fixture at 2× checks native
Save/Copy/Done/Back, text/selection and listener retention.

The About landscape and artwork final screenshots show the last heading lines
after scrolling; earlier lines are outside the current viewport. The per-line
receipts prove sequential native-scroll reachability, not simultaneous complete
visibility. Credit portrait includes a saved toast, and its landscape screenshot
shows an initially partial action area before later successful native scrolling.
No clipped initial frame is silently relabelled as a fully visible viewport.

The colour case deliberately records the known short-landscape limitation and
Cancel once/no commit. Its current provenance pins the independently verified
[untouched-develop installed failure](https://github.com/c933103/AN-Paint/tree/8096234be003cd6a287660d32884c2541c518e65/verification/advanced-colour-viewport-2026-10-11/baseline-run-38112708313).
`positive_viewport_accepted` remains false. The original positive oracle belongs
to the separate PR51 correction and must replace this diagnostic explicitly when
those source changes are composed.

## Evidence and remaining boundaries

`receipt.json` records identities, phase/case timing, exact screenshot hashes and
scope. The source binding, original protocol replay and collector verification
are preserved beside it. Standalone current installed evidence uses bounded
50,000-byte deterministic parts with verified original ZIP/member hashes; it is
independent of the held historical archive bytes.

Earlier failures remain failed. In particular, run38114313848's combined About
case ended after 45.715s without completing the flow (the recorded
`block_completed` value is false); the succeeding source decomposes all three
complete flows without changing their per-notice assertion body. Its original
source/range and failure are retained under the PR49 source's
`notice-case-successor/` directory.

The full historical raw archive chain remains unpinned while original part166 is
held. That pending action is not retried or bypassed by this independent current
acceptance record. Current success does not erase earlier model/device failures.

Source applicability covers the default and 142 catalogues, while model runtime
coverage samples 15 horizontal and five vertical profiles. No all-language,
native-language, physical-device, TalkBack, API30-installed shared-dialog,
original-signer, merge or release acceptance is implied. The artificial joined
Mongolian stress captures prove reading offsets only; actual-caption model
footer/pointer cases remain distinct.
