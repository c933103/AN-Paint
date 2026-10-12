# M04 recovery checkpoint — 12 October 2026

This evidence-only checkpoint preserves recovered work after loss of the temporary filesystem. It does not change application source or claim M04 is complete.

- `frozen-partial53.tar.gz`: all 116 frozen source, fixture, font and evidence files from the **53-value partial** checkpoint. Every recovered file was verified against its original Git blob SHA and byte count in `frozen-partial53-manifest.json`. Historical test failures and provisional review remain historical.
- `language-review59-recovery.tar.gz`: independently recovered successor language-review artifacts.
- `accepted-and-proposed-values-v4.json`: exact final 59 accepted UI values, SHA256 `00830298aefa73ca075d585c4d9191e1f2fdf5becbd9320783b5e11fa7409e1d`, matching the pre-recovery recorded hash.
- Final decision v4 and successor source registry are explicitly labeled reconstructions where their original whole-file bytes/hash were unavailable. The exact values were recovered; no new linguistic review or native-speaker certification is claimed.

Pinned application base: `4231edaac45d89c52f51e2b77d0f94a1176ad88c`; base tree `c1d65b3f0f89a8af12a9dbe69eb1824ef19e28c1`. The historical expected partial tree `ef14491b87fb4a1cccfa02887a5ca17fdb46c65f` returned GitHub 404 during recovery. No application branch or PR had been created. Prior font blob creation was confirmed, while binary readback through the UTF-8-only connector was unavailable. This checkpoint is a separate reachable preservation record, not a retry of the interrupted partial tree write.

Next: integrate all 59 exact values into application resources, preserve strict completeness and historical baselines, rerun scoped/full host tests, obtain fresh independent technical review and hosted Android CI/render evidence before readiness. Root owns readiness and merge. M02/PR47, AN53 archive, device/archive/release holds remain unchanged.
