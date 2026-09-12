#!/usr/bin/env bash
set -euo pipefail
: "${TEST_API:?Set TEST_API to 30 or 35}"
case "$TEST_API" in 30|35) ;; *) exit 2;; esac
export ANDROID_SERIAL=emulator-5554
adb="$ANDROID_HOME/platform-tools/adb"
report="build/reports/android-api-$TEST_API"
mkdir -p "$report"
emulator_pid=''
cleanup() {
  set +e
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
trap cleanup EXIT
trap 'exit 124' TERM INT
timeout --kill-after=5s 30s "$ANDROID_HOME/cmdline-tools/latest/bin/avdmanager" create avd \
  --force --name "codec$TEST_API" --package "system-images;android-$TEST_API;google_apis;x86_64" <<< no
"$ANDROID_HOME/emulator/emulator" -avd "codec$TEST_API" -port 5554 \
  -no-window -no-audio -no-boot-anim -no-snapshot -gpu swiftshader_indirect \
  -memory 2048 -cores 2 > "$report/emulator.log" 2>&1 &
emulator_pid=$!
timeout --kill-after=5s 60s "$adb" wait-for-device
deadline=$((SECONDS + 120))
until test "$(timeout 10s "$adb" shell getprop sys.boot_completed | tr -d '\r')" = 1; do
  if (( SECONDS >= deadline )); then echo 'Emulator boot timed out' >&2; exit 124; fi
  kill -0 "$emulator_pid"
  sleep 2
done
test "$(timeout 10s "$adb" shell getprop ro.build.version.sdk | tr -d '\r')" = "$TEST_API"
for setting in window_animation_scale transition_animation_scale animator_duration_scale; do
  timeout 10s "$adb" shell settings put global "$setting" 0
done
timeout 10s "$adb" shell input keyevent 82
timeout --kill-after=5s 60s "$adb" install -r -t build/prebuilt/app/build/outputs/apk/debug/app-debug.apk
failed=0
extra=()
if test "$TEST_API" = 30; then
  extra+=(--exclude-class org.catrobat.paintroid.classic.UltraHdrImportTest)
fi
python3 tools/run_android_instrumentation.py --adb "$adb" \
  --apk build/prebuilt/Paintroid/build/outputs/apk/androidTest/debug/Paintroid-debug-androidTest.apk \
  --component org.catrobat.paintroid.test/androidx.test.runner.AndroidJUnitRunner \
  --source-tests Paintroid/src/androidTest --output "$report/Paintroid/androidTest-results" \
  --suite Paintroid --timeout-seconds 180 "${extra[@]}" || failed=1
python3 tools/run_android_instrumentation.py --adb "$adb" \
  --apk build/prebuilt/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk \
  --component io.github.c933103.anpaint.test/androidx.test.runner.AndroidJUnitRunner \
  --source-tests app/src/androidTest --output "$report/app/androidTest-results" \
  --suite app --timeout-seconds 180 || failed=1
exit "$failed"
