# MetalFX Effect Selection

## Source anchors

- [MetalFX](https://developer.apple.com/documentation/metalfx)
- [Applying temporal antialiasing and upscaling using MetalFX](https://developer.apple.com/documentation/metalfx/applying-temporal-antialiasing-and-upscaling-using-metalfx)
- [WWDC26 Metal guide](https://developer.apple.com/wwdc26/guides/metal/)

Use spatial scaling when there is no temporal history contract. Use temporal scaling when the renderer can provide coherent motion/depth/history inputs. Use interpolation only with an explicit present cadence and a dedicated rendering/presentation flow. Use denoising when the input is intentionally noisy, such as a real-time ray-traced pass.

The current Dash Apple reference includes `MTLFXSpatialScalerDescriptor`, `MTLFXTemporalScalerDescriptor`, `MTLFXFrameInterpolatorDescriptor`, and `MTLFXTemporalDenoisedScalerDescriptor`. Check availability for the actual deployment target rather than assuming all effects travel together.
