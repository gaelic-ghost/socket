# Apple System Artifacts Reference

## Required Identity

- Product family, device or Mac model, board identifier, and SoC.
- OS marketing version and exact build.
- Container hash and component member path.
- Component hash, UUID, architecture, and version metadata.
- KDK build and symbol UUID when used.
- Restore manifest and personalization or signing state when present.
- Extraction tool, version, command, and output hash.

## Correlation Rules

Public XNU, dyld, Security, objc4, and distribution manifests are valuable architectural and historical sources. A repository tag or tarball name is not sufficient proof that code exactly matches a shipping component. Record symbol, UUID, binary structure, build manifest, or behavior evidence supporting the correspondence.

Exact-build KDK availability is a prerequisite for exact symbol claims. A nearby KDK can suggest names or structure but must remain labeled as a hypothesis source.

## Boot Context

Use Apple Platform Security to place Boot ROM, later boot stages, LocalPolicy, secure boot, signed system volume, kernel collections, and auxiliary kernel collections in context. Keep architecture descriptions separate from observations on a particular artifact or security policy state.

## Authoritative Sources

- [Apple XNU source](https://github.com/apple-oss-distributions/xnu)
- [Apple dyld source](https://github.com/apple-oss-distributions/dyld)
- [Apple Security source](https://github.com/apple-oss-distributions/Security)
- [Apple Silicon boot process](https://support.apple.com/guide/security/secac71d5623/web)
- [Secure software updates and personalization](https://support.apple.com/guide/security/secf683e0b36/web)
- [Debugging a custom kernel extension](https://developer.apple.com/documentation/apple-silicon/debugging-a-custom-kernel-extension)
- [Running macOS in a VM on Apple Silicon](https://developer.apple.com/documentation/virtualization/running-macos-in-a-virtual-machine-on-apple-silicon)

Check current release documentation for KDK, restore, security-policy, and beta behavior.
