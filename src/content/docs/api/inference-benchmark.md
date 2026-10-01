---
title: Inference benchmarking
description: Signatures, parameters, return contracts, and source for inference benchmarking.
section: API reference
order: 219
---

## Module contract

The benchmark measures model sequence execution across batch sizes, horizons, and precision choices. It does not include the complete connected population runtime. Preserve the warmup, repetitions, synchronization, compilation mode, device, and shape contract with every reported timing.

Source revision: `306a51ed950b`. [Public export index](/api/).

## benchmark_inference_matrix

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/inference_benchmark.py#L12-L103)

```python
benchmark_inference_matrix(model: torch.nn.Module, *, batch_sizes: Iterable[int], time_steps: Iterable[int], input_dim: int, device: str='cpu', precision: str='float32', warmup_runs: int=5, runs: int=20, compile_model: bool=False, accuracy_metrics_path: str | Path | None=None) -> dict[str, Any]
```

Benchmark dense full-window inference for deployment-oriented comparisons.

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `torch.nn.Module` | required |
| `batch_sizes` | `Iterable[int]` | required |
| `time_steps` | `Iterable[int]` | required |
| `input_dim` | `int` | required |
| `device` | `str` | `'cpu'` |
| `precision` | `str` | `'float32'` |
| `warmup_runs` | `int` | `5` |
| `runs` | `int` | `20` |
| `compile_model` | `bool` | `False` |
| `accuracy_metrics_path` | `str \| Path \| None` | `None` |

`time_steps`: Native sequence horizon. `input_dim`: Native input-channel count. `device`: Execution or allocation device.

Returns `dict[str, Any]`.

## count_parameters

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/inference_benchmark.py#L106-L107)

```python
count_parameters(model: torch.nn.Module) -> int
```

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `torch.nn.Module` | required |

Returns `int`.

## write_inference_benchmark

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/inference_benchmark.py#L110-L113)

```python
write_inference_benchmark(report: dict[str, Any], path: str | Path) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `report` | `dict[str, Any]` | required |
| `path` | `str \| Path` | required |

Returns `None`.

## parse_int_list

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/inference_benchmark.py#L116-L120)

```python
parse_int_list(value: str) -> list[int]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `value` | `str` | required |

Returns `list[int]`.
