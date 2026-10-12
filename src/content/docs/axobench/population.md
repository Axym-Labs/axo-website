---
title: Population contexts
description: Teacher responses to input histories recorded in connected AxoSim networks, split by network context.
section: AxoBench datasets
order: 132
---

## Contents

[`Axym-Labs/axobench-population`](https://huggingface.co/datasets/Axym-Labs/axobench-population) samples the input distribution that recurrent feedback produces. A thresholded AxoSim network generates branch-resolved input histories; detailed teachers of the matching cell type replay those histories to produce somatic voltage and spike labels. The labels are teacher responses to inputs recorded from the learned network, not a closed biophysical loop.

| Split | Contexts | Traces | Excitatory | Inhibitory | NPZ shards |
| --- | ---: | ---: | ---: | ---: | ---: |
| `train` | 80 | 40,000 | 32,000 | 8,000 | 480 |
| `val` | 20 | 10,000 | 8,000 | 2,000 | 120 |
| total | 100 | 50,000 | 40,000 | 10,000 | 600 |

Each trace has 1,200 native 1 ms steps on the common 1,278-channel input contract. The excitatory teachers are the five morphologies of the [single-neuron release](/axobench/single-neuron/); the inhibitory teacher is an Allen SST cell, `allen_sst_specimen_482690728`. Complete network contexts define the split, so no context contributes traces to both `train` and `val`. The release is 1.59 GB.

The release validator checked all 600 shards for schema, finite values, sample counts, role balance, manifest hashes, and disjoint context splits. This establishes package integrity; it does not show that a training recipe that improves trace metrics on these inputs also improves connected-population behavior.

## Shard format

Shards are named `excitatory__<morphology>__i<context>.npz` or `inhibitory__i<context>.npz`. Each split has a `manifest.json` with the schema, shard counts, sample IDs, and SHA-256 hashes.

| Array | Type and shape | Content |
| --- | --- | --- |
| `inputs` | `int8[trace, 1200, 1278]` | Signed input events, as in the single-neuron release |
| `targets` | `float32[trace, 1200, 2]` | Spike indicator and normalized somatic voltage |
| `soma_mv` | `float32[trace, 1200]` | Unclipped somatic voltage in millivolts |
| `context_index` | `int16[trace]` | Network context of the trace |
| `target_is_inhibitory` | `bool[trace]` | Teacher role |
| `target_role` | `str[trace]` | `excitatory` or `inhibitory` |
| `target_morphology` | `str[trace]` | Teacher morphology identity |
| `window_start_ms` | `int32[trace]` | Start of the 1,200 ms window |
| `sample_ids` | `str[trace]` | `<morphology>:population:<context iteration>:<target index>:<window start>:<role>` |

The shards also carry `target_population_index`, `context_iteration`, `context_seed`, `context_kind`, and `split`. The morphology prefix of each sample ID gives six identities, so AxoBench balances and stratifies over five excitatory morphologies and the SST teacher.

## Split by context

Traces from one context share its network and its activity history. Keep every partition at context granularity. The comparison in the [technical report](/report/main.pdf) uses 64 of the 80 training contexts for fitting, the remaining 16 for selecting one learning-rate schedule per architecture family, and the 20 validation contexts only for the final evaluation, with a fixed budget of 30,000 presentations per model. This partitions the training split by context:

```python
import numpy as np
from axobench.data import ShardedNeuronIODataset

train = ShardedNeuronIODataset("data/axobench-population/train")
contexts = train.get_optional_array_batch("context_index", range(len(train)))
rng = np.random.default_rng(0)
selection = rng.choice(np.unique(contexts), size=16, replace=False)
fit_indices = np.flatnonzero(~np.isin(contexts, selection))
select_indices = np.flatnonzero(np.isin(contexts, selection))
print(np.unique(contexts).size, fit_indices.size, select_indices.size)
```

```text
80 32000 8000
```

A new study may choose another partition. State the context partition, recipe-selection boundary, presentation budget, and target-domain metrics with the result.

## Download and evaluate

```bash
hf download Axym-Labs/axobench-population --repo-type dataset \
  --local-dir data/axobench-population
```

The validation split has the directory layout that the [AxoBench evaluator](/axobench/benchmarking/) reads, so `evaluate_model(predict, dataset_root="data/axobench-population", multiple_morphologies=True)` scores it under the same metric protocol. The default 500-step exclusion leaves 700 scored steps per trace; state it, or set `EvaluationConfig.ignore_start`, when you report results. In single-morphology mode the evaluator selects the alphabetically first identity, which here is the inhibitory SST teacher; pass `morphology_id` or `multiple_morphologies=True` deliberately. The release contains no intervention pairs, so Response SERA is unavailable.

## Trace fidelity is not recurrent validity

In the [technical report](/report/main.pdf), training on all 50,000 traces improved held-out Voltage SERA, Dynamics SERA, and spike F1, yet the connected model missed the morphology-conditioned firing-rate criterion on all three unseen connectomes. Use population-context metrics to select a model for this input distribution, and connected-population measurements to decide whether it behaves correctly in recurrent simulation.

## Next steps

Fine-tune a trained neuron model on these traces as part of [inference-time adaptation](/adaptation/), then simulate it in a [connected population](/connected-populations/).
