---
title: GRU temporal models
description: Signatures, parameters, return contracts, and source for gru temporal models.
section: API reference
order: 204
---

## Module contract

AxoTemporalModel wraps the common backbone with a selected temporal core. Named public GRU profiles use this class. Full-sequence forward calls reset temporal state; streaming calls use an explicitly allocated persistent state. Low-level temporal cores and behavior adapters are included below for direct construction.

Source revision: `306a51ed950b`. [Public export index](/api/).

## AxoTemporalStreamingState

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L16-L24)

Mutable online state for a replacement temporal core.

```python
AxoTemporalStreamingState(core_state: torch.Tensor | tuple[torch.Tensor, torch.Tensor], local_tcn_histories: list[torch.Tensor], morphology_feature_gains: torch.Tensor | None, patch_sum: torch.Tensor | None = None, patch_correction: torch.Tensor | None = None, patch_position: int = 0) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `core_state` | `torch.Tensor \| tuple[torch.Tensor, torch.Tensor]` | required |
| `local_tcn_histories` | `list[torch.Tensor]` | required |
| `morphology_feature_gains` | `torch.Tensor \| None` | required |
| `patch_sum` | `torch.Tensor \| None` | `None` |
| `patch_correction` | `torch.Tensor \| None` | `None` |
| `patch_position` | `int` | `0` |

## AxoTemporalCoreConfig

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L28-L85)

Configuration for a temporal core behind the shared AxoMamba encoder.

```python
AxoTemporalCoreConfig(kind: TemporalCoreKind, gru_hidden_units: int | None = None, branch_memory_units: int = 30, branch_hidden_units: int = 64, branch_synapse_decay: float = 0.85, branch_memory_decay: float = 0.9, residual_scale_init: float = 0.1, keep_local_tcn: bool = False, patch_size: int = 1, behavior_adapter_morphology_id: str | None = None, behavior_adapter_rank: int = 0, behavior_adapter_branch_token_offset: bool = False) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `kind` | `TemporalCoreKind` | required |
| `gru_hidden_units` | `int \| None` | `None` |
| `branch_memory_units` | `int` | `30` |
| `branch_hidden_units` | `int` | `64` |
| `branch_synapse_decay` | `float` | `0.85` |
| `branch_memory_decay` | `float` | `0.9` |
| `residual_scale_init` | `float` | `0.1` |
| `keep_local_tcn` | `bool` | `False` |
| `patch_size` | `int` | `1` |
| `behavior_adapter_morphology_id` | `str \| None` | `None` |
| `behavior_adapter_rank` | `int` | `0` |
| `behavior_adapter_branch_token_offset` | `bool` | `False` |

`patch_size`: Native timesteps represented by one block.

## NeuronBehaviorAdapter

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L88-L205)

Neuron-specific response parameters around shared GRU dynamics.

Bases: `nn.Module`.

### NeuronBehaviorAdapter.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L91-L159)

```python
__init__(self, *, branches: int, width: int, outputs: int, morphology_index: int, rank: int=0, branch_token_offset: bool=False) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `branches` | `int` | required |
| `width` | `int` | required |
| `outputs` | `int` | required |
| `morphology_index` | `int` | required |
| `rank` | `int` | `0` |
| `branch_token_offset` | `bool` | `False` |

Returns `None`.

### NeuronBehaviorAdapter.parameter_counts

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L162-L201)

```python
NeuronBehaviorAdapter.parameter_counts: dict[str, int]
```

Read-only property. Access as `instance.parameter_counts`; do not call it as a function.

Returns `dict[str, int]`.

### NeuronBehaviorAdapter.parameter_count

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L204-L205)

```python
NeuronBehaviorAdapter.parameter_count: int
```

Read-only property. Access as `instance.parameter_count`; do not call it as a function.

Returns `int`.

## ResidualGRUTemporalCore

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L208-L328)

Vendor-fused GRU with the same residual contract as AxoMamba blocks.

Bases: `nn.Module`.

### ResidualGRUTemporalCore.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L211-L238)

```python
__init__(self, width: int, *, hidden_units: int | None=None, residual_scale_init: float) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `width` | `int` | required |
| `hidden_units` | `int \| None` | `None` |
| `residual_scale_init` | `float` | required |

Returns `None`.

### ResidualGRUTemporalCore.forward

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L240-L253)

```python
forward(self, hidden: torch.Tensor, *, weight_ih_delta: torch.Tensor | None=None, weight_hh_delta: torch.Tensor | None=None, adapter_mask: torch.Tensor | None=None) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `hidden` | `torch.Tensor` | required |
| `weight_ih_delta` | `torch.Tensor \| None` | `None` |
| `weight_hh_delta` | `torch.Tensor \| None` | `None` |
| `adapter_mask` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### ResidualGRUTemporalCore.temporal_correction

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L255-L286)

```python
temporal_correction(self, hidden: torch.Tensor, *, weight_ih_delta: torch.Tensor | None=None, weight_hh_delta: torch.Tensor | None=None, adapter_mask: torch.Tensor | None=None) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `hidden` | `torch.Tensor` | required |
| `weight_ih_delta` | `torch.Tensor \| None` | `None` |
| `weight_hh_delta` | `torch.Tensor \| None` | `None` |
| `adapter_mask` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### ResidualGRUTemporalCore.recurrent_state_elements

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L327-L328)

```python
ResidualGRUTemporalCore.recurrent_state_elements: int
```

Read-only property. Access as `instance.recurrent_state_elements`; do not call it as a function.

Returns `int`.

## BranchELMTemporalCore

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L331-L393)

Leaky branch/memory recurrence behind the shared biological encoder.

Bases: `nn.Module`.

### BranchELMTemporalCore.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L334-L359)

```python
__init__(self, width: int, *, memory_units: int, hidden_units: int, synapse_decay: float, memory_decay: float, residual_scale_init: float) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `width` | `int` | required |
| `memory_units` | `int` | required |
| `hidden_units` | `int` | required |
| `synapse_decay` | `float` | required |
| `memory_decay` | `float` | required |
| `residual_scale_init` | `float` | required |

Returns `None`.

### BranchELMTemporalCore.forward

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L361-L362)

```python
forward(self, hidden: torch.Tensor) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `hidden` | `torch.Tensor` | required |

Returns `torch.Tensor`.

### BranchELMTemporalCore.temporal_correction

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L364-L389)

```python
temporal_correction(self, hidden: torch.Tensor) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `hidden` | `torch.Tensor` | required |

Returns `torch.Tensor`.

### BranchELMTemporalCore.recurrent_state_elements

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L392-L393)

```python
BranchELMTemporalCore.recurrent_state_elements: int
```

Read-only property. Access as `instance.recurrent_state_elements`; do not call it as a function.

Returns `int`.

## CausalPatchedTemporalCore

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L396-L455)

Run a temporal core on causal patch means and delay its correction.

Bases: `nn.Module`.

### CausalPatchedTemporalCore.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L399-L411)

```python
__init__(self, core: nn.Module, *, width: int, patch_size: int) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `core` | `nn.Module` | required |
| `width` | `int` | required |
| `patch_size` | `int` | required |

`patch_size`: Native timesteps represented by one block.

Returns `None`.

### CausalPatchedTemporalCore.forward

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L413-L448)

```python
forward(self, hidden: torch.Tensor, **temporal_kwargs) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `hidden` | `torch.Tensor` | required |
| `temporal_kwargs` | `unspecified` | `variadic` |

Returns `torch.Tensor`.

### CausalPatchedTemporalCore.recurrent_state_elements

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L451-L455)

```python
CausalPatchedTemporalCore.recurrent_state_elements: int
```

Read-only property. Access as `instance.recurrent_state_elements`; do not call it as a function.

Returns `int`.

## AxoTemporalModel

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L458-L1163)

Shared AxoMamba encoder/heads with an interchangeable temporal core.

Bases: `nn.Module`.

### AxoTemporalModel.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L461-L522)

```python
__init__(self, source: BranchOfficialMamba, temporal_config: AxoTemporalCoreConfig) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `source` | `BranchOfficialMamba` | required |
| `temporal_config` | `AxoTemporalCoreConfig` | required |

Returns `None`.

### AxoTemporalModel.config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L525-L526)

```python
AxoTemporalModel.config
```

Read-only property. Access as `instance.config`; do not call it as a function.

### AxoTemporalModel.num_input

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L529-L530)

```python
AxoTemporalModel.num_input: int
```

Read-only property. Access as `instance.num_input`; do not call it as a function.

Returns `int`.

### AxoTemporalModel.num_output

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L533-L534)

```python
AxoTemporalModel.num_output: int
```

Read-only property. Access as `instance.num_output`; do not call it as a function.

Returns `int`.

### AxoTemporalModel.num_branch

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L537-L538)

```python
AxoTemporalModel.num_branch: int
```

Read-only property. Access as `instance.num_branch`; do not call it as a function.

Returns `int`.

### AxoTemporalModel.base_soma_prediction

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L541-L542)

```python
AxoTemporalModel.base_soma_prediction: torch.Tensor | None
```

Read-only property. Access as `instance.base_soma_prediction`; do not call it as a function.

Returns `torch.Tensor \| None`.

### AxoTemporalModel.forward

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L544-L652)

```python
forward(self, x: torch.Tensor, *, morphology_indices: torch.Tensor | None=None) -> torch.Tensor
```

x is (B,T,num_input), with integer morphology_indices (B,) when morphology conditioning or behavior adaptation is configured. Returns (B,T,num_output). Each sequence forward initializes the core state.

| Parameter | Type | Default |
| --- | --- | --- |
| `x` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### AxoTemporalModel.allocate_streaming_state

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L654-L729)

```python
allocate_streaming_state(self, batch_size: int, *, device: torch.device | str | None=None, dtype: torch.dtype | None=None) -> AxoTemporalStreamingState
```

Allocate exact online state without retaining native-rate history.

Allocates an AxoTemporalStreamingState for batch_size on the requested device and dtype; the state contains temporal-core values and causal local-filter histories.

| Parameter | Type | Default |
| --- | --- | --- |
| `batch_size` | `int` | required |
| `device` | `torch.device \| str \| None` | `None` |
| `dtype` | `torch.dtype \| None` | `None` |

`batch_size`: Examples processed per batch. `device`: Execution or allocation device. `dtype`: Floating-point execution or allocation dtype.

Returns `AxoTemporalStreamingState`.

### AxoTemporalModel.streaming_step

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L731-L769)

```python
streaming_step(self, x: torch.Tensor, state: AxoTemporalStreamingState, *, morphology_indices: torch.Tensor | None=None) -> torch.Tensor
```

Advance one dense native-rate timestep.

Advances one native input step using persistent state. The guide supplies x as (B,num_input) and morphology_indices as (B,) when required. Returns (B,1,num_output).

| Parameter | Type | Default |
| --- | --- | --- |
| `x` | `torch.Tensor` | required |
| `state` | `AxoTemporalStreamingState` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### AxoTemporalModel.streaming_step_events

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L771-L921)

```python
streaming_step_events(self, event_indices: torch.Tensor, event_values: torch.Tensor, state: AxoTemporalStreamingState, *, morphology_indices: torch.Tensor | None=None, chunk_size: int | None=None, output_buffer: torch.Tensor | None=None, retain_base_soma_prediction: bool=True) -> torch.Tensor
```

Advance one timestep from padded sparse channel/value rows.

| Parameter | Type | Default |
| --- | --- | --- |
| `event_indices` | `torch.Tensor` | required |
| `event_values` | `torch.Tensor` | required |
| `state` | `AxoTemporalStreamingState` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |
| `chunk_size` | `int \| None` | `None` |
| `output_buffer` | `torch.Tensor \| None` | `None` |
| `retain_base_soma_prediction` | `bool` | `True` |

Returns `torch.Tensor`.

### AxoTemporalModel.recurrent_state_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L1127-L1135)

```python
recurrent_state_bytes(self, *, dtype: torch.dtype) -> int
```

| Parameter | Type | Default |
| --- | --- | --- |
| `dtype` | `torch.dtype` | required |

`dtype`: Floating-point execution or allocation dtype.

Returns `int`.

### AxoTemporalModel.component_manifest

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L1137-L1163)

```python
component_manifest(self) -> dict[str, object]
```

Returns `dict[str, object]`.

## create_temporal_model

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L1166-L1174)

```python
create_temporal_model(source: BranchOfficialMamba, temporal_config: AxoTemporalCoreConfig) -> BranchOfficialMamba | AxoTemporalModel
```

Compose a selected AxoMamba front end with one temporal core.

| Parameter | Type | Default |
| --- | --- | --- |
| `source` | `BranchOfficialMamba` | required |
| `temporal_config` | `AxoTemporalCoreConfig` | required |

Returns `BranchOfficialMamba \| AxoTemporalModel`.

## migrate_legacy_gru_state_dict

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/temporal_core.py#L1177-L1195)

```python
migrate_legacy_gru_state_dict(state_dict: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]
```

Map the internal I108 GRU wrapper into the unified checkpoint schema.

| Parameter | Type | Default |
| --- | --- | --- |
| `state_dict` | `dict[str, torch.Tensor]` | required |

Returns `dict[str, torch.Tensor]`.
