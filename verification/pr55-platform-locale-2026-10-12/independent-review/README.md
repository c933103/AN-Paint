# Platform locale binding: independent narrow source review

PASS for source review of tree `dc1ba97dacc573ead73729297eb739ecb244dcf5` over exact current integration tree `b5d8cbeac9bf6d613ed7c3be787aa984826daafd`. No blocking source finding. This is not a fresh Android acceptance result.

Only three paths change: the previously reviewed HANDOFF 81→108 correction; `android:localeConfig="@xml/app_locales"` on the actual application manifest; and a framework configuration check at the start of an existing API33+ installed method. All other 1,091 leaves and executable modes match. Removing the new import/check restores the complete prior installed test bytes, including language switches and return-to-system assertions. No new test identity, timeout, workflow, resource tag, wording, font, layout or pixel guard is introduced.

The new check uses instrumentation.targetContext. It records actual framework status and full expected/actual tags before assertions; requires success, nonnull locales, nonempty and unique current picker tags, equal counts and exact set equality. This rejects missing, extra, duplicated or changed supported tags. Expected values come from current resources, not a hard-coded count. The independent one-time audit also verifies that current picker/XML sequences agree at 167 unique identities.

The [official API reference](https://developer.android.com/reference/android/app/LocaleConfig) confirms the constructor/status APIs start at API33, and `fromContextIgnoringOverride` starts at API34. The runtime SDK branch is correct; API34+ bypasses dynamic overrides and observes application resources. The API33 constructor branch is source-reviewed but is not exercised by the normal API30/API35 matrix. API30 excludes the existing method as before. Framework discovery is separate from actual Settings-screen eligibility/visibility, which is not claimed.

## Evidence and limits

- Reviewer focused checks: 24 passed normally in 7.154s and 24 optimized in 4.976s, both exits 0. These are current resource/scope/deadline contracts.
- Writer receipts independently bound: 27 normal and 27 optimized focused methods pass. Current inventories remain 910 JVM and 95/104 installed executions; no identity was added or removed.
- `check_scope.py` is a portable one-time review check, not a new permanent source-snapshot CI gate. A first reviewer trial used the wrong XML owner path; `reviewer-trial.txt` preserves the correction, which made no application change.
- Local Android compilation, runtime and new APK evidence remain UNRUN. No full aggregate is claimed or required by this narrowly scoped receipt; parent controls proportional hosted execution.

Fresh acceptance requires the compiled application attribute to resolve to the delivered `xml/app_locales`, exact current tags and unchanged resource controls, plus the actual installed API35 method reporting STATUS_SUCCESS and the exact 167-tag set. Preserve full source/run/APK/test-artifact bindings and all original method assertions. No Settings UI observation is implied. The current b0697 artifact checkpoint remains failed for static platform registration despite its passing existing CI, and cannot be relabelled as this successor.

The exact-version cause is archived separately in `anpaint-pr55-localeconfig-diagnosis-20261012`: default AGP8.13.0 → builder8.13.0 → manifest-merger31.13.0 accepts localeConfig only from MAIN/OVERLAY, not LIBRARY. This matches the library-only source and delivered absence; no archived CI merger-decision report was available. The broader corresponding-source bundle will also change its HANDOFF bytes; older APK/source ZIP identity is not transferred to this candidate.
