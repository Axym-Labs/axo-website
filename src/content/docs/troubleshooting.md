---
title: Troubleshooting
description: Diagnose checkpoint, population, sparse-event, CUDA capture, and evaluation mismatches.
section: Evaluate and deploy
order: 120
---

## Checkpoint loading fails

Check the saved `model_kind` and architecture configuration against the installed source. Official and PyTorch Mamba backends have different state-dictionary formats. Reconstruct through `load_checkpoint`, preserve the recorded backend, and install the optional fused backend when required. See [checkpoint API](/api/checkpoint/) and [installation](/installation/).

Historical checkpoints may contain retired configuration fields handled by the loader. An unknown model kind still raises an error; replacing the kind string does not establish weight compatibility.

## Population shapes do not match

For dense input, verify `(N, T, K)` against the population's persistent neuron and contact counts. For batches, verify `(B, N, T, K)`. Morphology indices require one index per persistent neuron, and branch indices require `(N, K)` values within the Lite input width. Route features require `(morphologies, input_dim, route_feature_dim)`.

The [population guide](/populations/) defines these dimensions. A new batch axis shares the existing population banks; it does not change the persistent neuron count.

## Sparse events are rejected

Ensure all three event arrays are one-dimensional and have the same length. Both index arrays must use integer dtypes, event values must be floating point, and all tensors must share the population device. Decode each index and confirm that `summary_index // T == contact_index // K`. Check timestep and contact bounds before calling the module.

The [sparse-event guide](/sparse-events/) provides a valid four-event example and explains gradient and memory behavior.

## CUDA Graph replay fails

Replays must match the captured input and target shapes and dtypes. Keep the captured module, optimizer groups, parameter allocations, and static buffers valid. Use a capturable optimizer, then recapture after structural changes. New source input tensors are copied into the helper's static buffers.

Validate the eager path first and compare successive eager and captured updates from identical states. See [CUDA Graphs](/cuda-graphs/) for capture's state-restoration behavior.

## Voltage or spike metrics look inconsistent

Verify the voltage target coordinates before comparing predictions with millivolt traces. The standard NeuronIO conversion includes clipping and normalization; applying its inverse transform twice changes the voltage error. Calibrate spike thresholds only on the declared development or calibration partition.

Use the [AxoBench evaluation path](/evaluation/) to preserve the metric protocol. SERA and Root-SERA are different presentations; confirm the field and units rather than taking an undocumented square root.

## Evaluation caches cannot be paired

Compare target hashes, ordered trace identities, calibration boundaries, and metric configuration. A shared directory and matching sample count are insufficient. Evaluate candidate and baseline on a common block if those identities differ, then save the new baseline cache.

## Report the remaining issue

Include a reproducing command or script and the metadata listed in [reproducibility](/reproducibility/). That information distinguishes data or backend mismatches from discrepancies in the model or metric implementation.
