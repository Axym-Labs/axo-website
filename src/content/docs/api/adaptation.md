---
title: CUDA Graph adaptation
description: Signatures, parameters, return contracts, and source for cuda graph adaptation.
section: API reference
order: 209
---

## Module contract

CudaGraphAdaptationStep captures one fixed-shape forward, loss, backward, optional gradient transform, and optimizer update. It restores module and optimizer state after warmup and capture. Replay copies source tensors into retained static buffers. CUDA inputs and optimizer parameters are required; shape, dtype, parameter groups, and allocations must remain compatible.

Source revision: `306a51ed950b`. [Public export index](/api/).

## CudaGraphAdaptationStep

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/adaptation.py#L55-L169)

A captured full-forward, backward, and optimizer update.

```python
CudaGraphAdaptationStep(module: nn.Module, optimizer: torch.optim.Optimizer, static_inputs: torch.Tensor, static_targets: torch.Tensor, graph: torch.cuda.CUDAGraph, static_loss: torch.Tensor) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `module` | `nn.Module` | required |
| `optimizer` | `torch.optim.Optimizer` | required |
| `static_inputs` | `torch.Tensor` | required |
| `static_targets` | `torch.Tensor` | required |
| `graph` | `torch.cuda.CUDAGraph` | required |
| `static_loss` | `torch.Tensor` | required |

`optimizer`: Optimizer attached to the selected parameters.

### CudaGraphAdaptationStep.capture

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/adaptation.py#L66-L141)

```python
@classmethod
capture(cls, module: nn.Module, optimizer: torch.optim.Optimizer, example_inputs: torch.Tensor, example_targets: torch.Tensor, loss_function: TensorLoss, *, warmup_steps: int=3, gradient_transform: GradientTransform | None=None) -> 'CudaGraphAdaptationStep'
```

Capture a fixed-shape adaptation update without consuming it.

module and optimizer parameters must be CUDA-resident; example_inputs and example_targets establish fixed shape/dtype. loss_function(prediction,targets) must return a scalar differentiable tensor. gradient_transform is a zero-argument callable executed after backward. Returns a captured step while restoring pre-capture module/optimizer values.

| Parameter | Type | Default |
| --- | --- | --- |
| `module` | `nn.Module` | required |
| `optimizer` | `torch.optim.Optimizer` | required |
| `example_inputs` | `torch.Tensor` | required |
| `example_targets` | `torch.Tensor` | required |
| `loss_function` | `TensorLoss` | required |
| `warmup_steps` | `int` | `3` |
| `gradient_transform` | `GradientTransform \| None` | `None` |

`optimizer`: Optimizer attached to the selected parameters. `warmup_steps`: Warmup updates executed and restored during capture. `gradient_transform`: Optional zero-argument gradient transform after backward.

Returns `'CudaGraphAdaptationStep'`.

### CudaGraphAdaptationStep.__call__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/adaptation.py#L143-L169)

```python
__call__(self, inputs: torch.Tensor, targets: torch.Tensor, *, synchronize: bool=False) -> torch.Tensor
```

inputs and targets must match captured shapes and dtypes. Copies values to retained static CUDA buffers, replays the complete update, and returns a detached cloned scalar loss. synchronize=True waits for CUDA completion.

| Parameter | Type | Default |
| --- | --- | --- |
| `inputs` | `torch.Tensor` | required |
| `targets` | `torch.Tensor` | required |
| `synchronize` | `bool` | `False` |

`synchronize`: Wait for CUDA completion before returning.

Returns `torch.Tensor`.
