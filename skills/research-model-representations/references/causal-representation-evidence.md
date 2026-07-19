# Causal Representation Evidence

Use an evidence ladder:

1. observation: activations differ between matched groups;
2. decoding: a held-out probe predicts the label;
3. localization: the signal is specific enough to layers, positions, or features to test;
4. intervention: changing the candidate representation changes the target behavior;
5. specificity: matched random or unrelated interventions do not produce the same effect;
6. mediation: patching or counterfactual tests connect the representation to the output under the stated conditions.

Avoid claiming a human-readable concept is stored in one direction merely because a linear classifier succeeds. Record preprocessing, mean-centering, normalization, probe regularization, seeds, and all searched layers so the result can be reproduced and corrected for selection.
