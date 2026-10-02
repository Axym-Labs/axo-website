---
title: CUDA Graph adaptation
description: Signatures, parameters, return contracts, and source for cuda graph adaptation.
section: API reference
apiGroup: Training and evaluation
order: 211
---

## Overview

CudaGraphAdaptationStep captures one fixed-shape forward, loss, backward, optional gradient transform, and optimizer update. It restores module and optimizer state after warmup and capture. Replay copies source tensors into retained static buffers. CUDA inputs and optimizer parameters are required; shape, dtype, parameter groups, and allocations must remain compatible.

Source revision: `0f546adfd8fc`. [Public export index](/api/).

<section class="api-symbol" id="adaptation-cudagraphadaptationstep">

## CudaGraphAdaptationStep

<div class="api-signature">

```python
axosim.adaptation.CudaGraphAdaptationStep(module: nn.Module, optimizer: torch.optim.Optimizer, static_inputs: torch.Tensor, static_targets: torch.Tensor, graph: torch.cuda.CUDAGraph, static_loss: torch.Tensor)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/adaptation.py#L55-L169)

</div>

A captured full-forward, backward, and optimizer update.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>module</code> <span class="api-type">nn.Module</span></dt>
<dd><span class="api-default">required.</span> Module whose forward execution participates in the captured update.</dd>
<dt><code>optimizer</code> <span class="api-type">torch.optim.Optimizer</span></dt>
<dd><span class="api-default">required.</span> Optimizer attached to the selected parameters.</dd>
<dt><code>static_inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>static_targets</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>graph</code> <span class="api-type">torch.cuda.CUDAGraph</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>static_loss</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as attributes.

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#adaptation-cudagraphadaptationstep-capture"><code>CudaGraphAdaptationStep.capture()</code></a></li>
<li><a href="#adaptation-cudagraphadaptationstep---call--"><code>CudaGraphAdaptationStep.__call__()</code></a></li>
</ul>

<section class="api-method" id="adaptation-cudagraphadaptationstep-capture">

### CudaGraphAdaptationStep.capture

<div class="api-signature">

```python
@classmethod
axosim.adaptation.CudaGraphAdaptationStep.capture(module: nn.Module, optimizer: torch.optim.Optimizer, example_inputs: torch.Tensor, example_targets: torch.Tensor, loss_function: TensorLoss, *, warmup_steps: int=3, gradient_transform: GradientTransform | None=None) -> 'CudaGraphAdaptationStep'
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/adaptation.py#L66-L141)

</div>

Capture a fixed-shape adaptation update without consuming it.

module and optimizer parameters must be CUDA-resident; example_inputs and example_targets establish fixed shape/dtype. loss_function(prediction,targets) must return a scalar differentiable tensor. gradient_transform is a zero-argument callable executed after backward. Returns a captured step while restoring pre-capture module/optimizer values.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>module</code> <span class="api-type">nn.Module</span></dt>
<dd><span class="api-default">required.</span> Module whose forward execution participates in the captured update.</dd>
<dt><code>optimizer</code> <span class="api-type">torch.optim.Optimizer</span></dt>
<dd><span class="api-default">required.</span> Optimizer attached to the selected parameters.</dd>
<dt><code>example_inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> CUDA tensor establishing the input shape, dtype, and static buffer for capture.</dd>
<dt><code>example_targets</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> CUDA tensor establishing the target shape, dtype, and static buffer for capture.</dd>
<dt><code>loss_function</code> <span class="api-type">TensorLoss</span></dt>
<dd><span class="api-default">required.</span> Callable receiving predictions and targets and returning a differentiable scalar loss.</dd>
<dt><code>warmup_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=3.</span> Warmup updates executed and restored during capture.</dd>
<dt><code>gradient_transform</code> <span class="api-type">GradientTransform | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional zero-argument gradient transform after backward.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>step</code> <span class="api-type">CudaGraphAdaptationStep</span></dt>
<dd>Captured update with retained static buffers; warmup/capture changes to stored module and optimizer values have been restored.</dd>
</dl>

</section>

<section class="api-method" id="adaptation-cudagraphadaptationstep---call--">

### CudaGraphAdaptationStep.__call__

<div class="api-signature">

```python
axosim.adaptation.CudaGraphAdaptationStep.__call__(inputs: torch.Tensor, targets: torch.Tensor, *, synchronize: bool=False) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/adaptation.py#L143-L169)

</div>

Replay the captured adaptation update with new input and target values.

inputs and targets must match captured shapes and dtypes. Copies values to retained static CUDA buffers, replays the complete update, and returns a detached cloned scalar loss. synchronize=True waits for CUDA completion.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> New input values with exactly the captured shape, dtype, and CUDA device.</dd>
<dt><code>targets</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> New target values with exactly the captured shape, dtype, and CUDA device.</dd>
<dt><code>synchronize</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Wait for CUDA completion before returning.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>loss</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Detached cloned scalar loss from the replayed optimizer update.</dd>
</dl>

</section>

</section>
