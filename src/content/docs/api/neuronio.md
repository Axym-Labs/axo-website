---
title: NeuronIO conversion
description: Signatures, parameters, return contracts, and source for neuronio conversion.
section: API reference
apiGroup: Compatibility
order: 218
---

## Overview

The converter reads raw NeuronIO teacher traces and creates deterministic shards. Standard soma normalization clips at -55 mV and applies (v_mV-bias)*scale with bias=-67.7 and scale=0.1. Preserve conversion metadata: normalized targets cannot recover clipped spike peaks.

Source revision: `0f546adfd8fc`. [Public export index](/api/).

<section class="api-symbol" id="neuronio-raw-rawneuronio">

## RawNeuronIO

<div class="api-signature">

```python
axosim.neuronio_raw.RawNeuronIO(inputs: np.ndarray, spikes: np.ndarray, soma: np.ndarray, metadata: dict[str, object])
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/neuronio_raw.py#L17-L21)

</div>

Parsed raw simulations with separate input-event arrays, spike labels, voltage traces, and metadata.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Raw input events (simulations,time,2*segments), with excitatory channels followed by inhibitory channels before the converter applies E/I signs.</dd>
<dt><code>spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Binary output spike labels (simulations,time).</dd>
<dt><code>soma</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Raw soma voltage in millivolts, shaped (simulations,time).</dd>
<dt><code>metadata</code> <span class="api-type">dict[str, object]</span></dt>
<dd><span class="api-default">required.</span> Simulation counts, duration, synapse count, segment types, and available segment-to-soma distances extracted from the raw file.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="neuronio-raw-parse-neuronio-pickle">

## parse_neuronio_pickle

<div class="api-signature">

```python
axosim.neuronio_raw.parse_neuronio_pickle(path: str | Path) -> RawNeuronIO
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/neuronio_raw.py#L24-L64)

</div>

Parse a public NeuronIO simulation pickle into `(sim, time, channel)` arrays.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Filesystem location to read or write; see the operation&#x27;s persistence contract.</dd>
</dl>

<p class="api-label">Returns</p>

`RawNeuronIO`

</section>

<section class="api-symbol" id="neuronio-raw-convert-neuronio-pickles">

## convert_neuronio_pickles

<div class="api-signature">

```python
axosim.neuronio_raw.convert_neuronio_pickles(input_path: str | Path, output_dir: str | Path, *, shard_size: int=128, window_size: int | None=None, window_stride: int | None=None, ignore_start: int=0, y_soma_threshold: float=DEFAULT_Y_SOMA_THRESHOLD, y_train_soma_bias: float=DEFAULT_Y_TRAIN_SOMA_BIAS, y_train_soma_scale: float=DEFAULT_Y_TRAIN_SOMA_SCALE) -> list[Path]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/neuronio_raw.py#L67-L132)

</div>

Convert raw NeuronIO pickle files to deterministic `.npz` shards.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>input_path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Raw NeuronIO pickle file or directory to discover and convert.</dd>
<dt><code>output_dir</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Directory receiving converted shards and their manifest.</dd>
<dt><code>shard_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=128.</span> Maximum sample count in each converted shard.</dd>
<dt><code>window_size</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Native timesteps per extracted window.</dd>
<dt><code>window_stride</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Native timestep distance between successive window starts.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial native timesteps excluded by the declared path.</dd>
<dt><code>y_soma_threshold</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-55.0.</span> Upper voltage clipping threshold in millivolts.</dd>
<dt><code>y_train_soma_bias</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-67.7.</span> Voltage bias subtracted before target scaling, in millivolts.</dd>
<dt><code>y_train_soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale converting the biased voltage to the training target coordinate.</dd>
</dl>

<p class="api-label">Returns</p>

`list[Path]`

</section>

<section class="api-symbol" id="neuronio-raw-create-neuronio-input-type">

## create_neuronio_input_type

<div class="api-signature">

```python
axosim.neuronio_raw.create_neuronio_input_type(num_input: int) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/neuronio_raw.py#L135-L139)

</div>

Build an E/I sign vector with positive excitatory channels followed by negative inhibitory channels.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>num_input</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Input-channel count.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>signs</code> <span class="api-type">np.ndarray</span></dt>
<dd>Float32 vector (num_input,) with +1 in its first half and -1 in its second half; num_input must be even.</dd>
</dl>

</section>

<section class="api-symbol" id="neuronio-raw-normalize-soma">

## normalize_soma

<div class="api-signature">

```python
axosim.neuronio_raw.normalize_soma(soma: np.ndarray, threshold: float=DEFAULT_Y_SOMA_THRESHOLD, bias: float=DEFAULT_Y_TRAIN_SOMA_BIAS, scale: float=DEFAULT_Y_TRAIN_SOMA_SCALE) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/neuronio_raw.py#L142-L150)

</div>

Clip soma voltage and convert it to the normalized training coordinate.

Returns normalized soma targets after clipping teacher voltage at threshold and applying (voltage-bias)*scale. The default threshold is -55.0 mV, bias is -67.7 mV, and scale is 0.1.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>soma</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Raw soma voltage array in millivolts.</dd>
<dt><code>threshold</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=-55.0.</span> Upper clipping threshold in millivolts.</dd>
<dt><code>bias</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=-67.7.</span> Millivolt bias subtracted after clipping.</dd>
<dt><code>scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span> Multiplier converting biased millivolt values to the training coordinate.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>normalized</code> <span class="api-type">np.ndarray</span></dt>
<dd>Float32 array matching soma.shape, equal to (minimum(soma,threshold)-bias)*scale.</dd>
</dl>

</section>
