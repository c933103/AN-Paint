/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android;

/** Native gesture planning only; never replaces the post-gesture visibility check. */
final class NativeRevealDistance {
    private int previousDirection;
    private boolean lookahead = true;

    // One planner per target reveal. Real native motion can exceed requested
    // travel; after an observed overshoot, stop aligning to opposite edges.
    int plan(int direction, int hidden, int leadingSpace, int touchSlop, int maximum) {
        if (direction != -1 && direction != 1)
            throw new IllegalArgumentException("Invalid reveal direction");
        if (previousDirection != 0 && previousDirection != direction) lookahead = false;
        previousDirection = direction;
        return choose(hidden, lookahead ? leadingSpace : 0, touchSlop, maximum);
    }

    static int choose(int hidden, int leadingSpace, int touchSlop, int maximum) {
        if (hidden <= 0 || touchSlop < 0 || maximum <= 0)
            throw new IllegalArgumentException("Invalid reveal geometry");
        // Minimum travel compensates for native touch slop as before. When
        // space permits, advance the current tile toward the leading edge:
        // subsequent tiles then share this viewport instead of each needing
        // a tiny, expensive injected gesture. Never exceed the native lane.
        long minimum = (long) hidden + touchSlop + 2;
        return (int) Math.min(maximum, Math.max(minimum, leadingSpace));
    }
}
