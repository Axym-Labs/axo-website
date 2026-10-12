---
title: Diagnostics
description: Read the 24-row attention panel, test metric sensitivity with controlled defects, and write teacher and model diagnostic rows.
section: AxoBench metrics
order: 146
---

## Read the attention panel

Every evaluation report ends with the same 24 rows. A row reads `YES` when its value crosses the trigger, `NO` when it does not, and `NA` when the evidence is unavailable, for example without intervention pairs or with a single morphology. `YES` is an early watch that points at a failure mode to inspect; it is not a pass or fail decision. Each row's `basis` field in the returned report states the reason for its trigger.

| Area | Row | Trigger | Basis |
| --- | --- | --- | --- |
| validity | `nonfinite_outputs` | > 0 | Every emitted score and voltage must be finite |
| physiology | `voltage_bounds` | > 0 | Fraction of predicted voltages outside −120 to +60 mV |
| physiology | `voltage_slew` | > 0 | Fraction of one-step changes above 120 mV/ms |
| voltage | `voltage_null_skill` | ≤ 0 | `1 − MSE / MSE` of the per-trace teacher mean; non-positive skill does not beat that null |
| voltage | `voltage_bias` | > 0.10 SD | Mean offset in teacher standard deviations |
| voltage | `voltage_gain` | outside 0.90–1.10 | Least-squares gain of predicted on teacher voltage |
| dynamics | `residual_lag1` | \|r\| > 0.10 | Lag-1 autocorrelation of the residual; above 0.10, more than 1% of residual variance is linearly predictable |
| states | `low_input_state_error` | > 1.10× and > 0.5 mV | RMSE in the lowest 10% of input load, away from teacher spikes, relative to the overall RMSE |
| states | `hyperpolarized_state_error` | > 1.10× and > 0.5 mV | Same ratio in the lowest 10% of teacher voltage |
| states | `depolarized_state_error` | > 1.10× and > 0.5 mV | Same ratio in the highest 10% of teacher voltage |
| states | `high_dvdt_error` | > 1.10× and > 0.5 mV | Same ratio in the highest 10% of teacher slope |
| states | `near_spike_error` | > 1.10× and > 0.5 mV | Same ratio within 5 ms of teacher spikes |
| states | `post_input_burst_error` | > 1.10× and > 0.5 mV | Same ratio in the 5 ms after the highest 10% of input load |
| spikes | `spike_exact_fidelity` | < 0.90 | F1 at 0 ms |
| spikes | `spike_5ms_fidelity` | < 0.95 | F1 at 5 ms |
| spikes | `spike_timing_tolerance_gap` | > 0.05 | F1 gain from 0 to 5 ms tolerance |
| spikes | `spike_count_error` | > 0.10 | Per-trace count error relative to the mean teacher count |
| spikes | `spike_timing_bias` | \|bias\| > 0.5 ms | Median displacement of matched spikes |
| calibration | `default_threshold_count` | outside 0.80–1.25 | Predicted-to-teacher count ratio at the uncalibrated default threshold |
| physiology | `refractory_violations` | > 0 | Fraction of predicted inter-spike intervals below 2 ms |
| intervention | `intervention_response_skill` | < 0.80 | Response skill of the worst condition against a zero-response prediction |
| intervention | `intervention_direction` | < 0.95 | Sign agreement of the worst condition on teacher changes of at least 0.5 mV |
| intervention | `intervention_gain` | outside 0.80–1.20 | Response gain of the condition furthest from 1 |
| transfer | `morphology_error_disparity` | > 1.25× median | Worst morphology's voltage RMSE relative to the median morphology |

A 1.10 RMSE ratio corresponds to at least 21% higher mean squared error in that state. The voltage and state rows use the unclipped teacher voltage over all scored steps. The count, timing-bias, default-threshold, and refractory rows count supra-threshold timesteps rather than the score-peak events of spike F1, so a spike score that stays above threshold for two steps registers there as a short interval. Intervention and transfer rows name the condition or morphology that triggered them in brackets.

## Test metric sensitivity

A fidelity metric should worsen steadily as a known defect grows. `axobench.benchmark.defect_injection` corrupts teacher traces with one controlled defect at a time and scores the corrupted traces against the original teacher. Spike-timing defects move the action-potential waveform with the spike, so voltage and spike train stay consistent; voltage defects leave the spike train exact.

| Defect | Dose | Default doses |
| --- | --- | --- |
| `spike_jitter` | Gaussian spike-time jitter, standard deviation in steps | 0, 0.5, 1, 2, 4, 8 |
| `spike_deletion` | Fraction of spikes deleted | 0, 0.1, 0.25, 0.5, 0.75, 1 |
| `spike_insertion` | Spurious spikes added, as a fraction of the spike count | 0, 0.1, 0.25, 0.5, 1, 2 |
| `global_lag` | Whole output delayed by this many steps | 0, 1, 2, 3, 5, 10 |
| `ap_clip` | Fraction of the voltage range above −55 mV removed by clipping; 1 is the NeuronIO target | 0, 0.25, 0.5, 0.75, 0.9, 1 |
| `ap_smoothing` | Gaussian smoothing of the action-potential window, sigma in steps | 0, 0.5, 1, 2, 4 |
| `voltage_lowpass` | Gaussian low-pass of the whole trace, sigma in steps | 0, 0.5, 1, 2, 4, 8 |
| `voltage_offset` | Constant voltage offset in mV | 0, 0.5, 1, 2, 4, 8 |
| `voltage_gain` | Fractional gain error around each trace's mean | 0, 0.05, 0.1, 0.25, 0.5 |
| `post_spike` | Fraction by which the 50 steps after each action potential are replaced by a straight line | 0, 0.25, 0.5, 0.75, 1 |

```python
from axobench.data import ShardedNeuronIODataset
from axobench.benchmark.defect_injection import defect_dose_rows

val = ShardedNeuronIODataset("data/axobench/val", cache_shards=1)
indices = range(16)
_, targets = val.get_batch(indices)
soma_mv = val.get_optional_array_batch("soma_mv", indices)

rows = defect_dose_rows(
    targets[..., 0],
    soma_mv,
    doses={"spike_jitter": (0, 1, 2, 4), "voltage_offset": (0, 1, 2, 4)},
    ignore_start=500,
)
for row in rows:
    print(row["defect"], row["dose"], row["mean_f1"],
          row["voltage_sera"], row["subthreshold_rmse_mv"], row["auc"])
```

Each row contains the AxoBench scores, Mean F1 with its tolerance curve, the coincidence factor at 2 ms, Voltage and Dynamics SERA with their skill against the per-trace mean, and the subthreshold RMSE and skill, next to the historical NeuronIO scores: timestep AUC of a smoothed spike train and the clipped voltage RMSE with and without rescaling. Some responses follow from the definitions: a constant offset leaves Mean F1 unchanged, and spike jitter leaves the subthreshold RMSE near zero because the moved action potentials fall inside excluded windows. The informative comparisons are the doses at which a score stops responding or responds to a defect it should ignore. The random defects use a seed derived from the defect name, so rows are reproducible.

## Check the teacher

Teacher QC rows describe the dataset before any model is involved:

```bash
axobench benchmark-rows --mode teacher-qc \
  --dataset-root data/axobench \
  --max-samples 128 \
  --morphology-id specimen_479770916 \
  --output rows/teacher-qc.jsonl \
  --summary-output rows/teacher-qc.md
```

The rows report the teacher voltage distribution, spike counts and rates, the input event fraction, and the distortion that clipping at −55 mV introduces, overall and near spikes. The command reads the first `--max-samples` traces of `val` in manifest order; `--morphology-id` labels the rows. `--mode intervention` writes the corresponding teacher response rows for one [intervention condition](/axobench/interventions/#inspect-the-teacher-response).

`axobench benchmark-v1` runs the whole teacher bundle: QC rows for `val`, routing rows for the five [morphologies](/axobench/morphologies/), intervention rows for every condition and morphology, and morphology-contrast rows across morphologies. It writes JSONL rows, Markdown summaries, and a `manifest.json` to `--output-dir`. `--suite` selects `teacher-qc`, `paper-summary`, or `full`.

## Write model diagnostic rows

Beyond the bounded panel, `evaluate_model_diagnostic_rows` scores a model on supplied arrays and returns tidy rows for trace fidelity, state-conditioned dynamics, spike behavior, feature fidelity, and mechanistic response:

```python
from axobench.benchmark import (
    DiagnosticContext,
    evaluate_model_diagnostic_rows,
    write_diagnostic_rows,
)

indices = range(16)
inputs, targets = val.get_batch(indices)
rows = evaluate_model_diagnostic_rows(
    predict,
    inputs,
    targets,
    context=DiagnosticContext(
        suites=("paper-summary",),
        model_id="candidate-17",
        morphology_id="specimen_479770916",
        calibrated_spike_threshold=0.0,
    ),
    trace_ids=val.get_sample_ids(indices),
    raw_soma_mv=val.get_optional_array_batch("soma_mv", indices),
)
write_diagnostic_rows(rows, "rows/candidate-17.csv")
```

Pass a threshold calibrated on separate traces. `run_v1_benchmark_bundle(model_fn=predict, ...)` adds these model rows and model intervention rows to the teacher bundle. `morphology_contrast_diagnostic_rows` turns rows from several morphologies into mean, spread, and range across morphologies.

Every row has the columns `diagnostic`, `suite`, `model_id`, `teacher_id`, `morphology_id`, `split`, `condition`, `intervention`, `trace_id`, `state`, `metric`, `value`, `unit`, and `n`, plus the target view, `ignore_start`, and calibrated threshold. `write_diagnostic_rows` writes `.json`, `.jsonl`, or `.csv`, and `write_diagnostic_summary` writes a Markdown or JSON summary. The rows load directly into a dataframe.

## Select diagnostic suites

A suite is a named set of diagnostics; a row is kept when its diagnostic belongs to one of the requested suites.

| Diagnostic | Suites | Content |
| --- | --- | --- |
| `teacher_distribution_qc` | teacher-qc, paper-summary, full | Teacher voltage and spike distribution |
| `clipping_distortion` | teacher-qc, trace-core, paper-summary, full | Raw versus clipped target distortion |
| `morphology_routing_qc` | teacher-qc, paper-summary, full | Morphology and routing features |
| `trace_core` | trace-core, paper-summary, full | Trace fidelity, SERA, subthreshold RMSE, spike discrimination, count, and timing |
| `state_dynamics` | state-dynamics, paper-summary, full | State- and regime-conditioned errors |
| `spike_behavior` | spike-behavior, paper-summary, full | Spike calibration, counts, F1 timing, and threshold behavior |
| `feature_fidelity` | feature-fidelity, full | Electrophysiology-style features |
| `mechanistic_response` | mechanistic-response, paper-summary, full | Phase plane, event-triggered responses, history-conditioned error |
| `intervention_response` | teacher-qc, intervention-response, paper-summary, full | Paired response deltas |
| `morphology_contrast` | morphology-contrast, paper-summary, full | Differences across morphologies |

`axobench dataset-schema --kind diagnostics` prints the complete catalog, including audit diagnostics derived from saved comparison artifacts and the plotters attached to each diagnostic.

## Next steps

Return to [benchmarking](/axobench/benchmarking/) for the evaluation protocol, or see the [diagnostics API](/axobench-api/diagnostics/) for every argument.
