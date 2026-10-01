---
title: Population simulation contracts
description: Signatures, parameters, return contracts, and source for population simulation contracts.
section: API reference
apiGroup: Populations
order: 210
---

## Overview

The immutable simulation contract specifies the connected workload and timing boundary. PopulationInferenceProfile specifies a deployment recipe. These values are declarations, not measured speed results. Check the technical report's measured throughput at the contact count and population scale relevant to your application.

Source revision: `306a51ed950b`. [Public export index](/api/).

<section class="api-symbol" id="simulation-contract-largepopulationsimulationcontract">

## LargePopulationSimulationContract

<div class="api-signature">

```python
axosim.simulation_contract.LargePopulationSimulationContract(name: str, population_size: int, step_ms: float, input_step_ms: float, output_step_ms: float, target_latency_ms: float, model_family: str, patch_size: int, temporal_execution_mode: str, patch_phase_mode: str, patch_phase_assignment: str, patch_phase_storage_layout: str, lossless_ordered_temporal_io: bool, causal_block_feedback_required: bool, minimum_routing_delay_steps: int, synaptic_efficacy_values_per_neuron: int, adaptation_storage_bits: int, activation_storage_bits: int, recurrent_state_storage_bits: int, external_drive_storage_bits: int, morphology_classes: int, firing_rate: float, fanout: int, recurrent_contact_fraction: float, excitatory_fraction: float, local_connection_fraction: float, spatial_tile_neurons: int, delay_slots: int, branch_count: int, local_source_identity_required: bool, long_range_source_identity_required: bool, local_branch_input_mode: str, input_channel_collision_mode: str, local_source_summary_is_lossless_for_declared_router: bool, posthoc_source_projection_allowed: bool, morphology_assignment_independent: bool, activity_must_be_model_generated: bool, quota_activity_forcing_allowed: bool, activity_selection_mode: str, adaptation_reference_envelope_validation_required: bool, morphology_aware_branch_targeting: bool = True, source_type_aware_branch_targeting: bool = True, source_discovery_included: bool = True, event_delivery_included: bool = True, delay_queue_included: bool = True, every_neuron_has_custom_adaptation: bool = True, empirical_connectome: bool = False)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L9-L272)

</div>

Fully specified model and network workload for a population step.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Name of the optional shard array or declared record.</dd>
<dt><code>population_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Number of persistent neurons.</dd>
<dt><code>step_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>input_step_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>output_step_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>target_latency_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>model_family</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>patch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Native timesteps represented by one block.</dd>
<dt><code>temporal_execution_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>patch_phase_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>patch_phase_assignment</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>patch_phase_storage_layout</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>lossless_ordered_temporal_io</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>causal_block_feedback_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>minimum_routing_delay_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>synaptic_efficacy_values_per_neuron</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>adaptation_storage_bits</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>activation_storage_bits</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>recurrent_state_storage_bits</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>external_drive_storage_bits</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>morphology_classes</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>firing_rate</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>fanout</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>recurrent_contact_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>excitatory_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>local_connection_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>spatial_tile_neurons</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>delay_slots</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>branch_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>local_source_identity_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>long_range_source_identity_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>local_branch_input_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>input_channel_collision_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>local_source_summary_is_lossless_for_declared_router</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>posthoc_source_projection_allowed</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>morphology_assignment_independent</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>activity_must_be_model_generated</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>quota_activity_forcing_allowed</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>activity_selection_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>adaptation_reference_envelope_validation_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>morphology_aware_branch_targeting</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>source_type_aware_branch_targeting</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>source_discovery_included</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>event_delivery_included</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>delay_queue_included</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>every_neuron_has_custom_adaptation</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>empirical_connectome</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="simulation-contract-largepopulationsimulationcontract-steps-per-second"><code>LargePopulationSimulationContract.steps_per_second: float</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L216-L217">Source</a></dd>
<dt id="simulation-contract-largepopulationsimulationcontract-target-neuron-steps-per-second"><code>LargePopulationSimulationContract.target_neuron_steps_per_second: float</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L220-L221">Source</a></dd>
<dt id="simulation-contract-largepopulationsimulationcontract-largest-patch-phase-population"><code>LargePopulationSimulationContract.largest_patch_phase_population: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L224-L227">Source</a></dd>
<dt id="simulation-contract-largepopulationsimulationcontract-active-sources-per-step"><code>LargePopulationSimulationContract.active_sources_per_step: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L230-L231">Source</a></dd>
<dt id="simulation-contract-largepopulationsimulationcontract-events-per-step"><code>LargePopulationSimulationContract.events_per_step: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L234-L239">Source</a></dd>
<dt id="simulation-contract-largepopulationsimulationcontract-synaptic-efficacy-bank-bytes"><code>LargePopulationSimulationContract.synaptic_efficacy_bank_bytes: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L242-L248">Source</a></dd>
<dt id="simulation-contract-largepopulationsimulationcontract-delay-queue-bytes"><code>LargePopulationSimulationContract.delay_queue_bytes: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L251-L258">Source</a></dd>
<dt id="simulation-contract-largepopulationsimulationcontract-external-drive-block-bytes"><code>LargePopulationSimulationContract.external_drive_block_bytes: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L261-L268">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#simulation-contract-largepopulationsimulationcontract-bytes-to-gib"><code>LargePopulationSimulationContract.bytes_to_gib()</code></a></li>
</ul>

<section class="api-method" id="simulation-contract-largepopulationsimulationcontract-bytes-to-gib">

### LargePopulationSimulationContract.bytes_to_gib

<div class="api-signature">

```python
@staticmethod
axosim.simulation_contract.LargePopulationSimulationContract.bytes_to_gib(byte_count: int) -> float
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L271-L272)

</div>

Convert a byte count to gibibytes using 1024 cubed bytes per GiB.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>byte_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Storage count in bytes.</dd>
</dl>

<p class="api-label">Returns</p>

`float`

</section>

</section>

<section class="api-symbol" id="simulation-contract-populationinferenceprofile">

## PopulationInferenceProfile

<div class="api-signature">

```python
axosim.simulation_contract.PopulationInferenceProfile(name: str, support_model_id: str, support_token_width: int, support_state_width: int, support_block_rows: int, support_block_token: int, support_block_state: int, external_block_width: int, project_block_width: int, compiled_adaptation_values_per_neuron: int, morphology_adapter_values_per_class: int, synaptic_efficacy_values_per_neuron: int, output_export_fraction: float, primary_metric: str, minimum_neuron_steps_per_second: float, measured_median_neuron_steps_per_second: float, measured_p90_neuron_steps_per_second: float, measured_voltage_sera_mv2: float, measured_voltage_root_sera_mv: float, measured_spike_mean_f1: float, measured_population_firing_rate_hz: float, population_adaptation_initialization: str, population_adaptation_individually_fitted: bool, individual_behavior_adaptation_supported: bool, individual_synaptic_adaptation_supported: bool)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L276-L361)

</div>

Named operating point within the million-neuron contract.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Name of the optional shard array or declared record.</dd>
<dt><code>support_model_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>support_token_width</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>support_state_width</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>support_block_rows</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>support_block_token</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>support_block_state</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>external_block_width</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>project_block_width</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>compiled_adaptation_values_per_neuron</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>morphology_adapter_values_per_class</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>synaptic_efficacy_values_per_neuron</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>output_export_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>primary_metric</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>minimum_neuron_steps_per_second</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>measured_median_neuron_steps_per_second</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>measured_p90_neuron_steps_per_second</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>measured_voltage_sera_mv2</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>measured_voltage_root_sera_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>measured_spike_mean_f1</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>measured_population_firing_rate_hz</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>population_adaptation_initialization</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>population_adaptation_individually_fitted</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>individual_behavior_adaptation_supported</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>individual_synaptic_adaptation_supported</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="simulation-contract-million-neuron-realtime-contract">

## MILLION_NEURON_REALTIME_CONTRACT

<div class="api-signature">

```python
axosim.simulation_contract.MILLION_NEURON_REALTIME_CONTRACT: LargePopulationSimulationContract
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L362-L405)

</div>

Named workload contract for the connected population benchmark. Its attributes specify the population, cadence, contact topology, precision, and timing boundary.

</section>

<section class="api-symbol" id="simulation-contract-axosim-population-profile">

## AXOSIM_POPULATION_PROFILE

<div class="api-signature">

```python
axosim.simulation_contract.AXOSIM_POPULATION_PROFILE: PopulationInferenceProfile
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/simulation_contract.py#L407-L437)

</div>

Named compact population deployment recipe, including its behavior storage and model dimensions.

</section>
