# Agent Security Tool Controls

Record before execution:

```markdown
- Security question:
- Tool/source/version:
- Target and exclusions:
- Read paths:
- Write paths:
- Network destinations:
- Credentials and lifetime:
- Required privileges:
- Approval-gated actions:
- Output and evidence path:
- Timeout/stop condition:
- Cleanup and verification:
```

Use distinct approvals for:

1. sending data off-device;
2. probing a live target;
3. executing a proof of concept;
4. changing persistence or security controls;
5. accessing credentials or private data;
6. containment or remediation that can disrupt service.

An approval authorizes the described action, not adjacent targets or follow-on techniques.
