---
title: Activity and experimental control
description: Signatures, parameters, return contracts, and source for activity and experimental control.
section: API reference
order: 214
---

## Module contract

Threshold functions convert model-generated spike logits into events using fixed declared thresholds. Patch-phase layout helpers organize native cadence. HomeostaticThresholdController is an experimental optional code feature; it is not required by the lifecycle guides and is not a contribution presented in the technical report.

Source revision: `306a51ed950b`. [Public export index](/api/).

## StratifiedPatchPhaseLayout

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L12-L32)

Deterministic patch phases and a phase-major storage permutation.

```python
StratifiedPatchPhaseLayout(phase_ids: torch.Tensor, storage_permutation: torch.Tensor, inverse_permutation: torch.Tensor, phase_population_sizes: tuple[int, ...], storage_group_offsets: tuple[int, ...], storage_group_shape: tuple[int, int]) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `phase_ids` | `torch.Tensor` | required |
| `storage_permutation` | `torch.Tensor` | required |
| `inverse_permutation` | `torch.Tensor` | required |
| `phase_population_sizes` | `tuple[int, ...]` | required |
| `storage_group_offsets` | `tuple[int, ...]` | required |
| `storage_group_shape` | `tuple[int, int]` | required |

### StratifiedPatchPhaseLayout.patch_size

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L23-L24)

```python
StratifiedPatchPhaseLayout.patch_size: int
```

Read-only property. Access as `instance.patch_size`; do not call it as a function.

Returns `int`.

### StratifiedPatchPhaseLayout.population_size

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L27-L28)

```python
StratifiedPatchPhaseLayout.population_size: int
```

Read-only property. Access as `instance.population_size`; do not call it as a function.

Returns `int`.

### StratifiedPatchPhaseLayout.phase_sizes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L31-L32)

```python
StratifiedPatchPhaseLayout.phase_sizes: tuple[int, ...]
```

Read-only property. Access as `instance.phase_sizes`; do not call it as a function.

Returns `tuple[int, ...]`.

## FixedActivityThresholds

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L36-L67)

Fixed spike-score thresholds stratified by role and morphology.

```python
FixedActivityThresholds(excitatory: tuple[float, ...], inhibitory: tuple[float, ...]) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `excitatory` | `tuple[float, ...]` | required |
| `inhibitory` | `tuple[float, ...]` | required |

### FixedActivityThresholds.morphology_count

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L54-L55)

```python
FixedActivityThresholds.morphology_count: int
```

Read-only property. Access as `instance.morphology_count`; do not call it as a function.

Returns `int`.

### FixedActivityThresholds.as_tensor

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L57-L67)

```python
as_tensor(self, *, device: torch.device | str, dtype: torch.dtype) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `device` | `torch.device \| str` | required |
| `dtype` | `torch.dtype` | required |

`device`: Execution or allocation device. `dtype`: Floating-point execution or allocation dtype.

Returns `torch.Tensor`.

## FixedBlockActivityThresholds

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L71-L106)

Fixed role/morphology thresholds for each forecast position.

```python
FixedBlockActivityThresholds(forecast_steps: tuple[FixedActivityThresholds, ...]) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `forecast_steps` | `tuple[FixedActivityThresholds, ...]` | required |

### FixedBlockActivityThresholds.forecast_step_count

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L88-L89)

```python
FixedBlockActivityThresholds.forecast_step_count: int
```

Read-only property. Access as `instance.forecast_step_count`; do not call it as a function.

Returns `int`.

### FixedBlockActivityThresholds.morphology_count

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L92-L93)

```python
FixedBlockActivityThresholds.morphology_count: int
```

Read-only property. Access as `instance.morphology_count`; do not call it as a function.

Returns `int`.

### FixedBlockActivityThresholds.as_tensor

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L95-L106)

```python
as_tensor(self, *, device: torch.device | str, dtype: torch.dtype) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `device` | `torch.device \| str` | required |
| `dtype` | `torch.dtype` | required |

`device`: Execution or allocation device. `dtype`: Floating-point execution or allocation dtype.

Returns `torch.Tensor`.

## HomeostaticThresholdController

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L109-L253)

Adapt group thresholds to oppose sustained firing-rate errors.

### HomeostaticThresholdController.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L117-L204)

```python
__init__(self, *, group_ids: torch.Tensor, target_rates_hz: torch.Tensor, dt_ms: float, update_interval_ms: float, time_constant_ms: float, learning_rate: float, max_abs_offset: float) -> None
```

Experimental optional feature. group_ids assigns neurons to declared groups; target_rates_hz supplies each group's target. A causal group-rate estimate drives bounded threshold offsets. This interface does not establish biological timescales or biological realism.

| Parameter | Type | Default |
| --- | --- | --- |
| `group_ids` | `torch.Tensor` | required |
| `target_rates_hz` | `torch.Tensor` | required |
| `dt_ms` | `float` | required |
| `update_interval_ms` | `float` | required |
| `time_constant_ms` | `float` | required |
| `learning_rate` | `float` | required |
| `max_abs_offset` | `float` | required |

`learning_rate`: Optimizer step size.

Returns `None`.

### HomeostaticThresholdController.observe

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L207-L248)

```python
@torch.no_grad()
observe(self, activity: torch.Tensor) -> bool
```

Observe one simulation step and update at the window boundary.

Observes one neuron activity vector for a simulation step; returns whether the update interval triggered an offset update. No future activity is used.

| Parameter | Type | Default |
| --- | --- | --- |
| `activity` | `torch.Tensor` | required |

Returns `bool`.

### HomeostaticThresholdController.threshold_offsets_per_neuron

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L250-L253)

```python
threshold_offsets_per_neuron(self) -> torch.Tensor
```

Return the current group offset for every population member.

Returns one current group-derived threshold offset per neuron.

Returns `torch.Tensor`.

## build_stratified_patch_phase_layout

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L256-L376)

```python
build_stratified_patch_phase_layout(morphology_ids: torch.Tensor, inhibitory: torch.Tensor, *, patch_size: int, seed: int, tile_ids: torch.Tensor | None=None) -> StratifiedPatchPhaseLayout
```

Balance phases independently inside every morphology and E/I group.

| Parameter | Type | Default |
| --- | --- | --- |
| `morphology_ids` | `torch.Tensor` | required |
| `inhibitory` | `torch.Tensor` | required |
| `patch_size` | `int` | required |
| `seed` | `int` | required |
| `tile_ids` | `torch.Tensor \| None` | `None` |

`morphology_ids`: Ordered morphology identity vocabulary. `patch_size`: Native timesteps represented by one block. `seed`: Random seed for the declared operation.

Returns `StratifiedPatchPhaseLayout`.

## threshold_model_activity

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L379-L414)

```python
threshold_model_activity(spike_scores: torch.Tensor, morphology_ids: torch.Tensor, inhibitory: torch.Tensor, thresholds: FixedActivityThresholds) -> torch.Tensor
```

Return variable-cardinality events from fixed model-score crossings.

| Parameter | Type | Default |
| --- | --- | --- |
| `spike_scores` | `torch.Tensor` | required |
| `morphology_ids` | `torch.Tensor` | required |
| `inhibitory` | `torch.Tensor` | required |
| `thresholds` | `FixedActivityThresholds` | required |

`morphology_ids`: Ordered morphology identity vocabulary.

Returns `torch.Tensor`.

## threshold_block_model_activity

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/activity.py#L417-L451)

```python
threshold_block_model_activity(spike_scores: torch.Tensor, morphology_ids: torch.Tensor, inhibitory: torch.Tensor, thresholds: FixedBlockActivityThresholds) -> torch.Tensor
```

Threshold an ordered forecast block without fixing event counts.

| Parameter | Type | Default |
| --- | --- | --- |
| `spike_scores` | `torch.Tensor` | required |
| `morphology_ids` | `torch.Tensor` | required |
| `inhibitory` | `torch.Tensor` | required |
| `thresholds` | `FixedBlockActivityThresholds` | required |

`morphology_ids`: Ordered morphology identity vocabulary.

Returns `torch.Tensor`.
