---
title: Connectome routing
description: Signatures, parameters, return contracts, and source for connectome routing.
section: API reference
apiGroup: Populations
order: 214
---

## Overview

The routing modules construct procedural contact identities and delayed event delivery. ProceduralMorphologyConnectomeRouter retains morphology-conditioned branch targeting. Population IDs, local/long-range source identities, delay slots, and route topology must agree with the declared workload; procedural routing does not imply an empirical connectome.

Source revision: `856207f6de56`. [Public export index](/api/).

<section class="api-symbol" id="connectome-delaybucket">

## DelayBucket

<div class="api-signature">

```python
axosim.connectome.DelayBucket(delay_steps: int, first_fanout_offset: int, event_count_per_source: int, local_targets: bool)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L24-L35)

</div>

Routing metadata for contacts with one delivery delay.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>delay_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>first_fanout_offset</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>event_count_per_source</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>local_targets</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="connectome-delaybucket-fanout-offsets"><code>DelayBucket.fanout_offsets: tuple[int, ...]</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L31-L35">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="connectome-procedural-delay-buckets">

## procedural_delay_buckets

<div class="api-signature">

```python
axosim.connectome.procedural_delay_buckets(*, fanout: int, local_fanout: int, minimum_delay_steps: int=1) -> tuple[DelayBucket, ...]
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L38-L71)

</div>

Partition fanout offsets into local/long-range delay classes.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>fanout</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>local_fanout</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>minimum_delay_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span></dd>
</dl>

<p class="api-label">Returns</p>

`tuple[DelayBucket, ...]`

</section>

<section class="api-symbol" id="connectome-compact-active-sources">

## compact_active_sources

<div class="api-signature">

```python
axosim.connectome.compact_active_sources(outputs: torch.Tensor, *, threshold: float=0.0) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L74-L86)

</div>

Return source-sorted int32 indices whose scalar output fires.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>outputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Number of readout channels.</dd>
<dt><code>threshold</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-symbol" id="connectome-build-typed-tile-pools">

## build_typed_tile_pools

<div class="api-signature">

```python
axosim.connectome.build_typed_tile_pools(source_is_inhibitory: torch.Tensor, physical_to_logical: torch.Tensor, *, spatial_tile_neurons: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L89-L164)

</div>

Build invertible logical E/I ranks within every spatial tile.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>source_is_inhibitory</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>physical_to_logical</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>spatial_tile_neurons</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
</dl>

<p class="api-label">Returns</p>

`tuple[torch.Tensor, torch.Tensor, torch.Tensor]`

</section>

<section class="api-symbol" id="connectome-build-external-count-branch-bank">

## build_external_count_branch_bank

<div class="api-signature">

```python
axosim.connectome.build_external_count_branch_bank(*, slot_map: torch.Tensor, morphology_gain: torch.Tensor, feature_gain: torch.Tensor, synapses_per_branch: int, max_event_count: int=32, channels_per_type: int | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L167-L261)

</div>

Precompute exact branch currents for a consecutive event pattern.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>slot_map</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>morphology_gain</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>feature_gain</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>synapses_per_branch</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>max_event_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=32.</span></dd>
<dt><code>channels_per_type</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-symbol" id="connectome-trajectoryexternalbranchdrive">

## TrajectoryExternalBranchDrive

<div class="api-signature">

```python
axosim.connectome.TrajectoryExternalBranchDrive(*, trajectories: torch.Tensor, branch_bank: torch.Tensor, logical_ids: torch.Tensor, morphology: torch.Tensor, seed: int, excitatory_gain: float, inhibitory_gain: float, slot_map: torch.Tensor | None=None, morphology_gain: torch.Tensor | None=None, feature_gain: torch.Tensor | None=None, synapses_per_branch: int | None=None, block_rows: int=8, block_branches: int=128)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L1514-L1768)

</div>

Exact native-time trajectory drive at the learned branch boundary.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>trajectories</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>branch_bank</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>logical_ids</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>morphology</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Enable gradients on morphology-shared adaptation rows.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Random seed for the declared operation.</dd>
<dt><code>excitatory_gain</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>inhibitory_gain</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>slot_map</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>morphology_gain</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>feature_gain</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>synapses_per_branch</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>block_rows</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span></dd>
<dt><code>block_branches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=128.</span></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#connectome-trajectoryexternalbranchdrive-materialize"><code>TrajectoryExternalBranchDrive.materialize()</code></a></li>
</ul>

<section class="api-method" id="connectome-trajectoryexternalbranchdrive-materialize">

### TrajectoryExternalBranchDrive.materialize

<div class="api-signature">

```python
axosim.connectome.TrajectoryExternalBranchDrive.materialize(step: int, *, output: torch.Tensor | None=None, add_existing: bool=False, existing: torch.Tensor | None=None, recurrent_bits: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L1642-L1768)

</div>

Materialize exact branch currents for one native timestep.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>step</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>output</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>add_existing</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span></dd>
<dt><code>existing</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>recurrent_bits</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="connectome-proceduralbinarychannelconnectomerouter">

## ProceduralBinaryChannelConnectomeRouter

<div class="api-signature">

```python
axosim.connectome.ProceduralBinaryChannelConnectomeRouter(contract: LargePopulationSimulationContract, *, slot_map: torch.Tensor, morphology: torch.Tensor, source_is_inhibitory: torch.Tensor, morphology_gain: torch.Tensor, feature_gain: torch.Tensor, synapses_per_branch: int, physical_to_logical: torch.Tensor | None=None, logical_to_physical: torch.Tensor | None=None, route_block_size: int=512, route_num_warps: int=4, branch_block_rows: int=8, branch_block_size: int=128)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L1771-L2083)

</div>

Exact delayed routing in AxoBench's signed binary-channel space.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>contract</code> <span class="api-type">LargePopulationSimulationContract</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>slot_map</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>morphology</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Enable gradients on morphology-shared adaptation rows.</dd>
<dt><code>source_is_inhibitory</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>morphology_gain</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>feature_gain</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>synapses_per_branch</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>physical_to_logical</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>logical_to_physical</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>route_block_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=512.</span></dd>
<dt><code>route_num_warps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=4.</span></dd>
<dt><code>branch_block_rows</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span></dd>
<dt><code>branch_block_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=128.</span></dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="connectome-proceduralbinarychannelconnectomerouter-queue-bytes"><code>ProceduralBinaryChannelConnectomeRouter.queue_bytes: int</code></dt>
<dd>Physical storage allocated to the delayed event queue. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L1952-L1953">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#connectome-proceduralbinarychannelconnectomerouter-current-channel-bits"><code>ProceduralBinaryChannelConnectomeRouter.current_channel_bits()</code></a></li>
<li><a href="#connectome-proceduralbinarychannelconnectomerouter-current-inputs"><code>ProceduralBinaryChannelConnectomeRouter.current_inputs()</code></a></li>
<li><a href="#connectome-proceduralbinarychannelconnectomerouter-clear-and-route"><code>ProceduralBinaryChannelConnectomeRouter.clear_and_route()</code></a></li>
</ul>

<section class="api-method" id="connectome-proceduralbinarychannelconnectomerouter-current-channel-bits">

### ProceduralBinaryChannelConnectomeRouter.current_channel_bits

<div class="api-signature">

```python
axosim.connectome.ProceduralBinaryChannelConnectomeRouter.current_channel_bits(current_slot: int) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L1955-L1957)

</div>

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>current_slot</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="connectome-proceduralbinarychannelconnectomerouter-current-inputs">

### ProceduralBinaryChannelConnectomeRouter.current_inputs

<div class="api-signature">

```python
axosim.connectome.ProceduralBinaryChannelConnectomeRouter.current_inputs(current_slot: int, *, output: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L1959-L2018)

</div>

Convert one exact binary channel slot to learned branch currents.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>current_slot</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>output</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="connectome-proceduralbinarychannelconnectomerouter-clear-and-route">

### ProceduralBinaryChannelConnectomeRouter.clear_and_route

<div class="api-signature">

```python
axosim.connectome.ProceduralBinaryChannelConnectomeRouter.clear_and_route(active_sources: torch.Tensor, *, current_slot: int, clear_consumed: bool=True) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2020-L2079)

</div>

Clear a consumed slot and OR new delayed recurrent channels.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>active_sources</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>current_slot</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>clear_consumed</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="connectome-proceduralexactbranchconnectomerouter">

## ProceduralExactBranchConnectomeRouter

<div class="api-signature">

```python
axosim.connectome.ProceduralExactBranchConnectomeRouter(*args, external_trajectories: torch.Tensor | None=None, external_seed: int=0, external_excitatory_gain: float=1.0, external_inhibitory_gain: float=1.0, max_external_event_count: int=32, **kwargs)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2086-L2277)

</div>

Sparse exact-OR routing with ready-to-consume branch currents.

Bases: `ProceduralBinaryChannelConnectomeRouter`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>args</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span></dd>
<dt><code>external_trajectories</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>external_seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span></dd>
<dt><code>external_excitatory_gain</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span></dd>
<dt><code>external_inhibitory_gain</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span></dd>
<dt><code>max_external_event_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=32.</span></dd>
<dt><code>kwargs</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span></dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="connectome-proceduralexactbranchconnectomerouter-queue-bytes"><code>ProceduralExactBranchConnectomeRouter.queue_bytes: int</code></dt>
<dd>Physical storage allocated to the delayed event queue. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2150-L2156">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#connectome-proceduralexactbranchconnectomerouter-current-inputs"><code>ProceduralExactBranchConnectomeRouter.current_inputs()</code></a></li>
<li><a href="#connectome-proceduralexactbranchconnectomerouter-clear-and-route"><code>ProceduralExactBranchConnectomeRouter.clear_and_route()</code></a></li>
</ul>

<section class="api-method" id="connectome-proceduralexactbranchconnectomerouter-current-inputs">

### ProceduralExactBranchConnectomeRouter.current_inputs

<div class="api-signature">

```python
axosim.connectome.ProceduralExactBranchConnectomeRouter.current_inputs(current_slot: int, *, output: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2158-L2179)

</div>

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>current_slot</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>output</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="connectome-proceduralexactbranchconnectomerouter-clear-and-route">

### ProceduralExactBranchConnectomeRouter.clear_and_route

<div class="api-signature">

```python
axosim.connectome.ProceduralExactBranchConnectomeRouter.clear_and_route(active_sources: torch.Tensor, *, current_slot: int, current_step: int | None=None, clear_consumed: bool=True) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2181-L2277)

</div>

Clear consumed state and route each binary channel at most once.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>active_sources</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>current_slot</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>current_step</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>clear_consumed</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="connectome-proceduralmorphologyconnectomerouter">

## ProceduralMorphologyConnectomeRouter

<div class="api-signature">

```python
axosim.connectome.ProceduralMorphologyConnectomeRouter(contract: LargePopulationSimulationContract, *, slot_map: torch.Tensor, morphology: torch.Tensor, source_is_inhibitory: torch.Tensor, morphology_gain: torch.Tensor, feature_gain: torch.Tensor, synapses_per_branch: int, physical_to_logical: torch.Tensor | None=None, logical_to_physical: torch.Tensor | None=None, route_block_size: int=512, route_num_warps: int=4)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2280-L2606)

</div>

Persistent delay-queue router for the scalable connectome control.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>contract</code> <span class="api-type">LargePopulationSimulationContract</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>slot_map</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>morphology</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Enable gradients on morphology-shared adaptation rows.</dd>
<dt><code>source_is_inhibitory</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>morphology_gain</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>feature_gain</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>synapses_per_branch</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>physical_to_logical</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>logical_to_physical</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>route_block_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=512.</span></dd>
<dt><code>route_num_warps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=4.</span></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#connectome-proceduralmorphologyconnectomerouter-current-inputs"><code>ProceduralMorphologyConnectomeRouter.current_inputs()</code></a></li>
<li><a href="#connectome-proceduralmorphologyconnectomerouter-clear-and-route"><code>ProceduralMorphologyConnectomeRouter.clear_and_route()</code></a></li>
<li><a href="#connectome-proceduralmorphologyconnectomerouter-clear-recorded-branches"><code>ProceduralMorphologyConnectomeRouter.clear_recorded_branches()</code></a></li>
</ul>

<section class="api-method" id="connectome-proceduralmorphologyconnectomerouter-current-inputs">

### ProceduralMorphologyConnectomeRouter.current_inputs

<div class="api-signature">

```python
axosim.connectome.ProceduralMorphologyConnectomeRouter.current_inputs(current_slot: int) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2447-L2449)

</div>

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>current_slot</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="connectome-proceduralmorphologyconnectomerouter-clear-and-route">

### ProceduralMorphologyConnectomeRouter.clear_and_route

<div class="api-signature">

```python
axosim.connectome.ProceduralMorphologyConnectomeRouter.clear_and_route(active_sources: torch.Tensor, *, current_slot: int, clear_consumed: bool=True, touched_offsets: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2451-L2577)

</div>

Clear a consumed queue slot and schedule new delayed events.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>active_sources</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>current_slot</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>clear_consumed</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span></dd>
<dt><code>touched_offsets</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="connectome-proceduralmorphologyconnectomerouter-clear-recorded-branches">

### ProceduralMorphologyConnectomeRouter.clear_recorded_branches

<div class="api-signature">

```python
axosim.connectome.ProceduralMorphologyConnectomeRouter.clear_recorded_branches(touched_offsets: torch.Tensor) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2579-L2602)

</div>

Clear branch queue destinations recorded by event delivery.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>touched_offsets</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

</section>

<section class="api-symbol" id="connectome-proceduraluniquechannelconnectomerouter">

## ProceduralUniqueChannelConnectomeRouter

<div class="api-signature">

```python
axosim.connectome.ProceduralUniqueChannelConnectomeRouter(*args, synaptic_efficacy_bank: QuantizedSynapticEfficacyBank | None=None, external_trajectories: torch.Tensor | None=None, external_seed: int=0, external_excitatory_gain: float=1.0, external_inhibitory_gain: float=1.0, max_external_event_count: int=32, allow_repeated_source_target_pairs: bool=False, **kwargs)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2609-L3007)

</div>

Collision-free typed fan-in with invertible event-wise routing.

Bases: `ProceduralMorphologyConnectomeRouter`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>args</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span></dd>
<dt><code>synaptic_efficacy_bank</code> <span class="api-type">QuantizedSynapticEfficacyBank | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>external_trajectories</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>external_seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span></dd>
<dt><code>external_excitatory_gain</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span></dd>
<dt><code>external_inhibitory_gain</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span></dd>
<dt><code>max_external_event_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=32.</span></dd>
<dt><code>allow_repeated_source_target_pairs</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span></dd>
<dt><code>kwargs</code> <span class="api-type">unannotated</span></dt>
<dd><span class="api-default">variadic.</span></dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="connectome-proceduraluniquechannelconnectomerouter-queue-bytes"><code>ProceduralUniqueChannelConnectomeRouter.queue_bytes: int</code></dt>
<dd>Physical storage allocated to the delayed event queue. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2756-L2757">Source</a></dd>
<dt id="connectome-proceduraluniquechannelconnectomerouter-recorded-offsets-per-source"><code>ProceduralUniqueChannelConnectomeRouter.recorded_offsets_per_source: int</code></dt>
<dd>Candidate offset slots needed to record one routed source. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2760-L2779">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#connectome-proceduraluniquechannelconnectomerouter-clear-and-route"><code>ProceduralUniqueChannelConnectomeRouter.clear_and_route()</code></a></li>
</ul>

<section class="api-method" id="connectome-proceduraluniquechannelconnectomerouter-clear-and-route">

### ProceduralUniqueChannelConnectomeRouter.clear_and_route

<div class="api-signature">

```python
axosim.connectome.ProceduralUniqueChannelConnectomeRouter.clear_and_route(active_sources: torch.Tensor, *, current_slot: int, current_step: int | None=None, clear_consumed: bool=True, touched_offsets: torch.Tensor | None=None, unique_rows: torch.Tensor | None=None, unique_row_flags: torch.Tensor | None=None, unique_row_count: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/connectome.py#L2781-L3007)

</div>

Route the exact selected typed channel for each active source.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>active_sources</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>current_slot</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span></dd>
<dt><code>current_step</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>clear_consumed</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span></dd>
<dt><code>touched_offsets</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>unique_rows</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>unique_row_flags</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
<dt><code>unique_row_count</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span></dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>
