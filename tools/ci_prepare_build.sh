#!/usr/bin/env bash
# Prepare dependencies and sources; the build workflow separately manages ccache.
# Never restore compiled app classes, APKs or CMake build directories.
set -euo pipefail
export JAVA_HOME="$JAVA_HOME_17_X64"
export PATH="$JAVA_HOME/bin:$PATH"
echo "JAVA_HOME=$JAVA_HOME" >> "$GITHUB_ENV"
echo "$JAVA_HOME/bin" >> "$GITHUB_PATH"
timeout --kill-after=15s 5m "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" \
  'platforms;android-35' 'build-tools;35.0.0' 'ndk;27.2.12479018' 'cmake;3.22.1'
chmod +x gradlew
./gradlew --no-daemon --max-workers=2 --console=plain :app:writeDependencyInventory
python3 tools/generate_native_runtime_notices.py --ndk "$ANDROID_HOME/ndk/27.2.12479018"
python3 tools/generate_legal_notices.py
mkdir -p verification-tools/lib64
cp "$ANDROID_HOME/build-tools/35.0.0/lib/apksigner.jar" verification-tools/
cp "$ANDROID_HOME/build-tools/35.0.0/zipalign" verification-tools/
cp "$ANDROID_HOME/build-tools/35.0.0/aapt2" verification-tools/
cp "$ANDROID_HOME/build-tools/35.0.0/lib64/libc++.so" verification-tools/lib64/
