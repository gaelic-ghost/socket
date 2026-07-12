# Face Geometry, Blend Shapes, and Authentication Boundary

## Face Tracking

Check `ARFaceTrackingConfiguration.isSupported`, supported video formats, maximum tracked faces where available, and world-tracking support before configuration. Preserve `ARFaceAnchor.identifier`, transform, `ARFaceGeometry` vertices/texture coordinates/triangle indices, blend-shape dictionary, eye transforms, timestamp, and session generation.

Blend shapes are animation coefficients keyed by documented locations. They are not universal emotion classifications. Eye transforms support effects relative to tracked face geometry; they do not prove attention, intent, identity, or medically meaningful gaze.

Use `supportsWorldTracking` and the configuration's documented world-tracking setting only when the device supports the combined behavior. Surface the different tracking limitations of front-camera face sensing and world tracking.

## Face ID Boundary

Local Authentication uses `LAContext` and an `LAPolicy` to evaluate whether the device owner can authenticate with Face ID, Touch ID, passcode, or another supported method. The app receives policy availability and an authentication outcome, not an enrolled biometric template, reusable face identity, AR face mesh, depth map, or blend shapes.

ARKit TrueDepth face tracking produces geometry and expression-related tracking for supported experiences. It is not Face ID and must not be used or described as system biometric authentication.
