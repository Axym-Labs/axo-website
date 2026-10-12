---
title: Paired interventions
description: Matched baseline and intervention traces that measure how a model's response changes with its input.
section: AxoBench datasets
order: 133
---

## Contents

[`Axym-Labs/axobench-interventions`](https://huggingface.co/datasets/Axym-Labs/axobench-interventions) contains 12,500 pairs. Each pair simulates one input sample twice with the same teacher: once unchanged and once after a defined edit of its input events. The difference between the two teacher traces is the response that a model should reproduce. The release is separate from the single-neuron traces, so ordinary benchmark users do not download it.

| Condition | Edit of the baseline input | Pairs | NPZ shards |
| --- | --- | ---: | ---: |
| `event_dropout` | Every nonzero event is removed independently with probability 0.35 | 2,500 | 40 |
| `exc_dropout` | Excitatory (`+1`) events are removed with probability 0.35 | 2,500 | 40 |
| `inh_dropout` | Inhibitory (`-1`) events are removed with probability 0.35 | 2,500 | 40 |
| `temporal_jitter` | Every event moves by an integer shift drawn uniformly from −2 to +2 ms, clipped to the trace | 2,500 | 40 |
| `site_silence` | Events on source sites 0–159, 25% of the 639 sites, are removed in both the excitatory and inhibitory halves | 2,500 | 40 |

Each condition has 500 pairs per morphology for the five morphologies of the [single-neuron release](/axobench/single-neuron/), with 6,000 ms traces. The parameters are the v1 defaults of the AxoBench generator. Jittered events that land on the same channel and step merge into one event. Because some source sites have no synapse on a given morphology ([channel coverage](/axobench/single-neuron/#channel-coverage)), `site_silence` removes a different number of effective synapses on each morphology.

## Shard format

Each condition directory holds the NPZ shards, one JSON sidecar per shard, and a `manifest.json` with sample IDs and shard counts. `checksums.sha256` covers the complete release.

| Array | Type and shape | Content |
| --- | --- | --- |
| `baseline_inputs`, `intervention_inputs` | `int8[pair, 6000, 1278]` | Signed events before and after the edit |
| `baseline_targets`, `intervention_targets` | `float32[pair, 6000, 2]` | Spike indicator and normalized somatic voltage |
| `baseline_soma_mv`, `intervention_soma_mv` | `float32[pair, 6000]` | Unclipped somatic voltage in millivolts |
| `changed_event_mask` | `bool[pair, 6000, 1278]` | Baseline events that the edit removed or moved |
| `sample_ids` | `str[pair]` | `specimen_<id>:intervention:<condition>:<shard>:<index>:seed<seed>` |

```python
from pathlib import Path
import numpy as np

shard = sorted(Path("data/axobench/interventions/site_silence").glob("*.npz"))[0]
with np.load(shard, allow_pickle=False) as pair:
    baseline = pair["baseline_inputs"]
    changed = pair["changed_event_mask"]
    response_mv = pair["intervention_soma_mv"] - pair["baseline_soma_mv"]
    sample_ids = pair["sample_ids"]
silenced = np.flatnonzero(changed.any(axis=(0, 1)))
print(baseline.shape, response_mv.shape, silenced[[0, 159, 160, -1]])
print(sample_ids[0])
```

```text
(64, 6000, 1278) (64, 6000) [  0 159 639 798]
specimen_479770916:intervention:site_silence:00763:0000:seed1271366164
```

## Add the pairs to an evaluation

Download the release into the `interventions` directory of the evaluation root:

```bash
hf download Axym-Labs/axobench-interventions --repo-type dataset \
  --local-dir data/axobench/interventions
```

The [evaluator](/axobench/benchmarking/) then predicts both inputs of each pair and scores the predicted change in voltage against the teacher's change.

- It discovers every condition directory in sorted order, up to `max_interventions` (default 8), or the names you pass as `intervention_names`.
- It loads `max_intervention_samples` pairs per condition (default 40). Single-morphology mode takes the first pairs of the selected morphology in file-name order; multiple-morphology mode divides the same number evenly among the morphologies found in the file names.
- The first `ignore_start` steps (default 500) are excluded. No pairs are used for spike-threshold calibration.
- The report contains [Response SERA](/axobench/metrics/#response-sera), pooled over conditions, and per condition the response skill against a zero-response prediction, the direction agreement on samples where the teacher changes by at least 0.5 mV, and the least-squares response gain. Three [attention rows](/axobench/diagnostics/#read-the-attention-panel) flag the worst condition for each quantity.

Pass `--interventions event_dropout,inh_dropout` to `axosim-evaluate-model`, or `intervention_names=` in Python, to fix the selection and keep the condition names in the report.

## Inspect the teacher response

Before comparing models, check that a condition changes the teacher measurably. This command writes teacher-only rows for one condition: event fractions, spike-rate and voltage deltas, a detected-response flag, and the direction label.

```bash
axobench benchmark-rows --mode intervention \
  --selector intervention --intervention event_dropout \
  --dataset-root data/axobench \
  --morphology-id specimen_479770916 \
  --max-samples 64 \
  --output rows/event_dropout-teacher.jsonl
```

The command reads the first `--max-samples` pairs of the condition in file order, which belong to the alphabetically first morphology; `--morphology-id` only labels the rows. `axobench benchmark-v1` instead groups the pairs of every condition by morphology. [Diagnostics](/axobench/diagnostics/#check-the-teacher) describes both commands and the row format.

## Next steps

AxoSim users can study how adapted contacts and behavior parameters respond to these edits after [inference-time adaptation](/adaptation/). The [Response SERA definition](/axobench/metrics/#response-sera) explains how pairs are weighted.
