---
title: NeuronIO conversion
description: Signatures, parameters, return values, and source for neuronIO conversion.
section: AxoBench API
apiGroup: Data
order: 309
---

## Overview

Parse raw NeuronIO simulation pickles and write deterministic AxoBench shards. Inhibitory channels receive the sign -1, and the soma target is clipped at -55 mV and normalized as (v + 67.7) * 0.1. Converted shards store no unclipped voltage; [NeuronIO compatibility](/axobench/neuronio/) explains the consequences for the metrics. Raw files are Python pickles: parse only trusted files.

Source revision: `496e0c1a2dfd`. [Export index](/axobench-api/).

<section class="api-symbol" id="neuronio-raw-convert-neuronio-pickles">

## convert_neuronio_pickles

<div class="api-signature">

```python
axobench.neuronio_raw.convert_neuronio_pickles(input_path: str | Path, output_dir: str | Path, *, shard_size: int=128, window_size: int | None=None, window_stride: int | None=None, ignore_start: int=0, y_soma_threshold: float=DEFAULT_Y_SOMA_THRESHOLD, y_train_soma_bias: float=DEFAULT_Y_TRAIN_SOMA_BIAS, y_train_soma_scale: float=DEFAULT_Y_TRAIN_SOMA_SCALE) -> list[Path]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/neuronio_raw.py#L67-L132)

</div>

Convert raw NeuronIO files (*sim__* below input_path, or one file) to shards named neuronio_00000.npz with a manifest. Existing manifest entries in output_dir are kept and new shards are numbered after them.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>input_path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Raw file or directory searched recursively.</dd>
<dt><code>output_dir</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Destination directory.</dd>
<dt><code>shard_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=128.</span> Traces per shard.</dd>
<dt><code>window_size</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional window length; None keeps whole simulations.</dd>
<dt><code>window_stride</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Window stride; defaults to window_size.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> First window start when windowing.</dd>
<dt><code>y_soma_threshold</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=DEFAULT_Y_SOMA_THRESHOLD = -55.0.</span> Clipping level in millivolts.</dd>
<dt><code>y_train_soma_bias</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=DEFAULT_Y_TRAIN_SOMA_BIAS = -67.7.</span> Millivolt bias subtracted after clipping.</dd>
<dt><code>y_train_soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=DEFAULT_Y_TRAIN_SOMA_SCALE.</span> Scale applied after the bias.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>paths</code> <span class="api-type">list[Path]</span></dt>
<dd>Written shard files.</dd>
</dl>

</section>

<section class="api-symbol" id="neuronio-raw-parse-neuronio-pickle">

## parse_neuronio_pickle

<div class="api-signature">

```python
axobench.neuronio_raw.parse_neuronio_pickle(path: str | Path) -> RawNeuronIO
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/neuronio_raw.py#L24-L64)

</div>

Parse one raw NeuronIO pickle into dense arrays at 1 ms.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Raw pickle file.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>raw</code> <span class="api-type">RawNeuronIO</span></dt>
<dd>Unsigned inputs, spikes, soma voltage, and metadata.</dd>
</dl>

</section>

<section class="api-symbol" id="neuronio-raw-rawneuronio">

## RawNeuronIO

<div class="api-signature">

```python
axobench.neuronio_raw.RawNeuronIO(inputs: np.ndarray, spikes: np.ndarray, soma: np.ndarray, metadata: dict[str, object])
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/neuronio_raw.py#L17-L21)

</div>

Arrays of one raw NeuronIO file.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Unsigned input events (simulation, time, 2 x segments), excitatory segments first.</dd>
<dt><code>spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Output spike indicators, (simulation, time).</dd>
<dt><code>soma</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Soma voltage in millivolts, (simulation, time).</dd>
<dt><code>metadata</code> <span class="api-type">dict[str, object]</span></dt>
<dd><span class="api-default">required.</span> Simulation count, duration, synapse count, segment types, and distances from the soma.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="neuronio-raw-normalize-soma">

## normalize_soma

<div class="api-signature">

```python
axobench.neuronio_raw.normalize_soma(soma: np.ndarray, threshold: float=DEFAULT_Y_SOMA_THRESHOLD, bias: float=DEFAULT_Y_TRAIN_SOMA_BIAS, scale: float=DEFAULT_Y_TRAIN_SOMA_SCALE) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/neuronio_raw.py#L142-L150)

</div>

Clip at the threshold and normalize: (min(v, threshold) - bias) * scale.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>soma</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Voltage in millivolts.</dd>
<dt><code>threshold</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=DEFAULT_Y_SOMA_THRESHOLD = -55.0.</span> Clipping level in millivolts.</dd>
<dt><code>bias</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=DEFAULT_Y_TRAIN_SOMA_BIAS = -67.7.</span> Millivolt bias.</dd>
<dt><code>scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=DEFAULT_Y_TRAIN_SOMA_SCALE.</span> Scale after the bias.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>normalized</code> <span class="api-type">np.ndarray</span></dt>
<dd>float32 target coordinate.</dd>
</dl>

</section>

<section class="api-symbol" id="neuronio-raw-create-neuronio-input-type">

## create_neuronio_input_type

<div class="api-signature">

```python
axobench.neuronio_raw.create_neuronio_input_type(num_input: int) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/neuronio_raw.py#L135-L139)

</div>

Channel signs: +1 for the first half and -1 for the second half.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>num_input</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Even channel count.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>signs</code> <span class="api-type">np.ndarray</span></dt>
<dd>float32 sign per channel.</dd>
</dl>

</section>
