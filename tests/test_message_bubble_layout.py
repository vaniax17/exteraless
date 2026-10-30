"""Execute the preview background alpha handoff without an Android runtime."""
import subprocess
from pathlib import Path


def test_preview_background_ignores_pending_list_alpha_and_restores_it(tmp_path):
    source = Path("TMessagesProj/src/main/java/org/telegram/ui/MessageSendPreview.java").read_text()
    if "final float destAlpha =" in source:
        start = source.index("final float destAlpha =")
        end = source.index("destCell.setAlpha(destAlpha);", start) + len("destCell.setAlpha(destAlpha);")
        block = source[start:end]
    else:
        block = "destCell.drawBackgroundInternal(canvas, true);"
        assert block in source
    java = """
class BubbleLayoutTest {
    static class Cell {
        float alpha;
        float getAlpha() { return alpha; }
        void setAlpha(float value) { alpha = value; }
        void drawBackgroundInternal(Object canvas, boolean parent) {
            if (alpha != 1f) throw new AssertionError("Transition background is transparent");
        }
    }
    public static void main(String[] args) {
        Cell destCell = new Cell();
        Object canvas = new Object();
        // Pending list insertion, partial animation, acknowledgment, settled redraw.
        for (float alpha : new float[] {0f, .25f, 1f, 1f}) {
            destCell.setAlpha(alpha);
            BLOCK
            if (destCell.getAlpha() != alpha) throw new AssertionError("List alpha changed");
        }
    }
}
""".replace("BLOCK", block)
    path = tmp_path / "BubbleLayoutTest.java"
    path.write_text(java)
    subprocess.run(["javac", str(path)], check=True, capture_output=True, text=True)
    subprocess.run(["java", "-cp", str(tmp_path), "BubbleLayoutTest"], check=True, capture_output=True, text=True)
