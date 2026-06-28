# Model, Presentation, and Performance

Use this reference when diagnosing Core Animation visual state, hit testing, or performance claims.

## Model and Presentation Layers

- Treat the model layer as durable state.
- Treat the presentation layer as an in-flight visual snapshot.
- Use presentation-layer values for diagnostics, animation-time hit testing, or visual interpolation only.
- Do not persist presentation-layer values back into app state unless the interaction explicitly commits that in-flight visual state.
- When an explicit animation ends, the model layer should already represent the intended final value.

## Timing and Transactions

- `CATransaction` groups layer-tree changes and can control implicit animation behavior.
- `CAMediaTiming` concepts such as duration, begin time, speed, time offset, repeat count, and autoreverses belong to layer animation timing, not arbitrary app model timing.
- Prefer framework animation APIs when their timing model already matches the task.
- Avoid timers for ordinary layer animation. Use framework timing primitives or display links only when the visual state is truly frame-driven.

## Performance Evidence

- Static code review can flag likely problems, but it cannot prove frame pacing.
- Use Xcode runtime diagnostics, Instruments, Core Animation tools, Time Profiler, or platform-specific performance tools when performance is the claim.
- Report missing validation honestly when device refresh rate, compositor behavior, or visual artifacts cannot be inspected.
- Screenshots can show final layout, but they cannot prove timing, smoothness, or flicker absence.

## Repair Checklist

- Verify owner lifetime for the layer tree.
- Verify model-layer final values.
- Verify implicit animations are enabled or disabled intentionally.
- Verify contents scale and backing scale behavior.
- Verify animations are removed, replaced, or allowed to complete intentionally.
- Verify hit testing uses the right visual or model state.
- Hand off to `xcode-build-run-workflow` for runtime validation.
