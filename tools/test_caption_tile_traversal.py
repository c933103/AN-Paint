"""Exercise the device test's real Java tiler. Scroll counts are a model, not device timing."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'app/src/androidTest/java/paint/anpaint/android/CaptionTileTraversal.java'
HARNESS = r'''
package paint.anpaint.android;
public final class CaptionTileHarness {
    public static void main(String[] args) {
        CaptionTileTraversal.visit(Integer.parseInt(args[0]), Integer.parseInt(args[1]),
            Integer.parseInt(args[2]), Integer.parseInt(args[3]), Integer.parseInt(args[4]),
            (left, top, right, bottom) -> System.out.printf("%d,%d,%d,%d%n", left, top, right, bottom));
    }
}
'''


def row_major(left, top, right, bottom, tile):
    return [(x, y, min(x + tile, right), min(y + tile, bottom))
            for y in range(top, bottom, tile) for x in range(left, right, tile)]


def horizontal_scrolls(tiles, viewport):
    """Minimum native horizontal moves needed to reveal each exact tile in order."""
    offset = 0
    moves = []
    for left, _, right, _ in tiles:
        next_offset = left if left < offset else right - viewport if right > offset + viewport else offset
        if next_offset != offset:
            moves.append(next_offset - offset)
        offset = next_offset
    return moves


class CaptionTileTraversalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('java'):
            raise RuntimeError('Java runtime required for caption traversal checks')
        cls.temp = tempfile.TemporaryDirectory()
        cls.build = Path(cls.temp.name)
        harness = cls.build / 'CaptionTileHarness.java'
        harness.write_text(HARNESS)
        compiler = ['javac'] if shutil.which('javac') else ['java', '-m', 'jdk.compiler/com.sun.tools.javac.Main']
        subprocess.run(compiler + ['-source', '17', '-target', '17', '-d', str(cls.build), str(SOURCE), str(harness)],
                       check=True, capture_output=True, text=True, timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def tiles(self, bounds, tile=64):
        result = subprocess.run(['java', '-cp', str(self.build), 'paint.anpaint.android.CaptionTileHarness',
                                 *map(str, (*bounds, tile))], capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return [tuple(map(int, line.split(','))) for line in result.stdout.splitlines()]

    def test_exact_same_rectangles_and_area_without_gaps_or_duplicates(self):
        # Portrait/landscape-sized, wide vertical captions, partial edge tiles,
        # padded/negative origins, sub-tile bounds, and empty regions.
        for bounds in [(0, 0, 320, 592), (0, 0, 601, 272), (5, 8, 1542, 128),
                       (12, 4, 143, 325), (-7, -3, 71, 88), (1, 2, 3, 4),
                       (0, 0, 0, 90), (0, 0, 90, 0)]:
            with self.subTest(bounds=bounds):
                actual = self.tiles(bounds)
                expected = row_major(*bounds, 64)
                self.assertCountEqual(actual, expected)
                self.assertEqual(len(actual), len(set(actual)))
                left, top, right, bottom = bounds
                self.assertEqual(sum((r-l)*(b-t) for l, t, r, b in actual), (right-left)*(bottom-top))

    def test_wide_caption_visits_each_column_without_repeated_horizontal_sweeps(self):
        for viewport, height in [(276, 320), (577, 120)]:
            with self.subTest(viewport=viewport, height=height):
                bounds = (0, 0, 1537, height)
                actual = self.tiles(bounds)
                self.assertEqual([tile[0] for tile in actual], sorted(tile[0] for tile in actual))
                before = horizontal_scrolls(row_major(*bounds, 64), viewport)
                after = horizontal_scrolls(actual, viewport)
                self.assertTrue(any(move < 0 for move in before))
                self.assertTrue(all(move > 0 for move in after))
                self.assertLess(len(after), len(before))
                self.assertLess(sum(map(abs, after)), sum(map(abs, before)))

    def test_large_coordinate_edges_do_not_overflow(self):
        bounds = (2147483600, 2147483601, 2147483647, 2147483647)
        self.assertEqual(self.tiles(bounds), [bounds])


if __name__ == '__main__':
    unittest.main()
