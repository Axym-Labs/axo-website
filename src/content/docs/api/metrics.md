---
title: Local metrics and dataset evaluation
description: Signatures, parameters, return contracts, and source for local metrics and dataset evaluation.
section: API reference
apiGroup: Training and evaluation
order: 219
---

## Overview

These local utility functions support RMSE, AUC, and dataset evaluation. AxoBench introduces and implements the report's Mean F1, Voltage SERA, and Dynamics SERA protocol; use axosim-evaluate-model for that core metric set. SERA uses squared error; Root-SERA is its square-root presentation.

Source revision: `0f546adfd8fc`. [Public export index](/api/).

<section class="api-symbol" id="metrics-soma-rmse">

## soma_rmse

<div class="api-signature">

```python
axosim.metrics.soma_rmse(prediction: np.ndarray, target: np.ndarray) -> float
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/metrics.py#L6-L9)

</div>

Compute root-mean-square error from channel 1 of matched prediction and target arrays.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Prediction array with a final channel axis; channel 1 contains soma values.</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Matched reference array in the same soma coordinate as prediction.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rmse</code> <span class="api-type">float</span></dt>
<dd>Root-mean-square error in the supplied soma target coordinate, aggregated over channel 1.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-binary-auc">

## binary_auc

<div class="api-signature">

```python
axosim.metrics.binary_auc(scores: np.ndarray, labels: np.ndarray) -> float
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/metrics.py#L12-L34)

</div>

Compute rank-based binary ROC AUC with averaged tied ranks; return NaN when either label class is absent.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>scores</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Continuous scores; larger values indicate greater evidence for a positive label.</dd>
<dt><code>labels</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Binary reference labels, classified as positive above 0.5.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>auc</code> <span class="api-type">float</span></dt>
<dd>ROC AUC over all flattened entries, or NaN when labels contain only one class.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-spike-auc">

## spike_auc

<div class="api-signature">

```python
axosim.metrics.spike_auc(prediction: np.ndarray, target: np.ndarray) -> float
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/metrics.py#L37-L38)

</div>

Compute binary ROC AUC from channel 0 of prediction and target arrays.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Prediction array whose channel 0 contains continuous spike scores.</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Matched reference array whose channel 0 contains spike labels.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>auc</code> <span class="api-type">float</span></dt>
<dd>ROC AUC over channel 0, or NaN when reference labels contain only one class.</dd>
</dl>

</section>

<section class="api-symbol" id="evaluate-evaluate-dataset">

## evaluate_dataset

<div class="api-signature">

```python
axosim.evaluate.evaluate_dataset(model: BranchELM, dataset: ShardedNeuronIODataset, *, batch_size: int=8, device: str='cpu', soma_units: str='millivolts', y_train_soma_scale: float=DEFAULT_Y_TRAIN_SOMA_SCALE, ignore_start: int=0, mask_mode: str='ignore-start', stitch_burn_in: int=150, soma_affine_calibration: bool=False, pin_memory: bool=False, non_blocking: bool=True) -> dict[str, float | int]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/evaluate.py#L17-L122)

</div>

Evaluate local spike AUC and soma RMSE over dataset batches, with the selected temporal mask and soma coordinate convention.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">BranchELM</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
<dt><code>dataset</code> <span class="api-type">ShardedNeuronIODataset</span></dt>
<dd><span class="api-default">required.</span> Trace dataset supporting the batching contract used by this operation.</dd>
<dt><code>batch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span> Examples processed per batch.</dd>
<dt><code>device</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;cpu&#x27;.</span> Execution or allocation device.</dd>
<dt><code>soma_units</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;millivolts&#x27;.</span> Coordinate convention used when computing the local soma metric.</dd>
<dt><code>y_train_soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale converting the biased voltage to the training target coordinate.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial native timesteps excluded by the declared path.</dd>
<dt><code>mask_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;ignore-start&#x27;.</span> Initial-timestep exclusion or official overlap-stitching mask.</dd>
<dt><code>stitch_burn_in</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=150.</span> Native overlap timesteps excluded from subsequent stitched windows.</dd>
<dt><code>soma_affine_calibration</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Rescale predictions to the evaluation targets&#x27; mean and standard deviation; declare this calibration when comparing metrics.</dd>
<dt><code>pin_memory</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Stage CPU arrays in pinned memory before a CUDA transfer.</dd>
<dt><code>non_blocking</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Request asynchronous tensor transfers where supported.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>metrics</code> <span class="api-type">dict[str, float | int]</span></dt>
<dd>Sample count, temporal-mask and calibration settings, elapsed time, throughput, soma RMSE and units, spike AUC, and related local spike metrics.</dd>
</dl>

</section>

<section class="api-symbol" id="evaluate-write-metrics">

## write_metrics

<div class="api-signature">

```python
axosim.evaluate.write_metrics(metrics: dict[str, float | int], output: str | Path) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/evaluate.py#L125-L128)

</div>

Write the local metrics dictionary as JSON, creating its parent directory when needed.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>metrics</code> <span class="api-type">dict[str, float | int]</span></dt>
<dd><span class="api-default">required.</span> Metrics dictionary to serialize.</dd>
<dt><code>output</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>
