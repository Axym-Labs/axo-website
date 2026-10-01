---
title: Model profiles
description: Signatures, parameters, return contracts, and source for model profiles.
section: API reference
order: 202
---

## Module contract

Named profiles provide fixed architecture recipes. Construction returns an untrained model. Mamba profiles use AxoMamba; GRU profiles use AxoTemporalModel with a GRU temporal core. Preserve the backend and saved model kind when loading weights.

Source revision: `306a51ed950b`. [Public export index](/api/).

## AxoSimModelProfile

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model_family.py#L25-L35)

Stable recipe for one trained-model capacity point.

```python
AxoSimModelProfile(profile_id: str, public_name: str, family: ModelFamily, model_dim: int, state_dim: int, num_layers: int, head_dim: int, mamba_update_normalization: Literal['none', 'fixed_rms'] = 'none') -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `profile_id` | `str` | required |
| `public_name` | `str` | required |
| `family` | `ModelFamily` | required |
| `model_dim` | `int` | required |
| `state_dim` | `int` | required |
| `num_layers` | `int` | required |
| `head_dim` | `int` | required |
| `mamba_update_normalization` | `Literal['none', 'fixed_rms']` | `'none'` |

`model_dim`: Temporal hidden-feature width. `state_dim`: Temporal state width. `num_layers`: Number of temporal layers.

## AXOSIM_MODEL_PROFILES

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model_family.py#L86-L88)

```python
AXOSIM_MODEL_PROFILES: Mapping[str, AxoSimModelProfile] = MappingProxyType({profile.profile_id: profile for profile in _PROFILES})
```

## create_axosim_profile

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/model_family.py#L91-L126)

```python
create_axosim_profile(profile_id: str, *, base_config: AxoMambaConfig | None=None, use_pytorch_fallback: bool=False) -> nn.Module
```

Build one named GRU or Mamba profile from the common AxoSim shell.

profile_id must exist in AXOSIM_MODEL_PROFILES. A Mamba profile returns an AxoMamba or fallback backbone; a GRU profile returns AxoTemporalModel with a GRU core. Weights are newly initialized, not downloaded.

| Parameter | Type | Default |
| --- | --- | --- |
| `profile_id` | `str` | required |
| `base_config` | `AxoMambaConfig \| None` | `None` |
| `use_pytorch_fallback` | `bool` | `False` |

Returns `nn.Module`.
