# PR59 finite native-screenshot profile

[Source 575a23220f5baac57fbfafa26c66bbfbea268c7a](https://github.com/c933103/AN-Paint/pull/59), tree 5194abcd7521c26b97a3e4bbffec36911272323a. The complete 1,099-file remote tree and modes match the reviewed checkout.

The correction replaces general palette/ancillary PNG handling with a documented static RGB8/RGBA8 screenshot profile. CRC, bounded metadata/chunks/scanlines/zlib, archive and source binding remain checked. Unknown formats fail explicitly as unsupported; image interpretation and visual/input acceptance remain separate. No dependency or Android production change.

Both frozen host modes pass 662 tests (ordinary 129.868s, optimized 133.765s) within 240s with unchanged tree; focused transport modes pass 38. Independent complete-contract review is recorded separately. Existing 202 API30/API35 capture bytes and hashes were checked against this finite profile. Those one-time comparisons are not source CI dependencies.

[Exact-head Codex](https://github.com/c933103/AN-Paint/pull/59#issuecomment-6135037526) is clean. [Final-source full Android CI 38325525117](https://github.com/c933103/AN-Paint/actions/runs/38325525117) is running at this receipt. Predecessor 21884777 full run 38323867743 succeeded, but is not final-source acceptance.

Initial preparation and intermediate findings remain alongside this directory on the separate evidence ref. No old denied raw-evidence upload was resumed. Font 2x, physical-device, TalkBack, linguistic and release acceptance remain open.
