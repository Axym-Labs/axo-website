---
title: Mamba models and configuration
description: Signatures, parameters, return contracts, and source for mamba models and configuration.
section: API reference
order: 203
---

## Module contract

AxoMamba is the public Mamba implementation and inherits BranchOfficialMamba. AxoMambaConfig inherits all BranchOfficialMambaConfig fields. The default_axomamba_config factory supplies the promoted recipe, which differs from the dataclass's raw field defaults. AxoPyTorchMamba is a test-oriented fallback with a different checkpoint format.

Source revision: `306a51ed950b`. [Public export index](/api/).

## AxoMambaConfig

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L20-L21)

Bases: `BranchOfficialMambaConfig`.

Inherits every configuration field and default in `BranchOfficialMambaConfig` below. `default_axomamba_config` applies the selected AxoSim recipe over those raw defaults.

## default_axomamba_config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L24-L83)

```python
default_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

Build the default AxoSim Mamba recipe and apply keyword overrides.

| Parameter | Type | Default |
| --- | --- | --- |
| `overrides` | `Any` | `variadic` |

Returns `AxoMambaConfig`.

## structured_compact_axomamba_config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L86-L96)

```python
structured_compact_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

Build the structured compact recipe and apply keyword overrides.

| Parameter | Type | Default |
| --- | --- | --- |
| `overrides` | `Any` | `variadic` |

Returns `AxoMambaConfig`.

## regression_axomamba_config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L99-L108)

```python
regression_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

Build the voltage-focused recipe and apply keyword overrides.

| Parameter | Type | Default |
| --- | --- | --- |
| `overrides` | `Any` | `variadic` |

Returns `AxoMambaConfig`.

## population_axomamba_config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L111-L125)

```python
population_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

Build the population-domain recipe and apply keyword overrides.

| Parameter | Type | Default |
| --- | --- | --- |
| `overrides` | `Any` | `variadic` |

Returns `AxoMambaConfig`.

## spike_axomamba_config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L128-L139)

```python
spike_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

Build the spike-focused recipe and apply keyword overrides.

| Parameter | Type | Default |
| --- | --- | --- |
| `overrides` | `Any` | `variadic` |

Returns `AxoMambaConfig`.

## load_axomamba_config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L142-L148)

```python
load_axomamba_config(path: str | Path | None=None, **overrides: Any) -> AxoMambaConfig
```

| Parameter | Type | Default |
| --- | --- | --- |
| `path` | `str \| Path \| None` | `None` |
| `overrides` | `Any` | `variadic` |

Returns `AxoMambaConfig`.

## coerce_axomamba_config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L151-L158)

```python
coerce_axomamba_config(config: AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None) -> AxoMambaConfig
```

| Parameter | Type | Default |
| --- | --- | --- |
| `config` | `AxoMambaConfig \| BranchOfficialMambaConfig \| Mapping[str, Any] \| None` | required |

Returns `AxoMambaConfig`.

## AxoMamba

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L161-L170)

Bases: `BranchOfficialMamba`.

Inherits full-sequence and streaming methods from `BranchOfficialMamba` below. The fallback uses a distinct checkpoint backend.

### AxoMamba.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L164-L170)

```python
__init__(self, config: AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None=None, *, mamba_classes: tuple[type, type | None] | None=None) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `config` | `AxoMambaConfig \| BranchOfficialMambaConfig \| Mapping[str, Any] \| None` | `None` |
| `mamba_classes` | `tuple[type, type \| None] \| None` | `None` |

Returns `None`.

## AxoPyTorchMamba

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L173-L182)

Bases: `AxoMamba`.

Inherits full-sequence and streaming methods from `BranchOfficialMamba` below. The fallback uses a distinct checkpoint backend.

### AxoPyTorchMamba.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L176-L182)

```python
__init__(self, config: AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None=None) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `config` | `AxoMambaConfig \| BranchOfficialMambaConfig \| Mapping[str, Any] \| None` | `None` |

Returns `None`.

## create_axomamba

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axomamba.py#L185-L192)

```python
create_axomamba(config: AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None=None, *, use_pytorch_fallback: bool=False) -> AxoMamba
```

| Parameter | Type | Default |
| --- | --- | --- |
| `config` | `AxoMambaConfig \| BranchOfficialMambaConfig \| Mapping[str, Any] \| None` | `None` |
| `use_pytorch_fallback` | `bool` | `False` |

Returns `AxoMamba`.

## BranchOfficialMambaConfig

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L29-L98)

```python
BranchOfficialMambaConfig(num_input: int = 1278, num_output: int = 2, num_branch: int = 45, num_synapse_per_branch: int = 100, input_to_synapse_routing: str | None = 'neuronio_routing', model_dim: int = 64, num_layers: int = 2, block_repeats: int = 1, state_dim: int = 16, conv_kernel: int = 4, expansion: int = 2, block_type: str = 'mamba1', head_dim: int = 64, num_groups: int = 1, chunk_size: int = 256, block_norm: bool = True, final_norm: bool = True, dropout: float = 0.0, residual_scale_init: float = 0.1, mamba_update_normalization: str = 'none', separate_heads: bool = False, soma_filter: bool = False, soma_filter_tau: float = 25.0, soma_filter_kernel: int = 129, learn_soma_filter_decay: bool = True, soma_multiplicative_gate: bool = False, soma_multiplicative_scale_init: float = 0.1, soma_peak_correction: bool = False, soma_peak_correction_scale_init: float = 0.1, soma_highpass_correction: bool = False, soma_highpass_correction_scale_init: float = 0.1, spike_voltage_coupling_scale: float = 0.0, morphology_ids: list[str] | None = None, morphology_embedding_scale: float | None = None, population_adapter_morphology_id: str | None = None, synapse_gain_scale: float | None = None, morphology_synapse_gain_scale: float | None = None, share_morphology_synapse_gain: bool = False, morphology_synapse_gain_rank: int = 0, morphology_synapse_feature_dim: int = 0, morphology_synapse_feature_hidden: int = 0, morphology_synapse_feature_scale: float | None = None, morphology_synapse_feature_storage_dtype: str = 'float32', local_tcn_scale: float | None = None, local_tcn_mode: str = 'dilated', local_tcn_position: str = 'parallel', share_local_tcn_pointwise: bool = False, local_tcn_pointwise_adapter_rank: int = 0, local_tcn_pointwise_rank: int = 0, local_tcn_output_rank: int = 0, mamba_projection_rank: int = 0, branch_gain: bool = False, branch_nonlinearity: str = 'none', branch_nonlinearity_scale_init: float = 0.1, branch_subunits: int = 0, branch_subunit_routing: str = 'contiguous', branch_subunit_scale: float = 1.0, branch_bilinear_rank: int = 0, branch_bilinear_scale: float | None = None, branch_trace_taus: list[float] | None = None, branch_trace_kernel: int = 65, hidden_trace_taus: list[float] | None = None, hidden_trace_kernel: int = 129, temporal_refine_kernel: int = 0, integrative_mixer: bool = False, integrative_mixer_short_kernel: int = 9, integrative_mixer_long_kernel: int = 65, integrative_mixer_position: str = 'pre', integrative_mixer_long_path_bias: float = 0.5) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `num_input` | `int` | `1278` |
| `num_output` | `int` | `2` |
| `num_branch` | `int` | `45` |
| `num_synapse_per_branch` | `int` | `100` |
| `input_to_synapse_routing` | `str \| None` | `'neuronio_routing'` |
| `model_dim` | `int` | `64` |
| `num_layers` | `int` | `2` |
| `block_repeats` | `int` | `1` |
| `state_dim` | `int` | `16` |
| `conv_kernel` | `int` | `4` |
| `expansion` | `int` | `2` |
| `block_type` | `str` | `'mamba1'` |
| `head_dim` | `int` | `64` |
| `num_groups` | `int` | `1` |
| `chunk_size` | `int` | `256` |
| `block_norm` | `bool` | `True` |
| `final_norm` | `bool` | `True` |
| `dropout` | `float` | `0.0` |
| `residual_scale_init` | `float` | `0.1` |
| `mamba_update_normalization` | `str` | `'none'` |
| `separate_heads` | `bool` | `False` |
| `soma_filter` | `bool` | `False` |
| `soma_filter_tau` | `float` | `25.0` |
| `soma_filter_kernel` | `int` | `129` |
| `learn_soma_filter_decay` | `bool` | `True` |
| `soma_multiplicative_gate` | `bool` | `False` |
| `soma_multiplicative_scale_init` | `float` | `0.1` |
| `soma_peak_correction` | `bool` | `False` |
| `soma_peak_correction_scale_init` | `float` | `0.1` |
| `soma_highpass_correction` | `bool` | `False` |
| `soma_highpass_correction_scale_init` | `float` | `0.1` |
| `spike_voltage_coupling_scale` | `float` | `0.0` |
| `morphology_ids` | `list[str] \| None` | `None` |
| `morphology_embedding_scale` | `float \| None` | `None` |
| `population_adapter_morphology_id` | `str \| None` | `None` |
| `synapse_gain_scale` | `float \| None` | `None` |
| `morphology_synapse_gain_scale` | `float \| None` | `None` |
| `share_morphology_synapse_gain` | `bool` | `False` |
| `morphology_synapse_gain_rank` | `int` | `0` |
| `morphology_synapse_feature_dim` | `int` | `0` |
| `morphology_synapse_feature_hidden` | `int` | `0` |
| `morphology_synapse_feature_scale` | `float \| None` | `None` |
| `morphology_synapse_feature_storage_dtype` | `str` | `'float32'` |
| `local_tcn_scale` | `float \| None` | `None` |
| `local_tcn_mode` | `str` | `'dilated'` |
| `local_tcn_position` | `str` | `'parallel'` |
| `share_local_tcn_pointwise` | `bool` | `False` |
| `local_tcn_pointwise_adapter_rank` | `int` | `0` |
| `local_tcn_pointwise_rank` | `int` | `0` |
| `local_tcn_output_rank` | `int` | `0` |
| `mamba_projection_rank` | `int` | `0` |
| `branch_gain` | `bool` | `False` |
| `branch_nonlinearity` | `str` | `'none'` |
| `branch_nonlinearity_scale_init` | `float` | `0.1` |
| `branch_subunits` | `int` | `0` |
| `branch_subunit_routing` | `str` | `'contiguous'` |
| `branch_subunit_scale` | `float` | `1.0` |
| `branch_bilinear_rank` | `int` | `0` |
| `branch_bilinear_scale` | `float \| None` | `None` |
| `branch_trace_taus` | `list[float] \| None` | `None` |
| `branch_trace_kernel` | `int` | `65` |
| `hidden_trace_taus` | `list[float] \| None` | `None` |
| `hidden_trace_kernel` | `int` | `129` |
| `temporal_refine_kernel` | `int` | `0` |
| `integrative_mixer` | `bool` | `False` |
| `integrative_mixer_short_kernel` | `int` | `9` |
| `integrative_mixer_long_kernel` | `int` | `65` |
| `integrative_mixer_position` | `str` | `'pre'` |
| `integrative_mixer_long_path_bias` | `float` | `0.5` |

`num_input`: Input-channel count. `num_output`: Output-channel count. `num_branch`: Branched input-feature count. `num_synapse_per_branch`: Contact slots per branch. `model_dim`: Temporal hidden-feature width. `num_layers`: Number of temporal layers. `state_dim`: Temporal state width. `morphology_ids`: Ordered morphology identity vocabulary.

## BranchMambaStreamingState

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L102-L107)

Mutable recurrent state for exact one-timestep AxoMamba inference.

```python
BranchMambaStreamingState(mamba_states: list[tuple[torch.Tensor, torch.Tensor]], local_tcn_histories: list[torch.Tensor], morphology_feature_gains: torch.Tensor | None = None) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `mamba_states` | `list[tuple[torch.Tensor, torch.Tensor]]` | required |
| `local_tcn_histories` | `list[torch.Tensor]` | required |
| `morphology_feature_gains` | `torch.Tensor \| None` | `None` |

## BranchOfficialMamba

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L110-L1808)

Branch-routed wrapper around the official mamba-ssm Mamba module.

Bases: `nn.Module`.

### BranchOfficialMamba.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L113-L588)

```python
__init__(self, config: BranchOfficialMambaConfig, *, mamba_classes: tuple[type[nn.Module], type[nn.Module] | None] | None=None) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `config` | `BranchOfficialMambaConfig` | required |
| `mamba_classes` | `tuple[type[nn.Module], type[nn.Module] \| None] \| None` | `None` |

Returns `None`.

### BranchOfficialMamba.forward

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L678-L689)

```python
forward(self, x: torch.Tensor, *, morphology_indices: torch.Tensor | None=None) -> torch.Tensor
```

x is (B,T,num_input), and optional morphology_indices is integer (B,). Morphology-conditioned synaptic gains require valid morphology indices. Returns (B,T,num_output) in the checkpoint's spike-logit and soma-target coordinates.

| Parameter | Type | Default |
| --- | --- | --- |
| `x` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### BranchOfficialMamba.allocate_streaming_state

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L954-L994)

```python
allocate_streaming_state(self, batch_size: int, *, device: torch.device | str | None=None, dtype: torch.dtype | None=None) -> BranchMambaStreamingState
```

Allocate state that advances a population without replaying history.

Allocates a persistent streaming-state record for the requested batch_size, device, and dtype. Allocate a fresh state for independent traces or changed batch membership.

| Parameter | Type | Default |
| --- | --- | --- |
| `batch_size` | `int` | required |
| `device` | `torch.device \| str \| None` | `None` |
| `dtype` | `torch.dtype \| None` | `None` |

`batch_size`: Examples processed per batch. `device`: Execution or allocation device. `dtype`: Floating-point execution or allocation dtype.

Returns `BranchMambaStreamingState`.

### BranchOfficialMamba.streaming_step

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L996-L1087)

```python
streaming_step(self, x: torch.Tensor, state: BranchMambaStreamingState, *, morphology_indices: torch.Tensor | None=None, chunk_size: int | None=None) -> torch.Tensor
```

Advance one timestep and return `(batch, 1, output)` predictions.

Advances the supplied mutable streaming state by one native input step. The guide supplies x as (B,num_input), with one morphology index per item when configured. Returns (B,1,num_output).

| Parameter | Type | Default |
| --- | --- | --- |
| `x` | `torch.Tensor` | required |
| `state` | `BranchMambaStreamingState` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |
| `chunk_size` | `int \| None` | `None` |

Returns `torch.Tensor`.

### BranchOfficialMamba.streaming_step_events

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L1310-L1451)

```python
streaming_step_events(self, event_indices: torch.Tensor, event_values: torch.Tensor, state: BranchMambaStreamingState, *, morphology_indices: torch.Tensor | None=None, chunk_size: int | None=None, output_buffer: torch.Tensor | None=None, retain_base_soma_prediction: bool=True) -> torch.Tensor
```

Advance one timestep from padded sparse channel/value event rows.

| Parameter | Type | Default |
| --- | --- | --- |
| `event_indices` | `torch.Tensor` | required |
| `event_values` | `torch.Tensor` | required |
| `state` | `BranchMambaStreamingState` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |
| `chunk_size` | `int \| None` | `None` |
| `output_buffer` | `torch.Tensor \| None` | `None` |
| `retain_base_soma_prediction` | `bool` | `True` |

Returns `torch.Tensor`.

## BranchPyTorchMamba

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L1810-L1818)

Branch-routed Mamba wrapper using the differentiable PyTorch fallback block.

Bases: `BranchOfficialMamba`.

### BranchPyTorchMamba.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/mamba_official.py#L1813-L1818)

```python
__init__(self, config: BranchOfficialMambaConfig) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `config` | `BranchOfficialMambaConfig` | required |

Returns `None`.
