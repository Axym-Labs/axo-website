#!/usr/bin/env python3
"""Generate source-linked AxoSim references without importing the package.

Only AST parsing and argparse construction are used; no torch/GPU dependency.
Pass --source to select a local AxoSim checkout. Generated files are
the module/API pages and public/api-inventory.json; guide prose is handwritten.
"""
from __future__ import annotations

import argparse
import ast
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
}


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


def callable_doc(module, node, repository, commit, owner=None, level=2):
    full = f"{module}.{owner+'.' if owner else ''}{node.name}"
    display = f"{owner+'.' if owner else ''}{node.name}"
    decorators = [expression(d) for d in node.decorator_list]
    is_property = "property" in decorators
    shown_signature = display + (f": {expression(node.returns)}" if node.returns else "") if is_property else signature(node)
    lines = ["#"*level+" "+display, "", f"[Source]({source_link(repository, commit, module, node)})", "", "```python"]
    if not is_property:
        lines.extend("@" + decorator for decorator in decorators)
    lines.extend([shown_signature, "```", ""])
    if is_property:
        lines.extend([f"Read-only property. Access as {code('instance.'+node.name)}; do not call it as a function.", ""])
    if doc := DOC_OVERRIDES.get(full, paragraph(ast.get_docstring(node))):
        lines.extend([doc, ""])
    if full in CONTRACTS:
        lines.extend([CONTRACTS[full], ""])
    params = param_records(node, DEFAULT_CONSTANTS.get(module))
    if params:
        lines.extend(table(params) + [""])
        descriptions = [f"{code(p['name'])}: {FIELD_HELP[p['name']]}" for p in params if p["name"] in FIELD_HELP]
        if descriptions:
            lines.extend([" ".join(descriptions), ""])
    if node.returns:
        lines.extend([f"Returns {code(expression(node.returns))}.", ""])
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
    lines = ["---", f"title: {title}", f"description: Complete options and defaults for {cli['command']}.", "section: API reference", f"order: {order}", "---", "", "## Command contract", "", "The tables include parser defaults, choices, required arguments, flag actions, and compatibility options hidden from ordinary help. Every command and subcommand accepts `-h` or `--help`. Flag defaults refer to their destination value: `store_true` sets it true, while `store_false` sets it false. For example, `--blocking-transfer` changes `non_blocking` from its default true to false. Named presets may override parser defaults; explicitly supplied options take precedence. Use the installed command's `--help` when working with another revision.", ""]
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
        lines.extend(["| Argument | Type/action | Default | Required | Choices |", "| --- | --- | --- | --- | --- |"])
        for option in section["options"]:
            lines.append(f"| {', '.join(code(f) for f in option['flags'])} | {code(option['type'])} / {code(option['action'])} | {code(repr(option['default']))} | {'yes' if option['required'] else 'no'} | {code(repr(option['choices'])) if option['choices'] is not None else '—'} |")
        lines.append("")
        explained = [o for o in section["options"] if o["help"] or o.get("const") or o.get("mutually_exclusive_group")]
        for option in explained:
            flag = ", ".join(code(f) for f in option["flags"])
            help_text = "Compatibility option hidden from default help." if option["hidden"] else option["help"]
            if "const" in option:
                help_text += f" When selected, sets {code(option['dest'])} to {code(repr(option['const']))}."
            if help_text:
                lines.extend([f"{flag}: {help_text}", ""])
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
        lines = ["---", f"title: {title}", f"description: Signatures, parameters, return contracts, and source for {title.lower()}.", "section: API reference", f"order: {200+offset}", "---", "", "## Module contract", "", intro, "", f"Source revision: {code(commit[:12])}. [Public export index](/api/).", ""]
        inventory["pages"].append({"slug": "api/"+slug, "modules": modules})
        for module in modules:
            tree = trees[module]
            for n in tree.body:
                if isinstance(n, (ast.Assign, ast.AnnAssign)):
                    targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                    for target in targets:
                        if isinstance(target, ast.Name) and target.id in exports:
                            lines.extend(["## "+target.id, "", f"[Source]({source_link(repository, commit, module, n)})", "", "```python", ast.unparse(n), "```", ""])
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
                    lines.extend(["## "+n.name, "", f"[Source]({source_link(repository, commit, module, n)})", ""])
                    if doc := DOC_OVERRIDES.get(module+"."+n.name, paragraph(ast.get_docstring(n))):
                        # Historical release notes stay in source, not reader-facing descriptions.
                        if module != "axomamba":
                            lines.extend([doc, ""])
                    if item["bases"]:
                        lines.extend(["Bases: "+", ".join(code(b) for b in item["bases"])+".", ""])
                    is_dataclass = any((isinstance(d, ast.Name) and d.id == "dataclass") or (isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "dataclass") for d in n.decorator_list)
                    if is_dataclass:
                        complete_fields = inherited_fields(n)
                        item["inherited_fields"] = [x for x in complete_fields if x["name"] not in {f["name"] for f in item["fields"]}]
                        item["parameters"] = [{**x, "kind": "positional_or_keyword"} for x in complete_fields]
                        field_signatures = [f"{x['name']}: {x['type']}" + (f" = {x['default']}" if x["default"] is not None else "") for x in complete_fields]
                        item["signature"] = n.name+"("+", ".join(field_signatures)+") -> None"
                        # The inherited Mamba configuration has many fields; its complete
                        # constructor remains machine-readable and the field table is below.
                        if n.name != "AxoMambaConfig":
                            lines.extend(["```python", item["signature"], "```", ""])
                    if module == "axomamba" and n.name == "AxoMambaConfig":
                        lines.extend(["Inherits every configuration field and default in `BranchOfficialMambaConfig` below. `default_axomamba_config` applies the selected AxoSim recipe over those raw defaults.", ""])
                    if module == "axomamba" and n.name in {"AxoMamba", "AxoPyTorchMamba"}:
                        lines.extend(["Inherits full-sequence and streaming methods from `BranchOfficialMamba` below. The fallback uses a distinct checkpoint backend.", ""])
                    if item["fields"]:
                        lines.extend(["### Fields", ""] + table(item["fields"]) + [""])
                        if any(x["name"] in FIELD_HELP for x in item["fields"]):
                            lines.extend([" ".join(f"{code(x['name'])}: {FIELD_HELP[x['name']]}" for x in item["fields"] if x["name"] in FIELD_HELP), ""])
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
                            lines.extend(callable_doc(module, method, repository, commit, owner=n.name, level=3))
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
