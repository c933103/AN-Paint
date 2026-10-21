/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/** Chooses a real touch lane outside editable descendants, without changing their behavior. */
final class NativeScrollLane {
    private NativeScrollLane() { }

    /** Bounds and occupied intervals are half-open screen coordinates on the cross axis. */
    static int choose(int low, int high, int[][] occupied, int clearance) {
        if (low >= high || clearance < 0) throw new IllegalArgumentException("Invalid scroll bounds");
        List<long[]> blocked = new ArrayList<>();
        for (int[] interval : occupied) {
            if (interval.length != 2 || interval[0] >= interval[1])
                throw new IllegalArgumentException("Invalid editable bounds");
            long start = Math.max(low, (long) interval[0] - clearance);
            long end = Math.min(high, (long) interval[1] + clearance);
            if (start < end) blocked.add(new long[] {start, end});
        }
        blocked.sort(Comparator.comparingLong(interval -> interval[0]));
        // The final sentinel also considers the free interval after the last obstacle.
        blocked.add(new long[] {high, high});
        long cursor = low, bestWidth = 0, best = 0;
        long center = (long) low + ((long) high - low) / 2;
        for (long[] interval : blocked) {
            if (interval[0] > cursor) {
                long width = interval[0] - cursor;
                long candidate = cursor + width / 2;
                if (width > bestWidth || (width == bestWidth
                        && Math.abs(candidate - center) < Math.abs(best - center))) {
                    bestWidth = width;
                    best = candidate;
                }
            }
            cursor = Math.max(cursor, interval[1]);
        }
        if (bestWidth == 0)
            throw new IllegalArgumentException("No scroll lane outside editable controls");
        return (int) best;
    }
}
