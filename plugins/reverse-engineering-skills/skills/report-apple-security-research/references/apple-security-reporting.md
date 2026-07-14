# Apple Security Reporting Reference

## Evidence Checklist

- Product, hardware, SoC, OS marketing version, and build.
- Xcode, SDK, KDK, debugger, and analysis-tool versions when relevant.
- Artifact hashes, UUIDs, signing and entitlement state, and transformations.
- Expected and observed behavior with timestamps.
- Minimal reproduction and cleanup.
- Crash, log, trace, screenshot, or sysdiagnose excerpt tied to the reproduction.
- Direct observations, generated output, inferences, and alternatives separated.
- Impact supported by the demonstrated boundary crossing or failure.
- Builds tested, first and last observations, and beta revalidation date.

## Version Language

- `Observed on build A`: one-build fact.
- `Not observed on build B`: bounded negative observation using the same method.
- `Changed between A and B`: endpoint comparison.
- `First observed in B among A, B, and C`: supported tested range.
- `Fixed in B`: use only when the behavior is absent and the relevant conditions are comparable; avoid claiming the underlying patch without evidence.

## Privacy And Attachment Check

Before transmission, inventory every attachment and remove unrelated personal data, credentials, customer data, device identifiers, broad logs, and proprietary artifacts. Preserve the unredacted local evidence separately when required for reproducibility.

## Current Apple Sources

- [Apple Security Research](https://security.apple.com/)
- [Apple Security Bounty guidelines](https://security.apple.com/bounty/guidelines/)
- [Apple Security Research Device](https://security.apple.com/research-device)
- [Apple security releases](https://support.apple.com/100100)
- [Apple developer release feed](https://developer.apple.com/news/releases/)

Read these sources live before stating current eligibility, beta requirements, confidentiality, submission mechanics, or research-device obligations.
