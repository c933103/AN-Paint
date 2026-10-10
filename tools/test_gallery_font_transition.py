"""AOSP queue-ordering models, not Android tests or causal proof.

The display-ack argument assumes normal FIFO delivery with no intervening
synchronization barrier. DMS messages are async, unlike ordinary ATMS messages;
the counterexample below explicitly models their ability to bypass a barrier.
"""
from collections import deque
import unittest
from pathlib import Path
import json
import re
import subprocess

class Framework:
    """Normal FIFO model; no MessageQueue synchronization barrier is present."""
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
    def queue_display_ack(self, event, display_id, delivered):
        # Sharing DisplayThread is not enough when a sync barrier is present.
        callback = lambda: delivered.add((event, display_id))
        callback.asynchronous = True  # AOSP DisplayManagerHandler is async.
        self.display_queue.append(callback)
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

class FrameworkWithSyncBarrier(Framework):
    """An active MessageQueue barrier stalls ordinary work, but permits async work."""
    def __init__(self, initial=2):
        super().__init__(initial)
        self.sync_barrier = False

    def next_message(self):
        if not self.sync_barrier:
            return super().next_message()
        for index, callback in enumerate(self.display_queue):
            if getattr(callback, 'asynchronous', False):
                del self.display_queue[index]
                callback()
                return
        raise AssertionError('No asynchronous message can pass the active barrier')


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

    def test_api30_display_acks_wait_behind_snapshot_under_normal_fifo(self):
        f = Framework()
        delivered = {('added', 9)}  # An unrelated ID is not an acknowledgment.
        for display_id, scale in ((10, 1), (11, 2), (12, 1), (13, 2)):
            f.shell_write(scale)
            while not f.matches(scale):
                f.next_message()
            for event in ('added', 'removed'):
                f.queue_display_ack(event, display_id, delivered)
                self.assertNotIn((event, display_id), delivered)
                while (event, display_id) not in delivered:
                    f.next_message()
            self.assertTrue(f.matches(scale))
            f.drain()
            self.assertTrue(f.matches(scale))

    def test_second_ack_under_normal_fifo_covers_snapshot_posted_during_config(self):
        f = Framework()
        # The first event may have been requested during the config callback,
        # before that callback had enqueued its persistent snapshot.
        f.setting = f.system = f.target = 1
        delivered = set()
        f.queue_display_ack('added', 10, delivered)
        f.display_queue.append(lambda: f.persist_snapshot(1))
        f.next_message()
        self.assertIn(('added', 10), delivered)
        f.queue_display_ack('removed', 10, delivered)
        while ('removed', 10) not in delivered:
            f.next_message()
        f.shell_write(2)
        f.drain()
        self.assertTrue(f.matches(2))

    def test_async_display_acks_cannot_prove_queue_drained_across_sync_barrier(self):
        f = FrameworkWithSyncBarrier()
        f.shell_write(1)
        f.next_message()  # Configuration arrived, but its snapshot is still queued.
        self.assertTrue(f.matches(1))
        f.sync_barrier = True
        pending = tuple(f.display_queue)
        delivered = set()
        for event in ('added', 'removed'):
            f.queue_display_ack(event, 10, delivered)
            f.next_message()
        self.assertEqual(delivered, {('added', 10), ('removed', 10)})
        self.assertEqual(tuple(f.display_queue), pending)  # Neither ack drained ATMS.
        self.assertTrue(f.matches(1))  # Even the immediate three-way check can pass.
        f.shell_write(2)
        f.sync_barrier = False
        f.drain()
        self.assertTrue(f.matches(1))  # Stale persistence overwrites the next request.
        self.assertFalse(f.matches(2))

    def test_api30_missing_or_wrong_kind_display_ack_is_not_a_success(self):
        f = Framework()
        f.shell_write(1)
        f.next_message()
        delivered = {('added', 9), ('changed', 10)}
        f.drain()
        self.assertTrue(f.matches(1))
        self.assertNotIn(('added', 10), delivered)
        self.assertNotIn(('removed', 10), delivered)

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

    def test_public_pipe_api_is_gated_and_older_path_requires_display_ack(self):
        self.assertIn('if(Build.VERSION.SDK_INT>=34)', SOURCE)
        self.assertIn('@androidx.annotation.RequiresApi(34)', SOURCE)
        self.assertIn('executeShellCommandRwe("sh")', SOURCE)
        self.assertNotIn('legacy synchronization only', SOURCE)
        self.assertIn('awaitLegacyDisplayThread(deadline)', SOURCE)
        self.assertIn('legacyFontShell("settings put system font_scale $scale",deadline)', SOURCE)
        self.assertNotIn('wait-for-broadcast-idle', SOURCE)
        self.assertIn('output.get(remainingTime(),TimeUnit.MILLISECONDS)', SOURCE)
        self.assertIn('error.get(remainingTime(),TimeUnit.MILLISECONDS)', SOURCE)
        self.assertIn('readers.shutdownNow()', SOURCE)

    def test_legacy_ack_has_unique_identity_no_capture_and_finally_cleanup(self):
        helper = SOURCE.split('private fun awaitLegacyDisplayThread(deadline: Long)', 1)[1].split(
            'private fun legacyFontShell', 1)[0]
        self.assertLess(helper.index('registerDisplayListener'), helper.index('createVirtualDisplay'))
        self.assertIn('createVirtualDisplay("ANPaint font synchronization",1,1,160,null,', helper)
        self.assertIn('DisplayManager.VIRTUAL_DISPLAY_FLAG_OWN_CONTENT_ONLY', helper)
        self.assertIn('val id=display!!.display.displayId', helper)
        self.assertIn('deadline) {added.contains(id)}', helper)
        self.assertIn('deadline) {removed.contains(id)}', helper)
        self.assertLess(helper.index('added.contains(id)'), helper.index('display.release()'))
        self.assertLess(helper.index('display.release()'), helper.index('removed.contains(id)'))
        self.assertIn('finally {display!!.release()}', helper)
        self.assertIn('finally {manager.unregisterDisplayListener(listener)}', helper)
        for disallowed in ('VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR', 'VIRTUAL_DISPLAY_FLAG_PUBLIC',
                           'VIRTUAL_DISPLAY_FLAG_PRESENTATION', 'MediaProjection', 'Surface('):
            self.assertNotIn(disallowed, helper)

    def test_shipped_docs_qualify_display_ack_ordering(self):
        comment = SOURCE.split('API30-33 lack the shell looper-flush command.', 1)[1].split('*/', 1)[0]
        docs = (Path(__file__).resolve().parents[1] / 'CI.md').read_text()
        for text in (comment, docs):
            self.assertIn('normal FIFO', text.replace('\n', ' '))
            self.assertIn('synchronization barrier', text)
            self.assertIn('ATMS messages', text)
            self.assertIn('portable queue-drain guarantee', text)

    def test_legacy_shell_read_is_bounded_and_closes_resources(self):
        helper = SOURCE.split('private fun legacyFontShell(command: String,deadline: Long)', 1)[1].split(
            'private var fontShellVerified', 1)[0]
        self.assertIn('executeShellCommand("timeout -s KILL ${seconds}s $command")', helper)
        self.assertIn('output.get(readRemaining,TimeUnit.MILLISECONDS)', helper)
        self.assertIn('pipe.close()', helper)
        self.assertIn('reader.shutdownNow()', helper)
        self.assertNotIn('+10000', helper)

if __name__ == '__main__':
    unittest.main(verbosity=2)
