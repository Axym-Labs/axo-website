---
title: Train a model
description: Train from trace shards, select a development recipe, and save model weights and metadata.
section: Training and adaptation
order: 60
---

## Prepare training and validation data

The trainer reads NeuronIO-style shards with input and target arrays. Use a training split for optimization and a separate development split for selecting the recipe. Keep final test data untouched until architecture, hyperparameters, preprocessing, and spike calibration are fixed.

For a quick command-line smoke test, create synthetic shards:

```bash
axosim make-demo-data --output data/demo --samples 8 --shards 1
```

These deterministic synthetic targets test the pipeline; they do not establish biological fidelity. See [datasets](/datasets/) and the [data API](/api/data/) for real trace preparation and windowing contracts.

## Train with a named preset

From the AxoSim checkout, provide real training and validation shard directories:

```bash
axosim train \
  --preset axomamba-probe \
  --data data/full-trace-shards/nmda-train \
  --val-data data/full-trace-shards/nmda-val \
  --device cuda \
  --epochs 10 \
  --epoch-samples 80000 \
  --checkpoint runs/axosim-mamba.pt \
  --metrics runs/axosim-mamba-training.json
```

The example retains the report's named research preset and explicitly selects CUDA for its fused Mamba backend. `--epoch-samples` controls the number of training presentations per epoch, while `--epochs` controls how often that presentation budget is repeated. Change those values deliberately when comparing recipes so a longer run is not mistaken for an architectural improvement. Presets resolve architecture and training options, while explicitly supplied command-line options take precedence; the resolved configuration is recorded in the output metrics.

## Training artifacts

| Artifact | Content |
| --- | --- |
| Model checkpoint | Model kind, architecture configuration, weights, and metadata |
| Training metrics JSON | Resolved training settings and recorded measurements |
| Optional best checkpoint | A model selected using the supplied validation path |
| Experiment registry | A JSONL record, unless registry output is disabled |

The trainer creates parent directories and writes checkpoints atomically. A public model checkpoint contains model weights and metadata rather than the complete optimizer and scheduler state. To resume an optimization trajectory, save those states separately alongside the training step, random states, and data-order information required by your procedure.

## Choose a training recipe

Set the optimizer, learning-rate schedule, loss weights, batch size, and horizon using development data. The command supports Adam and AdamW, constant and cosine schedules, and separate spike and voltage loss terms. Windowing, burn-in, and the voltage-coordinate convention must agree with your targets.

The presets are starting recipes. A new morphology, sampling cadence, or channel convention requires validation and fresh calibration. The [CLI reference](/api/cli/) lists every option; the [training API](/api/training/) describes the Python functions and defaults.

## Adapt a fitted population

If the shared Lite response model is already trained, [inference-time adaptation](/adaptation/) optimizes smaller behavior, morphology, and synaptic banks. Full temporal gradients remain available through the ordinary PyTorch interface. [CUDA Graphs](/cuda-graphs/) can capture a fixed-shape update after you verify the eager training path.

## Next steps

Load the saved model in [inference](/inference/) and compute [AxoBench metrics](/evaluation/).
