---
title: Single-neuron traces
description: CoreNEURON traces from five layer-5 pyramidal morphologies for training and the ordinary AxoBench evaluation.
section: AxoBench
order: 131
---

## Contents

[`Axym-Labs/axobench`](https://huggingface.co/datasets/Axym-Labs/axobench) contains 125,000 traces of 6,000 ms, simulated with CoreNEURON on GPU. The teachers are five reconstructed mouse layer-5 pyramidal neurons from the Allen Cell Types Database, simulated with a Hay-compatible template and mechanisms; [morphologies](/axobench/morphologies/) lists them. Every trace has its own seeded sample of excitatory and inhibitory input events, and the somatic voltage and output spikes are recorded at 1 ms.

| Split | Traces | Per morphology | NPZ shards | Compressed size |
| --- | ---: | ---: | ---: | ---: |
| `train` | 100,000 | 20,000 | 785 | 21.2 GB |
| `val` | 12,500 | 2,500 | 100 | 2.65 GB |
| `test` | 12,500 | 2,500 | 100 | 2.65 GB |

Every split contains all five morphologies. An unreleased confirmation set is held separately and is not part of the Hugging Face repository.

## Shard format

Each split directory contains `.npz` shards of up to 128 traces, one JSON sidecar per shard, and a `manifest.json` that lists every shard with its trace count and sample IDs. `checksums.sha256` at the repository root covers every shard and sidecar.

| Array | Type and shape | Content |
| --- | --- | --- |
| `inputs` | `int8[trace, 6000, 1278]` | `+1` for an excitatory event on channels 0–638, `-1` for an inhibitory event on channels 639–1277, otherwise `0` |
| `targets` | `float32[trace, 6000, 2]` | Channel 0 is the binary spike indicator; channel 1 is the somatic voltage clipped at −55 mV, shifted by +67.7 mV, and divided by 10 |
| `soma_mv` | `float32[trace, 6000]` | Unclipped somatic voltage in millivolts |
| `sample_ids` | `str[trace]` | `specimen_<id>:split:<split>:<shard>:<index>:seed<seed>` |

The voltage target is the historical NeuronIO coordinate, `(min(V, −55 mV) + 67.7 mV) / 10`, so action-potential peaks are absent from `targets`. AxoBench scores voltage against `soma_mv` whenever it is present, which keeps the spike waveform in the measurement. The text before the first colon of a sample ID is the morphology identity used for balancing, stratification, and per-cell analysis.

## Channel coverage

The 1,278 channels follow NeuronIO's layout of 639 excitatory and 639 inhibitory synapse sites, and events are sampled on all of them. The five morphologies have fewer dendritic segments. Each basal or apical segment receives the source site of the same compartment type at the nearest normalized arc length, recorded as `normalized_by_type_arclength` in the sidecars. Source sites without a segment receive no synapse, so events on those channels do not reach the teacher.

| Morphology | Segments with a synapse, per sign | Source channels with a synapse, per sign | Source channels without a synapse, per sign |
| --- | ---: | ---: | ---: |
| `specimen_488683425` | 283 | 282 | 357 |
| `specimen_487664663` | 265 | 264 | 375 |
| `specimen_479770916` | 302 | 301 | 338 |
| `specimen_589427435` | 340 | 335 | 304 |
| `specimen_488679042` | 377 | 370 | 269 |

The values come from the `input_routing` record of the shard sidecars, which is identical for every trace of a morphology. A model therefore receives events on channels that carry no information for that morphology, and the informative set differs between morphologies. A morphology-conditioned model receives the identity that distinguishes the five channel maps; a model without it is trained on their mixture.

## Download and load

Download one split at a time:

```bash
python -m pip install -U huggingface_hub
hf download Axym-Labs/axobench --repo-type dataset \
  --include "val/*" \
  --local-dir data/axobench
```

Replace `val/*` with `train/*` or `test/*` for the other splits. The split directories are ordinary shard directories, readable by AxoBench and by the AxoSim trainer:

```python
from axobench.data import ShardedNeuronIODataset

val = ShardedNeuronIODataset("data/axobench/val", cache_shards=1)
inputs, targets = val.get_batch(range(4))
soma_mv = val.get_optional_array_batch("soma_mv", range(4))
print(len(val), inputs.dtype, inputs.shape, targets.shape, soma_mv.shape)
print(val.get_sample_ids([0])[0])
```

```text
12500 float32 (4, 6000, 1278) (4, 6000, 2) (4, 6000)
specimen_479770916:split:val:00671:0000:seed143761753
```

`get_batch` converts inputs to `float32`. Reading any trace decompresses the input array of its whole shard, about 0.98 GB as `int8` for 128 traces, so request indices grouped by shard and keep `cache_shards` small.

## Use the splits

Train on `train`, choose the recipe and spike threshold on `val`, and evaluate once on `test`. The AxoSim [training guide](/training/) uses these directories directly. The [AxoBench evaluator](/axobench/benchmarking/) reads `<root>/val`; [score stored predictions](/axobench/benchmarking/#score-stored-predictions) to evaluate the `test` split under the same protocol.

The AxoBench README states that the released datasets are licensed CC BY-NC 4.0: every trace is simulated on Allen Cell Types Database reconstructions, whose terms permit derived works for noncommercial purposes only.

## Next steps

Check teacher statistics with the [diagnostics](/axobench/diagnostics/#check-the-teacher), or add the [paired interventions](/axobench/interventions/) to the same root.
