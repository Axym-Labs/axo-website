---
title: Datasets
description: Download population and intervention releases and preserve the input and target contracts.
section: Evaluation and deployment
order: 100
---

## Select the data domain

| Dataset | Use |
| --- | --- |
| Ordinary AxoBench | Primary single-neuron fidelity evaluation under the AxoBench metric protocol |
| [AxoBench Population](https://huggingface.co/datasets/Axym-Labs/axobench-population) | Population-context training and evaluation |
| [AxoBench Interventions](https://huggingface.co/datasets/Axym-Labs/axobench-interventions) | Matched intervention responses and mechanistic analysis |

Population contexts, ordinary traces, and intervention pairs represent different distributions. Report which release and split you use, and retain the manifest and shard hashes with derived results.

## Download the population and intervention releases

Install the Hugging Face CLI, then download each release separately:

```bash
python -m pip install -U huggingface_hub
hf download Axym-Labs/axobench-population \
  --repo-type dataset \
  --local-dir data/axobench-population
hf download Axym-Labs/axobench-interventions \
  --repo-type dataset \
  --local-dir data/axobench-interventions
```

Download the population release when fitting responses under population context, and the intervention release when comparing a response before and after a defined intervention. Keeping those directories separate makes the data domain explicit in subsequent commands. Consult each card and manifest before feeding arrays into a model; a Hugging Face checkout is not automatically a NeuronIO shard directory accepted by every trainer.

## Preserve the tensor conventions

Single-neuron inputs use `(batch, time, input_channels)` and targets use `(batch, time, 2)`. Population contact inputs use `(population, time, contacts)`. Preserve channel identity, event sign, sampling cadence, morphology identity, target coordinate conversion, and causal padding rules through preprocessing.

The NeuronIO converter supports raw pickle input and deterministic shard output. The [data reference](/api/data/) documents sharded, deterministic-window, random-window, and official-style full-trace datasets; [conversion reference](/api/neuronio/) documents the voltage and spike conversion path.

## Keep splits independent

The population comparison described in the report uses 80 released training contexts, with 64 for fitting and 16 for selecting a family recipe, while the 20 released validation contexts are reserved for final evaluation. The fixed comparison budget is 30,000 presentations per model. Preserve context identity across splitting so overlapping windows from one context do not leak into final evaluation.

A new study may choose a different protocol, but it should state its context partition, recipe-selection boundary, presentation budget, and target-domain metrics. The [evaluation guide](/evaluation/) describes paired ordinary-AxoBench comparisons.

## Next steps

Use [training](/training/) to fit traces, [inference-time adaptation](/adaptation/) to fit population banks, or [evaluation](/evaluation/) to measure fidelity.
