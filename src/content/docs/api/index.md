---
title: API reference
description: Public exports, exact implementation aliases, and complete module and CLI references.
section: API reference
order: 200
---

## Public Python surface

This reference covers all 34 names in `axosim.__all__` at revision `0f546adfd8fc`, plus the public module functions, configuration fields, dataset methods, and CLI options used by the guides. The package lazily imports these names; implementation aliases are stated explicitly.

| Import from axosim | Implementation | Reference |
| --- | --- | --- |
| `AXOSIM_POPULATION_PROFILE` | `axosim.simulation_contract.AXOSIM_POPULATION_PROFILE` | [Open](/api/simulation-contract/) |
| `MILLION_NEURON_REALTIME_CONTRACT` | `axosim.simulation_contract.MILLION_NEURON_REALTIME_CONTRACT` | [Open](/api/simulation-contract/) |
| `AxoMamba` | `axosim.axomamba.AxoMamba` | [Open](/api/mamba/) |
| `AxoMambaConfig` | `axosim.axomamba.AxoMambaConfig` | [Open](/api/mamba/) |
| `AxoSimGRU` | `axosim.block_forecast.CausalBlockForecastModel` | [Open](/api/block-forecast/) |
| `AxoSimLite` | `axosim.support_surrogate.AdaptiveSupportP4Surrogate` | [Open](/api/lite/) |
| `AxoSimMamba` | `axosim.axomamba.AxoMamba` | [Open](/api/mamba/) |
| `AxoSimModelProfile` | `axosim.model_family.AxoSimModelProfile` | [Open](/api/model-family/) |
| `AxoSimPopulation` | `axosim.interfaces.AxoSimPopulation` | [Open](/api/interfaces/) |
| `CudaGraphAdaptationStep` | `axosim.adaptation.CudaGraphAdaptationStep` | [Open](/api/adaptation/) |
| `HomeostaticThresholdController` | `axosim.activity.HomeostaticThresholdController` | [Open](/api/activity/) |
| `HistoryScanBackend` | `axosim.history_scan.HistoryScanBackend` | [Open](/api/history-scan/) |
| `HistoryScanResult` | `axosim.history_scan.HistoryScanResult` | [Open](/api/history-scan/) |
| `AXOSIM_MODEL_PROFILES` | `axosim.model_family.AXOSIM_MODEL_PROFILES` | [Open](/api/model-family/) |
| `BranchELM` | `axosim.model.BranchELM` | [Open](/api/model/) |
| `BranchELMConfig` | `axosim.model.BranchELMConfig` | [Open](/api/model/) |
| `LargePopulationSimulationContract` | `axosim.simulation_contract.LargePopulationSimulationContract` | [Open](/api/simulation-contract/) |
| `MixedQuantizedNeuronBehaviorBank` | `axosim.population.MixedQuantizedNeuronBehaviorBank` | [Open](/api/population/) |
| `PopulationInferenceProfile` | `axosim.simulation_contract.PopulationInferenceProfile` | [Open](/api/simulation-contract/) |
| `ProceduralMorphologyConnectomeRouter` | `axosim.connectome.ProceduralMorphologyConnectomeRouter` | [Open](/api/connectome/) |
| `QuantizedSynapticEfficacyBank` | `axosim.synapse.QuantizedSynapticEfficacyBank` | [Open](/api/synapse/) |
| `compact_active_sources` | `axosim.connectome.compact_active_sources` | [Open](/api/connectome/) |
| `dequantize_synaptic_efficacies` | `axosim.synapse.dequantize_synaptic_efficacies` | [Open](/api/synapse/) |
| `dequantize_mixed_neuron_behavior_parameters` | `axosim.population.dequantize_mixed_neuron_behavior_parameters` | [Open](/api/population/) |
| `quantize_synaptic_efficacies` | `axosim.synapse.quantize_synaptic_efficacies` | [Open](/api/synapse/) |
| `quantize_mixed_neuron_behavior_parameters` | `axosim.population.quantize_mixed_neuron_behavior_parameters` | [Open](/api/population/) |
| `create_axosim_profile` | `axosim.model_family.create_axosim_profile` | [Open](/api/model-family/) |
| `ConnectedPopulation` | `axosim.connected_population.ConnectedPopulation` | [Open](/api/connected-population/) |
| `ExplicitConnectome` | `axosim.connected_population.ExplicitConnectome` | [Open](/api/connected-population/) |
| `InputEvents` | `axosim.connected_population.InputEvents` | [Open](/api/connected-population/) |
| `PopulationFrame` | `axosim.connected_population.PopulationFrame` | [Open](/api/connected-population/) |
| `ProceduralConnectome` | `axosim.connected_population.ProceduralConnectome` | [Open](/api/connected-population/) |
| `create_population` | `axosim.connected_population.create_population` | [Open](/api/connected-population/) |
| `scan_histories` | `axosim.history_scan.scan_histories` | [Open](/api/history-scan/) |

`HomeostaticThresholdController` is experimental. Configuration recipes and workload constants describe construction or execution contracts; they are not benchmark measurements. Historical checkpoint classes remain documented because the loader supports them.

## Modules and configuration

- [Connected population lifecycle](/api/connected-population/)
- [Population interfaces](/api/interfaces/)
- [Supplied-history scan](/api/history-scan/)
- [Model profiles](/api/model-family/)
- [Mamba models and configuration](/api/mamba/)
- [GRU temporal models](/api/temporal-core/)
- [Block-forecast models](/api/block-forecast/)
- [Lite neuron and configuration](/api/lite/)
- [Branch-ELM compatibility](/api/model/)
- [Checkpoints](/api/checkpoint/)
- [CUDA Graph adaptation](/api/adaptation/)
- [Population simulation contracts](/api/simulation-contract/)
- [Behavior banks and population runners](/api/population/)
- [Synaptic efficacy banks](/api/synapse/)
- [Connectome routing](/api/connectome/)
- [Activity and experimental control](/api/activity/)
- [Trace datasets](/api/data/)
- [NeuronIO conversion](/api/neuronio/)
- [Local metrics and dataset evaluation](/api/metrics/)
- [Training functions](/api/training/)
- [Inference benchmarking](/api/inference-benchmark/)
- [AxoBench prediction adapters](/api/axobench/)
- [Setup workflow](/api/setup/)

## Command-line tools

- [AxoSim CLI](/api/cli/)
- [Setup CLI](/api/setup-cli/)
- [AxoBench evaluation CLI](/api/axobench-cli/)

## Source and inventory

Every source link is pinned to [revision 0f546adfd8fc](https://github.com/Axym-Labs/axosim/tree/0f546adfd8fc8530ff8ec0952ce7a1367616cf24). Repository access is currently required to open the AxoSim and AxoBench source links because these repositories are private. The [machine-readable API inventory](/api-inventory.json) records source locations, exact signatures, parameters/defaults, fields, methods, exported aliases, and CLI options. It is generated using AST parsing without importing PyTorch.
