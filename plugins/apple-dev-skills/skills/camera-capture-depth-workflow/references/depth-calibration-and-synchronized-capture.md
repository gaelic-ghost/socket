# Depth, Calibration, and Synchronized Capture

## Depth Formats and Values

Select an `activeDepthDataFormat` compatible with the active video format when streaming depth. Keep the native depth or disparity format and accuracy inspectable. Use `AVDepthData.converting(toDepthDataType:)` only with a documented target type and record whether the result is depth or disparity.

Filtering can improve temporal or spatial usability but changes raw sensor characteristics. Record `isDepthDataFiltered`, `depthDataAccuracy`, quality, pixel dimensions, timestamp, orientation, and the selected filtering policy.

## Calibration

Preserve `AVCameraCalibrationData`, intrinsic matrix, intrinsic reference dimensions, extrinsic relationship, pixel size, and lens-distortion lookup tables where provided. Scale intrinsics only according to the documented relationship between reference dimensions and the actual image/depth buffers. Do not call disparity metric distance without the calibration and baseline relationship needed by that representation.

## Synchronized Outputs

Use `AVCaptureDataOutputSynchronizer` for output streams that must be consumed as a synchronized collection. Inspect each `AVCaptureSynchronizedData` subtype, timestamp, and `wasDataDropped` state. A synchronized collection may contain dropped data; do not treat its arrival as proof every output delivered a usable sample.

Keep the synchronizer delegate queue serial when downstream state assumes ordering. Bound downstream work and preserve collection/frame identity when handing video and depth to Vision, Core Image, recording, or UI consumers.

## Photo Depth and Mattes

For photo capture, enable supported depth or matte delivery on the output and request it in the photo settings. Read depth, calibration, portrait-effects matte, and semantic segmentation mattes from the resulting `AVCapturePhoto`; keep their orientation, dimensions, metadata, and relationship to the primary image explicit.
