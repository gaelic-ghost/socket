# Body Skeleton, Scale, Rendering, and Diagnostics

## Body Tracking

Check `ARBodyTrackingConfiguration.isSupported` before configuration. Preserve `ARBodyAnchor`, `ARSkeleton3D`, skeleton definition, joint names, parent indices, model transforms, local transforms, root/anchor transform, timestamp, tracking state, and session generation.

Use `automaticSkeletonScaleEstimationEnabled` only when supported and required. Treat `estimatedScaleFactor` as an estimate that can evolve; do not use it as an exact body measurement.

## Rendering and Animation

Define the transform chain from AR anchor to skeleton joint to model bone. Keep retargeting, bind pose, handedness, scale, smoothing, occlusion, and animation constraints with the rendering layer. RealityKit or SceneKit may own the character/scene; Metal owns advanced custom rendering. ARKit remains the sensing source.

## Diagnostics and Validation

Report configuration support, selected video format, tracking state, anchor ID, skeleton definition, missing/low-confidence behavior where exposed, scale-estimation state, frame/session identity, transform stage, elapsed time, and next inspection point. Do not log raw body or face geometry by default.

Test transform math, joint lookup, retargeting, smoothing, session reset, and stale-anchor rejection with fixtures. Validate tracking range, occlusion, lighting, multi-person limitations, animation quality, scale, and performance on representative physical devices.
