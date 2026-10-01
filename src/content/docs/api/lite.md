---
title: Lite neuron and configuration
description: Signatures, parameters, return contracts, and source for lite neuron and configuration.
section: API reference
order: 206
---

## Module contract

AxoSimLite aliases AdaptiveSupportP4Surrogate. Route features have shape (morphologies, input_dim, route_feature_dim). The Lite neuron forecasts four native outputs from preceding input blocks; sequence losses should mask the first four causal padding positions. SupportP4Config requires positive dimensions, patch_size=4, output_dim=2, and at least one morphology ID.

Source revision: `306a51ed950b`. [Public export index](/api/).

## SupportP4Config

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L13-L38)

Trainable low-order support recurrence at exact P4 cadence.

```python
SupportP4Config(input_dim: int = 1278, route_feature_dim: int = 118, token_dim: int = 58, state_dim: int = 16, patch_size: int = 4, output_dim: int = 2, morphology_ids: tuple[str, ...] = (), behavior_adaptation: bool = True) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `input_dim` | `int` | `1278` |
| `route_feature_dim` | `int` | `118` |
| `token_dim` | `int` | `58` |
| `state_dim` | `int` | `16` |
| `patch_size` | `int` | `4` |
| `output_dim` | `int` | `2` |
| `morphology_ids` | `tuple[str, ...]` | `()` |
| `behavior_adaptation` | `bool` | `True` |

`input_dim`: Native input-channel count. `route_feature_dim`: Width of aggregated route features. `token_dim`: Width of each encoded P4 token. `state_dim`: Temporal state width. `patch_size`: Native timesteps represented by one block. `output_dim`: Readout-channel count; Lite requires two. `morphology_ids`: Ordered morphology identity vocabulary. `behavior_adaptation`: Enable the learned behavior adaptation bank.

## AdaptiveSupportP4Surrogate

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L41-L535)

Learned support dynamics with compiled neuron adaptation.

Bases: `nn.Module`.

### AdaptiveSupportP4Surrogate.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L44-L115)

```python
__init__(self, config: SupportP4Config, route_features: torch.Tensor) -> None
```

route_features must match (len(config.morphology_ids),config.input_dim,config.route_feature_dim). They are cloned as a fixed floating-point buffer. Runtime cache width is 2*token_dim+3*state_dim+2*(patch_size*output_dim).

| Parameter | Type | Default |
| --- | --- | --- |
| `config` | `SupportP4Config` | required |
| `route_features` | `torch.Tensor` | required |

`route_features`: Fixed morphology-conditioned route-feature tensor.

Returns `None`.

### AdaptiveSupportP4Surrogate.patch_size

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L118-L119)

```python
AdaptiveSupportP4Surrogate.patch_size: int
```

Read-only property. Access as `instance.patch_size`; do not call it as a function.

Returns `int`.

### AdaptiveSupportP4Surrogate.gate_feature_dim

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L122-L123)

```python
AdaptiveSupportP4Surrogate.gate_feature_dim: int
```

Read-only property. Access as `instance.gate_feature_dim`; do not call it as a function.

Returns `int`.

### AdaptiveSupportP4Surrogate.reset_parameters

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L135-L149)

```python
reset_parameters(self) -> None
```

Returns `None`.

### AdaptiveSupportP4Surrogate.aggregate_inputs

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L151-L172)

```python
aggregate_inputs(self, inputs: torch.Tensor, *, morphology_indices: torch.Tensor) -> torch.Tensor
```

inputs is (B,T,input_dim), and morphology_indices is integer (B,). Selects each item's route feature bank and returns feature summaries (B,T,route_feature_dim).

| Parameter | Type | Default |
| --- | --- | --- |
| `inputs` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor` | required |

Returns `torch.Tensor`.

### AdaptiveSupportP4Surrogate.compile_adaptation

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L174-L186)

```python
compile_adaptation(self, behavior_parameters: torch.Tensor) -> torch.Tensor
```

behavior_parameters is (B,behavior_parameter_count). Returns compiled coefficients (B,cache_width). Raises ValueError if the configuration disables the adaptation compiler or the width is incompatible.

| Parameter | Type | Default |
| --- | --- | --- |
| `behavior_parameters` | `torch.Tensor` | required |

Returns `torch.Tensor`.

### AdaptiveSupportP4Surrogate.initial_state

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L188-L200)

```python
initial_state(self, batch_size: int, *, device: torch.device, dtype: torch.dtype) -> torch.Tensor
```

Allocates a zero state with shape (batch_size,state_dim) on the requested device/dtype.

| Parameter | Type | Default |
| --- | --- | --- |
| `batch_size` | `int` | required |
| `device` | `torch.device` | required |
| `dtype` | `torch.dtype` | required |

`batch_size`: Examples processed per batch. `device`: Execution or allocation device. `dtype`: Floating-point execution or allocation dtype.

Returns `torch.Tensor`.

### AdaptiveSupportP4Surrogate.runtime_coefficient_slices

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L212-L248)

```python
AdaptiveSupportP4Surrogate.runtime_coefficient_slices: dict[str, slice]
```

Read-only property. Access as `instance.runtime_coefficient_slices`; do not call it as a function.

Name the direct deployed coefficients in their packed order.

Returns named slices for the seven deployed coefficient groups: token offset/gain, decay delta, recurrent-state gain/offset, and native-output gain/offset. The slices partition cache_width.

Returns `dict[str, slice]`.

### AdaptiveSupportP4Surrogate.step_token

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L250-L312)

```python
step_token(self, token: torch.Tensor, state: torch.Tensor, *, adaptation_cache: torch.Tensor | None) -> tuple[torch.Tensor, torch.Tensor]
```

token is (B,token_dim), state is (B,state_dim), and optional adaptation_cache is (B,cache_width). Returns (forecast,next_state) with shapes (B,4,2) and (B,state_dim). This low-level step returns the decoded forecast directly.

| Parameter | Type | Default |
| --- | --- | --- |
| `token` | `torch.Tensor` | required |
| `state` | `torch.Tensor` | required |
| `adaptation_cache` | `torch.Tensor \| None` | required |

Returns `tuple[torch.Tensor, torch.Tensor]`.

### AdaptiveSupportP4Surrogate.step_p4

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L314-L342)

```python
step_p4(self, feature_patch: torch.Tensor, state: torch.Tensor, *, behavior_parameters: torch.Tensor | None=None, adaptation_cache: torch.Tensor | None=None) -> tuple[torch.Tensor, torch.Tensor]
```

feature_patch is (B,4,route_feature_dim) and state is (B,state_dim). Supply either logical behavior_parameters or compiled adaptation_cache. Returns (forecast,next_state) with shapes (B,4,2) and (B,state_dim).

| Parameter | Type | Default |
| --- | --- | --- |
| `feature_patch` | `torch.Tensor` | required |
| `state` | `torch.Tensor` | required |
| `behavior_parameters` | `torch.Tensor \| None` | `None` |
| `adaptation_cache` | `torch.Tensor \| None` | `None` |

Returns `tuple[torch.Tensor, torch.Tensor]`.

### AdaptiveSupportP4Surrogate.forward_feature_summaries

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L453-L469)

```python
forward_feature_summaries(self, summaries: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

summaries is (B,T,route_feature_dim), with T>0. Select logical adaptation by morphology_indices or supply behavior_parameters when configured. Returns (B,T,2) with four initial causal padding positions.

| Parameter | Type | Default |
| --- | --- | --- |
| `summaries` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |
| `behavior_parameters` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.

### AdaptiveSupportP4Surrogate.forward_runtime_coefficients

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L471-L489)

```python
forward_runtime_coefficients(self, summaries: torch.Tensor, *, runtime_coefficients: torch.Tensor) -> torch.Tensor
```

Run with direct deployed coefficients instead of a compiler.

summaries is (B,T,route_feature_dim), and runtime_coefficients must be (B,cache_width). Bypasses the logical adaptation compiler and returns (B,T,2) with the same causal padding as the summary sequence path.

| Parameter | Type | Default |
| --- | --- | --- |
| `summaries` | `torch.Tensor` | required |
| `runtime_coefficients` | `torch.Tensor` | required |

Returns `torch.Tensor`.

### AdaptiveSupportP4Surrogate.forward_with_gate_features

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L491-L516)

```python
forward_with_gate_features(self, inputs: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> tuple[torch.Tensor, torch.Tensor]
```

Return predictions and their existing causal token/state values.

inputs is (B,T,input_dim); morphology_indices is required. Returns (predictions,gate_features) with shapes (B,T,2) and (B,floor(T/4),token_dim+state_dim). Gate features are shifted causally by one block, and their first block is zero.

| Parameter | Type | Default |
| --- | --- | --- |
| `inputs` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |
| `behavior_parameters` | `torch.Tensor \| None` | `None` |

Returns `tuple[torch.Tensor, torch.Tensor]`.

### AdaptiveSupportP4Surrogate.forward

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/support_surrogate.py#L518-L535)

```python
forward(self, inputs: torch.Tensor, *, morphology_indices: torch.Tensor | None=None, behavior_parameters: torch.Tensor | None=None) -> torch.Tensor
```

inputs is (batch,native_steps,input_dim), with one morphology index per batch item where required. Return shape is (batch,native_steps,2). Mask the first four causal padding positions.

| Parameter | Type | Default |
| --- | --- | --- |
| `inputs` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor \| None` | `None` |
| `behavior_parameters` | `torch.Tensor \| None` | `None` |

Returns `torch.Tensor`.
