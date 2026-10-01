---
title: Training functions
description: Signatures, parameters, return contracts, and source for training functions.
section: API reference
apiGroup: Training and evaluation
order: 219
---

## Overview

The trainer fits native spike and soma targets with configurable losses, optimization, windowing, and validation. Model checkpoints store weights and metadata; preserve optimizer, scheduler, random, and data-order states separately when continuing an optimization trajectory.

Source revision: `856207f6de56`. [Public export index](/api/).

<section class="api-symbol" id="train-train-dataset">

## train_dataset

<div class="api-signature">

```python
axosim.train.train_dataset(model: BranchELM, dataset: ShardedNeuronIODataset, *, epochs: int=1, batch_size: int=8, learning_rate: float=0.0005, burn_in: int=0, device: str='cpu', seed: int=0, validation_dataset: ShardedNeuronIODataset | None=None, validation_batch_size: int | None=None, best_checkpoint_path: str | Path | None=None, validation_soma_units: str='millivolts', validation_metric_ignore_start: int=0, validation_metric_mask_mode: str='ignore-start', validation_metric_stitch_burn_in: int=150, validation_soma_affine_calibration: bool=False, max_train_batches: int | None=None, lr_schedule: str='constant', lr_schedule_steps: int | None=None, optimizer_name: str='adam', weight_decay: float=0.0, l1_lambda: float=0.0, spike_loss_weight: float=0.5, soma_loss_weight: float=0.5, sparse_soma_loss_weight: float=0.0, sparse_soma_high_voltage_quantile: float=0.9, sparse_soma_high_dvdt_quantile: float=0.9, sparse_soma_input_event_quantile: float=0.95, sparse_soma_spike_window: int=5, sparse_soma_post_event_window: int=5, sera_soma_loss_weight: float=0.0, sera_soma_min_weight: float=0.05, sera_soma_relevance_power: float=1.0, soma_slope_loss_weight: float=0.0, grad_clip_norm: float=0.0, update_log_interval: int=0, update_log_path: str | Path | None=None, prefetch_batches: int=0, pin_memory: bool=False, non_blocking: bool=True) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/train.py#L21-L392)

</div>

Fit the supplied model with spike and soma losses; optionally validate after each epoch and save the best voltage result.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">BranchELM</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
<dt><code>dataset</code> <span class="api-type">ShardedNeuronIODataset</span></dt>
<dd><span class="api-default">required.</span> Trace dataset supporting the batching contract used by this operation.</dd>
<dt><code>epochs</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Number of passes over the declared epoch sampling budget.</dd>
<dt><code>batch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span> Examples processed per batch.</dd>
<dt><code>learning_rate</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0005.</span> Optimizer step size.</dd>
<dt><code>burn_in</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from training losses.</dd>
<dt><code>device</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;cpu&#x27;.</span> Execution or allocation device.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed for the declared operation.</dd>
<dt><code>validation_dataset</code> <span class="api-type">ShardedNeuronIODataset | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Development data for choosing trained states and calibration.</dd>
<dt><code>validation_batch_size</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Validation batch size; None uses the training batch size.</dd>
<dt><code>best_checkpoint_path</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Destination for the state with the lowest validation soma RMSE.</dd>
<dt><code>validation_soma_units</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;millivolts&#x27;.</span> Soma coordinate convention for validation RMSE.</dd>
<dt><code>validation_metric_ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial native timesteps excluded from validation metrics.</dd>
<dt><code>validation_metric_mask_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;ignore-start&#x27;.</span> Temporal masking policy used for validation metrics.</dd>
<dt><code>validation_metric_stitch_burn_in</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=150.</span> Overlap exclusion for stitched validation traces.</dd>
<dt><code>validation_soma_affine_calibration</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Apply target-statistic affine calibration to validation soma predictions.</dd>
<dt><code>max_train_batches</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional cap on batches in each training epoch.</dd>
<dt><code>lr_schedule</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;constant&#x27;.</span> Learning-rate schedule selection.</dd>
<dt><code>lr_schedule_steps</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Number of optimizer steps used to parameterize the schedule.</dd>
<dt><code>optimizer_name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;adam&#x27;.</span> Optimizer selection supported by this training path.</dd>
<dt><code>weight_decay</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Optimizer regularization coefficient.</dd>
<dt><code>l1_lambda</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Coefficient of the L1 penalty on model parameters.</dd>
<dt><code>spike_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.5.</span> Multiplier applied to the spike training loss.</dd>
<dt><code>soma_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.5.</span> Multiplier applied to the soma training loss.</dd>
<dt><code>sparse_soma_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Coefficient of auxiliary soma MSE over teacher-defined high-importance timesteps.</dd>
<dt><code>sparse_soma_high_voltage_quantile</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.9.</span> Teacher-voltage quantile used to select high-voltage timesteps.</dd>
<dt><code>sparse_soma_high_dvdt_quantile</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.9.</span> Absolute teacher-voltage difference quantile used to select rapidly changing timesteps.</dd>
<dt><code>sparse_soma_input_event_quantile</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.95.</span> Positive input-activity quantile used to select event-adjacent timesteps.</dd>
<dt><code>sparse_soma_spike_window</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=5.</span> Symmetric native-timestep radius around reference spikes in the auxiliary mask.</dd>
<dt><code>sparse_soma_post_event_window</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=5.</span> Causal native-timestep window after selected input events.</dd>
<dt><code>sera_soma_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Coefficient of the relevance-weighted auxiliary soma loss.</dd>
<dt><code>sera_soma_min_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.05.</span> Minimum timestep weight in the relevance-weighted soma loss.</dd>
<dt><code>sera_soma_relevance_power</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span> Exponent applied to the teacher-derived relevance weights.</dd>
<dt><code>soma_slope_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Coefficient of squared error in adjacent-timestep soma differences.</dd>
<dt><code>grad_clip_norm</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Maximum gradient norm when clipping is enabled.</dd>
<dt><code>update_log_interval</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Optimizer-step interval between update-log records; zero disables logging.</dd>
<dt><code>update_log_path</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Destination for per-update JSON log records.</dd>
<dt><code>prefetch_batches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Number of dataset batches prepared ahead of consumption.</dd>
<dt><code>pin_memory</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Stage CPU arrays in pinned memory before a CUDA transfer.</dd>
<dt><code>non_blocking</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Request asynchronous tensor transfers where supported.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>metrics</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>Epoch history, final training loss and timing, optimizer/loss settings, and optional validation and best-state metrics. The supplied model retains its final trained weights.</dd>
</dl>

</section>

<section class="api-symbol" id="train-train-and-save">

## train_and_save

<div class="api-signature">

```python
axosim.train.train_and_save(model: BranchELM, dataset: ShardedNeuronIODataset, *, checkpoint_path: str | Path, metrics_path: str | Path, epochs: int=1, batch_size: int=8, learning_rate: float=0.0005, burn_in: int=0, device: str='cpu', seed: int=0, validation_dataset: ShardedNeuronIODataset | None=None, validation_batch_size: int | None=None, best_checkpoint_path: str | Path | None=None, validation_soma_units: str='millivolts', validation_metric_ignore_start: int=0, validation_metric_mask_mode: str='ignore-start', validation_metric_stitch_burn_in: int=150, validation_soma_affine_calibration: bool=False, max_train_batches: int | None=None, lr_schedule: str='constant', lr_schedule_steps: int | None=None, optimizer_name: str='adam', weight_decay: float=0.0, l1_lambda: float=0.0, spike_loss_weight: float=0.5, soma_loss_weight: float=0.5, sparse_soma_loss_weight: float=0.0, sparse_soma_high_voltage_quantile: float=0.9, sparse_soma_high_dvdt_quantile: float=0.9, sparse_soma_input_event_quantile: float=0.95, sparse_soma_spike_window: int=5, sparse_soma_post_event_window: int=5, sera_soma_loss_weight: float=0.0, sera_soma_min_weight: float=0.05, sera_soma_relevance_power: float=1.0, soma_slope_loss_weight: float=0.0, grad_clip_norm: float=0.0, update_log_interval: int=0, update_log_path: str | Path | None=None, prefetch_batches: int=0, pin_memory: bool=False, non_blocking: bool=True) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/train.py#L395-L493)

</div>

Train the supplied model, save its final weights and configuration, and write training metrics as JSON.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">BranchELM</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
<dt><code>dataset</code> <span class="api-type">ShardedNeuronIODataset</span></dt>
<dd><span class="api-default">required.</span> Trace dataset supporting the batching contract used by this operation.</dd>
<dt><code>checkpoint_path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Trusted model-weight file to reconstruct or evaluate.</dd>
<dt><code>metrics_path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Destination for training metrics JSON.</dd>
<dt><code>epochs</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Number of passes over the declared epoch sampling budget.</dd>
<dt><code>batch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span> Examples processed per batch.</dd>
<dt><code>learning_rate</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0005.</span> Optimizer step size.</dd>
<dt><code>burn_in</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from training losses.</dd>
<dt><code>device</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;cpu&#x27;.</span> Execution or allocation device.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed for the declared operation.</dd>
<dt><code>validation_dataset</code> <span class="api-type">ShardedNeuronIODataset | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Development data for choosing trained states and calibration.</dd>
<dt><code>validation_batch_size</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Validation batch size; None uses the training batch size.</dd>
<dt><code>best_checkpoint_path</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Destination for the state with the lowest validation soma RMSE.</dd>
<dt><code>validation_soma_units</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;millivolts&#x27;.</span> Soma coordinate convention for validation RMSE.</dd>
<dt><code>validation_metric_ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial native timesteps excluded from validation metrics.</dd>
<dt><code>validation_metric_mask_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;ignore-start&#x27;.</span> Temporal masking policy used for validation metrics.</dd>
<dt><code>validation_metric_stitch_burn_in</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=150.</span> Overlap exclusion for stitched validation traces.</dd>
<dt><code>validation_soma_affine_calibration</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Apply target-statistic affine calibration to validation soma predictions.</dd>
<dt><code>max_train_batches</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional cap on batches in each training epoch.</dd>
<dt><code>lr_schedule</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;constant&#x27;.</span> Learning-rate schedule selection.</dd>
<dt><code>lr_schedule_steps</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Number of optimizer steps used to parameterize the schedule.</dd>
<dt><code>optimizer_name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;adam&#x27;.</span> Optimizer selection supported by this training path.</dd>
<dt><code>weight_decay</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Optimizer regularization coefficient.</dd>
<dt><code>l1_lambda</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Coefficient of the L1 penalty on model parameters.</dd>
<dt><code>spike_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.5.</span> Multiplier applied to the spike training loss.</dd>
<dt><code>soma_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.5.</span> Multiplier applied to the soma training loss.</dd>
<dt><code>sparse_soma_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Coefficient of auxiliary soma MSE over teacher-defined high-importance timesteps.</dd>
<dt><code>sparse_soma_high_voltage_quantile</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.9.</span> Teacher-voltage quantile used to select high-voltage timesteps.</dd>
<dt><code>sparse_soma_high_dvdt_quantile</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.9.</span> Absolute teacher-voltage difference quantile used to select rapidly changing timesteps.</dd>
<dt><code>sparse_soma_input_event_quantile</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.95.</span> Positive input-activity quantile used to select event-adjacent timesteps.</dd>
<dt><code>sparse_soma_spike_window</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=5.</span> Symmetric native-timestep radius around reference spikes in the auxiliary mask.</dd>
<dt><code>sparse_soma_post_event_window</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=5.</span> Causal native-timestep window after selected input events.</dd>
<dt><code>sera_soma_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Coefficient of the relevance-weighted auxiliary soma loss.</dd>
<dt><code>sera_soma_min_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.05.</span> Minimum timestep weight in the relevance-weighted soma loss.</dd>
<dt><code>sera_soma_relevance_power</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span> Exponent applied to the teacher-derived relevance weights.</dd>
<dt><code>soma_slope_loss_weight</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Coefficient of squared error in adjacent-timestep soma differences.</dd>
<dt><code>grad_clip_norm</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Maximum gradient norm when clipping is enabled.</dd>
<dt><code>update_log_interval</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Optimizer-step interval between update-log records; zero disables logging.</dd>
<dt><code>update_log_path</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Destination for per-update JSON log records.</dd>
<dt><code>prefetch_batches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Number of dataset batches prepared ahead of consumption.</dd>
<dt><code>pin_memory</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Stage CPU arrays in pinned memory before a CUDA transfer.</dd>
<dt><code>non_blocking</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Request asynchronous tensor transfers where supported.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>metrics</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>The training metrics returned by train_dataset; the requested checkpoint and metrics JSON are also written.</dd>
</dl>

</section>
