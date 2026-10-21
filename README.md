# Application locale configuration repair evidence

This dedicated evidence ref preserves test-first receipts for AN Paint PR #158. It is not an application/release tree and does not authorize a merge or publication.

## Original installed failure

Release candidate `1c9b71afb5f5cbde39bc5fff70630bca1a7a3419`, version 0.0.41/code 98, failed API30 core job 119030652466 in [run 39540842251](https://github.com/c933103/AN-Paint/actions/runs/39540842251). Activity resources and selected preference were `mnc-Mong`; process default was `en-US` after portrait then first landscape View input. The original exact runtime reset caller is untraced. Raw artifact 12319937300 has SHA-256 `c0f21c0db7240b1387b858ba72029fac45bebe023057fd2b515079df62d0feba`.

## First test-only baseline

Source head `e25ec0b3ab22db220383c1ec8d42beab5576ab71`, checked out by the PR workflow as merge `fc11740c874d07e38e232efcfa382bb5cd7e3b0a`. [Run 39543517996](https://github.com/c933103/AN-Paint/actions/runs/39543517996) completed with a failed JVM stage: 1,272 tests, 8 failures, 0 errors/skips, all failures in ApplicationLocaleConfigurationTest. Existing tests passed; APK/source, exact-script, lint, API35 core/position and final API35 gate passed. Those passes do not make the run a pass.

`baseline1-raw-test-receipts.zip` contains all 134 original JVM XML reports, CI phase receipts/logs, raw lint XML, original Actions job log and parsed failure summary. The complete downloaded 84,013,565-byte artifact is identified by ID 12321207345 and SHA-256 `7be16aeeb61085beed17c4de18a158bd9d1ea77acd2cb751fe2cf1819339c5f4`; bulky screenshot/HTML assets from that artifact are not included in this compact archive.

The first fixture's bare Robolectric Activity shared Application Resources. Its actual Android11 framework-operation test therefore first failed the private Korean alias leak (`ko-Kore-KR` to `ko-Kore-KR-anpaint`), not the desired Manchu-to-English transition. Other controls failed stale Application `en-US` after choice changes. This limitation is preserved, not concealed as the intended reproduction.

## Corrected fixture and proposed repair

Corrected test-only baseline `82cd160e9dc059eb7ccfa9aedc81f959b22a4e93` introduces an independently localized Activity context and stronger controls. [Run 39545448579](https://github.com/c933103/AN-Paint/actions/runs/39545448579) selects release/API30+35. Its outcome is pending at this evidence checkpoint.

Proposed repair `456df2b35bd168cfc575fa1468b3c7409f966bdb`, tree `77beaf518aa7c3a7535309b6245d030ae934e18f`, is stored separately on `repair/application-locale-candidate-v2`. Application exposes the live public app identity to framework locale resets, while Activity/currentResources retain exact private UI resource routing. No system resources/default mutation occurs on the Application resource read. Independent source review found no production blocker; hosted verification is still required.

All version/publication inputs and previous releases remain untouched. PR #114 translations are excluded. No signing, publication, or merge is claimed.
