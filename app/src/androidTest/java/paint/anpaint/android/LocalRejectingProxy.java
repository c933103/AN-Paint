/* AN Paint contributors, 2026. GNU AGPL-3.0-or-later. */
package paint.anpaint.android;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicReference;

/** Test-only loopback sink. It never resolves or connects to a requested destination. */
public final class LocalRejectingProxy implements AutoCloseable {
    private final ServerSocket listener;
    private final Thread worker;
    private final CopyOnWriteArrayList<String> requests = new CopyOnWriteArrayList<>();
    private final AtomicReference<Throwable> failure = new AtomicReference<>();
    private volatile boolean closed;
    private volatile Socket current;

    public LocalRejectingProxy() throws IOException {
        listener = new ServerSocket(0, 16, InetAddress.getByName("127.0.0.1"));
        worker = new Thread(this::serve, "gallery-local-rejecting-proxy");
        worker.setDaemon(true);
        worker.start();
    }

    public int port() { return listener.getLocalPort(); }
    public String rule() { return "http://127.0.0.1:" + port(); }
    public List<String> requests() { return new ArrayList<>(requests); }
    public void assertHealthy() {
        if (failure.get() != null) throw new AssertionError("Local rejecting proxy failed", failure.get());
    }

    private void serve() {
        try {
            while (!closed) {
                try (Socket client = listener.accept()) {
                    current = client;
                    client.setSoTimeout(2000);
                    InputStream input = client.getInputStream();
                    String request = line(input);
                    if (request == null) continue; // A speculative socket sent no request.
                    int remaining = 65536 - request.length();
                    for (String header = line(input); header != null && !header.isEmpty(); header = line(input)) {
                        remaining -= header.length();
                        if (remaining < 0) throw new IOException("Proxy fixture header budget exceeded");
                    }
                    requests.add(request);
                    // Reject HTTP and HTTPS CONNECT alike. There is no upstream socket,
                    // DNS lookup of the target, TLS tunnel, redirect or direct fallback.
                    try {
                        client.getOutputStream().write(("HTTP/1.1 502 Bad Gateway\r\n"
                                + "Content-Length: 0\r\nConnection: close\r\n\r\n")
                                .getBytes(StandardCharsets.US_ASCII));
                        client.getOutputStream().flush();
                    } catch (SocketException cancelled) {
                        // stopLoading/destroy may close a denied request after observation.
                    }
                } catch (SocketTimeoutException idle) {
                    // A speculative idle socket cannot become a tunnel or hold cleanup.
                } finally {
                    current = null;
                }
            }
        } catch (IOException error) {
            if (!closed) failure.compareAndSet(null, error);
        }
    }

    private static String line(InputStream input) throws IOException {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        for (int count = 0; count < 8192; count++) {
            int value = input.read();
            if (value < 0) return bytes.size() == 0 ? null : bytes.toString("US-ASCII");
            if (value == '\n') return bytes.toString("US-ASCII").replaceFirst("\\r$", "");
            bytes.write(value);
        }
        throw new IOException("Proxy fixture request line too long");
    }

    @Override public void close() throws IOException, InterruptedException {
        closed = true;
        listener.close();
        Socket client = current;
        if (client != null) client.close();
        worker.join(3000);
        if (worker.isAlive()) throw new IOException("Proxy fixture worker did not stop");
        assertHealthy();
    }
}
