"""Host-only deterministic checks for rejecting-sink shutdown/error ordering."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SINK = ROOT / 'app/src/androidTest/java/paint/anpaint/android/LocalRejectingProxy.java'

# Add scheduling hooks only to a temporary compilation of the real fixture.
# Parsing, socket closure, exception publication and close/join remain unchanged.
# Latches expose the same ordering as a descheduled worker, without adding sleeps
# or lengthening the fixture's deadlines. No hooks ship in the Android test APK.
HARNESS = r'''
package paint.anpaint.android;
import java.io.IOException;
import java.net.ProtocolException;
import java.net.Socket;
import java.net.SocketException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
public final class GalleryBudgetShutdownHarness {
    private static final CountDownLatch accepted = new CountDownLatch(1);
    private static final CountDownLatch caught = new CountDownLatch(1);
    private static final CountDownLatch closing = new CountDownLatch(1);
    private static volatile IOException observed;

    static void afterAccept() { accepted.countDown(); }
    static void afterCloseFlag() { closing.countDown(); }
    static void beforePublication(IOException error) {
        observed = error;
        caught.countDown();
        await(closing, "close flag");
    }
    private static void await(CountDownLatch latch, String event) {
        try {
            if (!latch.await(3, TimeUnit.SECONDS)) throw new AssertionError("Missing " + event);
        } catch (InterruptedException error) {
            Thread.currentThread().interrupt();
            throw new AssertionError(error);
        }
    }
    public static void main(String[] args) throws Exception {
        LocalRejectingProxy proxy = new LocalRejectingProxy();
        if (args[0].equals("idle")) {
            try (Socket idle = new Socket("127.0.0.1", proxy.port())) {
                await(accepted, "accepted idle socket");
                proxy.close();
            }
            if (!(observed instanceof SocketException)) throw new AssertionError("Shutdown was not exercised", observed);
            if (!proxy.requests().isEmpty()) throw new AssertionError("Idle request was recorded");
            proxy.assertHealthy();
            return;
        }
        String payload;
        String expected;
        switch (args[0]) {
            case "line":
                payload = "X".repeat(8192) + "\r\n\r\n";
                expected = "Proxy fixture request line too long";
                break;
            case "header-line":
                payload = "GET / HTTP/1.1\r\nX: " + "X".repeat(8192) + "\r\n\r\n";
                expected = "Proxy fixture request line too long";
                break;
            case "headers":
                payload = "GET / HTTP/1.1\r\n" + ("X: " + "X".repeat(4093) + "\r\n").repeat(16) + "\r\n";
                expected = "Proxy fixture header budget exceeded";
                break;
            default: throw new AssertionError(args[0]);
        }
        try (Socket client = new Socket("127.0.0.1", proxy.port())) {
            client.setSoTimeout(3000);
            client.getOutputStream().write(payload.getBytes(StandardCharsets.US_ASCII));
            try {
                if (client.getInputStream().readAllBytes().length != 0)
                    throw new AssertionError("Oversized input got a response");
            } catch (SocketException closed) { }
        }
        await(caught, "budget exception before shutdown");
        if (!expected.equals(observed.getMessage())) throw new AssertionError("Wrong parser error", observed);
        if (!proxy.requests().isEmpty()) throw new AssertionError("Oversized request recorded as accepted");
        // The worker is paused after try-with-resources closed the socket, before
        // it checks closed. close() must not erase this already-detected failure.
        try {
            proxy.close();
            throw new AssertionError("Missing budget failure");
        } catch (AssertionError error) {
            if (!"Local rejecting proxy failed".equals(error.getMessage())) throw error;
            if (!(error.getCause() instanceof ProtocolException)
                    || !expected.equals(error.getCause().getMessage()))
                throw new AssertionError("Wrong budget failure cause", error);
        }
    }
}
'''


class GallerySinkShutdownTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('java'):
            raise RuntimeError('Java runtime required for gallery sink checks')
        compiler = ['javac'] if shutil.which('javac') else ['java', '-m', 'jdk.compiler/com.sun.tools.javac.Main']
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.build = Path(cls.temp.name)
        source = SINK.read_text()
        hooks = {
            '        } catch (IOException error) {\n': '            GalleryBudgetShutdownHarness.beforePublication(error);\n',
            '        closed = true;\n': '        GalleryBudgetShutdownHarness.afterCloseFlag();\n',
            '                    current = client;\n': '                    GalleryBudgetShutdownHarness.afterAccept();\n',
        }
        for anchor, hook in hooks.items():
            if source.count(anchor) != 1:
                raise AssertionError('Review shutdown scheduling hook after source change: ' + anchor.strip())
            source = source.replace(anchor, anchor + hook)
        fixture = cls.build / 'LocalRejectingProxy.java'
        fixture.write_text(source)
        harness = cls.build / 'GalleryBudgetShutdownHarness.java'
        harness.write_text(HARNESS)
        subprocess.run(compiler + ['-source', '17', '-target', '17', '-d', str(cls.build), str(fixture), str(harness)],
                       check=True, capture_output=True, text=True, timeout=30)

    def check_shutdown(self, mode):
        result = subprocess.run(['java', '-cp', str(self.build), 'paint.anpaint.android.GalleryBudgetShutdownHarness', mode],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_request_line_budget_survives_shutdown_before_publication(self):
        self.check_shutdown('line')

    def test_header_line_budget_survives_shutdown_before_publication(self):
        self.check_shutdown('header-line')

    def test_total_header_budget_survives_shutdown_before_publication(self):
        self.check_shutdown('headers')

    def test_intentional_idle_socket_shutdown_is_not_a_failure(self):
        self.check_shutdown('idle')


if __name__ == '__main__':
    unittest.main()
