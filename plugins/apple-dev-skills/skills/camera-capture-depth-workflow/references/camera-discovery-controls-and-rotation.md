# Camera Discovery, Controls, and Rotation

## Discovery and Formats

Use `AVCaptureDevice.DiscoverySession` with the documented device types, media type, and position required by the product. Treat virtual devices as devices with constituent cameras; inspect constituent switching behavior and supported zoom ranges rather than counting lenses.

Inspect `formats`, supported frame-rate ranges, dimensions, media subtype, color-space support, field of view, stabilization, depth formats, and related format properties before selecting `activeFormat`. Prefer a session preset when it expresses the requirement; choose an explicit format only when frame rate, depth pairing, pixel format, resolution, HDR, or another concrete constraint requires it.

Use `AVCaptureMultiCamSession.isMultiCamSupported` and `DiscoverySession.supportedMultiCamDeviceSets` when simultaneous cameras are required. Monitor hardware and system pressure cost and degrade deliberately.

## Device Controls

Balance `lockForConfiguration()` and `unlockForConfiguration()` on every path. Check support before changing focus mode and point, exposure mode and point, custom duration/ISO, white-balance mode and gains, zoom factor or ramp, torch mode and level, stabilization-related format choices, and low-light settings.

Do not continuously overwrite automatic controls from UI polling. Define whether the user, automatic camera behavior, subject-area monitoring, or a capture feature owns each control and when ownership returns.

## Rotation and Mirroring

Use `AVCaptureDevice.RotationCoordinator` and its documented horizon-level preview and capture angles where available. Apply a supported `AVCaptureConnection.videoRotationAngle` to the correct connection. Keep preview and capture angles distinct.

Treat front-camera mirroring separately from rotation. Record whether pixel buffers, preview, photos, metadata, depth, and mattes are physically transformed or carry orientation metadata, and normalize only at a named boundary.
