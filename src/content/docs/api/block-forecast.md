---
title: Block-forecast models
description: Signatures, parameters, return contracts, and source for block-forecast models.
section: API reference
order: 205
---

## Module contract

CausalBlockForecastModel predicts native outputs through causal block forecasting. The top-level AxoSimGRU alias points to this implementation. Its backbone and BlockForecastConfig constructor contract differs from the named GRU-profile factory.

Source revision: `306a51ed950b`. [Public export index](/api/).

## BlockForecastConfig

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L22-L63)

Configuration for causal next-block trajectory prediction.

```python
BlockForecastConfig(core_kind: BlockForecastCore, patch_size: int, max_patch_rank: int = 8, max_trajectory_rank: int = 8, keep_local_tcn: bool = False, gru_hidden_units: int | None = None, residual_scale_init: float = 0.1, voltage_anchor_count: int | None = None, event_template: tuple[float, ...] | None = None, event_template_center_init: float = 0.9208316802978516, event_template_temperature: float = 0.25, event_template_hard: bool = False, behavior_adaptation: bool = False) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `core_kind` | `BlockForecastCore` | required |
| `patch_size` | `int` | required |
| `max_patch_rank` | `int` | `8` |
| `max_trajectory_rank` | `int` | `8` |
| `keep_local_tcn` | `bool` | `False` |
| `gru_hidden_units` | `int \| None` | `None` |
| `residual_scale_init` | `float` | `0.1` |
| `voltage_anchor_count` | `int \| None` | `None` |
| `event_template` | `tuple[float, ...] \| None` | `None` |
| `event_template_center_init` | `float` | `0.9208316802978516` |
| `event_template_temperature` | `float` | `0.25` |
| `event_template_hard` | `bool` | `False` |
| `behavior_adaptation` | `bool` | `False` |

`patch_size`: Native timesteps represented by one block. `behavior_adaptation`: Enable the learned behavior adaptation bank.

## CausalBlockForecastModel

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L66-L811)

Predict each native-resolution output block from prior input blocks.

Bases: `nn.Module`.

### CausalBlockForecastModel.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L69-L206)

```python
__init__(self, source: nn.Module, forecast_config: BlockForecastConfig) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `source` | `nn.Module` | required |
| `forecast_config` | `BlockForecastConfig` | required |

Returns `None`.

### CausalBlockForecastModel.config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L209-L210)

```python
CausalBlockForecastModel.config
```

Read-only property. Access as `instance.config`; do not call it as a function.

### CausalBlockForecastModel.num_input

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L213-L214)

```python
CausalBlockForecastModel.num_input: int
```

Read-only property. Access as `instance.num_input`; do not call it as a function.

Returns `int`.

### CausalBlockForecastModel.num_output

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L217-L218)

```python
CausalBlockForecastModel.num_output: int
```

Read-only property. Access as `instance.num_output`; do not call it as a function.

Returns `int`.

### CausalBlockForecastModel.num_branch

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L221-L222)

```python
CausalBlockForecastModel.num_branch: int
```

Read-only property. Access as `instance.num_branch`; do not call it as a function.

Returns `int`.

### CausalBlockForecastModel.patch_size

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L225-L226)

```python
CausalBlockForecastModel.patch_size: int
```

Read-only property. Access as `instance.patch_size`; do not call it as a function.

Returns `int`.

### CausalBlockForecastModel.sparse_voltage_output

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L229-L230)

```python
CausalBlockForecastModel.sparse_voltage_output: bool
```

Read-only property. Access as `instance.sparse_voltage_output`; do not call it as a function.

Returns `bool`.

### CausalBlockForecastModel.behavior_parameter_count

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L233-L238)

```python
CausalBlockForecastModel.behavior_parameter_count: int
```

Read-only property. Access as `instance.behavior_parameter_count`; do not call it as a function.

Returns `int`.

### CausalBlockForecastModel.block_state_sequence

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L447-L485)

```python
block_state_sequence(self, x: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

Encode a native sequence and return each causal macro state.

| Parameter | Type | Default |
| --- | --- | --- |
| `x` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |
| `behavior_parameters` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### CausalBlockForecastModel.decode_block_state_sequence

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L487-L509)

```python
decode_block_state_sequence(self, block_state: torch.Tensor, *, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

Decode dense native-rate trajectories from causal macro states.

| Parameter | Type | Default |
| --- | --- | --- |
| `block_state` | `torch.Tensor` | required |
| `behavior_parameters` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### CausalBlockForecastModel.forward

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L611-L716)

```python
forward(self, x: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `x` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |
| `behavior_parameters` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### CausalBlockForecastModel.component_manifest

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/block_forecast.py#L782-L811)

```python
component_manifest(self) -> dict[str, object]
```

Returns `dict[str, object]`.
