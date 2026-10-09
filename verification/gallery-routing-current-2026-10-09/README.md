# Current-source gallery routing candidate

Prepared from accepted develop `4b615ce2d9e27814df84812b90858b5f676ce51a` for review before changing existing PR19's branch/base. The original experiment remains at `dc518e7663ee3173f81ee6a931e15fb4ab9c467f`.

## Exact bounded scope

- Add `GalleryDraftDeviceTest`: three actual Android editor → gallery → recreated covered editor flows, retaining confirmation, cancellation and a saved first source followed by an empty cancelled second draft.
- Preserve the real activity/result route. The monitor observes the gallery and returns null; only external SAF destination results are substituted. Fixtures are inserted directly into the local drawing before opening the gallery. The tests do not click image-use, metadata-copy, search, provider-navigation or download controls.
- Replace old inline-ledger assumptions with the current private `image_credit_session` token, read-only session-file assertions and the editor's retained ownership token. Wait for actual asynchronous startup and scheduled autosave completion.
- Retain complete committed/floating pixels, geometry/rotation, separate ledgers, undo, a further editor recreation, collapsed Save/Export credit panels, real clipboard checks and decoded Base64/PNG output with distinct dirty-state behavior.
- Preserve the accepted sentinel clipboard-preview fix before input, including checks that dismissal leaves both clipboard contents and the dialog intact.
- Add a test-only loopback rejection fixture and an `androidTestImplementation` dependency on AndroidX WebKit 1.12.1. No production runtime dependency, source, resources, manifest, native code or release behavior is changed.

## Pre-load containment contract

Require `PROXY_OVERRIDE`, set a process-local proxy rule with no DIRECT fallback or bypass, remove implicit localhost/link-local bypasses, and await the applied callback before creating a probe or launching any gallery. An HTTPS request to a reserved `.invalid` hostname must be positively observed as CONNECT by the local sink. Unsupported APIs, missing callback or missing sink evidence fail; nothing is skipped or sent directly as a fallback.

The sink binds only to 127.0.0.1. It records the request line and returns HTTP 502 for HTTP and CONNECT alike. It contains no upstream connection, destination DNS lookup or TLS forwarding. The first actual gallery home request must also appear at that sink before the WebView content is replaced with local HTML. Later recreated WebViews use local HTML with network loads disabled.

The selected flows never initiate the gallery's Java/native acquisition actions. As a separate fail-closed tripwire, each real gallery's existing `openConnection` test seam is replaced at PRE_ON_CREATE with a callback that counts and rejects any acquisition before a connection is made. Teardown requires zero attempts. No new production hook is added. This is a containment fixture for those flows, not a universal firewall or provider-integration test. All tracked gallery activities must be destroyed and WebViews detached/settled before clearing the proxy override. Cleanup failure retains the rejecting override rather than reopening network access.

API contracts: [process-local ProxyController and callback requirement](https://developer.android.com/reference/androidx/webkit/ProxyController), [proxy rules and implicit bypass removal](https://developer.android.com/reference/androidx/webkit/ProxyConfig.Builder), [pinned WebKit 1.12.1 release](https://developer.android.com/jetpack/androidx/releases/webkit#1.12.1).

## Existing runner architecture is preserved

No CI workflow, emulator script, deadline or instrumentation runner changes are proposed. The three gallery methods join the existing ordinary app partition; the accepted seed/verify pair and external live-process force-stop boundary remain byte-for-byte unchanged. Host checks require that the new gallery methods are included exactly once and that omitting them makes the existing aggregate verifier fail.

The accepted develop post-merge run measured its 14 ordinary app cases at 110.100 seconds. Historical PR19's three gallery cases took 39.789 seconds in a separate old-tree invocation. These are different runs/source trees and cannot establish the combined candidate duration. The unchanged ordinary invocation has a 180-second deadline; fresh measurement is required and deadline exhaustion must remain a failure.

## Verification limits

The host fixture checks compile and execute the actual Java rejection server for HTTP/CONNECT denial, bounded malformed requests and idle cleanup. They also check source ordering, test-only dependency scope and exact restart-partition accounting. Host-JDK compilation is not Android API compatibility verification, and source checks do not establish actual WebView proxy behavior.

The local environment has Java 21's compiler module but lacks the javac launcher and historical ct.sym data; the host fixture uses Java-17 source/target syntax against the host JDK. No Android SDK, adb or Gradle installation was found. Kotlin/Android compilation, live emulator routing, actual WebView containment, lint and the candidate suite duration remain pending exact-head CI. Physical-device, API30, process-death routing and language acceptance are not claimed.

Historical old-tree evidence is separately preserved at [977ec6a2](https://github.com/c933103/AN-Paint/tree/977ec6a272413b2e0508966638f68211aeebfbc8/verification/gallery-routing-reconciliation-2026-10-09). Its successful runtime results do not validate this candidate.
