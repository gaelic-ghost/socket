# Renderer Architecture And Version Gates

## Source anchors

- [Understanding the Metal 4 core API](https://developer.apple.com/documentation/metal/understanding-the-metal-4-core-api)
- [Drawing a triangle with Metal 4](https://developer.apple.com/documentation/metal/drawing-a-triangle-with-metal-4)
- [Metal developer workflows](https://developer.apple.com/documentation/xcode/metal-developer-workflows)
- [Metal feature set tables](https://developer.apple.com/metal/capabilities/)

Metal 4 has a distinct command model: command buffers originate from the device, queues submit them, encoders bind argument tables, and command buffers do not strongly retain resources. This can coexist with Metal 3, but only with an explicit synchronization and lifetime boundary.

Use Metal 4 for a measured need such as reusable command buffers, multi-threaded encoding, argument tables, new barriers, or a Metal 4-only effect. Do not rewrite a working Metal 3 renderer merely because Metal 4 exists.

The runtime gate is an applicable OS availability check together with `device.supportsFamily(.metal4)`. Extract shared render-data and pipeline-key construction before porting an independent pass; preserve the Metal 3 backend until fallback validation passes. `MTLBinaryArchive` can persist pipelines populated during development for shipping, but should not be treated as a runtime write cache in the shipping renderer.

For every frame, identify: drawable owner, command allocator or per-frame allocation owner, resources read and written, pass dependencies, presentation owner, and completion/lifetime boundary. GPU captures are interpretable only when resources and encoder labels carry these domain names.
