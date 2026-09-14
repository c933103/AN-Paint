# AN Paint 0.0.28 release preparation

Package `paint.anpaint.android`; version code 81. The intended release updates
0.0.27 and previous compatible builds using the existing signing certificate.

[PR #1 review and corrections](verification/0.0.28-review.md) records the findings,
preserved behaviour and translation limitations. The merged PR's existing CI
passed; the corrected release build is undergoing release-variant regression,
lint and Android 30/35 verification. No release-completion claim is made here yet.

The release will contain the signed universal APK, exact corresponding source,
checksums and verification evidence. The private signing key and private build
backup must never be published to GitHub.
