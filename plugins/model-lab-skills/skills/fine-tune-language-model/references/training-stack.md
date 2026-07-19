# Training Stack Selection

Use the smallest stack that supports the required architecture and intervention:

- [Transformers](https://github.com/huggingface/transformers) for model/tokenizer loading and trainer primitives.
- [PEFT](https://github.com/huggingface/peft) for parameter-efficient adapters.
- [TRL](https://github.com/huggingface/trl) for supervised and preference-oriented post-training workflows.
- [MLX LM](https://github.com/ml-explore/mlx-lm) for Apple-silicon-native inference and supported fine-tuning workflows.

Verify support against the pinned release and target architecture. Examples from a moving main branch are not versioned proof. Save the resolved lockfile and exact command/config beside every checkpoint.
