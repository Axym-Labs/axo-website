---
title: Model evaluation
description: Signatures, parameters, return values, and source for model evaluation.
section: AxoBench API
apiGroup: Evaluation
order: 301
---

## Overview

The model-iteration evaluator selects validation traces and intervention pairs, calls a prediction function in batches, calibrates the spike threshold on a held-out block, and returns a fixed report of metrics and 24 attention rows. evaluate_predictions applies the same protocol to stored arrays. The guide [Benchmarking with AxoBench](/axobench/benchmarking/) describes the protocol.

Source revision: `22e52ec6c023`. [Export index](/axobench-api/).

<section class="api-symbol" id="benchmark-iteration-evaluator-evaluationconfig">

## EvaluationConfig

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.EvaluationConfig(soma_scale: float = 0.1, soma_bias_mv: float = -67.7, ignore_start: int = 500, timestep_ms: float = 1.0, calibration_fraction: float = 0.25, default_spike_threshold: float = 0.5, f1_tolerances_steps: tuple[int, ...] = (0, 1, 2, 3, 4, 5), selected_f1_steps: tuple[int, int] = (0, 5), physiological_voltage_bounds_mv: tuple[float, float] = (-120.0, 60.0), physiological_slew_bound_mv_per_ms: float = 120.0, refractory_period_ms: float = 2.0, state_error_ratio_watch: float = 1.1, state_error_floor_mv: float = 0.5)
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/iteration_evaluator.py#L109-L141)

</div>

Frozen settings of the metric protocol and attention thresholds. Its fields are part of every cache protocol, so paired comparisons require equal configurations. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span> Scale of the soma target coordinate.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=-67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=500.</span> Initial timesteps excluded from every metric and diagnostic.</dd>
<dt><code>timestep_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=1.0.</span> Duration of one timestep in milliseconds.</dd>
<dt><code>calibration_fraction</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.25.</span> Share of traces, in (0, 1), used only to calibrate the spike threshold.</dd>
<dt><code>default_spike_threshold</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.5.</span> Uncalibrated threshold checked by the default_threshold_count attention row; it does not set the scoring threshold.</dd>
<dt><code>f1_tolerances_steps</code> <span class="api-type">tuple[int, ...]</span></dt>
<dd><span class="api-default">default=(0, 1, 2, 3, 4, 5).</span> Timing tolerances of the F1 curve in steps; Mean F1 averages over them.</dd>
<dt><code>selected_f1_steps</code> <span class="api-type">tuple[int, int]</span></dt>
<dd><span class="api-default">default=(0, 5).</span> Tolerances reported as spike_f1_exact and spike_f1_5ms; both must be in f1_tolerances_steps.</dd>
<dt><code>physiological_voltage_bounds_mv</code> <span class="api-type">tuple[float, float]</span></dt>
<dd><span class="api-default">default=(-120.0, 60.0).</span> Envelope of the voltage_bounds attention row.</dd>
<dt><code>physiological_slew_bound_mv_per_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=120.0.</span> One-step slope bound of the voltage_slew attention row.</dd>
<dt><code>refractory_period_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=2.0.</span> Minimum inter-spike interval of the refractory_violations attention row.</dd>
<dt><code>state_error_ratio_watch</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=1.1.</span> State-to-overall RMSE ratio that triggers a state attention row.</dd>
<dt><code>state_error_floor_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.5.</span> Minimum state RMSE for a state attention row to trigger.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-pairedinterventionpredictions">

## PairedInterventionPredictions

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.PairedInterventionPredictions(name: str, baseline_prediction: np.ndarray, intervention_prediction: np.ndarray, baseline_target: np.ndarray, intervention_target: np.ndarray, baseline_raw_soma_mv: np.ndarray | None = None, intervention_raw_soma_mv: np.ndarray | None = None, morphology_ids: list[str] | np.ndarray | None = None)
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/iteration_evaluator.py#L145-L155)

</div>

Predictions and teacher traces for one intervention condition, used for Response SERA and the intervention attention rows. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Condition name reported with the results.</dd>
<dt><code>baseline_prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs for the baseline inputs, (pair, time, 2).</dd>
<dt><code>intervention_prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs for the edited inputs, (pair, time, 2).</dd>
<dt><code>baseline_target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets for the baseline inputs.</dd>
<dt><code>intervention_target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets for the edited inputs.</dd>
<dt><code>baseline_raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">default=None.</span> Optional unclipped baseline teacher voltage in millivolts.</dd>
<dt><code>intervention_raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">default=None.</span> Optional unclipped intervention teacher voltage in millivolts.</dd>
<dt><code>morphology_ids</code> <span class="api-type">list[str] | np.ndarray | None</span></dt>
<dd><span class="api-default">default=None.</span> Optional morphology per pair, used to stratify the paired bootstrap.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-evaluate-model">

## evaluate_model

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.evaluate_model(model_fn: Callable[[np.ndarray], np.ndarray], *, dataset_root: str | Path, model_id: str='model', max_samples: int | None=None, batch_size: int=DEFAULT_BATCH_SIZE, max_intervention_samples: int | None=None, max_interventions: int=8, intervention_workers: int=DEFAULT_INTERVENTION_WORKERS, intervention_names: Iterable[str] | None=None, multiple_morphologies: bool=False, morphology_id: str | None=None, validation_sample_start: int=0, cache_shards: int=1, config: EvaluationConfig | None=None) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/iteration_evaluator.py#L172-L298)

</div>

Run batched inference on an evaluation root and return the evaluation report. Selected traces are reordered round-robin by morphology before calibration, so the calibration block covers every selected morphology. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model_fn</code> <span class="api-type">Callable[[np.ndarray], np.ndarray]</span></dt>
<dd><span class="api-default">required.</span> Prediction function mapping float32 inputs (batch, time, 1278) to (batch, time, 2) outputs: a spike score and the soma target coordinate. With supports_morphology_ids=True it is called with a morphology_ids keyword.</dd>
<dt><code>dataset_root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Evaluation root containing val/ and optionally interventions/&lt;condition&gt;/.</dd>
<dt><code>model_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;model&#x27;.</span> Model name in the report.</dd>
<dt><code>max_samples</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Validation traces to select; None uses default_iteration_sample_limits (120).</dd>
<dt><code>batch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=DEFAULT_BATCH_SIZE = 128.</span> Traces per prediction call.</dd>
<dt><code>max_intervention_samples</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Pairs per intervention condition; None uses the default of 40.</dd>
<dt><code>max_interventions</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=8.</span> Maximum number of condition directories read, in sorted order.</dd>
<dt><code>intervention_workers</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=DEFAULT_INTERVENTION_WORKERS = 4.</span> Threads that load intervention shards in parallel.</dd>
<dt><code>intervention_names</code> <span class="api-type">Iterable[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Condition directory names to evaluate; None discovers all. A missing name raises FileNotFoundError.</dd>
<dt><code>multiple_morphologies</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Balance traces and pairs across all morphologies instead of using one.</dd>
<dt><code>morphology_id</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Morphology for single-morphology mode; None uses the alphabetically first. Cannot be combined with multiple_morphologies=True.</dd>
<dt><code>validation_sample_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Start of the selected block within the morphology, or within the balanced order in multiple-morphology mode.</dd>
<dt><code>cache_shards</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Decoded shards kept in memory by the reader.</dd>
<dt><code>config</code> <span class="api-type">EvaluationConfig | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Evaluation settings; None uses EvaluationConfig().</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>report</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>The evaluate_predictions report plus evaluation_seconds, morphology_mode, morphology_ids, standard_sample_limit, intervention_sample_limit_per_condition, validation_sample_start, and sample_profile.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-evaluate-predictions">

## evaluate_predictions

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.evaluate_predictions(prediction: np.ndarray, target: np.ndarray, *, inputs: np.ndarray | None=None, raw_soma_mv: np.ndarray | None=None, trace_ids: list[str] | None=None, interventions: Iterable[PairedInterventionPredictions]=(), config: EvaluationConfig | None=None, model_id: str='model') -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/iteration_evaluator.py#L612-L800)

</div>

Evaluate stored predictions. The first round(calibration_fraction * traces) traces, at least one and at most all but one, calibrate the spike threshold by prevalence matching; all metrics and diagnostics use the remaining traces. At least two traces are required. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs shaped (trace, time, 2), in calibration-then-scoring order.</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets in the same order.</dd>
<dt><code>inputs</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional per-step input summary shaped (trace, time, channels); its absolute sum per step is the input load of the low-input and post-burst diagnostics. Excitatory and inhibitory event counts suffice.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher soma voltage in millivolts, shaped (trace, time); replaces the voltage reconstructed from the target.</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
<dt><code>interventions</code> <span class="api-type">Iterable[PairedInterventionPredictions]</span></dt>
<dd><span class="api-default">keyword-only, default=().</span> Per-condition paired predictions for Response SERA and the intervention rows.</dd>
<dt><code>config</code> <span class="api-type">EvaluationConfig | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Evaluation settings; None uses EvaluationConfig().</dd>
<dt><code>model_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;model&#x27;.</span> Model name in the report.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>report</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>model_id, samples, calibration_samples, scored_samples, spike_threshold, spike_f1_curve, subthreshold_ap_window, metrics (id, value, unit, meaning, core), diagnostics (24 rows with area, id, attention, value, unit, primary, trigger, basis), and interventions.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-default-iteration-sample-limits">

## default_iteration_sample_limits

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.default_iteration_sample_limits(*, multiple_morphologies: bool=False) -> tuple[int, int]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/iteration_evaluator.py#L597-L609)

</div>

Default ordinary and per-condition intervention sample limits for a morphology mode. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>multiple_morphologies</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Select the multiple-morphology defaults.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>limits</code> <span class="api-type">tuple[int, int]</span></dt>
<dd>(120, 40) in both modes.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-format-evaluation-report">

## format_evaluation_report

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.format_evaluation_report(report: dict[str, Any]) -> str
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/iteration_evaluator.py#L1188-L1249)

</div>

Render the bounded plain-text report: header, core and secondary metrics, action-potential window ends, and the attention panel with its summary line. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>report</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Report returned by evaluate_model or evaluate_predictions.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>text</code> <span class="api-type">str</span></dt>
<dd>Deterministic plain-text report.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-write-evaluation-report">

## write_evaluation_report

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.write_evaluation_report(report: dict[str, Any], path: str | Path) -> Path
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/iteration_evaluator.py#L1263-L1305)

</div>

Write a report as strict JSON or tidy CSV, selected by the suffix; non-finite values become null or empty. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>report</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Report to write.</dd>
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Destination ending in .json or .csv; parent directories are created.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">Path</span></dt>
<dd>The written path.</dd>
</dl>

</section>
