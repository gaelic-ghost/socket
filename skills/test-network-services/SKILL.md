---
name: test-network-services
description: Inventory and test explicitly authorized network services with bounded discovery and protocol-aware validation. Use for approved hosts, address ranges, ports, TLS, banners, service versions, authentication, exposure, segmentation, configuration, packet evidence, or narrowly reviewed vulnerability checks when rate, source, third-party boundaries, and stop conditions are explicit.
---

# Test Network Services

## Overview

Establish what is actually listening and reachable before making vulnerability claims. Keep discovery, identification, configuration review, authentication tests, and exploit validation as separate authorized levels.

Read [references/network-test-levels.md](references/network-test-levels.md) before selecting tools or scan intensity.

## Workflow

1. Load approved targets/exclusions, source addresses, network path, time/rate limits, credentials, and contacts.
2. Resolve target identity.
   - Record DNS, addresses, cloud/CDN/load-balancer ownership, environment, and routes; stop on third-party or out-of-scope resolution.
3. Discover conservatively.
   - Start with known assets and low-rate reachability/port checks; record tool/version/options, packet source, loss, and filtering.
4. Identify services.
   - Validate protocol, TLS/certificate, banner/version, authentication exposure, and application behavior instead of trusting port numbers or one fingerprint.
5. Assess configuration and exposure.
   - Review unnecessary listeners, network boundary, encryption, weak/default access, anonymous behavior, management interfaces, and segmentation from approved vantage points.
6. Validate vulnerability candidates.
   - Review scanner/template logic and use the smallest protocol-aware proof; route protocol mechanics to `network-protocol-skills`.
7. Stop and clean up.
   - Halt on instability, rate-limit distress, unexpected sensitive data, third parties, or scope drift; close sessions and remove temporary access.

## Output

Return target resolution, discovery coverage, validated services, configuration/exposure observations, vulnerability candidates/validation, negative results, impact, and cleanup.
