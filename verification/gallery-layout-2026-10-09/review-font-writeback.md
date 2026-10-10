# System font transition: queued persistent write-back

## What failed, and what remains a hypothesis

Combined head `c48f68b95360f87e21ccd4c59b995f25ee5d2462` is the verified pure
union with accepted PR31. Its [first CI run](https://github.com/c933103/AN-Paint/actions/runs/37946657315)
passed 716 JVM checks and zero-issue lint. Installed library 74 and ordinary 17
passed, while the gallery viewport test failed before launching Mongolian.
Both restart tests were never run. The ordinary runner did not time out.

French real 2× portrait/landscape browser, wrapping and IME checks passed. ATMS
then logged fontScale 1 at 15:00:16.849; persisted/system/target all read 1 at 16.917;
the next 2× request began 16.918. No later ATMS 2× event appears, and all three
values remained 1 at 27.005. Prior 03abccd had the same sequence followed by an
ATMS 2× event 54ms after its second write. This excludes an isolated stale app
resource explanation. It does not distinguish a failed shell write from an
asynchronous overwrite: the former fixture discarded shell output/status.

[Original failure receipt and constituent hashes](https://github.com/c933103/AN-Paint/tree/81b4e15e83a21740cdd8463c264fcf05658bdc42/verification/gallery-layout-captures-2026-10-09/combined-ci-c48f68b)
remain separate from later acceptance. No blind rerun or production change is
used to label that failure harmless.

## Confirmed framework ordering

In AOSP Android 15 r1:

- [ActivityTaskManagerService](https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/services/core/java/com/android/server/wm/ActivityTaskManagerService.java#818)
  observes the setting on mH (818–832), reads the setting and applies a persistent
  configuration (4915–4931), queues a snapshot write-back before distributing
  app configurations (4694–4707), and later invokes putConfigurationForUser
  (4868–4870).
- [Settings.putConfigurationForUser](https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/core/java/android/provider/Settings.java#4674)
  writes FONT_SCALE again (4674–4679). App-side setting/resource agreement can
  therefore precede the queued old-value write-back.
- [ActivityManagerService](https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/services/core/java/com/android/server/am/ActivityManagerService.java#2621)
  initializes ATMS with DisplayThread (2621–2623). The failed emulator log
  explicitly registered android.display with BroadcastLoopers.
- The [AMS barrier](https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/services/core/java/com/android/server/am/ActivityManagerService.java#20168)
  flushes registered system loopers before the broadcast queue (20168–20177).
  [BroadcastLoopers.waitForBarrier](https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/services/core/java/com/android/server/am/BroadcastLoopers.java#95)
  posts a latch behind already-queued messages (95–101), covering the pending
  DisplayThread write-back rather than merely waiting for app idle.
- [The shell command](https://android.googlesource.com/platform/frameworks/base/+/android-15.0.0_r1/services/core/java/com/android/server/am/ActivityManagerShellCommand.java#3597)
  exposes wait-for-broadcast-barrier with --flush-broadcast-loopers (3597–3613).

These facts support a stale 1× write-back as an explanation for this run; they
are not a historical trace proving which writer changed its setting.

## Bounded API 34+ correction

Each setFontScale call owns one absolute ten-second deadline from entry. It:

1. Performs exactly one real settings write and captures stdout, stderr and
   the command's explicit exit status. A shell error fails the fixture.
2. Waits for the persisted setting and actual system/target configurations.
3. Flushes queued system-loop work using the supported barrier, with only the
   deadline's remaining time available.
4. Requires successful completion, app idle, and three-way agreement again
   before returning. Another font transition cannot overtake queued write-back.

No automatic setting retry, synthetic Resources override, smaller-text change,
removed locale/rotation case or increased deadline is introduced. Existing real
2× browser reserve, wrapped editable query, Search EditorInfo, same-Activity
rotation and exact cleanup checks remain. Application sources are unchanged.

The public [UiAutomation API](https://developer.android.com/reference/android/app/UiAutomation#executeShellCommandRwe(java.lang.String))
provides separate stdin/stdout/stderr pipes from API 34. The fixture executes sh
and feeds script bytes to stdin, rather than assuming Runtime.exec(String)
understands shell quotes. Two concurrent readers use the same remaining deadline;
all descriptors close and the executor shuts down on failure. Killing the command
client does not cancel a system-server Binder operation already underway, so
the readers independently enforce the same remaining deadline.

[Android 15 toybox timeout](https://android.googlesource.com/platform/external/toybox/+/android-15.0.0_r1/toys/other/timeout.c)
accepts decimal seconds; SIGKILL timeout returns 137 and kills the command's process
group, while the enclosing shell remains able to report status (51–53,79–88,
105–108). The fixture probes the actual emulator's decimal/KILL behavior once
before relying on it. Unsupported utilities, commands, missing status or timeout
are failures, never silent fallbacks. The probe consumes the first transition's
same ten-second budget.

## Compatibility and regression limits

API 30–33 lack the flush option. [API 30's command implementation](https://android.googlesource.com/platform/frameworks/base/+/android-11.0.0_r1/services/core/java/com/android/server/am/ActivityManagerShellCommand.java)
and [queue-only idle implementation](https://android.googlesource.com/platform/frameworks/base/+/android-11.0.0_r1/services/core/java/com/android/server/am/ActivityManagerService.java#19911)
are not equivalent DisplayThread barriers. That older path keeps its real-setting
and three-resource checks, emits an explicit legacy-synchronization diagnostic,
and has weaker synchronization that this correction does not verify or claim
to fix. No hidden API or pretend flush is used.

`tools/test_gallery_font_transition.py` models the cited queue ordering: the old
three-way check permits the lost-write interleaving; the barrier prevents that
same interleaving. This is a deterministic sensitivity model, not an Android
execution or proof of the historical writer. Additional tests execute the
actual Kotlin stdin-script literal on the host to preserve stdout/stderr/nonzero
status and decimal hard timeout, and guard deadline/real-transition/API gating.
The actual Android utility and real layout still require the fresh installed CI.

Local verification: all 342 Python checks passed in 52.717s with zero skips;
the six focused protocol/model checks also passed after the final diagnostic
logging adjustment. Android compilation and real target execution remain CI
requirements, not inferred from these host results.
