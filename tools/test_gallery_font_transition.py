"""Ordering model of the cited AOSP protocol, not an Android test or causal proof."""
from collections import deque
import unittest
from pathlib import Path
import json
import re
import subprocess

class Framework:
    def __init__(self, initial=2):
        self.setting = self.system = self.target = initial
        self.display_queue = deque()
    def shell_write(self, value):
        self.setting = value
        self.display_queue.append(self.observe_setting)
    def observe_setting(self):
        value = self.setting
        if value != self.system:
            self.system = value
            # ATMS queues persistent snapshot write-back before app delivery.
            self.display_queue.append(lambda: self.persist_snapshot(value))
            self.target = value
    def persist_snapshot(self, value):
        self.setting = value
        self.display_queue.append(self.observe_setting)
    def next_message(self):
        self.display_queue.popleft()()
    def flush_barrier(self):
        barrier = object()
        self.display_queue.append(barrier)
        while self.display_queue:
            message = self.display_queue.popleft()
            if message is barrier:
                return
            message()
    def matches(self, value):
        return self.setting == self.system == self.target == value
    def drain(self):
        while self.display_queue:
            self.next_message()

class FontTransitionOrderingTest(unittest.TestCase):
    def test_old_three_way_agreement_can_overtake_pending_writeback(self):
        f = Framework()
        f.shell_write(1)
        f.next_message()
        self.assertTrue(f.matches(1))
        f.shell_write(2)
        f.drain()
        self.assertTrue(f.matches(1))
        self.assertFalse(f.matches(2))
    def test_barrier_between_transitions_prevents_that_exact_interleaving(self):
        f = Framework()
        f.shell_write(1)
        f.next_message()
        self.assertTrue(f.matches(1))
        f.flush_barrier()
        self.assertTrue(f.matches(1))
        f.shell_write(2)
        # The earlier no-op observer may remain behind the first barrier.
        while not f.matches(2):
            f.next_message()
        f.flush_barrier()
        self.assertTrue(f.matches(2))
        f.drain()
        self.assertTrue(f.matches(2))

SOURCE = (Path(__file__).resolve().parents[1] / 'app/src/androidTest/java/paint/anpaint/android/GalleryViewportDeviceTest.kt').read_text()

class FontShellProtocolTest(unittest.TestCase):
    def script(self, command, seconds):
        encoded = re.search(r'it.write\("(timeout -s KILL .*?)"\)', SOURCE).group(1)
        # Decode the actual Kotlin string's common escapes; substitute only the
        # fixture's three explicit interpolations, not an independently copied script.
        return json.loads('"' + encoded + '"').replace("${'$'}", '$').replace('${seconds}', seconds).replace('$command', command)

    def run_script(self, command, seconds='0.500'):
        return subprocess.run(['sh'], input=self.script(command, seconds), text=True,
                              capture_output=True, timeout=2)

    def test_stdin_script_preserves_command_output_stderr_and_exit_status(self):
        for code in [0, 7]:
            with self.subTest(code=code):
                result = self.run_script(f"sh -c 'echo stdout; echo stderr >&2; exit {code}'")
                self.assertIn('stdout\n', result.stdout)
                self.assertIn('stderr\n', result.stderr)
                self.assertEqual(re.findall(r'^ANPAINT_FONT_EXIT=(\d+)$', result.stdout, re.M), [str(code)])

    def test_decimal_kill_timeout_cannot_be_reported_as_success(self):
        result = self.run_script('sleep 1', '0.010')
        self.assertEqual(re.findall(r'^ANPAINT_FONT_EXIT=(\d+)$', result.stdout, re.M), ['137'])

    def test_one_absolute_deadline_and_both_real_font_transitions_remain(self):
        transition = SOURCE.split('private fun setFontScale(scale: Float)', 1)[1].split('private var fontShellVerified', 1)[0]
        self.assertEqual(transition.count('SystemClock.uptimeMillis()+10000'), 1)
        self.assertIn('awaitUntil("real system font scale $scale",deadline,::matches)', transition)
        self.assertIn('fontShell("settings put system font_scale $scale",deadline)', transition)
        self.assertIn('fontShell("am wait-for-broadcast-barrier --flush-broadcast-loopers",deadline)', transition)
        self.assertIn('setFontScale(1f);setFontScale(2f)', SOURCE)
        self.assertIn('after the barrier",matches())', transition)
        self.assertNotIn('while(', transition)

    def test_public_pipe_api_is_gated_and_older_path_is_not_called_equivalent(self):
        self.assertIn('if(Build.VERSION.SDK_INT>=34)', SOURCE)
        self.assertIn('@androidx.annotation.RequiresApi(34)', SOURCE)
        self.assertIn('executeShellCommandRwe("sh")', SOURCE)
        self.assertIn('legacy synchronization only', SOURCE)
        self.assertIn('API30-33 do not expose the system-looper flush command', SOURCE)
        self.assertNotIn('wait-for-broadcast-idle', SOURCE)
        self.assertIn('output.get(remainingTime(),TimeUnit.MILLISECONDS)', SOURCE)
        self.assertIn('error.get(remainingTime(),TimeUnit.MILLISECONDS)', SOURCE)
        self.assertIn('readers.shutdownNow()', SOURCE)

if __name__ == '__main__':
    unittest.main(verbosity=2)
