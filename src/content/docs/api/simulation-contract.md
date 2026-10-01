---
title: Population simulation contracts
description: Signatures, parameters, return contracts, and source for population simulation contracts.
section: API reference
order: 210
---

## Module contract

The immutable simulation contract specifies the connected workload and timing boundary. PopulationInferenceProfile specifies a deployment recipe. These values are declarations, not measured speed results. Check the technical report's measured throughput at the contact count and population scale relevant to your application.

Source revision: `306a51ed950b`. [Public export index](/api/).

## LargePopulationSimulationContract

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L9-L272)

Fully specified model and network workload for a population step.

```python
LargePopulationSimulationContract(name: str, population_size: int, step_ms: float, input_step_ms: float, output_step_ms: float, target_latency_ms: float, model_family: str, patch_size: int, temporal_execution_mode: str, patch_phase_mode: str, patch_phase_assignment: str, patch_phase_storage_layout: str, lossless_ordered_temporal_io: bool, causal_block_feedback_required: bool, minimum_routing_delay_steps: int, synaptic_efficacy_values_per_neuron: int, adaptation_storage_bits: int, activation_storage_bits: int, recurrent_state_storage_bits: int, external_drive_storage_bits: int, morphology_classes: int, firing_rate: float, fanout: int, recurrent_contact_fraction: float, excitatory_fraction: float, local_connection_fraction: float, spatial_tile_neurons: int, delay_slots: int, branch_count: int, local_source_identity_required: bool, long_range_source_identity_required: bool, local_branch_input_mode: str, input_channel_collision_mode: str, local_source_summary_is_lossless_for_declared_router: bool, posthoc_source_projection_allowed: bool, morphology_assignment_independent: bool, activity_must_be_model_generated: bool, quota_activity_forcing_allowed: bool, activity_selection_mode: str, adaptation_reference_envelope_validation_required: bool, morphology_aware_branch_targeting: bool = True, source_type_aware_branch_targeting: bool = True, source_discovery_included: bool = True, event_delivery_included: bool = True, delay_queue_included: bool = True, every_neuron_has_custom_adaptation: bool = True, empirical_connectome: bool = False) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `name` | `str` | required |
| `population_size` | `int` | required |
| `step_ms` | `float` | required |
| `input_step_ms` | `float` | required |
| `output_step_ms` | `float` | required |
| `target_latency_ms` | `float` | required |
| `model_family` | `str` | required |
| `patch_size` | `int` | required |
| `temporal_execution_mode` | `str` | required |
| `patch_phase_mode` | `str` | required |
| `patch_phase_assignment` | `str` | required |
| `patch_phase_storage_layout` | `str` | required |
| `lossless_ordered_temporal_io` | `bool` | required |
| `causal_block_feedback_required` | `bool` | required |
| `minimum_routing_delay_steps` | `int` | required |
| `synaptic_efficacy_values_per_neuron` | `int` | required |
| `adaptation_storage_bits` | `int` | required |
| `activation_storage_bits` | `int` | required |
| `recurrent_state_storage_bits` | `int` | required |
| `external_drive_storage_bits` | `int` | required |
| `morphology_classes` | `int` | required |
| `firing_rate` | `float` | required |
| `fanout` | `int` | required |
| `recurrent_contact_fraction` | `float` | required |
| `excitatory_fraction` | `float` | required |
| `local_connection_fraction` | `float` | required |
| `spatial_tile_neurons` | `int` | required |
| `delay_slots` | `int` | required |
| `branch_count` | `int` | required |
| `local_source_identity_required` | `bool` | required |
| `long_range_source_identity_required` | `bool` | required |
| `local_branch_input_mode` | `str` | required |
| `input_channel_collision_mode` | `str` | required |
| `local_source_summary_is_lossless_for_declared_router` | `bool` | required |
| `posthoc_source_projection_allowed` | `bool` | required |
| `morphology_assignment_independent` | `bool` | required |
| `activity_must_be_model_generated` | `bool` | required |
| `quota_activity_forcing_allowed` | `bool` | required |
| `activity_selection_mode` | `str` | required |
| `adaptation_reference_envelope_validation_required` | `bool` | required |
| `morphology_aware_branch_targeting` | `bool` | `True` |
| `source_type_aware_branch_targeting` | `bool` | `True` |
| `source_discovery_included` | `bool` | `True` |
| `event_delivery_included` | `bool` | `True` |
| `delay_queue_included` | `bool` | `True` |
| `every_neuron_has_custom_adaptation` | `bool` | `True` |
| `empirical_connectome` | `bool` | `False` |

`population_size`: Number of persistent neurons. `patch_size`: Native timesteps represented by one block.

### LargePopulationSimulationContract.steps_per_second

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L216-L217)

```python
LargePopulationSimulationContract.steps_per_second: float
```

Read-only property. Access as `instance.steps_per_second`; do not call it as a function.

Returns `float`.

### LargePopulationSimulationContract.target_neuron_steps_per_second

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L220-L221)

```python
LargePopulationSimulationContract.target_neuron_steps_per_second: float
```

Read-only property. Access as `instance.target_neuron_steps_per_second`; do not call it as a function.

Returns `float`.

### LargePopulationSimulationContract.largest_patch_phase_population

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L224-L227)

```python
LargePopulationSimulationContract.largest_patch_phase_population: int
```

Read-only property. Access as `instance.largest_patch_phase_population`; do not call it as a function.

Returns `int`.

### LargePopulationSimulationContract.active_sources_per_step

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L230-L231)

```python
LargePopulationSimulationContract.active_sources_per_step: int
```

Read-only property. Access as `instance.active_sources_per_step`; do not call it as a function.

Returns `int`.

### LargePopulationSimulationContract.events_per_step

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L234-L239)

```python
LargePopulationSimulationContract.events_per_step: int
```

Read-only property. Access as `instance.events_per_step`; do not call it as a function.

Returns `int`.

### LargePopulationSimulationContract.synaptic_efficacy_bank_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L242-L248)

```python
LargePopulationSimulationContract.synaptic_efficacy_bank_bytes: int
```

Read-only property. Access as `instance.synaptic_efficacy_bank_bytes`; do not call it as a function.

Returns `int`.

### LargePopulationSimulationContract.delay_queue_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L251-L258)

```python
LargePopulationSimulationContract.delay_queue_bytes: int
```

Read-only property. Access as `instance.delay_queue_bytes`; do not call it as a function.

Returns `int`.

### LargePopulationSimulationContract.external_drive_block_bytes

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L261-L268)

```python
LargePopulationSimulationContract.external_drive_block_bytes: int
```

Read-only property. Access as `instance.external_drive_block_bytes`; do not call it as a function.

Returns `int`.

### LargePopulationSimulationContract.bytes_to_gib

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L271-L272)

```python
@staticmethod
bytes_to_gib(byte_count: int) -> float
```

| Parameter | Type | Default |
| --- | --- | --- |
| `byte_count` | `int` | required |

Returns `float`.

## PopulationInferenceProfile

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L276-L361)

Named operating point within the million-neuron contract.

```python
PopulationInferenceProfile(name: str, support_model_id: str, support_token_width: int, support_state_width: int, support_block_rows: int, support_block_token: int, support_block_state: int, external_block_width: int, project_block_width: int, compiled_adaptation_values_per_neuron: int, morphology_adapter_values_per_class: int, synaptic_efficacy_values_per_neuron: int, output_export_fraction: float, primary_metric: str, minimum_neuron_steps_per_second: float, measured_median_neuron_steps_per_second: float, measured_p90_neuron_steps_per_second: float, measured_voltage_sera_mv2: float, measured_voltage_root_sera_mv: float, measured_spike_mean_f1: float, measured_population_firing_rate_hz: float, population_adaptation_initialization: str, population_adaptation_individually_fitted: bool, individual_behavior_adaptation_supported: bool, individual_synaptic_adaptation_supported: bool) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `name` | `str` | required |
| `support_model_id` | `str` | required |
| `support_token_width` | `int` | required |
| `support_state_width` | `int` | required |
| `support_block_rows` | `int` | required |
| `support_block_token` | `int` | required |
| `support_block_state` | `int` | required |
| `external_block_width` | `int` | required |
| `project_block_width` | `int` | required |
| `compiled_adaptation_values_per_neuron` | `int` | required |
| `morphology_adapter_values_per_class` | `int` | required |
| `synaptic_efficacy_values_per_neuron` | `int` | required |
| `output_export_fraction` | `float` | required |
| `primary_metric` | `str` | required |
| `minimum_neuron_steps_per_second` | `float` | required |
| `measured_median_neuron_steps_per_second` | `float` | required |
| `measured_p90_neuron_steps_per_second` | `float` | required |
| `measured_voltage_sera_mv2` | `float` | required |
| `measured_voltage_root_sera_mv` | `float` | required |
| `measured_spike_mean_f1` | `float` | required |
| `measured_population_firing_rate_hz` | `float` | required |
| `population_adaptation_initialization` | `str` | required |
| `population_adaptation_individually_fitted` | `bool` | required |
| `individual_behavior_adaptation_supported` | `bool` | required |
| `individual_synaptic_adaptation_supported` | `bool` | required |

## MILLION_NEURON_REALTIME_CONTRACT

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L362-L405)

```python
MILLION_NEURON_REALTIME_CONTRACT = LargePopulationSimulationContract(name='million-neuron-realtime-rtx5090', population_size=1048576, step_ms=1.0, input_step_ms=1.0, output_step_ms=1.0, target_latency_ms=1.0, model_family='axosim-lite-causal-block-gru-regression', patch_size=4, temporal_execution_mode='causal_next_block_forecast', patch_phase_mode='staggered', patch_phase_assignment='morphology_role_stratified_random', patch_phase_storage_layout='phase_tile_major', lossless_ordered_temporal_io=True, causal_block_feedback_required=True, minimum_routing_delay_steps=4, synaptic_efficacy_values_per_neuron=362, adaptation_storage_bits=8, activation_storage_bits=16, recurrent_state_storage_bits=16, external_drive_storage_bits=8, morphology_classes=5, firing_rate=0.003869090909090909, fanout=1448, recurrent_contact_fraction=1.0 / 4.0, excitatory_fraction=0.8, local_connection_fraction=0.9, spatial_tile_neurons=4096, delay_slots=8, branch_count=118, local_source_identity_required=True, long_range_source_identity_required=True, local_branch_input_mode='binary_channels_then_exact_weighted_branch_currents', input_channel_collision_mode='binary_or_before_branch_weighting', local_source_summary_is_lossless_for_declared_router=True, posthoc_source_projection_allowed=False, morphology_assignment_independent=True, activity_must_be_model_generated=True, quota_activity_forcing_allowed=False, activity_selection_mode='fixed_model_score_threshold_crossing', adaptation_reference_envelope_validation_required=True)
```

## AXOSIM_POPULATION_PROFILE

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L407-L437)

```python
AXOSIM_POPULATION_PROFILE = PopulationInferenceProfile(name='axosim-population', support_model_id='support_t24_s8_distilled_i600', support_token_width=24, support_state_width=8, support_block_rows=32, support_block_token=32, support_block_state=16, external_block_width=32, project_block_width=64, compiled_adaptation_values_per_neuron=88, morphology_adapter_values_per_class=88, synaptic_efficacy_values_per_neuron=362, output_export_fraction=0.01, primary_metric='neuron_steps_per_second', minimum_neuron_steps_per_second=MILLION_NEURON_REALTIME_CONTRACT.target_neuron_steps_per_second, measured_median_neuron_steps_per_second=1201327144.0976055, measured_p90_neuron_steps_per_second=1177454556.7997348, measured_voltage_sera_mv2=225.82762062058336, measured_voltage_root_sera_mv=15.02756203183282, measured_spike_mean_f1=0.35383167978104685, measured_population_firing_rate_hz=3.956115245819092, population_adaptation_initialization='five_fitted_morphology_rows_plus_direct_w8_behavior_residuals', population_adaptation_individually_fitted=False, individual_behavior_adaptation_supported=True, individual_synaptic_adaptation_supported=True)
```
