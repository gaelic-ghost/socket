# Apple Camera Capability Contract

Treat camera support as a layered runtime fact, not a device-name assumption.

## Capability Layers

Check each layer needed by the requested behavior:

1. Framework and API availability for the deployment target.
2. Capture authorization and required purpose strings.
3. A discovered `AVCaptureDevice` of an appropriate documented device type and position.
4. Device and virtual-device constituent characteristics.
5. A compatible `AVCaptureDevice.Format`, frame-rate range, color format, depth format, field of view, dimensions, and media subtype.
6. Session support for the input and output combination, including MultiCam cost where applicable.
7. Output support and enabled state for photo, depth, mattes, responsive capture, deferred delivery, Live Photos, RAW, spatial, cinematic, or other requested features.
8. Connection support for rotation angle, mirroring, stabilization, camera intrinsic delivery, and other connection properties.
9. Discovered runtime behavior under pressure, interruption, backgrounding, and media-services reset.
10. Physical-device evidence for hardware-dependent correctness and quality.

Do not collapse these layers into one Boolean such as `hasAdvancedCamera`.

## Capability Matrix

Report the device unique ID only in diagnostics where appropriate, device type, position, virtual/constituent relationship, selected format, frame range, depth format, session class, outputs, connections, requested features, supported features, active features, and validation state. Keep unsupported and unverified distinct.

## Configuration

Mutate a device only while holding its configuration lock, and unlock it on every path. Check support immediately before setting a property whose support depends on the selected device or format. Re-evaluate dependent settings after changing active format, device, output, session topology, or pressure mitigation.

## Evidence Language

- `documented`: current Apple documentation describes the API or behavior.
- `discovered`: the running app observed support from current framework objects.
- `simulator-limited`: the simulator cannot prove the requested sensor behavior.
- `device-verified`: the behavior was exercised on the named device/OS/configuration.
- `unverified`: no suitable runtime evidence exists.

Never promote documented or discovered support to device-verified behavior without exercising the actual path.
