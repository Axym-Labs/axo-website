---
title: Connectivity builders
description: Signatures, parameters, return contracts, and source for connectivity builders.
section: API reference
apiGroup: Populations
order: 202
---

## Overview

PyNN-style builders wire one population of n neurons, optionally restricted to pre source and post target IDs, and return an ordinary validated ExplicitConnectome for create_population. Each edge takes its source neuron's role (neuron_roles, +1 or -1; None makes every neuron excitatory) and a destination channel drawn uniformly from the checkpoint channels with that role (channel_roles), unless explicit channels are given. Efficacies and delays are constants, one value per edge, or callables fn(sources, targets, generator); delays are integer native milliseconds of at least MIN_DELAY_MS = 4, the Lite P4 recurrent minimum. One seeded generator is drawn in a fixed order (topology, channels, efficacies, delays), so a seed reproduces the exact graph, and edge IDs follow the returned edge order. Shared keyword arguments are neuron_roles, channel_roles, channels, efficacies, and delays. The builders are exported from axosim; MIN_DELAY_MS is imported from axosim.connectors.

Source revision: `caef7be03abd`. [Public export index](/api/).

<section class="api-symbol" id="connectors-all-to-all">

## all_to_all

<div class="api-signature">

```python
axosim.connectors.all_to_all(n: int, *, seed: int=0, allow_self: bool=False, pre=None, post=None, **kwargs) -> ExplicitConnectome
```

[Source](https://github.com/Axym-Labs/axosim/blob/caef7be03abdbde76ab00080ba7c4866da81278e/src/axosim/connectors.py#L58-L74)

</div>

Connect every ``pre`` neuron to every ``post`` neuron once (source-major).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>n</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Positive population size; neuron IDs are 0..n-1.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Integer seed of the one generator drawn for topology, channels, efficacies, and delays, in that order; equal seeds give identical graphs.</dd>
<dt><code>allow_self</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Keep edges from a neuron to itself.</dd>
<dt><code>pre</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Source neuron IDs; None uses all n neurons.</dd>
<dt><code>post</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Target neuron IDs; None uses all n neurons.</dd>
<dt><code>kwargs</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span> Shared edge options: neuron_roles ((n,) +1/-1, default all excitatory), channel_roles (the checkpoint&#x27;s (input_dim,) +1/-1 vector, required unless channels is given), channels, efficacies (default 1.0), and delays (default 4 ms). Values are a constant, one per edge, or a callable fn(sources, targets, generator).</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>connectome</code> <span class="api-type">ExplicitConnectome</span></dt>
<dd>One edge per (pre, post) pair, source-major, without self-edges unless allow_self.</dd>
</dl>

</section>

<section class="api-symbol" id="connectors-one-to-one">

## one_to_one

<div class="api-signature">

```python
axosim.connectors.one_to_one(n: int, *, seed: int=0, pre=None, post=None, **kwargs) -> ExplicitConnectome
```

[Source](https://github.com/Axym-Labs/axosim/blob/caef7be03abdbde76ab00080ba7c4866da81278e/src/axosim/connectors.py#L77-L84)

</div>

Connect ``pre[i]`` to ``post[i]``; the default ``pre == post`` gives autapses.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>n</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Positive population size; neuron IDs are 0..n-1.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Integer seed of the one generator drawn for topology, channels, efficacies, and delays, in that order; equal seeds give identical graphs.</dd>
<dt><code>pre</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Source neuron IDs; None uses all n neurons.</dd>
<dt><code>post</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Target neuron IDs; None uses all n neurons.</dd>
<dt><code>kwargs</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span> Shared edge options: neuron_roles ((n,) +1/-1, default all excitatory), channel_roles (the checkpoint&#x27;s (input_dim,) +1/-1 vector, required unless channels is given), channels, efficacies (default 1.0), and delays (default 4 ms). Values are a constant, one per edge, or a callable fn(sources, targets, generator).</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>connectome</code> <span class="api-type">ExplicitConnectome</span></dt>
<dd>Edges pre[i] -&gt; post[i]; pre and post must have equal length.</dd>
</dl>

</section>

<section class="api-symbol" id="connectors-fixed-probability">

## fixed_probability

<div class="api-signature">

```python
axosim.connectors.fixed_probability(n: int, p: float | Callable[[torch.Tensor, torch.Tensor], torch.Tensor], *, seed: int=0, allow_self: bool=False, pre=None, post=None, **kwargs) -> ExplicitConnectome
```

[Source](https://github.com/Axym-Labs/axosim/blob/caef7be03abdbde76ab00080ba7c4866da81278e/src/axosim/connectors.py#L87-L126)

</div>

Keep each ``pre -> post`` pair independently with probability ``p``.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>n</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Positive population size; neuron IDs are 0..n-1.</dd>
<dt><code>p</code> <span class="api-type">float | Callable[[torch.Tensor, torch.Tensor], torch.Tensor]</span></dt>
<dd><span class="api-default">required.</span> Connection probability in [0, 1], or a callable p(sources, targets) returning one probability per candidate pair, evaluated in chunks; for example a distance-dependent kernel over neuron positions.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Integer seed of the one generator drawn for topology, channels, efficacies, and delays, in that order; equal seeds give identical graphs.</dd>
<dt><code>allow_self</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Keep edges from a neuron to itself.</dd>
<dt><code>pre</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Source neuron IDs; None uses all n neurons.</dd>
<dt><code>post</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Target neuron IDs; None uses all n neurons.</dd>
<dt><code>kwargs</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span> Shared edge options: neuron_roles ((n,) +1/-1, default all excitatory), channel_roles (the checkpoint&#x27;s (input_dim,) +1/-1 vector, required unless channels is given), channels, efficacies (default 1.0), and delays (default 4 ms). Values are a constant, one per edge, or a callable fn(sources, targets, generator).</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>connectome</code> <span class="api-type">ExplicitConnectome</span></dt>
<dd>Independently kept pairs in source-major order, without parallel edges.</dd>
</dl>

</section>

<section class="api-symbol" id="connectors-fixed-indegree">

## fixed_indegree

<div class="api-signature">

```python
axosim.connectors.fixed_indegree(n: int, k: int, *, seed: int=0, allow_self: bool=False, with_replacement: bool=False, pre=None, post=None, **kwargs) -> ExplicitConnectome
```

[Source](https://github.com/Axym-Labs/axosim/blob/caef7be03abdbde76ab00080ba7c4866da81278e/src/axosim/connectors.py#L129-L170)

</div>

Give every ``post`` neuron exactly ``k`` sources drawn uniformly from ``pre``.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>n</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Positive population size; neuron IDs are 0..n-1.</dd>
<dt><code>k</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Nonnegative number of sources per post neuron.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Integer seed of the one generator drawn for topology, channels, efficacies, and delays, in that order; equal seeds give identical graphs.</dd>
<dt><code>allow_self</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Keep edges from a neuron to itself.</dd>
<dt><code>with_replacement</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Draw sources with replacement; repeated draws become parallel edges. Without replacement the k sources of a target are distinct.</dd>
<dt><code>pre</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Source neuron IDs; None uses all n neurons.</dd>
<dt><code>post</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Target neuron IDs; None uses all n neurons.</dd>
<dt><code>kwargs</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span> Shared edge options: neuron_roles ((n,) +1/-1, default all excitatory), channel_roles (the checkpoint&#x27;s (input_dim,) +1/-1 vector, required unless channels is given), channels, efficacies (default 1.0), and delays (default 4 ms). Values are a constant, one per edge, or a callable fn(sources, targets, generator).</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>connectome</code> <span class="api-type">ExplicitConnectome</span></dt>
<dd>Exactly k edges into every post neuron, ordered by target, then source.</dd>
</dl>

</section>

<section class="api-symbol" id="connectors-from-list">

## from_list

<div class="api-signature">

```python
axosim.connectors.from_list(n: int, edges, *, efficacies: EdgeValues | None=None, delays: EdgeValues | None=None, seed: int=0, **kwargs) -> ExplicitConnectome
```

[Source](https://github.com/Axym-Labs/axosim/blob/caef7be03abdbde76ab00080ba7c4866da81278e/src/axosim/connectors.py#L173-L215)

</div>

Build from rows ``(source, target[, efficacy[, delay]])`` in the given order.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>n</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Positive population size; neuron IDs are 0..n-1.</dd>
<dt><code>edges</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">required.</span> Rows (source, target[, efficacy[, delay]]) in edge order; integer neuron IDs in [0, n).</dd>
<dt><code>efficacies</code> <span class="api-type">EdgeValues | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Nonnegative edge magnitudes: a constant, one value per edge, or a callable; exclusive with an efficacy column. None means 1.0.</dd>
<dt><code>delays</code> <span class="api-type">EdgeValues | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer native delays of at least 4 ms: a constant, one value per edge, or a callable; exclusive with a delay column. None means 4 ms.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Integer seed of the one generator drawn for topology, channels, efficacies, and delays, in that order; equal seeds give identical graphs.</dd>
<dt><code>kwargs</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span> Shared edge options: neuron_roles ((n,) +1/-1, default all excitatory), channel_roles (the checkpoint&#x27;s (input_dim,) +1/-1 vector, required unless channels is given), channels, efficacies (default 1.0), and delays (default 4 ms). Values are a constant, one per edge, or a callable fn(sources, targets, generator).</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>connectome</code> <span class="api-type">ExplicitConnectome</span></dt>
<dd>The listed edges in the given order.</dd>
</dl>

</section>

<section class="api-symbol" id="connectors-concatenate">

## concatenate

<div class="api-signature">

```python
axosim.connectors.concatenate(*connectomes: ExplicitConnectome) -> ExplicitConnectome
```

[Source](https://github.com/Axym-Labs/axosim/blob/caef7be03abdbde76ab00080ba7c4866da81278e/src/axosim/connectors.py#L218-L238)

</div>

Join graphs edge-wise; part ``i``'s edge IDs follow those of parts ``< i``.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>connectomes</code> <span class="api-type">ExplicitConnectome</span></dt>
<dd><span class="api-default">variadic.</span> ExplicitConnectome parts; the outgoing edges of each neuron must share one role across parts.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>connectome</code> <span class="api-type">ExplicitConnectome</span></dt>
<dd>All edges joined; the edge IDs of part i follow those of the parts before it.</dd>
</dl>

</section>
