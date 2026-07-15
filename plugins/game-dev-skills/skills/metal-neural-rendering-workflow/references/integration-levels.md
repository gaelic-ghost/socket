# Neural Rendering Integration Levels

## Source anchors

- [Machine learning passes](https://developer.apple.com/documentation/metal/machine-learning-passes)
- [Running a machine learning model on the GPU timeline](https://developer.apple.com/documentation/metal/running-a-machine-learning-model-on-the-gpu-timeline)
- [Running inline ML operations in a shader with Metal 4](https://developer.apple.com/documentation/metal/running-inline-ml-operations-in-a-shader-with-metal-4)
- [Metal Performance Shaders](https://developer.apple.com/documentation/metalperformanceshaders)
- [WWDC26 Metal guide](https://developer.apple.com/wwdc26/guides/metal/)

MetalFX is the highest-level option. Metal 4 machine-learning passes schedule a prepared model inside a command buffer. Inline tensor operations are the lowest-level path: a shader uses tensor inputs and tensor operations directly.

Current Apple documentation says inline tensor operations require Metal Shading Language 4 and identifies Apple GPU family 10 and later as adding neural accelerators for tensor operations. Treat that as a capability gate, not a marketing label or an assumption about every Apple-silicon device.

The WWDC26 Metal guide describes newer quantized tensor formats, scale factors, and Metal Performance Primitives as current beta-era work. Recheck the shipping SDK before adopting those APIs in a release target.
