---
title: Checkpoints
description: Signatures, parameters, return contracts, and source for checkpoints.
section: API reference
apiGroup: Models
order: 210
---

## Overview

Checkpoint files contain model_kind, config, state_dict, and metadata. save_checkpoint writes a temporary sibling then atomically replaces the destination. Model-only checkpoints do not store a complete optimizer or scheduler trajectory. load_checkpoint uses torch.load with weights_only=False, so load trusted artifacts.

Source revision: `0f546adfd8fc`. [Public export index](/api/).

<section class="api-symbol" id="checkpoint-save-checkpoint">

## save_checkpoint

<div class="api-signature">

```python
axosim.checkpoint.save_checkpoint(model: torch.nn.Module, path: str | Path, *, metadata: dict[str, Any] | None=None) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/checkpoint.py#L188-L206)

</div>

Serialize supported model weights, configuration, model kind, and caller metadata.

Writes model kind, serializable configuration, state_dict, and metadata. Creates parent directories. Unsupported model types raise TypeError. Returns None.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">torch.nn.Module</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Filesystem location to read or write; see the operation&#x27;s persistence contract.</dd>
<dt><code>metadata</code> <span class="api-type">dict[str, Any] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Caller metadata stored with model state.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-symbol" id="checkpoint-load-checkpoint">

## load_checkpoint

<div class="api-signature">

```python
axosim.checkpoint.load_checkpoint(path: str | Path, *, map_location: str='cpu') -> tuple[torch.nn.Module, dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/checkpoint.py#L209-L329)

</div>

Reconstruct a supported model and its stored metadata from a trusted checkpoint.

Returns (reconstructed torch.nn.Module, metadata dictionary). Supports baseline/branch_elm, official, branch-trace-rnn, axomamba and axomamba-pytorch, axo-temporal variants, axo-block-forecast variants, adaptive P4 variants, and generic Mamba kinds. An unknown kind raises ValueError; PyTorch artifacts are loaded with weights_only=False.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Filesystem location to read or write; see the operation&#x27;s persistence contract.</dd>
<dt><code>map_location</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;cpu&#x27;.</span> PyTorch destination for loaded tensors.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">torch.nn.Module</span></dt>
<dd>Reconstructed model with its stored weights, architecture configuration, and backend.</dd>
<dt><code>metadata</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>Metadata stored with the checkpoint; an empty dictionary when absent.</dd>
</dl>

</section>
