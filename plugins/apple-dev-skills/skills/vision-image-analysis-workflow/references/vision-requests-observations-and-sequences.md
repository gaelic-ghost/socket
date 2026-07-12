# Vision Requests, Observations, and Sequences

## API Family

For new code, inspect the current Swift Vision request type and execute it through the current documented handler, such as `ImageRequestHandler`, when platform availability and task support fit. Existing code may correctly use the original `VNRequest`, `VNImageRequestHandler`, and `VNSequenceRequestHandler` APIs. Modernize deliberately; do not maintain two application paths after choosing one supported family.

Set original-API request revisions only for a documented compatibility or reproducibility reason. Otherwise use the current default supported by the deployment target and record behavioral changes when moving revisions.

## Request Families

- Text and documents: recognition level, languages, language correction, regions, and candidate selection.
- Barcodes: supported symbologies, payload interpretation, and geometry.
- Faces: rectangles, landmarks, quality, capture quality, or tracking where the selected API documents them; never biometric identity.
- Shapes and scenes: rectangles, contours, horizon, saliency, trajectories, and other current built-in requests.
- Pose: body, hand, and animal landmarks with recognized-point groups, confidence, and platform availability.
- Segmentation: person, foreground, subjects, masks, pixel formats, and image alignment.
- Feature prints: compatible revisions, distance comparison, and domain-specific threshold evidence.

## Still Images and Sequences

Use independent handlers for unrelated still images. Use sequence state only for temporally related requests such as tracking. Serialize access to a sequence handler and reset it at a named stream boundary. Do not hide request errors, nil observations, cancellation, or unsupported revisions behind an empty-results success path.
