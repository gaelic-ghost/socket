# Steering Controls

At minimum compare: no intervention, the proposed direction, its negative, a random direction with matched norm, and a simple prompt-based control. If the direction was estimated from contrastive means, repeat estimation across resamples or seeds and test on held-out topics.

Report target metrics as a function of layer and strength, not only the best point discovered after search. Keep the selection set separate from final evaluation. Record whether vectors were normalized per layer, scaled relative to activation norms, applied to every token or a subset, and added before or after the relevant residual operation.
