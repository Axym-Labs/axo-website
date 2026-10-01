---
title: Training functions
description: Signatures, parameters, return contracts, and source for training functions.
section: API reference
order: 218
---

## Module contract

The trainer fits native spike and soma targets with configurable losses, optimization, windowing, and validation. Model checkpoints store weights and metadata; preserve optimizer, scheduler, random, and data-order states separately when continuing an optimization trajectory.

Source revision: `306a51ed950b`. [Public export index](/api/).

## train_dataset

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/train.py#L21-L392)

```python
train_dataset(model: BranchELM, dataset: ShardedNeuronIODataset, *, epochs: int=1, batch_size: int=8, learning_rate: float=0.0005, burn_in: int=0, device: str='cpu', seed: int=0, validation_dataset: ShardedNeuronIODataset | None=None, validation_batch_size: int | None=None, best_checkpoint_path: str | Path | None=None, validation_soma_units: str='millivolts', validation_metric_ignore_start: int=0, validation_metric_mask_mode: str='ignore-start', validation_metric_stitch_burn_in: int=150, validation_soma_affine_calibration: bool=False, max_train_batches: int | None=None, lr_schedule: str='constant', lr_schedule_steps: int | None=None, optimizer_name: str='adam', weight_decay: float=0.0, l1_lambda: float=0.0, spike_loss_weight: float=0.5, soma_loss_weight: float=0.5, sparse_soma_loss_weight: float=0.0, sparse_soma_high_voltage_quantile: float=0.9, sparse_soma_high_dvdt_quantile: float=0.9, sparse_soma_input_event_quantile: float=0.95, sparse_soma_spike_window: int=5, sparse_soma_post_event_window: int=5, sera_soma_loss_weight: float=0.0, sera_soma_min_weight: float=0.05, sera_soma_relevance_power: float=1.0, soma_slope_loss_weight: float=0.0, grad_clip_norm: float=0.0, update_log_interval: int=0, update_log_path: str | Path | None=None, prefetch_batches: int=0, pin_memory: bool=False, non_blocking: bool=True) -> dict[str, Any]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `BranchELM` | required |
| `dataset` | `ShardedNeuronIODataset` | required |
| `epochs` | `int` | `1` |
| `batch_size` | `int` | `8` |
| `learning_rate` | `float` | `0.0005` |
| `burn_in` | `int` | `0` |
| `device` | `str` | `'cpu'` |
| `seed` | `int` | `0` |
| `validation_dataset` | `ShardedNeuronIODataset \| None` | `None` |
| `validation_batch_size` | `int \| None` | `None` |
| `best_checkpoint_path` | `str \| Path \| None` | `None` |
| `validation_soma_units` | `str` | `'millivolts'` |
| `validation_metric_ignore_start` | `int` | `0` |
| `validation_metric_mask_mode` | `str` | `'ignore-start'` |
| `validation_metric_stitch_burn_in` | `int` | `150` |
| `validation_soma_affine_calibration` | `bool` | `False` |
| `max_train_batches` | `int \| None` | `None` |
| `lr_schedule` | `str` | `'constant'` |
| `lr_schedule_steps` | `int \| None` | `None` |
| `optimizer_name` | `str` | `'adam'` |
| `weight_decay` | `float` | `0.0` |
| `l1_lambda` | `float` | `0.0` |
| `spike_loss_weight` | `float` | `0.5` |
| `soma_loss_weight` | `float` | `0.5` |
| `sparse_soma_loss_weight` | `float` | `0.0` |
| `sparse_soma_high_voltage_quantile` | `float` | `0.9` |
| `sparse_soma_high_dvdt_quantile` | `float` | `0.9` |
| `sparse_soma_input_event_quantile` | `float` | `0.95` |
| `sparse_soma_spike_window` | `int` | `5` |
| `sparse_soma_post_event_window` | `int` | `5` |
| `sera_soma_loss_weight` | `float` | `0.0` |
| `sera_soma_min_weight` | `float` | `0.05` |
| `sera_soma_relevance_power` | `float` | `1.0` |
| `soma_slope_loss_weight` | `float` | `0.0` |
| `grad_clip_norm` | `float` | `0.0` |
| `update_log_interval` | `int` | `0` |
| `update_log_path` | `str \| Path \| None` | `None` |
| `prefetch_batches` | `int` | `0` |
| `pin_memory` | `bool` | `False` |
| `non_blocking` | `bool` | `True` |

`batch_size`: Examples processed per batch. `learning_rate`: Optimizer step size. `device`: Execution or allocation device. `seed`: Random seed for the declared operation.

Returns `dict[str, Any]`.

## train_and_save

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/train.py#L395-L493)

```python
train_and_save(model: BranchELM, dataset: ShardedNeuronIODataset, *, checkpoint_path: str | Path, metrics_path: str | Path, epochs: int=1, batch_size: int=8, learning_rate: float=0.0005, burn_in: int=0, device: str='cpu', seed: int=0, validation_dataset: ShardedNeuronIODataset | None=None, validation_batch_size: int | None=None, best_checkpoint_path: str | Path | None=None, validation_soma_units: str='millivolts', validation_metric_ignore_start: int=0, validation_metric_mask_mode: str='ignore-start', validation_metric_stitch_burn_in: int=150, validation_soma_affine_calibration: bool=False, max_train_batches: int | None=None, lr_schedule: str='constant', lr_schedule_steps: int | None=None, optimizer_name: str='adam', weight_decay: float=0.0, l1_lambda: float=0.0, spike_loss_weight: float=0.5, soma_loss_weight: float=0.5, sparse_soma_loss_weight: float=0.0, sparse_soma_high_voltage_quantile: float=0.9, sparse_soma_high_dvdt_quantile: float=0.9, sparse_soma_input_event_quantile: float=0.95, sparse_soma_spike_window: int=5, sparse_soma_post_event_window: int=5, sera_soma_loss_weight: float=0.0, sera_soma_min_weight: float=0.05, sera_soma_relevance_power: float=1.0, soma_slope_loss_weight: float=0.0, grad_clip_norm: float=0.0, update_log_interval: int=0, update_log_path: str | Path | None=None, prefetch_batches: int=0, pin_memory: bool=False, non_blocking: bool=True) -> dict[str, Any]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `BranchELM` | required |
| `dataset` | `ShardedNeuronIODataset` | required |
| `checkpoint_path` | `str \| Path` | required |
| `metrics_path` | `str \| Path` | required |
| `epochs` | `int` | `1` |
| `batch_size` | `int` | `8` |
| `learning_rate` | `float` | `0.0005` |
| `burn_in` | `int` | `0` |
| `device` | `str` | `'cpu'` |
| `seed` | `int` | `0` |
| `validation_dataset` | `ShardedNeuronIODataset \| None` | `None` |
| `validation_batch_size` | `int \| None` | `None` |
| `best_checkpoint_path` | `str \| Path \| None` | `None` |
| `validation_soma_units` | `str` | `'millivolts'` |
| `validation_metric_ignore_start` | `int` | `0` |
| `validation_metric_mask_mode` | `str` | `'ignore-start'` |
| `validation_metric_stitch_burn_in` | `int` | `150` |
| `validation_soma_affine_calibration` | `bool` | `False` |
| `max_train_batches` | `int \| None` | `None` |
| `lr_schedule` | `str` | `'constant'` |
| `lr_schedule_steps` | `int \| None` | `None` |
| `optimizer_name` | `str` | `'adam'` |
| `weight_decay` | `float` | `0.0` |
| `l1_lambda` | `float` | `0.0` |
| `spike_loss_weight` | `float` | `0.5` |
| `soma_loss_weight` | `float` | `0.5` |
| `sparse_soma_loss_weight` | `float` | `0.0` |
| `sparse_soma_high_voltage_quantile` | `float` | `0.9` |
| `sparse_soma_high_dvdt_quantile` | `float` | `0.9` |
| `sparse_soma_input_event_quantile` | `float` | `0.95` |
| `sparse_soma_spike_window` | `int` | `5` |
| `sparse_soma_post_event_window` | `int` | `5` |
| `sera_soma_loss_weight` | `float` | `0.0` |
| `sera_soma_min_weight` | `float` | `0.05` |
| `sera_soma_relevance_power` | `float` | `1.0` |
| `soma_slope_loss_weight` | `float` | `0.0` |
| `grad_clip_norm` | `float` | `0.0` |
| `update_log_interval` | `int` | `0` |
| `update_log_path` | `str \| Path \| None` | `None` |
| `prefetch_batches` | `int` | `0` |
| `pin_memory` | `bool` | `False` |
| `non_blocking` | `bool` | `True` |

`batch_size`: Examples processed per batch. `learning_rate`: Optimizer step size. `device`: Execution or allocation device. `seed`: Random seed for the declared operation.

Returns `dict[str, Any]`.
