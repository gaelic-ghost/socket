# Apple Spatial Data and Privacy Contract

Spatial data can reveal a person's face, body, home, workplace, possessions, location, movement, and bystanders. Treat collection, processing, persistence, sharing, and deletion as part of the technical design.

## Data Inventory

Inventory every collected or derived value: camera frames, depth/confidence, anchors, transforms, feature points, planes, meshes/classification, world maps, room structure, geographic anchors, reference images/objects, face geometry, blend shapes, eye transforms, body skeletons, and provider events.

For each value record:

- framework type and coordinate space
- source session/provider and timestamp
- documented accuracy or uncertainty
- whether it contains or derives from a person, bystander, private space, or precise location
- whether it remains in memory, persists locally, synchronizes, transmits, or enters analytics/ML
- purpose, user notice/consent, access controls, retention, deletion, and export policy

## Platform Authorization

Use the platform's documented authorization model. On visionOS, request only the `ARKitSession` authorization types needed by the selected providers and react to authorization changes. On iOS/iPadOS, keep camera/privacy requirements and ARKit configuration support explicit. Authorization does not replace product-level notice or data minimization.

## Accuracy Language

Anchors, meshes, raycasts, planes, depth, face coefficients, eye transforms, and body joints are estimates with changing tracking quality. Do not describe them as exact survey, medical, identity, emotion, attention, or safety measurements without separate validated evidence and authority.

## Retention and Sharing

Default to in-memory, session-scoped processing. Persist only the minimum data required by a named feature. Version persisted spatial formats, bind them to the intended app/user/context, protect them at rest and in transit, and provide a deletion path. Revalidate assumptions before public sharing or server use.

## Diagnostic Safety

Log identifiers, states, counts, timings, and error context rather than raw camera frames, face/body geometry, world maps, precise locations, or room meshes. If a private diagnostic artifact is explicitly required, make its scope, storage path, access, and deletion visible.
