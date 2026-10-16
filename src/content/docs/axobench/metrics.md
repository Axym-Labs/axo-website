---
title: Core metrics
description: Definitions and rationale for Voltage SERA, spike F1, the subthreshold voltage RMSE, and Response SERA.
section: AxoBench metrics
order: 140
---

## Metric set

AxoBench 0.2.1 reports four core metrics, the same set as 0.2.0. Each isolates a different error, and no single one captures every biologically relevant difference between a model and its teacher.

| Metric | Measures | Better |
| --- | --- | --- |
| [Voltage SERA](#voltage-sera) | Voltage error weighted toward extreme teacher voltages, dominated by action potentials | Lower, mV²/spike |
| [Spike F1](#spike-f1) | Recovery of output spike times at 0–5 ms tolerance | Higher |
| [Subthreshold voltage RMSE](#subthreshold-voltage-rmse) | Voltage offset, gain, and post-spike error outside action potentials | Lower, mV |
| [Response SERA](#response-sera) | Error in the voltage change caused by an input intervention | Lower, mV²/spike |

[Dynamics SERA](#dynamics-sera), the subthreshold skill, and the [dataset-relative SERA skill rows](/axobench/skill/) are secondary rows. All metrics are computed on the scored traces after the first `ignore_start` steps, as described in [benchmarking](/axobench/benchmarking/#calibration-and-scoring).

## Voltage coordinates

A prediction's voltage channel `y` is converted to millivolts as `V̂ = 10 y − 67.7`. The teacher voltage `V` is the stored unclipped `soma_mv` when available; otherwise it is reconstructed from the target in the same way and is therefore clipped at −55 mV. The metrics below use the unclipped teacher unless stated.

## Voltage SERA

SERA is the squared error-relevance area of Ribeiro and Moniz (2020), computed with the default relevance function of their IRon package. It weights errors by how extreme the teacher value is, so the rare action potentials and deep hyperpolarizations are not averaged away by the subthreshold majority of samples.

1. **Relevance.** From all scored teacher voltages pooled, compute the adjusted-boxplot fences of Hubert and Vandervieren (2008). With quartiles `Q1`, `Q3`, interquartile range `IQR`, and medcouple `mc`, the fences are `Q1 − 1.5 e^(−4 mc) IQR` and `Q3 + 1.5 e^(3 mc) IQR` for `mc ≥ 0`, mirrored for `mc < 0`. The relevance `φ` is 1 at and beyond either fence, 0 at the median, and follows the cubic `3t² − 2t³` between them.
2. **Area.** For a threshold `t`, `SER(t)` is the sum of squared errors `(V̂ − V)²` over samples with `φ ≥ t`. SERA integrates `SER(t)` over `t` from 0 to 1 with the trapezoid rule on a grid of step 0.001. Equivalently, each sample's squared error is weighted by the area of the thresholds it passes, which reaches 1 at `φ = 1`.
3. **Normalization.** The area is divided by the number of teacher spikes in the scored region, which makes values comparable across trace counts and lengths.

The relevance function depends on the scored teacher traces, so a paired comparison on one block holds it fixed. AxoBench reproduces IRon's default `phi.control` settings, extremes on both sides with coefficient 1.5, and computes the medcouple exactly. A block without teacher spikes has no defined value.

## Spike F1

Spike F1 compares predicted and teacher spike events with one-to-one matching.

- **Predicted events** are local maxima of the spike score at or above the calibrated threshold. A step is a maximum if its score exceeds the previous step and is not below the next. Maxima are kept from the highest score down, and a kept event suppresses other maxima within 2 steps, so a run of high scores counts as one spike.
- **Teacher events** are the steps marked in the target's spike channel.
- **Matching.** Within each trace, events are paired in time order when they lie within the tolerance `τ` of each other; each event is matched at most once. True positives, false positives, and false negatives are summed over all scored traces, and `F1 = 2 TP / (2 TP + FP + FN)`.

F1 is computed for `τ = 0, 1, 2, 3, 4, 5` ms. **Mean F1** is the arithmetic mean of these six values, so each tolerance has equal weight and the score is higher-is-better. The report also lists the exact (0 ms) and 5 ms values and the trapezoidal area over the tolerance interval, which is retained as a compatibility view.

## Subthreshold voltage RMSE

Voltage SERA is dominated by spike timing near action potentials, and F1 scores only event times. The subthreshold RMSE measures what both miss: voltage offset, gain, and errors after spikes such as afterhyperpolarization.

- **Excluded windows.** Every step from 2 steps before to `L` steps after a teacher spike or a predicted spike event is excluded. Excluding the predicted events as well prevents spike-timing errors from being counted twice.
- **Window end.** `L` is set per cell type, the sample-ID prefix. AxoBench averages the teacher waveform around isolated spikes, those without another teacher spike in the following 30 steps, and sets `L` to the first lag at which this mean waveform changes by less than 1 mV per 1 ms step. Repolarization and the fast afterhyperpolarization last until 4 to 9 ms after the spike depending on the cell, so a fixed end would score part of the spike waveform as subthreshold. With fewer than 20 isolated spikes, no flat lag, or no unclipped voltage, `L` is 4. The ends are computed from the teacher traces of the whole evaluated block and printed in the report.
- **Value.** Both voltages are clipped at −55 mV. The RMSE pools squared errors over the retained steps of all scored traces. The **subthreshold skill** is `1 − RMSE / RMSE_null`, where the null prediction is each trace's mean clipped teacher voltage over its retained steps.

## Response SERA

Response SERA scores the [paired interventions](/axobench/interventions/). For each pair, the teacher response is `ΔV = V_intervention − V_baseline` and the predicted response is the same difference of the model's two predictions. The error is the predicted minus the teacher response.

Relevance is fitted on the pooled teacher responses of a condition, so large teacher changes carry the weight. The relevance area of the response error is divided by the number of teacher spikes in the baseline and intervention traces. The core metric pools conditions as the summed area over the summed spike count. Per condition, the report adds the response skill, `1 − area / area_zero`, where `area_zero` scores a model that predicts no change with the same relevance; the fraction of samples with a teacher change of at least 0.5 mV whose predicted change has the same sign; and the least-squares gain of the predicted on the teacher response.

## Dynamics SERA

Dynamics SERA applies the Voltage SERA construction to the one-step voltage change, in mV/ms, with relevance fitted on the teacher's rate of change. It is reported per teacher spike in mV²/ms² and has been a secondary metric since AxoBench 0.2.0. Its skill against a constant voltage is the `dynamics_sera_skill` row.

## Relation to the technical report

<!-- TODO(v2 retraining): once the report's ordinary-AxoBench results use AxoBench 0.2 metrics, shorten this section. -->
The AxoSim [technical report](/report/main.pdf) uses these metrics for its central figure and its dataset-relative comparison: SERA per teacher spike with IRon-default relevance, the subthreshold voltage error, and spike Mean F1. Its ordinary-AxoBench results still use an earlier definition, SERA as a support-normalized integral over 101 relevance thresholds in mV², with Dynamics SERA in the core set; those values are not comparable with AxoBench 0.2's. Report the AxoBench version with every value.

## Compute metrics on arrays

`compute_core_metric_set` returns the metric set for arrays you have already aligned. It does not separate calibration and scoring traces: without `spike_threshold` it chooses the threshold on the same traces so that the predicted event count equals the teacher spike count. Pass a threshold calibrated elsewhere, or use [`evaluate_predictions`](/axobench/benchmarking/#score-stored-predictions) for the full protocol. Scoring the clipped target as a prediction shows the effect of the target coordinate:

```python
from axobench.data import ShardedNeuronIODataset
from axobench.metrics import compute_core_metric_set

val = ShardedNeuronIODataset("data/axobench/val", cache_shards=1)
indices = range(8)
_, targets = val.get_batch(indices)
result = compute_core_metric_set(
    targets,
    targets,
    raw_soma_mv=val.get_optional_array_batch("soma_mv", indices),
    trace_ids=val.get_sample_ids(indices),
    ignore_start=500,
    spike_threshold=0.5,
)
print(f"{result['spike_mean_f1']:.3f} {result['subthreshold_rmse_mv']:.3f}",
      result["voltage_sera_iron_per_spike_mv2"] > 0)
```

```text
1.000 0.000 True
```

The spike train and the clipped subthreshold voltage are exact, but Voltage SERA is positive because the target lacks the action-potential peaks that `soma_mv` contains.

## Next steps

Express SERA as [dataset-relative skill](/axobench/skill/), break errors down with the [error anatomy](/axobench/error-anatomy/), use [diagnostics](/axobench/diagnostics/) to test how these metrics respond to controlled defects, or see the [metric API](/axobench-api/metrics/) for every function and its arguments.
