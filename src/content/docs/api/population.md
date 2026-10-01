---
title: Behavior banks and population runners
description: Signatures, parameters, return contracts, and source for behavior banks and population runners.
section: API reference
order: 211
---

## Module contract

Behavior-bank quantization stores component scales and W4/W8 values separately from the shared model. Quantization is a deployment transformation, while training uses floating-point parameters. The low-level GRU population runners and deployment records expose the contracts used for direct runtime construction.

Source revision: `306a51ed950b`. [Public export index](/api/).

## QuantizedNeuronBehaviorBank

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L20-L33)

Physical low-bit storage for a logical behavior-adaptation bank.

```python
QuantizedNeuronBehaviorBank(values: torch.Tensor, scales: torch.Tensor, bits: int, logical_parameters_per_neuron: int) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `values` | `torch.Tensor` | required |
| `scales` | `torch.Tensor` | required |
| `bits` | `int` | required |
| `logical_parameters_per_neuron` | `int` | required |

`bits`: Quantization precision, restricted to the supported bit widths.

### QuantizedNeuronBehaviorBank.storage_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L29-L33)

```python
QuantizedNeuronBehaviorBank.storage_bytes: int
```

Read-only property. Access as `instance.storage_bytes`; do not call it as a function.

Returns `int`.

## MixedQuantizedNeuronBehaviorBank

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L37-L51)

Component-wise W4/W8 storage for a logical adaptation bank.

```python
MixedQuantizedNeuronBehaviorBank(values: torch.Tensor, scales: torch.Tensor, byte_slices: dict[str, slice], component_bits: dict[str, int], logical_parameters_per_neuron: int) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `values` | `torch.Tensor` | required |
| `scales` | `torch.Tensor` | required |
| `byte_slices` | `dict[str, slice]` | required |
| `component_bits` | `dict[str, int]` | required |
| `logical_parameters_per_neuron` | `int` | required |

### MixedQuantizedNeuronBehaviorBank.storage_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L47-L51)

```python
MixedQuantizedNeuronBehaviorBank.storage_bytes: int
```

Read-only property. Access as `instance.storage_bytes`; do not call it as a function.

Returns `int`.

## quantize_neuron_behavior_parameters

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L54-L108)

```python
quantize_neuron_behavior_parameters(parameters: torch.Tensor, *, adaptation: NeuronBehaviorAdaptation, bits: int) -> QuantizedNeuronBehaviorBank
```

Quantize each adaptation component with one symmetric scale.

parameters is floating-point (N,adaptation.parameter_count). bits is 4 or 8. W4 requires even logical width and packs two values per byte. Returns physical values and one scale per adaptation component.

| Parameter | Type | Default |
| --- | --- | --- |
| `parameters` | `torch.Tensor` | required |
| `adaptation` | `NeuronBehaviorAdaptation` | required |
| `bits` | `int` | required |

`bits`: Quantization precision, restricted to the supported bit widths.

Returns `QuantizedNeuronBehaviorBank`.

## quantize_mixed_neuron_behavior_parameters

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L111-L183)

```python
quantize_mixed_neuron_behavior_parameters(parameters: torch.Tensor, *, adaptation: NeuronBehaviorAdaptation, component_bits: dict[str, int]) -> MixedQuantizedNeuronBehaviorBank
```

Quantize each adaptation component to its declared W4/W8 tier.

parameters is floating-point (N,adaptation.parameter_count). component_bits declares W4/W8 for each named adaptation component. Returns packed byte slices and scale metadata needed for reconstruction.

| Parameter | Type | Default |
| --- | --- | --- |
| `parameters` | `torch.Tensor` | required |
| `adaptation` | `NeuronBehaviorAdaptation` | required |
| `component_bits` | `dict[str, int]` | required |

Returns `MixedQuantizedNeuronBehaviorBank`.

## dequantize_neuron_behavior_parameters

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L186-L215)

```python
dequantize_neuron_behavior_parameters(bank: QuantizedNeuronBehaviorBank, *, adaptation: NeuronBehaviorAdaptation) -> torch.Tensor
```

Materialize a low-bit behavior bank for validation or export.

| Parameter | Type | Default |
| --- | --- | --- |
| `bank` | `QuantizedNeuronBehaviorBank` | required |
| `adaptation` | `NeuronBehaviorAdaptation` | required |

Returns `torch.Tensor`.

## dequantize_mixed_neuron_behavior_parameters

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L218-L251)

```python
dequantize_mixed_neuron_behavior_parameters(bank: MixedQuantizedNeuronBehaviorBank, *, adaptation: NeuronBehaviorAdaptation) -> torch.Tensor
```

Materialize a component-wise W4/W8 adaptation bank.

| Parameter | Type | Default |
| --- | --- | --- |
| `bank` | `MixedQuantizedNeuronBehaviorBank` | required |
| `adaptation` | `NeuronBehaviorAdaptation` | required |

Returns `torch.Tensor`.

## pack_neuron_behavior_adapter

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L341-L393)

```python
pack_neuron_behavior_adapter(adapter: NeuronBehaviorAdapter, *, adaptation: NeuronBehaviorAdaptation) -> torch.Tensor
```

Pack a trained behavior adapter into the population ABI.

| Parameter | Type | Default |
| --- | --- | --- |
| `adapter` | `NeuronBehaviorAdapter` | required |
| `adaptation` | `NeuronBehaviorAdaptation` | required |

Returns `torch.Tensor`.

## GRUPopulationRunner

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1344-L1556)

Compiled persistent-state inference for a shared-weight GRU population.

### GRUPopulationRunner.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1347-L1441)

```python
__init__(self, model: AxoTemporalModel, *, population: int, chunk_size: int, compile_step: bool=True, compile_mode: str='reduce-overhead', population_embedding_adapters: torch.Tensor | None=None) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `AxoTemporalModel` | required |
| `population` | `int` | required |
| `chunk_size` | `int` | required |
| `compile_step` | `bool` | `True` |
| `compile_mode` | `str` | `'reduce-overhead'` |
| `population_embedding_adapters` | `torch.Tensor \| None` | `None` |

Returns `None`.

### GRUPopulationRunner.recurrent_state

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1444-L1447)

```python
GRUPopulationRunner.recurrent_state: torch.Tensor
```

Read-only property. Access as `instance.recurrent_state`; do not call it as a function.

Returns `torch.Tensor`.

### GRUPopulationRunner.patch_sum

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1450-L1451)

```python
GRUPopulationRunner.patch_sum: torch.Tensor | None
```

Read-only property. Access as `instance.patch_sum`; do not call it as a function.

Returns `torch.Tensor \| None`.

### GRUPopulationRunner.patch_correction

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1454-L1455)

```python
GRUPopulationRunner.patch_correction: torch.Tensor | None
```

Read-only property. Access as `instance.patch_correction`; do not call it as a function.

Returns `torch.Tensor \| None`.

### GRUPopulationRunner.patch_position

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1458-L1459)

```python
GRUPopulationRunner.patch_position: int
```

Read-only property. Access as `instance.patch_position`; do not call it as a function.

Returns `int`.

### GRUPopulationRunner.step

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1461-L1526)

```python
step(self, event_indices: torch.Tensor, event_values: torch.Tensor, morphology_indices: torch.Tensor) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `event_indices` | `torch.Tensor` | required |
| `event_values` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor` | required |

Returns `torch.Tensor`.

## GRUBranchPopulationRunner

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1559-L1701)

Compiled GRU inference from pre-aggregated raw branch inputs.

Bases: `GRUPopulationRunner`.

### GRUBranchPopulationRunner.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1562-L1617)

```python
__init__(self, model: AxoTemporalModel, *, population: int, chunk_size: int, compile_step: bool=True, compile_mode: str='reduce-overhead', population_embedding_adapters: torch.Tensor | None=None) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `AxoTemporalModel` | required |
| `population` | `int` | required |
| `chunk_size` | `int` | required |
| `compile_step` | `bool` | `True` |
| `compile_mode` | `str` | `'reduce-overhead'` |
| `population_embedding_adapters` | `torch.Tensor \| None` | `None` |

Returns `None`.

### GRUBranchPopulationRunner.step

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1619-L1701)

```python
step(self, branch_inputs: torch.Tensor, morphology_indices: torch.Tensor) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `branch_inputs` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor` | required |

Returns `torch.Tensor`.

## AdaptedGRUBranchPopulationRunner

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1704-L1995)

Packed per-neuron behavior adaptation around one shared GRU base.

Bases: `GRUBranchPopulationRunner`.

### AdaptedGRUBranchPopulationRunner.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1709-L1918)

```python
__init__(self, model: AxoTemporalModel, *, population: int, chunk_size: int, behavior_parameters: torch.Tensor | QuantizedNeuronBehaviorBank | MixedQuantizedNeuronBehaviorBank, adaptation: NeuronBehaviorAdaptation, compile_step: bool=True, compile_mode: str='max-autotune-no-cudagraphs') -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `AxoTemporalModel` | required |
| `population` | `int` | required |
| `chunk_size` | `int` | required |
| `behavior_parameters` | `torch.Tensor \| QuantizedNeuronBehaviorBank \| MixedQuantizedNeuronBehaviorBank` | required |
| `adaptation` | `NeuronBehaviorAdaptation` | required |
| `compile_step` | `bool` | `True` |
| `compile_mode` | `str` | `'max-autotune-no-cudagraphs'` |

Returns `None`.

### AdaptedGRUBranchPopulationRunner.step

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1920-L1995)

```python
step(self, branch_inputs: torch.Tensor, morphology_indices: torch.Tensor) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `branch_inputs` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor` | required |

Returns `torch.Tensor`.

## GroupedGRUPopulationRunner

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1998-L2270)

Compiled GRU inference with one recurrent parameter set per group.

### GroupedGRUPopulationRunner.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L2001-L2109)

```python
__init__(self, model: AxoTemporalModel, *, population: int, groups: int, chunk_size: int, compile_step: bool=True, compile_mode: str='reduce-overhead') -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `model` | `AxoTemporalModel` | required |
| `population` | `int` | required |
| `groups` | `int` | required |
| `chunk_size` | `int` | required |
| `compile_step` | `bool` | `True` |
| `compile_mode` | `str` | `'reduce-overhead'` |

Returns `None`.

### GroupedGRUPopulationRunner.resident_parameter_count

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L2112-L2116)

```python
GroupedGRUPopulationRunner.resident_parameter_count: int
```

Read-only property. Access as `instance.resident_parameter_count`; do not call it as a function.

Returns `int`.

### GroupedGRUPopulationRunner.patch_position

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L2119-L2120)

```python
GroupedGRUPopulationRunner.patch_position: int
```

Read-only property. Access as `instance.patch_position`; do not call it as a function.

Returns `int`.

### GroupedGRUPopulationRunner.step

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L2122-L2191)

```python
step(self, event_indices: torch.Tensor, event_values: torch.Tensor, morphology_indices: torch.Tensor) -> torch.Tensor
```

| Parameter | Type | Default |
| --- | --- | --- |
| `event_indices` | `torch.Tensor` | required |
| `event_values` | `torch.Tensor` | required |
| `morphology_indices` | `torch.Tensor` | required |

Returns `torch.Tensor`.

### GroupedGRUPopulationRunner.load_group_recurrent_parameters

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L2193-L2229)

```python
load_group_recurrent_parameters(self, group: int, source: AxoTemporalModel) -> None
```

Load one group's recurrent weights from a compatible GRU model.

| Parameter | Type | Default |
| --- | --- | --- |
| `group` | `int` | required |
| `source` | `AxoTemporalModel` | required |

Returns `None`.

## NeuronBehaviorAdaptation

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L7-L135)

Mechanism-level parameters that remain unique to each neuron.

```python
NeuronBehaviorAdaptation(width: int, branches: int, outputs: int, matrix_rank: int, adapt_recurrent: bool, branch_token_offset: bool = False) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `width` | `int` | required |
| `branches` | `int` | required |
| `outputs` | `int` | required |
| `matrix_rank` | `int` | required |
| `adapt_recurrent` | `bool` | required |
| `branch_token_offset` | `bool` | `False` |

### NeuronBehaviorAdaptation.tensor_shapes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L18-L77)

```python
NeuronBehaviorAdaptation.tensor_shapes: dict[str, tuple[int, ...]]
```

Read-only property. Access as `instance.tensor_shapes`; do not call it as a function.

Returns `dict[str, tuple[int, ...]]`.

### NeuronBehaviorAdaptation.tensor_slices

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L80-L89)

```python
NeuronBehaviorAdaptation.tensor_slices: dict[str, slice]
```

Read-only property. Access as `instance.tensor_slices`; do not call it as a function.

Returns `dict[str, slice]`.

### NeuronBehaviorAdaptation.parameter_counts

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L92-L116)

```python
NeuronBehaviorAdaptation.parameter_counts: dict[str, int]
```

Read-only property. Access as `instance.parameter_counts`; do not call it as a function.

Returns `dict[str, int]`.

### NeuronBehaviorAdaptation.parameter_count

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L119-L120)

```python
NeuronBehaviorAdaptation.parameter_count: int
```

Read-only property. Access as `instance.parameter_count`; do not call it as a function.

Returns `int`.

### NeuronBehaviorAdaptation.adapted_components

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L123-L124)

```python
NeuronBehaviorAdaptation.adapted_components: frozenset[str]
```

Read-only property. Access as `instance.adapted_components`; do not call it as a function.

Returns `frozenset[str]`.

### NeuronBehaviorAdaptation.shared_components

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L127-L135)

```python
NeuronBehaviorAdaptation.shared_components: frozenset[str]
```

Read-only property. Access as `instance.shared_components`; do not call it as a function.

Returns `frozenset[str]`.

## PopulationDeploymentMeasurement

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L139-L165)

One complete population-simulation measurement.

```python
PopulationDeploymentMeasurement(population: int, adapted_parameters_per_neuron: int, adapted_components: tuple[str, ...], shared_components: tuple[str, ...], unique_adaptation_per_neuron: bool, adaptation_quality_validated: bool, shared_frozen_base: bool, output_materialized: bool, routing_feeds_model: bool, model_latency_ms: float, routing_latency_ms: float | None, complete_stack_latency_ms: float | None, model_peak_bytes: int, routing_peak_bytes: int | None, complete_stack_peak_bytes: int | None, local_source_identity_retained: bool = False, long_range_source_identity_retained: bool = False, morphology_assignment_independent: bool = False, activity_generation_mode: str = 'unknown', activity_dynamics_validated: bool = False, adaptation_execution_mode: str = 'direct', adaptation_reference_envelope_validated: bool = False, forecast_block_size: int = 1, complete_block_latency_ms: float | None = None) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `population` | `int` | required |
| `adapted_parameters_per_neuron` | `int` | required |
| `adapted_components` | `tuple[str, ...]` | required |
| `shared_components` | `tuple[str, ...]` | required |
| `unique_adaptation_per_neuron` | `bool` | required |
| `adaptation_quality_validated` | `bool` | required |
| `shared_frozen_base` | `bool` | required |
| `output_materialized` | `bool` | required |
| `routing_feeds_model` | `bool` | required |
| `model_latency_ms` | `float` | required |
| `routing_latency_ms` | `float \| None` | required |
| `complete_stack_latency_ms` | `float \| None` | required |
| `model_peak_bytes` | `int` | required |
| `routing_peak_bytes` | `int \| None` | required |
| `complete_stack_peak_bytes` | `int \| None` | required |
| `local_source_identity_retained` | `bool` | `False` |
| `long_range_source_identity_retained` | `bool` | `False` |
| `morphology_assignment_independent` | `bool` | `False` |
| `activity_generation_mode` | `str` | `'unknown'` |
| `activity_dynamics_validated` | `bool` | `False` |
| `adaptation_execution_mode` | `str` | `'direct'` |
| `adaptation_reference_envelope_validated` | `bool` | `False` |
| `forecast_block_size` | `int` | `1` |
| `complete_block_latency_ms` | `float \| None` | `None` |

## PopulationDeploymentTarget

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L169-L376)

Requirements for a defensible real-time population claim.

```python
PopulationDeploymentTarget(headline_population: int, benchmark_population: int, biological_step_ms: float, adaptation: NeuronBehaviorAdaptation, shared_frozen_base: bool, output_materialization_required: bool, network_routing_required: bool, local_source_identity_required: bool, long_range_source_identity_required: bool, independent_morphology_assignment_required: bool, activity_dynamics_validation_required: bool, quota_activity_allowed: bool, forecast_block_size: int, firing_rate: float, fanout: int) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `headline_population` | `int` | required |
| `benchmark_population` | `int` | required |
| `biological_step_ms` | `float` | required |
| `adaptation` | `NeuronBehaviorAdaptation` | required |
| `shared_frozen_base` | `bool` | required |
| `output_materialization_required` | `bool` | required |
| `network_routing_required` | `bool` | required |
| `local_source_identity_required` | `bool` | required |
| `long_range_source_identity_required` | `bool` | required |
| `independent_morphology_assignment_required` | `bool` | required |
| `activity_dynamics_validation_required` | `bool` | required |
| `quota_activity_allowed` | `bool` | required |
| `forecast_block_size` | `int` | required |
| `firing_rate` | `float` | required |
| `fanout` | `int` | required |

### PopulationDeploymentTarget.adapted_parameters_per_neuron

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L189-L190)

```python
PopulationDeploymentTarget.adapted_parameters_per_neuron: int
```

Read-only property. Access as `instance.adapted_parameters_per_neuron`; do not call it as a function.

Returns `int`.

### PopulationDeploymentTarget.validation_errors

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L192-L340)

```python
validation_errors(self, measurement: PopulationDeploymentMeasurement) -> tuple[str, ...]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `measurement` | `PopulationDeploymentMeasurement` | required |

Returns `tuple[str, ...]`.

### PopulationDeploymentTarget.evaluate

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L342-L376)

```python
evaluate(self, measurement: PopulationDeploymentMeasurement) -> dict[str, int | float | bool]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `measurement` | `PopulationDeploymentMeasurement` | required |

Returns `dict[str, int \| float \| bool]`.
