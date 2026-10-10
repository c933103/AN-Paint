# Retained device artifacts from failed PR34/PR41 run 38073935029

This is an exact-byte archive of the original API30 and API35 device artifacts, not a new validation run or a successful combined result.

- Source head: `739a3dcf1a59785d98a5f5a00f4b76a1b00e6472`.
- Source/tested tree: `6d6b90c1999d9e771970ab08e4c275e999c446ca`.
- [Original failed Actions run](https://github.com/c933103/AN-Paint/actions/runs/38073935029).
- API30 artifact `11677704020`: exact `device30.zip`, 630,778 bytes, SHA256 `a676f3ee8e164864e613c3a696256391bc096df1492763b399641234e8ad12b2`. Its 73 native + 22 app method union passed; external-files screenshot collection failed with Permission denied. No API30 screenshot acceptance is claimed.
- API35 artifact `11678419053`: exact `device35.zip`, 5,106,985 bytes, SHA256 `a813678e7a67623567a5b7e890449be7c822c8af38463db22c2a3db9f1463ca6`. It is stored as 20 ordered pieces, each no larger than 256 KiB, because the earlier whole-blob orchestration never returned. The deterministic whole-blob identity was checked and absent before these piece uploads. No uncertain write was duplicated.

Run `python3 reassemble.py` to verify both archives without writing or extracting anything. To reconstruct API35, pass `--output` with a new directory whose parent exists. The script checks every piece's size and SHA256, the complete ordered inventory, both original ZIP hashes and ZIP integrity before writing. Checks remain active under Python optimization.

The original API35 source/raw union, 96 decoded images, eight reachability receipts and 28 native drags passed independently. This historical run was not given a pixel-review acceptance. Its API35 subjob success does not supersede the failed Python Actions step or API30 collection failure.

The Python Actions step timed out after two minutes. A later process exit zero (462 tests in 176.348 seconds, two named inherited optional-Pillow skips) remains a late process result and does not convert that Actions failure into a pass.

[Separate immutable failure annotations, source bindings and budget preparation](https://github.com/c933103/AN-Paint/tree/191424b803957be1a87ec185d0b6d13e7badfbb8/verification/pr34-pr41-integration-2026-10-10/budget-preparation).
[Separate completed source/transport preparation](https://github.com/c933103/AN-Paint/tree/ffdf867fa5c7e3552f2806d55a51b10a5aa8ae2a/verification/pr34-pr41-integration-2026-10-10/transport-preparation).

Scope limit: this directory permanently retains the two raw device ZIP artifacts. The larger original build/regression/instrumentation ZIPs are not claimed archived here. Their original artifact identities and the already retained text/source receipts remain separately recorded. Later PR34 heads and CI outcomes are separate and are owned by the current integration coordinator.
