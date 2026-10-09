#!/usr/bin/env bash
set -euo pipefail

progress() {
  printf '[+%ss] %s\n' "$SECONDS" "$*" | tee -a "$report/startup.log"
}

# All readiness probes share one deadline. A service that is still starting may
# fail or stall briefly after sys.boot_completed; that is not a failed app test.
# Never retry instrumentation or an APK installation through this function.
wait_until_ready() {
  local label="$1" expected="$2" remaining probe status
  shift 2
  phase="$label"
  progress "$phase"
  while true; do
    if ! kill -0 "$emulator_pid" 2>/dev/null; then
      progress "FAILED: emulator exited during $phase" >&2
      return 1
    fi
    remaining=$((readiness_deadline - SECONDS))
    if (( remaining <= 0 )); then
      progress "FAILED: startup deadline reached during $phase" >&2
      return 124
    fi
    probe=10
    if (( remaining < probe )); then probe="$remaining"; fi
    if ready_output=$(timeout --kill-after=1s "${probe}s" "$adb" "$@" 2> "$report/last-probe-error.txt"); then
      ready_output="${ready_output//$'\r'/}"
      if [[ "$ready_output" == $expected ]]; then
        progress "Ready: $phase"
        return 0
      fi
      status=0
    else
      status=$?
    fi
    progress "Waiting: $phase (probe exit $status; $((readiness_deadline - SECONDS))s remain)"
    cat "$report/last-probe-error.txt" >> "$report/startup.log"
    # Keep the shared budget even when the last probe used its remaining time.
    if (( SECONDS < readiness_deadline )); then sleep 1; fi
  done
}

# This boundary is API35-only. Every command is bounded and every unexpected
# response fails; an absent process is never mistaken for an ADB transport error.
credit_restart_command() {
  local label="$1" seconds="$2" status
  shift 2
  printf '[+%ss] %s (maximum %ss)\n' "$SECONDS" "$label" "$seconds" >> "$boundary_log"
  if boundary_output=$(timeout --kill-after=1s "${seconds}s" "$adb" "$@" 2>&1); then status=0; else status=$?; fi
  printf '%s\nexit=%s\n' "$boundary_output" "$status" >> "$boundary_log"
  return "$status"
}

credit_restart_pid() {
  credit_restart_command 'Read app PID with explicit absence protocol' 10 shell \
    'p=$(pidof paint.anpaint.android); s=$?; if [ "$s" = 0 ]; then printf "alive:%s\n" "$p"; elif [ "$s" = 1 ]; then echo absent; else exit "$s"; fi' || return
  boundary_output="${boundary_output//$'\r'/}"
  if [[ "$boundary_output" == absent || "$boundary_output" =~ ^alive:[1-9][0-9]*$ ]]; then return 0; fi
  printf 'FAILED: malformed PID response\n' >> "$boundary_log"
  return 1
}

run_credit_restart_regression() {
  local seed_class=paint.anpaint.android.AcceptedCreditRestartSeedTest
  local verify_class=paint.anpaint.android.AcceptedCreditRestartVerifyTest
  local phase_root="$report/app/accepted-credit-restart" classes owner seed_pid
  local -a seed_exclude=(--exclude-class "$verify_class") verify_exclude=(--exclude-class "$seed_class")
  rm -rf "$phase_root/seed" "$phase_root/verify"
  mkdir -p "$phase_root"
  boundary_log="$phase_root/boundary.log"
  : > "$boundary_log"
  # Initialize before doing anything: a failed seed/boundary never inherits a
  # stale successful verify summary from an earlier invocation.
  printf 'NOT RUN: seed and external live-process boundary have not passed\n' > "$phase_root/verify-status.txt"
  rm -f "$phase_root/coverage.json" "$phase_root/seed/summary.json" "$phase_root/verify/summary.json"
  classes=$(python3 - <<'INVENTORY'
import sys
from pathlib import Path
sys.path.insert(0, 'tools')
from run_android_instrumentation import declared_tests, restart_partition
ordinary, _, _ = restart_partition(declared_tests(Path('app/src/androidTest')))
print('\n'.join(sorted({owner for owner, _ in ordinary})))
INVENTORY
  ) || return
  while IFS= read -r owner; do
    seed_exclude+=(--exclude-class "$owner")
    verify_exclude+=(--exclude-class "$owner")
  done <<< "$classes"
  phase='Accepted-credit restart: bootstrap live app'
  progress "$phase"
  credit_restart_command 'Start ordinary launcher' 30 shell am start -W -n \
    paint.anpaint.android/org.catrobat.paintroid.classic.ClassicPaintActivity || return
  credit_restart_pid || return
  [[ "$boundary_output" =~ ^alive:[1-9][0-9]*$ ]] || { echo 'FAILED: no live seed process' >> "$boundary_log"; return 1; }
  seed_pid="${boundary_output#alive:}"
  phase='Accepted-credit restart: complete seed without activity cleanup'
  progress "$phase"
  python3 tools/run_android_instrumentation.py --adb "$adb" \
    --apk "build/prebuilt/app/build/outputs/apk/androidTest/$variant/app-$variant-androidTest.apk" \
    --component paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner \
    --source-tests app/src/androidTest --output "$phase_root/seed" \
    --suite app-credit-restart-seed --timeout-seconds 60 --leave-target-running "${seed_exclude[@]}" || return
  # Do not trust exit=0 alone, including a wrapper accidentally changed later.
  python3 - "$phase_root/seed/summary.json" "$seed_pid" <<'SEED_REPORT' || return
import json, sys
from runpy import run_path
runner = run_path('tools/run_android_instrumentation.py')
report = json.load(open(sys.argv[1]))
seed = runner['restart_partition'](runner['declared_tests'](runner['Path']('app/src/androidTest')))[1]
actual = [(c['classname'], c['name']) for c in report['cases'] if c['status'] == 'passed']
if (report.get('success') is not True or report.get('leave_target_running') is not True
        or report.get('target_pid_before_instrumentation') != int(sys.argv[2])
        or report.get('expected_tests') != 1 or report.get('completed_tests') != 1
        or len(report['cases']) != 1 or len(actual) != 1 or set(actual) != seed):
    raise SystemExit('Seed report does not prove complete success in the original live process')
SEED_REPORT
  printf '[+%ss] Complete successful seed report verified; PID=%s\n' "$SECONDS" "$seed_pid" >> "$boundary_log"
  credit_restart_pid || return
  [[ "$boundary_output" == "alive:$seed_pid" ]] || { echo 'FAILED: seed process changed or died before force-stop' >> "$boundary_log"; return 1; }
  credit_restart_command 'Gallery must still be the resumed activity' 10 shell dumpsys activity activities || return
  grep -Eq '(topResumedActivity|mResumedActivity).*paint\.anpaint\.android/org\.catrobat\.paintroid\.classic\.MediaGalleryActivity' <<< "$boundary_output" || {
    echo 'FAILED: Gallery is no longer resumed' >> "$boundary_log"; return 1;
  }
  # Check again after dumpsys: only a currently live original PID may be killed.
  credit_restart_pid || return
  [[ "$boundary_output" == "alive:$seed_pid" ]] || { echo 'FAILED: seed process vanished before force-stop' >> "$boundary_log"; return 1; }
  phase='Accepted-credit restart: external force-stop of live seed'
  progress "$phase"
  credit_restart_command "Force-stop verified live PID $seed_pid" 10 shell am force-stop paint.anpaint.android || return
  credit_restart_pid || return
  [[ "$boundary_output" == absent ]] || { echo 'FAILED: process remains after force-stop' >> "$boundary_log"; return 1; }
  printf '[+%ss] Verified target PID absent before normal verify instrumentation\n' "$SECONDS" >> "$boundary_log"
  phase='Accepted-credit restart: fresh-process verification'
  progress "$phase"
  printf 'RUNNING: complete seed and external live-process boundary passed\n' > "$phase_root/verify-status.txt"
  if ! python3 tools/run_android_instrumentation.py --adb "$adb" \
    --apk "build/prebuilt/app/build/outputs/apk/androidTest/$variant/app-$variant-androidTest.apk" \
    --component paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner \
    --source-tests app/src/androidTest --output "$phase_root/verify" \
    --suite app-credit-restart-verify --timeout-seconds 60 "${verify_exclude[@]}"; then
    printf 'FAILED: see verify summary and raw instrumentation log\n' > "$phase_root/verify-status.txt"
    return 1
  fi
  printf 'COMPLETED: see strict verify summary\n' > "$phase_root/verify-status.txt"
  python3 - "$report/app/androidTest-results/summary.json" "$phase_root" <<'COVERAGE'
import json, sys
from pathlib import Path
sys.path.insert(0, 'tools')
from run_android_instrumentation import declared_tests, verify_restart_reports
root = Path(sys.argv[2])
reports = [json.loads(path.read_text()) for path in
           (Path(sys.argv[1]), root/'seed/summary.json', root/'verify/summary.json')]
coverage = verify_restart_reports(declared_tests(Path('app/src/androidTest')), reports)
(root/'coverage.json').write_text(json.dumps(coverage, indent=2)+'\n')
COVERAGE
}

cleanup() {
  local status=$?
  trap - ERR
  set +e
  progress "Collecting logs and stopping emulator (result $status, phase: $phase)"
  timeout --kill-after=3s 10s "$adb" logcat -d > "$report/logcat.txt" 2>&1
  timeout --kill-after=3s 10s "$adb" emu kill
  if test -n "$emulator_pid"; then
    kill "$emulator_pid" 2>/dev/null
    for attempt in $(seq 1 10); do
      kill -0 "$emulator_pid" 2>/dev/null || break
      sleep 1
    done
    kill -KILL "$emulator_pid" 2>/dev/null || true
  fi
}

main() {
  : "${TEST_API:?Set TEST_API to 30 or 35}"
  case "$TEST_API" in 30|35) ;; *) exit 2;; esac
  variant="${BUILD_VARIANT:-debug}"
  case "$variant" in debug|release) ;; *) exit 2;; esac
  export ANDROID_SERIAL=emulator-5554
  adb="$ANDROID_HOME/platform-tools/adb"
  report="build/reports/android-api-$TEST_API"
  mkdir -p "$report"
  emulator_pid=''
  phase='Create virtual device'
  trap cleanup EXIT
  trap 'progress "Interrupted during $phase"; exit 124' TERM INT
  trap 'status=$?; progress "FAILED: $phase (exit $status): $BASH_COMMAND" >&2; exit "$status"' ERR
  progress "$phase"
  timeout --kill-after=5s 30s "$ANDROID_HOME/cmdline-tools/latest/bin/avdmanager" create avd \
    --force --name "codec$TEST_API" --package "system-images;android-$TEST_API;google_apis;x86_64" <<< no
  phase='Launch emulator'
  progress "$phase"
  "$ANDROID_HOME/emulator/emulator" -avd "codec$TEST_API" -port 5554 \
    -no-window -no-audio -no-boot-anim -no-snapshot -no-metrics -gpu swiftshader_indirect \
    -memory 2048 -cores 2 > "$report/emulator.log" 2>&1 &
  emulator_pid=$!
  phase='Discover ADB device (60s maximum)'
  progress "$phase"
  timeout --kill-after=5s 60s "$adb" wait-for-device
  readiness_deadline=$((SECONDS + 120))
  wait_until_ready 'Android boot' 1 shell getprop sys.boot_completed
  wait_until_ready 'Verify Android API' '*' shell getprop ro.build.version.sdk
  if [[ "$ready_output" != "$TEST_API" ]]; then
    progress "FAILED: expected API $TEST_API, received $ready_output" >&2
    exit 1
  fi
  wait_until_ready 'Package manager' 'package:*' shell cmd package path android
  for setting in window_animation_scale transition_animation_scale animator_duration_scale; do
    wait_until_ready "Disable $setting" '*' shell settings put global "$setting" 0
  done
  # A synthetic MENU key can wait for a launcher window that has not appeared
  # yet, triggering an input-dispatch ANR during first boot. Dismiss directly.
  wait_until_ready 'Dismiss keyguard' '*' shell wm dismiss-keyguard
  phase='Install main APK (60s maximum)'
  progress "$phase"
  timeout --kill-after=5s 60s "$adb" install -r -t "build/prebuilt/app/build/outputs/apk/$variant/app-$variant.apk"
  failed=0
  extra=()
  if test "$TEST_API" = 30; then
    extra+=(--exclude-class org.catrobat.paintroid.classic.UltraHdrImportTest)
  fi
  phase='Native/import instrumentation'
  progress "$phase"
  python3 tools/run_android_instrumentation.py --adb "$adb" \
    --apk "build/prebuilt/Paintroid/build/outputs/apk/androidTest/$variant/Paintroid-$variant-androidTest.apk" \
    --component org.catrobat.paintroid.test/androidx.test.runner.AndroidJUnitRunner \
    --source-tests Paintroid/src/androidTest --output "$report/Paintroid/androidTest-results" \
    --suite Paintroid --timeout-seconds 180 "${extra[@]}" || failed=1
  rm -rf "$report/app/accepted-credit-restart"
  editor_failed=0
  phase='Editor instrumentation'
  progress "$phase"
  python3 tools/run_android_instrumentation.py --adb "$adb" \
    --apk "build/prebuilt/app/build/outputs/apk/androidTest/$variant/app-$variant-androidTest.apk" \
    --component paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner \
    --source-tests app/src/androidTest --output "$report/app/androidTest-results" \
    --suite app --timeout-seconds 180 \
    --exclude-class paint.anpaint.android.AcceptedCreditRestartSeedTest \
    --exclude-class paint.anpaint.android.AcceptedCreditRestartVerifyTest || editor_failed=1
  if (( editor_failed )); then failed=1; fi
  if test "$TEST_API" = 35; then
    if (( editor_failed )); then
      mkdir -p "$report/app/accepted-credit-restart"
      printf 'NOT RUN: ordinary editor suite failed\n' > "$report/app/accepted-credit-restart/verify-status.txt"
    else
      run_credit_restart_regression || failed=1
    fi
  else
    mkdir -p "$report/app/accepted-credit-restart"
    printf 'NOT RUN: accepted-credit abrupt-process-stop regression is API35-only; both phase classes excluded on API30\n' \
      > "$report/app/accepted-credit-restart/verify-status.txt"
  fi
  phase='Instrumentation complete'
  progress "$phase (result $failed)"
  exit "$failed"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then main "$@"; fi
