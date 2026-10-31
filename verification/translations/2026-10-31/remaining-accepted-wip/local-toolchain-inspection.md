# Local compilation prerequisite inspection — 31 October 2026, 07:03 UTC

Inspection for the remaining 739-value WIP candidate, not a compilation attempt or final-main verification.

- Installed Java reports OpenJDK 21.0.12.1, Debian build 21.0.12.1+1-1-deb13u1.
- Repository Gradle wrapper JAR and executable are present. The pinned distribution is Gradle 8.13 with checksum 20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78.
- `ANDROID_HOME`, `ANDROID_SDK_ROOT`, `JAVA_HOME`, and `GRADLE_USER_HOME` are unset.
- No `gradle`, `adb`, `aapt2`, `sdkmanager`, or `kotlinc` executable is on PATH.
- No SDK exists at `/opt/android-sdk`, `/opt/android`, `/usr/local/lib/android/sdk`, or `/home/agent/Android/Sdk`; `/home/agent/.gradle` and `/tmp/codex_deps` are absent.
- A bounded depth-four search of `/tmp`, `/workspace`, `/opt`, `/usr/local` and `/home/agent/.cache` found no Android SDK, build-tools, platform-tools, android-35 or Gradle8.13 distribution directory. Standard `/usr/share`, `/usr/lib` and `/var/cache`/`/var/lib` Android/Gradle paths were absent. The user cache is empty.
- Prior source worktrees contain wrapper inputs and some empty build directories, not a usable SDK/dependency cache.

Thus a bounded local offline compiled-resource/JVM run is not available with the inspected installed inputs. No software installation, permission change, network bypass or shared-cache mutation was attempted. Compilation, the new 739-value JVM test, lint, APK and device checks remain unrun for this WIP; hosted exact-source verification remains necessary after actual final-base synchronization. The provisional source parent remains PR245 initial head0f802aa5. PR245's later candidate aad55c3a (including actual PR246) is known but not asserted merged here.
