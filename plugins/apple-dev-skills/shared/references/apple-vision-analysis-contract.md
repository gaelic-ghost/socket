# Apple Vision Analysis Contract

Keep four values attached to every analysis result: source identity, source orientation, preprocessing transform, and observation coordinate space. A result without those values cannot be safely placed back onto its image, video frame, preview, or UI.

## Source and Orientation

Record the source dimensions and `CGImagePropertyOrientation` supplied to Vision. Do not assume pixels are already upright merely because a platform image container displays them upright. Apply mirroring exactly once and distinguish sensor orientation from display orientation.

## Preprocessing Transform

Record region of interest plus crop-and-scale behavior. For custom models, include the transform from source pixels into model input. For output boxes, points, contours, landmarks, or masks, invert that preprocessing before applying preview-layer, aspect-fit/fill, or view-coordinate transforms.

## Coordinates

Vision normalized coordinates use a documented image coordinate system that may differ from UIKit, AppKit, Core Animation, and preview-layer coordinates. Use framework conversion functions where they apply. Test corners, non-square images, every supported orientation, mirroring, crop modes, and aspect-fit/fill behavior.

## Confidence and Identity

Treat confidence as request- or model-specific ranking evidence. It is not automatically a calibrated probability and never proves personal identity, authorization, safety, fairness, or correctness. Define thresholds from representative evaluation data and expose uncertainty where the product decision requires it.

Face rectangles, landmarks, and tracking are image analysis. TrueDepth face geometry is ARKit sensing. Face ID and Touch ID authentication belong to Local Authentication. Do not name one as another.

## Live Frames

Attach a monotonically increasing frame identity or source timestamp to every request and result. Bound in-flight work. Cancel or discard obsolete results where possible. Keep stateful sequence handlers serialized and never allow an older result to overwrite a newer presentation state.

## Model Evidence

For custom models, record immutable provenance, labels, input/output meanings, training or vendor claims, known limitations, and the local evaluation performed. Re-run a small regression set after model, preprocessing, crop, threshold, label, or postprocessing changes.
