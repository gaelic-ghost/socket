# Legacy Archive Boundary

Apple documentation archive material is useful for understanding old Core Audio code, but it should not be treated as the default modern implementation guide when current AVFAudio documentation covers the job.

Archive material can help explain:

- Audio Session Programming Guide era category behavior
- Audio Queue Services design
- Audio Unit Programming Guide callback and component concepts
- Core Audio Overview terminology
- older sample-code shapes that appear in inherited projects

Current guidance should come first for:

- `AVAudioSession` categories, modes, options, activation, and permissions
- `AVAudioEngine` graph and rendering behavior
- `AVAudioUnit` async instantiation
- modern Swift error handling and concurrency boundaries
- current platform privacy, sandbox, entitlement, and route behavior

When using archive context, say that it is historical or migration context and name the current API surface that replaces or narrows it.
