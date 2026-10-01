---
title: Troubleshooting
description: Diagnose checkpoint, population, sparse-event, CUDA capture, and evaluation mismatches.
section: Evaluation and deployment
order: 120
---

## Checkpoint loading fails

<aside class="error-callout"><code>ValueError: unknown model_kind in checkpoint: {model_kind}</code></aside>

<aside class="error-callout"><code>TypeError: unsupported checkpoint model type: {type(model).__name__}</code></aside>

Check the saved `model_kind` and architecture configuration against the installed source. Official and PyTorch Mamba backends have different state-dictionary formats. Reconstruct through `load_checkpoint`, preserve the recorded backend, and install the optional fused backend when required. See [checkpoint API](/api/checkpoint/) and [installation](/installation/).

Historical checkpoints may contain retired configuration fields handled by the loader. An unknown model kind still raises an error; replacing the kind string does not establish weight compatibility. These templates come from the [checkpoint loader and saver](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/checkpoint.py#L320).

## A backend or evaluator is missing

<aside class="error-callout"><code>ImportError: mamba-ssm is required for BranchOfficialMamba. Use the mamba-official venv or install a compatible mamba-ssm wheel.</code></aside>

<aside class="error-callout"><code>RuntimeError: AxoBench with the model-iteration evaluator is required; install the current axobench package</code></aside>

Install the fused backend when the checkpoint records an official Mamba model kind. To evaluate the AxoBench core metrics, install the current AxoBench package into the same Python environment as the AxoSim commands. The fallback backend has a different checkpoint format, so installing it does not replace a missing fused dependency. See [installation](/installation/) and the source checks for [Mamba](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L123) and [AxoBench](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axobench_iteration.py#L254).

## Population shapes do not match

<aside class="error-callout"><code>ValueError: contact_inputs must have shape {expected}</code></aside>

<aside class="error-callout"><code>ValueError: contact_inputs must have shape (batch, population, time, contacts)</code></aside>

<aside class="error-callout"><code>ValueError: contact branch index lies outside the model</code></aside>

For dense input, verify `(N, T, K)` against the population's persistent neuron and contact counts. For batches, verify `(B, N, T, K)`. Morphology indices require one index per persistent neuron, and branch indices require `(N, K)` values within the Lite input width. Route features require `(morphologies, input_dim, route_feature_dim)`.

The [population guide](/populations/) defines these dimensions. A new batch axis shares the existing population banks; it does not change the persistent neuron count.

## Sparse events are rejected

<aside class="error-callout"><code>ValueError: sparse contact event tensors must have equal length</code></aside>

<aside class="error-callout"><code>ValueError: event summary and contact indices must address the same target neuron</code></aside>

<aside class="error-callout"><code>ValueError: sparse contact event tensors must share the model device</code></aside>

Ensure all three event arrays are one-dimensional and have the same length. Both index arrays must use integer dtypes, event values must be floating point, and all tensors must share the population device. Decode each index and confirm that `summary_index // T == contact_index // K`. Check timestep and contact bounds before calling the module.

The [sparse-event guide](/sparse-events/) provides a valid four-event example and explains gradient and memory behavior.

## CUDA Graph replay fails

<aside class="error-callout"><code>RuntimeError: CUDA Graph adaptation requires CUDA</code></aside>

<aside class="error-callout"><code>ValueError: inputs must have shape {expected_inputs}</code></aside>

<aside class="error-callout"><code>ValueError: inputs must have dtype {self.static_inputs.dtype}</code></aside>

Replays must match the captured input and target shapes and dtypes. Keep the captured module, optimizer groups, parameter allocations, and static buffers valid. Use a capturable optimizer, then recapture after structural changes. New source input tensors are copied into the helper's static buffers.

Validate the eager path first and compare successive eager and captured updates from identical states. See [CUDA Graphs](/cuda-graphs/) for capture's state-restoration behavior.

## Voltage or spike metrics look inconsistent

<aside class="error-callout"><code>ValueError: prediction and target must match with shape (trace, time, 2), got {pred.shape} and {tgt.shape}</code></aside>

<aside class="error-callout"><code>ValueError: conditioned checkpoint requires one morphology ID per input sample</code></aside>

Verify the voltage target coordinates before comparing predictions with millivolt traces. The standard NeuronIO conversion includes clipping and normalization; applying its inverse transform twice changes the voltage error. Calibrate spike thresholds only on the declared development or calibration partition.

These messages identify incompatible prediction/target shapes or absent morphology context. A wrong voltage conversion can also change metrics without raising an exception. Use the [AxoBench evaluation path](/evaluation/) to preserve the metric protocol. SERA and Root-SERA are different presentations; confirm the field and units rather than taking an undocumented square root. The shape template is checked in [AxoBench](https://github.com/Axym-Labs/axobench/blob/6c10504e0c7d52ae4c9921b28186be7b72a8407a/src/axobench/benchmark/iteration_evaluator.py#L607).

## Evaluation caches cannot be paired

<aside class="error-callout"><code>ValueError: baseline cache protocol does not match candidate evaluation</code></aside>

<aside class="error-callout"><code>ValueError: baseline cache trace selection does not match candidate evaluation</code></aside>

<aside class="error-callout"><code>ValueError: baseline cache targets do not match candidate evaluation</code></aside>

Compare target hashes, ordered trace identities, calibration boundaries, and metric configuration. A shared directory and matching sample count are insufficient. Evaluate candidate and baseline on a common block if those identities differ, then save the new baseline cache.

The three checks are separate because each fixes a different part of the comparison: the metric/calibration protocol, the selected trace order, and the target values. They are enforced by [AxoBench's cache comparison](https://github.com/Axym-Labs/axobench/blob/6c10504e0c7d52ae4c9921b28186be7b72a8407a/src/axobench/benchmark/iteration_evaluator.py#L412).

If the issue remains, include a reproducing command or script and the metadata listed in [reproducibility](/reproducibility/). That information distinguishes data or backend mismatches from discrepancies in the model or metric implementation. Braced values in the callouts are placeholders filled by the source at runtime, not literal exception text.
