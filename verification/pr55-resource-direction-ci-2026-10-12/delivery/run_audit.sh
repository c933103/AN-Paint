#!/usr/bin/env bash
# Read-only inputs; write fresh outputs to a caller-selected new directory.
set -euo pipefail
if [[ $# -ne 4 ]]; then
  echo 'Usage: run_audit.sh SOURCE_REPO CI_ARTIFACT_ROOT AAPT2 NEW_OUTPUT_DIRECTORY' >&2
  exit 2
fi
scripts=$(cd -- "$(dirname -- "$0")" && pwd)
repo=$(cd -- "$1" && pwd)
ci=$(cd -- "$2" && pwd)
aapt2=$(realpath -- "$3")
output=$4
mkdir -- "$output"
output=$(cd -- "$output" && pwd)
export PYTHONDONTWRITEBYTECODE=1
mkdir -- "$output/disposable"
export TMPDIR="$output/disposable"
trap 'rmdir -- "$TMPDIR"' EXIT
python3 "$scripts/audit_artifact_bindings.py" --ci-root "$ci" --publication "$scripts/source-publication.json" --output "$output/artifact-bindings-result.json" > "$output/artifact-bindings-check.log"
python3 "$scripts/audit_direction_probes.py" --repo "$repo" --probes "$ci/exact-script" --artifact "$ci/exact-script.zip" --output "$output/probes-result.json" > "$output/probes-check.log"
python3 "$scripts/audit_direction_delivery.py" --repo "$repo" --archive "$ci/apk-and-source.zip" --probes "$ci/exact-script" --output "$output/delivery-result.json" > "$output/delivery-check.log"
python3 "$scripts/audit_build_log.py" --log "$ci/build-job.log" --delivery-result "$output/delivery-result.json" --output "$output/build-log-result.json" > "$output/build-log-check.log"
for scope in direction_compiled_m04 compiled_arabic; do
  name=compiled-m04
  [[ $scope == compiled_arabic ]] && name=compiled-arabic
  python3 "$scripts/audit_${scope}.py" --repo "$repo" --apk "$ci/apk-and-source/app/build/outputs/apk/debug/app-debug.apk" --aapt2 "$aapt2" --delivery-result "$output/delivery-result.json" --output "$output/${name}-result.json" > "$output/${name}-check.log"
done
python3 "$scripts/test_probe_checker.py" --repo "$repo" --ci-root "$ci" -v > "$output/checker-negative-controls.log" 2>&1
python3 -O "$scripts/test_probe_checker.py" --repo "$repo" --ci-root "$ci" -v > "$output/checker-negative-controls-optimized.log" 2>&1
echo "PASS: artifact/build-log bindings, seven probes, current source/font/legal equality, compiled M04/Arabic and checker negative controls. Outputs: $output"
