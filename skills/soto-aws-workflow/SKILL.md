---
name: soto-aws-workflow
description: Add, review, or migrate AWS integrations in server-side Swift using Soto as the standard SDK, with one shared AWSClient per application or Lambda environment and explicit single-owner shutdown.
license: Apache-2.0
compatibility: SwiftPM server components using Soto on native macOS development and GitHub Actions Linux deployment workflows.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: server-side-swift-aws
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(swift:*) Bash(curl:*)
---

# Soto AWS Workflow

## Purpose

Make Soto the one default AWS integration path for Gale-owned server-side Swift components. This skill owns SDK choice, manifest wiring, credentials and region configuration, `AWSClient` lifecycle, service-object reuse, tests, and migration boundaries.

## Standard Path

1. Add `https://github.com/soto-project/soto.git` and only the Soto service products the component uses.
2. Create one `AWSClient` for the application or Lambda execution environment.
3. Construct S3, SES, DynamoDB, SQS, or other Soto service objects with that shared client. Do not create an `AWSClient` per request, route, repository, actor, or service object.
4. Use the normal credential provider chain and runtime configuration. Never commit static credentials or put them in generated examples.
5. Give one lifecycle owner responsibility for shutdown. Call async `shutdown()` or `syncShutdown()` exactly once before the owner is released; do not let every consumer attempt cleanup.
6. In Lambda, create the client outside per-invocation work so warm invocations reuse it, and connect the single shutdown to the Lambda environment lifecycle.
7. Unit-test domain adapters behind narrow first-party protocols. Use live AWS tests only in an explicitly protected GitHub Actions environment.

## SDK Decision

- Soto is the default for all new server-side Swift AWS work.
- Existing Soto integrations stay on Soto.
- Existing official AWS SDK for Swift integrations stay in place unless the task explicitly authorizes migration.
- Choose the official AWS SDK for Swift only when a required AWS capability is absent or materially incompatible in Soto, or an existing public contract already exposes official-SDK types. Record the concrete service/API/version evidence for the exception.
- Record an approved exception with `references/official-sdk-exception.template.md` so the deviation is specific and reviewable.
- “AWS publishes it,” familiarity, generated examples, or another skill default are not sufficient exceptions.

## Local And Cloud Boundary

- Compile and test Soto integrations natively on macOS.
- Use local fakes or protocol-backed test doubles for ordinary local tests. Do not start LocalStack, a Linux VM, or a container runtime.
- Run live AWS integration tests, Linux artifact builds, and deployments only in GitHub Actions with OIDC and protected environments.

## Evidence

- [Soto AWSClient guide](https://soto.codes/user-guides/awsclient.html)
- [Soto AWS service objects](https://soto.codes/user-guides/service-objects.html)
- [Using Soto on AWS Lambda](https://soto.codes/user-guides/using-soto-on-aws-lambda.html)
- [Official AWS SDK for Swift](https://docs.aws.amazon.com/sdk-for-swift/)
- `references/awsclient-lifecycle.md`
- `references/official-sdk-exception.template.md`
