---
title: NeuronIO compatibility
description: Convert NeuronIO simulations to AxoBench shards and account for the differences in metrics and channel meaning.
section: AxoBench datasets
order: 134
---

## Shared contract

NeuronIO is an earlier single-neuron corpus of one layer-5 pyramidal cell model with 639 excitatory and 639 inhibitory synapse sites. AxoBench adopts its packaging and conventions, so a converted NeuronIO directory can be read, trained on, and scored with the same tools:

- 1,278 input channels at 1 ms, excitatory sites first with value `+1` and inhibitory sites second with value `-1`;
- targets shaped `(time, 2)`: a spike indicator and the somatic voltage clipped at −55 mV, shifted by +67.7 mV, and divided by 10;
- `.npz` shards with `inputs`, `targets`, and `sample_ids`, listed in a `manifest.json`.

The two corpora are not interchangeable. Their teachers, input routing, and stored arrays differ, and these differences change what the metrics measure.

## Convert raw simulations

The raw NeuronIO release is distributed through Kaggle. `axosim-setup --install-kaggle --download-data` downloads its training and test archives to `data/raw/nmda-train` and `data/raw/nmda-test`, as described in [installation](/installation/#inspect-data-setup-before-running-it). Convert a directory of raw simulation files, which follow the upstream `*sim__*` naming:

```bash
axobench convert-neuronio \
  --input data/raw/nmda-test \
  --output data/neuronio-root/val
```

The converter writes shards of 128 simulations named `neuronio_00000.npz`, with sample IDs `<raw file stem>:<simulation index>`. `--window-size` and `--window-stride` cut each simulation into windows with IDs ending in `@<start>`; with windowing, `--ignore-start` sets the first window start. `axosim convert-neuronio` performs the same conversion. The [evaluator](/axobench/benchmarking/) scores the shards it finds in `<root>/val`, so writing the converted test simulations there makes `data/neuronio-root` a valid evaluation root.

## Differences that affect evaluation

| Property | AxoBench single-neuron traces | Converted NeuronIO |
| --- | --- | --- |
| Teachers | Five Allen reconstructions, CoreNEURON | One layer-5 pyramidal cell model |
| Unclipped voltage | `soma_mv` stored with every trace | Not stored; only the clipped target |
| Channels with a synapse | 264–370 source channels per sign, depending on morphology | Every channel corresponds to a synapse site |
| Sample-ID prefix | Morphology, `specimen_<id>` | Raw file stem |

Without `soma_mv`, AxoBench reconstructs the teacher voltage from the clipped target. Voltage SERA, Dynamics SERA, the subthreshold RMSE, and the voltage rows of the attention panel then compare against a teacher whose action potentials are cut at −55 mV, and the action-potential windows of the subthreshold RMSE use the fixed fallback end of 4 steps. Values computed this way are not comparable with values computed against `soma_mv`.

The evaluator treats the text before the first colon of a sample ID as the morphology. For converted NeuronIO this is the raw file stem, so `multiple_morphologies=True` balances over source files, the bootstrap stratifies by source file, and the morphology-disparity row compares files rather than cells.

A model trained on NeuronIO learns a channel map in which every channel reaches a synapse. On AxoBench, a morphology-dependent subset of channels has no synapse ([channel coverage](/axobench/single-neuron/#channel-coverage)). Evaluate such a model on the target corpus before drawing conclusions about transfer.

## Evaluate Branch-ELM checkpoints

AxoSim's `make_official_elm_predictor` loads an upstream Branch-ELM checkpoint as an AxoBench prediction function on the same target coordinate; see the [prediction adapter reference](/api/axobench/). Score it with the evaluator like any other predictor.

## Next steps

Use [choose a dataset](/datasets/) to decide between the corpora, or [benchmark a model](/axobench/benchmarking/) on the converted root.
