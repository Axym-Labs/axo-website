---
title: Dataset-relative skill
description: Express SERA against a constant reference and the best prediction without action potentials, and compare datasets on a common firing-rate distribution.
section: AxoBench metrics
order: 142
---

Voltage SERA in mV² per teacher spike has no natural scale, and its value depends on the dataset as much as on the model. AxoBench 0.2.1 adds secondary rows that express SERA as skill against references computed on the same traces, and a reweighting that compares datasets on a common firing-rate distribution.

## Why raw SERA does not transfer

[Voltage SERA](/axobench/metrics/#voltage-sera) weights each squared error by the relevance of the teacher voltage, fitted on the scored block, and divides the area by the block's teacher spikes. Both the relevance and the share of the trace that lies in action potentials depend on the teacher's firing rate and voltage distribution. Two blocks with different spike rates therefore give different values for models of equal quality, and a value such as 4,690 mV²/spike does not say whether a model is good.

A skill score divides out the scale: `1 − SERA(model) / SERA(reference)` is 1 for a perfect prediction, 0 for one no better than the reference, and negative for a worse one. The reference must use the same relevance and spike count as the model, so the ratio of SERA values is a ratio of relevance areas.

## The constant reference

The reference prediction is a constant voltage: the mean teacher voltage, clipped at −55 mV, over the scored steps of the calibration traces (`sera_reference_voltage`). It uses no scored trace, so it is fixed before any model is scored. In the worked example below it is −67.3 mV.

`voltage_sera_skill` is the Voltage SERA skill against this constant, and `dynamics_sera_skill` is the [Dynamics SERA](/axobench/metrics/#dynamics-sera) analogue. A constant has zero rate of change, so the Dynamics reference area is the relevance-weighted squared teacher rate of change.

## The AP-free ceiling

Voltage SERA is dominated by action-potential windows, where the teacher voltage is extreme. The teacher clipped at −55 mV, `min(V, −55 mV)`, is exact everywhere except above −55 mV. For any prediction that stays at or below −55 mV, each step's error is at least that of the clipped teacher: below −55 mV the clipped teacher is exact, and above it no such prediction comes closer than −55 mV. The clipped teacher is therefore the best prediction without action potentials, and its skill, `voltage_sera_ceiling_skill`, bounds the skill of every such prediction.

Models that do not emit action potentials, for example because they were trained on the clipped NeuronIO target coordinate, stay near this ceiling. The ceiling depends only on the teacher traces, so it is the same for every model on a block, and its difference in a paired comparison is zero.

The ceiling falls as the firing rate rises, because a larger share of the relevance area lies in action potentials. In the [error anatomy](/axobench/error-anatomy/#skill-by-firing-rate-and-morphology) of the worked example, it is 0.73 for traces firing below 1 Hz and 0.42 for traces above 6 Hz; the AxoBench README reports 0.48 on the AxoBench confirmation block and about 0.72 on the NeuronIO test set.

## Skill as a fraction of the ceiling

`voltage_sera_skill_of_ceiling` divides the Voltage SERA skill by the ceiling. It is 1 for a model as good as the best AP-free prediction and exceeds 1 only for a model that reproduces part of the action-potential waveform. It removes the rate dependence of the ceiling, not that of the model: a model that also fails more often at high rates, as in the example below, still shows a lower fraction there.

## Subthreshold skill

The `subthreshold_skill` row, present since 0.2.0, is `1 − RMSE / RMSE_null` of the [subthreshold voltage RMSE](/axobench/metrics/#subthreshold-voltage-rmse), where the null prediction is each trace's mean clipped teacher voltage over its retained steps. It is a ratio of root-mean-square errors, whereas the SERA skills are ratios of squared-error areas, so their values are not on the same scale: a subthreshold skill of 0.5 corresponds to a squared-error ratio of 0.25.

## Worked example

AxoSim–GRU Medium on the confirmation block of `val`, with the evaluator settings of its cache (`validation_sample_start=120`, 120 traces balanced over morphologies, `calibration_fraction=0.2`, so 96 scored traces):

```python
import numpy as np
from axobench.benchmark import EvaluationConfig, evaluate_predictions

with np.load("runs/gru-medium/axobench-evaluation-cache.npz") as cache:
    prediction = cache["prediction"]
with np.load("runs/confirmation-block-targets.npz") as block:
    target, raw_soma_mv = block["target"], block["raw_soma_mv"]
    trace_ids = [str(i) for i in block["trace_ids"]]

report = evaluate_predictions(
    prediction, target, raw_soma_mv=raw_soma_mv, trace_ids=trace_ids,
    config=EvaluationConfig(calibration_fraction=0.2),
)
for row in report["metrics"]:
    if "skill" in row["id"]:
        print(f"{row['id']} {row['value']:.3f}")
```

```text
subthreshold_skill 0.671
voltage_sera_skill 0.423
voltage_sera_ceiling_skill 0.483
voltage_sera_skill_of_ceiling 0.875
dynamics_sera_skill 0.050
```

The model's Voltage SERA, 4,690 mV²/spike, is 42% below that of the constant. The best prediction without action potentials reaches 48%, so the model attains 0.875 of what is possible without action potentials. Its voltage channel does not produce the action-potential waveform, as the [spike-triggered voltage](/axobench/error-anatomy/#spike-triggered-voltage) shows, which is why its skill stays below the ceiling. The Dynamics SERA skill of 0.050 is close to zero: the relevant rates of change are the action-potential upstroke and repolarization, which the model does not reproduce.

## Compare datasets on a common rate distribution

The fraction of the ceiling still depends on how a model handles each firing rate, and two datasets differ in their mix of rates. `reweight_to_rate_distribution` recomputes the skills of an [error anatomy](/axobench/error-anatomy/) with each trace weighted by the reference share of its rate bin (0–1, 1–3, 3–6, 6+ Hz) divided by its own share. The reference is another anatomy, whose shares are used, or a mapping from bin label to share:

```python
import json
from axobench.benchmark import reweight_to_rate_distribution

with open("runs/gru-medium/anatomy/error-anatomy.json") as source:
    anatomy = json.load(source)
low_rate = reweight_to_rate_distribution(anatomy, {"0-1": 0.5, "1-3": 0.5})
for key in ("voltage_sera_skill", "voltage_sera_ceiling_skill", "voltage_sera_skill_of_ceiling"):
    print(key, round(anatomy["overall"][key], 3), round(low_rate[key], 3))
print(low_rate["bins"])
```

```text
voltage_sera_skill 0.423 0.6
voltage_sera_ceiling_skill 0.483 0.625
voltage_sera_skill_of_ceiling 0.875 0.96
['0-1', '1-3']
```

Restricted to an even mix of traces below 3 Hz, the same predictions reach skill 0.60, ceiling 0.63, and 0.96 of the ceiling. Bins that the reference lacks receive weight zero, so the comparison covers only the rates both datasets contain; a bin that the reference weights but the anatomy lacks raises `ValueError`. Choose the reference over the common support and report it. The relevance, the constant reference, and the action-potential windows stay those of the anatomy's own block: reweighting changes how traces are pooled, not how they are scored.

## Use the skill rows

- All four SERA skill rows are ratios of per-trace sums, so they are pooled over traces like SERA and included in the [paired bootstrap](/axobench/benchmarking/#compare-with-a-baseline). Higher is better in comparisons.
- Report the Voltage SERA skill with its ceiling or its fraction of the ceiling. Raw skill alone mixes model quality with the dataset's spike rate.
- Compare values across datasets only on a common rate distribution, and state the bins and shares used.
- The skill rows are secondary. Voltage SERA, spike Mean F1, the subthreshold RMSE, and Response SERA remain the [core metrics](/axobench/metrics/).

## Next steps

Find where the remaining error lies with the [error anatomy](/axobench/error-anatomy/), or look up `sera_skill_trace_terms` and `sera_skills` in the [metric API](/axobench-api/metrics/).
