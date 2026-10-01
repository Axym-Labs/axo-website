---
title: Population interfaces
description: Signatures, parameters, return contracts, and source for population interfaces.
section: API reference
order: 201
---

## Module contract

The public differentiable population combines one Lite model with persistent neuron identities, morphology assignments, contact routes, and adaptation banks. AxoSimMamba aliases AxoMamba; AxoSimLite aliases AdaptiveSupportP4Surrogate; AxoSimGRU currently aliases CausalBlockForecastModel. Named GRU profiles are built by create_axosim_profile and return AxoTemporalModel.

Source revision: `306a51ed950b`. [Public export index](/api/).

## AxoSimPopulation

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L24-L470)

Differentiable AxoSim-Lite population with distinct adaptation banks.

Bases: `nn.Module`.

### AxoSimPopulation.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L27-L76)

```python
__init__(self, neuron: AxoSimLite, *, morphology_indices: torch.Tensor, contact_branch_indices: torch.Tensor) -> None
```

neuron is a Lite model. morphology_indices is integer (N,); contact_branch_indices is integer (N,K), with values in [0, neuron.config.input_dim). The morphology indices must refer to declared morphology classes. Buffers are cloned and converted to long.

| Parameter | Type | Default |
| --- | --- | --- |
| `neuron` | `AxoSimLite` | required |
| `morphology_indices` | `torch.Tensor` | required |
| `contact_branch_indices` | `torch.Tensor` | required |

Returns `None`.

### AxoSimPopulation.population_size

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L79-L80)

```python
AxoSimPopulation.population_size: int
```

Read-only property. Access as `instance.population_size`; do not call it as a function.

Returns `int`.

### AxoSimPopulation.runtime_coefficients_per_neuron

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L83-L84)

```python
AxoSimPopulation.runtime_coefficients_per_neuron: int
```

Read-only property. Access as `instance.runtime_coefficients_per_neuron`; do not call it as a function.

Returns `int`.

### AxoSimPopulation.synaptic_efficacies_per_neuron

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L87-L88)

```python
AxoSimPopulation.synaptic_efficacies_per_neuron: int
```

Read-only property. Access as `instance.synaptic_efficacies_per_neuron`; do not call it as a function.

Returns `int`.

### AxoSimPopulation.adaptation_parameters

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L90-L93)

```python
adaptation_parameters(self) -> Iterator[nn.Parameter]
```

Yields behavior_adapter, morphology_adapter, and synaptic_log_efficacy in that order.

Returns `Iterator[nn.Parameter]`.

### AxoSimPopulation.trainable_adaptation_parameters

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L95-L100)

```python
trainable_adaptation_parameters(self) -> Iterator[nn.Parameter]
```

Yields only adaptation parameters whose requires_grad flag is true.

Returns `Iterator[nn.Parameter]`.

### AxoSimPopulation.enable_adaptation_training

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L102-L113)

```python
enable_adaptation_training(self, *, behavior: bool=True, morphology: bool=True, synaptic: bool=True) -> None
```

Freezes shared Lite parameters, then independently enables or freezes behavior_adapter, morphology_adapter, and synaptic_log_efficacy. The defaults enable all three groups.

| Parameter | Type | Default |
| --- | --- | --- |
| `behavior` | `bool` | `True` |
| `morphology` | `bool` | `True` |
| `synaptic` | `bool` | `True` |

Returns `None`.

### AxoSimPopulation.enable_full_training

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L115-L117)

```python
enable_full_training(self) -> None
```

Enables requires_grad on every module parameter, including shared neuron weights.

Returns `None`.

### AxoSimPopulation.synaptic_efficacies

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L119-L134)

```python
synaptic_efficacies(self, synaptic_log_efficacy: torch.Tensor | None=None) -> torch.Tensor
```

Returns exp(log_efficacy) with shape (N,K). Signed contact event amplitudes carry excitation/inhibition; efficacy remains positive.

| Parameter | Type | Default |
| --- | --- | --- |
| `synaptic_log_efficacy` | `torch.Tensor \| None` | `None` |

`synaptic_log_efficacy`: Optional (N,K) log-efficacy override.

Returns `torch.Tensor`.

### AxoSimPopulation.forward

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L198-L211)

```python
forward(self, contact_inputs: torch.Tensor, *, synaptic_log_efficacy: torch.Tensor | None=None) -> torch.Tensor
```

contact_inputs is (N,T,K). Optional synaptic_log_efficacy is (N,K) and replaces the stored efficacy values for this call. Return shape is (N,T,2); hidden state starts fresh for the sequence.

| Parameter | Type | Default |
| --- | --- | --- |
| `contact_inputs` | `torch.Tensor` | required |
| `synaptic_log_efficacy` | `torch.Tensor \| None` | `None` |

`contact_inputs`: Dense signed contact histories; shape defined above. `synaptic_log_efficacy`: Optional (N,K) log-efficacy override.

Returns `torch.Tensor`.

### AxoSimPopulation.forward_sparse_contacts

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L213-L327)

```python
forward_sparse_contacts(self, event_summary_indices: torch.Tensor, event_contact_indices: torch.Tensor, event_values: torch.Tensor, *, time_steps: int, synaptic_log_efficacy: torch.Tensor | None=None) -> torch.Tensor
```

Run exact sparse contact events with full temporal gradients.

The three event tensors are equal-length one-dimensional arrays. Summary indices address n*T+t; contact indices address n*K+k, and both must identify the same neuron. Integer indices and floating event values must share the module device. Return shape is (N,time_steps,2). Gradients propagate through amplitudes and selected efficacies.

| Parameter | Type | Default |
| --- | --- | --- |
| `event_summary_indices` | `torch.Tensor` | required |
| `event_contact_indices` | `torch.Tensor` | required |
| `event_values` | `torch.Tensor` | required |
| `time_steps` | `int` | required |
| `synaptic_log_efficacy` | `torch.Tensor \| None` | `None` |

`time_steps`: Native sequence horizon. `synaptic_log_efficacy`: Optional (N,K) log-efficacy override.

Returns `torch.Tensor`.

### AxoSimPopulation.forward_batch

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L329-L392)

```python
forward_batch(self, contact_inputs: torch.Tensor, *, synaptic_log_efficacy: torch.Tensor | None=None) -> torch.Tensor
```

Run independent examples through one persistent population.

contact_inputs is (B,N,T,K). Independent examples share population identities and adaptation banks. Return shape is (B,N,T,2).

| Parameter | Type | Default |
| --- | --- | --- |
| `contact_inputs` | `torch.Tensor` | required |
| `synaptic_log_efficacy` | `torch.Tensor \| None` | `None` |

`contact_inputs`: Dense signed contact histories; shape defined above. `synaptic_log_efficacy`: Optional (N,K) log-efficacy override.

Returns `torch.Tensor`.

### AxoSimPopulation.forward_tokens

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L394-L418)

```python
forward_tokens(self, tokens: torch.Tensor) -> torch.Tensor
```

Run pre-encoded P4 tokens with full temporal gradients.

tokens is (N,blocks,token_dim), already encoded at P4 cadence. Return shape is (N,blocks*4,2). This path decodes supplied tokens directly rather than adding the dense-input path's initial padding.

| Parameter | Type | Default |
| --- | --- | --- |
| `tokens` | `torch.Tensor` | required |

Returns `torch.Tensor`.

### AxoSimPopulation.forward_token_batch

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L420-L470)

```python
forward_token_batch(self, tokens: torch.Tensor) -> torch.Tensor
```

Run batched pre-encoded P4 tokens with full temporal gradients.

tokens is (B,N,blocks,token_dim). Return shape is (B,N,blocks*4,2).

| Parameter | Type | Default |
| --- | --- | --- |
| `tokens` | `torch.Tensor` | required |

Returns `torch.Tensor`.
