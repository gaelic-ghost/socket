# Network Test Levels

1. Asset resolution: owner, DNS/address, route, environment, third parties.
2. Reachability: bounded host/port checks from an approved source.
3. Service identification: protocol handshake, TLS, banner, version, authentication surface.
4. Configuration review: exposure, encryption, access, segmentation, management interfaces.
5. Vulnerability check: reviewed, narrowly selected probe with safe matcher.
6. Exploit validation: separately authorized minimum proof and cleanup.

Do not jump levels because a tool supports it. Record rate, retries, concurrency, timeouts, excluded ports/hosts, and any service degradation. Use packet capture only when authorized and minimize unrelated traffic/data.
