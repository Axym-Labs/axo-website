---
title: Choose a dataset
description: Match the single-neuron, population, and intervention releases to training, selection, and evaluation questions.
section: AxoBench
order: 130
---

## Compare the releases

AxoBench releases three datasets on Hugging Face. They share one input and target contract: native 1 ms samples, 1,278 signed event channels (639 excitatory, then 639 inhibitory), and a `(time, 2)` target of spike indicator and normalized somatic voltage. They differ in where the inputs come from and therefore in the question they answer.

| Dataset | Content | Use |
| --- | --- | --- |
| [Single-neuron traces](/axobench/single-neuron/) | 125,000 traces of 6,000 ms from five layer-5 pyramidal morphologies, in train, validation, and test splits | Pretraining, recipe selection, and the ordinary AxoBench evaluation |
| [Population contexts](/axobench/population/) | 50,000 traces of 1,200 ms whose inputs come from 100 connected AxoSim networks; five excitatory teachers and one inhibitory teacher | Fine-tuning and evaluation under recurrent input statistics |
| [Paired interventions](/axobench/interventions/) | 12,500 baseline and intervention pairs in five input-intervention conditions | Response fidelity and mechanistic analysis |

AxoBench follows the packaging and target coordinate of [NeuronIO](/axobench/neuronio/), an earlier single-neuron corpus, which can be converted to the same shard format. These pages describe the current v1 releases.

## Match the dataset to the question

**Train a single-neuron model.** Fit on the single-neuron `train` split. Select the architecture, recipe, checkpoint, and spike threshold on `val`, and evaluate the final choice once on `test`. An unreleased confirmation set is held separately from the public splits.

**Compare a candidate with a baseline.** Use the [AxoBench evaluator](/axobench/benchmarking/) on `val`. It scores the [core metrics](/axobench/metrics/), calibrates the spike threshold on a separate part of the selected traces, and reports paired differences with bootstrap intervals.

**Measure the response to an input change.** Add the intervention pairs to the evaluation root. The evaluator then reports Response SERA, which compares the predicted change in voltage with the teacher's change.

**Prepare a model for recurrent deployment.** Fine-tune and evaluate on the population contexts, splitting by context. Trace metrics on these inputs do not establish recurrent validity; connected-population measurements remain necessary.

**Test transfer to an unseen morphology.** No split withholds a morphology: every split contains all five. Build leave-one-morphology-out partitions from the sample IDs as described in [morphologies](/axobench/morphologies/).

## Assemble an evaluation root

The evaluator reads `<root>/val` and, if present, every condition directory under `<root>/interventions`. Download only the validation split of the single-neuron release, then place the intervention release inside the same root:

```bash
python -m pip install -U huggingface_hub
hf download Axym-Labs/axobench --repo-type dataset \
  --include "val/*" \
  --local-dir data/axobench
hf download Axym-Labs/axobench-interventions --repo-type dataset \
  --local-dir data/axobench/interventions
```

The first command transfers 2.65 GB of validation shards and the second 5.86 GB of intervention files. The complete single-neuron release adds 21.2 GB for `train` and 2.65 GB for `test`; the population release is 1.59 GB. Download a split with `--include "train/*"` or `--include "test/*"` when you need it.

## Preserve the conventions

Single-neuron inputs use `(batch, time, input_channels)` and targets use `(batch, time, 2)`. AxoSim's population interface uses contact inputs shaped `(population, time, contacts)`, which are a different representation from the 1,278-channel dataset inputs. Preserve channel identity, event sign, sampling cadence, morphology identity, target coordinate conversion, and causal padding rules through preprocessing. The [data reference](/api/data/) documents AxoSim's sharded and windowed readers; the [conversion reference](/api/neuronio/) documents the voltage and spike conversion path.

Population contexts, ordinary traces, and intervention pairs represent different input distributions. Report which release and split you use, and retain the manifest and shard hashes with derived results.

## Next steps

Read the page for the selected dataset, then [benchmark a model](/axobench/benchmarking/). AxoSim users can continue with [training](/training/), [inference-time adaptation](/adaptation/), or [evaluation](/evaluation/).
