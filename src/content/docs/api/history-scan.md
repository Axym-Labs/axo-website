---
title: Supplied-history scan
description: Process complete Mamba input histories with explicit fused or sequential backend reporting.
section: API reference
apiGroup: Populations
order: 203
---

## Overview

Process one or more complete native input histories through a provided Mamba1 model. All neuron rows share its weights; the function partitions neurons when requested while preserving each complete time sequence. The [supplied-history guide](/history-scan/) provides runnable single-neuron, population and gradient checks. For continuing streams, use the model's streaming API; for delayed network feedback, use [connected population rollout](/connected-populations/).

This reference describes `axosim.history_scan`. [Repository access](/installation/#install-axosim) is currently required to inspect the source. [Export index](/api/).

<section class="api-symbol" id="history-scan-scan-histories">

## scan_histories

<div class="api-signature">

```python
axosim.scan_histories(
    model: BranchOfficialMamba,
    inputs: torch.Tensor,
    *,
    morphology_indices: torch.Tensor | None = None,
    neuron_batch_size: int | None = None,
    require_parallel: bool = True,
) -> HistoryScanResult
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/history_scan.py#L30-L94)

</div>

Evaluate complete histories with fresh temporal state, retaining autograd and the caller's training/evaluation mode. The default requires the official fused CUDA Mamba1 full-sequence path. An explicitly permitted portable model reports sequential execution; this option never replaces a checkpoint's architecture or weights.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">BranchOfficialMamba</span></dt>
<dd><span class="api-default">required.</span> Provided AxoMamba or Branch-routed Mamba1 model, including the portable AxoPyTorchMamba reference. Official execution requires the actual <code>mamba_ssm</code> Mamba1 blocks and enabled fused kernels. GRU, Lite, Mamba2 and unrelated custom block implementations are unsupported. The function neither moves the model nor changes its mode or weights.</dd>
<dt><code>inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Floating tensor <code>(N, T, C)</code> with positive <code>N</code> and <code>T</code> and <code>C == model.num_input</code>. One neuron uses <code>N=1</code>. Supply the checkpoint's native channel order, input convention and sampling cadence on the model's device. No dtype or device conversion occurs. Official kernels accept float16, bfloat16 or float32 inputs; use a dtype compatible with the model's weights.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">default=None.</span> Integer tensor <code>(N,)</code> indexing <code>model.config.morphology_ids</code>, with each value in <code>[0, len(morphology_ids))</code>. Required when the model declares that vocabulary; omit it for an unconditioned model. Indices are sliced with their matching neuron rows. The underlying model places the indices on its execution device.</dd>
<dt><code>neuron_batch_size</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">default=None.</span> Positive integer maximum rows per forward call; <code>None</code> processes all rows together. Only <code>N</code> is partitioned, with the complete <code>T</code> sequence retained in each partition. Output order remains the input order. This limits intermediate per-forward memory, not the size of the complete returned predictions or retained autograd graph.</dd>
<dt><code>require_parallel</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span> Require the enabled official CUDA fused temporal scan. Set <code>False</code> to accept the sequential portable PyTorch Mamba1 model; official checkpoints still require their CUDA backend. Inspect <code>result.backend</code> for the actual path.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>HistoryScanResult</code></dt>
<dd><code>prediction</code> is a tensor <code>(N, T, model.num_output)</code> in the provided model's output coordinates, with its derivative graph retained when gradient tracking is enabled. <code>backend</code> describes the path that executed. No streaming state, recurrent events or new graph topology are returned.</dd>
</dl>

<p class="api-label">Execution and sequence boundaries</p>

Each call invokes full-sequence model forward from its initial state. Separate calls on time chunks do not continue one another. The function does not generate future network inputs from emitted spikes: those inputs must already be present in the supplied histories. It also does not impose <code>eval()</code> or disable gradients; use <code>model.eval()</code> and <code>torch.inference_mode()</code> for inference. Training-mode stochastic layers retain their usual behavior, so comparisons across different neuron batch sizes should use evaluation mode when testing numerical parity. Batch partitioning can also change floating-point results; strict CUDA FP32 comparisons require consistent TF32 settings and appropriate numerical tolerances, not bitwise equality. The function does not change those settings.

<p class="api-label">Raises</p>

| Exception | Condition and source message |
| --- | --- |
| `TypeError` | Unsupported model: `scan_histories requires an AxoSim or Branch-routed Mamba model` |
| `TypeError` | Non-tensor input: `inputs must be a torch.Tensor` |
| `TypeError` | Non-boolean parallel flag: `require_parallel must be a bool` |
| `ValueError` | Wrong rank: `inputs must have shape (neurons, time, input_channels)`; empty neuron/time dimension: `inputs must have non-empty neuron and time dimensions` |
| `ValueError` | Wrong width: `inputs must have num_input={model.num_input} channels`; non-floating input: `inputs must have a floating-point dtype` |
| `ValueError` | Invalid batch size: `neuron_batch_size must be a positive integer or None` |
| `ValueError` | Device mismatch: `inputs and model parameters must be on the same device` |
| `ValueError` | Missing conditioning: `morphology_indices are required for a morphology-conditioned model`; unnecessary conditioning: `morphology_indices were provided to an unconditioned model` |
| `ValueError` | Invalid morphology tensor: `morphology_indices must have shape (neurons,)`, `morphology_indices must have an integer dtype`, or `morphology_indices must be in range [0, {len(ids)})` |
| `RuntimeError` | Unsupported Mamba variant: `scan_histories currently supports only the Mamba1 history backend` |
| `RuntimeError` | Sequential path rejected: `require_parallel=True rejects the sequential PyTorch Mamba reference; use an official CUDA Mamba model or explicitly set require_parallel=False` |
| `RuntimeError` | Official dependency missing: `The official Mamba1 fused CUDA backend is unavailable`; unsupported blocks: `The model does not contain the supported official Mamba1 blocks` |
| `RuntimeError` | Official model on CPU: `Official Mamba1 history scan requires CUDA inputs and model; require_parallel=False does not replace checkpoint backends` |
| `ValueError` | Unsupported official input precision: `Official Mamba1 scan requires float16, bfloat16 or float32 inputs` |
| `RuntimeError` | Fast path disabled: `Official Mamba1 history scan requires use_fast_path=True in every block` |
| `RuntimeError` | Kernels unavailable: `Official Mamba1 fused selective-scan or causal-convolution kernels are unavailable` |

Errors raised by the model or dependencies during forward are propagated. See [installation](/installation/) for the official CUDA dependencies.

</section>

<section class="api-symbol" id="history-scan-historyscanbackend">

## HistoryScanBackend

<div class="api-signature">

```python
axosim.HistoryScanBackend(name: str, parallel: bool, reason: str)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/history_scan.py#L14-L19)

</div>

Frozen execution metadata returned with a scan. This describes the provided model's validated execution path, rather than a requested backend preference.

<p class="api-label">Attributes</p>

<dl class="api-attributes">
<dt><code>name: str</code></dt>
<dd><code>official-mamba1-fused</code> for official Mamba1's enabled fused CUDA path, or <code>pytorch-sequential-reference</code> for the explicitly permitted portable implementation.</dd>
<dt><code>parallel: bool</code></dt>
<dd>True for the fused temporal scan; false for the portable recurrence evaluated sequentially in time. Neuron batching alone does not make this value true.</dd>
<dt><code>reason: str</code></dt>
<dd>Source explanation of the selected path: <code>Official Mamba1 full-sequence mamba_inner_fn with fused CUDA selective scan and causal convolution.</code> or <code>Portable PyTorch Mamba evaluates the state recurrence sequentially in time.</code></dd>
</dl>

All constructor fields are required. The dataclass's attributes cannot be reassigned.

</section>

<section class="api-symbol" id="history-scan-historyscanresult">

## HistoryScanResult

<div class="api-signature">

```python
axosim.HistoryScanResult(prediction: torch.Tensor, backend: HistoryScanBackend)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/history_scan.py#L23-L27)

</div>

Predictions and validated execution metadata for complete supplied histories.

<p class="api-label">Attributes</p>

<dl class="api-attributes">
<dt><code>prediction: torch.Tensor</code></dt>
<dd>Model predictions <code>(N, T, model.num_output)</code>, ordered like the input neuron rows. Standard two-output models return spike logits and soma-target coordinates. The function does not threshold spikes, convert soma units, detach derivatives or clone the tensor into an immutable snapshot.</dd>
<dt><code>backend: HistoryScanBackend</code></dt>
<dd>Actual fused or sequential execution path, including its explanatory reason.</dd>
</dl>

Both constructor fields are required. The dataclass's attributes cannot be reassigned; its prediction tensor retains normal PyTorch mutability and autograd semantics. It contains no continuation state.

</section>
