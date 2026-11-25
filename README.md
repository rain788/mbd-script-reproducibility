# Reproducibility package

Public materials supporting the manuscript

> A Staged Generation Method for Simulation-Driven Multibody Dynamics Design Workflows: Rule Constraints and Execution Feedback

## Contents

| Path | Content |
|---|---|
| `tasks/task_specs.md` | Parameters and acceptance checks of the 12 tasks (T1–T6 development, H1–H6 held out) |
| `tasks/T1-T6_task_definitions.json` | Natural-language task definitions of T1–T6 |
| `reference_traces/` | Reference response histories (NumPy `.npz`) used by the acceptance checker |
| `protocol/study_protocol.json` | Model digests, quantisation, sampling, seeds, budget, tolerances, run period |
| `rules/rule_library_summary.md` | Global, stage and API-level rules supplied to the rule-using methods |
| `prompts/prompt_templates.md` | Generation, diagnosis and local-repair prompt templates |
| `results/controlled_study/runs_summary.csv` | One row per run (3,360 formal + 600 ablation + 7 infrastructure stops): gates, errors, calls, solver runs, text units, timing, root cause |
| `results/controlled_study/checker_test_results.csv` | Gate truth-table and tolerance-boundary tests of the checker |
| `results/controlled_study/gate_combinations.csv` | Counts of each gate combination |
| `results/controlled_study/h6_geometry_audit.csv` | Loop-closure audit of H6 histories |
| `results/buffer_case/adams_nine_case_screen.csv` | Nine-case screen obtained with the generated Adams model |
| `results/buffer_case/reference_solutions.csv` | Independent two-DOF reference at 2, 1 and 0.5 ms maximum steps |
| `results/earlier_api_evaluation/` | Aggregates of the earlier API-based evaluation (not used for inference) |
| `checks/check_package.py` | Recomputes the main statistics and the buffer checks from these files |

## Reproduce the checks

```
pip install numpy
python checks/check_package.py
```

The script verifies the gate logic, recomputes the complete-success counts with Wilson intervals and the task-cluster bootstrap differences, and re-solves the buffer reference (RK4 against the matrix-exponential solution, static deflection, feasibility under the declared limits).

## Definitions

* Complete success = execution AND numerical agreement AND parameter fidelity AND export.
* Trace error = max_t |y(t) − y_ref(t)| / max_t |y_ref(t)|; T1–T3 use the absolute error of a closed-form terminal value.
* Text units are counted by the run controller over all model calls in a run (input and output). They are not provider tokenizer counts.
* End-to-end time = inference + Adams execution + orchestration, excluding one-off model loading.

## Limits

Models were run locally through Ollama on an NVIDIA GeForce RTX 4090 workstation and are identified by the manifest digests in `protocol/study_protocol.json`. The full Adams interface registry, CAD/Parasolid files and raw per-call payloads are not redistributed. Bitwise-identical regeneration of model outputs is not claimed. The buffer results are computational and are not physical validation data.

## License

MIT for code, templates and schemas; result files are released for research reuse with attribution.
