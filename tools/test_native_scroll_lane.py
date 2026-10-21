"""Execute the same lane planner used by native position-dialog gestures."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'app/src/androidTest/java/paint/anpaint/android/NativeScrollLane.java'
HARNESS = r'''
package paint.anpaint.android;
public final class NativeScrollLaneHarness {
    public static void main(String[] args) {
        int[][] occupied = new int[(args.length - 3) / 2][2];
        for (int i = 0; i < occupied.length; i++) {
            occupied[i][0] = Integer.parseInt(args[3 + i * 2]);
            occupied[i][1] = Integer.parseInt(args[4 + i * 2]);
        }
        System.out.println(NativeScrollLane.choose(Integer.parseInt(args[0]),
            Integer.parseInt(args[1]), occupied, Integer.parseInt(args[2])));
    }
}
'''


class NativeScrollLaneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('java'):
            raise RuntimeError('Java runtime required for native scroll-lane checks')
        cls.temp = tempfile.TemporaryDirectory()
        cls.build = Path(cls.temp.name)
        harness = cls.build / 'NativeScrollLaneHarness.java'
        harness.write_text(HARNESS)
        compiler = ['javac'] if shutil.which('javac') else ['java', '-m', 'jdk.compiler/com.sun.tools.javac.Main']
        subprocess.run(compiler + ['-source', '17', '-target', '17', '-d', str(cls.build),
                                  str(SOURCE), str(harness)],
                       check=True, capture_output=True, text=True, timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def lane(self, low, high, occupied=(), clearance=2):
        args = [low, high, clearance] + [coordinate for interval in occupied for coordinate in interval]
        return subprocess.run(['java', '-cp', str(self.build), 'paint.anpaint.android.NativeScrollLaneHarness',
                               *map(str, args)], capture_output=True, text=True, timeout=10)

    def assert_lane(self, low, high, occupied=(), clearance=2):
        result = self.lane(low, high, occupied, clearance)
        self.assertEqual(0, result.returncode, result.stderr)
        lane = int(result.stdout)
        self.assertTrue(low <= lane < high)
        for left, right in occupied:
            self.assertFalse(left - clearance <= lane < right + clearance)
        return lane

    def test_landscape_center_crosses_field_but_gutter_does_not(self):
        # The failing field's real screen X extent is [144, 496), and the
        # old vertical gesture used x=320. A 16px body gutter is available.
        self.assertTrue(144 <= 320 < 496)
        self.assert_lane(130, 510, [(144, 496)])

    def test_horizontal_gesture_uses_same_geometry_on_y_axis(self):
        self.assert_lane(26, 270, [(60, 120), (140, 240)])

    def test_unoccupied_viewport_keeps_center(self):
        self.assertEqual(160, self.assert_lane(2, 318))

    def test_overlapping_and_unsorted_controls_merge_without_false_gap(self):
        obstacles = [(100, 170), (60, 120), (160, 240), (75, 90)]
        self.assertEqual(self.assert_lane(0, 280, obstacles),
                         self.assert_lane(0, 280, list(reversed(obstacles))))

    def test_offscreen_controls_are_clipped_and_touching_edges_are_blocked(self):
        self.assert_lane(10, 90, [(-100, 15), (80, 1000), (35, 60)])

    def test_one_pixel_safe_lane_is_not_mistaken_for_no_lane(self):
        self.assertEqual(10, self.assert_lane(0, 21, [(0, 8), (13, 21)], 2))

    def test_fully_obstructed_path_fails_instead_of_touching_an_editor(self):
        result = self.lane(0, 100, [(0, 50), (50, 100)])
        self.assertNotEqual(0, result.returncode)
        self.assertIn('No scroll lane outside editable controls', result.stderr)

    def test_large_and_negative_screen_coordinates_do_not_overflow(self):
        self.assert_lane(-2147483648, 2147483647, [(-10, 10)], 2147483600)

    def test_invalid_geometry_is_rejected(self):
        for args in [(5, 5, (), 2), (6, 5, (), 2), (0, 10, (), -1),
                     (0, 10, [(4, 4)], 2)]:
            with self.subTest(args=args):
                self.assertNotEqual(0, self.lane(*args).returncode)

    def test_device_keeps_native_input_and_checks_scroll_side_effects(self):
        source = (SOURCE.parent / 'AssemblyPositionDeviceTest.kt').read_text()
        self.assertIn('NativeScrollLane.choose(', source)
        self.assertIn('descendants(gesture.owner).filterIsInstance<EditText>()', source)
        self.assertIn('device.swipe(arrayOf(first,last,last,last),16)', source)
        self.assertIn('assertSame("Caption scrolling must not focus an editable control"', source)
        self.assertIn('assertEquals("Caption scrolling must not edit ${input.tag}"', source)
        self.assertIn('await("IME shown for native field input:', source)
        for forbidden in ('showSoftInput(', 'requestFocus(', '.setText(', '.scrollTo(', '.scrollBy('):
            self.assertNotIn(forbidden, source)


if __name__ == '__main__':
    unittest.main()
