# Prompt templates

The templates below are sanitized structural templates. They retain the information flow used by the implementation while replacing project-specific paths, credentials, and proprietary API text with placeholders.

## Initial skeleton generation

```text
You are generating an Adams/View simulation script for task {task_id}.
Generate only the minimum runnable skeleton for stages {skeleton_stages}.
Task intent: {task_description}
Available registered APIs: {stage_api_subset}
Applicable rules: {global_rules}; {stage_rules}
Requirements: preserve object ownership, declared units, and deterministic output naming.
Do not add measurements or exports that are outside the requested skeleton.
Return executable code only.
```

## Execution diagnosis

```text
Diagnose the primary failed stage using the evidence hierarchy below.
Stage state: {stage_state}
Traceback and solver log: {execution_log}
Failure signature history: {repair_memory}
First classify textual/API errors, then model/topology errors, then solver errors.
If a generic L5 solver failure is compatible with an upstream L1/L2 cause, report the ambiguity,
propose one targeted upstream diagnostic check, and do not claim causal certainty from the log alone.
Return: primary_stage, confidence, diagnostic_check, rationale.
```

## Monotonic local repair

```text
Repair only target stages {target_stages}.
Stable stages {stable_stages} are frozen unless the task-completeness gate identifies an explicit
cross-stage dependency that cannot be satisfied otherwise. If unfreezing is required, mark the
global restart boundary and regenerate the dependent stage contract before editing code.
Use only these APIs: {stage_api_subset}
Use only these rules: {matched_rules}
Rejected patterns: {repair_memory}
Execution evidence: {execution_log}
Return replacement code for target stages and a short dependency note.
```
