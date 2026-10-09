"""Host checks for the local sink and installed-test inventory; not Android execution."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from run_android_instrumentation import declared_tests, restart_partition, verify_restart_reports

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / 'app/src/androidTest/java/paint/anpaint/android'
GALLERY = 'paint.anpaint.android.GalleryDraftDeviceTest'


HARNESS = r'''
import paint.anpaint.android.LocalRejectingProxy;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
public final class GallerySinkHarness {
    public static void main(String[] args) throws Exception {
        LocalRejectingProxy proxy = new LocalRejectingProxy();
        if (!proxy.rule().equals("http://127.0.0.1:" + proxy.port())) throw new AssertionError();
        if (args[0].equals("requests")) {
            try {
                String[] requests = {"CONNECT gallery-fixture.invalid:443 HTTP/1.1",
                    "GET http://gallery-fixture.invalid/page HTTP/1.1"};
                for (String request : requests) {
                    try (Socket client = new Socket("127.0.0.1", proxy.port())) {
                        client.setSoTimeout(3000);
                        client.getOutputStream().write((request + "\r\nHost: fixture.invalid\r\n\r\n")
                            .getBytes(StandardCharsets.US_ASCII));
                        String reply = new String(client.getInputStream().readAllBytes(), StandardCharsets.US_ASCII);
                        if (!reply.equals("HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"))
                            throw new AssertionError(reply);
                    }
                }
                if (!proxy.requests().equals(java.util.Arrays.asList(requests))) throw new AssertionError(proxy.requests());
                proxy.assertHealthy();
            } finally { proxy.close(); }
        } else if (args[0].equals("idle-close")) {
            try (Socket idle = new Socket("127.0.0.1", proxy.port())) {
                proxy.close();
            }
        } else if (args[0].equals("oversized")) {
            try (Socket client = new Socket("127.0.0.1", proxy.port())) {
                client.setSoTimeout(3000);
                client.getOutputStream().write(("X".repeat(8192) + "\r\n\r\n").getBytes(StandardCharsets.US_ASCII));
                try { client.getInputStream().readAllBytes(); } catch (java.net.SocketException expected) { }
            }
            if (!proxy.requests().isEmpty()) throw new AssertionError("Oversized request recorded as accepted");
            try { proxy.close(); throw new AssertionError("Missing budget failure"); }
            catch (AssertionError expected) {
                if (!"Local rejecting proxy failed".equals(expected.getMessage())) throw expected;
            }
        } else throw new AssertionError(args[0]);
    }
}
'''


class GallerySinkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This project already requires Java for its Android build. No silent skip.
        if not shutil.which('java'):
            raise RuntimeError('Java runtime required for gallery sink checks')
        compiler = ['javac'] if shutil.which('javac') else ['java', '-m', 'jdk.compiler/com.sun.tools.javac.Main']
        cls.temp = tempfile.TemporaryDirectory()
        cls.build = Path(cls.temp.name)
        harness = cls.build / 'GallerySinkHarness.java'
        harness.write_text(HARNESS)
        # The cloud JRE includes jdk.compiler but omits historical ct.sym files.
        # Compile Java-17 syntax/bytecode against this host JDK; Android API
        # compatibility is separately checked by the actual Android test build.
        subprocess.run(compiler + ['-source', '17', '-target', '17', '-d', str(cls.build),
                        str(ANDROID / 'LocalRejectingProxy.java'), str(harness)],
                       check=True, capture_output=True, text=True, timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def check_sink(self, mode):
        result = subprocess.run(['java', '-cp', str(self.build), 'GallerySinkHarness', mode],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_http_and_https_connect_receive_only_local_rejection(self):
        self.check_sink('requests')

    def test_idle_socket_cannot_hold_cleanup(self):
        self.check_sink('idle-close')

    def test_oversized_request_fails_closed(self):
        self.check_sink('oversized')


class GalleryRoutingContractTest(unittest.TestCase):
    def test_three_gallery_methods_stay_in_existing_ordinary_restart_partition(self):
        inventory = declared_tests(ROOT / 'app/src/androidTest')
        ordinary, seed, verify = restart_partition(inventory)
        gallery = {item for item in inventory if item[0] == GALLERY}
        self.assertEqual(len(gallery), 3)
        self.assertTrue(gallery.issubset(ordinary))
        self.assertEqual(len(seed), 1)
        self.assertEqual(len(verify), 1)
        self.assertEqual(ordinary | seed | verify, inventory)
        self.assertFalse(ordinary & seed or ordinary & verify or seed & verify)
        reports = [{'success': True, 'leave_target_running': mode,
                    'expected_tests': len(part), 'completed_tests': len(part),
                    'cases': [{'classname': owner, 'name': name, 'status': 'passed'}
                              for owner, name in sorted(part)]}
                   for part, mode in zip((ordinary, seed, verify), (False, True, False))]
        self.assertTrue(verify_restart_reports(inventory, reports)['success'])
        reports[0]['cases'] = [x for x in reports[0]['cases'] if x['classname'] != GALLERY]
        with self.assertRaises(ValueError):
            verify_restart_reports(inventory, reports)

    def test_proxy_boundary_precedes_launch_and_has_no_direct_fallback(self):
        source = (ANDROID / 'GalleryDraftDeviceTest.kt').read_text()
        setup = source.split('@Before fun launchEditorWithLocalDocument()', 1)[1].split('@After', 1)[0]
        self.assertLess(setup.index('establishNetworkBoundary()'), setup.index('ActivityScenario.launch'))
        boundary = source.split('private fun establishNetworkBoundary()', 1)[1]
        self.assertIn('WebViewFeature.PROXY_OVERRIDE', boundary)
        self.assertIn('awaitProxyChange', boundary)
        self.assertIn('CONNECT gallery-fixture.invalid:443', boundary)
        self.assertIn('.removeImplicitRules()', boundary)
        self.assertNotIn('.addDirect(', source)
        self.assertNotIn('.addBypassRule(', source)
        self.assertNotIn('Assume.', source)
        self.assertNotIn('.onActivityResult(', source)
        self.assertIn('requests.add(Intent(intent));return null', source)
        self.assertIn('galleries.all {it.isDestroyed}', source)
        self.assertIn('stage==Stage.PRE_ON_CREATE', source)
        self.assertIn('getDeclaredField("openConnection")', source)
        self.assertIn('0,nativeAcquisitions.get()', source)
        self.assertLess(source.index('galleries.all {it.isDestroyed}'), source.index('clearProxyOverride'))
        gradle = (ROOT / 'app/build.gradle').read_text()
        matches = [line.strip() for line in gradle.splitlines() if 'androidx.webkit:webkit:' in line]
        self.assertEqual(matches, ["androidTestImplementation 'androidx.webkit:webkit:1.12.1'"])


if __name__ == '__main__':
    unittest.main()
