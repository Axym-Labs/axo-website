---
title: AxoBench prediction adapters
description: Signatures, parameters, return contracts, and source for axobench prediction adapters.
section: API reference
apiGroup: Data
order: 222
---

## Overview

Prediction adapters reconstruct checkpoint models, select morphology identities, and return NumPy arrays in AxoBench's expected coordinates. The current AxoBench package is an additional dependency for the CLI evaluator. The source supports native and streaming predictor options in Python; the CLI exposes its declared subset.

Source revision: `0f546adfd8fc`. [Public export index](/api/).

<section class="api-symbol" id="axobench-iteration-make-official-elm-predictor">

## make_official_elm_predictor

<div class="api-signature">

```python
axosim.axobench_iteration.make_official_elm_predictor(config_path: str | Path, checkpoint_path: str | Path, *, device: str='auto', dtype: str | torch.dtype='float32') -> tuple[Callable[[np.ndarray], np.ndarray], dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/axobench_iteration.py#L22-L83)

</div>

Load an upstream Branch-ELM checkpoint on the shared AxoBench contract.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>config_path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Architecture JSON used to reconstruct the upstream baseline.</dd>
<dt><code>checkpoint_path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Trusted model-weight file to reconstruct or evaluate.</dd>
<dt><code>device</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;auto&#x27;.</span> Execution or allocation device.</dd>
<dt><code>dtype</code> <span class="api-type">str | torch.dtype</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;float32&#x27;.</span> Floating-point execution or allocation dtype.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>predict</code> <span class="api-type">Callable[[np.ndarray], np.ndarray]</span></dt>
<dd>Upstream Branch-ELM predictor on the shared AxoBench target-coordinate contract.</dd>
<dt><code>metadata</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>Configuration, checkpoint identity, parameter counts, dtype, and output conventions.</dd>
</dl>

</section>

<section class="api-symbol" id="axobench-iteration-make-checkpoint-predictor">

## make_checkpoint_predictor

<div class="api-signature">

```python
axosim.axobench_iteration.make_checkpoint_predictor(checkpoint: str | Path, *, device: str='auto', dtype: str | torch.dtype='float32', streaming: bool=False, streaming_chunk_size: int | None=None) -> tuple[Callable[[np.ndarray], np.ndarray], dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/axobench_iteration.py#L86-L189)

</div>

Load a standard AxoSim checkpoint as an AxoBench prediction callable.

Returns (predictor,metadata). The predictor accepts native NumPy inputs (B,T,C), optionally with morphology IDs when supported, and returns floating-point NumPy (B,T,2) outputs in AxoBench coordinates. Streaming requires the checkpoint's streaming API. Metadata includes resident parameter count and inference dtype.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>checkpoint</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Upstream baseline checkpoint file.</dd>
<dt><code>device</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;auto&#x27;.</span> Execution or allocation device.</dd>
<dt><code>dtype</code> <span class="api-type">str | torch.dtype</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;float32&#x27;.</span> Floating-point execution or allocation dtype.</dd>
<dt><code>streaming</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Use the checkpoint&#x27;s explicit streaming-state interface.</dd>
<dt><code>streaming_chunk_size</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Chunk size passed to a supported streaming backend.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>predict</code> <span class="api-type">Callable[[np.ndarray], np.ndarray]</span></dt>
<dd>Prediction function mapping native inputs (B,T,C) to spike logits and normalized soma targets (B,T,2).</dd>
<dt><code>metadata</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>Stored checkpoint metadata plus parameter counts, inference dtype, and streaming configuration.</dd>
</dl>

</section>
