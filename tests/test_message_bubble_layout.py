"""Execute the production background layout gate without an Android runtime."""
import subprocess
from pathlib import Path


def test_background_ready_on_first_draw_and_after_rebind(tmp_path):
    source = Path("TMessagesProj/src/main/java/org/telegram/ui/Cells/ChatMessageCell.java").read_text()
    start = source.index("private boolean drawBackgroundInternal(Canvas canvas, boolean fromParent, boolean internal) {")
    gate = source[start:source.index("final boolean hasUnsupportedBlocks", start)]
    java = """
class BubbleLayoutTest {
    static class Canvas {}
    Object currentMessageObject = new Object();
    boolean wasLayout, animationRunning, forcedLayout;
    void forceLayout() {}
    int getLeft() { return 0; }
    int getTop() { return 0; }
    int getRight() { return 100; }
    int getBottom() { return 50; }
    void onLayout(boolean changed, int l, int t, int r, int b) {
        wasLayout = true;
        forcedLayout = false;
    }
    GATE
        return true;
    }
    public static void main(String[] args) {
        BubbleLayoutTest cell = new BubbleLayoutTest();
        for (boolean parent : new boolean[] {false, true}) {
            for (boolean animating : new boolean[] {false, true}) {
                cell.animationRunning = animating;
                // Optimistic bind, acknowledgment rebind, later update.
                for (int update = 0; update < 3; update++) {
                    cell.wasLayout = false;
                    if (!cell.drawBackgroundInternal(new Canvas(), parent, false) || !cell.wasLayout)
                        throw new AssertionError("Background skipped after bind");
                    if (!cell.drawBackgroundInternal(new Canvas(), parent, false))
                        throw new AssertionError("Background disappeared");
                }
            }
        }
        cell.currentMessageObject = null;
        if (cell.drawBackgroundInternal(new Canvas(), true, false))
            throw new AssertionError("Unbound cell must not draw");
    }
}
""".replace("GATE", gate)
    path = tmp_path / "BubbleLayoutTest.java"
    path.write_text(java)
    subprocess.run(["javac", str(path)], check=True, capture_output=True, text=True)
    subprocess.run(["java", "-cp", str(tmp_path), "BubbleLayoutTest"], check=True, capture_output=True, text=True)
