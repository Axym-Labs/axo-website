---
title: Connectome routing
description: Signatures, parameters, return contracts, and source for connectome routing.
section: API reference
order: 213
---

## Module contract

The routing modules construct procedural contact identities and delayed event delivery. ProceduralMorphologyConnectomeRouter retains morphology-conditioned branch targeting. Population IDs, local/long-range source identities, delay slots, and route topology must agree with the declared workload; procedural routing does not imply an empirical connectome.

Source revision: `306a51ed950b`. [Public export index](/api/).

## DelayBucket

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L24-L35)

```python
DelayBucket(delay_steps: int, first_fanout_offset: int, event_count_per_source: int, local_targets: bool) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `delay_steps` | `int` | required |
| `first_fanout_offset` | `int` | required |
| `event_count_per_source` | `int` | required |
| `local_targets` | `bool` | required |

### DelayBucket.fanout_offsets

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L31-L35)

```python
DelayBucket.fanout_offsets: tuple[int, ...]
```

Read-only property. Access as `instance.fanout_offsets`; do not call it as a function.

Returns `tuple[int, ...]`.

## procedural_delay_buckets

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L38-L71)

```python
procedural_delay_buckets(*, fanout: int, local_fanout: int, minimum_delay_steps: int=1) -> tuple[DelayBucket, ...]
```

Partition fanout offsets into local/long-range delay classes.

| Parameter | Type | Default |
| --- | --- | --- |
| `fanout` | `int` | required |
| `local_fanout` | `int` | required |
| `minimum_delay_steps` | `int` | `1` |

Returns `tuple[DelayBucket, ...]`.

## compact_active_sources

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L74-L86)

```python
compact_active_sources(outputs: torch.Tensor, *, threshold: float=0.0) -> torch.Tensor
```

Return source-sorted int32 indices whose scalar output fires.

| Parameter | Type | Default |
| --- | --- | --- |
| `outputs` | `torch.Tensor` | required |
| `threshold` | `float` | `0.0` |

Returns `torch.Tensor`.

## build_typed_tile_pools

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L89-L164)

```python
build_typed_tile_pools(source_is_inhibitory: torch.Tensor, physical_to_logical: torch.Tensor, *, spatial_tile_neurons: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]
```

Build invertible logical E/I ranks within every spatial tile.

| Parameter | Type | Default |
| --- | --- | --- |
| `source_is_inhibitory` | `torch.Tensor` | required |
| `physical_to_logical` | `torch.Tensor` | required |
| `spatial_tile_neurons` | `int` | required |

Returns `tuple[torch.Tensor, torch.Tensor, torch.Tensor]`.

## build_external_count_branch_bank

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L167-L261)

```python
build_external_count_branch_bank(*, slot_map: torch.Tensor, morphology_gain: torch.Tensor, feature_gain: torch.Tensor, synapses_per_branch: int, max_event_count: int=32, channels_per_type: int | None=None) -> torch.Tensor
```

Precompute exact branch currents for a consecutive event pattern.

| Parameter | Type | Default |
| --- | --- | --- |
| `slot_map` | `torch.Tensor` | required |
| `morphology_gain` | `torch.Tensor` | required |
| `feature_gain` | `torch.Tensor` | required |
| `synapses_per_branch` | `int` | required |
| `max_event_count` | `int` | `32` |
| `channels_per_type` | `int \| None` | `None` |

Returns `torch.Tensor`.

## TrajectoryExternalBranchDrive

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L1514-L1768)

Exact native-time trajectory drive at the learned branch boundary.

### TrajectoryExternalBranchDrive.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L1517-L1640)

```python
__init__(self, *, trajectories: torch.Tensor, branch_bank: torch.Tensor, logical_ids: torch.Tensor, morphology: torch.Tensor, seed: int, excitatory_gain: float, inhibitory_gain: float, slot_map: torch.Tensor | None=None, morphology_gain: torch.Tensor | None=None, feature_gain: torch.Tensor | None=None, synapses_per_branch: int | None=None, block_rows: int=8, block_branches: int=128) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `trajectories` | `torch.Tensor` | required |
| `branch_bank` | `torch.Tensor` | required |
| `logical_ids` | `torch.Tensor` | required |
| `morphology` | `torch.Tensor` | required |
| `seed` | `int` | required |
| `excitatory_gain` | `float` | required |
| `inhibitory_gain` | `float` | required |
| `slot_map` | `torch.Tensor \| None` | `None` |
| `morphology_gain` | `torch.Tensor \| None` | `None` |
| `feature_gain` | `torch.Tensor \| None` | `None` |
| `synapses_per_branch` | `int \| None` | `None` |
| `block_rows` | `int` | `8` |
| `block_branches` | `int` | `128` |

`seed`: Random seed for the declared operation.

Returns `None`.

### TrajectoryExternalBranchDrive.materialize

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L1642-L1768)

```python
materialize(self, step: int, *, output: torch.Tensor | None=None, add_existing: bool=False, existing: torch.Tensor | None=None, recurrent_bits: torch.Tensor | None=None) -> torch.Tensor
```

Materialize exact branch currents for one native timestep.

| Parameter | Type | Default |
| --- | --- | --- |
| `step` | `int` | required |
| `output` | `torch.Tensor \| None` | `None` |
| `add_existing` | `bool` | `False` |
| `existing` | `torch.Tensor \| None` | `None` |
| `recurrent_bits` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

## ProceduralBinaryChannelConnectomeRouter

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L1771-L2083)

Exact delayed routing in AxoBench's signed binary-channel space.

### ProceduralBinaryChannelConnectomeRouter.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L1774-L1949)

```python
__init__(self, contract: LargePopulationSimulationContract, *, slot_map: torch.Tensor, morphology: torch.Tensor, source_is_inhibitory: torch.Tensor, morphology_gain: torch.Tensor, feature_gain: torch.Tensor, synapses_per_branch: int, physical_to_logical: torch.Tensor | None=None, logical_to_physical: torch.Tensor | None=None, route_block_size: int=512, route_num_warps: int=4, branch_block_rows: int=8, branch_block_size: int=128) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `contract` | `LargePopulationSimulationContract` | required |
| `slot_map` | `torch.Tensor` | required |
| `morphology` | `torch.Tensor` | required |
| `source_is_inhibitory` | `torch.Tensor` | required |
| `morphology_gain` | `torch.Tensor` | required |
| `feature_gain` | `torch.Tensor` | required |
| `synapses_per_branch` | `int` | required |
| `physical_to_logical` | `torch.Tensor \| None` | `None` |
| `logical_to_physical` | `torch.Tensor \| None` | `None` |
| `route_block_size` | `int` | `512` |
| `route_num_warps` | `int` | `4` |
| `branch_block_rows` | `int` | `8` |
| `branch_block_size` | `int` | `128` |

Returns `None`.

### ProceduralBinaryChannelConnectomeRouter.queue_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L1952-L1953)

```python
ProceduralBinaryChannelConnectomeRouter.queue_bytes: int
```

Read-only property. Access as `instance.queue_bytes`; do not call it as a function.

Returns `int`.

### ProceduralBinaryChannelConnectomeRouter.current_channel_bits

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L1955-L1957)

```python
current_channel_bits(self, current_slot: int) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `current_slot` | `int` | required |

Returns `torch.Tensor`.

### ProceduralBinaryChannelConnectomeRouter.current_inputs

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L1959-L2018)

```python
current_inputs(self, current_slot: int, *, output: torch.Tensor | None=None) -> torch.Tensor
```

Convert one exact binary channel slot to learned branch currents.

| Parameter | Type | Default |
| --- | --- | --- |
| `current_slot` | `int` | required |
| `output` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### ProceduralBinaryChannelConnectomeRouter.clear_and_route

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2020-L2079)

```python
clear_and_route(self, active_sources: torch.Tensor, *, current_slot: int, clear_consumed: bool=True) -> torch.Tensor
```

Clear a consumed slot and OR new delayed recurrent channels.

| Parameter | Type | Default |
| --- | --- | --- |
| `active_sources` | `torch.Tensor` | required |
| `current_slot` | `int` | required |
| `clear_consumed` | `bool` | `True` |

Returns `torch.Tensor`.

## ProceduralExactBranchConnectomeRouter

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2086-L2277)

Sparse exact-OR routing with ready-to-consume branch currents.

Bases: `ProceduralBinaryChannelConnectomeRouter`.

### ProceduralExactBranchConnectomeRouter.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2091-L2147)

```python
__init__(self, *args, external_trajectories: torch.Tensor | None=None, external_seed: int=0, external_excitatory_gain: float=1.0, external_inhibitory_gain: float=1.0, max_external_event_count: int=32, **kwargs) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `args` | `unspecified` | `variadic` |
| `external_trajectories` | `torch.Tensor \| None` | `None` |
| `external_seed` | `int` | `0` |
| `external_excitatory_gain` | `float` | `1.0` |
| `external_inhibitory_gain` | `float` | `1.0` |
| `max_external_event_count` | `int` | `32` |
| `kwargs` | `unspecified` | `variadic` |

Returns `None`.

### ProceduralExactBranchConnectomeRouter.queue_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2150-L2156)

```python
ProceduralExactBranchConnectomeRouter.queue_bytes: int
```

Read-only property. Access as `instance.queue_bytes`; do not call it as a function.

Returns `int`.

### ProceduralExactBranchConnectomeRouter.current_inputs

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2158-L2179)

```python
current_inputs(self, current_slot: int, *, output: torch.Tensor | None=None) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `current_slot` | `int` | required |
| `output` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### ProceduralExactBranchConnectomeRouter.clear_and_route

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2181-L2277)

```python
clear_and_route(self, active_sources: torch.Tensor, *, current_slot: int, current_step: int | None=None, clear_consumed: bool=True) -> torch.Tensor
```

Clear consumed state and route each binary channel at most once.

| Parameter | Type | Default |
| --- | --- | --- |
| `active_sources` | `torch.Tensor` | required |
| `current_slot` | `int` | required |
| `current_step` | `int \| None` | `None` |
| `clear_consumed` | `bool` | `True` |

Returns `torch.Tensor`.

## ProceduralMorphologyConnectomeRouter

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2280-L2606)

Persistent delay-queue router for the scalable connectome control.

### ProceduralMorphologyConnectomeRouter.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2283-L2445)

```python
__init__(self, contract: LargePopulationSimulationContract, *, slot_map: torch.Tensor, morphology: torch.Tensor, source_is_inhibitory: torch.Tensor, morphology_gain: torch.Tensor, feature_gain: torch.Tensor, synapses_per_branch: int, physical_to_logical: torch.Tensor | None=None, logical_to_physical: torch.Tensor | None=None, route_block_size: int=512, route_num_warps: int=4) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `contract` | `LargePopulationSimulationContract` | required |
| `slot_map` | `torch.Tensor` | required |
| `morphology` | `torch.Tensor` | required |
| `source_is_inhibitory` | `torch.Tensor` | required |
| `morphology_gain` | `torch.Tensor` | required |
| `feature_gain` | `torch.Tensor` | required |
| `synapses_per_branch` | `int` | required |
| `physical_to_logical` | `torch.Tensor \| None` | `None` |
| `logical_to_physical` | `torch.Tensor \| None` | `None` |
| `route_block_size` | `int` | `512` |
| `route_num_warps` | `int` | `4` |

Returns `None`.

### ProceduralMorphologyConnectomeRouter.current_inputs

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2447-L2449)

```python
current_inputs(self, current_slot: int) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `current_slot` | `int` | required |

Returns `torch.Tensor`.

### ProceduralMorphologyConnectomeRouter.clear_and_route

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2451-L2577)

```python
clear_and_route(self, active_sources: torch.Tensor, *, current_slot: int, clear_consumed: bool=True, touched_offsets: torch.Tensor | None=None) -> torch.Tensor
```

Clear a consumed queue slot and schedule new delayed events.

| Parameter | Type | Default |
| --- | --- | --- |
| `active_sources` | `torch.Tensor` | required |
| `current_slot` | `int` | required |
| `clear_consumed` | `bool` | `True` |
| `touched_offsets` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### ProceduralMorphologyConnectomeRouter.clear_recorded_branches

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2579-L2602)

```python
clear_recorded_branches(self, touched_offsets: torch.Tensor) -> None
```

Clear branch queue destinations recorded by event delivery.

| Parameter | Type | Default |
| --- | --- | --- |
| `touched_offsets` | `torch.Tensor` | required |

Returns `None`.

## ProceduralUniqueChannelConnectomeRouter

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2609-L3007)

Collision-free typed fan-in with invertible event-wise routing.

Bases: `ProceduralMorphologyConnectomeRouter`.

### ProceduralUniqueChannelConnectomeRouter.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2614-L2753)

```python
__init__(self, *args, synaptic_efficacy_bank: QuantizedSynapticEfficacyBank | None=None, external_trajectories: torch.Tensor | None=None, external_seed: int=0, external_excitatory_gain: float=1.0, external_inhibitory_gain: float=1.0, max_external_event_count: int=32, allow_repeated_source_target_pairs: bool=False, **kwargs) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `args` | `unspecified` | `variadic` |
| `synaptic_efficacy_bank` | `QuantizedSynapticEfficacyBank \| None` | `None` |
| `external_trajectories` | `torch.Tensor \| None` | `None` |
| `external_seed` | `int` | `0` |
| `external_excitatory_gain` | `float` | `1.0` |
| `external_inhibitory_gain` | `float` | `1.0` |
| `max_external_event_count` | `int` | `32` |
| `allow_repeated_source_target_pairs` | `bool` | `False` |
| `kwargs` | `unspecified` | `variadic` |

Returns `None`.

### ProceduralUniqueChannelConnectomeRouter.queue_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2756-L2757)

```python
ProceduralUniqueChannelConnectomeRouter.queue_bytes: int
```

Read-only property. Access as `instance.queue_bytes`; do not call it as a function.

Returns `int`.

### ProceduralUniqueChannelConnectomeRouter.recorded_offsets_per_source

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2760-L2779)

```python
ProceduralUniqueChannelConnectomeRouter.recorded_offsets_per_source: int
```

Read-only property. Access as `instance.recorded_offsets_per_source`; do not call it as a function.

Candidate offset slots needed to record one routed source.

Returns `int`.

### ProceduralUniqueChannelConnectomeRouter.clear_and_route

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/connectome.py#L2781-L3007)

```python
clear_and_route(self, active_sources: torch.Tensor, *, current_slot: int, current_step: int | None=None, clear_consumed: bool=True, touched_offsets: torch.Tensor | None=None, unique_rows: torch.Tensor | None=None, unique_row_flags: torch.Tensor | None=None, unique_row_count: torch.Tensor | None=None) -> torch.Tensor
```

Route the exact selected typed channel for each active source.

| Parameter | Type | Default |
| --- | --- | --- |
| `active_sources` | `torch.Tensor` | required |
| `current_slot` | `int` | required |
| `current_step` | `int \| None` | `None` |
| `clear_consumed` | `bool` | `True` |
| `touched_offsets` | `torch.Tensor \| None` | `None` |
| `unique_rows` | `torch.Tensor \| None` | `None` |
| `unique_row_flags` | `torch.Tensor \| None` | `None` |
| `unique_row_count` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.
