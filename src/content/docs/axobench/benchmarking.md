---
title: Benchmarking with AxoBench
description: Evaluate any prediction function under the AxoBench protocol, read the report, and compare models on paired traces.
section: AxoBench metrics
order: 145
---

## Install AxoBench

AxoBench needs Python 3.10 or newer and depends only on NumPy, Matplotlib, and Requests; it does not import a model framework.

```bash
python -m pip install "axobench>=0.2.1"
```

These pages describe AxoBench 0.2.1. Since 0.2.0, it defines SERA as the IRon-default relevance area per teacher spike and replaces Dynamics SERA in the core set with the subthreshold voltage RMSE; earlier versions report different quantities under similar names. Record the installed version, for example with `importlib.metadata.version("axobench")`, alongside every result. A source checkout installs with `python -m pip install -e .`; the source repository currently requires access.

## Supply a prediction function

The evaluator calls a function on batches of NumPy inputs and expects NumPy outputs of the same batch and time length:

| | Shape | Content |
| --- | --- | --- |
| Input | `float32[batch, time, 1278]` | Signed events, excitatory channels first |
| Output channel 0 | `[batch, time]` | Spike score; any score that increases with spike evidence, such as a logit |
| Output channel 1 | `[batch, time]` | Somatic voltage in the target coordinate `(V + 67.7 mV) / 10` |

The evaluator converts channel 1 back to millivolts with `V = 10 y − 67.7`. Predictions above the −55 mV clipping level are allowed and scored. A model that needs morphology identity declares it with an attribute and receives one sample-ID prefix per trace:

```python
import numpy as np

def predict(inputs: np.ndarray, *, morphology_ids) -> np.ndarray:
    # inputs: (batch, time, 1278); morphology_ids: e.g. ["specimen_479770916", ...]
    ...
    return outputs  # (batch, time, 2)

predict.supports_morphology_ids = True
```

Without the attribute, the evaluator calls `predict(inputs)`. AxoSim checkpoints become prediction functions through `make_checkpoint_predictor`, which handles device placement, dtype, and the morphology vocabulary; see the [AxoSim prediction adapter](/api/axobench/).

## Evaluate a model

Assemble an evaluation root with `val` and, optionally, `interventions` as described in [choose a dataset](/datasets/#assemble-an-evaluation-root). Then:

```python
from axobench.benchmark import (
    evaluate_model,
    format_evaluation_report,
    write_evaluation_report,
)

report = evaluate_model(
    predict,
    dataset_root="data/axobench",
    model_id="candidate-17",
    multiple_morphologies=True,
)
print(format_evaluation_report(report))
write_evaluation_report(report, "runs/candidate-17.json")
```

`evaluate_model` streams inputs in batches and retains only predictions, targets, unclipped voltage, and per-step excitatory and inhibitory event counts. Its defaults define the iteration profile:

| Setting | Default | Effect |
| --- | --- | --- |
| `max_samples` | 120 | Validation traces of the alphabetically first morphology, or of `morphology_id`. With `multiple_morphologies=True`, 24 from each of the five |
| `max_intervention_samples` | 40 | Pairs per intervention condition, divided among morphologies in multiple-morphology mode |
| `max_interventions` | 8 | Condition directories read from `<root>/interventions`, in sorted order |
| `EvaluationConfig.ignore_start` | 500 | Initial steps excluded from every metric |
| `EvaluationConfig.calibration_fraction` | 0.25 | Share of the selected traces used only to set the spike threshold |
| `EvaluationConfig.f1_tolerances_steps` | `(0, 1, 2, 3, 4, 5)` | Timing tolerances of the spike F1 curve |
| `batch_size` | 128 | Traces per prediction call |

Trace-level variation differs between morphologies, so confirmation runs can raise `max_samples` and `max_intervention_samples`.

## Calibration and scoring

The evaluator orders the selected traces round-robin by morphology and splits them in that order. The first quarter, here 30 traces, is the calibration block; the remaining 90 are scored. On the calibration block it sets the spike threshold to the score of the k-th highest timestep after `ignore_start`, where k is the number of teacher spike timesteps in the same block. Every metric is then computed on the scored traces only, with that fixed threshold. The action-potential windows of the subthreshold RMSE are computed from the teacher traces of the whole block, so they are identical for every model scored on it.

`EvaluationConfig.default_spike_threshold` does not set the threshold. It enters only the `default_threshold_count` diagnostic, which checks how many spikes an uncalibrated threshold would produce. `axosim-evaluate-model` sets it to 0, a logit of zero.

For model selection followed by an untouched confirmation, evaluate the selection block with `validation_sample_start=0` and the confirmation block with `validation_sample_start=120`, using the same `max_samples`. In multiple-morphology mode the start indexes the balanced order, so both blocks remain balanced. The start is recorded in the report and in cache protocols, so paired comparisons cannot mix blocks.

## Score stored predictions

`evaluate_predictions` applies the same protocol to arrays. Use it for predictions computed elsewhere or for a split other than `val`. Order the traces so that the calibration block contains every morphology. This example scores the first 24 test traces of each morphology:

```python
import numpy as np
from axobench.data import ShardedNeuronIODataset
from axobench.benchmark import evaluate_predictions, format_evaluation_report

dataset = ShardedNeuronIODataset("data/axobench/test", cache_shards=1)
ids = dataset.get_sample_ids(range(len(dataset)))
groups = {}
for index, trace_id in enumerate(ids):
    groups.setdefault(trace_id.split(":", 1)[0], []).append(index)
selected = sorted(index for members in groups.values() for index in members[:24])

predictions, targets, soma_mv, event_counts, trace_ids = [], [], [], [], []
for start in range(0, len(selected), 32):
    batch = selected[start : start + 32]
    inputs, batch_targets = dataset.get_batch(batch)
    predictions.append(predict(inputs))
    targets.append(batch_targets)
    soma_mv.append(dataset.get_optional_array_batch("soma_mv", batch))
    event_counts.append(np.stack([(inputs > 0).sum(-1), (inputs < 0).sum(-1)], axis=-1))
    trace_ids += dataset.get_sample_ids(batch)

# Interleave morphologies so the calibration block contains each of them.
position, keys = {}, []
for trace_id in trace_ids:
    morphology = trace_id.split(":", 1)[0]
    keys.append((position.get(morphology, 0), morphology))
    position[morphology] = position.get(morphology, 0) + 1
order = sorted(range(len(trace_ids)), key=keys.__getitem__)

report = evaluate_predictions(
    np.concatenate(predictions)[order],
    np.concatenate(targets)[order],
    inputs=np.concatenate(event_counts)[order],
    raw_soma_mv=np.concatenate(soma_mv)[order],
    trace_ids=[trace_ids[index] for index in order],
    model_id="candidate-17",
)
print(format_evaluation_report(report))
```

Selecting indices in sorted order keeps each shard to one read. `inputs` takes the compact per-step event counts used by the input-conditioned diagnostics; full input arrays are not needed. Pass `interventions=` a list of `PairedInterventionPredictions` to include Response SERA.

## Read the report

The terminal report has a header with the model, sample counts, calibrated threshold, morphologies, and runtime, followed by a fixed table of metrics, the action-potential window ends, and the 24-row [attention panel](/axobench/diagnostics/#read-the-attention-panel).

| Metric ID | Unit | Role |
| --- | --- | --- |
| `voltage_sera_iron_per_spike_mv2` | mV²/spike | Core: [Voltage SERA](/axobench/metrics/#voltage-sera) |
| `subthreshold_rmse_mv` | mV | Core: [subthreshold voltage RMSE](/axobench/metrics/#subthreshold-voltage-rmse) |
| `spike_mean_f1_0_5ms` | fraction | Core: [Mean F1](/axobench/metrics/#spike-f1) over 0–5 ms |
| `spike_f1_area_0_5ms` | fraction | Trapezoidal F1 area, a compatibility view |
| `spike_f1_exact`, `spike_f1_5ms` | fraction | F1 at 0 ms and 5 ms |
| `response_sera_iron_per_spike_mv2` | mV²/spike | Core: [Response SERA](/axobench/metrics/#response-sera), pooled over conditions |
| `subthreshold_skill` | skill | Secondary: improvement over the per-trace mean voltage |
| `dynamics_sera_iron_per_spike_mv2_per_ms2` | mV²/ms²/spike | Secondary: [Dynamics SERA](/axobench/metrics/#dynamics-sera) |
| `voltage_sera_skill` | skill | Secondary: Voltage SERA skill against a [constant voltage](/axobench/skill/#the-constant-reference) |
| `voltage_sera_ceiling_skill` | skill | Secondary: skill of the teacher clipped at −55 mV, the [AP-free ceiling](/axobench/skill/#the-ap-free-ceiling) |
| `voltage_sera_skill_of_ceiling` | ratio | Secondary: Voltage SERA skill as a [fraction of the ceiling](/axobench/skill/#skill-as-a-fraction-of-the-ceiling) |
| `dynamics_sera_skill` | skill | Secondary: Dynamics SERA skill against the constant voltage |

The returned dictionary also contains the full F1 curve with precision, recall, and event counts per tolerance, one record per intervention condition, every diagnostic with its trigger and basis, and the selection settings. `write_evaluation_report` writes it as strict JSON or as tidy CSV rows of type `metric`, `diagnostic`, and `intervention`, selected by the file suffix.

## Compare with a baseline

Evaluate the baseline once, save its predictions, and compare every candidate against that cache:

```python
from axobench.benchmark import (
    create_model_evaluation_cache,
    evaluate_model_against_cache,
    format_model_comparison,
    write_model_comparison,
    write_model_evaluation_cache,
)

cache = create_model_evaluation_cache(
    baseline_predict,
    dataset_root="data/axobench",
    model_id="baseline",
    multiple_morphologies=True,
)
write_model_evaluation_cache(cache, "runs/baseline-cache.npz")

comparison = evaluate_model_against_cache(
    predict,
    baseline_cache="runs/baseline-cache.npz",
    dataset_root="data/axobench",
    candidate_id="candidate-17",
    multiple_morphologies=True,
)
print(format_model_comparison(comparison))
write_model_comparison(comparison, "runs/candidate-17-vs-baseline.csv")
```

The cache is a compressed, pickle-free `.npz` with the baseline predictions, intervention predictions and targets, ordered trace IDs, a SHA-256 hash of the targets, the baseline report, and the protocol: sample limits, morphology selection, intervention names, sample start, and the complete `EvaluationConfig`. The comparison fails unless the candidate's protocol, ordered trace IDs, and target hash all match. `compare_predictions` computes the same paired comparison from arrays that you have already aligned.

Each metric row reports the candidate value, the baseline value, their difference, a 95% interval, and an assessment. The interval comes from a paired bootstrap with 250 replicates and seed 20260711 by default:

- Scored traces are resampled with replacement within each morphology, and both models are evaluated on the same resample.
- Each model keeps its calibrated threshold, and the relevance weights and action-potential windows stay at their full-sample values.
- Response SERA resamples pairs within each condition and morphology and pools conditions as summed relevance area per summed teacher spike count.
- The interval spans the 2.5% and 97.5% quantiles of the replicate differences.

A metric is `improved` or `regressed` when the interval excludes zero in the preferred direction, which is lower for SERA and RMSE and higher for F1 and skill, and `uncertain` otherwise. The interval measures trace-sampling uncertainty for fixed predictions. It does not include variation between training runs, so compare several seeds when that is the question. The labels are evidence for a decision, not a promotion rule.

## Use the command line

The `axobench` command converts and inspects data and writes [diagnostic rows](/axobench/diagnostics/); it does not load models. For AxoSim checkpoints, `axosim-evaluate-model` wraps `evaluate_model`, `create_model_evaluation_cache`, and `evaluate_model_against_cache`; [evaluate models](/evaluation/) shows the commands. For other frameworks, call the Python functions above with your prediction function.

## Report a result

State the AxoBench version, dataset and split, sample limits and start, morphology mode, intervention conditions, `ignore_start`, calibration fraction, and the bootstrap settings. Report Voltage SERA, subthreshold RMSE, Response SERA, and Mean F1 with the tolerance grid. No single metric captures every biologically relevant error; the [metric definitions](/axobench/metrics/) explain what each one isolates.

## Next steps

Read the [metric definitions](/axobench/metrics/), explain a model's errors with the [error anatomy](/axobench/error-anatomy/), inspect the [attention panel and diagnostics](/axobench/diagnostics/), or look up exact signatures in the [AxoBench API](/axobench-api/).
