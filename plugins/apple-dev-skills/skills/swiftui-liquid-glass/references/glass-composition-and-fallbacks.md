# Glass Composition And Fallbacks

Choose glass for semantically elevated, related controls or surfaces; do not use it as a blanket background effect.

- Prefer native controls and standard toolbars first.
- Apply layout, clipping, shape, tint, and other visual definition before `glassEffect` so the glass reflects the intended surface.
- Group neighboring related glass controls in `GlassEffectContainer`; leave unrelated cards, content rows, and navigation panes outside it.
- Match shape and spacing across a control group. Use interactive glass only for controls that actually accept input.
- Use availability checks around version-sensitive APIs. Earlier-OS fallback should preserve action, hierarchy, and contrast with standard materials or controls rather than pretending to be glass.

Use a glass morphing identity only for a real visual relationship across a hierarchy change. Keep the namespace local to that feature surface.
