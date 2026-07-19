# Checkpoint Provenance

Record the upstream model identifier and immutable revision, tokenizer identifier and revision, training code commit, dataset revision, adapter configuration, merge procedure, quantization or pruning recipe, conversion tool and version, tensor format, declared architecture, generation configuration, artifact checksum, and file sizes.

For directory artifacts, retain a per-file checksum inventory. A directory checksum produced from sorted relative paths plus their file digests is useful for detecting change, but it does not replace the upstream revision or conversion recipe.
