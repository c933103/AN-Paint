/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android;

/** Native gesture planning only; never replaces the post-gesture visibility check. */
final class NativeRevealDistance {
    private NativeRevealDistance() { }

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
