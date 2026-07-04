---
name: http3-quic-workflow
description: Plan, implement, test, and diagnose HTTP/3 or QUIC work, including RFC-backed source checks, ALPN, Alt-Svc, TLS, UDP reachability, QUIC streams and datagrams, HTTP semantics over QUIC, proxy/CDN/server support, qlog or packet evidence, and handoffs to stack-specific implementation plugins.
---

# HTTP/3 And QUIC Workflow

## Purpose

Use this skill when the protocol behavior matters, not merely because an API is served over HTTPS. The practical decision is whether the task needs HTTP/3 enablement, direct QUIC transport behavior, deployment diagnostics, or a handoff back to ordinary HTTP framework work.

## Source Check

Check current sources before claiming behavior:

- [RFC 9000: QUIC](https://datatracker.ietf.org/doc/rfc9000/)
- [RFC 9001: Using TLS to Secure QUIC](https://datatracker.ietf.org/doc/rfc9001/)
- [RFC 9002: QUIC Loss Detection and Congestion Control](https://datatracker.ietf.org/doc/rfc9002/)
- [RFC 9114: HTTP/3](https://datatracker.ietf.org/doc/rfc9114/)
- [RFC 9204: QPACK](https://datatracker.ietf.org/doc/rfc9204/)
- [RFC 9220: WebSockets over HTTP/3](https://datatracker.ietf.org/doc/rfc9220/)
- [RFC 9297: HTTP Datagrams and Capsule Protocol](https://datatracker.ietf.org/doc/rfc9297/)

Also check the selected server, client, browser, CDN, proxy, OS, or library docs because HTTP/3 availability is often implementation-specific.

## Planning Workflow

1. Inspect the current path:
   - client, server, reverse proxy, CDN, load balancer, TLS terminator, and local dev server
   - HTTP versions currently negotiated
   - ALPN, Alt-Svc, certificates, port exposure, UDP support, firewall rules, and hosting platform limits
   - library support for HTTP/3, QUIC streams, datagrams, WebSockets over HTTP/3, and qlog
2. Decide the scope:
   - enable HTTP/3 for existing HTTP semantics
   - diagnose why HTTP/3 negotiation falls back to HTTP/2 or HTTP/1.1
   - use direct QUIC streams or datagrams
   - use HTTP Datagrams or WebTransport-adjacent behavior
   - preserve HTTP/2 or WebSocket fallback
3. Keep semantics clear:
   - HTTP/3 changes the transport under HTTP; it does not automatically change API shape
   - direct QUIC is a transport design choice and should have a concrete reason
   - datagrams can be unreliable and need loss, ordering, and fallback behavior spelled out
   - Alt-Svc advertisement is not proof that clients successfully negotiated HTTP/3
4. Route implementation:
   - use `server-side-swift` for Vapor, Hummingbird, SwiftNIO, or SwiftPM work
   - use `rust-skills`, `python-skills`, or `server-side-jvm` for language-specific server/client work
   - use `web-dev-skills`, `apple-dev-skills`, or `android-dev-skills` for client integration
   - use `cloud-deployment-skills` for CDN, proxy, load balancer, firewall, hosting, or container platform constraints

## Diagnostics

Prefer evidence that shows negotiated protocol and the failing hop:

- browser network panel or runtime logs
- `curl` with HTTP version reporting when local curl supports it
- server access logs that include protocol version
- proxy/CDN dashboard or config
- TLS and ALPN inspection
- UDP reachability checks
- qlog, packet capture, or library-level QUIC events when transport behavior is the bug

When reporting a failure, name the exact hop: browser, app client, TLS terminator, reverse proxy, CDN, origin, container, firewall, NAT, or library.

## Output Shape

Return:

1. `Protocol shape`: HTTP/3 over QUIC, direct QUIC, datagrams, WebSockets over HTTP/3, or fallback.
2. `Evidence`: negotiated version, ALPN/Alt-Svc state, UDP path, proxy/CDN/server support, and logs or traces.
3. `Change`: config, code, dependency, deployment, or diagnostics-only.
4. `Fallback`: HTTP/2, HTTP/1.1, WebSocket, SSE, or disabled path.
5. `Validation`: exact commands, browser checks, runtime logs, qlog, packet capture, or deployment checks.
6. `Handoffs`: stack plugin or cloud/deployment follow-up.

## Guardrails

- Do not claim HTTP/3 is enabled from config alone; verify negotiation where practical.
- Do not expose UDP or change TLS termination without naming the deployment surface.
- Do not replace ordinary HTTP code with direct QUIC unless the feature needs transport ownership.
- Do not remove fallback paths unless the target clients and deployment are known to support the new protocol.
