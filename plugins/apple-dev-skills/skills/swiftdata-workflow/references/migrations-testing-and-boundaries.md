# Migrations, Testing, And Boundaries

- Treat schema changes as data-compatibility work and identify the existing store versions before mutation.
- Use explicit migration plans when lightweight evolution is insufficient; never assume destructive recreation is acceptable.
- Use isolated in-memory or temporary containers for previews and tests when persistence across runs is not part of the test.
- Use `GEAWhateverDTO` for network or transfer boundaries and `GEAWhateverRecord` only for a genuinely distinct stored or serialized representation.
- Keep import/export, networking, server sync, and migration tooling outside the direct SwiftUI integration path while converting explicitly at the boundary.
