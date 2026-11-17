"""Execute native Position gesture-distance planning, including coverage controls."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'app/src/androidTest/java/paint/anpaint/android/NativeRevealDistance.java'
HARNESS = '''package paint.anpaint.android;
public final class RevealHarness {
 public static void main(String[] args) {
  for(int i=0;i<args.length;i+=4)
   System.out.println(NativeRevealDistance.choose(Integer.parseInt(args[i]),
    Integer.parseInt(args[i+1]),Integer.parseInt(args[i+2]),Integer.parseInt(args[i+3])));
 }
}'''

class NativeRevealDistanceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.build = Path(cls.temp.name)
        harness = cls.build / 'RevealHarness.java'
        harness.write_text(HARNESS)
        compiler = ['javac'] if shutil.which('javac') else ['java', '-m', 'jdk.compiler/com.sun.tools.javac.Main']
        subprocess.run(compiler + ['-source', '17', '-target', '17', '-d', str(cls.build),
                                  str(SOURCE), str(harness)], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def choose(self, *args):
        return subprocess.run(['java', '-cp', str(self.build), 'paint.anpaint.android.RevealHarness',
                               *map(str, args)], capture_output=True, text=True, timeout=10)

    def test_reveals_more_than_minimum_without_overshooting_current_tile(self):
        # Real portrait viewport width244, tile64, maximum native lane148.
        self.assertEqual('148', self.choose(63, 243, 8, 148).stdout.strip())
        # Near the end of a viewport, align toward its leading edge safely.
        self.assertEqual('102', self.choose(2, 102, 8, 148).stdout.strip())

    def test_tight_target_retains_original_slop_compensation(self):
        self.assertEqual('12', self.choose(2, 4, 8, 148).stdout.strip())

    def test_long_distance_is_capped_and_arithmetic_does_not_overflow(self):
        self.assertEqual('148', self.choose(2147483647, 2147483647, 2147483647, 148).stdout.strip())

    def test_invalid_geometry_fails_closed(self):
        for args in [(0, 0, 8, 148), (-1, 0, 8, 148), (1, 10, -1, 148), (1, 10, 8, 0)]:
            with self.subTest(args=args):
                self.assertNotEqual(0, self.choose(*args).returncode)

    def test_each_tile_still_has_to_fit_across_viewport_sizes(self):
        cases = []
        for viewport in (142, 244, 545):
            for tile in (16, 35, 64):
                for hidden in (1, 17, 63, 127):
                    spare = viewport + hidden - tile
                    maximum = viewport - 2 * (viewport // 5)
                    cases.extend((hidden, spare, 8, maximum))
        result = self.choose(*cases)
        self.assertEqual(0, result.returncode, result.stderr)
        for i, distance in enumerate(map(int, result.stdout.split())):
            hidden, spare, slop, maximum = cases[4*i:4*i+4]
            self.assertTrue(0 < distance <= maximum)
            # Model the native slop loss, not Android dispatch. If a single
            # gesture reaches the tile, it may not skip beyond its leading edge.
            travel = max(0, distance - slop)
            if travel >= hidden:
                self.assertLessEqual(travel, spare)

    def test_native_obligations_and_budgets_remain(self):
        source = (SOURCE.parent / 'AssemblyPositionDeviceTest.kt').read_text()
        for required in ('NativeRevealDistance.choose(', 'CaptionTileTraversal.visit(',
                         'visibleBounds(view).contains(target())', 'repeat(24)',
                         'SystemClock.uptimeMillis()+45000', 'SystemClock.uptimeMillis()+8000',
                         'device.swipe(arrayOf(first,last,last,last),16)',
                         'await("IME shown for native field input:',
                         'Caption scrolling must not focus an editable control',
                         'Caption scrolling must not edit ${input.tag}'):
            self.assertIn(required, source)
        for forbidden in ('showSoftInput(', 'requestFocus(', '.scrollTo(', '.scrollBy('):
            self.assertNotIn(forbidden, source)

if __name__ == '__main__':
    unittest.main()
