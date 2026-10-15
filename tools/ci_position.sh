#!/usr/bin/env bash
# Sourced only by the separate position job after ci_emulator.sh startup/install.
run_position_regression() {
  local position_class=paint.anpaint.android.AssemblyPositionDeviceTest failed=0
  rm -rf "$report/app-position"
  phase='Position dialog: Ainu Kana/Latin + Manchu'
  progress "$phase"
  python3 tools/run_android_instrumentation.py --adb "$adb" \
    --apk "build/prebuilt/app/build/outputs/apk/androidTest/$variant/app-$variant-androidTest.apk" \
    --component paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner \
    --source-tests app/src/androidTest --output "$report/app-position/ainu-manchu/androidTest-results" \
    --suite app-position-ainu-manchu --timeout-seconds 180 \
    --include-test "$position_class#ainuKanaPositionTextAndNativeEditing" \
    --include-test "$position_class#ainuLatinPositionTextAndNativeEditing" \
    --include-test "$position_class#manchuPositionColumnsAndNativeEditing" || failed=1
  phase='Position dialog: Tibetan/Dzongkha + Jeju + Nôm'
  progress "$phase"
  python3 tools/run_android_instrumentation.py --adb "$adb" \
    --apk "build/prebuilt/app/build/outputs/apk/androidTest/$variant/app-$variant-androidTest.apk" \
    --component paint.anpaint.android.test/androidx.test.runner.AndroidJUnitRunner \
    --source-tests app/src/androidTest --output "$report/app-position/tibetan-jeju-nom/androidTest-results" \
    --suite app-position-tibetan-jeju-nom --timeout-seconds 180 \
    --include-test "$position_class#tibetanPositionTextAndNativeEditing" \
    --include-test "$position_class#dzongkhaPositionTextAndNativeEditing" \
    --include-test "$position_class#jejuPositionTextAndNativeEditing" \
    --include-test "$position_class#nomPositionTextAndNativeEditing" || failed=1
  python3 tools/app_instrumentation_matrix.py --source-tests app/src/androidTest \
    --sdk "$TEST_API" --root "$report" --group position || failed=1
  return "$failed"
}
