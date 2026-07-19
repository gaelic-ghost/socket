# Dataset Controls

Choose the split boundary that matches the likely contamination path. Related turns from one conversation, files from one repository, passages from one document, or samples derived from one original must not cross splits merely because their row identifiers differ.

Use exact hashes for byte- or normalization-identical records and a documented approximate method for near duplicates. Preserve the algorithm, normalization, threshold, and counts.

Never infer permission from public accessibility. Record the source terms and whether the resulting artifact may be redistributed, used only locally, or requires access-controlled storage.

Treat evaluator prompts and hidden tests as test data. Do not train on them, tune repeatedly against them without documenting adaptive overfitting, or include their content in public logs.
