# Current-base translation handling: local and resource evidence

Source head: `3ff637e64b8d8931f20186fd159e75d118232e8b`  
Source tree: `c962e24433181f4006d1356c922f54b3bf207daa`  
CI merge checkout: `8f4875ee53cd9d58d79d3a99c5d74ac89e6ef554`, with the same tree.

## Passed

- Normal and optimized final-tree host aggregates: 1,098 tests each, 221.242 and 223.296 seconds.
- Actual Kotlin formatter/prefix suite: 15 tests.
- Fresh AAPT catalogue comparison: 52,063 rows / 145 configurations / 723 canonical entries; 104,126 typed/literal and 20,744 present-null comparisons, zero mismatches or Formatter exceptions.
- Source generator: 9 tests, including companion-file add/change/remove, duplicates, aliases/plurals/overlays and per-file/entry-local namespace scopes. AAPT accepts the generated valid XLIFF fixture.
- Hosted clean/incremental resource generation: all 13 probes, including companion addition/removal and expected rejection of a reserved ID in an application English/debug overlay.
- Exact-head security review: completed without findings. Code review and remaining CI were pending at this snapshot.

The only resource-file change versus develop9a7a052d is Japanese crop percent encoding. Current numeric display locale, expanded Czech/Swedish resources, all 18 Ainu/Manchu percent templates, merged vertical feedback and current CI budgets are preserved.

## Evidence and remaining work

[Archive](local-and-resource-evidence.zip) includes actual logs, hosted resource receipt, review-state snapshot, compact source identities, original/generated XLIFF input, comparison scripts and intermediate hashes. See verification-notes.md inside for precise scope and reproduction inputs. Large reproducible APK/resource-table/TSV intermediates are not duplicated here.

Initial failed and superseded test outputs remain retained and labelled, not converted into passes. Full JVM/native tests, lint, APK/source binding and API35 results must still pass on this exact tree. No merge or release is claimed.

[PR114](https://github.com/c933103/AN-Paint/pull/114) · [CI run39538234683](https://github.com/c933103/AN-Paint/actions/runs/39538234683)

Archive SHA-256: `97e3d13f40970bdf0e7e1cfc8a53181feb145fdd952510af5b8aecad06814bba`.
