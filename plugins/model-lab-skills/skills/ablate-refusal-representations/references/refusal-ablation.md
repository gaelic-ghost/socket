# Refusal Ablation Research

Primary starting points:

- [Refusal in language models is mediated by a single direction](https://arxiv.org/abs/2406.11717)
- [Reference implementation](https://github.com/andyrdt/refusal_direction)

Treat the paper and repository as a reproducible hypothesis, not a universal API or result. Verify model-family assumptions, hook points, chat templates, token selection, mean-difference construction, layer search, and weight-edit formulas against the pinned source revision.

Required controls include held-out harm categories, harmless prompts matched for topic and syntax, random and unrelated directions, strength/layer sweeps, benign compliance, capability tasks, and evaluation of the serialized artifact. Preserve enough harmful-output evidence for evaluation while avoiding unnecessary redistribution of generated harmful content.
