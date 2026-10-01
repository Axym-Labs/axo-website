---
title: Checkpoints
description: Signatures, parameters, return contracts, and source for checkpoints.
section: API reference
order: 208
---

## Module contract

Checkpoint files contain model_kind, config, state_dict, and metadata. save_checkpoint writes a temporary sibling then atomically replaces the destination. Model-only checkpoints do not store a complete optimizer or scheduler trajectory. load_checkpoint uses torch.load with weights_only=False, so load trusted artifacts.

Source revision: `306a51ed950b`. [Public export index](/api/).

## save_checkpoint

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/checkpoint.py#L188-L206)

```python
save_checkpoint(model: torch.nn.Module, path: str | Path, *, metadata: dict[str, Any] | None=None) -> None
```

Writes model kind, serializable configuration, state_dict, and metadata. Creates parent directories. Unsupported model types raise TypeError. Returns None.

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `torch.nn.Module` | required |
| `path` | `str \| Path` | required |
| `metadata` | `dict[str, Any] \| None` | `None` |

`metadata`: Caller metadata stored with model state.

Returns `None`.

## load_checkpoint

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/checkpoint.py#L209-L329)

```python
load_checkpoint(path: str | Path, *, map_location: str='cpu') -> tuple[torch.nn.Module, dict[str, Any]]
```

Returns (reconstructed torch.nn.Module, metadata dictionary). Supports baseline/branch_elm, official, branch-trace-rnn, axomamba and axomamba-pytorch, axo-temporal variants, axo-block-forecast variants, adaptive P4 variants, and generic Mamba kinds. An unknown kind raises ValueError; PyTorch artifacts are loaded with weights_only=False.

| Parameter | Type | Default |
| --- | --- | --- |
| `path` | `str \| Path` | required |
| `map_location` | `str` | `'cpu'` |

`map_location`: PyTorch destination for loaded tensors.

Returns `tuple[torch.nn.Module, dict[str, Any]]`.
