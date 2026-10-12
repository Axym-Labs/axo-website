---
title: Intervention inputs
description: Signatures, parameters, return values, and source for intervention inputs.
section: AxoBench API
apiGroup: Data
order: 308
---

## Overview

Input-side constructors for the five intervention conditions and a loader for paired intervention shards. Each constructor returns the edited inputs and a boolean mask of the baseline events it removed or moved. Producing teacher targets for new inputs requires the simulator stack in axobench.generation. [Paired interventions](/axobench/interventions/) describes the released conditions.

Source revision: `22e52ec6c023`. [Export index](/axobench-api/).

<section class="api-symbol" id="benchmark-structured-intervention-make-structured-intervention-inputs">

## make_structured_intervention_inputs

<div class="api-signature">

```python
axobench.benchmark.structured_intervention.make_structured_intervention_inputs(inputs: np.ndarray, *, intervention: str, seed: int=0, dropout_probability: float=0.35, jitter_steps: int=2, site_start_fraction: float=0.0, site_fraction: float=0.25) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/structured_intervention.py#L118-L165)

</div>

Apply one named condition with the released v1 parameters as defaults. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Signed inputs, (trace, time, channels) or (time, channels).</dd>
<dt><code>intervention</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, required.</span> event_dropout, exc_dropout, inh_dropout, temporal_jitter, or site_silence.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Seed of the random conditions.</dd>
<dt><code>dropout_probability</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.35.</span> Removal probability of the dropout conditions.</dd>
<dt><code>jitter_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Maximum absolute shift of temporal_jitter.</dd>
<dt><code>site_start_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Start of the silenced band as a fraction of the sites per sign.</dd>
<dt><code>site_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.25.</span> Width of the silenced band as a fraction of the sites per sign.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>intervened</code> <span class="api-type">np.ndarray</span></dt>
<dd>Edited inputs.</dd>
<dt><code>changed</code> <span class="api-type">np.ndarray</span></dt>
<dd>Boolean mask of edited baseline events.</dd>
<dt><code>metadata</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>Condition parameters and baseline, intervention, and changed event counts.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-structured-intervention-make-event-dropout-inputs">

## make_event_dropout_inputs

<div class="api-signature">

```python
axobench.benchmark.structured_intervention.make_event_dropout_inputs(inputs: np.ndarray, *, dropout_probability: float, seed: int=0) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/structured_intervention.py#L18-L36)

</div>

Remove each nonzero event independently with the given probability. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Signed inputs.</dd>
<dt><code>dropout_probability</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Removal probability in [0, 1].</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>intervened</code> <span class="api-type">np.ndarray</span></dt>
<dd>Edited inputs.</dd>
<dt><code>changed</code> <span class="api-type">np.ndarray</span></dt>
<dd>Mask of removed events.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-structured-intervention-make-selective-event-dropout-inputs">

## make_selective_event_dropout_inputs

<div class="api-signature">

```python
axobench.benchmark.structured_intervention.make_selective_event_dropout_inputs(inputs: np.ndarray, *, dropout_probability: float, event_sign: int, seed: int=0) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/structured_intervention.py#L39-L59)

</div>

Remove only excitatory (+1) or only inhibitory (-1) events with the given probability. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Signed inputs.</dd>
<dt><code>dropout_probability</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Removal probability in [0, 1].</dd>
<dt><code>event_sign</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> 1 for excitatory or -1 for inhibitory events.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>intervened</code> <span class="api-type">np.ndarray</span></dt>
<dd>Edited inputs.</dd>
<dt><code>changed</code> <span class="api-type">np.ndarray</span></dt>
<dd>Mask of removed events.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-structured-intervention-make-temporal-jitter-inputs">

## make_temporal_jitter_inputs

<div class="api-signature">

```python
axobench.benchmark.structured_intervention.make_temporal_jitter_inputs(inputs: np.ndarray, *, max_jitter_steps: int, seed: int=0) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/structured_intervention.py#L62-L87)

</div>

Move every event by an integer shift drawn uniformly from -max_jitter_steps to +max_jitter_steps, clipped to the trace. Events that land on the same step and channel merge. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Signed inputs.</dd>
<dt><code>max_jitter_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Maximum absolute shift; 0 returns a copy.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Random seed.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>intervened</code> <span class="api-type">np.ndarray</span></dt>
<dd>Edited inputs, (trace, time, channels).</dd>
<dt><code>changed</code> <span class="api-type">np.ndarray</span></dt>
<dd>Mask of baseline events that moved.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-structured-intervention-make-site-silence-inputs">

## make_site_silence_inputs

<div class="api-signature">

```python
axobench.benchmark.structured_intervention.make_site_silence_inputs(inputs: np.ndarray, *, start_fraction: float=0.0, site_fraction: float=0.25) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/structured_intervention.py#L90-L115)

</div>

Remove all events on a contiguous band of sites in both the excitatory and the inhibitory half of the channels. The band is a channel range; on a morphology that leaves some sites without a synapse it silences fewer effective synapses. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Signed inputs with excitatory and inhibitory halves.</dd>
<dt><code>start_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Start of the band as a fraction of the sites per sign.</dd>
<dt><code>site_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.25.</span> Width of the band as a fraction of the sites per sign; at least one site.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>intervened</code> <span class="api-type">np.ndarray</span></dt>
<dd>Edited inputs.</dd>
<dt><code>changed</code> <span class="api-type">np.ndarray</span></dt>
<dd>Mask of removed events.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-runner-load-intervention-pair-npz">

## load_intervention_pair_npz

<div class="api-signature">

```python
axobench.benchmark.runner.load_intervention_pair_npz(path: str | Path, *, max_samples: int | None=None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/runner.py#L38-L61)

</div>

Load the first pairs of a paired intervention shard. The file is opened with allow_pickle=True, so load only trusted files. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Pair shard.</dd>
<dt><code>max_samples</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Maximum pairs; None loads all.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>arrays</code> <span class="api-type">tuple</span></dt>
<dd>baseline_inputs, baseline_targets, intervention_inputs, intervention_targets, and the sample IDs.</dd>
</dl>

</section>
