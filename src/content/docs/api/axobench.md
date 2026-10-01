---
title: AxoBench prediction adapters
description: Signatures, parameters, return contracts, and source for axobench prediction adapters.
section: API reference
order: 220
---

## Module contract

Prediction adapters reconstruct checkpoint models, select morphology identities, and return NumPy arrays in AxoBench's expected coordinates. The current AxoBench package is an additional dependency for the CLI evaluator. The source supports native and streaming predictor options in Python; the CLI exposes its declared subset.

Source revision: `306a51ed950b`. [Public export index](/api/).

## make_official_elm_predictor

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axobench_iteration.py#L22-L83)

```python
make_official_elm_predictor(config_path: str | Path, checkpoint_path: str | Path, *, device: str='auto', dtype: str | torch.dtype='float32') -> tuple[Callable[[np.ndarray], np.ndarray], dict[str, Any]]
```

Load an upstream Branch-ELM checkpoint on the shared AxoBench contract.

| Parameter | Type | Default |
| --- | --- | --- |
| `config_path` | `str \| Path` | required |
| `checkpoint_path` | `str \| Path` | required |
| `device` | `str` | `'auto'` |
| `dtype` | `str \| torch.dtype` | `'float32'` |

`device`: Execution or allocation device. `dtype`: Floating-point execution or allocation dtype.

Returns `tuple[Callable[[np.ndarray], np.ndarray], dict[str, Any]]`.

## make_checkpoint_predictor

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axobench_iteration.py#L86-L189)

```python
make_checkpoint_predictor(checkpoint: str | Path, *, device: str='auto', dtype: str | torch.dtype='float32', streaming: bool=False, streaming_chunk_size: int | None=None) -> tuple[Callable[[np.ndarray], np.ndarray], dict[str, Any]]
```

Load a standard AxoSim checkpoint as an AxoBench prediction callable.

Returns (predictor,metadata). The predictor accepts native NumPy inputs (B,T,C), optionally with morphology IDs when supported, and returns floating-point NumPy (B,T,2) outputs in AxoBench coordinates. Streaming requires the checkpoint's streaming API. Metadata includes resident parameter count and inference dtype.

| Parameter | Type | Default |
| --- | --- | --- |
| `checkpoint` | `str \| Path` | required |
| `device` | `str` | `'auto'` |
| `dtype` | `str \| torch.dtype` | `'float32'` |
| `streaming` | `bool` | `False` |
| `streaming_chunk_size` | `int \| None` | `None` |

`device`: Execution or allocation device. `dtype`: Floating-point execution or allocation dtype.

Returns `tuple[Callable[[np.ndarray], np.ndarray], dict[str, Any]]`.
