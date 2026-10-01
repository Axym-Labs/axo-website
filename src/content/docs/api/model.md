---
title: Branch-ELM compatibility
description: Signatures, parameters, return contracts, and source for branch-elm compatibility.
section: API reference
order: 207
---

## Module contract

BranchELM and BranchELMConfig provide the baseline and checkpoint-compatible branched neuron implementation. Inputs use (batch, time, input_channels); the standard two-channel readout contains a spike logit and a soma target coordinate.

Source revision: `306a51ed950b`. [Public export index](/api/).

## BranchELMConfig

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model.py#L10-L20)

```python
BranchELMConfig(input_dim: int = 1278, memory_units: int = 30, num_branches: int = 32, hidden_units: int = 64, synapse_decay: float = 0.85, memory_decay: float = 0.9) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `input_dim` | `int` | `1278` |
| `memory_units` | `int` | `30` |
| `num_branches` | `int` | `32` |
| `hidden_units` | `int` | `64` |
| `synapse_decay` | `float` | `0.85` |
| `memory_decay` | `float` | `0.9` |

`input_dim`: Native input-channel count.

### BranchELMConfig.branch_elm_30

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model.py#L19-L20)

```python
@classmethod
branch_elm_30(cls, *, input_dim: int=1278, num_branches: int=32) -> 'BranchELMConfig'
```

| Parameter | Type | Default |
| --- | --- | --- |
| `input_dim` | `int` | `1278` |
| `num_branches` | `int` | `32` |

`input_dim`: Native input-channel count.

Returns `'BranchELMConfig'`.

## BranchELM

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model.py#L23-L74)

Branch-factorized recurrent surrogate with spike and soma outputs.

Bases: `nn.Module`.

### BranchELM.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model.py#L26-L46)

```python
__init__(self, config: BranchELMConfig) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `config` | `BranchELMConfig` | required |

Returns `None`.

### BranchELM.forward

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model.py#L48-L71)

```python
forward(self, x: torch.Tensor) -> torch.Tensor
```

x must be (B,T,config.input_dim). Returns (B,T,2), with one spike logit and one soma target coordinate per step. Synaptic and memory states start at zero for each call.

| Parameter | Type | Default |
| --- | --- | --- |
| `x` | `torch.Tensor` | required |

Returns `torch.Tensor`.

### BranchELM.parameter_count

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model.py#L73-L74)

```python
parameter_count(self) -> int
```

Returns `int`.
