---
title: Trace datasets
description: Signatures, parameters, return values, and source for trace datasets.
section: AxoBench API
apiGroup: Data
order: 306
---

## Overview

ShardedNeuronIODataset reads a split directory of NPZ shards, or of NPY shards listed in a manifest, as used by every AxoBench release. Inputs are returned as float32 (batch, time, channels) and targets as float32 (batch, time, 2). See [single-neuron traces](/axobench/single-neuron/#download-and-load) for an example.

Source revision: `22e52ec6c023`. [Export index](/axobench-api/).

<section class="api-symbol" id="data-shardedneuroniodataset">

## ShardedNeuronIODataset

<div class="api-signature">

```python
axobench.data.ShardedNeuronIODataset(root: str | Path, *, shuffle: bool=False, seed: int=0, shuffle_mode: Literal['sample', 'shard']='sample', cache_shards: int=0)
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L28-L185)

</div>

Deterministic reader for a directory of shards. With a manifest.json, the index follows the manifest entries whose shards are present; otherwise every *.npz file is read in sorted order. Reading a trace decodes the input array of its whole shard.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Split directory.</dd>
<dt><code>shuffle</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Shuffle the index at construction and on reshuffle.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Seed of the initial shuffle.</dd>
<dt><code>shuffle_mode</code> <span class="api-type">Literal[&#x27;sample&#x27;, &#x27;shard&#x27;]</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;sample&#x27;.</span> &#x27;sample&#x27; permutes all traces; &#x27;shard&#x27; permutes shards and the traces within each shard.</dd>
<dt><code>cache_shards</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Decoded shards kept in an LRU cache; 0 disables caching.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#data-shardedneuroniodataset---len--"><code>ShardedNeuronIODataset.__len__()</code></a></li>
<li><a href="#data-shardedneuroniodataset-reshuffle"><code>ShardedNeuronIODataset.reshuffle()</code></a></li>
<li><a href="#data-shardedneuroniodataset---getitem--"><code>ShardedNeuronIODataset.__getitem__()</code></a></li>
<li><a href="#data-shardedneuroniodataset-get-batch"><code>ShardedNeuronIODataset.get_batch()</code></a></li>
<li><a href="#data-shardedneuroniodataset-get-sample-ids"><code>ShardedNeuronIODataset.get_sample_ids()</code></a></li>
<li><a href="#data-shardedneuroniodataset-get-optional-array-batch"><code>ShardedNeuronIODataset.get_optional_array_batch()</code></a></li>
</ul>

<section class="api-method" id="data-shardedneuroniodataset---len--">

### ShardedNeuronIODataset.__len__

<div class="api-signature">

```python
axobench.data.ShardedNeuronIODataset.__len__() -> int
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L67-L68)

</div>

Number of indexed traces.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>count</code> <span class="api-type">int</span></dt>
<dd>Trace count.</dd>
</dl>

</section>

<section class="api-method" id="data-shardedneuroniodataset-reshuffle">

### ShardedNeuronIODataset.reshuffle

<div class="api-signature">

```python
axobench.data.ShardedNeuronIODataset.reshuffle(seed: int) -> None
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L70-L78)

</div>

Reshuffle the index with a new seed; no effect unless shuffle=True.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Shuffle seed.</dd>
</dl>

</section>

<section class="api-method" id="data-shardedneuroniodataset---getitem--">

### ShardedNeuronIODataset.__getitem__

<div class="api-signature">

```python
axobench.data.ShardedNeuronIODataset.__getitem__(index: int) -> NeuronIOSample
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L80-L89)

</div>

Load one trace.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>index</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Position in the index.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>sample</code> <span class="api-type">NeuronIOSample</span></dt>
<dd>Sample ID, (time, channels) inputs, and (time, 2) targets.</dd>
</dl>

</section>

<section class="api-method" id="data-shardedneuroniodataset-get-batch">

### ShardedNeuronIODataset.get_batch

<div class="api-signature">

```python
axobench.data.ShardedNeuronIODataset.get_batch(indices: range | list[int]) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L91-L99)

</div>

Load several traces. Consecutive indices from the same shard are read together, so sorted indices minimize shard reads.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Positions in the index.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd>float32 (batch, time, channels).</dd>
<dt><code>targets</code> <span class="api-type">np.ndarray</span></dt>
<dd>float32 (batch, time, 2).</dd>
</dl>

</section>

<section class="api-method" id="data-shardedneuroniodataset-get-sample-ids">

### ShardedNeuronIODataset.get_sample_ids

<div class="api-signature">

```python
axobench.data.ShardedNeuronIODataset.get_sample_ids(indices: range | list[int]) -> list[str]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L101-L102)

</div>

Sample IDs of the given positions.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Positions in the index.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>sample_ids</code> <span class="api-type">list[str]</span></dt>
<dd>Sample IDs in order.</dd>
</dl>

</section>

<section class="api-method" id="data-shardedneuroniodataset-get-optional-array-batch">

### ShardedNeuronIODataset.get_optional_array_batch

<div class="api-signature">

```python
axobench.data.ShardedNeuronIODataset.get_optional_array_batch(name: str, indices: range | list[int]) -> np.ndarray | None
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L104-L116)

</div>

Load an additional per-trace array, such as soma_mv or context_index, from NPZ shards.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Array name in the shard.</dd>
<dt><code>indices</code> <span class="api-type">range | list[int]</span></dt>
<dd><span class="api-default">required.</span> Positions in the index.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>array</code> <span class="api-type">np.ndarray | None</span></dt>
<dd>Concatenated values, or None when a shard lacks the array or is stored as NPY files.</dd>
</dl>

</section>

</section>

<section class="api-symbol" id="data-neuroniosample">

## NeuronIOSample

<div class="api-signature">

```python
axobench.data.NeuronIOSample(sample_id: str, inputs: np.ndarray, targets: np.ndarray)
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L13-L16)

</div>

One trace returned by indexing a dataset.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>sample_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Sample ID.</dd>
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Inputs, (time, channels).</dd>
<dt><code>targets</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Targets, (time, 2).</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="data-write-demo-shards">

## write_demo_shards

<div class="api-signature">

```python
axobench.data.write_demo_shards(root: str | Path, *, shard_count: int=2, samples_per_shard: int=8, time_steps: int=32, input_dim: int=64, seed: int=0) -> None
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L479-L504)

</div>

Write small deterministic shards with random signed events and a synthetic target, for smoke tests only.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Output directory.</dd>
<dt><code>shard_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Number of shards.</dd>
<dt><code>samples_per_shard</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span> Traces per shard.</dd>
<dt><code>time_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=32.</span> Steps per trace.</dd>
<dt><code>input_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=64.</span> Input channels.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed.</dd>
</dl>

</section>

<section class="api-symbol" id="data-repack-shards-as-npy">

## repack_shards_as_npy

<div class="api-signature">

```python
axobench.data.repack_shards_as_npy(input_root: str | Path, output_root: str | Path, *, input_dtype: np.dtype | type=np.int8) -> list[Path]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/data.py#L507-L550)

</div>

Repack shards as separate .npy arrays with a manifest, preserving the trace order, so arrays can be memory-mapped. Raises ValueError if input_dtype would change values.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>input_root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Source split directory.</dd>
<dt><code>output_root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Destination directory.</dd>
<dt><code>input_dtype</code> <span class="api-type">np.dtype | type</span></dt>
<dd><span class="api-default">keyword-only, default=np.int8.</span> Storage dtype of the inputs.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>paths</code> <span class="api-type">list[Path]</span></dt>
<dd>Written input files.</dd>
</dl>

</section>
