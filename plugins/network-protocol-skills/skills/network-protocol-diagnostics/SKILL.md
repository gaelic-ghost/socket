---
name: network-protocol-diagnostics
description: Diagnose modern network protocol failures with evidence, including HTTP version negotiation, QUIC and UDP reachability, TLS and ALPN, Alt-Svc, browser networking, WebRTC ICE/STUN/TURN, MoQ relay logs, proxies, CDNs, firewalls, NAT, packet captures, qlog, server logs, and stack-specific handoffs.
---

# Network Protocol Diagnostics

## Purpose

Use this skill when the main job is finding where a protocol path breaks. The goal is to name the failing hop and gather evidence before changing code, configuration, or infrastructure.

## Source Check

Check relevant current sources for the protocol under investigation:

- [RFC 9000: QUIC](https://datatracker.ietf.org/doc/rfc9000/)
- [RFC 9114: HTTP/3](https://datatracker.ietf.org/doc/rfc9114/)
- [W3C WebRTC](https://www.w3.org/TR/webrtc/)
- [RFC 8825: Real-Time Protocols for Browser-Based Applications](https://datatracker.ietf.org/doc/rfc8825/)
- [IETF MoQ working group documents](https://datatracker.ietf.org/wg/moq/documents/)

Then check the actual implementation docs: browser, client library, server framework, CDN, proxy, container platform, TURN service, relay, or hosting provider.

## Diagnostic Workflow

1. Preserve the symptom:
   - exact user-visible failure, status code, browser console line, log line, timeout, media symptom, negotiated protocol, or degraded fallback
   - client, server, region, network, host, container, browser, app version, and timestamp
2. Map the path:
   - client runtime
   - local network, NAT, corporate firewall, VPN, or mobile network
   - DNS, SVCB/HTTPS records, TLS, ALPN, Alt-Svc, proxy, CDN, load balancer, origin, container, and service
   - STUN/TURN/SFU/relay path for WebRTC or MoQ
3. Gather the narrowest useful evidence:
   - browser network panel, WebRTC internals, or client logs
   - server/proxy/CDN logs
   - `curl` or protocol client output when it proves negotiated version or failure point
   - TLS and ALPN inspection
   - UDP reachability checks
   - qlog or packet capture when transport behavior is genuinely unclear
4. Classify the failure:
   - protocol unsupported
   - fallback expected but missing
   - DNS or certificate issue
   - ALPN or Alt-Svc mismatch
   - UDP blocked or NAT traversal failed
   - proxy/CDN/load balancer does not pass the protocol
   - framework or library lacks support
   - app code confused signaling, media, transport, or API semantics
5. Choose the next owner:
   - protocol skill for design correction
   - stack plugin for code changes
   - cloud/deployment plugin for infrastructure
   - user/manual validation when the missing evidence requires a real browser, network, device, account, relay, CDN, or media endpoint

## Output Shape

Return:

1. `Symptom`: exact failure and affected client/server path.
2. `Path`: client, network, proxy/CDN, origin, relay/TURN/SFU, and service boundaries.
3. `Evidence`: logs, negotiated protocol, TLS/ALPN, Alt-Svc, ICE, qlog, packet capture, or command output.
4. `Likely cause`: specific failing hop and why.
5. `Fix owner`: code, config, dependency, cloud/deployment, protocol design, or manual environment.
6. `Validation`: exact repeat check and fallback check.

## Guardrails

- Do not change infrastructure before naming the failing hop when read-only evidence is available.
- Do not claim UDP, TURN, HTTP/3, or WebRTC behavior from local success alone if the bug is on a different network.
- Do not paste secrets, TURN credentials, session tokens, full private URLs, or packet captures containing sensitive payloads into reports.
- Do not reduce protocol failures to vague strings like `network error`; name the protocol, hop, and likely cause.
