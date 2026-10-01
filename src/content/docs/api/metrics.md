---
title: Local metrics and dataset evaluation
description: Signatures, parameters, return contracts, and source for local metrics and dataset evaluation.
section: API reference
order: 217
---

## Module contract

These local utility functions support RMSE, AUC, and dataset evaluation. AxoBench introduces and implements the report's Mean F1, Voltage SERA, and Dynamics SERA protocol; use axosim-evaluate-model for that core metric set. SERA uses squared error; Root-SERA is its square-root presentation.

Source revision: `306a51ed950b`. [Public export index](/api/).

## soma_rmse

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/metrics.py#L6-L9)

```python
soma_rmse(prediction: np.ndarray, target: np.ndarray) -> float
```

| Parameter | Type | Default |
| --- | --- | --- |
| `prediction` | `np.ndarray` | required |
| `target` | `np.ndarray` | required |

Returns `float`.

## binary_auc

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/metrics.py#L12-L34)

```python
binary_auc(scores: np.ndarray, labels: np.ndarray) -> float
```

| Parameter | Type | Default |
| --- | --- | --- |
| `scores` | `np.ndarray` | required |
| `labels` | `np.ndarray` | required |

Returns `float`.

## spike_auc

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/metrics.py#L37-L38)

```python
spike_auc(prediction: np.ndarray, target: np.ndarray) -> float
```

| Parameter | Type | Default |
| --- | --- | --- |
| `prediction` | `np.ndarray` | required |
| `target` | `np.ndarray` | required |

Returns `float`.

## evaluate_dataset

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/evaluate.py#L17-L122)

```python
evaluate_dataset(model: BranchELM, dataset: ShardedNeuronIODataset, *, batch_size: int=8, device: str='cpu', soma_units: str='millivolts', y_train_soma_scale: float=DEFAULT_Y_TRAIN_SOMA_SCALE, ignore_start: int=0, mask_mode: str='ignore-start', stitch_burn_in: int=150, soma_affine_calibration: bool=False, pin_memory: bool=False, non_blocking: bool=True) -> dict[str, float | int]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `BranchELM` | required |
| `dataset` | `ShardedNeuronIODataset` | required |
| `batch_size` | `int` | `8` |
| `device` | `str` | `'cpu'` |
| `soma_units` | `str` | `'millivolts'` |
| `y_train_soma_scale` | `float` | `DEFAULT_Y_TRAIN_SOMA_SCALE` = `0.1` |
| `ignore_start` | `int` | `0` |
| `mask_mode` | `str` | `'ignore-start'` |
| `stitch_burn_in` | `int` | `150` |
| `soma_affine_calibration` | `bool` | `False` |
| `pin_memory` | `bool` | `False` |
| `non_blocking` | `bool` | `True` |

`batch_size`: Examples processed per batch. `device`: Execution or allocation device. `ignore_start`: Initial native timesteps excluded by the declared path.

Returns `dict[str, float \| int]`.

## write_metrics

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/evaluate.py#L125-L128)

```python
write_metrics(metrics: dict[str, float | int], output: str | Path) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `metrics` | `dict[str, float \| int]` | required |
| `output` | `str \| Path` | required |

Returns `None`.
