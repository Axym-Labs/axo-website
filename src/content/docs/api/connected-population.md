---
title: Connected population lifecycle
description: Signatures, parameters, return contracts, and source for connected population lifecycle.
section: API reference
apiGroup: Populations
order: 201
---

## Overview

create_population constructs an actually connected Lite inference simulator from an explicitly supplied model and graph. Persistent state, thresholded recurrent events, native time and delayed deliveries belong to this object. Read the connected population guide for the complete lifecycle. AxoSimPopulation remains the separate supplied-history autograd interface. Reference and fused-neuron backends support the same explicit or deterministic procedural graphs; the historical specialized quantized large-population runtime has a different topology and timing contract.

Source revision: `0f546adfd8fc`. [Public export index](/api/).

<section class="api-symbol" id="connected-population-inputevents">

## InputEvents

<div class="api-signature">

```python
axosim.connected_population.InputEvents(neurons: Sequence[int] | torch.Tensor, channels: Sequence[int] | torch.Tensor, values: Sequence[float] | torch.Tensor)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L48-L68)

</div>

Sparse external inputs in the model's declared input encoding.

Owns equally sized one-dimensional CPU arrays; duplicate neuron/channel events add. Neuron/channel bounds and input signs are checked before a native step changes runtime state. Channel-encoded inputs must be nonnegative. Signed amplitudes must agree with channel_roles when declared. External values receive no second source-role sign.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>neurons</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer (events,) destination neuron IDs for one native input sample.</dd>
<dt><code>channels</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer (events,) Lite input-channel IDs, paired with neurons.</dd>
<dt><code>values</code> <span class="api-type">Sequence[float] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Finite (events,) native amplitudes in the declared input convention; no additional source sign is applied.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="connected-population-explicitconnectome">

## ExplicitConnectome

<div class="api-signature">

```python
axosim.connected_population.ExplicitConnectome(sources: Sequence[int] | torch.Tensor, targets: Sequence[int] | torch.Tensor, channels: Sequence[int] | torch.Tensor, delays: Sequence[int] | torch.Tensor, source_roles: Sequence[int] | torch.Tensor, efficacies: Sequence[float] | torch.Tensor)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L72-L110)

</div>

An exact directed multigraph with one efficacy per retained edge.

The six owned CPU arrays have equal length E. Parallel edges and ragged degrees are retained. Integer source/target bounds [0,n), channel bounds [0,input_dim), consistent source roles (+1/-1), and P4 delays >=4 ms are checked at population construction. Efficacies are independently stored nonnegative float32 magnitudes, including zero for a disabled edge. Edge ID is its original row index.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>sources</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer (E,) source neuron IDs; outgoing edges of one neuron must share a role.</dd>
<dt><code>targets</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer (E,) destination neuron IDs; ragged degrees and parallel edges are preserved.</dd>
<dt><code>channels</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer (E,) destination Lite input-channel IDs.</dd>
<dt><code>delays</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer (E,) native delivery delays in milliseconds; Lite requires each &gt;=4.</dd>
<dt><code>source_roles</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer (E,) source roles, +1 excitatory or -1 inhibitory.</dd>
<dt><code>efficacies</code> <span class="api-type">Sequence[float] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Finite nonnegative (E,) independent edge magnitudes; zero disables deliveries without deleting the edge.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="connected-population-explicitconnectome-edge-count"><code>ExplicitConnectome.edge_count: int</code></dt>
<dd>Number of retained edges, including parallel edges. <a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L108-L110">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="connected-population-proceduralconnectome">

## ProceduralConnectome

<div class="api-signature">

```python
axosim.connected_population.ProceduralConnectome(n: int, out_degree: int, input_dim: int, neuron_roles: Sequence[int] | torch.Tensor, channel_roles: Sequence[int] | torch.Tensor, delay_ms: int = 4, seed: int = 0, efficacy: float = 1.0)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L114-L184)

</div>

Implicit deterministic fan-out graph with an exact efficacy per edge.

Retains n*out_degree edges with edge ID source*out_degree+contact. Target ID is (source+seed+contact*104729)%n; channel cycles through declared channels matching the source role. Self and parallel edges are allowed. Any positive n is supported; source and channel roles must have shapes (n,) and (input_dim,), and each source role requires a matching channel. Topology is computed only for active sources, but exact mutable efficacies still require O(E) storage. This is a deterministic graph, not an empirical connectome or the old tiled unique-channel topology.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>n</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Positive population size; no power-of-two constraint.</dd>
<dt><code>out_degree</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Positive retained outgoing edge count per source; total E=n*out_degree.</dd>
<dt><code>input_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Destination input-channel count, matching the supplied Lite model.</dd>
<dt><code>neuron_roles</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer (n,) +1/-1 role for each source neuron.</dd>
<dt><code>channel_roles</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer (input_dim,) +1/-1 role for each destination input channel.</dd>
<dt><code>delay_ms</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=4.</span> Common native delivery delay in milliseconds; Lite population construction requires &gt;=4.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span> Nonnegative integer &lt;2**31 added to the deterministic target formula; not a random generator state.</dd>
<dt><code>efficacy</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=1.0.</span> Initial nonnegative float32 magnitude copied into all E independently mutable edges.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="connected-population-proceduralconnectome-edge-count"><code>ProceduralConnectome.edge_count: int</code></dt>
<dd>Exact retained edge count; implicit topology does not discard edges. <a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L168-L170">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#connected-population-proceduralconnectome-materialize"><code>ProceduralConnectome.materialize()</code></a></li>
</ul>

<section class="api-method" id="connected-population-proceduralconnectome-materialize">

### ProceduralConnectome.materialize

<div class="api-signature">

```python
axosim.connected_population.ProceduralConnectome.materialize() -> ExplicitConnectome
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L172-L184)

</div>

Return an equivalent owned explicit graph, allocating all E edges.

Allocates O(E) CPU edge-index arrays for the equivalent exact explicit multigraph. It preserves every procedural edge ID, role, destination channel, delay and initial efficacy; use for small topology inspection or parity checks.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>graph</code> <span class="api-type">ExplicitConnectome</span></dt>
<dd>Equivalent exact CPU multigraph with all E edge identities and initial efficacies.</dd>
</dl>

</section>

</section>

<section class="api-symbol" id="connected-population-populationframe">

## PopulationFrame

<div class="api-signature">

```python
axosim.connected_population.PopulationFrame(time_ms: int, valid: bool, signals: dict[str, torch.Tensor], neuron_ids: dict[str, torch.Tensor])
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L199-L212)

</div>

Owned selected tensors at one native timestamp.

Signals and matching row identities are selected before copying and stay on the simulation device. Returned frames own ordinary tensors, so later steps and caller edits do not change runtime buffers. valid=False identifies the first four causal-padding samples; spikes are always false there. Before any step, observe has time_ms=-1. The runtime time_ms attribute instead names the next sample to process.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>time_ms</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Processed native sample timestamp; -1 before the first step.</dd>
<dt><code>valid</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span> False for the first four causal-padding samples; true from timestamp 4 ms onward.</dd>
<dt><code>signals</code> <span class="api-type">dict[str, torch.Tensor]</span></dt>
<dd><span class="api-default">required.</span> Mapping of subscribed signal names to owned selected device tensors.</dd>
<dt><code>neuron_ids</code> <span class="api-type">dict[str, torch.Tensor]</span></dt>
<dd><span class="api-default">required.</span> Mapping of each signal name to its integer row identities in the same order.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="connected-population-connectedpopulation">

## ConnectedPopulation

<div class="api-signature">

```python
axosim.connected_population.ConnectedPopulation(*, model: AdaptiveSupportP4Surrogate, n: int, connectome: ExplicitConnectome | ProceduralConnectome, morphology_indices: Sequence[int] | torch.Tensor, input_encoding: Literal['signed', 'channel'], channel_roles: Sequence[int] | torch.Tensor | None=None, stream_inputs: StreamInput | None=None, stream_outputs: Mapping[str, Sequence[int] | torch.Tensor | Literal['all']] | None=None, backend: Literal['reference', 'fused']='reference', spike_threshold: float | Sequence[float] | torch.Tensor=0.0, sample_every_ms: int=1, soma_transform: tuple[float, float] | None=None, runtime_coefficients: torch.Tensor | None=None)
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L221-L905)

</div>

A state-owning, closed-loop inference simulator for a supplied Lite model.

Use create_population with the same keyword arguments. The reference backend executes the supplied Lite model on CPU or CUDA. The fused backend requires an explicitly CUDA FP16 Lite model and Triton; it fuses the neuron recurrence/decoder, not the old specialized million-neuron router. Edge efficacies and feature queue accumulation remain float32. stream_outputs=None selects all-neuron spikes; {} selects no signals. sample_every_ms applies to run; step always returns its native frame.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">AdaptiveSupportP4Surrogate</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Explicit trained AxoSimLite model, copied with its weights/configuration. The factory never chooses or initializes weights for you.</dd>
<dt><code>n</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Positive persistent neuron count.</dd>
<dt><code>connectome</code> <span class="api-type">ExplicitConnectome | ProceduralConnectome</span></dt>
<dd><span class="api-default">keyword-only, required.</span> ExplicitConnectome or ProceduralConnectome, copied and validated without altering topology/delays.</dd>
<dt><code>morphology_indices</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Integer (n,) assignments into model.config.morphology_ids, one per persistent neuron.</dd>
<dt><code>input_encoding</code> <span class="api-type">Literal[&#x27;signed&#x27;, &#x27;channel&#x27;]</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Required training-compatible convention: &#x27;signed&#x27; applies recurrent E/I sign; &#x27;channel&#x27; uses positive counts and inhibitory channel identity/features.</dd>
<dt><code>channel_roles</code> <span class="api-type">Sequence[int] | torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional integer (input_dim,) +1/-1 vector for explicit-graph and external-sign validation; the procedural schema carries its own vector.</dd>
<dt><code>stream_inputs</code> <span class="api-type">StreamInput | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Deterministic callback(time_ms) or owned timestamp mapping returning InputEvents, dense (n,input_dim) tensors, or None. Arbitrary iterators are rejected.</dd>
<dt><code>stream_outputs</code> <span class="api-type">Mapping[str, Sequence[int] | torch.Tensor | Literal[&#x27;all&#x27;]] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Signal-name to neuron-ID-selection mapping; &#x27;all&#x27; selects all rows. None defaults to all-neuron spikes; {} selects no signals.</dd>
<dt><code>backend</code> <span class="api-type">Literal[&#x27;reference&#x27;, &#x27;fused&#x27;]</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;reference&#x27;.</span> &#x27;reference&#x27; executes the actual Lite PyTorch step; &#x27;fused&#x27; requires CUDA FP16 plus Triton and fuses neuron recurrence/decoding only.</dd>
<dt><code>spike_threshold</code> <span class="api-type">float | Sequence[float] | torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Finite scalar or (n,) native spike-logit threshold; calibrate on development data. Warmup never emits spikes.</dd>
<dt><code>sample_every_ms</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Positive integer output-sampling cadence for run, aligned to absolute timestamps 0, k, 2k, ...; step always exports its native sample.</dd>
<dt><code>soma_transform</code> <span class="api-type">tuple[float, float] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional (positive scale_mv,offset_mv) affine transform: soma_mv=soma_target*scale_mv+offset_mv. Required to request soma_mv.</dd>
<dt><code>runtime_coefficients</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional finite (n,model.cache_width) packed coefficients. Otherwise compile the model&#x27;s morphology behavior rows, or use zeros when adaptation is disabled.</dd>
</dl>

<p class="api-label">Attributes</p>

<dl class="api-attributes">
<dt><code>n</code> <span class="api-type">int</span></dt>
<dd>Persistent population size.</dd>
<dt><code>time_ms</code> <span class="api-type">int</span></dt>
<dd>Next native sample timestamp; the latest observed frame has time_ms-1.</dd>
<dt><code>backend</code> <span class="api-type">str</span></dt>
<dd>Explicit reference or fused-neuron backend.</dd>
<dt><code>device</code> <span class="api-type">torch.device</span></dt>
<dd>Device inherited from the explicitly supplied Lite model.</dd>
<dt><code>dtype</code> <span class="api-type">torch.dtype</span></dt>
<dd>Neuron-execution dtype; edge efficacies and the feature queue remain float32.</dd>
<dt><code>input_encoding</code> <span class="api-type">str</span></dt>
<dd>Declared signed or channel input convention.</dd>
<dt><code>sample_every_ms</code> <span class="api-type">int</span></dt>
<dd>Absolute-timestamp observation cadence used by run.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="connected-population-connectedpopulation-connectome"><code>ConnectedPopulation.connectome: ExplicitConnectome | ProceduralConnectome</code></dt>
<dd>Owned graph-schema copy; editing it cannot change validated runtime topology. <a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L489-L491">Source</a></dd>
<dt id="connected-population-connectedpopulation-morphology-indices"><code>ConnectedPopulation.morphology_indices: torch.Tensor</code></dt>
<dd>Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron. <a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L494-L496">Source</a></dd>
<dt id="connected-population-connectedpopulation-efficacies"><code>ConnectedPopulation.efficacies: torch.Tensor</code></dt>
<dd>Positive floating-point contact multipliers, shaped by the retained topology. <a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L499-L501">Source</a></dd>
<dt id="connected-population-connectedpopulation-thresholds"><code>ConnectedPopulation.thresholds: torch.Tensor</code></dt>
<dd>Owned ``(n,)`` snapshot of native spike-logit thresholds. <a href="https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L504-L506">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#connected-population-connectedpopulation-set-efficacies"><code>ConnectedPopulation.set_efficacies()</code></a></li>
<li><a href="#connected-population-connectedpopulation-set-thresholds"><code>ConnectedPopulation.set_thresholds()</code></a></li>
<li><a href="#connected-population-connectedpopulation-step"><code>ConnectedPopulation.step()</code></a></li>
<li><a href="#connected-population-connectedpopulation-run"><code>ConnectedPopulation.run()</code></a></li>
<li><a href="#connected-population-connectedpopulation-observe"><code>ConnectedPopulation.observe()</code></a></li>
<li><a href="#connected-population-connectedpopulation-state-dict"><code>ConnectedPopulation.state_dict()</code></a></li>
<li><a href="#connected-population-connectedpopulation-load-state-dict"><code>ConnectedPopulation.load_state_dict()</code></a></li>
<li><a href="#connected-population-connectedpopulation-reset"><code>ConnectedPopulation.reset()</code></a></li>
</ul>

<section class="api-method" id="connected-population-connectedpopulation-set-efficacies">

### ConnectedPopulation.set_efficacies

<div class="api-signature">

```python
axosim.connected_population.ConnectedPopulation.set_efficacies(edge_ids: Sequence[int] | torch.Tensor, values: Sequence[float] | torch.Tensor) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L508-L538)

</div>

Set selected nonnegative edge magnitudes; queued deliveries are unchanged.

edge_ids is a unique integer selection into E retained edges; values is an equally sized finite nonnegative array. Values are stored as float32 even for FP16 neuron execution. An emitted event uses its emission-time efficacy; already scheduled deliveries do not change.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>edge_ids</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Unique valid integer retained-edge IDs.</dd>
<dt><code>values</code> <span class="api-type">Sequence[float] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Equally sized finite nonnegative edge magnitudes, stored as float32.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-method" id="connected-population-connectedpopulation-set-thresholds">

### ConnectedPopulation.set_thresholds

<div class="api-signature">

```python
axosim.connected_population.ConnectedPopulation.set_thresholds(values: float | Sequence[float] | torch.Tensor) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L540-L547)

</div>

Replace scalar or per-neuron spike-logit thresholds for future samples.

values is a finite scalar or (n,) vector in spike-logit coordinates. Changes future native threshold decisions; warmup remains spike-free at any finite threshold.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>values</code> <span class="api-type">float | Sequence[float] | torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Finite scalar or (n,) threshold vector in native spike-logit coordinates.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-method" id="connected-population-connectedpopulation-step">

### ConnectedPopulation.step

<div class="api-signature">

```python
axosim.connected_population.ConnectedPopulation.step(inputs: InputEvents | torch.Tensor | None=None) -> PopulationFrame
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L710-L719)

</div>

Advance one native millisecond and return an owned subscribed frame.

Advances one native 1-ms sample. Optional sparse InputEvents or dense inputs (n,input_dim) add to the configured native-time stream. The returned frame contains only subscribed signals. At timestamps 3,7,11,... hidden_state is updated from the completed patch; spike/soma values are the current sample from the preceding forecast. State is held between these boundaries.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">InputEvents | torch.Tensor | None</span></dt>
<dd><span class="api-default">default=None.</span> Optional InputEvents or dense (n,input_dim) native sample, added to the configured stream at the current timestamp.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>frame</code> <span class="api-type">PopulationFrame</span></dt>
<dd>Owned subscribed signals and row identities at the native sample just processed; population.time_ms now names the next sample.</dd>
</dl>

</section>

<section class="api-method" id="connected-population-connectedpopulation-run">

### ConnectedPopulation.run

<div class="api-signature">

```python
axosim.connected_population.ConnectedPopulation.run(duration_ms: int) -> Iterator[PopulationFrame]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L721-L739)

</div>

Yield sampled frames while continuing state for exactly duration_ms steps.

Consuming the iterator advances exactly duration_ms native steps unless iteration is stopped early. Observations are copied/yielded only at absolute timestamps divisible by sample_every_ms; intervening steps still execute. The consumer controls progress, with no background/unbounded output queue. Coarse samples do not aggregate skipped spikes: use sample_every_ms=1 for the complete event history. duration_ms=0 does not advance.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>duration_ms</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Nonnegative integer number of native 1-ms steps to execute when consumed.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>frames</code> <span class="api-type">Iterator[PopulationFrame]</span></dt>
<dd>Owned frames at requested absolute sample timestamps; consuming the iterator executes all intervening native steps.</dd>
</dl>

</section>

<section class="api-method" id="connected-population-connectedpopulation-observe">

### ConnectedPopulation.observe

<div class="api-signature">

```python
axosim.connected_population.ConnectedPopulation.observe(*, neurons: Sequence[int] | torch.Tensor | None=None, signals: Sequence[str] | None=None) -> PopulationFrame
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L742-L783)

</div>

Copy selected current signals without advancing state or time.

Copies selected signals without advancing time. Without arguments, uses the output subscriptions. With signals, neurons selects a shared row order (all neurons when omitted). Known signals: spikes (L,) bool; spike_logit (L,) native logit; soma_target (L,) native coordinate; soma_mv (L,) validated affine millivolts; hidden_state (L,state_dim) learned state; input_features (L,route_feature_dim) current routed input. soma_mv requires soma_transform=(positive scale_mv,offset_mv).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>neurons</code> <span class="api-type">Sequence[int] | torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Selected neuron IDs in desired row order; omit for all neurons when signals is supplied.</dd>
<dt><code>signals</code> <span class="api-type">Sequence[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Known signal names; omit to use output subscriptions. Supplying neurons requires an explicit signals selection.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>frame</code> <span class="api-type">PopulationFrame</span></dt>
<dd>Owned selected current signals and neuron IDs without any time/state advance.</dd>
</dl>

</section>

<section class="api-method" id="connected-population-connectedpopulation-state-dict">

### ConnectedPopulation.state_dict

<div class="api-signature">

```python
axosim.connected_population.ConnectedPopulation.state_dict() -> dict[str, object]
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L827-L854)

</div>

Return owned device tensors sufficient for queue/phase/state replay.

Returns owned runtime tensors: learned state, partial patch, forecasts, delayed queue, current routed features/outputs/spikes, thresholds, direct coefficients and exact efficacies, plus version, clock, validity and model/topology fingerprint. Save with torch.save; read with torch.load(...,weights_only=True). Recreate the same model/topology/encoding/backend; weights and topology are not embedded. A native-time input callback must reproduce the same value on replay; arbitrary callback/random state is not saved.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>state</code> <span class="api-type">dict[str, object]</span></dt>
<dd>Owned runtime tensors, native clock/validity, schema version and model/topology identity fingerprint; weights and external callback state are not embedded.</dd>
</dl>

</section>

<section class="api-method" id="connected-population-connectedpopulation-load-state-dict">

### ConnectedPopulation.load_state_dict

<div class="api-signature">

```python
axosim.connected_population.ConnectedPopulation.load_state_dict(state: Mapping[str, object]) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L857-L901)

</div>

Restore a compatible owned snapshot; reject mismatch before mutation.

Checks identity, time/validity, complete tensor schema, shapes, dtypes, finite values and nonnegative efficacies before any runtime mutation. Compatible tensor values are transferred to the execution device. The external stream remains the configured callback or owned timestamp mapping.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>state</code> <span class="api-type">Mapping[str, object]</span></dt>
<dd><span class="api-default">required.</span> Owned compatible runtime snapshot returned by state_dict or read with weights_only=True.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-method" id="connected-population-connectedpopulation-reset">

### ConnectedPopulation.reset

<div class="api-signature">

```python
axosim.connected_population.ConnectedPopulation.reset() -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L903-L905)

</div>

Restore construction-time clock, state, empty queue, thresholds and efficacies.

Restores construction-time state, zero clock, empty delayed queue, initial forecasts/patch, original thresholds, runtime coefficients and exact edge efficacies. External callbacks must likewise return their original timestamp-dependent inputs.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

</section>

<section class="api-symbol" id="connected-population-create-population">

## create_population

<div class="api-signature">

```python
axosim.connected_population.create_population(*, model: AdaptiveSupportP4Surrogate, n: int, connectome: ExplicitConnectome | ProceduralConnectome, morphology_indices: Sequence[int] | torch.Tensor, input_encoding: Literal['signed', 'channel'], channel_roles: Sequence[int] | torch.Tensor | None=None, stream_inputs: StreamInput | None=None, stream_outputs: Mapping[str, Sequence[int] | torch.Tensor | Literal['all']] | None=None, backend: Literal['reference', 'fused']='reference', spike_threshold: float | Sequence[float] | torch.Tensor=0.0, sample_every_ms: int=1, soma_transform: tuple[float, float] | None=None, runtime_coefficients: torch.Tensor | None=None) -> ConnectedPopulation
```

[Source](https://github.com/Axym-Labs/axosim/blob/0f546adfd8fc8530ff8ec0952ce7a1367616cf24/src/axosim/connected_population.py#L908-L949)

</div>

Create an actually connected Lite inference simulation from supplied weights.

The model is mandatory and must be AxoSimLite (AdaptiveSupportP4Surrogate). Morphology indices have shape (n,) and address the model's declared vocabulary. One native step is 1 ms, and recurrent delays must be integer >=4 ms; graph delays are never adjusted. 'signed' applies the source role to recurrent event amplitude; 'channel' uses nonnegative counts with inhibition encoded by channel identity/features. External amplitudes are already in that convention. Every outgoing edge of a source must declare the same role, and channel_roles validates destination-channel compatibility when supplied. Model weights, graph topology, morphology assignments and initial banks are copied rather than borrowed. The connected threshold/event loop is inference-only.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">AdaptiveSupportP4Surrogate</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Explicit trained AxoSimLite model, copied with its weights/configuration. The factory never chooses or initializes weights for you.</dd>
<dt><code>n</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Positive persistent neuron count.</dd>
<dt><code>connectome</code> <span class="api-type">ExplicitConnectome | ProceduralConnectome</span></dt>
<dd><span class="api-default">keyword-only, required.</span> ExplicitConnectome or ProceduralConnectome, copied and validated without altering topology/delays.</dd>
<dt><code>morphology_indices</code> <span class="api-type">Sequence[int] | torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Integer (n,) assignments into model.config.morphology_ids, one per persistent neuron.</dd>
<dt><code>input_encoding</code> <span class="api-type">Literal[&#x27;signed&#x27;, &#x27;channel&#x27;]</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Required training-compatible convention: &#x27;signed&#x27; applies recurrent E/I sign; &#x27;channel&#x27; uses positive counts and inhibitory channel identity/features.</dd>
<dt><code>channel_roles</code> <span class="api-type">Sequence[int] | torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional integer (input_dim,) +1/-1 vector for explicit-graph and external-sign validation; the procedural schema carries its own vector.</dd>
<dt><code>stream_inputs</code> <span class="api-type">StreamInput | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Deterministic callback(time_ms) or owned timestamp mapping returning InputEvents, dense (n,input_dim) tensors, or None. Arbitrary iterators are rejected.</dd>
<dt><code>stream_outputs</code> <span class="api-type">Mapping[str, Sequence[int] | torch.Tensor | Literal[&#x27;all&#x27;]] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Signal-name to neuron-ID-selection mapping; &#x27;all&#x27; selects all rows. None defaults to all-neuron spikes; {} selects no signals.</dd>
<dt><code>backend</code> <span class="api-type">Literal[&#x27;reference&#x27;, &#x27;fused&#x27;]</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;reference&#x27;.</span> &#x27;reference&#x27; executes the actual Lite PyTorch step; &#x27;fused&#x27; requires CUDA FP16 plus Triton and fuses neuron recurrence/decoding only.</dd>
<dt><code>spike_threshold</code> <span class="api-type">float | Sequence[float] | torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Finite scalar or (n,) native spike-logit threshold; calibrate on development data. Warmup never emits spikes.</dd>
<dt><code>sample_every_ms</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Positive integer output-sampling cadence for run, aligned to absolute timestamps 0, k, 2k, ...; step always exports its native sample.</dd>
<dt><code>soma_transform</code> <span class="api-type">tuple[float, float] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional (positive scale_mv,offset_mv) affine transform: soma_mv=soma_target*scale_mv+offset_mv. Required to request soma_mv.</dd>
<dt><code>runtime_coefficients</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional finite (n,model.cache_width) packed coefficients. Otherwise compile the model&#x27;s morphology behavior rows, or use zeros when adaptation is disabled.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>population</code> <span class="api-type">ConnectedPopulation</span></dt>
<dd>State-owning Lite inference simulator with closed-loop delayed recurrence, exact edge efficacies and selected timestamped observations.</dd>
</dl>

</section>
