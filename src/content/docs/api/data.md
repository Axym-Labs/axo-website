---
title: Trace datasets
description: Signatures, parameters, return contracts, and source for trace datasets.
section: API reference
apiGroup: Data
order: 217
---

## Overview

NeuronIO shards store inputs (samples, time, channels), targets (samples, time, 2), and sample identities. Dataset samples expose one (time, channels) input and one (time, 2) target. get_batch returns batched NumPy arrays. Window datasets preserve sample identity while selecting native time windows; preserve context boundaries when splitting data.

Source revision: `0f546adfd8fc`. [Public export index](/api/).

<section class="api-symbol" id="data-neuroniosample">

## NeuronIOSample

<div class="api-signature">

```python
axosim.data.NeuronIOSample(sample_id: str, inputs: np.ndarray, targets: np.ndarray)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L14-L17)

</div>

One identified native input trace and its two-channel target trace.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>sample_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Persistent trace identity from the shard&#x27;s sample_ids array.</dd>
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> One native input trace, shaped (time,input_channels).</dd>
<dt><code>targets</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> One spike/soma target trace, shaped (time,2).</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="data-shardedneuroniodataset">

## ShardedNeuronIODataset

<div class="api-signature">

```python
axosim.data.ShardedNeuronIODataset(root: str | Path, *, shuffle: bool=False, seed: int=0, shuffle_mode: Literal['sample', 'shard']='sample', cache_shards: int=0)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L29-L222)

</div>

Deterministic reader for pre-sharded NeuronIO-style NPZ files.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Dataset shard directory or manifest root.</dd>
<dt><code>shuffle</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Enable deterministic reordering controlled by seed and shuffle_mode.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed for the declared operation.</dd>
<dt><code>shuffle_mode</code> <span class="api-type">Literal[&#x27;sample&#x27;, &#x27;shard&#x27;]</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;sample&#x27;.</span> Choose sample-level or shard-level reordering.</dd>
<dt><code>cache_shards</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Maximum cached shards; zero disables the cache.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#data-shardedneuroniodataset---len--"><code>ShardedNeuronIODataset.__len__()</code></a></li>
<li><a href="#data-shardedneuroniodataset-reshuffle"><code>ShardedNeuronIODataset.reshuffle()</code></a></li>
<li><a href="#data-shardedneuroniodataset---getitem--"><code>ShardedNeuronIODataset.__getitem__()</code></a></li>
<li><a href="#data-shardedneuroniodataset-get-batch"><code>ShardedNeuronIODataset.get_batch()</code></a></li>
<li><a href="#data-shardedneuroniodataset-get-sample-ids"><code>ShardedNeuronIODataset.get_sample_ids()</code></a></li>
<li><a href="#data-shardedneuroniodataset-get-optional-array-batch"><code>ShardedNeuronIODataset.get_optional_array_batch()</code></a></li>
<li><a href="#data-shardedneuroniodataset-get-shard-sequence-length"><code>ShardedNeuronIODataset.get_shard_sequence_length()</code></a></li>
</ul>

<section class="api-method" id="data-shardedneuroniodataset---len--">

### ShardedNeuronIODataset.__len__

<div class="api-signature">

```python
axosim.data.ShardedNeuronIODataset.__len__() -> int
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L69-L70)

</div>

Return the number of indexed samples.

<p class="api-label">Returns</p>

`int`

</section>

<section class="api-method" id="data-shardedneuroniodataset-reshuffle">

### ShardedNeuronIODataset.reshuffle

<div class="api-signature">

```python
axosim.data.ShardedNeuronIODataset.reshuffle(seed: int) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L72-L80)

</div>

Reorder the enabled sampling index using the supplied seed.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Random seed for the declared operation.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-method" id="data-shardedneuroniodataset---getitem--">

### ShardedNeuronIODataset.__getitem__

<div class="api-signature">

```python
axosim.data.ShardedNeuronIODataset.__getitem__(index: int) -> NeuronIOSample
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L82-L91)

</div>

Read one sample and its input/target contract.

Returns NeuronIOSample with sample_id, inputs (T,C), and targets (T,2).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>index</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Index of one dataset sample.</dd>
</dl>

<p class="api-label">Returns</p>

`NeuronIOSample`

</section>

<section class="api-method" id="data-shardedneuroniodataset-get-batch">

### ShardedNeuronIODataset.get_batch

<div class="api-signature">

```python
axosim.data.ShardedNeuronIODataset.get_batch(indices: range | list[int]) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L93-L101)

</div>

Read the requested input and target arrays as a batch.

Returns (inputs,targets) NumPy arrays with shapes (B,T,C) and (B,T,2). Selected shard windows must have compatible lengths for stacking.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Requested dataset sample indices.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd>Native inputs with shape (batch,time,input_channels).</dd>
<dt><code>targets</code> <span class="api-type">np.ndarray</span></dt>
<dd>Spike and soma targets with shape (batch,time,2).</dd>
</dl>

</section>

<section class="api-method" id="data-shardedneuroniodataset-get-sample-ids">

### ShardedNeuronIODataset.get_sample_ids

<div class="api-signature">

```python
axosim.data.ShardedNeuronIODataset.get_sample_ids(indices: range | list[int]) -> list[str]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L103-L104)

</div>

Return the sample identities associated with the selected indices.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Requested dataset sample indices.</dd>
</dl>

<p class="api-label">Returns</p>

`list[str]`

</section>

<section class="api-method" id="data-shardedneuroniodataset-get-optional-array-batch">

### ShardedNeuronIODataset.get_optional_array_batch

<div class="api-signature">

```python
axosim.data.ShardedNeuronIODataset.get_optional_array_batch(name: str, indices: range | list[int]) -> np.ndarray | None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L106-L115)

</div>

Return an optional per-sample array from NPZ shards when present.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Name of the optional shard array or declared record.</dd>
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Requested dataset sample indices.</dd>
</dl>

<p class="api-label">Returns</p>

`np.ndarray \| None`

</section>

<section class="api-method" id="data-shardedneuroniodataset-get-shard-sequence-length">

### ShardedNeuronIODataset.get_shard_sequence_length

<div class="api-signature">

```python
axosim.data.ShardedNeuronIODataset.get_shard_sequence_length(shard_idx: int) -> int
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L117-L130)

</div>

Read the input time dimension without materializing a shard array.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>shard_idx</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Index of the shard in the dataset manifest.</dd>
</dl>

<p class="api-label">Returns</p>

`int`

</section>

</section>

<section class="api-symbol" id="data-deterministicwindowdataset">

## DeterministicWindowDataset

<div class="api-signature">

```python
axosim.data.DeterministicWindowDataset(base: ShardedNeuronIODataset, *, window_size: int, stride: int | None=None, start_offset: int=0)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L225-L280)

</div>

Enumerate fixed-size windows from another NeuronIO-style dataset.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>base</code> <span class="api-type">ShardedNeuronIODataset</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>window_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Native timesteps per extracted window.</dd>
<dt><code>stride</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Distance between selected positions in the relevant sequence.</dd>
<dt><code>start_offset</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Native timestep index before the first selected window.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#data-deterministicwindowdataset---len--"><code>DeterministicWindowDataset.__len__()</code></a></li>
<li><a href="#data-deterministicwindowdataset---getitem--"><code>DeterministicWindowDataset.__getitem__()</code></a></li>
<li><a href="#data-deterministicwindowdataset-get-batch"><code>DeterministicWindowDataset.get_batch()</code></a></li>
<li><a href="#data-deterministicwindowdataset-get-sample-ids"><code>DeterministicWindowDataset.get_sample_ids()</code></a></li>
</ul>

<section class="api-method" id="data-deterministicwindowdataset---len--">

### DeterministicWindowDataset.__len__

<div class="api-signature">

```python
axosim.data.DeterministicWindowDataset.__len__() -> int
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L259-L260)

</div>

Return the number of indexed samples.

<p class="api-label">Returns</p>

`int`

</section>

<section class="api-method" id="data-deterministicwindowdataset---getitem--">

### DeterministicWindowDataset.__getitem__

<div class="api-signature">

```python
axosim.data.DeterministicWindowDataset.__getitem__(index: int) -> NeuronIOSample
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L262-L270)

</div>

Read one sample and its input/target contract.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>index</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Index of one dataset sample.</dd>
</dl>

<p class="api-label">Returns</p>

`NeuronIOSample`

</section>

<section class="api-method" id="data-deterministicwindowdataset-get-batch">

### DeterministicWindowDataset.get_batch

<div class="api-signature">

```python
axosim.data.DeterministicWindowDataset.get_batch(indices: range | list[int]) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L272-L277)

</div>

Read the requested input and target arrays as a batch.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Requested dataset sample indices.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd>Native inputs with shape (batch,time,input_channels).</dd>
<dt><code>targets</code> <span class="api-type">np.ndarray</span></dt>
<dd>Spike and soma targets with shape (batch,time,2).</dd>
</dl>

</section>

<section class="api-method" id="data-deterministicwindowdataset-get-sample-ids">

### DeterministicWindowDataset.get_sample_ids

<div class="api-signature">

```python
axosim.data.DeterministicWindowDataset.get_sample_ids(indices: range | list[int]) -> list[str]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L279-L280)

</div>

Return the sample identities associated with the selected indices.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Requested dataset sample indices.</dd>
</dl>

<p class="api-label">Returns</p>

`list[str]`

</section>

</section>

<section class="api-symbol" id="data-randomfulltracewindowdataset">

## RandomFullTraceWindowDataset

<div class="api-signature">

```python
axosim.data.RandomFullTraceWindowDataset(base: ShardedNeuronIODataset, *, window_size: int=500, start_offset: int=500, samples_per_epoch: int | None=None, batch_size: int=8, shard_reuse_batches: int=1, sequence_length: int | None=None, seed: int=0, cache_full_shards: bool=True)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L283-L399)

</div>

Sample deterministic random windows from cached full-trace shards.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>base</code> <span class="api-type">ShardedNeuronIODataset</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>window_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=500.</span> Native timesteps per extracted window.</dd>
<dt><code>start_offset</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=500.</span> Native timestep index before the first selected window.</dd>
<dt><code>samples_per_epoch</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Number of training window presentations requested per epoch.</dd>
<dt><code>batch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span> Examples processed per batch.</dd>
<dt><code>shard_reuse_batches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Number of consecutive batches sampled before advancing to another shard.</dd>
<dt><code>sequence_length</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Native timestep count of a trace.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed for the declared operation.</dd>
<dt><code>cache_full_shards</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Retain complete shard arrays rather than only selected data.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#data-randomfulltracewindowdataset---len--"><code>RandomFullTraceWindowDataset.__len__()</code></a></li>
<li><a href="#data-randomfulltracewindowdataset-reshuffle"><code>RandomFullTraceWindowDataset.reshuffle()</code></a></li>
<li><a href="#data-randomfulltracewindowdataset---getitem--"><code>RandomFullTraceWindowDataset.__getitem__()</code></a></li>
<li><a href="#data-randomfulltracewindowdataset-get-batch"><code>RandomFullTraceWindowDataset.get_batch()</code></a></li>
<li><a href="#data-randomfulltracewindowdataset-get-sample-ids"><code>RandomFullTraceWindowDataset.get_sample_ids()</code></a></li>
</ul>

<section class="api-method" id="data-randomfulltracewindowdataset---len--">

### RandomFullTraceWindowDataset.__len__

<div class="api-signature">

```python
axosim.data.RandomFullTraceWindowDataset.__len__() -> int
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L328-L329)

</div>

Return the number of indexed samples.

<p class="api-label">Returns</p>

`int`

</section>

<section class="api-method" id="data-randomfulltracewindowdataset-reshuffle">

### RandomFullTraceWindowDataset.reshuffle

<div class="api-signature">

```python
axosim.data.RandomFullTraceWindowDataset.reshuffle(seed: int) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L331-L354)

</div>

Reorder the enabled sampling index using the supplied seed.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Random seed for the declared operation.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-method" id="data-randomfulltracewindowdataset---getitem--">

### RandomFullTraceWindowDataset.__getitem__

<div class="api-signature">

```python
axosim.data.RandomFullTraceWindowDataset.__getitem__(index: int) -> NeuronIOSample
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L356-L364)

</div>

Read one sample and its input/target contract.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>index</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Index of one dataset sample.</dd>
</dl>

<p class="api-label">Returns</p>

`NeuronIOSample`

</section>

<section class="api-method" id="data-randomfulltracewindowdataset-get-batch">

### RandomFullTraceWindowDataset.get_batch

<div class="api-signature">

```python
axosim.data.RandomFullTraceWindowDataset.get_batch(indices: range | list[int]) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L366-L383)

</div>

Read the requested input and target arrays as a batch.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Requested dataset sample indices.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd>Native inputs with shape (batch,time,input_channels).</dd>
<dt><code>targets</code> <span class="api-type">np.ndarray</span></dt>
<dd>Spike and soma targets with shape (batch,time,2).</dd>
</dl>

</section>

<section class="api-method" id="data-randomfulltracewindowdataset-get-sample-ids">

### RandomFullTraceWindowDataset.get_sample_ids

<div class="api-signature">

```python
axosim.data.RandomFullTraceWindowDataset.get_sample_ids(indices: range | list[int]) -> list[str]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L385-L386)

</div>

Return the sample identities associated with the selected indices.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Requested dataset sample indices.</dd>
</dl>

<p class="api-label">Returns</p>

`list[str]`

</section>

</section>

<section class="api-symbol" id="data-officialstylefulltracewindowdataset">

## OfficialStyleFullTraceWindowDataset

<div class="api-signature">

```python
axosim.data.OfficialStyleFullTraceWindowDataset(base: ShardedNeuronIODataset, *, window_size: int=500, start_offset: int=500, samples_per_epoch: int | None=None, batch_size: int=8, file_load_fraction: float=0.3, source_simulations: int=128, sequence_length: int | None=None, seed: int=0, cache_full_shards: bool=True)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L402-L543)

</div>

Deterministic port of the official NeuronIO file/simulation/time sampling policy.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>base</code> <span class="api-type">ShardedNeuronIODataset</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>window_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=500.</span> Native timesteps per extracted window.</dd>
<dt><code>start_offset</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=500.</span> Native timestep index before the first selected window.</dd>
<dt><code>samples_per_epoch</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Number of training window presentations requested per epoch.</dd>
<dt><code>batch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span> Examples processed per batch.</dd>
<dt><code>file_load_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.3.</span> Fraction of each shard made available to the sampling path.</dd>
<dt><code>source_simulations</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=128.</span> Number of source simulations included by the dataset declaration.</dd>
<dt><code>sequence_length</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Native timestep count of a trace.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed for the declared operation.</dd>
<dt><code>cache_full_shards</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Retain complete shard arrays rather than only selected data.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#data-officialstylefulltracewindowdataset---len--"><code>OfficialStyleFullTraceWindowDataset.__len__()</code></a></li>
<li><a href="#data-officialstylefulltracewindowdataset-reshuffle"><code>OfficialStyleFullTraceWindowDataset.reshuffle()</code></a></li>
<li><a href="#data-officialstylefulltracewindowdataset---getitem--"><code>OfficialStyleFullTraceWindowDataset.__getitem__()</code></a></li>
<li><a href="#data-officialstylefulltracewindowdataset-get-batch"><code>OfficialStyleFullTraceWindowDataset.get_batch()</code></a></li>
<li><a href="#data-officialstylefulltracewindowdataset-get-sample-ids"><code>OfficialStyleFullTraceWindowDataset.get_sample_ids()</code></a></li>
</ul>

<section class="api-method" id="data-officialstylefulltracewindowdataset---len--">

### OfficialStyleFullTraceWindowDataset.__len__

<div class="api-signature">

```python
axosim.data.OfficialStyleFullTraceWindowDataset.__len__() -> int
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L451-L452)

</div>

Return the number of indexed samples.

<p class="api-label">Returns</p>

`int`

</section>

<section class="api-method" id="data-officialstylefulltracewindowdataset-reshuffle">

### OfficialStyleFullTraceWindowDataset.reshuffle

<div class="api-signature">

```python
axosim.data.OfficialStyleFullTraceWindowDataset.reshuffle(seed: int) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L454-L482)

</div>

Reorder the enabled sampling index using the supplied seed.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Random seed for the declared operation.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-method" id="data-officialstylefulltracewindowdataset---getitem--">

### OfficialStyleFullTraceWindowDataset.__getitem__

<div class="api-signature">

```python
axosim.data.OfficialStyleFullTraceWindowDataset.__getitem__(index: int) -> NeuronIOSample
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L484-L492)

</div>

Read one sample and its input/target contract.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>index</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Index of one dataset sample.</dd>
</dl>

<p class="api-label">Returns</p>

`NeuronIOSample`

</section>

<section class="api-method" id="data-officialstylefulltracewindowdataset-get-batch">

### OfficialStyleFullTraceWindowDataset.get_batch

<div class="api-signature">

```python
axosim.data.OfficialStyleFullTraceWindowDataset.get_batch(indices: range | list[int]) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L494-L511)

</div>

Read the requested input and target arrays as a batch.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Requested dataset sample indices.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd>Native inputs with shape (batch,time,input_channels).</dd>
<dt><code>targets</code> <span class="api-type">np.ndarray</span></dt>
<dd>Spike and soma targets with shape (batch,time,2).</dd>
</dl>

</section>

<section class="api-method" id="data-officialstylefulltracewindowdataset-get-sample-ids">

### OfficialStyleFullTraceWindowDataset.get_sample_ids

<div class="api-signature">

```python
axosim.data.OfficialStyleFullTraceWindowDataset.get_sample_ids(indices: range | list[int]) -> list[str]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L513-L514)

</div>

Return the sample identities associated with the selected indices.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Requested dataset sample indices.</dd>
</dl>

<p class="api-label">Returns</p>

`list[str]`

</section>

</section>

<section class="api-symbol" id="data-write-demo-shards">

## write_demo_shards

<div class="api-signature">

```python
axosim.data.write_demo_shards(root: str | Path, *, shard_count: int=2, samples_per_shard: int=8, time_steps: int=32, input_dim: int=64, seed: int=0) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L546-L571)

</div>

Create small deterministic NeuronIO-style shards for smoke tests.

Creates deterministic synthetic shard files for pipeline checks. The generated targets are not biological reference data. Returns written shard paths.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Dataset shard directory or manifest root.</dd>
<dt><code>shard_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Number of synthetic shard files to write.</dd>
<dt><code>samples_per_shard</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span> Synthetic sample count in each generated shard.</dd>
<dt><code>time_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=32.</span> Native sequence horizon.</dd>
<dt><code>input_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=64.</span> Native input-channel count.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed for the declared operation.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>paths</code> <span class="api-type">list[Path]</span></dt>
<dd>Written synthetic shard paths. These shards exercise the reader and trainer contracts.</dd>
</dl>

<p class="api-label">Examples</p>

Create synthetic shards to verify the reader contract before using biological data.

```python
from tempfile import TemporaryDirectory
from axosim.data import ShardedNeuronIODataset, write_demo_shards

with TemporaryDirectory() as directory:
    write_demo_shards(directory, samples_per_shard=2, time_steps=12, input_dim=6)
    inputs, targets = ShardedNeuronIODataset(directory).get_batch([0, 1])
    print(inputs.shape, targets.shape)
```

```text
(2, 12, 6) (2, 12, 2)
```

</section>

<section class="api-symbol" id="data-repack-shards-as-npy">

## repack_shards_as_npy

<div class="api-signature">

```python
axosim.data.repack_shards_as_npy(input_root: str | Path, output_root: str | Path, *, input_dtype: np.dtype | type=np.int8) -> list[Path]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/data.py#L574-L617)

</div>

Repack existing shards as sliceable `.npy` arrays with identical sample order.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>input_root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Directory containing the source dataset shards.</dd>
<dt><code>output_root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Directory receiving converted dataset shards.</dd>
<dt><code>input_dtype</code> <span class="api-type">np.dtype | type</span></dt>
<dd><span class="api-default">keyword-only, default=np.int8.</span> Stored NumPy dtype of the converted input arrays.</dd>
</dl>

<p class="api-label">Returns</p>

`list[Path]`

</section>
