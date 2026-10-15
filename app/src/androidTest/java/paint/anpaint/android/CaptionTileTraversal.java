/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android;

/** Exact caption coverage in column order; shared by the device test and host checks. */
final class CaptionTileTraversal {
    private CaptionTileTraversal() { }

    interface Visitor {
        void visit(int left, int top, int right, int bottom);
    }

    static void visit(int left, int top, int right, int bottom, int tile, Visitor visitor) {
        if (tile <= 0) throw new IllegalArgumentException("Tile must be positive");
        for (int x = left; x < right;) {
            int nextX = (int) Math.min((long) x + tile, right);
            for (int y = top; y < bottom;) {
                int nextY = (int) Math.min((long) y + tile, bottom);
                visitor.visit(x, y, nextX, nextY);
                y = nextY;
            }
            x = nextX;
        }
    }
}
