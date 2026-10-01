#!/usr/bin/env python3
"""Generate source-linked AxoSim references without importing the package.

Only AST parsing and argparse construction are used; no torch/GPU dependency.
Pass --source to select a local AxoSim checkout. Generated files are
the module/API pages and public/api-inventory.json; guide prose is handwritten.
"""
from __future__ import annotations

import argparse
import ast
from copy import deepcopy
from html import escape
import json
import subprocess
from pathlib import Path


PAGES = [
    ("interfaces", "Population interfaces", ["interfaces"], "The public differentiable population combines one Lite model with persistent neuron identities, morphology assignments, contact routes, and adaptation banks. AxoSimMamba aliases AxoMamba; AxoSimLite aliases AdaptiveSupportP4Surrogate; AxoSimGRU currently aliases CausalBlockForecastModel. Named GRU profiles are built by create_axosim_profile and return AxoTemporalModel."),
    ("model-family", "Model profiles", ["model_family"], "Named profiles provide fixed architecture recipes. Construction returns an untrained model. Mamba profiles use AxoMamba; GRU profiles use AxoTemporalModel with a GRU temporal core. Preserve the backend and saved model kind when loading weights."),
    ("mamba", "Mamba models and configuration", ["axomamba", "mamba_official"], "AxoMamba is the public Mamba implementation and inherits BranchOfficialMamba. AxoMambaConfig inherits all BranchOfficialMambaConfig fields. The default_axomamba_config factory supplies the promoted recipe, which differs from the dataclass's raw field defaults. AxoPyTorchMamba is a test-oriented fallback with a different checkpoint format."),
    ("temporal-core", "GRU temporal models", ["temporal_core"], "AxoTemporalModel wraps the common backbone with a selected temporal core. Named public GRU profiles use this class. Full-sequence forward calls reset temporal state; streaming calls use an explicitly allocated persistent state. Low-level temporal cores and behavior adapters are included below for direct construction."),
    ("block-forecast", "Block-forecast models", ["block_forecast"], "CausalBlockForecastModel predicts native outputs through causal block forecasting. The top-level AxoSimGRU alias points to this implementation. Its backbone and BlockForecastConfig constructor contract differs from the named GRU-profile factory."),
    ("lite", "Lite neuron and configuration", ["support_surrogate"], "AxoSimLite aliases AdaptiveSupportP4Surrogate. Route features have shape (morphologies, input_dim, route_feature_dim). The Lite neuron forecasts four native outputs from preceding input blocks; sequence losses should mask the first four causal padding positions. SupportP4Config requires positive dimensions, patch_size=4, output_dim=2, and at least one morphology ID."),
    ("model", "Branch-ELM compatibility", ["model"], "BranchELM and BranchELMConfig provide the baseline and checkpoint-compatible branched neuron implementation. Inputs use (batch, time, input_channels); the standard two-channel readout contains a spike logit and a soma target coordinate."),
    ("checkpoint", "Checkpoints", ["checkpoint"], "Checkpoint files contain model_kind, config, state_dict, and metadata. save_checkpoint writes a temporary sibling then atomically replaces the destination. Model-only checkpoints do not store a complete optimizer or scheduler trajectory. load_checkpoint uses torch.load with weights_only=False, so load trusted artifacts."),
    ("adaptation", "CUDA Graph adaptation", ["adaptation"], "CudaGraphAdaptationStep captures one fixed-shape forward, loss, backward, optional gradient transform, and optimizer update. It restores module and optimizer state after warmup and capture. Replay copies source tensors into retained static buffers. CUDA inputs and optimizer parameters are required; shape, dtype, parameter groups, and allocations must remain compatible."),
    ("simulation-contract", "Population simulation contracts", ["simulation_contract"], "The immutable simulation contract specifies the connected workload and timing boundary. PopulationInferenceProfile specifies a deployment recipe. These values are declarations, not measured speed results. Check the technical report's measured throughput at the contact count and population scale relevant to your application."),
    ("population", "Behavior banks and population runners", ["population", "deployment"], "Behavior-bank quantization stores component scales and W4/W8 values separately from the shared model. Quantization is a deployment transformation, while training uses floating-point parameters. The low-level GRU population runners and deployment records expose the contracts used for direct runtime construction."),
    ("synapse", "Synaptic efficacy banks", ["synapse"], "An efficacy bank contains one positive multiplier for each retained incoming E/I contact slot. The retained width is 2*ceil(channels_per_role/recurrent_stride). W8 storage quantizes deviation around a positive baseline with one shared scale; dequantization reconstructs floating-point multipliers."),
    ("connectome", "Connectome routing", ["connectome"], "The routing modules construct procedural contact identities and delayed event delivery. ProceduralMorphologyConnectomeRouter retains morphology-conditioned branch targeting. Population IDs, local/long-range source identities, delay slots, and route topology must agree with the declared workload; procedural routing does not imply an empirical connectome."),
    ("activity", "Activity and experimental control", ["activity"], "Threshold functions convert model-generated spike logits into events using fixed declared thresholds. Patch-phase layout helpers organize native cadence. HomeostaticThresholdController is an experimental optional code feature; it is not required by the lifecycle guides and is not a contribution presented in the technical report."),
    ("data", "Trace datasets", ["data"], "NeuronIO shards store inputs (samples, time, channels), targets (samples, time, 2), and sample identities. Dataset samples expose one (time, channels) input and one (time, 2) target. get_batch returns batched NumPy arrays. Window datasets preserve sample identity while selecting native time windows; preserve context boundaries when splitting data."),
    ("neuronio", "NeuronIO conversion", ["neuronio_raw"], "The converter reads raw NeuronIO teacher traces and creates deterministic shards. Standard soma normalization clips at -55 mV and applies (v_mV-bias)*scale with bias=-67.7 and scale=0.1. Preserve conversion metadata: normalized targets cannot recover clipped spike peaks."),
    ("metrics", "Local metrics and dataset evaluation", ["metrics", "evaluate"], "These local utility functions support RMSE, AUC, and dataset evaluation. AxoBench introduces and implements the report's Mean F1, Voltage SERA, and Dynamics SERA protocol; use axosim-evaluate-model for that core metric set. SERA uses squared error; Root-SERA is its square-root presentation."),
    ("training", "Training functions", ["train"], "The trainer fits native spike and soma targets with configurable losses, optimization, windowing, and validation. Model checkpoints store weights and metadata; preserve optimizer, scheduler, random, and data-order states separately when continuing an optimization trajectory."),
    ("inference-benchmark", "Inference benchmarking", ["inference_benchmark"], "The benchmark measures model sequence execution across batch sizes, horizons, and precision choices. It does not include the complete connected population runtime. Preserve the warmup, repetitions, synchronization, compilation mode, device, and shape contract with every reported timing."),
    ("axobench", "AxoBench prediction adapters", ["axobench_iteration"], "Prediction adapters reconstruct checkpoint models, select morphology identities, and return NumPy arrays in AxoBench's expected coordinates. The current AxoBench package is an additional dependency for the CLI evaluator. The source supports native and streaming predictor options in Python; the CLI exposes its declared subset."),
    ("setup", "Setup workflow", ["setup_workflow"], "Setup planning separates the declared installation/download/conversion steps from execution. Default setup creates local directories and installs the checkout; downloads occur only when explicitly requested. A dry run prints the plan without executing its commands."),
]

API_GROUPS = {
    **dict.fromkeys(("model-family", "mamba", "temporal-core", "block-forecast", "lite", "checkpoint"), "Models"),
    **dict.fromkeys(("interfaces", "population", "simulation-contract", "synapse", "connectome", "activity"), "Populations"),
    **dict.fromkeys(("adaptation", "training", "metrics", "inference-benchmark"), "Training and evaluation"),
    **dict.fromkeys(("data", "axobench"), "Data"),
    **dict.fromkeys(("model", "neuronio"), "Compatibility"),
    **dict.fromkeys(("cli", "setup-cli", "axobench-cli", "setup"), "CLI"),
}

CONTRACTS = {
    "interfaces.AxoSimPopulation.__init__": "neuron is a Lite model. morphology_indices is integer (N,); contact_branch_indices is integer (N,K), with values in [0, neuron.config.input_dim). The morphology indices must refer to declared morphology classes. Buffers are cloned and converted to long.",
    "interfaces.AxoSimPopulation.forward": "contact_inputs is (N,T,K). Optional synaptic_log_efficacy is (N,K) and replaces the stored efficacy values for this call. Return shape is (N,T,2); hidden state starts fresh for the sequence.",
    "interfaces.AxoSimPopulation.forward_sparse_contacts": "The three event tensors are equal-length one-dimensional arrays. Summary indices address n*T+t; contact indices address n*K+k, and both must identify the same neuron. Integer indices and floating event values must share the module device. Return shape is (N,time_steps,2). Gradients propagate through amplitudes and selected efficacies.",
    "interfaces.AxoSimPopulation.forward_batch": "contact_inputs is (B,N,T,K). Independent examples share population identities and adaptation banks. Return shape is (B,N,T,2).",
    "interfaces.AxoSimPopulation.forward_tokens": "tokens is (N,blocks,token_dim), already encoded at P4 cadence. Return shape is (N,blocks*4,2). This path decodes supplied tokens directly rather than adding the dense-input path's initial padding.",
    "interfaces.AxoSimPopulation.forward_token_batch": "tokens is (B,N,blocks,token_dim). Return shape is (B,N,blocks*4,2).",
    "interfaces.AxoSimPopulation.enable_adaptation_training": "Freezes shared Lite parameters, then independently enables or freezes behavior_adapter, morphology_adapter, and synaptic_log_efficacy. The defaults enable all three groups.",
    "interfaces.AxoSimPopulation.enable_full_training": "Enables requires_grad on every module parameter, including shared neuron weights.",
    "interfaces.AxoSimPopulation.synaptic_efficacies": "Returns exp(log_efficacy) with shape (N,K). Signed contact event amplitudes carry excitation/inhibition; efficacy remains positive.",
    "interfaces.AxoSimPopulation.adaptation_parameters": "Yields behavior_adapter, morphology_adapter, and synaptic_log_efficacy in that order.",
    "interfaces.AxoSimPopulation.trainable_adaptation_parameters": "Yields only adaptation parameters whose requires_grad flag is true.",
    "support_surrogate.AdaptiveSupportP4Surrogate.__init__": "route_features must match (len(config.morphology_ids),config.input_dim,config.route_feature_dim). They are cloned as a fixed floating-point buffer. Runtime cache width is 2*token_dim+3*state_dim+2*(patch_size*output_dim).",
    "support_surrogate.AdaptiveSupportP4Surrogate.forward": "inputs is (batch,native_steps,input_dim), with one morphology index per batch item where required. Return shape is (batch,native_steps,2). Mask the first four causal padding positions.",
    "support_surrogate.AdaptiveSupportP4Surrogate.aggregate_inputs": "inputs is (B,T,input_dim), and morphology_indices is integer (B,). Selects each item's route feature bank and returns feature summaries (B,T,route_feature_dim).",
    "support_surrogate.AdaptiveSupportP4Surrogate.compile_adaptation": "behavior_parameters is (B,behavior_parameter_count). Returns compiled coefficients (B,cache_width). Raises ValueError if the configuration disables the adaptation compiler or the width is incompatible.",
    "support_surrogate.AdaptiveSupportP4Surrogate.initial_state": "Allocates a zero state with shape (batch_size,state_dim) on the requested device/dtype.",
    "support_surrogate.AdaptiveSupportP4Surrogate.runtime_coefficient_slices": "Returns named slices for the seven deployed coefficient groups: token offset/gain, decay delta, recurrent-state gain/offset, and native-output gain/offset. The slices partition cache_width.",
    "support_surrogate.AdaptiveSupportP4Surrogate.step_token": "token is (B,token_dim), state is (B,state_dim), and optional adaptation_cache is (B,cache_width). Returns (forecast,next_state) with shapes (B,4,2) and (B,state_dim). This low-level step returns the decoded forecast directly.",
    "support_surrogate.AdaptiveSupportP4Surrogate.step_p4": "feature_patch is (B,4,route_feature_dim) and state is (B,state_dim). Supply either logical behavior_parameters or compiled adaptation_cache. Returns (forecast,next_state) with shapes (B,4,2) and (B,state_dim).",
    "support_surrogate.AdaptiveSupportP4Surrogate.forward_feature_summaries": "summaries is (B,T,route_feature_dim), with T>0. Select logical adaptation by morphology_indices or supply behavior_parameters when configured. Returns (B,T,2) with four initial causal padding positions.",
    "support_surrogate.AdaptiveSupportP4Surrogate.forward_runtime_coefficients": "summaries is (B,T,route_feature_dim), and runtime_coefficients must be (B,cache_width). Bypasses the logical adaptation compiler and returns (B,T,2) with the same causal padding as the summary sequence path.",
    "support_surrogate.AdaptiveSupportP4Surrogate.forward_with_gate_features": "inputs is (B,T,input_dim); morphology_indices is required. Returns (predictions,gate_features) with shapes (B,T,2) and (B,floor(T/4),token_dim+state_dim). Gate features are shifted causally by one block, and their first block is zero.",
    "mamba_official.BranchOfficialMamba.forward": "x is (B,T,num_input), and optional morphology_indices is integer (B,). Morphology-conditioned synaptic gains require valid morphology indices. Returns (B,T,num_output) in the checkpoint's spike-logit and soma-target coordinates.",
    "mamba_official.BranchOfficialMamba.allocate_streaming_state": "Allocates a persistent streaming-state record for the requested batch_size, device, and dtype. Allocate a fresh state for independent traces or changed batch membership.",
    "mamba_official.BranchOfficialMamba.streaming_step": "Advances the supplied mutable streaming state by one native input step. The guide supplies x as (B,num_input), with one morphology index per item when configured. Returns (B,1,num_output).",
    "temporal_core.AxoTemporalModel.forward": "x is (B,T,num_input), with integer morphology_indices (B,) when morphology conditioning or behavior adaptation is configured. Returns (B,T,num_output). Each sequence forward initializes the core state.",
    "temporal_core.AxoTemporalModel.allocate_streaming_state": "Allocates an AxoTemporalStreamingState for batch_size on the requested device and dtype; the state contains temporal-core values and causal local-filter histories.",
    "temporal_core.AxoTemporalModel.streaming_step": "Advances one native input step using persistent state. The guide supplies x as (B,num_input) and morphology_indices as (B,) when required. Returns (B,1,num_output).",
    "model.BranchELM.forward": "x must be (B,T,config.input_dim). Returns (B,T,2), with one spike logit and one soma target coordinate per step. Synaptic and memory states start at zero for each call.",
    "checkpoint.save_checkpoint": "Writes model kind, serializable configuration, state_dict, and metadata. Creates parent directories. Unsupported model types raise TypeError. Returns None.",
    "checkpoint.load_checkpoint": "Returns (reconstructed torch.nn.Module, metadata dictionary). Supports baseline/branch_elm, official, branch-trace-rnn, axomamba and axomamba-pytorch, axo-temporal variants, axo-block-forecast variants, adaptive P4 variants, and generic Mamba kinds. An unknown kind raises ValueError; PyTorch artifacts are loaded with weights_only=False.",
    "model_family.create_axosim_profile": "profile_id must exist in AXOSIM_MODEL_PROFILES. A Mamba profile returns an AxoMamba or fallback backbone; a GRU profile returns AxoTemporalModel with a GRU core. Weights are newly initialized, not downloaded.",
    "adaptation.CudaGraphAdaptationStep.capture": "module and optimizer parameters must be CUDA-resident; example_inputs and example_targets establish fixed shape/dtype. loss_function(prediction,targets) must return a scalar differentiable tensor. gradient_transform is a zero-argument callable executed after backward. Returns a captured step while restoring pre-capture module/optimizer values.",
    "adaptation.CudaGraphAdaptationStep.__call__": "inputs and targets must match captured shapes and dtypes. Copies values to retained static CUDA buffers, replays the complete update, and returns a detached cloned scalar loss. synchronize=True waits for CUDA completion.",
    "synapse.quantize_synaptic_efficacies": "efficacies is floating-point (N,2*ceil(channels_per_role/recurrent_stride)) with all values positive. Returns a W8 bank containing int8 values, one colocated floating scale, topology metadata, and positive baseline.",
    "synapse.dequantize_synaptic_efficacies": "Returns floating-point (N,K) values reconstructed as bank.values*bank.scale+bank.baseline. Validates the bank's layout and scale device.",
    "population.quantize_neuron_behavior_parameters": "parameters is floating-point (N,adaptation.parameter_count). bits is 4 or 8. W4 requires even logical width and packs two values per byte. Returns physical values and one scale per adaptation component.",
    "population.quantize_mixed_neuron_behavior_parameters": "parameters is floating-point (N,adaptation.parameter_count). component_bits declares W4/W8 for each named adaptation component. Returns packed byte slices and scale metadata needed for reconstruction.",
    "activity.HomeostaticThresholdController.__init__": "Experimental optional feature. group_ids assigns neurons to declared groups; target_rates_hz supplies each group's target. A causal group-rate estimate drives bounded threshold offsets. This interface does not establish biological timescales or biological realism.",
    "activity.HomeostaticThresholdController.observe": "Observes one neuron activity vector for a simulation step; returns whether the update interval triggered an offset update. No future activity is used.",
    "activity.HomeostaticThresholdController.threshold_offsets_per_neuron": "Returns one current group-derived threshold offset per neuron.",
    "data.ShardedNeuronIODataset.__getitem__": "Returns NeuronIOSample with sample_id, inputs (T,C), and targets (T,2).",
    "data.ShardedNeuronIODataset.get_batch": "Returns (inputs,targets) NumPy arrays with shapes (B,T,C) and (B,T,2). Selected shard windows must have compatible lengths for stacking.",
    "data.write_demo_shards": "Creates deterministic synthetic shard files for pipeline checks. The generated targets are not biological reference data. Returns written shard paths.",
    "neuronio_raw.normalize_soma": "Returns normalized soma targets after clipping teacher voltage at threshold and applying (voltage-bias)*scale. The default threshold is -55.0 mV, bias is -67.7 mV, and scale is 0.1.",
    "axobench_iteration.make_checkpoint_predictor": "Returns (predictor,metadata). The predictor accepts native NumPy inputs (B,T,C), optionally with morphology IDs when supported, and returns floating-point NumPy (B,T,2) outputs in AxoBench coordinates. Streaming requires the checkpoint's streaming API. Metadata includes resident parameter count and inference dtype.",
}

FIELD_HELP = {
    "morphology_ids": "Ordered morphology identity vocabulary.",
    "route_features": "Fixed morphology-conditioned route-feature tensor.",
    "input_dim": "Native input-channel count.",
    "route_feature_dim": "Width of aggregated route features.",
    "token_dim": "Width of each encoded P4 token.",
    "state_dim": "Temporal state width.",
    "patch_size": "Native timesteps represented by one block.",
    "output_dim": "Readout-channel count; Lite requires two.",
    "behavior_adaptation": "Enable the learned behavior adaptation bank.",
    "model_dim": "Temporal hidden-feature width.",
    "num_layers": "Number of temporal layers.",
    "num_input": "Input-channel count.",
    "num_output": "Output-channel count.",
    "num_branch": "Branched input-feature count.",
    "num_synapse_per_branch": "Contact slots per branch.",
    "model_kind": "Checkpoint architecture/backend discriminator.",
    "map_location": "PyTorch destination for loaded tensors.",
    "population_size": "Number of persistent neurons.",
    "time_steps": "Native sequence horizon.",
    "batch_size": "Examples processed per batch.",
    "device": "Execution or allocation device.",
    "dtype": "Floating-point execution or allocation dtype.",
    "seed": "Random seed for the declared operation.",
    "warmup_steps": "Warmup updates executed and restored during capture.",
    "gradient_transform": "Optional zero-argument gradient transform after backward.",
    "synchronize": "Wait for CUDA completion before returning.",
    "synaptic_log_efficacy": "Optional (N,K) log-efficacy override.",
    "contact_inputs": "Dense signed contact histories; shape defined above.",
    "metadata": "Caller metadata stored with model state.",
    "optimizer": "Optimizer attached to the selected parameters.",
    "learning_rate": "Optimizer step size.",
    "ignore_start": "Initial native timesteps excluded by the declared path.",
    "bits": "Quantization precision, restricted to the supported bit widths.",
    "baseline": "Positive shared reference efficacy for deviation quantization.",
    "channels_per_role": "Available contact-channel slots for each E/I role.",
    "recurrent_stride": "Stride selecting retained contact slots.",
}

DOC_OVERRIDES = {
    "axomamba.default_axomamba_config": "Build the default AxoSim Mamba recipe and apply keyword overrides.",
    "axomamba.structured_compact_axomamba_config": "Build the structured compact recipe and apply keyword overrides.",
    "axomamba.regression_axomamba_config": "Build the voltage-focused recipe and apply keyword overrides.",
    "axomamba.population_axomamba_config": "Build the population-domain recipe and apply keyword overrides.",
    "axomamba.spike_axomamba_config": "Build the spike-focused recipe and apply keyword overrides.",
    "support_surrogate.AdaptiveSupportP4Surrogate": "Learned support dynamics with compiled neuron adaptation.",
    "axomamba.load_axomamba_config": "Read a JSON architecture configuration and apply keyword overrides; without a path, use the default AxoSim Mamba recipe.",
    "axomamba.coerce_axomamba_config": "Convert a configuration object or mapping to AxoMambaConfig; None selects the default recipe.",
    "axomamba.create_axomamba": "Construct a newly initialized AxoMamba, using the fused backend unless the PyTorch fallback is requested.",
    "mamba_official.BranchOfficialMambaConfig": "Architecture and optional branch, morphology, temporal-correction, and readout settings for the fused Mamba model.",
    "model.BranchELMConfig": "Dimensions and decay constants for the branched recurrent neuron.",
    "checkpoint.save_checkpoint": "Serialize supported model weights, configuration, model kind, and caller metadata.",
    "checkpoint.load_checkpoint": "Reconstruct a supported model and its stored metadata from a trusted checkpoint.",
    "connectome.DelayBucket": "Routing metadata for contacts with one delivery delay.",
    "data.NeuronIOSample": "One identified native input trace and its two-channel target trace.",
    "neuronio_raw.RawNeuronIO": "Parsed raw simulations with separate input-event arrays, spike labels, voltage traces, and metadata.",
    "neuronio_raw.create_neuronio_input_type": "Build an E/I sign vector with positive excitatory channels followed by negative inhibitory channels.",
    "neuronio_raw.normalize_soma": "Clip soma voltage and convert it to the normalized training coordinate.",
    "metrics.soma_rmse": "Compute root-mean-square error from channel 1 of matched prediction and target arrays.",
    "metrics.binary_auc": "Compute rank-based binary ROC AUC with averaged tied ranks; return NaN when either label class is absent.",
    "metrics.spike_auc": "Compute binary ROC AUC from channel 0 of prediction and target arrays.",
    "evaluate.evaluate_dataset": "Evaluate local spike AUC and soma RMSE over dataset batches, with the selected temporal mask and soma coordinate convention.",
    "evaluate.write_metrics": "Write the local metrics dictionary as JSON, creating its parent directory when needed.",
    "train.train_dataset": "Fit the supplied model with spike and soma losses; optionally validate after each epoch and save the best voltage result.",
    "train.train_and_save": "Train the supplied model, save its final weights and configuration, and write training metrics as JSON.",
    "inference_benchmark.count_parameters": "Count all resident model parameter elements, including frozen parameters.",
    "inference_benchmark.write_inference_benchmark": "Write the inference timing report as JSON, creating the parent directory when needed.",
    "inference_benchmark.parse_int_list": "Parse a comma-separated integer list, ignoring empty entries and rejecting an empty result.",
    "setup_workflow.DatasetSpec": "Kaggle dataset identity and its local directory name.",
    "setup_workflow.SetupOptions": "Installation, download, conversion, and path choices used to construct a setup plan.",
    "setup_workflow.SetupStep": "One directory-creation or subprocess step with a reader-facing description.",
    "setup_workflow.SetupPlan": "Ordered setup operations and follow-up commands.",
    "setup_workflow.build_setup_plan": "Construct the setup operations without executing installations, downloads, or conversions.",
    "setup_workflow.run_setup_plan": "Print and execute each planned operation; dry_run prints the same plan without filesystem or subprocess changes.",
}

FIELD_HELP.update({
    "config": "Model configuration; use the defaults and constraints documented for its configuration class.",
    "base_config": "Common backbone configuration whose capacity fields are replaced by the selected profile.",
    "profile_id": "Exact key in AXOSIM_MODEL_PROFILES, such as axosim-gru-small.",
    "use_pytorch_fallback": "Construct the CPU/test-compatible backend. Its checkpoint format differs from the fused backend.",
    "neuron": "Shared Lite neuron used by every persistent population member.",
    "morphology_indices": "Integer class assignments into the model's ordered morphology vocabulary; one per batch item or persistent neuron.",
    "contact_branch_indices": "Integer tensor (population, contacts), mapping each contact to a Lite input channel.",
    "behavior": "Enable gradients on per-neuron behavior rows.",
    "morphology": "Enable gradients on morphology-shared adaptation rows.",
    "synaptic": "Enable gradients on independently mutable contact log efficacies.",
    "event_summary_indices": "Flattened population-time addresses n*time_steps+t, in corresponding event order.",
    "event_contact_indices": "Flattened population-contact addresses n*contacts+k; paired addresses must name the same neuron.",
    "event_values": "Signed floating-point event amplitudes, one per paired address.",
    "runtime_coefficients": "Direct deployed adaptation coefficients, with shape (batch, cache_width).",
    "behavior_parameters": "Logical behavior coefficients to compile into the model's deployed coefficient width.",
    "adaptation_cache": "Compiled behavior coefficients; use the declared cache width for the neuron model.",
    "loss_function": "Callable receiving predictions and targets and returning a differentiable scalar loss.",
    "example_inputs": "CUDA tensor establishing the input shape, dtype, and static buffer for capture.",
    "example_targets": "CUDA tensor establishing the target shape, dtype, and static buffer for capture.",
    "module": "Module whose forward execution participates in the captured update.",
    "path": "Filesystem location to read or write; see the operation's persistence contract.",
    "checkpoint_path": "Trusted model-weight file to reconstruct or evaluate.",
    "root": "Dataset shard directory or manifest root.",
    "dataset": "Trace dataset supporting the batching contract used by this operation.",
    "validation_dataset": "Development data for choosing trained states and calibration.",
    "indices": "Requested dataset sample indices.",
    "index": "Index of one dataset sample.",
    "cache_shards": "Maximum cached shards; zero disables the cache.",
    "shuffle": "Enable deterministic reordering controlled by seed and shuffle_mode.",
    "shuffle_mode": "Choose sample-level or shard-level reordering.",
    "window_size": "Native timesteps per extracted window.",
    "window_stride": "Native timestep distance between successive window starts.",
    "start_offset": "Native timestep index before the first selected window.",
    "samples_per_epoch": "Number of training window presentations requested per epoch.",
    "epochs": "Number of passes over the declared epoch sampling budget.",
    "burn_in": "Initial timesteps excluded from training losses.",
    "optimizer_name": "Optimizer selection supported by this training path.",
    "weight_decay": "Optimizer regularization coefficient.",
    "grad_clip_norm": "Maximum gradient norm when clipping is enabled.",
    "spike_loss_weight": "Multiplier applied to the spike training loss.",
    "soma_loss_weight": "Multiplier applied to the soma training loss.",
    "lr_schedule": "Learning-rate schedule selection.",
    "lr_schedule_steps": "Number of optimizer steps used to parameterize the schedule.",
    "soma_units": "Coordinate convention used when computing the local soma metric.",
    "bank": "Quantized bank including its scale and layout metadata.",
    "efficacies": "Positive floating-point contact multipliers, shaped by the retained topology.",
    "parameters": "Floating-point adaptation rows before quantization.",
    "component_bits": "Mapping from adaptation component names to supported W4/W8 storage widths.",
    "adaptation": "Descriptor defining named behavior components and their logical shapes.",
    "scales": "Floating-point reconstruction scales for the stored quantized values.",
    "values": "Physical quantized values, interpreted using the bank's scale and layout metadata.",
    "group_ids": "Integer population vector whose contiguous groups cover the target-rate vector.",
    "target_rates_hz": "Positive finite firing-rate targets in hertz, one per declared group.",
    "dt_ms": "Native simulation step in milliseconds.",
    "update_interval_ms": "Interval between controller updates; an integer multiple of dt_ms.",
    "time_constant_ms": "Time constant of the controller's smoothed rate estimate.",
    "max_abs_offset": "Bound on the absolute threshold correction.",
    "activity": "Boolean neuron activity vector for one simulation step.",
    "plan": "Ordered setup steps and next-step instructions to execute or inspect.",
    "dry_run": "Print the plan without creating directories or executing subprocesses.",
    "options": "Setup flags and resolved local paths used to construct the plan.",
    "runs": "Measured repetitions after the declared warmup.",
    "warmup_runs": "Unmeasured iterations before the timing repetitions.",
    "precision": "Floating-point execution precision.",
    "batch_sizes": "Batch sizes included in the benchmark matrix.",
    "compile_model": "Enable the benchmark's compilation path.",
    "streaming": "Use the checkpoint's explicit streaming-state interface.",
    "streaming_chunk_size": "Chunk size passed to a supported streaming backend.",
    "family": "Temporal model family selected by the named profile.",
    "public_name": "Reader-facing name associated with the exact profile ID.",
    "head_dim": "Configured head width of the backbone.",
    "residual_scale_init": "Initial learned multiplier on the residual update.",
    "mamba_update_normalization": "Normalize residual updates when the supported fixed_rms mode is selected.",
    "forecast_config": "Block forecasting configuration, including core and cadence.",
    "temporal_config": "Temporal-core selection and its recurrence/adaptation settings.",
    "model": "Model to execute, optimize, count, or serialize for this operation.",
    "overrides": "Keyword fields that replace values in the selected architecture recipe.",
    "x": "Input tensor for the full-sequence or streaming operation.",
    "inputs": "Native input traces or the input tensor supplied to this operation.",
    "targets": "Reference spike and soma target traces.",
    "prediction": "Predicted arrays with spike values in channel 0 and soma values in channel 1.",
    "target": "Reference arrays matching the prediction's shape and coordinate convention.",
    "scores": "Continuous scores; larger values indicate greater evidence for a positive label.",
    "labels": "Binary reference labels, classified as positive above 0.5.",
    "state": "Temporal state returned by the matching initial-state or allocation method.",
    "hidden": "Hidden recurrent state for the selected temporal core.",
    "token": "One encoded P4 token.",
    "tokens": "Sequence of encoded P4 tokens.",
    "summaries": "Morphology-routed input-feature summaries.",
    "feature_patch": "Four native timesteps of routed features to encode as one token.",
    "block_state": "Persistent state of the block-forecast recurrence.",
    "chunk_size": "Chunk length for the supported Mamba or streaming execution path.",
    "mamba_classes": "Optional backend class pair used when constructing the Mamba implementation.",
    "state_dict": "Stored parameter and buffer mapping to load.",
    "output_buffer": "Optional preallocated output tensor for the operation.",
    "retain_base_soma_prediction": "Keep the base soma readout available for inspection.",
    "width": "Feature width of the behavior adapter or population recurrence.",
    "branches": "Number of routed branch features in the adapter.",
    "outputs": "Number of readout channels.",
    "rank": "Low-rank adapter factor width.",
    "branch_token_offset": "Include adaptation offsets for encoded branch tokens.",
    "morphology_index": "Index of the morphology row to select.",
    "hidden_units": "Width of the hidden feature layer.",
    "memory_units": "Width of the recurrent memory state.",
    "num_branches": "Number of branched input features.",
    "synapse_decay": "Decay coefficient of the synaptic trace.",
    "memory_decay": "Decay coefficient of recurrent memory.",
    "weight_ih_delta": "Optional correction to GRU input-to-hidden weights.",
    "weight_hh_delta": "Optional correction to GRU hidden-to-hidden weights.",
    "adapter_mask": "Mask selecting members that receive the adapter correction.",
    "core": "Temporal core instance used by the wrapper.",
    "temporal_kwargs": "Keyword options forwarded to temporal-core construction.",
    "population_embedding_adapters": "Population-group embedding corrections for the backbone.",
    "branch_inputs": "Current population branch-feature tensor.",
    "population": "Number of neurons represented by the population runner or record.",
    "measurement": "Measured deployment record to compare with the target requirements.",
    "byte_count": "Storage count in bytes.",
    "adapter": "Behavior adapter whose named components define the population bank.",
    "groups": "Population parameter-group count.",
    "group": "Index of the population parameter group to load.",
    "compile_step": "Compile the population step implementation.",
    "compile_mode": "Mode passed to torch.compile for the selected step.",
    "pin_memory": "Stage CPU arrays in pinned memory before a CUDA transfer.",
    "non_blocking": "Request asynchronous tensor transfers where supported.",
    "sequence_length": "Native timestep count of a trace.",
    "cache_full_shards": "Retain complete shard arrays rather than only selected data.",
    "shard_idx": "Index of the shard in the dataset manifest.",
    "name": "Name of the optional shard array or declared record.",
    "stride": "Distance between selected positions in the relevant sequence.",
    "shard_reuse_batches": "Number of consecutive batches sampled before advancing to another shard.",
    "file_load_fraction": "Fraction of each shard made available to the sampling path.",
    "source_simulations": "Number of source simulations included by the dataset declaration.",
    "shard_count": "Number of synthetic shard files to write.",
    "samples_per_shard": "Synthetic sample count in each generated shard.",
    "input_root": "Directory containing the source dataset shards.",
    "output_root": "Directory receiving converted dataset shards.",
    "input_dtype": "Stored NumPy dtype of the converted input arrays.",
    "input_path": "Raw NeuronIO pickle file or directory to discover and convert.",
    "output_dir": "Directory receiving converted shards and their manifest.",
    "shard_size": "Maximum sample count in each converted shard.",
    "y_soma_threshold": "Upper voltage clipping threshold in millivolts.",
    "y_train_soma_bias": "Voltage bias subtracted before target scaling, in millivolts.",
    "y_train_soma_scale": "Scale converting the biased voltage to the training target coordinate.",
    "soma": "Raw soma voltage array in millivolts.",
    "bias": "Voltage bias subtracted before normalization.",
    "scale": "Multiplicative normalization or reconstruction scale.",
    "mask_mode": "Initial-timestep exclusion or official overlap-stitching mask.",
    "stitch_burn_in": "Native overlap timesteps excluded from subsequent stitched windows.",
    "soma_affine_calibration": "Rescale predictions to the evaluation targets' mean and standard deviation; declare this calibration when comparing metrics.",
    "validation_batch_size": "Validation batch size; None uses the training batch size.",
    "best_checkpoint_path": "Destination for the state with the lowest validation soma RMSE.",
    "validation_soma_units": "Soma coordinate convention for validation RMSE.",
    "validation_metric_ignore_start": "Initial native timesteps excluded from validation metrics.",
    "validation_metric_mask_mode": "Temporal masking policy used for validation metrics.",
    "validation_metric_stitch_burn_in": "Overlap exclusion for stitched validation traces.",
    "validation_soma_affine_calibration": "Apply target-statistic affine calibration to validation soma predictions.",
    "max_train_batches": "Optional cap on batches in each training epoch.",
    "l1_lambda": "Coefficient of the L1 penalty on model parameters.",
    "sparse_soma_loss_weight": "Coefficient of auxiliary soma MSE over teacher-defined high-importance timesteps.",
    "sparse_soma_high_voltage_quantile": "Teacher-voltage quantile used to select high-voltage timesteps.",
    "sparse_soma_high_dvdt_quantile": "Absolute teacher-voltage difference quantile used to select rapidly changing timesteps.",
    "sparse_soma_input_event_quantile": "Positive input-activity quantile used to select event-adjacent timesteps.",
    "sparse_soma_spike_window": "Symmetric native-timestep radius around reference spikes in the auxiliary mask.",
    "sparse_soma_post_event_window": "Causal native-timestep window after selected input events.",
    "sera_soma_loss_weight": "Coefficient of the relevance-weighted auxiliary soma loss.",
    "sera_soma_min_weight": "Minimum timestep weight in the relevance-weighted soma loss.",
    "sera_soma_relevance_power": "Exponent applied to the teacher-derived relevance weights.",
    "soma_slope_loss_weight": "Coefficient of squared error in adjacent-timestep soma differences.",
    "update_log_interval": "Optimizer-step interval between update-log records; zero disables logging.",
    "update_log_path": "Destination for per-update JSON log records.",
    "prefetch_batches": "Number of dataset batches prepared ahead of consumption.",
    "metrics": "Metrics dictionary to serialize.",
    "metrics_path": "Destination for training metrics JSON.",
    "accuracy_metrics_path": "Optional metrics JSON included with the inference timing report.",
    "report": "Inference benchmark report to serialize.",
    "value": "Comma-separated string of integer values.",
    "config_path": "Architecture JSON used to reconstruct the upstream baseline.",
    "checkpoint": "Upstream baseline checkpoint file.",
    "project_root": "Source checkout containing the package to install and local run directories.",
    "data_dir": "Root of the raw-data and shard directories.",
    "install_kaggle": "Include installation of downloader dependencies in the plan.",
    "download_data": "Include explicit dataset downloads in the plan.",
    "convert_raw": "Include raw NeuronIO conversion in the plan.",
    "raw_dir": "Optional raw-data directory overriding data_dir/raw.",
    "shard_dir": "Optional converted-data directory overriding data_dir/shards.",
    "skip_install": "Omit editable package installation from the plan.",
    "datasets": "Kaggle dataset identities to download when download_data is enabled.",
    "python_executable": "Interpreter used for planned installation, download, and conversion commands.",
    "slug": "Kaggle owner/dataset identifier.",
    "description": "Reader-facing description of the setup operation.",
    "command": "Shell-quoted display of the planned subprocess arguments.",
    "argv": "Argument tuple passed directly to the planned subprocess.",
    "mkdir": "Directory created by this step, when provided.",
    "steps": "Ordered setup operations.",
    "next_steps": "Follow-up instructions printed after the plan.",
})

PARAM_HELP = {
    "data.NeuronIOSample": {
        "sample_id": "Persistent trace identity from the shard's sample_ids array.",
        "inputs": "One native input trace, shaped (time,input_channels).",
        "targets": "One spike/soma target trace, shaped (time,2).",
    },
    "neuronio_raw.RawNeuronIO": {
        "inputs": "Raw input events (simulations,time,2*segments), with excitatory channels followed by inhibitory channels before the converter applies E/I signs.",
        "spikes": "Binary output spike labels (simulations,time).",
        "soma": "Raw soma voltage in millivolts, shaped (simulations,time).",
        "metadata": "Simulation counts, duration, synapse count, segment types, and available segment-to-soma distances extracted from the raw file.",
    },
    "neuronio_raw.normalize_soma": {
        "threshold": "Upper clipping threshold in millivolts.",
        "bias": "Millivolt bias subtracted after clipping.",
        "scale": "Multiplier converting biased millivolt values to the training coordinate.",
    },
    "setup_workflow.DatasetSpec": {
        "name": "Local dataset subdirectory and archive name.",
        "slug": "Kaggle owner/dataset identifier passed to the downloader.",
    },
    "adaptation.CudaGraphAdaptationStep.__call__": {
        "inputs": "New input values with exactly the captured shape, dtype, and CUDA device.",
        "targets": "New target values with exactly the captured shape, dtype, and CUDA device.",
    },
    "metrics.soma_rmse": {
        "prediction": "Prediction array with a final channel axis; channel 1 contains soma values.",
        "target": "Matched reference array in the same soma coordinate as prediction.",
    },
    "metrics.spike_auc": {
        "prediction": "Prediction array whose channel 0 contains continuous spike scores.",
        "target": "Matched reference array whose channel 0 contains spike labels.",
    },
}

METHOD_ROLES = {
    "forward": "Predict native spike and soma outputs for the supplied sequence.",
    "forward_batch": "Run independent trials through the same persistent neurons and adaptation banks.",
    "forward_tokens": "Decode pre-encoded four-step tokens through the population recurrence.",
    "forward_token_batch": "Decode independent token batches with shared population parameters.",
    "enable_full_training": "Enable gradients on shared neuron weights and all adaptation parameters.",
    "synaptic_efficacies": "Materialize positive contact multipliers from their log parameters.",
    "parameter_count": "Return the count of trainable parameters.",
    "parameter_counts": "Return parameter counts for the declared components.",
    "reset_parameters": "Initialize the model's learned parameters.",
    "aggregate_inputs": "Project input histories through morphology-conditioned route features.",
    "compile_adaptation": "Project logical behavior rows into deployed runtime coefficients.",
    "initial_state": "Allocate the initial temporal state.",
    "step_token": "Advance the support recurrence and decode one four-step forecast.",
    "step_p4": "Encode a four-step feature patch and advance the support recurrence.",
    "allocate_streaming_state": "Allocate persistent state for an independent stream.",
    "streaming_step": "Advance one native input timestep using persistent state.",
    "streaming_step_events": "Advance persistent state from sparse input events.",
    "recurrent_state_bytes": "Report the declared recurrent-state storage in bytes.",
    "component_manifest": "Describe the model's temporal and readout components.",
    "recurrent_state_elements": "Report the recurrent-state element count.",
    "temporal_correction": "Compute the temporal correction for encoded features.",
    "clear_and_route": "Deliver active-source events and clear the consumed routing slot.",
    "clear_recorded_branches": "Clear the recorded branch values used by the router.",
    "step": "Advance the population runner by one declared simulation step.",
    "load_group_recurrent_parameters": "Load recurrent parameters for the declared population groups.",
    "get_batch": "Read the requested input and target arrays as a batch.",
    "get_sample_ids": "Return the sample identities associated with the selected indices.",
    "get_optional_array_batch": "Read an optional per-sample shard array when it is available.",
    "get_shard_sequence_length": "Read a shard's native time dimension without materializing its inputs.",
    "reshuffle": "Reorder the enabled sampling index using the supplied seed.",
    "__getitem__": "Read one sample and its input/target contract.",
    "__len__": "Return the number of indexed samples.",
    "__call__": "Replay the captured adaptation update with new input and target values.",
    "evaluate": "Compare a deployment measurement with the declared target requirements.",
    "validation_errors": "Return violated deployment requirements for the supplied measurement.",
    "bytes_to_gib": "Convert a byte count to gibibytes using 1024 cubed bytes per GiB.",
}

PROPERTY_HELP = {
    "population_size": "Number of persistent neurons.",
    "runtime_coefficients_per_neuron": "Width of the direct behavior coefficients for one neuron.",
    "synaptic_efficacies_per_neuron": "Number of independently mutable incoming contacts per neuron.",
    "storage_bytes": "Physical bank storage, including quantized values and reconstruction scales.",
    "queue_bytes": "Physical storage allocated to the delayed event queue.",
    "num_input": "Native input-channel count.",
    "num_output": "Readout-channel count.",
    "num_branch": "Branched input-feature count.",
    "config": "Configuration retained by the model or its shared backbone.",
    "base_soma_prediction": "Most recently retained base soma prediction, when available.",
    "patch_size": "Native timesteps represented by one forecast block.",
    "gate_feature_dim": "Width of the concatenated token and state gate features.",
    "values_per_neuron": "Logical retained-contact multiplier count per neuron.",
    "runtime_coefficient_slices": "Named packed slices of the direct deployed adaptation coefficients.",
}

API_EXAMPLES = {
    "interfaces.AxoSimPopulation": ("Run independent trials through one persistent population.", "import torch\nfrom population_example import build_population\n\npopulation = build_population()\nprediction = population.forward_batch(torch.zeros(2, 3, 12, 4))\nprint(prediction.shape)", "torch.Size([2, 3, 12, 2])"),
    "model_family.create_axosim_profile": ("Construct an untrained, CPU-compatible GRU profile for an interface check.", "from axosim import create_axosim_profile\n\nmodel = create_axosim_profile(\n    'axosim-gru-small', use_pytorch_fallback=True\n)\nprint(type(model).__name__)", "AxoTemporalModel"),
    "synapse.quantize_synaptic_efficacies": ("Quantize a unit-efficacy bank with four retained slots per E/I role.", "import torch\nfrom axosim.synapse import quantize_synaptic_efficacies\n\nbank = quantize_synaptic_efficacies(\n    torch.ones(2, 8), channels_per_role=4, recurrent_stride=1\n)\nprint(bank.values.shape, bank.values.dtype)", "torch.Size([2, 8]) torch.int8"),
    "data.write_demo_shards": ("Create synthetic shards to verify the reader contract before using biological data.", "from tempfile import TemporaryDirectory\nfrom axosim.data import ShardedNeuronIODataset, write_demo_shards\n\nwith TemporaryDirectory() as directory:\n    write_demo_shards(directory, samples_per_shard=2, time_steps=12, input_dim=6)\n    inputs, targets = ShardedNeuronIODataset(directory).get_batch([0, 1])\n    print(inputs.shape, targets.shape)", "(2, 12, 6) (2, 12, 2)"),
}

RETURN_HELP = {
    "checkpoint.load_checkpoint": [("model", "torch.nn.Module", "Reconstructed model with its stored weights, architecture configuration, and backend."), ("metadata", "dict[str, Any]", "Metadata stored with the checkpoint; an empty dictionary when absent.")],
    "model_family.create_axosim_profile": [("model", "nn.Module", "Newly initialized Mamba backbone or GRU AxoTemporalModel for the requested profile; no weights are downloaded.")],
    "adaptation.CudaGraphAdaptationStep.capture": [("step", "CudaGraphAdaptationStep", "Captured update with retained static buffers; warmup/capture changes to stored module and optimizer values have been restored.")],
    "adaptation.CudaGraphAdaptationStep.__call__": [("loss", "torch.Tensor", "Detached cloned scalar loss from the replayed optimizer update.")],
    "synapse.quantize_synaptic_efficacies": [("bank", "QuantizedSynapticEfficacyBank", "W8 values, one shared scale, positive baseline, and retained topology metadata.")],
    "synapse.dequantize_synaptic_efficacies": [("efficacies", "torch.Tensor", "Reconstructed floating-point contact multipliers with shape (population, retained_contacts).")],
    "data.write_demo_shards": [("paths", "list[Path]", "Written synthetic shard paths. These shards exercise the reader and trainer contracts.")],
    "axobench_iteration.make_checkpoint_predictor": [("predict", "Callable[[np.ndarray], np.ndarray]", "Prediction function mapping native inputs (B,T,C) to spike logits and normalized soma targets (B,T,2)."), ("metadata", "dict[str, Any]", "Stored checkpoint metadata plus parameter counts, inference dtype, and streaming configuration.")],
    "axobench_iteration.make_official_elm_predictor": [("predict", "Callable[[np.ndarray], np.ndarray]", "Upstream Branch-ELM predictor on the shared AxoBench target-coordinate contract."), ("metadata", "dict[str, Any]", "Configuration, checkpoint identity, parameter counts, dtype, and output conventions.")],
    "axomamba.load_axomamba_config": [("config", "AxoMambaConfig", "Configuration loaded from JSON with the requested overrides, or the default recipe when path is None.")],
    "axomamba.coerce_axomamba_config": [("config", "AxoMambaConfig", "Converted configuration; an existing AxoMambaConfig is returned unchanged.")],
    "axomamba.create_axomamba": [("model", "AxoMamba", "Newly initialized AxoMamba or AxoPyTorchMamba, according to use_pytorch_fallback.")],
    "interfaces.AxoSimPopulation.synaptic_efficacies": [("efficacies", "torch.Tensor", "Positive multipliers exp(synaptic_log_efficacy), shaped (population, contacts).")],
    "support_surrogate.AdaptiveSupportP4Surrogate.initial_state": [("state", "torch.Tensor", "Zero tensor (batch_size,state_dim) on the selected device and dtype.")],
    "support_surrogate.AdaptiveSupportP4Surrogate.aggregate_inputs": [("summaries", "torch.Tensor", "Morphology-routed features (batch,time,route_feature_dim).")],
    "support_surrogate.AdaptiveSupportP4Surrogate.compile_adaptation": [("coefficients", "torch.Tensor", "Compiled adaptation coefficients (batch,cache_width).")],
    "support_surrogate.AdaptiveSupportP4Surrogate.step_token": [("forecast", "torch.Tensor", "Decoded next-block prediction (batch,4,2)."), ("state", "torch.Tensor", "Updated recurrent state (batch,state_dim).")],
    "support_surrogate.AdaptiveSupportP4Surrogate.step_p4": [("forecast", "torch.Tensor", "Decoded next-block prediction (batch,4,2)."), ("state", "torch.Tensor", "Updated recurrent state (batch,state_dim).")],
    "support_surrogate.AdaptiveSupportP4Surrogate.forward_with_gate_features": [("prediction", "torch.Tensor", "Native output trace (batch,time,2)."), ("gate_features", "torch.Tensor", "Causally shifted token/state features (batch,floor(time/4),token_dim+state_dim), with a zero first block.")],
    "mamba_official.BranchOfficialMamba.allocate_streaming_state": [("state", "BranchMambaStreamingState", "Fresh recurrent buffers and local-filter histories for the selected batch, device, and dtype.")],
    "mamba_official.BranchOfficialMamba.streaming_step": [("prediction", "torch.Tensor", "One native output step (batch,1,num_output); the supplied state is updated in place.")],
    "temporal_core.AxoTemporalModel.allocate_streaming_state": [("state", "AxoTemporalStreamingState", "Fresh temporal-core buffers and local-filter histories for the selected batch, device, and dtype.")],
    "temporal_core.AxoTemporalModel.streaming_step": [("prediction", "torch.Tensor", "One native output step (batch,1,num_output); the supplied state is updated in place.")],
    "population.dequantize_neuron_behavior_parameters": [("parameters", "torch.Tensor", "Floating-point behavior rows (population,adaptation.parameter_count), reconstructed component by component.")],
    "population.dequantize_mixed_neuron_behavior_parameters": [("parameters", "torch.Tensor", "Floating-point behavior rows (population,adaptation.parameter_count), reconstructed from each component's W4/W8 slice.")],
    "activity.HomeostaticThresholdController.observe": [("updated", "bool", "True when the update interval triggers a threshold-offset update, otherwise False.")],
    "activity.HomeostaticThresholdController.threshold_offsets_per_neuron": [("offsets", "torch.Tensor", "Current group-derived threshold offsets, one per population member.")],
    "neuronio_raw.normalize_soma": [("normalized", "np.ndarray", "Float32 array matching soma.shape, equal to (minimum(soma,threshold)-bias)*scale.")],
    "neuronio_raw.create_neuronio_input_type": [("signs", "np.ndarray", "Float32 vector (num_input,) with +1 in its first half and -1 in its second half; num_input must be even.")],
    "metrics.soma_rmse": [("rmse", "float", "Root-mean-square error in the supplied soma target coordinate, aggregated over channel 1.")],
    "metrics.binary_auc": [("auc", "float", "ROC AUC over all flattened entries, or NaN when labels contain only one class.")],
    "metrics.spike_auc": [("auc", "float", "ROC AUC over channel 0, or NaN when reference labels contain only one class.")],
    "evaluate.evaluate_dataset": [("metrics", "dict[str, float | int]", "Sample count, temporal-mask and calibration settings, elapsed time, throughput, soma RMSE and units, spike AUC, and related local spike metrics.")],
    "train.train_dataset": [("metrics", "dict[str, Any]", "Epoch history, final training loss and timing, optimizer/loss settings, and optional validation and best-state metrics. The supplied model retains its final trained weights.")],
    "train.train_and_save": [("metrics", "dict[str, Any]", "The training metrics returned by train_dataset; the requested checkpoint and metrics JSON are also written.")],
    "inference_benchmark.count_parameters": [("count", "int", "Sum of numel() over every model parameter, independent of requires_grad.")],
    "inference_benchmark.benchmark_inference_matrix": [("report", "dict[str, Any]", "Timing rows for each batch/horizon pair, device/precision and repetition settings, resident parameter count, optional accuracy metadata, and the fastest successful row. Out-of-memory rows contain error details.")],
    "inference_benchmark.parse_int_list": [("values", "list[int]", "Parsed integers in their original order.")],
    "setup_workflow.build_setup_plan": [("plan", "SetupPlan", "Ordered directory-creation and subprocess steps plus follow-up instructions; no steps have run.")],
}

for _recipe in ("default", "structured_compact", "regression", "population", "spike"):
    RETURN_HELP[f"axomamba.{_recipe}_axomamba_config"] = [("config", "AxoMambaConfig", "Architecture recipe with the supplied keyword overrides applied.")]


def expression(node):
    return ast.unparse(node) if node is not None else None


DEFAULT_CONSTANTS = {}


def param_records(node, known=None):
    args = node.args
    positional = args.posonlyargs + args.args
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    records = []
    for p, default in zip(positional, defaults):
        if p.arg in {"self", "cls"}:
            continue
        records.append({"name": p.arg, "type": expression(p.annotation), "default": expression(default), "kind": "positional_only" if p in args.posonlyargs else "positional_or_keyword"})
    if args.vararg:
        records.append({"name": args.vararg.arg, "type": expression(args.vararg.annotation), "default": None, "kind": "variadic_positional"})
    for p, default in zip(args.kwonlyargs, args.kw_defaults):
        records.append({"name": p.arg, "type": expression(p.annotation), "default": expression(default), "kind": "keyword_only"})
    if args.kwarg:
        records.append({"name": args.kwarg.arg, "type": expression(args.kwarg.annotation), "default": None, "kind": "variadic_keyword"})
    if known:
        for record in records:
            if record["default"] is not None:
                try:
                    record["resolved_default"] = literal_value(ast.parse(record["default"], mode="eval").body, known)
                except (ValueError, TypeError, SyntaxError):
                    pass
    return records


def signature(node):
    # Unparse the original argument AST to preserve /, *, annotations/defaults.
    value = f"{node.name}({ast.unparse(node.args)})"
    return value + (f" -> {ast.unparse(node.returns)}" if node.returns else "")


def fields(node):
    result = []
    for value in node.body:
        if isinstance(value, ast.AnnAssign) and isinstance(value.target, ast.Name):
            result.append({"name": value.target.id, "type": expression(value.annotation), "default": expression(value.value)})
    return result


def public_node(node):
    return not node.name.startswith("_") or node.name in {"__init__", "__call__", "__getitem__", "__len__"}


def code(value):
    return "`" + str(value).replace("|", "\\|").replace("`", "'") + "`"


def paragraph(value):
    # Source docstrings may contain internal history; retain definitions only.
    return value.strip().split("\n\n")[0].replace("\n", " ") if value else ""


def source_link(repository, commit, module, node):
    return f"{repository}/blob/{commit}/src/axosim/{module}.py#L{node.lineno}-L{node.end_lineno}"


def table(records):
    lines = ["| Parameter | Type | Default |", "| --- | --- | --- |"]
    for item in records:
        default = item["default"]
        if item.get("kind", "").startswith("variadic"):
            default = "variadic"
        shown_default = code(default) if default is not None else 'required'
        if "resolved_default" in item and repr(item["resolved_default"]) != default:
            shown_default += " = " + code(repr(item["resolved_default"]))
        lines.append(f"| {code(item['name'])} | {code(item['type'] or 'unspecified')} | {shown_default} |")
    return lines


def object_anchor(module, owner, name=""):
    return (module+"-"+owner+("-"+name if name else "")).replace("_", "-").lower()


def bound_signature(module, node, owner=None):
    args = deepcopy(node.args)
    if args.posonlyargs and args.posonlyargs[0].arg in {"self", "cls"}:
        args.posonlyargs.pop(0)
    elif args.args and args.args[0].arg in {"self", "cls"}:
        args.args.pop(0)
    qualifier = f"axosim.{module}.{owner+'.' if owner else ''}{node.name}"
    result = qualifier+"("+ast.unparse(args)+")"
    return result+(" -> "+expression(node.returns) if node.returns else "")


def signature_block(value, source, decorators=()):
    lines = ['<div class="api-signature">', "", "```python"]
    lines.extend("@"+d for d in decorators if d in {"classmethod", "staticmethod"})
    lines.extend([value, "```", "", f"[Source]({source})", "", "</div>", ""])
    return lines


def parameter_definition_list(records, label="Parameters", css="api-parameters", context=None):
    if not records:
        return []
    lines = [f'<p class="api-label">{label}</p>', "", f'<dl class="{css}">']
    for parameter in records:
        name = parameter["name"]
        typename = parameter.get("type") or "unannotated"
        default = parameter.get("default")
        qualifiers = []
        if parameter.get("kind") == "keyword_only":
            qualifiers.append("keyword-only")
        if parameter.get("kind", "").startswith("variadic"):
            qualifiers.append("variadic")
        elif default is None:
            qualifiers.append("required")
        else:
            shown = repr(parameter["resolved_default"]) if "resolved_default" in parameter else default
            qualifiers.append("default="+shown)
        lines.append(f'<dt><code>{escape(name)}</code> <span class="api-type">{escape(typename)}</span></dt>')
        description = PARAM_HELP.get(context, {}).get(name, FIELD_HELP.get(name))
        declaration = escape(", ".join(qualifiers))
        lines.append(f'<dd><span class="api-default">{declaration}.</span>'+ (" "+escape(description) if description else "")+"</dd>")
    lines.extend(["</dl>", ""])
    return lines


def example_document(full):
    if full not in API_EXAMPLES:
        return []
    purpose, snippet, output = API_EXAMPLES[full]
    lines = ['<p class="api-label">Examples</p>', "", purpose, ""]
    if "population_example" in snippet:
        lines.extend(["Download [population_example.py](/examples/population_example.py) into your working directory first; [build populations](/populations/) explains its construction.", ""])
    lines.extend(["```python", snippet, "```", "", "```text", output, "```", ""])
    return lines


def callable_doc(module, node, repository, commit, owner=None, level=2):
    full = f"{module}.{owner+'.' if owner else ''}{node.name}"
    display = f"{owner+'.' if owner else ''}{node.name}"
    decorators = [expression(d) for d in node.decorator_list]
    css = "api-method" if owner else "api-symbol"
    anchor = object_anchor(module, owner or node.name, node.name if owner else "")
    lines = [f'<section class="{css}" id="{anchor}">', "", "#"*level+" "+display, ""]
    lines.extend(signature_block(bound_signature(module, node, owner), source_link(repository, commit, module, node), decorators))
    role = DOC_OVERRIDES.get(full, paragraph(ast.get_docstring(node))) or METHOD_ROLES.get(node.name)
    if role:
        lines.extend([role, ""])
    if full in CONTRACTS:
        lines.extend([CONTRACTS[full], ""])
    params = param_records(node, DEFAULT_CONSTANTS.get(module))
    lines.extend(parameter_definition_list(params, context=full))
    if node.returns:
        typename = expression(node.returns)
        returns = RETURN_HELP.get(full)
        if returns is None and node.name == "get_batch":
            returns = [("inputs", "np.ndarray", "Native inputs with shape (batch,time,input_channels)."), ("targets", "np.ndarray", "Spike and soma targets with shape (batch,time,2).")]
        if returns is None and node.name in {"forward", "forward_batch", "forward_sparse_contacts", "forward_tokens", "forward_token_batch"} and full in CONTRACTS:
            returns = [("prediction", typename, "Spike-logit and soma-target channels in the tensor shape specified above.")]
        if returns is None:
            description = "No return value." if typename == "None" else "Iterator over the declared parameter group." if "Iterator[" in typename else ""
            returns = [("result", typename, description)] if description else []
        lines.extend(['<p class="api-label">Returns</p>', ""])
        if returns:
            lines.append('<dl class="api-parameters">')
            for name, result_type, description in returns:
                lines.append(f"<dt><code>{escape(name)}</code> <span class=\"api-type\">{escape(result_type)}</span></dt>")
                lines.append(f"<dd>{escape(description)}</dd>")
            lines.extend(["</dl>", ""])
        else:
            lines.extend([code(typename), ""])
    lines.extend(example_document(full))
    lines.extend(["</section>", ""])
    return lines


def class_document(module, node, item, repository, commit):
    full = module+"."+node.name
    qualifier = "axosim."+full
    constructor = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == "__init__"), None)
    signature_value = qualifier + item["signature"][len(node.name):]
    if constructor is not None:
        signature_value = bound_signature(module, constructor).replace(".__init__(", "."+node.name+"(").removesuffix(" -> None")
    else:
        signature_value = signature_value.removesuffix(" -> None")
    lines = [f'<section class="api-symbol" id="{object_anchor(module, node.name)}">', "", "## "+node.name, ""]
    lines.extend(signature_block(signature_value, source_link(repository, commit, module, node)))
    role = DOC_OVERRIDES.get(full, paragraph(ast.get_docstring(node)))
    if role:
        lines.extend([role, ""])
    if item["bases"]:
        lines.extend(["Bases: "+", ".join(code(base) for base in item["bases"])+".", ""])
    if full+".__init__" in CONTRACTS:
        lines.extend([CONTRACTS[full+".__init__"], ""])
    if full == "axomamba.AxoMambaConfig":
        lines.extend(["Inherits all fields and raw defaults from `BranchOfficialMambaConfig`. `default_axomamba_config` applies the AxoSim recipe over those raw defaults.", ""])
    if full in {"axomamba.AxoMamba", "axomamba.AxoPyTorchMamba"}:
        lines.extend(["Full-sequence and streaming methods are inherited from `BranchOfficialMamba` below. Preserve the recorded fused/fallback backend when loading weights.", ""])
    lines.extend(parameter_definition_list(item["parameters"], context=full))
    properties = [(n, m) for n in node.body if isinstance(n, ast.FunctionDef) for m in item["methods"] if m["name"] == n.name and m["kind"] == "property"]
    if item["fields"] or item.get("inherited_fields"):
        frozen = any(isinstance(d, ast.Call) and any(k.arg == "frozen" and isinstance(k.value, ast.Constant) and k.value.value is True for k in d.keywords) for d in node.decorator_list)
        lines.extend(['<p class="api-label">Attributes</p>', "", "Constructor fields are retained as "+("read-only attributes." if frozen else "attributes."), ""])
    if properties:
        lines.extend(['<p class="api-label">Read-only attributes</p>', "", '<dl class="api-attributes">'])
        for property_node, record in properties:
            typename = expression(property_node.returns)
            label = f"{node.name}.{property_node.name}"+(": "+typename if typename else "")
            explanation = PROPERTY_HELP.get(property_node.name) or FIELD_HELP.get(property_node.name) or paragraph(ast.get_docstring(property_node))
            source_url = source_link(repository, commit, module, property_node)
            lines.append(f'<dt id="{object_anchor(module, node.name, property_node.name)}"><code>{escape(label)}</code></dt>')
            lines.append(f'<dd>'+ (escape(explanation)+" " if explanation else "")+f'<a href="{source_url}">Source</a></dd>')
        lines.extend(["</dl>", ""])
    methods = [n for n in node.body if isinstance(n, ast.FunctionDef) and public_node(n) and n.name != "__init__" and "property" not in [expression(d) for d in n.decorator_list]]
    if methods:
        lines.extend(['<p class="api-label">Methods</p>', "", '<ul class="api-method-list">'])
        for method in methods:
            lines.append(f'<li><a href="#{object_anchor(module, node.name, method.name)}"><code>{escape(node.name+"."+method.name)}()</code></a></li>')
        lines.extend(["</ul>", ""])
    lines.extend(example_document(full))
    for method in methods:
        lines.extend(callable_doc(module, method, repository, commit, owner=node.name, level=3))
    lines.extend(["</section>", ""])
    return lines


def literal_value(node, known):
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError):
        if isinstance(node, ast.Name) and node.id in known:
            return known[node.id]
        if isinstance(node, ast.BinOp):
            left, right = literal_value(node.left, known), literal_value(node.right, known)
            operations = {ast.Add: lambda: left+right, ast.Sub: lambda: left-right, ast.Mult: lambda: left*right, ast.Div: lambda: left/right, ast.FloorDiv: lambda: left//right, ast.Pow: lambda: left**right}
            if type(node.op) in operations:
                return operations[type(node.op)]()
        raise ValueError("dynamic expression")


def constants(tree):
    values = {}
    for n in tree.body:
        targets = n.targets if isinstance(n, ast.Assign) else [n.target] if isinstance(n, ast.AnnAssign) else []
        value = n.value if targets else None
        for target in targets:
            if isinstance(target, ast.Name) and value is not None:
                try:
                    values[target.id] = literal_value(value, values)
                except (ValueError, TypeError):
                    pass
    return values


def static_value(node, known, presets):
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError):
        if isinstance(node, ast.Name) and node.id in known:
            return known[node.id]
        value = ast.unparse(node)
        if value == "sorted(list_presets()['train'])":
            return sorted(presets.get("train", {}))
        if value == "sorted(list_presets()['evaluate'])":
            return sorted(presets.get("evaluate", {}))
        return value


def cli_inventory(module, tree, presets, command):
    known = constants(tree)
    sections = {"parser": {"name": command, "options": [], "description": ""}}
    groups = {}
    overrides = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            call = node.value
            if isinstance(call.func, ast.Attribute) and call.func.attr == "add_parser":
                var = node.targets[0].id
                section_name = command + " " + str(static_value(call.args[0], known, presets))
                kwargs = {k.arg: static_value(k.value, known, presets) for k in call.keywords}
                sections[var] = {"name": section_name, "options": [], "description": kwargs.get("help", "")}
            elif isinstance(call.func, ast.Attribute) and call.func.attr == "add_mutually_exclusive_group":
                groups[node.targets[0].id] = call.func.value.id
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if not isinstance(node.func.value, ast.Name):
            continue
        parser_var = node.func.value.id
        parser_var = groups.get(parser_var, parser_var)
        if parser_var not in sections:
            continue
        if node.func.attr == "set_defaults":
            overrides.setdefault(parser_var, {}).update({k.arg: static_value(k.value, known, presets) for k in node.keywords})
        if node.func.attr != "add_argument":
            continue
        flags = [static_value(n, known, presets) for n in node.args]
        kwargs = {k.arg: static_value(k.value, known, presets) for k in node.keywords}
        action = kwargs.get("action", "store")
        default = kwargs.get("default", False if action == "store_true" else True if action == "store_false" else None)
        dest = kwargs.get("dest", str(flags[0]).lstrip("-").replace("-", "_"))
        option = {"flags": flags, "dest": dest, "type": kwargs.get("type", "str" if action == "store" else "flag"), "default": default, "required": kwargs.get("required", not str(flags[0]).startswith("-")), "choices": kwargs.get("choices"), "action": action, "help": kwargs.get("help", ""), "line": node.lineno, "hidden": kwargs.get("help") == "argparse.SUPPRESS"}
        if "const" in kwargs:
            option["const"] = kwargs["const"]
        if node.func.value.id in groups:
            option["mutually_exclusive_group"] = node.func.value.id
        sections[parser_var]["options"].append(option)
    for parser_var, section in sections.items():
        defaults = {}
        for option in section["options"]:
            defaults.setdefault(option["dest"], option["default"])
        defaults.update(overrides.get(parser_var, {}))
        for option in section["options"]:
            option["default"] = defaults[option["dest"]]
    return {"command": command, "source_module": module, "sections": list(sections.values())}


def cli_document(cli, title, order, repository, commit):
    lines = ["---", f"title: {title}", f"description: Complete options and defaults for {cli['command']}.", "section: API reference", "apiGroup: CLI", f"order: {order}", "---", "", "## Usage", "", "```bash", cli['command']+" --help", "```", "", "Every command and subcommand accepts `-h` or `--help`. The option reference below includes exact parser defaults, choices, required arguments, and compatibility options hidden from ordinary help.", ""]
    if cli["command"] == "axosim":
        lines.extend(["A subcommand is required. Named presets replace their declared defaults, while explicitly supplied flags take precedence. Boolean defaults refer to the destination value: for example, `--blocking-transfer` sets `non_blocking=False`.", ""])
    if cli["command"] == "axosim-evaluate-model":
        lines.extend(["`--baseline-cache` and `--baseline-checkpoint` are mutually exclusive. `--output` and the compatibility alias `--output-json` are mutually exclusive. `--save-cache` cannot be combined with either baseline comparison path. The current AxoBench package is required for execution.", ""])
    elif cli["command"] == "axosim-setup":
        lines.extend(["The default data directory is `<project-root>/data`; raw and shard output directories are resolved by the plan. `--download-data` and `--convert-raw` are explicit actions. `--dry-run` prints the commands and directory operations without executing them.", ""])
    for section in cli["sections"]:
        if not section["options"] and section["name"] == "axosim":
            continue
        lines.extend(["## " + section["name"], ""])
        if section["description"]:
            lines.extend([section["description"], ""])
        if not section["options"]:
            lines.extend(["No additional arguments are required; this command prints the named recipes as JSON.", ""])
            continue
        lines.extend(['<p class="api-label">Parameters</p>', "", '<dl class="api-parameters">'])
        for option in section["options"]:
            flags = ", ".join(option["flags"])
            lines.append(f'<dt><code>{escape(flags)}</code> <span class="api-type">{escape(str(option["type"]))}</span> · '+("required" if option["required"] else "default="+escape(repr(option["default"])))+"</dt>")
            help_text = "Compatibility option hidden from default help." if option["hidden"] else option["help"]
            if not help_text:
                help_text = FIELD_HELP.get(option["dest"], "")
            if option["action"] == "store_true":
                help_text += f" Sets {option['dest']}=True."
            elif option["action"] == "store_false":
                help_text += f" Sets {option['dest']}=False."
            if "const" in option:
                help_text += f" Sets {option['dest']}={option['const']!r}."
            if option["choices"] is not None:
                help_text += " Choices: "+repr(option["choices"])+"."
            if not help_text:
                help_text = "Destination: "+option["dest"]+"."
            lines.append("<dd>"+escape(help_text.strip())+"</dd>")
        lines.extend(["</dl>", ""])
        first = section["options"][0]["line"] if section["options"] else 1
        lines.extend([f"[Parser source]({repository}/blob/{commit}/src/axosim/{cli['source_module']}.py#L{first})", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[2] / "AxoSim")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--repository", default="https://github.com/Axym-Labs/axosim", help="Canonical repository URL, which may differ from a stale local origin")
    args = parser.parse_args()
    source = args.source.resolve()
    repository = args.repository.rstrip("/").removesuffix(".git")
    commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    root = source / "src" / "axosim"
    all_modules = {m for _, _, modules, _ in PAGES for m in modules} | {"cli", "experiments", "__init__"}
    trees = {m: ast.parse((root / (m + ".py")).read_text()) for m in all_modules}
    DEFAULT_CONSTANTS.update({module: constants(tree) for module, tree in trees.items()})
    # Default values imported from the NeuronIO coordinate contract.
    for known in DEFAULT_CONSTANTS.values():
        for name, value in DEFAULT_CONSTANTS.get("neuronio_raw", {}).items():
            if name.startswith("DEFAULT_"):
                known.setdefault(name, value)
    exports = constants(trees["__init__"])["__all__"]
    import_map = {}
    for n in ast.walk(trees["__init__"]):
        if isinstance(n, ast.ImportFrom) and n.module and n.module.startswith("axosim."):
            for alias in n.names:
                import_map[alias.asname or alias.name] = (n.module.removeprefix("axosim."), alias.name)
    interface_aliases = {}
    for n in trees["interfaces"].body:
        if isinstance(n, ast.ImportFrom):
            for alias in n.names:
                interface_aliases[alias.asname or alias.name] = (n.module.removeprefix("axosim."), alias.name)
    inventory = {"schema_version": 1, "source": {"repository": repository, "commit": commit}, "exports": [], "pages": [], "symbols": [], "cli": []}
    output = args.output / "src" / "content" / "docs" / "api"
    output.mkdir(parents=True, exist_ok=True)
    module_pages = {m: slug for slug, _, modules, _ in PAGES for m in modules}
    for name in exports:
        module, implementation = import_map[name]
        if module == "interfaces" and implementation in interface_aliases:
            module, implementation = interface_aliases[implementation]
        inventory["exports"].append({"name": name, "module": module, "implementation": implementation, "page": "api/" + module_pages[module]})
    class_nodes = {n.name: n for tree in trees.values() for n in tree.body if isinstance(n, ast.ClassDef)}
    def inherited_fields(node):
        result = []
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id in class_nodes:
                result.extend(inherited_fields(class_nodes[base.id]))
        inherited = {x["name"]: x for x in result}
        inherited.update({x["name"]: x for x in fields(node)})
        return list(inherited.values())
    for offset, (slug, title, modules, intro) in enumerate(PAGES, start=1):
        lines = ["---", f"title: {title}", f"description: Signatures, parameters, return contracts, and source for {title.lower()}.", "section: API reference", f"apiGroup: {API_GROUPS[slug]}", f"order: {200+offset}", "---", "", "## Overview", "", intro, "", f"Source revision: {code(commit[:12])}. [Public export index](/api/).", ""]
        inventory["pages"].append({"slug": "api/"+slug, "modules": modules})
        for module in modules:
            tree = trees[module]
            for n in tree.body:
                if isinstance(n, (ast.Assign, ast.AnnAssign)):
                    targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                    for target in targets:
                        if isinstance(target, ast.Name) and target.id in exports:
                            typename = expression(n.annotation) if isinstance(n, ast.AnnAssign) else expression(n.value.func) if isinstance(n.value, ast.Call) else None
                            constant_roles = {"AXOSIM_MODEL_PROFILES": "Read-only mapping from exact profile IDs to architecture recipes. Use create_axosim_profile to construct a model from an entry.", "MILLION_NEURON_REALTIME_CONTRACT": "Named workload contract for the connected population benchmark. Its attributes specify the population, cadence, contact topology, precision, and timing boundary.", "AXOSIM_POPULATION_PROFILE": "Named compact population deployment recipe, including its behavior storage and model dimensions."}
                            lines.extend([f'<section class="api-symbol" id="{object_anchor(module, target.id)}">', "", "## "+target.id, ""])
                            lines.extend(signature_block("axosim."+module+"."+target.id+(": "+typename if typename else ""), source_link(repository, commit, module, n)))
                            lines.extend([constant_roles.get(target.id, "Named immutable configuration value."), "", "</section>", ""])
                            inventory["symbols"].append({"module": module, "name": target.id, "kind": "constant", "page": "api/"+slug, "line": n.lineno, "end_line": n.end_lineno, "signature": ast.unparse(n), "parameters": [], "fields": [], "methods": []})
                if not isinstance(n, (ast.ClassDef, ast.FunctionDef)) or not public_node(n):
                    continue
                if n.name == "main":
                    continue
                item = {"module": module, "name": n.name, "kind": "class" if isinstance(n, ast.ClassDef) else "function", "page": "api/"+slug, "line": n.lineno, "end_line": n.end_lineno, "signature": n.name if isinstance(n, ast.ClassDef) else signature(n), "parameters": [], "fields": [], "methods": []}
                if isinstance(n, ast.FunctionDef):
                    item["parameters"] = param_records(n, DEFAULT_CONSTANTS.get(module))
                    lines.extend(callable_doc(module, n, repository, commit))
                else:
                    item["fields"] = fields(n)
                    item["bases"] = [expression(b) for b in n.bases]
                    is_dataclass = any((isinstance(d, ast.Name) and d.id == "dataclass") or (isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "dataclass") for d in n.decorator_list)
                    if is_dataclass:
                        complete_fields = inherited_fields(n)
                        item["inherited_fields"] = [x for x in complete_fields if x["name"] not in {f["name"] for f in item["fields"]}]
                        item["parameters"] = [{**x, "kind": "positional_or_keyword"} for x in complete_fields]
                        field_signatures = [f"{x['name']}: {x['type']}" + (f" = {x['default']}" if x["default"] is not None else "") for x in complete_fields]
                        item["signature"] = n.name+"("+", ".join(field_signatures)+") -> None"
                    for method in n.body:
                        if isinstance(method, ast.FunctionDef) and public_node(method):
                            decorators = [expression(d) for d in method.decorator_list]
                            kind = "property" if "property" in decorators else "classmethod" if "classmethod" in decorators else "staticmethod" if "staticmethod" in decorators else "method"
                            method_signature = n.name+"."+method.name+(": "+expression(method.returns) if method.returns else "") if kind == "property" else signature(method)
                            method_item = {"name": method.name, "kind": kind, "signature": method_signature, "parameters": param_records(method, DEFAULT_CONSTANTS.get(module)), "line": method.lineno, "end_line": method.end_lineno, "return_type": expression(method.returns), "decorators": decorators}
                            item["methods"].append(method_item)
                            if method.name == "__init__":
                                item["signature"] = signature(method).replace("__init__", n.name, 1)
                                item["parameters"] = param_records(method, DEFAULT_CONSTANTS.get(module))
                    lines.extend(class_document(module, n, item, repository, commit))
                inventory["symbols"].append(item)
        (output / (slug+".md")).write_text("\n".join(lines))
    presets = constants(trees["experiments"]).get("_PRESETS", {})
    for slug, title, module, command, order in [
        ("cli", "AxoSim CLI", "cli", "axosim", 240),
        ("setup-cli", "Setup CLI", "setup_workflow", "axosim-setup", 241),
        ("axobench-cli", "AxoBench evaluation CLI", "axobench_iteration", "axosim-evaluate-model", 242),
    ]:
        cli = cli_inventory(module, trees[module], presets, command)
        inventory["cli"].append(cli)
        inventory["pages"].append({"slug": "api/"+slug, "modules": [module]})
        (output / (slug+".md")).write_text(cli_document(cli, title, order, repository, commit))
    index = ["---", "title: API reference", "description: Public exports, exact implementation aliases, and complete module and CLI references.", "section: API reference", "order: 200", "---", "", "## Public Python surface", "", f"This reference covers all {len(exports)} names in `axosim.__all__` at revision {code(commit[:12])}, plus the public module functions, configuration fields, dataset methods, and CLI options used by the guides. The package lazily imports these names; implementation aliases are stated explicitly.", "", "| Import from axosim | Implementation | Reference |", "| --- | --- | --- |"]
    for item in inventory["exports"]:
        index.append(f"| {code(item['name'])} | {code('axosim.'+item['module']+'.'+item['implementation'])} | [Open](/{item['page']}/) |")
    index.extend(["", "`HomeostaticThresholdController` is experimental. Configuration recipes and workload constants describe construction or execution contracts; they are not benchmark measurements. Historical checkpoint classes remain documented because the loader supports them.", "", "## Modules and configuration", ""])
    for slug, title, _, _ in PAGES:
        index.append(f"- [{title}](/api/{slug}/)")
    index.extend(["", "## Command-line tools", "", "- [AxoSim CLI](/api/cli/)", "- [Setup CLI](/api/setup-cli/)", "- [AxoBench evaluation CLI](/api/axobench-cli/)", "", "## Source and inventory", "", f"Every source link is pinned to [revision {commit[:12]}]({repository}/tree/{commit}). Repository access is currently required to open the AxoSim and AxoBench source links because these repositories are private. The [machine-readable API inventory](/api-inventory.json) records source locations, exact signatures, parameters/defaults, fields, methods, exported aliases, and CLI options. It is generated using AST parsing without importing PyTorch.", ""])
    (output / "index.md").write_text("\n".join(index))
    inventory["pages"].insert(0, {"slug": "api/index", "modules": ["__init__"]})
    inventory_path = args.output / "public" / "api-inventory.json"
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    inventory_path.write_text(json.dumps(inventory, indent=2)+"\n")
    method_count = sum(len(s["methods"]) for s in inventory["symbols"])
    option_count = sum(len(s["options"]) for c in inventory["cli"] for s in c["sections"])
    print(f"Generated {len(inventory['pages'])} reference pages, {len(exports)} exports, {len(inventory['symbols'])} symbols, {method_count} methods, {option_count} CLI argument declarations.")


if __name__ == "__main__":
    main()
