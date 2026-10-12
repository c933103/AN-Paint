#!/usr/bin/env bash
# Reads all inputs; writes only a new audit output directory and disposable controls.
set -euo pipefail
if [[ $# -ne 6 ]]; then
 echo 'Usage: run_audit.sh SOURCE_REPO CI_ROOT EXECUTABLE_AAPT2 HISTORICAL_REVIEW AUTHORING_REVIEW NEW_OUTPUT_DIRECTORY' >&2
 exit 2
fi
scripts=$(cd -- "$(dirname -- "$0")" && pwd)
repo=$(cd -- "$1" && pwd); ci=$(cd -- "$2" && pwd); aapt2=$(realpath -- "$3")
historical=$(cd -- "$4" && pwd); authoring=$(cd -- "$5" && pwd)
mkdir -- "$6"; output=$(cd -- "$6" && pwd)
export PYTHONDONTWRITEBYTECODE=1
mkdir -- "$output/disposable"; export TMPDIR="$output/disposable"
trap 'rmdir -- "$TMPDIR"' EXIT
python3 "$scripts/audit_source_context.py" --repo "$repo" --historical-review "$historical" --authoring-review "$authoring" --output-directory "$output" >"$output/source-preflight.log"
python3 "$scripts/audit_artifact_bindings.py" --ci-root "$ci" --publication "$scripts/source-publication.json" --output "$output/artifact-bindings-result.json" >"$output/artifact-bindings-check.log"
python3 "$scripts/audit_direction_probes.py" --repo "$repo" --probes "$ci/exact-script" --artifact "$ci/exact-script.zip" --output "$output/probes-result.json" >"$output/probes-check.log"
python3 "$scripts/audit_direction_delivery.py" --repo "$repo" --archive "$ci/apk-and-source.zip" --probes "$ci/exact-script" --output "$output/delivery-result.json" >"$output/delivery-check.log"
python3 "$scripts/audit_build_log.py" --log "$ci/build-job.log" --delivery-result "$output/delivery-result.json" --output "$output/build-log-result.json" >"$output/build-log-check.log"
for scope in direction_compiled_m04 compiled_arabic compiled_picker; do
 name=compiled-m04; [[ $scope == compiled_arabic ]] && name=compiled-arabic; [[ $scope == compiled_picker ]] && name=compiled-picker
 python3 "$scripts/audit_${scope}.py" --repo "$repo" --apk "$ci/apk-and-source/app/build/outputs/apk/debug/app-debug.apk" --aapt2 "$aapt2" --delivery-result "$output/delivery-result.json" --output "$output/${name}-result.json" >"$output/${name}-check.log"
done
python3 "$scripts/audit_delivery_comparison.py" --historical-review "$historical" --current-review "$output" >"$output/historical-comparison-check.log"
for optimize in '' '-O'; do
 suffix=''; [[ -n $optimize ]] && suffix='-optimized'
 python3 $optimize "$scripts/test_probe_checker.py" --repo "$repo" --ci-root "$ci" -v >"$output/probe-checker-controls${suffix}.log" 2>&1
 python3 $optimize "$scripts/test_compiled_picker_checker.py" -v >"$output/picker-checker-controls${suffix}.log" 2>&1
 python3 $optimize "$scripts/test_platform_binding_checker.py" --evidence-directory "$output" -v >"$output/platform-binding-controls${suffix}.log" 2>&1
 python3 $optimize "$scripts/test_typography_bindings.py" --ci-root "$ci" --report "$output" -v >"$output/typography-binding-controls${suffix}.log" 2>&1
done
python3 "$scripts/audit_evidence_screen.py" --ci-root "$ci" --packet "$output"
echo 'PASS: current typography source/delivery/probes/build/compiled resources and all checker controls. No new Gradle/Android execution or installed acceptance.'
