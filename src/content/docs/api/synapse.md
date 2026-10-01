---
title: Synaptic efficacy banks
description: Signatures, parameters, return contracts, and source for synaptic efficacy banks.
section: API reference
order: 212
---

## Module contract

An efficacy bank contains one positive multiplier for each retained incoming E/I contact slot. The retained width is 2*ceil(channels_per_role/recurrent_stride). W8 storage quantizes deviation around a positive baseline with one shared scale; dequantization reconstructs floating-point multipliers.

Source revision: `306a51ed950b`. [Public export index](/api/).

## QuantizedSynapticEfficacyBank

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/synapse.py#L11-L33)

One W8 multiplicative efficacy for every retained incoming contact.

```python
QuantizedSynapticEfficacyBank(values: torch.Tensor, scale: torch.Tensor, channels_per_role: int, recurrent_stride: int, baseline: float = 1.0) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `values` | `torch.Tensor` | required |
| `scale` | `torch.Tensor` | required |
| `channels_per_role` | `int` | required |
| `recurrent_stride` | `int` | required |
| `baseline` | `float` | `1.0` |

`channels_per_role`: Available contact-channel slots for each E/I role. `recurrent_stride`: Stride selecting retained contact slots. `baseline`: Positive shared reference efficacy for deviation quantization.

### QuantizedSynapticEfficacyBank.population_size

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/synapse.py#L21-L22)

```python
QuantizedSynapticEfficacyBank.population_size: int
```

Read-only property. Access as `instance.population_size`; do not call it as a function.

Returns `int`.

### QuantizedSynapticEfficacyBank.values_per_neuron

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/synapse.py#L25-L26)

```python
QuantizedSynapticEfficacyBank.values_per_neuron: int
```

Read-only property. Access as `instance.values_per_neuron`; do not call it as a function.

Returns `int`.

### QuantizedSynapticEfficacyBank.storage_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/synapse.py#L29-L33)

```python
QuantizedSynapticEfficacyBank.storage_bytes: int
```

Read-only property. Access as `instance.storage_bytes`; do not call it as a function.

Returns `int`.

## retained_synaptic_efficacies_per_neuron

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/synapse.py#L36-L50)

```python
retained_synaptic_efficacies_per_neuron(*, channels_per_role: int, recurrent_stride: int) -> int
```

Return compact E/I contact slots for the declared routed topology.

| Parameter | Type | Default |
| --- | --- | --- |
| `channels_per_role` | `int` | required |
| `recurrent_stride` | `int` | required |

`channels_per_role`: Available contact-channel slots for each E/I role. `recurrent_stride`: Stride selecting retained contact slots.

Returns `int`.

## quantize_synaptic_efficacies

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/synapse.py#L53-L97)

```python
quantize_synaptic_efficacies(efficacies: torch.Tensor, *, channels_per_role: int, recurrent_stride: int, baseline: float=1.0) -> QuantizedSynapticEfficacyBank
```

Quantize positive per-contact multipliers around a shared baseline.

efficacies is floating-point (N,2*ceil(channels_per_role/recurrent_stride)) with all values positive. Returns a W8 bank containing int8 values, one colocated floating scale, topology metadata, and positive baseline.

| Parameter | Type | Default |
| --- | --- | --- |
| `efficacies` | `torch.Tensor` | required |
| `channels_per_role` | `int` | required |
| `recurrent_stride` | `int` | required |
| `baseline` | `float` | `1.0` |

`channels_per_role`: Available contact-channel slots for each E/I role. `recurrent_stride`: Stride selecting retained contact slots. `baseline`: Positive shared reference efficacy for deviation quantization.

Returns `QuantizedSynapticEfficacyBank`.

## dequantize_synaptic_efficacies

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/synapse.py#L100-L109)

```python
dequantize_synaptic_efficacies(bank: QuantizedSynapticEfficacyBank) -> torch.Tensor
```

Materialize a W8 efficacy bank for training checks or export.

Returns floating-point (N,K) values reconstructed as bank.values*bank.scale+bank.baseline. Validates the bank's layout and scale device.

| Parameter | Type | Default |
| --- | --- | --- |
| `bank` | `QuantizedSynapticEfficacyBank` | required |

Returns `torch.Tensor`.
