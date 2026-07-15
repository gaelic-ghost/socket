# Metal Asset Streaming Model

## Source anchors

- [Loading textures and models using Metal fast resource loading](https://developer.apple.com/documentation/metal/loading-textures-and-models-using-metal-fast-resource-loading)
- [Streaming large images with Metal sparse textures](https://developer.apple.com/documentation/metal/streaming-large-images-with-metal-sparse-textures)
- [Simplifying GPU resource management with residency sets](https://developer.apple.com/documentation/metal/simplifying-gpu-resource-management-with-residency-sets)
- [Metal feature set tables](https://developer.apple.com/metal/capabilities/)

Start with a content budget and ordinary resource ownership. Add heaps, residency sets, fast loading, or sparse mapping only when a measured failure mode requires them.

Sparse mapping controls which regions of a large resource are backed at a given time; it adds mapping, synchronization, and fallback responsibilities. A streaming plan must define what remains visible while desired detail is unavailable.

For Metal 4, resource residency can be applied through residency sets on command queues or command buffers. Preserve the queue/frame lifetime contract before moving a resource into a set.
