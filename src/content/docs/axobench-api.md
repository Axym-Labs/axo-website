---
title: AxoBench API
description: Public AxoBench functions, classes, constants, and command-line options.
section: AxoBench API
order: 300
---

## Package surface

This reference covers AxoBench 0.2.0 at revision `22e52ec6c023`. Model evaluation, paired comparison, and diagnostics are exported lazily from `axobench.benchmark`; metrics, relevance, data readers, defect injection, and NeuronIO conversion are imported from their modules. The package needs NumPy and imports no model framework.

```python
from axobench.benchmark import evaluate_model, evaluate_model_against_cache
from axobench.metrics import compute_core_metric_set
from axobench.data import ShardedNeuronIODataset
```

## Exports of axobench.benchmark

| Name | Implementation | Reference |
| --- | --- | --- |
| `BenchmarkCostModel` | `axobench.benchmark.profiles.BenchmarkCostModel` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/profiles.py) |
| `BenchmarkProfile` | `axobench.benchmark.profiles.BenchmarkProfile` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/profiles.py) |
| `BenchmarkSuite` | `axobench.benchmark.suite.BenchmarkSuite` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/suite.py) |
| `DIAGNOSTIC_SUITES` | `axobench.benchmark.dataset_schema.DIAGNOSTIC_SUITES` | [Open](/axobench-api/layout/#benchmark-dataset-schema-diagnostic-suites) |
| `DatasetSelector` | `axobench.benchmark.selectors.DatasetSelector` | [Open](/axobench-api/layout/#benchmark-selectors-datasetselector) |
| `DiagnosticAuditSources` | `axobench.benchmark.diagnostic_audits.DiagnosticAuditSources` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/diagnostic_audits.py) |
| `DiagnosticContext` | `axobench.benchmark.diagnostic_rows.DiagnosticContext` | [Open](/axobench-api/diagnostics/#benchmark-diagnostic-rows-diagnosticcontext) |
| `EvaluationConfig` | `axobench.benchmark.iteration_evaluator.EvaluationConfig` | [Open](/axobench-api/evaluation/#benchmark-iteration-evaluator-evaluationconfig) |
| `INTERVENTION_CONDITIONS` | `axobench.benchmark.dataset_schema.INTERVENTION_CONDITIONS` | [Open](/axobench-api/layout/#benchmark-dataset-schema-intervention-conditions) |
| `LOCAL_CORENEURON_HAY_COST_MODEL` | `axobench.benchmark.profiles.LOCAL_CORENEURON_HAY_COST_MODEL` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/profiles.py) |
| `ModelEvaluationCache` | `axobench.benchmark.iteration_evaluator.ModelEvaluationCache` | [Open](/axobench-api/comparison/#benchmark-iteration-evaluator-modelevaluationcache) |
| `MorphologyTransferEvaluator` | `axobench.benchmark.morphology_transfer.MorphologyTransferEvaluator` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/morphology_transfer.py) |
| `ORDINARY_SPLITS` | `axobench.benchmark.dataset_schema.ORDINARY_SPLITS` | [Open](/axobench-api/layout/#benchmark-dataset-schema-ordinary-splits) |
| `PairedInterventionPredictions` | `axobench.benchmark.iteration_evaluator.PairedInterventionPredictions` | [Open](/axobench-api/evaluation/#benchmark-iteration-evaluator-pairedinterventionpredictions) |
| `PopulationDynamicsConfig` | `axobench.benchmark.population_dynamics.PopulationDynamicsConfig` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/population_dynamics.py) |
| `V1DatasetLayout` | `axobench.benchmark.selectors.V1DatasetLayout` | [Open](/axobench-api/layout/#benchmark-selectors-v1datasetlayout) |
| `V1_MORPHOLOGY_COUNT` | `axobench.benchmark.dataset_schema.V1_MORPHOLOGY_COUNT` | [Open](/axobench-api/layout/#benchmark-dataset-schema-v1-morphology-count) |
| `adapt_branch_count` | `axobench.benchmark.branch_adapter.adapt_branch_count` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/branch_adapter.py) |
| `adapter_fairness_diagnostic_rows` | `axobench.benchmark.diagnostic_audits.adapter_fairness_diagnostic_rows` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/diagnostic_audits.py) |
| `analyze_population_perturbation` | `axobench.benchmark.population_dynamics.analyze_population_perturbation` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/population_dynamics.py) |
| `analyze_population_spikes` | `axobench.benchmark.population_dynamics.analyze_population_spikes` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/population_dynamics.py) |
| `build_axis_plan` | `axobench.benchmark.profiles.build_axis_plan` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/profiles.py) |
| `build_diagnostic_suite_catalog` | `axobench.benchmark.dataset_schema.build_diagnostic_suite_catalog` | [Open](/axobench-api/layout/#benchmark-dataset-schema-build-diagnostic-suite-catalog) |
| `build_neuron_state_masks` | `axobench.benchmark.state_metrics.build_neuron_state_masks` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/state_metrics.py) |
| `build_v1_dataset_manifest_template` | `axobench.benchmark.dataset_schema.build_v1_dataset_manifest_template` | [Open](/axobench-api/layout/#benchmark-dataset-schema-build-v1-dataset-manifest-template) |
| `compare_predictions` | `axobench.benchmark.iteration_evaluator.compare_predictions` | [Open](/axobench-api/comparison/#benchmark-iteration-evaluator-compare-predictions) |
| `compute_paired_event_intervention_metrics` | `axobench.benchmark.structured_intervention.compute_paired_event_intervention_metrics` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/structured_intervention.py) |
| `compute_perturbation_stability` | `axobench.benchmark.perturbation_stability.compute_perturbation_stability` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/perturbation_stability.py) |
| `compute_regime_stratified_metrics` | `axobench.benchmark.regime_stratified.compute_regime_stratified_metrics` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/regime_stratified.py) |
| `compute_state_conditioned_metrics` | `axobench.benchmark.state_metrics.compute_state_conditioned_metrics` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/state_metrics.py) |
| `compute_trace_shape_metrics` | `axobench.benchmark.trace_shape.compute_trace_shape_metrics` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/trace_shape.py) |
| `core_metric_comparison_rows` | `axobench.benchmark.reports.core_metric_comparison_rows` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/reports.py) |
| `create_model_evaluation_cache` | `axobench.benchmark.iteration_evaluator.create_model_evaluation_cache` | [Open](/axobench-api/comparison/#benchmark-iteration-evaluator-create-model-evaluation-cache) |
| `default_diagnostic_specs` | `axobench.benchmark.dataset_schema.default_diagnostic_specs` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py) |
| `default_iteration_sample_limits` | `axobench.benchmark.iteration_evaluator.default_iteration_sample_limits` | [Open](/axobench-api/evaluation/#benchmark-iteration-evaluator-default-iteration-sample-limits) |
| `default_target_views` | `axobench.benchmark.dataset_schema.default_target_views` | [Open](/axobench-api/layout/#benchmark-dataset-schema-default-target-views) |
| `diagnostic_audit_rows` | `axobench.benchmark.diagnostic_audits.diagnostic_audit_rows` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/diagnostic_audits.py) |
| `diagnostic_audit_rows_from_sources` | `axobench.benchmark.diagnostic_audits.diagnostic_audit_rows_from_sources` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/diagnostic_audits.py) |
| `estimate_profile_cost` | `axobench.benchmark.profiles.estimate_profile_cost` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/profiles.py) |
| `evaluate_model` | `axobench.benchmark.iteration_evaluator.evaluate_model` | [Open](/axobench-api/evaluation/#benchmark-iteration-evaluator-evaluate-model) |
| `evaluate_model_against_cache` | `axobench.benchmark.iteration_evaluator.evaluate_model_against_cache` | [Open](/axobench-api/comparison/#benchmark-iteration-evaluator-evaluate-model-against-cache) |
| `evaluate_model_diagnostic_rows` | `axobench.benchmark.diagnostic_rows.evaluate_model_diagnostic_rows` | [Open](/axobench-api/diagnostics/#benchmark-diagnostic-rows-evaluate-model-diagnostic-rows) |
| `evaluate_predictions` | `axobench.benchmark.iteration_evaluator.evaluate_predictions` | [Open](/axobench-api/evaluation/#benchmark-iteration-evaluator-evaluate-predictions) |
| `evaluate_with_branch_adaptation` | `axobench.benchmark.branch_adapter.evaluate_with_branch_adaptation` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/branch_adapter.py) |
| `format_evaluation_report` | `axobench.benchmark.iteration_evaluator.format_evaluation_report` | [Open](/axobench-api/evaluation/#benchmark-iteration-evaluator-format-evaluation-report) |
| `format_model_comparison` | `axobench.benchmark.iteration_evaluator.format_model_comparison` | [Open](/axobench-api/comparison/#benchmark-iteration-evaluator-format-model-comparison) |
| `get_benchmark_profile` | `axobench.benchmark.profiles.get_benchmark_profile` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/profiles.py) |
| `infer_pair_metadata` | `axobench.benchmark.bundle.infer_pair_metadata` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/bundle.py) |
| `list_benchmark_profiles` | `axobench.benchmark.profiles.list_benchmark_profiles` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/profiles.py) |
| `load_artifact_rows` | `axobench.benchmark.diagnostic_audits.load_artifact_rows` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/diagnostic_audits.py) |
| `load_available_morphologies` | `axobench.benchmark.morphology_transfer.load_available_morphologies` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/morphology_transfer.py) |
| `load_intervention_pair_npz` | `axobench.benchmark.runner.load_intervention_pair_npz` | [Open](/axobench-api/interventions/#benchmark-runner-load-intervention-pair-npz) |
| `load_model_evaluation_cache` | `axobench.benchmark.iteration_evaluator.load_model_evaluation_cache` | [Open](/axobench-api/comparison/#benchmark-iteration-evaluator-load-model-evaluation-cache) |
| `load_selector_batch` | `axobench.benchmark.runner.load_selector_batch` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/runner.py) |
| `make_event_dropout_inputs` | `axobench.benchmark.structured_intervention.make_event_dropout_inputs` | [Open](/axobench-api/interventions/#benchmark-structured-intervention-make-event-dropout-inputs) |
| `make_selective_event_dropout_inputs` | `axobench.benchmark.structured_intervention.make_selective_event_dropout_inputs` | [Open](/axobench-api/interventions/#benchmark-structured-intervention-make-selective-event-dropout-inputs) |
| `make_site_silence_inputs` | `axobench.benchmark.structured_intervention.make_site_silence_inputs` | [Open](/axobench-api/interventions/#benchmark-structured-intervention-make-site-silence-inputs) |
| `make_structured_intervention_inputs` | `axobench.benchmark.structured_intervention.make_structured_intervention_inputs` | [Open](/axobench-api/interventions/#benchmark-structured-intervention-make-structured-intervention-inputs) |
| `make_temporal_jitter_inputs` | `axobench.benchmark.structured_intervention.make_temporal_jitter_inputs` | [Open](/axobench-api/interventions/#benchmark-structured-intervention-make-temporal-jitter-inputs) |
| `metric_decoupling_diagnostic_rows` | `axobench.benchmark.diagnostic_audits.metric_decoupling_diagnostic_rows` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/diagnostic_audits.py) |
| `morphology_contrast_diagnostic_rows` | `axobench.benchmark.diagnostic_rows.morphology_contrast_diagnostic_rows` | [Open](/axobench-api/diagnostics/#benchmark-diagnostic-rows-morphology-contrast-diagnostic-rows) |
| `morphology_routing_qc_rows` | `axobench.benchmark.diagnostic_rows.morphology_routing_qc_rows` | [Open](/axobench-api/diagnostics/#benchmark-diagnostic-rows-morphology-routing-qc-rows) |
| `multistep_branching_ratio` | `axobench.benchmark.population_dynamics.multistep_branching_ratio` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/population_dynamics.py) |
| `paired_intervention_diagnostic_rows` | `axobench.benchmark.diagnostic_rows.paired_intervention_diagnostic_rows` | [Open](/axobench-api/diagnostics/#benchmark-diagnostic-rows-paired-intervention-diagnostic-rows) |
| `protocol_coverage_diagnostic_rows` | `axobench.benchmark.diagnostic_audits.protocol_coverage_diagnostic_rows` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/diagnostic_audits.py) |
| `provisional_v1_morphologies` | `axobench.benchmark.dataset_schema.provisional_v1_morphologies` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py) |
| `robustness_directionality_diagnostic_rows` | `axobench.benchmark.diagnostic_audits.robustness_directionality_diagnostic_rows` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/diagnostic_audits.py) |
| `run_model_diagnostics_on_selector` | `axobench.benchmark.runner.run_model_diagnostics_on_selector` | [Open](/axobench-api/diagnostics/#benchmark-runner-run-model-diagnostics-on-selector) |
| `run_paired_intervention_on_npz` | `axobench.benchmark.runner.run_paired_intervention_on_npz` | [Open](/axobench-api/diagnostics/#benchmark-runner-run-paired-intervention-on-npz) |
| `run_paired_intervention_on_selector` | `axobench.benchmark.runner.run_paired_intervention_on_selector` | [Open](/axobench-api/diagnostics/#benchmark-runner-run-paired-intervention-on-selector) |
| `run_teacher_qc_on_selector` | `axobench.benchmark.runner.run_teacher_qc_on_selector` | [Open](/axobench-api/diagnostics/#benchmark-runner-run-teacher-qc-on-selector) |
| `run_v1_benchmark_bundle` | `axobench.benchmark.bundle.run_v1_benchmark_bundle` | [Open](/axobench-api/diagnostics/#benchmark-bundle-run-v1-benchmark-bundle) |
| `summarize_diagnostic_rows` | `axobench.benchmark.reports.summarize_diagnostic_rows` | [Open](/axobench-api/diagnostics/#benchmark-reports-summarize-diagnostic-rows) |
| `target_view_audit_diagnostic_rows` | `axobench.benchmark.diagnostic_audits.target_view_audit_diagnostic_rows` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/diagnostic_audits.py) |
| `teacher_qc_diagnostic_rows` | `axobench.benchmark.diagnostic_rows.teacher_qc_diagnostic_rows` | [Open](/axobench-api/diagnostics/#benchmark-diagnostic-rows-teacher-qc-diagnostic-rows) |
| `v1_morphologies` | `axobench.benchmark.dataset_schema.v1_morphologies` | [Open](/axobench-api/layout/#benchmark-dataset-schema-v1-morphologies) |
| `validate_diagnostic_rows` | `axobench.benchmark.diagnostic_rows.validate_diagnostic_rows` | [Open](/axobench-api/diagnostics/#benchmark-diagnostic-rows-validate-diagnostic-rows) |
| `validate_v1_manifest_template` | `axobench.benchmark.dataset_schema.validate_v1_manifest_template` | [Open](/axobench-api/layout/#benchmark-dataset-schema-validate-v1-manifest-template) |
| `write_core_metric_comparison_table` | `axobench.benchmark.reports.write_core_metric_comparison_table` | [Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/reports.py) |
| `write_diagnostic_rows` | `axobench.benchmark.diagnostic_rows.write_diagnostic_rows` | [Open](/axobench-api/diagnostics/#benchmark-diagnostic-rows-write-diagnostic-rows) |
| `write_diagnostic_summary` | `axobench.benchmark.reports.write_diagnostic_summary` | [Open](/axobench-api/diagnostics/#benchmark-reports-write-diagnostic-summary) |
| `write_evaluation_report` | `axobench.benchmark.iteration_evaluator.write_evaluation_report` | [Open](/axobench-api/evaluation/#benchmark-iteration-evaluator-write-evaluation-report) |
| `write_model_comparison` | `axobench.benchmark.iteration_evaluator.write_model_comparison` | [Open](/axobench-api/comparison/#benchmark-iteration-evaluator-write-model-comparison) |
| `write_model_evaluation_cache` | `axobench.benchmark.iteration_evaluator.write_model_evaluation_cache` | [Open](/axobench-api/comparison/#benchmark-iteration-evaluator-write-model-evaluation-cache) |

Exports marked Source link to their module. They include the combined BenchmarkSuite, benchmark profiles and cost models, branch adapters, morphology transfer, population dynamics, state, regime, trace-shape, and perturbation metrics, artifact audits, and comparison tables. They are part of the package but outside the evaluation protocol documented in this reference.

## Modules

- [Model evaluation](/axobench-api/evaluation/)
- [Paired comparison](/axobench-api/comparison/)
- [Core metric functions](/axobench-api/metrics/)
- [Spike event metrics](/axobench-api/spike-metrics/)
- [IRon relevance](/axobench-api/relevance/)
- [Trace datasets](/axobench-api/data/)
- [Dataset layout and schema](/axobench-api/layout/)
- [Intervention inputs](/axobench-api/interventions/)
- [NeuronIO conversion](/axobench-api/neuronio/)
- [Defect injection](/axobench-api/defect-injection/)
- [Diagnostic rows](/axobench-api/diagnostics/)
- [axobench CLI](/axobench-api/cli/)

## Source

Every source link is pinned to [revision 22e52ec6c023](https://github.com/Axym-Labs/axobench/tree/22e52ec6c0230edccf608076a9a1cdfd0011d5d8). Repository access is currently required to open the source links. The generator reads signatures and defaults with AST parsing and the CLI options from the argparse parser.
