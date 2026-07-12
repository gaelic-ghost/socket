# Vision Core ML Model Integration

## Model Contract

Inspect `MLModelDescription`, metadata, image input constraints, flexible dimensions, labels, and output descriptions before creating a Vision model request. Record the model's immutable source or revision and any compile, download, encryption, or update boundary.

Use the current `CoreMLRequest` for new Vision-integrated code when its availability and output contract fit. Repair existing `VNCoreMLModel` and `VNCoreMLRequest` code as the original API rather than translating symbol names mechanically.

## Preprocessing

Match the model's documented image color, dimensions, normalization, and crop assumptions. Choose crop-and-scale behavior deliberately. Record the source-to-model transform so boxes, points, and masks can return to source coordinates correctly.

Do not duplicate preprocessing that Vision already performs for the selected model and request. If custom pixel math is required, keep that Core Image, Core Video, Accelerate, or Metal boundary explicit and verify it against the model's training contract.

## Output Interpretation

- Classification: preserve identifier and confidence; define label mapping and thresholds from evidence.
- Detection: preserve label, confidence, and normalized box; apply model-specific suppression only when output semantics require it.
- Segmentation: preserve mask dimensions, pixel format, class mapping, and preprocessing transform.
- Feature outputs: preserve `MLFeatureValue`, `MLMultiArray`, or pixel-buffer meaning until a typed consumer boundary.

Do not infer output meaning from shape alone. Use model metadata, generated interfaces, or authoritative model documentation.
