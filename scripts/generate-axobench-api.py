#!/usr/bin/env python3
"""Generate source-linked AxoBench reference pages.

Signatures, defaults, dataclass fields, and source line ranges are read from
the AxoBench source with AST parsing. The axobench CLI options are read from
its argparse parser, which requires importing axobench.cli (NumPy only).
Every documented parameter and option must have a reviewed description below;
the generator fails instead of emitting an undocumented entry.
"""
from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECTION = "AxoBench API"

PAGES = [
    {
        "slug": "evaluation", "title": "Model evaluation", "group": "Evaluation", "order": 301,
        "overview": "The model-iteration evaluator selects validation traces and intervention pairs, calls a prediction function in batches, calibrates the spike threshold on a held-out block, and returns a fixed report of metrics and 24 attention rows. evaluate_predictions applies the same protocol to stored arrays. The guide [Benchmarking with AxoBench](/axobench/benchmarking/) describes the protocol.",
        "items": [
            ("benchmark.iteration_evaluator", "EvaluationConfig"),
            ("benchmark.iteration_evaluator", "PairedInterventionPredictions"),
            ("benchmark.iteration_evaluator", "evaluate_model"),
            ("benchmark.iteration_evaluator", "evaluate_predictions"),
            ("benchmark.iteration_evaluator", "calibrate_spike_threshold"),
            ("benchmark.iteration_evaluator", "sera_reference_voltage"),
            ("benchmark.iteration_evaluator", "default_iteration_sample_limits"),
            ("benchmark.iteration_evaluator", "format_evaluation_report"),
            ("benchmark.iteration_evaluator", "write_evaluation_report"),
        ],
    },
    {
        "slug": "comparison", "title": "Paired comparison", "group": "Evaluation", "order": 302,
        "overview": "A baseline cache freezes one model's predictions together with the trace selection, target hash, and protocol. Candidates are compared against it on identical traces with a morphology-stratified paired bootstrap; see [compare with a baseline](/axobench/benchmarking/#compare-with-a-baseline).",
        "items": [
            ("benchmark.iteration_evaluator", "ModelEvaluationCache"),
            ("benchmark.iteration_evaluator", "create_model_evaluation_cache"),
            ("benchmark.iteration_evaluator", "write_model_evaluation_cache"),
            ("benchmark.iteration_evaluator", "load_model_evaluation_cache"),
            ("benchmark.iteration_evaluator", "evaluate_model_against_cache"),
            ("benchmark.iteration_evaluator", "compare_predictions"),
            ("benchmark.iteration_evaluator", "format_model_comparison"),
            ("benchmark.iteration_evaluator", "write_model_comparison"),
        ],
    },
    {
        "slug": "metrics", "title": "Core metric functions", "group": "Metrics", "order": 303,
        "overview": "Array-level implementations of Voltage SERA, the subthreshold voltage RMSE, Response SERA, Dynamics SERA, and the SERA skill scores. Predictions and targets are (trace, time, 2) arrays in the AxoBench target coordinate; voltages are converted to millivolts as soma/soma_scale + soma_bias_mv, and raw_soma_mv replaces the reconstructed teacher voltage when supplied. [Core metrics](/axobench/metrics/) gives the definitions.",
        "items": [
            ("metrics", "compute_core_metric_set"),
            ("metrics", "iron_voltage_sera"),
            ("metrics", "sera_skill_trace_terms"),
            ("metrics", "sera_skills"),
            ("metrics", "subthreshold_voltage_error"),
            ("metrics", "subthreshold_voltage_point_terms"),
            ("metrics", "subthreshold_voltage_trace_terms"),
            ("metrics", "ap_window_ends"),
            ("metrics", "ap_window_mask"),
            ("metrics", "response_sera"),
            ("metrics", "response_sera_trace_terms"),
            ("metrics", "iron_dynamics_sera"),
            ("const", "metrics", ["AP_PRE_STEPS", "AP_POST_STEPS", "AP_FLAT_SLOPE_MV_PER_MS", "AP_WAVEFORM_PRE_STEPS", "AP_ISOLATION_STEPS", "AP_MIN_ISOLATED_SPIKES", "SOMA_CLIP_MV"]),
        ],
    },
    {
        "slug": "spike-metrics", "title": "Spike event metrics", "group": "Metrics", "order": 304,
        "overview": "Spike events, thresholds, one-to-one event matching, and F1 over timing tolerances, together with the coincidence factor and the historical timestep AUC and voltage RMSE. Spike arrays are (trace, time) or (time,); values above 0.5 count as events.",
        "items": [
            ("metrics", "spike_event_peaks"),
            ("metrics", "spike_events"),
            ("metrics", "prevalence_matched_threshold"),
            ("metrics", "event_count_matched_threshold"),
            ("metrics", "spike_event_matches"),
            ("metrics", "spike_event_confusion"),
            ("metrics", "spike_f1_curve"),
            ("metrics", "coincidence_factor"),
            ("metrics", "binary_auc"),
            ("metrics", "spike_auc"),
            ("metrics", "soma_rmse"),
        ],
    },
    {
        "slug": "relevance", "title": "IRon relevance", "group": "Metrics", "order": 305,
        "overview": "The relevance function and squared error-relevance area of the IRon R package (Ribeiro and Moniz, 2020) with its default settings: adjusted-boxplot fences (Hubert and Vandervieren, 2008) with an exact medcouple, relevance 1 at the fences and 0 at the median, and a trapezoidal area over thresholds with step 0.001.",
        "items": [
            ("relevance", "iron_relevance"),
            ("relevance", "iron_threshold_weights"),
            ("relevance", "iron_sera"),
            ("relevance", "adjusted_box_fences"),
            ("relevance", "medcouple"),
            ("relevance", "fivenum"),
        ],
    },
    {
        "slug": "data", "title": "Trace datasets", "group": "Data", "order": 306,
        "overview": "ShardedNeuronIODataset reads a split directory of NPZ shards, or of NPY shards listed in a manifest, as used by every AxoBench release. Inputs are returned as float32 (batch, time, channels) and targets as float32 (batch, time, 2). See [single-neuron traces](/axobench/single-neuron/#download-and-load) for an example.",
        "items": [
            ("data", "ShardedNeuronIODataset"),
            ("data", "NeuronIOSample"),
            ("data", "write_demo_shards"),
            ("data", "repack_shards_as_npy"),
        ],
    },
    {
        "slug": "layout", "title": "Dataset layout and schema", "group": "Data", "order": 307,
        "overview": "V1DatasetLayout resolves the split and intervention directories of an evaluation root. The schema module records the v1 split names, intervention conditions, morphology registry, target views, and diagnostic suite catalog.",
        "items": [
            ("benchmark.selectors", "V1DatasetLayout"),
            ("benchmark.selectors", "DatasetSelector"),
            ("const", "benchmark.dataset_schema", ["ORDINARY_SPLITS", "INTERVENTION_CONDITIONS", "V1_MORPHOLOGY_COUNT", "V1_TRAIN_TRACES_PER_MORPHOLOGY", "DIAGNOSTIC_SUITES", "DIAGNOSTIC_ROW_COLUMNS"]),
            ("benchmark.dataset_schema", "v1_morphologies"),
            ("benchmark.dataset_schema", "MorphologySpec"),
            ("benchmark.dataset_schema", "default_target_views"),
            ("benchmark.dataset_schema", "TargetViewSpec"),
            ("benchmark.dataset_schema", "build_v1_dataset_manifest_template"),
            ("benchmark.dataset_schema", "validate_v1_manifest_template"),
            ("benchmark.dataset_schema", "build_diagnostic_suite_catalog"),
        ],
    },
    {
        "slug": "interventions", "title": "Intervention inputs", "group": "Data", "order": 308,
        "overview": "Input-side constructors for the five intervention conditions and a loader for paired intervention shards. Each constructor returns the edited inputs and a boolean mask of the baseline events it removed or moved. Producing teacher targets for new inputs requires the simulator stack in axobench.generation. [Paired interventions](/axobench/interventions/) describes the released conditions.",
        "items": [
            ("benchmark.structured_intervention", "make_structured_intervention_inputs"),
            ("benchmark.structured_intervention", "make_event_dropout_inputs"),
            ("benchmark.structured_intervention", "make_selective_event_dropout_inputs"),
            ("benchmark.structured_intervention", "make_temporal_jitter_inputs"),
            ("benchmark.structured_intervention", "make_site_silence_inputs"),
            ("benchmark.runner", "load_intervention_pair_npz"),
        ],
    },
    {
        "slug": "neuronio", "title": "NeuronIO conversion", "group": "Data", "order": 309,
        "overview": "Parse raw NeuronIO simulation pickles and write deterministic AxoBench shards. Inhibitory channels receive the sign -1, and the soma target is clipped at -55 mV and normalized as (v + 67.7) * 0.1. Converted shards store no unclipped voltage; [NeuronIO compatibility](/axobench/neuronio/) explains the consequences for the metrics. Raw files are Python pickles: parse only trusted files.",
        "items": [
            ("neuronio_raw", "convert_neuronio_pickles"),
            ("neuronio_raw", "parse_neuronio_pickle"),
            ("neuronio_raw", "RawNeuronIO"),
            ("neuronio_raw", "normalize_soma"),
            ("neuronio_raw", "create_neuronio_input_type"),
        ],
    },
    {
        "slug": "defect-injection", "title": "Defect injection", "group": "Diagnostics", "order": 310,
        "overview": "Controlled defects injected into teacher traces, for testing whether a metric responds to a known error as it should. Spike-timing defects move the action-potential waveform with the spike; voltage defects leave the spike train exact. Import from axobench.benchmark.defect_injection. See [test metric sensitivity](/axobench/diagnostics/#test-metric-sensitivity).",
        "items": [
            ("const", "benchmark.defect_injection", ["DEFECTS", "DEFAULT_DOSES"]),
            ("benchmark.defect_injection", "inject_defect"),
            ("benchmark.defect_injection", "defect_dose_rows"),
            ("benchmark.defect_injection", "axobench_scores"),
            ("benchmark.defect_injection", "historical_scores"),
            ("benchmark.defect_injection", "smoothed_spike_score"),
        ],
    },
    {
        "slug": "diagnostics", "title": "Diagnostic rows", "group": "Diagnostics", "order": 311,
        "overview": "Dataframe-first diagnostic rows for teacher QC, model diagnostics, paired interventions, morphology routing, and morphology contrasts, with runners that read an evaluation root and a bundle that writes all of them. Every row carries the columns in DIAGNOSTIC_ROW_COLUMNS. A row is kept when its diagnostic belongs to one of the suites in the context. See [diagnostics](/axobench/diagnostics/).",
        "items": [
            ("benchmark.diagnostic_rows", "DiagnosticContext"),
            ("benchmark.diagnostic_rows", "evaluate_model_diagnostic_rows"),
            ("benchmark.diagnostic_rows", "teacher_qc_diagnostic_rows"),
            ("benchmark.diagnostic_rows", "paired_intervention_diagnostic_rows"),
            ("benchmark.diagnostic_rows", "morphology_routing_qc_rows"),
            ("benchmark.diagnostic_rows", "morphology_contrast_diagnostic_rows"),
            ("benchmark.diagnostic_rows", "validate_diagnostic_rows"),
            ("benchmark.diagnostic_rows", "write_diagnostic_rows"),
            ("benchmark.runner", "run_teacher_qc_on_selector"),
            ("benchmark.runner", "run_model_diagnostics_on_selector"),
            ("benchmark.runner", "run_paired_intervention_on_selector"),
            ("benchmark.runner", "run_paired_intervention_on_npz"),
            ("benchmark.bundle", "run_v1_benchmark_bundle"),
            ("benchmark.reports", "summarize_diagnostic_rows"),
            ("benchmark.reports", "write_diagnostic_summary"),
        ],
    },
    {
        "slug": "error-anatomy", "title": "Error anatomy", "group": "Diagnostics", "order": 312,
        "overview": "error_anatomy breaks a prediction's errors down by spike outcome, time from the nearest teacher spike, teacher firing rate, frequency band, and morphology, on the evaluator's scored traces with its threshold, spike events, action-potential windows, and relevance. plot_error_anatomy draws the result and writes a standalone pgfplots version. Import from axobench.benchmark.error_anatomy and axobench.benchmark.plots. [Error anatomy](/axobench/error-anatomy/) explains how to read each part.",
        "items": [
            ("benchmark.error_anatomy", "error_anatomy"),
            ("benchmark.error_anatomy", "reweight_to_rate_distribution"),
            ("const", "benchmark.error_anatomy", ["HIT_TOLERANCE_STEPS", "STA_LAGS_STEPS"]),
            ("benchmark.plots", "plot_error_anatomy"),
            ("benchmark.plots", "apply_paper_plot_style"),
        ],
    },
]

# Shared parameter descriptions; a symbol-specific entry in DOCS takes precedence.
COMMON = {
    "model_fn": "Prediction function mapping float32 inputs (batch, time, 1278) to (batch, time, 2) outputs: a spike score and the soma target coordinate. With supports_morphology_ids=True it is called with a morphology_ids keyword.",
    "dataset_root": "Evaluation root containing val/ and optionally interventions/<condition>/.",
    "max_samples": "Validation traces to select; None uses default_iteration_sample_limits (120).",
    "batch_size": "Traces per prediction call.",
    "max_intervention_samples": "Pairs per intervention condition; None uses the default of 40.",
    "max_interventions": "Maximum number of condition directories read, in sorted order.",
    "intervention_workers": "Threads that load intervention shards in parallel.",
    "intervention_names": "Condition directory names to evaluate; None discovers all. A missing name raises FileNotFoundError.",
    "multiple_morphologies": "Balance traces and pairs across all morphologies instead of using one.",
    "morphology_id": "Morphology for single-morphology mode; None uses the alphabetically first. Cannot be combined with multiple_morphologies=True.",
    "validation_sample_start": "Start of the selected block within the morphology, or within the balanced order in multiple-morphology mode.",
    "cache_shards": "Decoded shards kept in memory by the reader.",
    "config": "Evaluation settings; None uses EvaluationConfig().",
    "soma_scale": "Scale of the soma target coordinate; millivolts are soma / soma_scale + soma_bias_mv.",
    "soma_bias_mv": "Millivolt offset of the soma target coordinate.",
    "ignore_start": "Initial timesteps excluded from scoring.",
    "timestep_ms": "Duration of one timestep in milliseconds.",
    "raw_soma_mv": "Optional unclipped teacher soma voltage in millivolts, shaped (trace, time); replaces the voltage reconstructed from the target.",
    "trace_ids": "Sample IDs, one per trace; the text before the first ':' is the morphology or cell-type group.",
    "prediction": "Model outputs shaped (trace, time, 2).",
    "target": "Teacher targets shaped (trace, time, 2): spike indicator and soma target coordinate.",
    "context": "Row metadata and suite selection; None uses the function's default context.",
    "output": "Optional .json, .jsonl, or .csv path for the rows.",
    "path": "File path.",
    "rows": "Diagnostic row dictionaries.",
    "seed": "Random seed.",
    "model_id": "Model name in the report.",
    "selector": "Resolved split or intervention directory from V1DatasetLayout.",
}

DOCS = {
    # iteration_evaluator
    "benchmark.iteration_evaluator.EvaluationConfig": {
        "summary": "Frozen settings of the metric protocol and attention thresholds. Its fields are part of every cache protocol, so paired comparisons require equal configurations.",
        "params": {
            "soma_scale": "Scale of the soma target coordinate.",
            "soma_bias_mv": "Millivolt offset of the soma target coordinate.",
            "ignore_start": "Initial timesteps excluded from every metric and diagnostic.",
            "timestep_ms": "Duration of one timestep in milliseconds.",
            "calibration_fraction": "Share of traces, in (0, 1), used only to calibrate the spike threshold.",
            "default_spike_threshold": "Uncalibrated threshold checked by the default_threshold_count attention row; it does not set the scoring threshold.",
            "f1_tolerances_steps": "Timing tolerances of the F1 curve in steps; Mean F1 averages over them.",
            "selected_f1_steps": "Tolerances reported as spike_f1_exact and spike_f1_5ms; both must be in f1_tolerances_steps.",
            "physiological_voltage_bounds_mv": "Envelope of the voltage_bounds attention row.",
            "physiological_slew_bound_mv_per_ms": "One-step slope bound of the voltage_slew attention row.",
            "refractory_period_ms": "Minimum inter-spike interval of the refractory_violations attention row.",
            "state_error_ratio_watch": "State-to-overall RMSE ratio that triggers a state attention row.",
            "state_error_floor_mv": "Minimum state RMSE for a state attention row to trigger.",
        },
    },
    "benchmark.iteration_evaluator.PairedInterventionPredictions": {
        "summary": "Predictions and teacher traces for one intervention condition, used for Response SERA and the intervention attention rows.",
        "params": {
            "name": "Condition name reported with the results.",
            "baseline_prediction": "Model outputs for the baseline inputs, (pair, time, 2).",
            "intervention_prediction": "Model outputs for the edited inputs, (pair, time, 2).",
            "baseline_target": "Teacher targets for the baseline inputs.",
            "intervention_target": "Teacher targets for the edited inputs.",
            "baseline_raw_soma_mv": "Optional unclipped baseline teacher voltage in millivolts.",
            "intervention_raw_soma_mv": "Optional unclipped intervention teacher voltage in millivolts.",
            "morphology_ids": "Optional morphology per pair, used to stratify the paired bootstrap.",
        },
    },
    "benchmark.iteration_evaluator.ModelEvaluationCache": {
        "summary": "A frozen baseline: predictions, intervention predictions, trace selection, target hash, report, and protocol.",
        "params": {
            "model_id": "Baseline name.",
            "report": "Baseline evaluation report.",
            "prediction": "Baseline outputs for the selected traces, in report order.",
            "trace_ids": "Ordered sample IDs of the selected traces.",
            "target_sha256": "SHA-256 of the target array, including dtype and shape.",
            "interventions": "Baseline predictions and teacher traces per condition.",
            "protocol": "Sample limits, morphology selection, intervention names, sample start, and EvaluationConfig fields.",
            "source_path": "File the cache was loaded from, if any.",
        },
    },
    "benchmark.iteration_evaluator.evaluate_model": {
        "summary": "Run batched inference on an evaluation root and return the evaluation report. Selected traces are reordered round-robin by morphology before calibration, so the calibration block covers every selected morphology.",
        "returns": [("report", "dict[str, Any]", "The evaluate_predictions report plus evaluation_seconds, morphology_mode, morphology_ids, standard_sample_limit, intervention_sample_limit_per_condition, validation_sample_start, and sample_profile.")],
    },
    "benchmark.iteration_evaluator.evaluate_predictions": {
        "summary": "Evaluate stored predictions. The first round(calibration_fraction * traces) traces, at least one and at most all but one, calibrate the spike threshold by prevalence matching; all metrics and diagnostics use the remaining traces. At least two traces are required.",
        "params": {
            "prediction": "Model outputs shaped (trace, time, 2), in calibration-then-scoring order.",
            "target": "Teacher targets in the same order.",
            "inputs": "Optional per-step input summary shaped (trace, time, channels); its absolute sum per step is the input load of the low-input and post-burst diagnostics. Excitatory and inhibitory event counts suffice.",
            "interventions": "Per-condition paired predictions for Response SERA and the intervention rows.",
            "model_id": "Model name in the report.",
        },
        "returns": [("report", "dict[str, Any]", "model_id, samples, calibration_samples, scored_samples, spike_threshold, spike_f1_curve, subthreshold_ap_window, metrics (id, value, unit, meaning, core; seven core and six secondary rows, including the SERA skill rows), diagnostics (24 rows with area, id, attention, value, unit, primary, trigger, basis), and interventions.")],
    },
    "benchmark.iteration_evaluator.default_iteration_sample_limits": {
        "summary": "Default ordinary and per-condition intervention sample limits for a morphology mode.",
        "params": {"multiple_morphologies": "Select the multiple-morphology defaults."},
        "returns": [("limits", "tuple[int, int]", "(120, 40) in both modes.")],
    },
    "benchmark.iteration_evaluator.format_evaluation_report": {
        "summary": "Render the bounded plain-text report: header, core and secondary metrics, action-potential window ends, and the attention panel with its summary line.",
        "params": {"report": "Report returned by evaluate_model or evaluate_predictions."},
        "returns": [("text", "str", "Deterministic plain-text report.")],
    },
    "benchmark.iteration_evaluator.write_evaluation_report": {
        "summary": "Write a report as strict JSON or tidy CSV, selected by the suffix; non-finite values become null or empty.",
        "params": {"report": "Report to write.", "path": "Destination ending in .json or .csv; parent directories are created."},
        "returns": [("path", "Path", "The written path.")],
    },
    "benchmark.iteration_evaluator.create_model_evaluation_cache": {
        "summary": "Evaluate a baseline once and retain everything needed to compare later candidates on the same traces.",
        "params": {"model_id": "Baseline name stored in the cache and report."},
        "returns": [("cache", "ModelEvaluationCache", "Baseline predictions, report, trace IDs, target hash, interventions, and protocol.")],
    },
    "benchmark.iteration_evaluator.write_model_evaluation_cache": {
        "summary": "Write a cache as a compressed, pickle-free NPZ file with JSON metadata.",
        "params": {"cache": "Cache to write.", "path": "Destination ending in .npz; parent directories are created."},
        "returns": [("path", "Path", "The written path.")],
    },
    "benchmark.iteration_evaluator.load_model_evaluation_cache": {
        "summary": "Load a cache written by write_model_evaluation_cache, without pickle.",
        "params": {"path": "Cache file."},
        "returns": [("cache", "ModelEvaluationCache", "The cache, with source_path set.")],
    },
    "benchmark.iteration_evaluator.evaluate_model_against_cache": {
        "summary": "Evaluate a candidate and compare it with a cached baseline. Raises ValueError unless the protocol, ordered trace IDs, and target hash match the cache.",
        "params": {
            "candidate_model_fn": "Candidate prediction function, with the same contract as model_fn of evaluate_model.",
            "baseline_cache": "Cache object or path to a cache file.",
            "candidate_id": "Candidate name in the comparison.",
            "bootstrap_replicates": "Paired bootstrap replicates.",
            "bootstrap_seed": "Seed of the paired bootstrap.",
        },
        "returns": [("comparison", "dict[str, Any]", "The compare_predictions result plus evaluation_seconds and baseline_cache, the cache path.")],
    },
    "benchmark.iteration_evaluator.compare_predictions": {
        "summary": "Compare two models on the same traces. Scored traces are resampled within each morphology; each model keeps its calibrated threshold, and relevance weights and action-potential windows stay at their full-sample values. Intervals are the 2.5% and 97.5% quantiles of the replicate differences.",
        "params": {
            "candidate_prediction": "Candidate outputs, (trace, time, 2).",
            "baseline_prediction": "Baseline outputs for the same traces.",
            "target": "Teacher targets for the same traces.",
            "inputs": "Optional per-step input summary, as for evaluate_predictions.",
            "candidate_interventions": "Candidate paired predictions per condition.",
            "baseline_interventions": "Baseline paired predictions in the same condition order and with identical teacher targets.",
            "candidate_id": "Candidate name.",
            "baseline_id": "Baseline name; must equal baseline_report['model_id'] when a report is supplied.",
            "baseline_report": "Optional cached baseline report; recomputed when its metric set or action-potential windows differ from the candidate's.",
            "bootstrap_replicates": "Paired bootstrap replicates; must be positive.",
            "seed": "Seed of the paired bootstrap.",
        },
        "returns": [("comparison", "dict[str, Any]", "candidate and baseline reports, comparison rows (id, candidate, baseline, delta, ci95_low, ci95_high, unit, core, preferred_direction, assessment), bootstrap_replicates, bootstrap_seed, and confidence_level 0.95.")],
    },
    "benchmark.iteration_evaluator.format_model_comparison": {
        "summary": "Render the paired comparison table with candidate, baseline, difference, 95% interval, and assessment per metric.",
        "params": {"comparison": "Result of compare_predictions or evaluate_model_against_cache."},
        "returns": [("text", "str", "Plain-text table.")],
    },
    "benchmark.iteration_evaluator.write_model_comparison": {
        "summary": "Write a complete JSON comparison or a tidy CSV of the paired differences, selected by the suffix.",
        "params": {"comparison": "Comparison to write.", "path": "Destination ending in .json or .csv."},
        "returns": [("path", "Path", "The written path.")],
    },
    "benchmark.iteration_evaluator.calibrate_spike_threshold": {
        "summary": "Calibration trace count and spike threshold of evaluate_predictions. The first round(calibration_fraction * traces) traces, at least one and leaving at least one to score, set the threshold whose supra-threshold step count over their scored steps matches their teacher spike count.",
        "params": {"prediction": "Model outputs shaped (trace, time, 2), in calibration-then-scoring order.", "target": "Teacher targets in the same order.", "config": "Evaluation settings; calibration_fraction and ignore_start are used."},
        "returns": [("result", "tuple[int, float]", "Number of calibration traces and the calibrated threshold.")],
    },
    "benchmark.iteration_evaluator.sera_reference_voltage": {
        "summary": "Constant reference voltage of the SERA skill scores: the mean teacher voltage clipped at -55 mV over the scored steps of the calibration traces, so no scored trace enters it.",
        "params": {"target": "Teacher targets shaped (trace, time, 2), in calibration-then-scoring order.", "raw_soma_mv": "Optional unclipped teacher voltage (trace, time); otherwise the voltage is reconstructed from the target.", "n_calibration": "Number of leading calibration traces.", "config": "Evaluation settings; ignore_start and the voltage coordinate are used."},
        "returns": [("reference_mv", "float", "Reference voltage in mV.")],
    },
    # metrics
    "metrics.sera_skill_trace_terms": {
        "summary": "Per-trace IRon SERA areas behind the SERA skill scores. Relevance is fitted once on the pooled scored teacher, as in iron_voltage_sera and iron_dynamics_sera, so sums over any subset of traces give that subset's skills.",
        "params": {
            "prediction": "Scored model outputs shaped (trace, time, 2).",
            "target": "Scored teacher targets of the same shape.",
            "reference_mv": "Constant reference voltage in mV, usually sera_reference_voltage of the calibration traces.",
            "raw_soma_mv": "Optional unclipped teacher voltage (trace, time); replaces the voltage reconstructed from the target.",
        },
        "returns": [("terms", "dict[str, np.ndarray]", "Per trace: voltage (prediction area), voltage_reference (constant reference), voltage_ceiling (teacher clipped at -55 mV), dynamics and dynamics_reference (dV/dt areas of the prediction and of the constant, whose rate is zero), and teacher_spikes.")],
    },
    "metrics.sera_skills": {
        "summary": "SERA skill scores from sera_skill_trace_terms, pooled over all or selected traces. Each skill is 1 - area / reference area; prediction and reference share relevance and spike count, so this equals 1 - SERA / SERA(reference).",
        "params": {"terms": "Result of sera_skill_trace_terms.", "indices": "Trace indices to pool; None pools all, and repeated indices count repeatedly as in a bootstrap draw."},
        "returns": [("skills", "dict[str, float | None]", "voltage_sera_skill, voltage_sera_ceiling_skill (the skill of the teacher clipped at -55 mV, the best prediction without action potentials), voltage_sera_skill_of_ceiling (their ratio), and dynamics_sera_skill; None where a reference area or the ceiling is zero.")],
    },
    "metrics.subthreshold_voltage_point_terms": {
        "summary": "Per-step terms of the subthreshold voltage error on the scored steps, for breaking the error down by time or frequency. Steps in the action-potential windows of teacher or predicted spikes are excluded and both voltages are clipped at -55 mV.",
        "params": {
            "prediction": "Model outputs covering the whole trace, (trace, time, 2).",
            "target": "Teacher targets covering the whole trace.",
            "predicted_spikes": "Predicted spike events of the scored steps only, (trace, time - ignore_start).",
            "raw_soma_mv": "Optional unclipped teacher voltage covering the whole trace.",
            "ap_post_steps": "Per-trace window ends; None computes them with ap_window_ends from the scored teacher steps.",
        },
        "returns": [("terms", "dict[str, np.ndarray]", "keep (boolean mask of retained steps), error (clipped prediction minus clipped teacher), and deviation (clipped teacher minus its per-trace mean over retained steps), each (trace, time - ignore_start) and zero where not kept.")],
    },
    "metrics.compute_core_metric_set": {
        "summary": "Compute the core metrics on aligned arrays without a calibration split. Without spike_threshold, the default policy chooses the threshold on the same traces so that the predicted event count equals the teacher spike count.",
        "params": {
            "spike_threshold": "Fixed spike threshold; recommended when calibrated on other traces.",
            "spike_threshold_policy": "'prevalence' for the event-count-matched threshold or 'zero' for 0, used when spike_threshold is None.",
            "spike_tolerances_steps": "F1 timing tolerances in steps.",
            "spike_refractory_steps": "Suppression radius of spike events; None treats every supra-threshold step as an event.",
            "intervention_prediction": "Optional model outputs for edited inputs; target and prediction then act as the baseline.",
            "intervention_target": "Teacher targets for the edited inputs; required with intervention_prediction.",
            "intervention_raw_soma_mv": "Optional unclipped teacher voltage for the edited inputs.",
        },
        "returns": [("result", "dict[str, Any]", "voltage, dynamics, subthreshold, spike, and optionally response sub-results, plus voltage_sera_iron_per_spike_mv2, subthreshold_rmse_mv, subthreshold_skill, dynamics_sera_iron_per_spike_mv2_per_ms2, spike_mean_f1, spike_f1_area, spike_threshold, spike_threshold_kind, and response_sera_iron_per_spike_mv2 when available.")],
    },
    "metrics.iron_voltage_sera": {
        "summary": "IRon-default Voltage SERA per teacher spike, with relevance fitted on the pooled scored teacher voltage.",
        "returns": [("result", "dict[str, Any]", "voltage_sera_iron_mv2 (area), voltage_sera_iron_per_spike_mv2 (None without teacher spikes), teacher_spikes, and relevance_mean.")],
    },
    "metrics.iron_dynamics_sera": {
        "summary": "IRon-default SERA of the one-step voltage change per teacher spike, with relevance fitted on the teacher's rate of change. Requires at least two scored steps.",
        "returns": [("result", "dict[str, Any]", "dynamics_sera_iron_mv2_per_ms2, dynamics_sera_iron_per_spike_mv2_per_ms2, teacher_spikes, and relevance_mean.")],
    },
    "metrics.subthreshold_voltage_error": {
        "summary": "Somatic voltage RMSE outside action-potential windows of teacher and predicted spikes, with both voltages clipped at -55 mV, and its skill against the per-trace mean clipped teacher voltage.",
        "params": {
            "prediction": "Model outputs covering the whole trace, (trace, time, 2).",
            "target": "Teacher targets covering the whole trace.",
            "predicted_spikes": "Predicted spike events of the scored steps only, (trace, time - ignore_start).",
            "raw_soma_mv": "Optional unclipped teacher voltage covering the whole trace.",
            "ap_post_steps": "Per-trace window ends; None computes them with ap_window_ends from the scored teacher steps.",
        },
        "returns": [("result", "dict[str, Any]", "subthreshold_rmse_mv, subthreshold_skill, null_subthreshold_rmse_mv, and retained_points.")],
    },
    "metrics.subthreshold_voltage_trace_terms": {
        "summary": "Per-trace sums behind subthreshold_voltage_error, so that subsets of traces can be pooled with fixed windows, as the paired bootstrap does. Keyword arguments are those of subthreshold_voltage_point_terms.",
        "params": {
            "prediction": "Model outputs covering the whole trace, (trace, time, 2).",
            "target": "Teacher targets covering the whole trace.",
            "predicted_spikes": "Predicted spike events of the scored steps only, (trace, time - ignore_start).",
            "raw_soma_mv": "Optional unclipped teacher voltage covering the whole trace.",
            "ap_post_steps": "Per-trace window ends; None computes them with ap_window_ends.",
        },
        "returns": [("terms", "dict[str, np.ndarray]", "squared_error, null_squared_error, and retained_points per trace.")],
    },
    "metrics.ap_window_ends": {
        "summary": "Cell-type-specific end of the action-potential window. For each trace-ID prefix, the mean waveform of isolated teacher spikes (lags -6 to +30, no other spike in the next 30 steps) is computed, and the end is the first lag >= 1 at which it changes by less than 1 mV per ms. Groups with fewer than 20 isolated spikes, no flat lag, or no voltage use 4.",
        "params": {
            "raw_soma_mv": "Unclipped teacher voltage (trace, time), or None to use the fallback for every group.",
            "teacher_spikes": "Teacher spike indicators, (trace, time).",
        },
        "returns": [("result", "dict[str, Any]", "post_steps per trace, end_steps_by_cell_type, and fallback_cell_types.")],
    },
    "metrics.ap_window_mask": {
        "summary": "Boolean mask of the steps from 2 before to post_steps after each spike, inclusive.",
        "params": {
            "spikes": "Spike indicators, (trace, time).",
            "post_steps": "Window end per trace; None uses AP_POST_STEPS.",
        },
        "returns": [("mask", "np.ndarray", "Boolean (trace, time) mask.")],
    },
    "metrics.response_sera": {
        "summary": "IRon-default Response SERA per teacher spike. The error is the predicted minus the teacher voltage change (intervention minus baseline); relevance is fitted on the pooled teacher change, and the area is divided by the teacher spikes of baseline and intervention traces.",
        "params": {
            "baseline_prediction": "Model outputs for the baseline inputs, (pair, time, 2).",
            "intervention_prediction": "Model outputs for the edited inputs.",
            "baseline_target": "Teacher targets for the baseline inputs.",
            "intervention_target": "Teacher targets for the edited inputs.",
            "baseline_raw_soma_mv": "Optional unclipped baseline teacher voltage.",
            "intervention_raw_soma_mv": "Optional unclipped intervention teacher voltage.",
        },
        "returns": [("result", "dict[str, Any]", "response_sera_iron_mv2, response_sera_iron_per_spike_mv2, the zero-response control in both forms, teacher_spikes, response_rmse_mv, teacher_response_abs_mean_mv, and relevance_mean.")],
    },
    "metrics.response_sera_trace_terms": {
        "summary": "Per-pair terms of Response SERA with the relevance fitted once on all supplied pairs, so that subsets can be pooled with fixed relevance.",
        "params": {
            "baseline_prediction": "Model outputs for the baseline inputs, (pair, time, 2).",
            "intervention_prediction": "Model outputs for the edited inputs.",
            "baseline_target": "Teacher targets for the baseline inputs.",
            "intervention_target": "Teacher targets for the edited inputs.",
            "baseline_raw_soma_mv": "Optional unclipped baseline teacher voltage.",
            "intervention_raw_soma_mv": "Optional unclipped intervention teacher voltage.",
        },
        "returns": [("terms", "dict[str, np.ndarray]", "area, zero_response_area, and teacher_spikes per pair, plus the error, teacher_delta, and weights arrays.")],
    },
    "metrics.spike_event_peaks": {
        "summary": "Candidate spike events: local maxima of each trace's score, kept greedily from the highest score down with other maxima within refractory_steps suppressed. A step is a maximum if it exceeds the previous step and is not below the next.",
        "params": {
            "scores": "Spike scores, (trace, time).",
            "refractory_steps": "Suppression radius in steps; 0 keeps every maximum.",
            "min_score": "Maxima below this score are dropped first; this does not change which higher maxima are kept.",
        },
        "returns": [("events", "np.ndarray", "Boolean (trace, time) event array.")],
    },
    "metrics.spike_events": {
        "summary": "Binary spike events: score peaks at or above the threshold, or every supra-threshold step when refractory_steps is None.",
        "params": {"scores": "Spike scores, (trace, time).", "threshold": "Event threshold.", "refractory_steps": "Suppression radius; None disables peak detection."},
        "returns": [("events", "np.ndarray", "Boolean (trace, time) event array.")],
    },
    "metrics.prevalence_matched_threshold": {
        "summary": "Threshold at which the number of timesteps scoring at or above it reaches positive_count: the positive_count-th highest score. The evaluator calibrates with this function.",
        "params": {"scores": "Scores of any shape; flattened.", "positive_count": "Target number of positive timesteps."},
        "returns": [("threshold", "float", "The threshold; +inf for a non-positive count and -inf when the count covers every score.")],
    },
    "metrics.event_count_matched_threshold": {
        "summary": "Threshold at which spike_events yields positive_count events.",
        "params": {"scores": "Spike scores, (trace, time).", "positive_count": "Target number of events.", "refractory_steps": "Suppression radius; None matches timesteps instead."},
        "returns": [("threshold", "float", "The height of the positive_count-th highest score peak.")],
    },
    "metrics.spike_event_matches": {
        "summary": "One-to-one event matches under a symmetric timing tolerance. Within each trace, events are paired in time order when they lie within the tolerance, and each event is matched at most once.",
        "params": {"predicted_spikes": "Predicted events, (trace, time).", "target_spikes": "Teacher events of the same shape.", "tolerance_steps": "Non-negative matching tolerance in steps."},
        "returns": [("matches", "np.ndarray", "Integer (matches, 3) array of trace, predicted step, and teacher step.")],
    },
    "metrics.spike_event_confusion": {
        "summary": "One-to-one event confusion under a symmetric timing tolerance. Within each trace, events are paired in time order when they lie within the tolerance; counts are summed over traces.",
        "params": {"predicted_spikes": "Predicted events, (trace, time).", "target_spikes": "Teacher events of the same shape.", "tolerance_steps": "Non-negative matching tolerance in steps."},
        "returns": [("confusion", "dict[str, int]", "tp, fp, and fn.")],
    },
    "metrics.spike_f1_curve": {
        "summary": "Event F1 at each timing tolerance, the arithmetic Mean F1, and the trapezoidal F1 area normalized by the tolerance span.",
        "params": {
            "spike_scores": "Spike scores, (trace, time).",
            "target_spikes": "Teacher spike indicators of the same shape.",
            "threshold": "Event threshold applied to the scores.",
            "tolerances_steps": "Strictly increasing non-negative tolerances.",
            "refractory_steps": "Suppression radius of spike_events.",
        },
        "returns": [("curve", "dict[str, Any]", "threshold, refractory_steps, t_min_steps, t_max_steps, mean_f1, f1_area, and rows with precision, recall, f1, tp, fp, and fn per tolerance.")],
    },
    "metrics.coincidence_factor": {
        "summary": "Coincidence factor Gamma (Kistler et al. 1997; Jolivet et al. 2008): coincidences within the tolerance minus those expected from a Poisson train at the predicted rate, normalized so that a perfect prediction scores 1 and chance about 0.",
        "params": {"predicted_spikes": "Predicted events, (trace, time).", "target_spikes": "Teacher events of the same shape.", "delta_steps": "Coincidence tolerance in steps."},
        "returns": [("result", "dict[str, float | int]", "gamma, coincidences, expected_coincidences, predicted_spikes, target_spikes, and delta_steps.")],
    },
    "metrics.binary_auc": {
        "summary": "Rank-based ROC AUC with averaged tied ranks over all flattened entries.",
        "params": {"scores": "Continuous scores.", "labels": "Binary labels; values above 0.5 are positive."},
        "returns": [("auc", "float", "ROC AUC, or NaN when a class is absent.")],
    },
    "metrics.spike_auc": {
        "summary": "Timestep ROC AUC of channel 0 of a prediction against channel 0 of a target, the historical NeuronIO spike score.",
        "params": {"prediction": "Array whose channel 0 holds spike scores.", "target": "Array whose channel 0 holds spike labels."},
        "returns": [("auc", "float", "ROC AUC.")],
    },
    "metrics.soma_rmse": {
        "summary": "RMSE of channel 1 in the supplied coordinate.",
        "params": {"prediction": "Array whose channel 1 holds soma values.", "target": "Array in the same coordinate."},
        "returns": [("rmse", "float", "Root-mean-square error.")],
    },
    # relevance
    "relevance.iron_relevance": {
        "summary": "IRon default relevance phi of each value, with control points from the reference values: 1 at the lower adjusted-boxplot fence, 0 at the median, 1 at the upper fence, monotone cubic in between and constant beyond.",
        "params": {"target": "Values to score.", "reference": "Values that define the control points; None uses target."},
        "returns": [("relevance", "np.ndarray", "Relevance in [0, 1] with the shape of target.")],
    },
    "relevance.iron_threshold_weights": {
        "summary": "Per-sample weights A(phi) such that iron_sera(e, phi) equals the sum of e**2 * A(phi): the trapezoidal area of the thresholds a sample passes, and 1 for phi >= 1.",
        "params": {"relevance": "Relevance values.", "step": "Threshold grid step."},
        "returns": [("weights", "np.ndarray", "Weights in [0, 1].")],
    },
    "relevance.iron_sera": {
        "summary": "IRon sera: the trapezoidal area over thresholds t of SER(t), the summed squared error of samples with relevance at least t.",
        "params": {"error": "Prediction errors.", "relevance": "Relevance of each sample.", "step": "Threshold grid step."},
        "returns": [("sera", "float", "Squared error-relevance area, not normalized.")],
    },
    "relevance.adjusted_box_fences": {
        "summary": "Lower fence, median, and upper fence of the adjusted boxplot, as robustbase::adjboxStats: Q1 - coef exp(a mc) IQR and Q3 + coef exp(b mc) IQR for mc >= 0, mirrored for mc < 0.",
        "params": {"values": "Sample values; flattened.", "coef": "Whisker coefficient.", "a": "Lower exponent coefficient.", "b": "Upper exponent coefficient."},
        "returns": [("fences", "tuple[float, float, float]", "(lower fence, median, upper fence).")],
    },
    "relevance.medcouple": {
        "summary": "Exact medcouple, a robust skewness measure (Brys, Hubert and Struyf, 2004), computed in O(n log n).",
        "params": {"values": "Sample values; flattened."},
        "returns": [("mc", "float", "Medcouple in [-1, 1]; 0 for fewer than three values or zero spread.")],
    },
    "relevance.fivenum": {
        "summary": "Tukey's five-number summary, as R's fivenum.",
        "params": {"values": "Sample values; flattened. At least one is required."},
        "returns": [("summary", "np.ndarray", "Minimum, lower hinge, median, upper hinge, and maximum.")],
    },
    # data
    "data.ShardedNeuronIODataset": {
        "summary": "Deterministic reader for a directory of shards. With a manifest.json, the index follows the manifest entries whose shards are present; otherwise every *.npz file is read in sorted order. Reading a trace decodes the input array of its whole shard.",
        "params": {
            "root": "Split directory.",
            "shuffle": "Shuffle the index at construction and on reshuffle.",
            "seed": "Seed of the initial shuffle.",
            "shuffle_mode": "'sample' permutes all traces; 'shard' permutes shards and the traces within each shard.",
            "cache_shards": "Decoded shards kept in an LRU cache; 0 disables caching.",
        },
        "methods": {
            "__len__": {"summary": "Number of indexed traces.", "returns": [("count", "int", "Trace count.")]},
            "reshuffle": {"summary": "Reshuffle the index with a new seed; no effect unless shuffle=True.", "params": {"seed": "Shuffle seed."}},
            "__getitem__": {"summary": "Load one trace.", "params": {"index": "Position in the index."}, "returns": [("sample", "NeuronIOSample", "Sample ID, (time, channels) inputs, and (time, 2) targets.")]},
            "get_batch": {"summary": "Load several traces. Consecutive indices from the same shard are read together, so sorted indices minimize shard reads.", "params": {"indices": "Positions in the index."}, "returns": [("inputs", "np.ndarray", "float32 (batch, time, channels)."), ("targets", "np.ndarray", "float32 (batch, time, 2).")]},
            "get_sample_ids": {"summary": "Sample IDs of the given positions.", "params": {"indices": "Positions in the index."}, "returns": [("sample_ids", "list[str]", "Sample IDs in order.")]},
            "get_optional_array_batch": {"summary": "Load an additional per-trace array, such as soma_mv or context_index, from NPZ shards.", "params": {"name": "Array name in the shard.", "indices": "Positions in the index."}, "returns": [("array", "np.ndarray | None", "Concatenated values, or None when a shard lacks the array or is stored as NPY files.")]},
        },
    },
    "data.NeuronIOSample": {
        "summary": "One trace returned by indexing a dataset.",
        "params": {"sample_id": "Sample ID.", "inputs": "Inputs, (time, channels).", "targets": "Targets, (time, 2)."},
    },
    "data.write_demo_shards": {
        "summary": "Write small deterministic shards with random signed events and a synthetic target, for smoke tests only.",
        "params": {"root": "Output directory.", "shard_count": "Number of shards.", "samples_per_shard": "Traces per shard.", "time_steps": "Steps per trace.", "input_dim": "Input channels.", "seed": "Random seed."},
    },
    "data.repack_shards_as_npy": {
        "summary": "Repack shards as separate .npy arrays with a manifest, preserving the trace order, so arrays can be memory-mapped. Raises ValueError if input_dtype would change values.",
        "params": {"input_root": "Source split directory.", "output_root": "Destination directory.", "input_dtype": "Storage dtype of the inputs."},
        "returns": [("paths", "list[Path]", "Written input files.")],
    },
    # selectors
    "benchmark.selectors.V1DatasetLayout": {
        "summary": "Resolver for the v1 layout: <root>/<split> for ordinary splits and <root>/interventions/<name> for conditions.",
        "params": {"root": "Dataset or evaluation root."},
        "methods": {
            "split": {"summary": "Selector for an ordinary split.", "params": {"name": "One of ORDINARY_SPLITS."}, "returns": [("selector", "DatasetSelector", "Split selector.")]},
            "intervention": {"summary": "Selector for an intervention condition; unknown names are accepted if their directory exists.", "params": {"name": "Condition name."}, "returns": [("selector", "DatasetSelector", "Condition selector.")]},
            "default_validation": {"summary": "Selector for val.", "returns": [("selector", "DatasetSelector", "Validation selector.")]},
            "available_interventions": {"summary": "Condition directories present, known conditions first in INTERVENTION_CONDITIONS order.", "returns": [("names", "tuple[str, ...]", "Condition names.")]},
            "validate_minimal": {"summary": "Raise FileNotFoundError unless every ordinary split, and optionally every condition, has a manifest or shards.", "params": {"require_interventions": "Also require the five conditions."}},
        },
    },
    "benchmark.selectors.DatasetSelector": {
        "summary": "A resolved split or intervention directory.",
        "params": {"root": "Directory of the split or condition.", "split": "Split name, or None for a condition.", "condition": "Split name or interventions/<name>.", "intervention": "Condition name, or None for a split."},
        "methods": {"load": {"summary": "Open the directory as a dataset.", "params": {"cache_shards": "Decoded shards kept in memory."}, "returns": [("dataset", "ShardedNeuronIODataset", "Reader for the directory.")]}},
    },
    "benchmark.dataset_schema.v1_morphologies": {
        "summary": "The frozen five-morphology v1 registry.",
        "returns": [("morphologies", "tuple[MorphologySpec, ...]", "Specimen, role, Cre line, and shape ratios per morphology.")],
    },
    "benchmark.dataset_schema.MorphologySpec": {
        "summary": "One registry entry of v1_morphologies; ratios and differences are relative to the reference specimen.",
        "params": {
            "specimen_id": "Allen specimen ID.", "role": "Role in the morphology set.", "swc_path": "SWC path used at generation.",
            "line_name": "Cre line.", "reconstruction_type": "Allen reconstruction type.",
            "compatibility_score_lower_better": "Compatibility score against the reference.",
            "extracted_branches": "Branches extracted from the reconstruction.", "routed_branches": "Branches of the routed representation.",
            "total_length_ratio_vs_reference": "Total dendritic length ratio.", "routed_length_ratio_vs_reference": "Routed length ratio.",
            "apical_fraction_delta_vs_reference": "Apical fraction difference.", "radial_extent_ratio_vs_reference": "Radial extent ratio.",
            "routing_shape_match": "Whether the routed representation matches the reference shape.", "caveat": "Reconstruction caveat.",
        },
    },
    "benchmark.dataset_schema.default_target_views": {
        "summary": "Declared target views: neuronio_clipped_normalized for training and historical comparison, and raw_soma_mv for clipping diagnostics and spike-shape analysis.",
        "returns": [("views", "tuple[TargetViewSpec, ...]", "Target view declarations.")],
    },
    "benchmark.dataset_schema.TargetViewSpec": {
        "summary": "One stored view of the spike and soma target.",
        "params": {"name": "View name.", "columns": "Column names.", "units": "Column units.", "description": "Definition of the view.", "default_for_training": "Whether training uses this view by default.", "default_for_historical_comparison": "Whether historical comparisons use this view."},
    },
    "benchmark.dataset_schema.build_v1_dataset_manifest_template": {
        "summary": "The v1 manifest contract as JSON-like data: categories, morphologies, target views, trace shape, and default diagnostic selectors. Non-training splits hold one eighth of the training traces per morphology.",
        "params": {"morphology_count": "Number of morphologies.", "train_traces_per_morphology": "Training traces per morphology; at least 8."},
        "returns": [("manifest", "dict[str, Any]", "Manifest template.")],
    },
    "benchmark.dataset_schema.validate_v1_manifest_template": {
        "summary": "Validate a manifest against the v1 contract without reading shards; raises ValueError on a mismatch.",
        "params": {"manifest": "Manifest dictionary."},
    },
    "benchmark.dataset_schema.build_diagnostic_suite_catalog": {
        "summary": "Suites, diagnostic specifications with their attached plotters, and the row columns, as printed by axobench dataset-schema --kind diagnostics.",
        "returns": [("catalog", "dict[str, Any]", "suites, diagnostics, plotter_policy, and row_columns.")],
    },
    # interventions
    "benchmark.structured_intervention.make_structured_intervention_inputs": {
        "summary": "Apply one named condition with the released v1 parameters as defaults.",
        "params": {
            "inputs": "Signed inputs, (trace, time, channels) or (time, channels).",
            "intervention": "event_dropout, exc_dropout, inh_dropout, temporal_jitter, or site_silence.",
            "seed": "Seed of the random conditions.",
            "dropout_probability": "Removal probability of the dropout conditions.",
            "jitter_steps": "Maximum absolute shift of temporal_jitter.",
            "site_start_fraction": "Start of the silenced band as a fraction of the sites per sign.",
            "site_fraction": "Width of the silenced band as a fraction of the sites per sign.",
        },
        "returns": [("intervened", "np.ndarray", "Edited inputs."), ("changed", "np.ndarray", "Boolean mask of edited baseline events."), ("metadata", "dict[str, Any]", "Condition parameters and baseline, intervention, and changed event counts.")],
    },
    "benchmark.structured_intervention.make_event_dropout_inputs": {
        "summary": "Remove each nonzero event independently with the given probability.",
        "params": {"inputs": "Signed inputs.", "dropout_probability": "Removal probability in [0, 1].", "seed": "Random seed."},
        "returns": [("intervened", "np.ndarray", "Edited inputs."), ("changed", "np.ndarray", "Mask of removed events.")],
    },
    "benchmark.structured_intervention.make_selective_event_dropout_inputs": {
        "summary": "Remove only excitatory (+1) or only inhibitory (-1) events with the given probability.",
        "params": {"inputs": "Signed inputs.", "dropout_probability": "Removal probability in [0, 1].", "event_sign": "1 for excitatory or -1 for inhibitory events.", "seed": "Random seed."},
        "returns": [("intervened", "np.ndarray", "Edited inputs."), ("changed", "np.ndarray", "Mask of removed events.")],
    },
    "benchmark.structured_intervention.make_temporal_jitter_inputs": {
        "summary": "Move every event by an integer shift drawn uniformly from -max_jitter_steps to +max_jitter_steps, clipped to the trace. Events that land on the same step and channel merge.",
        "params": {"inputs": "Signed inputs.", "max_jitter_steps": "Maximum absolute shift; 0 returns a copy.", "seed": "Random seed."},
        "returns": [("intervened", "np.ndarray", "Edited inputs, (trace, time, channels)."), ("changed", "np.ndarray", "Mask of baseline events that moved.")],
    },
    "benchmark.structured_intervention.make_site_silence_inputs": {
        "summary": "Remove all events on a contiguous band of sites in both the excitatory and the inhibitory half of the channels. The band is a channel range; on a morphology that leaves some sites without a synapse it silences fewer effective synapses.",
        "params": {"inputs": "Signed inputs with excitatory and inhibitory halves.", "start_fraction": "Start of the band as a fraction of the sites per sign.", "site_fraction": "Width of the band as a fraction of the sites per sign; at least one site."},
        "returns": [("intervened", "np.ndarray", "Edited inputs."), ("changed", "np.ndarray", "Mask of removed events.")],
    },
    "benchmark.runner.load_intervention_pair_npz": {
        "summary": "Load the first pairs of a paired intervention shard. The file is opened with allow_pickle=True, so load only trusted files.",
        "params": {"path": "Pair shard.", "max_samples": "Maximum pairs; None loads all."},
        "returns": [("arrays", "tuple", "baseline_inputs, baseline_targets, intervention_inputs, intervention_targets, and the sample IDs.")],
    },
    # neuronio
    "neuronio_raw.convert_neuronio_pickles": {
        "summary": "Convert raw NeuronIO files (*sim__* below input_path, or one file) to shards named neuronio_00000.npz with a manifest. Existing manifest entries in output_dir are kept and new shards are numbered after them.",
        "params": {
            "input_path": "Raw file or directory searched recursively.",
            "output_dir": "Destination directory.",
            "shard_size": "Traces per shard.",
            "window_size": "Optional window length; None keeps whole simulations.",
            "window_stride": "Window stride; defaults to window_size.",
            "ignore_start": "First window start when windowing.",
            "y_soma_threshold": "Clipping level in millivolts.",
            "y_train_soma_bias": "Millivolt bias subtracted after clipping.",
            "y_train_soma_scale": "Scale applied after the bias.",
        },
        "returns": [("paths", "list[Path]", "Written shard files.")],
    },
    "neuronio_raw.parse_neuronio_pickle": {
        "summary": "Parse one raw NeuronIO pickle into dense arrays at 1 ms.",
        "params": {"path": "Raw pickle file."},
        "returns": [("raw", "RawNeuronIO", "Unsigned inputs, spikes, soma voltage, and metadata.")],
    },
    "neuronio_raw.RawNeuronIO": {
        "summary": "Arrays of one raw NeuronIO file.",
        "params": {"inputs": "Unsigned input events (simulation, time, 2 x segments), excitatory segments first.", "spikes": "Output spike indicators, (simulation, time).", "soma": "Soma voltage in millivolts, (simulation, time).", "metadata": "Simulation count, duration, synapse count, segment types, and distances from the soma."},
    },
    "neuronio_raw.normalize_soma": {
        "summary": "Clip at the threshold and normalize: (min(v, threshold) - bias) * scale.",
        "params": {"soma": "Voltage in millivolts.", "threshold": "Clipping level in millivolts.", "bias": "Millivolt bias.", "scale": "Scale after the bias."},
        "returns": [("normalized", "np.ndarray", "float32 target coordinate.")],
    },
    "neuronio_raw.create_neuronio_input_type": {
        "summary": "Channel signs: +1 for the first half and -1 for the second half.",
        "params": {"num_input": "Even channel count."},
        "returns": [("signs", "np.ndarray", "float32 sign per channel.")],
    },
    # defects
    "benchmark.defect_injection.inject_defect": {
        "summary": "Corrupt teacher spikes and voltage with one defect at a dose; dose 0 returns copies.",
        "params": {"spikes": "Binary teacher spikes, (trace, time).", "soma_mv": "Teacher voltage in millivolts, same shape.", "defect": "A key of DEFECTS.", "dose": "Defect strength in the unit of DEFECTS.", "rng": "Random generator for the random defects; None creates an unseeded one."},
        "returns": [("spikes", "np.ndarray", "Corrupted spikes."), ("soma_mv", "np.ndarray", "Corrupted voltage.")],
    },
    "benchmark.defect_injection.defect_dose_rows": {
        "summary": "Score every defect at every dose against the uncorrupted teacher with both the historical NeuronIO scores and the AxoBench scores. Each defect's generator is seeded from seed and the defect name.",
        "params": {"spikes": "Binary teacher spikes, (trace, time).", "soma_mv": "Teacher voltage in millivolts.", "doses": "Doses per defect; None uses DEFAULT_DOSES.", "seed": "Base seed.", "ignore_start": "Initial steps excluded after the defect is applied."},
        "returns": [("rows", "list[dict[str, Any]]", "defect, dose, spike counts, historical_scores fields, and axobench_scores fields per defect and dose.")],
    },
    "benchmark.defect_injection.axobench_scores": {
        "summary": "AxoBench scores of a prediction against unclipped teacher voltage and spikes: Voltage and Dynamics SERA with skill against the per-trace teacher mean, subthreshold RMSE and skill, the F1 curve at 0 to 5 steps with Mean F1, and the coincidence factor at 2 steps. Predicted spikes are used as events directly.",
        "params": {"pred_spikes": "Predicted binary spikes, (trace, time).", "pred_soma_mv": "Predicted voltage in millivolts.", "target_spikes": "Teacher spikes.", "target_soma_mv": "Unclipped teacher voltage in millivolts."},
        "returns": [("scores", "dict[str, Any]", "voltage_sera, voltage_skill, dynamics_sera, dynamics_skill, subthreshold_rmse_mv, subthreshold_skill, f1_curve, mean_f1, and gamma_2.")],
    },
    "benchmark.defect_injection.historical_scores": {
        "summary": "NeuronIO-protocol scores: timestep AUC of the Gaussian-smoothed predicted spike train, and the RMSE of voltages clipped at -55 mV with and without rescaling the prediction to the target's mean and standard deviation.",
        "params": {"pred_spikes": "Predicted binary spikes.", "pred_soma_mv": "Predicted voltage in millivolts.", "target_spikes": "Teacher spikes.", "target_soma_mv": "Teacher voltage in millivolts."},
        "returns": [("scores", "dict[str, float]", "auc, clipped_rmse_aligned_mv, and clipped_rmse_mv.")],
    },
    "benchmark.defect_injection.smoothed_spike_score": {
        "summary": "Spike train smoothed with a Gaussian, used as the ranking score of the historical AUC.",
        "params": {"spikes": "Binary spikes.", "sigma_steps": "Gaussian standard deviation in steps."},
        "returns": [("score", "np.ndarray", "Smoothed score, (trace, time).")],
    },
    # diagnostic rows
    "benchmark.diagnostic_rows.DiagnosticContext": {
        "summary": "Metadata attached to every row and the suites that select rows.",
        "params": {
            "suites": "Suites whose diagnostics are kept.", "model_id": "Model name.", "teacher_id": "Teacher name.",
            "morphology_id": "Morphology label of the rows.", "split": "Split label.", "condition": "Split or interventions/<name>.",
            "intervention": "Condition name.", "trace_id": "Trace label for per-trace rows.", "target_view": "Target view label.",
            "soma_scale": "Scale of the soma target coordinate.", "soma_bias_mv": "Millivolt offset of the soma target coordinate.",
            "ignore_start": "Initial steps excluded.", "calibrated_spike_threshold": "Spike threshold for model rows, calibrated on other traces.",
        },
    },
    "benchmark.diagnostic_rows.evaluate_model_diagnostic_rows": {
        "summary": "Evaluate a model on supplied arrays and return rows for trace fidelity, state-conditioned dynamics, spike behavior, feature fidelity, and mechanistic response.",
        "params": {"inputs": "Inputs, (trace, time, channels).", "targets": "Teacher targets, (trace, time, 2)."},
        "returns": [("rows", "list[dict[str, Any]]", "Rows of the selected suites.")],
    },
    "benchmark.diagnostic_rows.teacher_qc_diagnostic_rows": {
        "summary": "Teacher distribution rows and, with raw voltage, clipping-distortion rows.",
        "params": {"inputs": "Inputs, (trace, time, channels).", "targets": "Teacher targets, (trace, time, 2)."},
        "returns": [("rows", "list[dict[str, Any]]", "Rows of the selected suites.")],
    },
    "benchmark.diagnostic_rows.paired_intervention_diagnostic_rows": {
        "summary": "Teacher response rows for paired inputs and, with a model, model response rows: voltage-change errors, Response SERA, correlation, gain, spike-count deltas, and direction agreement. The model's spike threshold is context.calibrated_spike_threshold, or 0.",
        "params": {"baseline_inputs": "Baseline inputs.", "baseline_targets": "Baseline teacher targets.", "intervention_inputs": "Edited inputs.", "intervention_targets": "Edited teacher targets.", "model_fn": "Optional prediction function; None writes teacher rows only."},
        "returns": [("rows", "list[dict[str, Any]]", "Rows of the selected suites.")],
    },
    "benchmark.diagnostic_rows.morphology_routing_qc_rows": {
        "summary": "Rows of branch counts and shape ratios for the v1 morphology registry.",
        "returns": [("rows", "list[dict[str, Any]]", "Rows with role, Cre line, reconstruction type, SWC path, and caveat.")],
    },
    "benchmark.diagnostic_rows.morphology_contrast_diagnostic_rows": {
        "summary": "Mean, standard deviation, range, minimum, and maximum across morphologies of every numeric metric present for at least min_morphologies morphologies, grouped by diagnostic, metric, state, model, and condition.",
        "params": {"source_rows": "Rows with morphology labels.", "min_morphologies": "Minimum number of morphologies per contrast; at least 2."},
        "returns": [("rows", "list[dict[str, Any]]", "morphology_contrast rows with the per-morphology values attached.")],
    },
    "benchmark.diagnostic_rows.validate_diagnostic_rows": {
        "summary": "Raise ValueError if a row lacks a column of DIAGNOSTIC_ROW_COLUMNS.",
    },
    "benchmark.diagnostic_rows.write_diagnostic_rows": {
        "summary": "Validate and write rows as .json, .jsonl, or .csv.",
        "params": {"path": "Destination ending in .json, .jsonl, or .csv."},
    },
    "benchmark.runner.run_teacher_qc_on_selector": {
        "summary": "Teacher QC rows for the first max_samples traces of a selector, in index order.",
        "params": {"raw_soma_mv": "Optional raw voltage; None reads soma_mv from the shards.", "max_samples": "Maximum traces; None reads all."},
        "returns": [("rows", "list[dict[str, Any]]", "Teacher QC rows.")],
    },
    "benchmark.runner.run_model_diagnostics_on_selector": {
        "summary": "Model diagnostic rows for the first max_samples traces of a selector, with raw voltage when stored.",
        "params": {"max_samples": "Maximum traces; None reads all."},
        "returns": [("rows", "list[dict[str, Any]]", "Model diagnostic rows.")],
    },
    "benchmark.runner.run_paired_intervention_on_selector": {
        "summary": "Paired intervention rows for the first max_samples pairs of a condition directory, across its shards in sorted file order.",
        "params": {"model_fn": "Optional prediction function; None writes teacher rows only.", "max_samples": "Maximum pairs; None reads all."},
        "returns": [("rows", "list[dict[str, Any]]", "Intervention rows.")],
    },
    "benchmark.runner.run_paired_intervention_on_npz": {
        "summary": "Paired intervention rows for one pair file.",
        "params": {"path": "Pair shard.", "model_fn": "Optional prediction function; None writes teacher rows only.", "max_samples": "Maximum pairs; None reads all."},
        "returns": [("rows", "list[dict[str, Any]]", "Intervention rows.")],
    },
    "benchmark.bundle.run_v1_benchmark_bundle": {
        "summary": "Write teacher QC rows for val, morphology routing rows, intervention rows per condition and morphology, morphology-contrast rows, and, with a model, model rows, together with Markdown summaries and a manifest.json.",
        "params": {
            "output_dir": "Directory for the rows, summaries, and manifest.",
            "base_context": "Context copied into every row; its morphology_id labels the val rows.",
            "model_fn": "Optional prediction function; None runs the teacher bundle only.",
            "model_id": "Model name; defaults to base_context.model_id.",
            "intervention_pair_paths": "Explicit pair files; empty discovers every condition under <root>/interventions.",
            "suite": "teacher-qc, paper-summary, or full.",
            "max_val_samples": "Maximum validation traces, read in index order.",
            "max_intervention_samples": "Maximum pairs per condition and morphology.",
            "write_summaries": "Also write a Markdown summary per row file.",
        },
        "returns": [("manifest", "dict[str, Any]", "Settings and the written artifacts with row counts.")],
    },
    "benchmark.reports.summarize_diagnostic_rows": {
        "summary": "Compact summary of rows: counts, diagnostics, suites, models, teachers, morphologies, conditions, example trace IDs, and numeric and label metric summaries.",
        "returns": [("summary", "dict[str, Any]", "JSON-compatible summary.")],
    },
    "benchmark.reports.write_diagnostic_summary": {
        "summary": "Write summarize_diagnostic_rows as Markdown or JSON.",
        "params": {"path": "Destination ending in .md or .json."},
    },
    # error anatomy
    "benchmark.error_anatomy.error_anatomy": {
        "summary": "Break a prediction's errors down on the scored traces of evaluate_predictions, with the same calibration, spike threshold, predicted events, action-potential windows, relevance, and subthreshold masks. Sections: spike events (hits, misses, and false spikes within HIT_TOLERANCE_STEPS, F1 per tolerance, timing errors of matched events), spike-triggered mean voltage of teacher and model around isolated hit, missed, and false spikes, subthreshold error by time since the last and until the next teacher spike (bins 0-5, 5-10, 10-25, 25-50, 50-100, 100+ ms and none), skills by teacher firing rate (0-1, 1-3, 3-6, 6+ Hz) and by morphology, and subthreshold skill by frequency band (0-1, 1-5, 5-10, 10-25, 25-50, 50-100, 100+ Hz).",
        "params": {
            "prediction": "Model outputs shaped (trace, time, 2), in calibration-then-scoring order; at least two traces.",
            "target": "Teacher targets in the same order.",
        },
        "returns": [("anatomy", "dict[str, Any]", "JSON-serializable: config, calibration_samples, scored_samples, spike_threshold, overall, spike_events, spike_triggered_average, subthreshold_by_spike_distance, by_teacher_rate, subthreshold_by_frequency, and by_morphology. Times are in steps or ms and voltages in mV.")],
    },
    "benchmark.error_anatomy.reweight_to_rate_distribution": {
        "summary": "Skills of an error anatomy with its traces reweighted to another distribution over teacher firing-rate bins. Each trace is weighted by the reference share of its bin divided by the bin's own share; bins absent from the reference get weight zero, so the comparison covers the common support. Relevance and references stay those of the anatomy's own block.",
        "params": {
            "anatomy": "Result of error_anatomy to reweight.",
            "reference": "Another error_anatomy result, whose scored-trace shares per rate bin are used, or a mapping from bin label ('0-1', '1-3', '3-6', '6+') to share.",
        },
        "returns": [("skills", "dict[str, Any]", "voltage_sera_skill, voltage_sera_ceiling_skill, voltage_sera_skill_of_ceiling, subthreshold_skill, mean_f1, and the bins used. Raises ValueError when a weighted bin has no traces or no bin is shared.")],
    },
    "benchmark.plots.plot_error_anatomy": {
        "summary": "Plot an error_anatomy result in four panels: spike-triggered voltage of teacher and model around hit, missed, and false spikes; share of retained steps and of squared subthreshold error by time since the last teacher spike; skill by teacher firing rate; and subthreshold skill by frequency band. Uses apply_paper_plot_style.",
        "params": {
            "anatomy": "Result of error_anatomy.",
            "output": "Output path without suffix; each format is written with its own suffix.",
            "formats": "File formats passed to Matplotlib, for example ('pdf', 'png') or ('svg',).",
            "tikz": "Also write a standalone pgfplots .tex file of the same panels.",
        },
        "returns": [("paths", "list[str]", "Written figure paths, followed by the .tex path when tikz is set.")],
    },
    "benchmark.plots.apply_paper_plot_style": {
        "summary": "Set the Matplotlib style of AxoBench figures: STIX serif text at 7 to 8 pt, despined axes without grid, the Okabe-Ito palette, white background, text kept as text in PDF and SVG, and 300 dpi PNG. A style file named by the AXOBENCH_PAPER_STYLE environment variable is applied first.",
    },
}

CONSTANTS = {
    "AP_PRE_STEPS": "Steps before a spike included in its action-potential window.",
    "AP_POST_STEPS": "Fallback window end after a spike.",
    "AP_FLAT_SLOPE_MV_PER_MS": "Slope below which the mean spike waveform counts as flat.",
    "AP_WAVEFORM_PRE_STEPS": "Steps before a spike in the averaged waveform.",
    "AP_ISOLATION_STEPS": "Steps after a spike that must be free of other spikes, and the waveform length after the spike.",
    "AP_MIN_ISOLATED_SPIKES": "Isolated spikes required to estimate a cell type's window end.",
    "SOMA_CLIP_MV": "Clipping level of the subthreshold RMSE and the NeuronIO target, in mV.",
    "ORDINARY_SPLITS": "Ordinary split names of the v1 layout; private-test is not released.",
    "INTERVENTION_CONDITIONS": "Released intervention conditions.",
    "V1_MORPHOLOGY_COUNT": "Morphologies in the v1 single-neuron release.",
    "V1_TRAIN_TRACES_PER_MORPHOLOGY": "Training traces per morphology in v1.",
    "DIAGNOSTIC_SUITES": "Suite names accepted by diagnostic contexts.",
    "DIAGNOSTIC_ROW_COLUMNS": "Columns required in every diagnostic row.",
    "DEFECTS": "Defect names and the unit of their dose.",
    "DEFAULT_DOSES": "Doses scored by defect_dose_rows when none are given.",
    "HIT_TOLERANCE_STEPS": "Timing tolerance in steps within which a predicted spike counts as a hit of a teacher spike.",
    "STA_LAGS_STEPS": "First and last lag of the spike-triggered averages, in steps; events count as isolated when no other event of the same train falls in this window.",
}

CLI_HELP = {
    "make-demo-data": ("Write deterministic synthetic shards for smoke tests.", {
        "output": "Output directory.", "samples": "Traces per shard.", "shards": "Number of shards.", "time_steps": "Steps per trace.", "input_dim": "Input channels.", "seed": "Random seed."}),
    "make-arbor-hetero-data": ("Simulate heterogeneous Arbor cable cells into shards; requires the sim extra (Arbor 0.11).", {
        "config": "JSON file whose keys are option names of this command; explicit flags take precedence.",
        "output": "Output directory; required unless set in --config.",
        "samples": "Traces when --splits is not given.", "shards": "Shards when --splits is not given.",
        "splits": "Comma-separated NAME:SAMPLES pairs written as separate split directories.",
        "shards_per_split": "Shards per split with --splits.", "time_steps": "Steps per trace.", "input_dim": "Input channels.",
        "branches": "Dendritic branches of the cable cell.", "integration_dt_ms": "Simulator integration step in ms.",
        "input_protocol": "Input event generator.", "synapse_routing": "Synapse placement: one site per branch, or distributed sites.",
        "distributed_sites_per_polarity": "Sites per sign with distributed routing.", "spike_label_mode": "How output spikes are labeled.",
        "spike_peak_threshold_mv": "Voltage threshold of spike labels in mV.", "base_event_rate_hz": "Baseline input event rate in Hz.",
        "burst_probability": "Probability of an input burst.", "burst_event_rate_hz": "Input event rate during bursts in Hz.",
        "arbor_gpu_id": "GPU used by Arbor.", "cpu_only": "Use Arbor's CPU context.", "arbor_threads": "Arbor CPU threads.",
        "sim_batch_size": "Independent cells per Arbor simulation.", "seed": "Random seed.",
        "param_overrides": "JSON object, or a path to one, overriding heterogeneity parameters for all traces.",
        "report": "Optional path for a copy of the generation report."}),
    "convert-neuronio": ("Convert raw NeuronIO pickles to deterministic shards.", {
        "input": "Raw file or directory searched for *sim__* files.", "output": "Output directory.", "shard_size": "Traces per shard.",
        "window_size": "Optional window length.", "window_stride": "Window stride; defaults to the window length.", "ignore_start": "First window start when windowing."}),
    "repack-shards": ("Repack shards as sliceable .npy arrays with a manifest.", {
        "input": "Source split directory.", "output": "Destination directory.", "input_dtype": "Storage dtype of the inputs; values must be preserved."}),
    "benchmark-profile": ("Print an axis/default profile as JSON.", {
        "name": "Profile name.", "plan": "Print the expanded axis-composition plan.", "cost": "Print only the local capacity estimate."}),
    "dataset-schema": ("Print the v1 manifest template or the diagnostic suite catalog as JSON.", {
        "kind": "manifest for the template, diagnostics for the suite catalog."}),
    "benchmark-rows": ("Write teacher QC or teacher intervention rows for an evaluation root.", {
        "mode": "teacher-qc rows or intervention rows.", "dataset_root": "Evaluation root.",
        "selector": "Read val or an intervention condition.", "intervention": "Condition name with --selector intervention.",
        "pair_path": "Pair file outside the v1 layout; used with --mode intervention.", "output": "Rows file: .json, .jsonl, or .csv.",
        "summary_output": "Optional summary: .md or .json.", "suites": "Comma-separated suites.", "morphology_id": "Morphology label of the rows.",
        "teacher_id": "Teacher label.", "max_samples": "Maximum traces or pairs, read from the start.", "cache_shards": "Decoded shards kept in memory.",
        "ignore_start": "Initial steps excluded.", "soma_scale": "Scale of the soma target coordinate.", "soma_bias_mv": "Millivolt offset of the soma target coordinate.",
        "calibrated_spike_threshold": "Spike threshold recorded with the rows."}),
    "diagnostic-audits": ("Derive audit rows from saved comparison artifacts.", {
        "teacher_grounded_rows": "Teacher-grounded comparison rows.", "local_stability_rows": "Local stability rows.", "perturbation_rows": "Perturbation rows.",
        "pretrained_summary_rows": "Pretrained-model summary rows.", "teacher_protocol": "Teacher protocol JSON.", "output": "Rows file: .json, .jsonl, or .csv.",
        "summary_output": "Optional summary: .md or .json.", "suites": "Comma-separated audit suites.", "model_id": "Model label.", "teacher_id": "Teacher label.",
        "morphology_id": "Morphology label.", "split": "Split label.", "condition": "Condition label."}),
    "diagnostic-plots": ("Write the audit figures and tables from saved audit summaries.", {
        "canonical_summary": "Canonical audit summary JSON.", "mechanistic_summary": "Mechanistic response summary JSON.", "sparse_event_summary": "Sparse-event sensitivity summary JSON.",
        "point_rows": "Point metric rows.", "tcn_summary": "TCN preprocessing summary JSON; repeatable.", "morphology_contrast_rows": "Optional morphology contrast rows.",
        "neuronio_intervention_rows": "Optional NeuronIO intervention rows.", "neuronio_intervention_root": "Optional NeuronIO intervention directory.",
        "output_dir": "Output directory.", "formats": "Comma-separated figure formats."}),
    "error-anatomy": ("Break a cached prediction's errors down by spike outcome, spike distance, firing rate, frequency band, and morphology; writes error-anatomy.json, the figure, and error-anatomy.tex, and prints the overall skills.", {
        "cache": "Evaluation cache from write_model_evaluation_cache, or any NPZ with a prediction array.",
        "targets": "NPZ with target and optional raw_soma_mv and trace_ids; defaults to the cache file. Must match the cache's target hash and trace IDs when the cache records them.",
        "output": "Output directory.",
        "ignore_start": "Initial steps excluded; defaults to the cache protocol's value, else 500.",
        "calibration_fraction": "Fraction of traces used for threshold calibration; defaults to the cache protocol's value, else 0.25.",
        "formats": "Comma-separated figure formats."}),
    "benchmark-v1": ("Run the teacher bundle on an evaluation root: QC, routing, intervention, and morphology-contrast rows.", {
        "dataset_root": "Evaluation root.", "output_dir": "Output directory.", "suite": "Suite profile.",
        "intervention_pair_glob": "Glob of pair files outside the v1 layout; repeatable.", "morphology_id": "Morphology label of the val rows.",
        "teacher_id": "Teacher label.", "max_val_samples": "Maximum validation traces.", "max_intervention_samples": "Maximum pairs per condition and morphology.",
        "cache_shards": "Decoded shards kept in memory.", "ignore_start": "Initial steps excluded.", "soma_scale": "Scale of the soma target coordinate.",
        "soma_bias_mv": "Millivolt offset of the soma target coordinate.", "calibrated_spike_threshold": "Spike threshold recorded with the rows.",
        "write_summaries": "Write only machine-readable rows and the manifest."}),
}


def anchor(module, owner, name=""):
    return (module.replace(".", "-") + "-" + owner + ("-" + name if name else "")).replace("_", "-").lower()


def source_url(repository, commit, module, node):
    return f"{repository}/blob/{commit}/src/axobench/{module.replace('.', '/')}.py#L{node.lineno}-L{node.end_lineno}"


def module_constants(tree):
    values = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and node.value is not None:
                    try:
                        values[target.id] = ast.literal_eval(node.value)
                    except (ValueError, TypeError, SyntaxError):
                        pass
    return values


def records(args, known):
    positional = args.posonlyargs + args.args
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    result = []
    for p, default in zip(positional, defaults):
        if p.arg in {"self", "cls"}:
            continue
        result.append((p.arg, p.annotation, default, False))
    for p, default in zip(args.kwonlyargs, args.kw_defaults):
        result.append((p.arg, p.annotation, default, True))
    out = []
    for name, annotation, default, keyword in result:
        shown = None
        if default is not None:
            shown = ast.unparse(default)
            if isinstance(default, ast.Name) and default.id in known:
                shown += " = " + repr(known[default.id])
        out.append({"name": name, "type": ast.unparse(annotation) if annotation else "unannotated", "default": shown, "keyword": keyword})
    return out


def parameter_list(params, descriptions, context):
    if not params:
        return []
    lines = ['<p class="api-label">Parameters</p>', "", '<dl class="api-parameters">']
    for p in params:
        text = descriptions.get(p["name"]) or COMMON.get(p["name"])
        if not text:
            raise SystemExit(f"undocumented parameter {context}.{p['name']}")
        qualifiers = (["keyword-only"] if p["keyword"] else []) + (["required"] if p["default"] is None else ["default=" + p["default"]])
        lines.append(f'<dt><code>{escape(p["name"])}</code> <span class="api-type">{escape(p["type"])}</span></dt>')
        lines.append(f'<dd><span class="api-default">{escape(", ".join(qualifiers))}.</span> {escape(text)}</dd>')
    lines.extend(["</dl>", ""])
    return lines


def returns_list(doc, node):
    if node is None or node.returns is None or ast.unparse(node.returns) == "None":
        return []
    entries = doc.get("returns")
    if not entries:
        raise SystemExit(f"undocumented return of {node.name}")
    lines = ['<p class="api-label">Returns</p>', "", '<dl class="api-parameters">']
    for name, typename, text in entries:
        lines.append(f'<dt><code>{escape(name)}</code> <span class="api-type">{escape(typename)}</span></dt>')
        lines.append(f"<dd>{escape(text)}</dd>")
    lines.extend(["</dl>", ""])
    return lines


def signature_block(text, url):
    return ['<div class="api-signature">', "", "```python", text, "```", "", f"[Source]({url})", "", "</div>", ""]


def function_doc(module, node, known, repository, commit, exports, owner=None, doc=None):
    key = f"{module}.{owner + '.' if owner else ''}{node.name}"
    doc = doc if doc is not None else DOCS.get(key)
    if doc is None:
        raise SystemExit(f"undocumented symbol {key}")
    args = node.args
    display_args = ast.unparse(args)
    if owner:
        trimmed = ast.parse(f"def f({display_args}): pass").body[0].args
        if trimmed.args and trimmed.args[0].arg in {"self", "cls"}:
            trimmed.args.pop(0)
        display_args = ast.unparse(trimmed)
    qualified = f"axobench.{module}.{owner + '.' if owner else ''}{node.name}"
    signature = f"{qualified}({display_args})" + (f" -> {ast.unparse(node.returns)}" if node.returns else "")
    css = "api-method" if owner else "api-symbol"
    level = "###" if owner else "##"
    lines = [f'<section class="{css}" id="{anchor(module, owner or node.name, node.name if owner else "")}">', "", f"{level} {(owner + '.') if owner else ''}{node.name}", ""]
    lines.extend(signature_block(signature, source_url(repository, commit, module, node)))
    summary = doc["summary"]
    if not owner and node.name in exports:
        summary += f" Exported from `axobench.benchmark`."
    lines.extend([summary, ""])
    lines.extend(parameter_list(records(args, known), doc.get("params", {}), key))
    lines.extend(returns_list(doc, node))
    lines.extend(["</section>", ""])
    return lines


def class_doc(module, node, known, repository, commit, exports):
    key = f"{module}.{node.name}"
    doc = DOCS.get(key)
    if doc is None:
        raise SystemExit(f"undocumented symbol {key}")
    init = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == "__init__"), None)
    if init is not None:
        trimmed = ast.parse(f"def f({ast.unparse(init.args)}): pass").body[0].args
        trimmed.args.pop(0)
        params = records(trimmed, known)
        signature = f"axobench.{module}.{node.name}({ast.unparse(trimmed)})"
    else:
        fields = [n for n in node.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)]
        parts, params = [], []
        for f in fields:
            default = ast.unparse(f.value) if f.value is not None else None
            if isinstance(f.value, ast.Name) and f.value.id in known:
                default += " = " + repr(known[f.value.id])
            parts.append(f"{f.target.id}: {ast.unparse(f.annotation)}" + (f" = {ast.unparse(f.value)}" if f.value is not None else ""))
            params.append({"name": f.target.id, "type": ast.unparse(f.annotation), "default": default, "keyword": False})
        signature = f"axobench.{module}.{node.name}({', '.join(parts)})"
    lines = [f'<section class="api-symbol" id="{anchor(module, node.name)}">', "", f"## {node.name}", ""]
    lines.extend(signature_block(signature, source_url(repository, commit, module, node)))
    summary = doc["summary"] + (" Exported from `axobench.benchmark`." if node.name in exports else "")
    lines.extend([summary, ""])
    lines.extend(parameter_list(params, doc.get("params", {}), key))
    frozen = any(isinstance(d, ast.Call) and any(k.arg == "frozen" for k in d.keywords) for d in node.decorator_list)
    if init is None:
        lines.extend(['<p class="api-label">Attributes</p>', "", "Constructor fields are retained as " + ("read-only attributes." if frozen else "attributes."), ""])
    methods = doc.get("methods", {})
    method_nodes = [n for n in node.body if isinstance(n, ast.FunctionDef) and n.name in methods]
    missing = set(methods) - {n.name for n in method_nodes}
    if missing:
        raise SystemExit(f"missing methods {key}: {missing}")
    if method_nodes:
        lines.extend(['<p class="api-label">Methods</p>', "", '<ul class="api-method-list">'])
        for m in method_nodes:
            lines.append(f'<li><a href="#{anchor(module, node.name, m.name)}"><code>{escape(node.name + "." + m.name)}()</code></a></li>')
        lines.extend(["</ul>", ""])
        for m in method_nodes:
            lines.extend(function_doc(module, m, known, repository, commit, exports, owner=node.name, doc=methods[m.name]))
    lines.extend(["</section>", ""])
    return lines


def constants_doc(module, names, tree, known, repository, commit):
    nodes = {}
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    nodes[target.id] = node
    lines = [f'<section class="api-symbol" id="{anchor(module, "constants")}">', "", "## Constants", "", '<dl class="api-attributes">']
    for name in names:
        node = nodes[name]
        value = known.get(name)
        if isinstance(value, dict):
            shown = "{" + ", ".join(repr(k) for k in value) + "}"
        else:
            shown = repr(value)
        lines.append(f'<dt id="{anchor(module, name)}"><code>{escape(name)} = {escape(shown)}</code></dt>')
        lines.append(f'<dd>{escape(CONSTANTS[name])} <a href="{source_url(repository, commit, module, node)}">Source</a></dd>')
    lines.extend(["</dl>", "", "</section>", ""])
    return lines


def front_matter(title, description, order, group=None):
    lines = ["---", f"title: {title}", f"description: {description}", f"section: {SECTION}"]
    if group:
        lines.append(f"apiGroup: {group}")
    lines.extend([f"order: {order}", "---", ""])
    return lines


def capture_cli(source):
    sys.path.insert(0, str(source / "src"))
    import axobench.cli as cli

    class Captured(Exception):
        pass

    captured = {}
    original = argparse.ArgumentParser.parse_args

    def capture(self, args=None, namespace=None):
        captured["parser"] = self
        raise Captured

    argparse.ArgumentParser.parse_args = capture
    try:
        cli.main(["make-demo-data", "--output", "unused"])
    except Captured:
        pass
    finally:
        argparse.ArgumentParser.parse_args = original
    parser = captured["parser"]
    sub = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))
    return sub.choices


def cli_page(source, repository, commit):
    commands = capture_cli(source)
    tree_text = (source / "src/axobench/cli.py").read_text()
    lines = front_matter("axobench CLI", "Every subcommand, option, and default of the axobench command.", 320, "CLI")
    lines.extend(["## Usage", "", "```bash", "axobench <command> --help", "```", "",
                  "The `axobench` command converts and inspects data and writes diagnostic rows; it does not load models. AxoSim checkpoints are evaluated with [`axosim-evaluate-model`](/api/axobench-cli/), and other models through the [Python evaluator](/axobench-api/evaluation/). Errors in file paths or values exit with status 2 and print the message.", ""])
    if set(commands) != set(CLI_HELP):
        raise SystemExit(f"CLI commands differ: {sorted(set(commands) ^ set(CLI_HELP))}")
    for name, parser in commands.items():
        summary, options = CLI_HELP[name]
        match = re.search(r"add_parser\(\s*\"" + re.escape(name) + "\"", tree_text)
        line = tree_text.count("\n", 0, match.start()) + 1
        lines.extend([f"## {name}", "", summary, "", '<p class="api-label">Options</p>', "", '<dl class="api-parameters">'])
        for action in parser._actions:
            if isinstance(action, argparse._HelpAction):
                continue
            flags = ", ".join(action.option_strings) or action.dest
            if isinstance(action, argparse._StoreTrueAction):
                typename, detail = "flag", "default=False"
            elif isinstance(action, argparse._StoreFalseAction):
                typename, detail = "flag", "default=True"
            else:
                typename = getattr(action.type, "__name__", "str") if action.type else "str"
                detail = "required" if action.required else "default=" + repr(action.default)
            if isinstance(action, argparse._AppendAction):
                typename += ", repeatable"
            text = options.get(action.dest)
            if not text:
                raise SystemExit(f"undocumented option {name} {flags}")
            if action.choices:
                text += " Choices: " + ", ".join(map(str, action.choices)) + "."
            lines.append(f'<dt><code>{escape(flags)}</code> <span class="api-type">{escape(typename)}</span> · {escape(detail)}</dt>')
            lines.append(f"<dd>{escape(text)}</dd>")
        lines.extend(["</dl>", "", f"[Parser source]({repository}/blob/{commit}/src/axobench/cli.py#L{line})", ""])
    return "\n".join(lines)


def exports_of(source):
    tree = ast.parse((source / "src/axobench/benchmark/__init__.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "_EXPORTS":
            return {key: tuple(value) for key, value in ast.literal_eval(node.value).items()}
    raise SystemExit("axobench.benchmark exports not found")


def index_page(exports, documented, version, commit, repository):
    lines = front_matter("AxoBench API", "Public AxoBench functions, classes, constants, and command-line options.", 300)
    lines.extend([
        "## Package surface", "",
        f"This reference covers AxoBench {version} at revision `{commit[:12]}`. Model evaluation, paired comparison, and diagnostics are exported lazily from `axobench.benchmark`; metrics, relevance, data readers, defect injection, and NeuronIO conversion are imported from their modules. The package needs NumPy and imports no model framework.", "",
        "```python",
        "from axobench.benchmark import evaluate_model, evaluate_model_against_cache",
        "from axobench.metrics import compute_core_metric_set",
        "from axobench.data import ShardedNeuronIODataset",
        "```", "",
        "## Exports of axobench.benchmark", "",
        "| Name | Implementation | Reference |", "| --- | --- | --- |",
    ])
    for name in sorted(exports):
        module, attribute = exports[name]
        module = module.removeprefix("axobench.")
        page = documented.get((module, attribute))
        if page:
            link = f"[Open](/axobench-api/{page}/#{anchor(module, attribute)})"
        else:
            link = f"[Source]({repository}/blob/{commit}/src/axobench/{module.replace('.', '/')}.py)"
        lines.append(f"| `{name}` | `axobench.{module}.{attribute}` | {link} |")
    lines.extend(["", "Exports marked Source link to their module. They include the combined BenchmarkSuite, benchmark profiles and cost models, branch adapters, morphology transfer, population dynamics, state, regime, trace-shape, and perturbation metrics, artifact audits, and comparison tables. They are part of the package but outside the evaluation protocol documented in this reference.", "",
                  "## Modules", ""])
    for page in PAGES:
        lines.append(f"- [{page['title']}](/axobench-api/{page['slug']}/)")
    lines.extend(["- [axobench CLI](/axobench-api/cli/)", "", "## Source", "",
                  f"Every source link is pinned to [revision {commit[:12]}]({repository}/tree/{commit}). Repository access is currently required to open the source links. The generator reads signatures and defaults with AST parsing and the CLI options from the argparse parser.", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT.parent / "AxoBench")
    parser.add_argument("--output", type=Path, default=ROOT / "src/content/docs")
    parser.add_argument("--repository", default="https://github.com/Axym-Labs/axobench")
    args = parser.parse_args()
    source = args.source.resolve()
    commit = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    pyproject = (source / "pyproject.toml").read_text()
    version = next(line.split("=", 1)[1].strip().strip('"') for line in pyproject.splitlines() if line.startswith("version"))
    exports = exports_of(source)
    export_names = {attribute for _, attribute in exports.values()}
    trees = {}
    documented = {}
    out_dir = args.output / "axobench-api"
    out_dir.mkdir(parents=True, exist_ok=True)
    for page in PAGES:
        lines = front_matter(page["title"], f"Signatures, parameters, return values, and source for {page['title'][0].lower() + page['title'][1:]}.", page["order"], page["group"])
        lines.extend(["## Overview", "", page["overview"], "", f"Source revision: `{commit[:12]}`. [Export index](/axobench-api/).", ""])
        for item in page["items"]:
            if item[0] == "const":
                _, module, names = item
            else:
                module, name = item
            if module not in trees:
                trees[module] = ast.parse((source / "src/axobench" / (module.replace(".", "/") + ".py")).read_text())
            tree = trees[module]
            # Defaults imported from the NeuronIO module are resolved as well.
            known = {**module_constants(ast.parse((source / "src/axobench/neuronio_raw.py").read_text())), **module_constants(tree)}
            if item[0] == "const":
                lines.extend(constants_doc(module, names, tree, known, args.repository, commit))
                documented.update({(module, constant): page["slug"] for constant in names})
                continue
            node = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name), None)
            if node is None:
                raise SystemExit(f"missing symbol {module}.{name}")
            documented[(module, name)] = page["slug"]
            if isinstance(node, ast.ClassDef):
                lines.extend(class_doc(module, node, known, args.repository, commit, export_names))
            else:
                lines.extend(function_doc(module, node, known, args.repository, commit, export_names))
        (out_dir / f"{page['slug']}.md").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "cli.md").write_text(cli_page(source, args.repository, commit), encoding="utf-8")
    (args.output / "axobench-api.md").write_text(index_page(exports, documented, version, commit, args.repository), encoding="utf-8")
    print(f"Generated {len(PAGES) + 2} AxoBench reference pages for {version} at {commit[:12]}; {len(documented)} documented symbols.")


if __name__ == "__main__":
    main()
