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
  timeout --kill-after=5s 60s "$adb" install -r -t build/prebuilt/app/build/outputs/apk/debug/app-debug.apk
  failed=0
  extra=()
  if test "$TEST_API" = 30; then
    extra+=(--exclude-class org.catrobat.paintroid.classic.UltraHdrImportTest)
  fi
  phase='Native/import instrumentation'
  progress "$phase"
  python3 tools/run_android_instrumentation.py --adb "$adb" \
    --apk build/prebuilt/Paintroid/build/outputs/apk/androidTest/debug/Paintroid-debug-androidTest.apk \
    --component org.catrobat.paintroid.test/androidx.test.runner.AndroidJUnitRunner \
    --source-tests Paintroid/src/androidTest --output "$report/Paintroid/androidTest-results" \
    --suite Paintroid --timeout-seconds 180 "${extra[@]}" || failed=1
  phase='Editor instrumentation'
  progress "$phase"
  python3 tools/run_android_instrumentation.py --adb "$adb" \
    --apk build/prebuilt/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk \
    --component paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner \
    --source-tests app/src/androidTest --output "$report/app/androidTest-results" \
    --suite app --timeout-seconds 180 || failed=1
  phase='Instrumentation complete'
  progress "$phase (result $failed)"
  exit "$failed"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then main "$@"; fi
