---
title: Diagnostic rows
description: Signatures, parameters, return values, and source for diagnostic rows.
section: AxoBench API
apiGroup: Diagnostics
order: 311
---

## Overview

Dataframe-first diagnostic rows for teacher QC, model diagnostics, paired interventions, morphology routing, and morphology contrasts, with runners that read an evaluation root and a bundle that writes all of them. Every row carries the columns in DIAGNOSTIC_ROW_COLUMNS. A row is kept when its diagnostic belongs to one of the suites in the context. See [diagnostics](/axobench/diagnostics/).

Source revision: `496e0c1a2dfd`. [Export index](/axobench-api/).

<section class="api-symbol" id="benchmark-diagnostic-rows-diagnosticcontext">

## DiagnosticContext

<div class="api-signature">

```python
axobench.benchmark.diagnostic_rows.DiagnosticContext(suites: tuple[str, ...] = ('paper-summary',), model_id: str = DEFAULT_MODEL_ID, teacher_id: str = DEFAULT_TEACHER_ID, morphology_id: str = 'unknown', split: str = 'val', condition: str = 'val', intervention: str | None = None, trace_id: str | None = None, target_view: str = 'neuronio_clipped_normalized', soma_scale: float = 0.1, soma_bias_mv: float = DEFAULT_Y_TRAIN_SOMA_BIAS, ignore_start: int = 500, calibrated_spike_threshold: float | None = None)
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/diagnostic_rows.py#L31-L46)

</div>

Metadata attached to every row and the suites that select rows. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>suites</code> <span class="api-type">tuple[str, ...]</span></dt>
<dd><span class="api-default">default=(&#x27;paper-summary&#x27;,).</span> Suites whose diagnostics are kept.</dd>
<dt><code>model_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=DEFAULT_MODEL_ID = &#x27;model&#x27;.</span> Model name.</dd>
<dt><code>teacher_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=DEFAULT_TEACHER_ID = &#x27;teacher&#x27;.</span> Teacher name.</dd>
<dt><code>morphology_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;unknown&#x27;.</span> Morphology label of the rows.</dd>
<dt><code>split</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;val&#x27;.</span> Split label.</dd>
<dt><code>condition</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;val&#x27;.</span> Split or interventions/&lt;name&gt;.</dd>
<dt><code>intervention</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">default=None.</span> Condition name.</dd>
<dt><code>trace_id</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">default=None.</span> Trace label for per-trace rows.</dd>
<dt><code>target_view</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;neuronio_clipped_normalized&#x27;.</span> Target view label.</dd>
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span> Scale of the soma target coordinate.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=DEFAULT_Y_TRAIN_SOMA_BIAS = -67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=500.</span> Initial steps excluded.</dd>
<dt><code>calibrated_spike_threshold</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span> Spike threshold for model rows, calibrated on other traces.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="benchmark-diagnostic-rows-evaluate-model-diagnostic-rows">

## evaluate_model_diagnostic_rows

<div class="api-signature">

```python
axobench.benchmark.diagnostic_rows.evaluate_model_diagnostic_rows(model_fn: Callable[[np.ndarray], np.ndarray], inputs: np.ndarray, targets: np.ndarray, *, context: DiagnosticContext | None=None, trace_ids: list[str] | None=None, raw_soma_mv: np.ndarray | None=None) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/diagnostic_rows.py#L49-L103)

</div>

Evaluate a model on supplied arrays and return rows for trace fidelity, state-conditioned dynamics, spike behavior, feature fidelity, and mechanistic response. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model_fn</code> <span class="api-type">Callable[[np.ndarray], np.ndarray]</span></dt>
<dd><span class="api-default">required.</span> Prediction function mapping float32 inputs (batch, time, 1278) to (batch, time, 2) outputs: a spike score and the soma target coordinate. With supports_morphology_ids=True it is called with a morphology_ids keyword.</dd>
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Inputs, (trace, time, channels).</dd>
<dt><code>targets</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets, (trace, time, 2).</dd>
<dt><code>context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Row metadata and suite selection; None uses the function&#x27;s default context.</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher soma voltage in millivolts, shaped (trace, time); replaces the voltage reconstructed from the target.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>Rows of the selected suites.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-diagnostic-rows-teacher-qc-diagnostic-rows">

## teacher_qc_diagnostic_rows

<div class="api-signature">

```python
axobench.benchmark.diagnostic_rows.teacher_qc_diagnostic_rows(inputs: np.ndarray, targets: np.ndarray, *, context: DiagnosticContext | None=None, raw_soma_mv: np.ndarray | None=None, trace_ids: list[str] | None=None) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/diagnostic_rows.py#L170-L185)

</div>

Teacher distribution rows and, with raw voltage, clipping-distortion rows. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Inputs, (trace, time, channels).</dd>
<dt><code>targets</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets, (trace, time, 2).</dd>
<dt><code>context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Row metadata and suite selection; None uses the function&#x27;s default context.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher soma voltage in millivolts, shaped (trace, time); replaces the voltage reconstructed from the target.</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>Rows of the selected suites.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-diagnostic-rows-paired-intervention-diagnostic-rows">

## paired_intervention_diagnostic_rows

<div class="api-signature">

```python
axobench.benchmark.diagnostic_rows.paired_intervention_diagnostic_rows(baseline_inputs: np.ndarray, baseline_targets: np.ndarray, intervention_inputs: np.ndarray, intervention_targets: np.ndarray, *, model_fn: Callable[[np.ndarray], np.ndarray] | None=None, context: DiagnosticContext | None=None, trace_ids: list[str] | None=None) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/diagnostic_rows.py#L188-L291)

</div>

Teacher response rows for paired inputs and, with a model, model response rows: voltage-change errors, Response SERA, correlation, gain, spike-count deltas, and direction agreement. The model's spike threshold is context.calibrated_spike_threshold, or 0. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>baseline_inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Baseline inputs.</dd>
<dt><code>baseline_targets</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Baseline teacher targets.</dd>
<dt><code>intervention_inputs</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Edited inputs.</dd>
<dt><code>intervention_targets</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Edited teacher targets.</dd>
<dt><code>model_fn</code> <span class="api-type">Callable[[np.ndarray], np.ndarray] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional prediction function; None writes teacher rows only.</dd>
<dt><code>context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Row metadata and suite selection; None uses the function&#x27;s default context.</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>Rows of the selected suites.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-diagnostic-rows-morphology-routing-qc-rows">

## morphology_routing_qc_rows

<div class="api-signature">

```python
axobench.benchmark.diagnostic_rows.morphology_routing_qc_rows(*, context: DiagnosticContext | None=None) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/diagnostic_rows.py#L385-L432)

</div>

Rows of branch counts and shape ratios for the v1 morphology registry. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Row metadata and suite selection; None uses the function&#x27;s default context.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>Rows with role, Cre line, reconstruction type, SWC path, and caveat.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-diagnostic-rows-morphology-contrast-diagnostic-rows">

## morphology_contrast_diagnostic_rows

<div class="api-signature">

```python
axobench.benchmark.diagnostic_rows.morphology_contrast_diagnostic_rows(source_rows: Iterable[dict[str, Any]], *, context: DiagnosticContext | None=None, min_morphologies: int=2) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/diagnostic_rows.py#L294-L382)

</div>

Mean, standard deviation, range, minimum, and maximum across morphologies of every numeric metric present for at least min_morphologies morphologies, grouped by diagnostic, metric, state, model, and condition. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>source_rows</code> <span class="api-type">Iterable[dict[str, Any]]</span></dt>
<dd><span class="api-default">required.</span> Rows with morphology labels.</dd>
<dt><code>context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Row metadata and suite selection; None uses the function&#x27;s default context.</dd>
<dt><code>min_morphologies</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Minimum number of morphologies per contrast; at least 2.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>morphology_contrast rows with the per-morphology values attached.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-diagnostic-rows-validate-diagnostic-rows">

## validate_diagnostic_rows

<div class="api-signature">

```python
axobench.benchmark.diagnostic_rows.validate_diagnostic_rows(rows: Iterable[dict[str, Any]]) -> None
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/diagnostic_rows.py#L435-L443)

</div>

Raise ValueError if a row lacks a column of DIAGNOSTIC_ROW_COLUMNS. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">Iterable[dict[str, Any]]</span></dt>
<dd><span class="api-default">required.</span> Diagnostic row dictionaries.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-diagnostic-rows-write-diagnostic-rows">

## write_diagnostic_rows

<div class="api-signature">

```python
axobench.benchmark.diagnostic_rows.write_diagnostic_rows(rows: Iterable[dict[str, Any]], path: str | Path) -> None
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/diagnostic_rows.py#L446-L471)

</div>

Validate and write rows as .json, .jsonl, or .csv. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">Iterable[dict[str, Any]]</span></dt>
<dd><span class="api-default">required.</span> Diagnostic row dictionaries.</dd>
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Destination ending in .json, .jsonl, or .csv.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-runner-run-teacher-qc-on-selector">

## run_teacher_qc_on_selector

<div class="api-signature">

```python
axobench.benchmark.runner.run_teacher_qc_on_selector(selector: DatasetSelector, *, context: DiagnosticContext | None=None, raw_soma_mv: np.ndarray | None=None, max_samples: int | None=None, output: str | Path | None=None, cache_shards: int=1) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/runner.py#L215-L238)

</div>

Teacher QC rows for the first max_samples traces of a selector, in index order. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>selector</code> <span class="api-type">DatasetSelector</span></dt>
<dd><span class="api-default">required.</span> Resolved split or intervention directory from V1DatasetLayout.</dd>
<dt><code>context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Row metadata and suite selection; None uses the function&#x27;s default context.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional raw voltage; None reads soma_mv from the shards.</dd>
<dt><code>max_samples</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Maximum traces; None reads all.</dd>
<dt><code>output</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional .json, .jsonl, or .csv path for the rows.</dd>
<dt><code>cache_shards</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Decoded shards kept in memory by the reader.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>Teacher QC rows.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-runner-run-model-diagnostics-on-selector">

## run_model_diagnostics_on_selector

<div class="api-signature">

```python
axobench.benchmark.runner.run_model_diagnostics_on_selector(model_fn: Callable[[np.ndarray], np.ndarray], selector: DatasetSelector, *, context: DiagnosticContext | None=None, max_samples: int | None=None, output: str | Path | None=None, cache_shards: int=1) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/runner.py#L64-L93)

</div>

Model diagnostic rows for the first max_samples traces of a selector, with raw voltage when stored. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model_fn</code> <span class="api-type">Callable[[np.ndarray], np.ndarray]</span></dt>
<dd><span class="api-default">required.</span> Prediction function mapping float32 inputs (batch, time, 1278) to (batch, time, 2) outputs: a spike score and the soma target coordinate. With supports_morphology_ids=True it is called with a morphology_ids keyword.</dd>
<dt><code>selector</code> <span class="api-type">DatasetSelector</span></dt>
<dd><span class="api-default">required.</span> Resolved split or intervention directory from V1DatasetLayout.</dd>
<dt><code>context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Row metadata and suite selection; None uses the function&#x27;s default context.</dd>
<dt><code>max_samples</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Maximum traces; None reads all.</dd>
<dt><code>output</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional .json, .jsonl, or .csv path for the rows.</dd>
<dt><code>cache_shards</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Decoded shards kept in memory by the reader.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>Model diagnostic rows.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-runner-run-paired-intervention-on-selector">

## run_paired_intervention_on_selector

<div class="api-signature">

```python
axobench.benchmark.runner.run_paired_intervention_on_selector(selector: DatasetSelector, *, model_fn: Callable[[np.ndarray], np.ndarray] | None=None, context: DiagnosticContext | None=None, max_samples: int | None=None, output: str | Path | None=None) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/runner.py#L123-L159)

</div>

Paired intervention rows for the first max_samples pairs of a condition directory, across its shards in sorted file order. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>selector</code> <span class="api-type">DatasetSelector</span></dt>
<dd><span class="api-default">required.</span> Resolved split or intervention directory from V1DatasetLayout.</dd>
<dt><code>model_fn</code> <span class="api-type">Callable[[np.ndarray], np.ndarray] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional prediction function; None writes teacher rows only.</dd>
<dt><code>context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Row metadata and suite selection; None uses the function&#x27;s default context.</dd>
<dt><code>max_samples</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Maximum pairs; None reads all.</dd>
<dt><code>output</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional .json, .jsonl, or .csv path for the rows.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>Intervention rows.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-runner-run-paired-intervention-on-npz">

## run_paired_intervention_on_npz

<div class="api-signature">

```python
axobench.benchmark.runner.run_paired_intervention_on_npz(path: str | Path, *, model_fn: Callable[[np.ndarray], np.ndarray] | None=None, context: DiagnosticContext | None=None, max_samples: int | None=None, output: str | Path | None=None) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/runner.py#L96-L120)

</div>

Paired intervention rows for one pair file. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Pair shard.</dd>
<dt><code>model_fn</code> <span class="api-type">Callable[[np.ndarray], np.ndarray] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional prediction function; None writes teacher rows only.</dd>
<dt><code>context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Row metadata and suite selection; None uses the function&#x27;s default context.</dd>
<dt><code>max_samples</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Maximum pairs; None reads all.</dd>
<dt><code>output</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional .json, .jsonl, or .csv path for the rows.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>Intervention rows.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-bundle-run-v1-benchmark-bundle">

## run_v1_benchmark_bundle

<div class="api-signature">

```python
axobench.benchmark.bundle.run_v1_benchmark_bundle(*, dataset_root: str | Path, output_dir: str | Path, base_context: DiagnosticContext | None=None, model_fn: Callable[[np.ndarray], np.ndarray] | None=None, model_id: str | None=None, intervention_pair_paths: Iterable[str | Path]=(), suite: SuiteProfile='paper-summary', max_val_samples: int | None=None, max_intervention_samples: int | None=None, cache_shards: int=1, write_summaries: bool=True) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/bundle.py#L43-L207)

</div>

Write teacher QC rows for val, morphology routing rows, intervention rows per condition and morphology, morphology-contrast rows, and, with a model, model rows, together with Markdown summaries and a manifest.json. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>dataset_root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Evaluation root containing val/ and optionally interventions/&lt;condition&gt;/.</dd>
<dt><code>output_dir</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Directory for the rows, summaries, and manifest.</dd>
<dt><code>base_context</code> <span class="api-type">DiagnosticContext | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Context copied into every row; its morphology_id labels the val rows.</dd>
<dt><code>model_fn</code> <span class="api-type">Callable[[np.ndarray], np.ndarray] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional prediction function; None runs the teacher bundle only.</dd>
<dt><code>model_id</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Model name; defaults to base_context.model_id.</dd>
<dt><code>intervention_pair_paths</code> <span class="api-type">Iterable[str | Path]</span></dt>
<dd><span class="api-default">keyword-only, default=().</span> Explicit pair files; empty discovers every condition under &lt;root&gt;/interventions.</dd>
<dt><code>suite</code> <span class="api-type">SuiteProfile</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;paper-summary&#x27;.</span> teacher-qc, paper-summary, or full.</dd>
<dt><code>max_val_samples</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Maximum validation traces, read in index order.</dd>
<dt><code>max_intervention_samples</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Maximum pairs per condition and morphology.</dd>
<dt><code>cache_shards</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Decoded shards kept in memory by the reader.</dd>
<dt><code>write_summaries</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Also write a Markdown summary per row file.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>manifest</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>Settings and the written artifacts with row counts.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-reports-summarize-diagnostic-rows">

## summarize_diagnostic_rows

<div class="api-signature">

```python
axobench.benchmark.reports.summarize_diagnostic_rows(rows: list[dict[str, Any]]) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/reports.py#L15-L32)

</div>

Compact summary of rows: counts, diagnostics, suites, models, teachers, morphologies, conditions, example trace IDs, and numeric and label metric summaries. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd><span class="api-default">required.</span> Diagnostic row dictionaries.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>summary</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>JSON-compatible summary.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-reports-write-diagnostic-summary">

## write_diagnostic_summary

<div class="api-signature">

```python
axobench.benchmark.reports.write_diagnostic_summary(rows: list[dict[str, Any]], path: str | Path) -> None
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/reports.py#L35-L48)

</div>

Write summarize_diagnostic_rows as Markdown or JSON. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd><span class="api-default">required.</span> Diagnostic row dictionaries.</dd>
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Destination ending in .md or .json.</dd>
</dl>

</section>
