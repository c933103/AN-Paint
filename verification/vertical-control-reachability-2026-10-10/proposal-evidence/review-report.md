# Independent review: bounded source/mock acceptance

## First proposal

Tree `8a45b54bbbb975d4d7331d8a6ceb62b85eadbffc`, patch SHA-256
`4296f8a6ae8a9d6d576161eea5b54e70396866def2c7783acb0fd0b2b220e01b`.

1. Portrait confirmation persists quality 1. The landscape endpoint sequence
   `[100,1]` could leave Cancel's draft equal to remembered quality 1, so an
   erroneous Cancel-only persistence would not be detected.
2. Both test-only visibility helpers returned the output rectangle even when
   `getGlobalVisibleRect` returned false. Android explicitly leaves that output
   undefined on false; a nonempty intermediate rectangle cannot establish visibility.

## Corrected proposal

Tree `186de374ffce6dabd549a5b7982b5344f9724fec`, patch SHA-256
`3a74f71ef05f36fcba84beb7027f0aebdd89b420f75b0b9fc0ae692f4cdc1d96`.

- A real endpoint gesture makes Cancel's draft differ from remembered quality
  whenever needed. Both values are recorded and asserted; the receipt verifier
  rejects the equal-value landscape regression. Both endpoint images remain required.
- Both helpers now return a fresh empty Rect on false. Each has an installed
  fake-View negative that supplies nonempty output while returning false. Host
  source mutation contracts detect removal of either guard. Installed execution
  is still pending.
- An independent exhaustive control-flow model over all 100 remembered qualities
  confirms a distinct cancelled draft and detection of erroneous Cancel persistence.
- Independent exact-tree host run: 389 tests, zero skips, 55.167 seconds, exit 0.
  The index and patch hashes were rechecked after testing; the initial freeze
  remains intact. Shell syntax and diff checks pass. No new source blocker found.

Acceptance is limited to this source/mock review. Compilation, installed native
input, all actual screenshot pixels and the 180-second runtime budget remain
unverified. A drag-specific failure is not evidence that every endpoint tap route
is inaccessible. One pre-existing visibility-return line is deliberately hardened;
“every original line unchanged” is no longer an exact statement. All prior
assertions, production source, workflow and deadlines remain preserved. No previous
screenshot or accepted evidence is overwritten or retroactively revalidated.

Primary Android contract:
[View.java](https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-15.0.0_r1/core/java/android/view/View.java)
and [ViewGroup.java](https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-15.0.0_r1/core/java/android/view/ViewGroup.java).
