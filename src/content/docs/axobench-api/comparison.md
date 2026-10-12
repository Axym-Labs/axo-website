---
title: Paired comparison
description: Signatures, parameters, return values, and source for paired comparison.
section: AxoBench API
apiGroup: Evaluation
order: 302
---

## Overview

A baseline cache freezes one model's predictions together with the trace selection, target hash, and protocol. Candidates are compared against it on identical traces with a morphology-stratified paired bootstrap; see [compare with a baseline](/axobench/benchmarking/#compare-with-a-baseline).

Source revision: `496e0c1a2dfd`. [Export index](/axobench-api/).

<section class="api-symbol" id="benchmark-iteration-evaluator-modelevaluationcache">

## ModelEvaluationCache

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.ModelEvaluationCache(model_id: str, report: dict[str, Any], prediction: np.ndarray, trace_ids: tuple[str, ...], target_sha256: str, interventions: tuple[PairedInterventionPredictions, ...], protocol: dict[str, Any], source_path: Path | None = None)
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/iteration_evaluator.py#L172-L182)

</div>

A frozen baseline: predictions, intervention predictions, trace selection, target hash, report, and protocol. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Baseline name.</dd>
<dt><code>report</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Baseline evaluation report.</dd>
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Baseline outputs for the selected traces, in report order.</dd>
<dt><code>trace_ids</code> <span class="api-type">tuple[str, ...]</span></dt>
<dd><span class="api-default">required.</span> Ordered sample IDs of the selected traces.</dd>
<dt><code>target_sha256</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> SHA-256 of the target array, including dtype and shape.</dd>
<dt><code>interventions</code> <span class="api-type">tuple[PairedInterventionPredictions, ...]</span></dt>
<dd><span class="api-default">required.</span> Baseline predictions and teacher traces per condition.</dd>
<dt><code>protocol</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Sample limits, morphology selection, intervention names, sample start, and EvaluationConfig fields.</dd>
<dt><code>source_path</code> <span class="api-type">Path | None</span></dt>
<dd><span class="api-default">default=None.</span> File the cache was loaded from, if any.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-create-model-evaluation-cache">

## create_model_evaluation_cache

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.create_model_evaluation_cache(model_fn: Callable[[np.ndarray], np.ndarray], *, dataset_root: str | Path, model_id: str='baseline', max_samples: int | None=None, batch_size: int=DEFAULT_BATCH_SIZE, max_intervention_samples: int | None=None, max_interventions: int=8, intervention_workers: int=DEFAULT_INTERVENTION_WORKERS, intervention_names: Iterable[str] | None=None, multiple_morphologies: bool=False, morphology_id: str | None=None, validation_sample_start: int=0, cache_shards: int=1, config: EvaluationConfig | None=None) -> ModelEvaluationCache
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/iteration_evaluator.py#L314-L393)

</div>

Evaluate a baseline once and retain everything needed to compare later candidates on the same traces. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model_fn</code> <span class="api-type">Callable[[np.ndarray], np.ndarray]</span></dt>
<dd><span class="api-default">required.</span> Prediction function mapping float32 inputs (batch, time, 1278) to (batch, time, 2) outputs: a spike score and the soma target coordinate. With supports_morphology_ids=True it is called with a morphology_ids keyword.</dd>
<dt><code>dataset_root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Evaluation root containing val/ and optionally interventions/&lt;condition&gt;/.</dd>
<dt><code>model_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;baseline&#x27;.</span> Baseline name stored in the cache and report.</dd>
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
<dt><code>cache</code> <span class="api-type">ModelEvaluationCache</span></dt>
<dd>Baseline predictions, report, trace IDs, target hash, interventions, and protocol.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-write-model-evaluation-cache">

## write_model_evaluation_cache

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.write_model_evaluation_cache(cache: ModelEvaluationCache, path: str | Path) -> Path
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/iteration_evaluator.py#L501-L550)

</div>

Write a cache as a compressed, pickle-free NPZ file with JSON metadata. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>cache</code> <span class="api-type">ModelEvaluationCache</span></dt>
<dd><span class="api-default">required.</span> Cache to write.</dd>
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Destination ending in .npz; parent directories are created.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">Path</span></dt>
<dd>The written path.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-load-model-evaluation-cache">

## load_model_evaluation_cache

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.load_model_evaluation_cache(path: str | Path) -> ModelEvaluationCache
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/iteration_evaluator.py#L553-L607)

</div>

Load a cache written by write_model_evaluation_cache, without pickle. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Cache file.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>cache</code> <span class="api-type">ModelEvaluationCache</span></dt>
<dd>The cache, with source_path set.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-evaluate-model-against-cache">

## evaluate_model_against_cache

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.evaluate_model_against_cache(candidate_model_fn: Callable[[np.ndarray], np.ndarray], *, baseline_cache: ModelEvaluationCache | str | Path, dataset_root: str | Path, candidate_id: str='candidate', max_samples: int | None=None, batch_size: int=DEFAULT_BATCH_SIZE, max_intervention_samples: int | None=None, max_interventions: int=8, intervention_workers: int=DEFAULT_INTERVENTION_WORKERS, intervention_names: Iterable[str] | None=None, multiple_morphologies: bool=False, morphology_id: str | None=None, validation_sample_start: int=0, cache_shards: int=1, config: EvaluationConfig | None=None, bootstrap_replicates: int=250, bootstrap_seed: int=20260711) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/iteration_evaluator.py#L396-L498)

</div>

Evaluate a candidate and compare it with a cached baseline. Raises ValueError unless the protocol, ordered trace IDs, and target hash match the cache. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>candidate_model_fn</code> <span class="api-type">Callable[[np.ndarray], np.ndarray]</span></dt>
<dd><span class="api-default">required.</span> Candidate prediction function, with the same contract as model_fn of evaluate_model.</dd>
<dt><code>baseline_cache</code> <span class="api-type">ModelEvaluationCache | str | Path</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Cache object or path to a cache file.</dd>
<dt><code>dataset_root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Evaluation root containing val/ and optionally interventions/&lt;condition&gt;/.</dd>
<dt><code>candidate_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;candidate&#x27;.</span> Candidate name in the comparison.</dd>
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
<dt><code>bootstrap_replicates</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=250.</span> Paired bootstrap replicates.</dd>
<dt><code>bootstrap_seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=20260711.</span> Seed of the paired bootstrap.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>comparison</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>The compare_predictions result plus evaluation_seconds and baseline_cache, the cache path.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-compare-predictions">

## compare_predictions

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.compare_predictions(candidate_prediction: np.ndarray, baseline_prediction: np.ndarray, target: np.ndarray, *, inputs: np.ndarray | None=None, raw_soma_mv: np.ndarray | None=None, trace_ids: list[str] | None=None, candidate_interventions: Iterable[PairedInterventionPredictions]=(), baseline_interventions: Iterable[PairedInterventionPredictions]=(), config: EvaluationConfig | None=None, candidate_id: str='candidate', baseline_id: str='baseline', baseline_report: dict[str, Any] | None=None, bootstrap_replicates: int=250, seed: int=20260711) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/iteration_evaluator.py#L846-L969)

</div>

Compare two models on the same traces. Scored traces are resampled within each morphology; each model keeps its calibrated threshold, and relevance weights and action-potential windows stay at their full-sample values. Intervals are the 2.5% and 97.5% quantiles of the replicate differences. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>candidate_prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Candidate outputs, (trace, time, 2).</dd>
<dt><code>baseline_prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Baseline outputs for the same traces.</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets for the same traces.</dd>
<dt><code>inputs</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional per-step input summary, as for evaluate_predictions.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher soma voltage in millivolts, shaped (trace, time); replaces the voltage reconstructed from the target.</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
<dt><code>candidate_interventions</code> <span class="api-type">Iterable[PairedInterventionPredictions]</span></dt>
<dd><span class="api-default">keyword-only, default=().</span> Candidate paired predictions per condition.</dd>
<dt><code>baseline_interventions</code> <span class="api-type">Iterable[PairedInterventionPredictions]</span></dt>
<dd><span class="api-default">keyword-only, default=().</span> Baseline paired predictions in the same condition order and with identical teacher targets.</dd>
<dt><code>config</code> <span class="api-type">EvaluationConfig | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Evaluation settings; None uses EvaluationConfig().</dd>
<dt><code>candidate_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;candidate&#x27;.</span> Candidate name.</dd>
<dt><code>baseline_id</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;baseline&#x27;.</span> Baseline name; must equal baseline_report[&#x27;model_id&#x27;] when a report is supplied.</dd>
<dt><code>baseline_report</code> <span class="api-type">dict[str, Any] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional cached baseline report; recomputed when its metric set or action-potential windows differ from the candidate&#x27;s.</dd>
<dt><code>bootstrap_replicates</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=250.</span> Paired bootstrap replicates; must be positive.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=20260711.</span> Seed of the paired bootstrap.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>comparison</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>candidate and baseline reports, comparison rows (id, candidate, baseline, delta, ci95_low, ci95_high, unit, core, preferred_direction, assessment), bootstrap_replicates, bootstrap_seed, and confidence_level 0.95.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-format-model-comparison">

## format_model_comparison

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.format_model_comparison(comparison: dict[str, Any]) -> str
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/iteration_evaluator.py#L1145-L1179)

</div>

Render the paired comparison table with candidate, baseline, difference, 95% interval, and assessment per metric. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>comparison</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Result of compare_predictions or evaluate_model_against_cache.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>text</code> <span class="api-type">str</span></dt>
<dd>Plain-text table.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-iteration-evaluator-write-model-comparison">

## write_model_comparison

<div class="api-signature">

```python
axobench.benchmark.iteration_evaluator.write_model_comparison(comparison: dict[str, Any], path: str | Path) -> Path
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/iteration_evaluator.py#L1182-L1226)

</div>

Write a complete JSON comparison or a tidy CSV of the paired differences, selected by the suffix. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>comparison</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Comparison to write.</dd>
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Destination ending in .json or .csv.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">Path</span></dt>
<dd>The written path.</dd>
</dl>

</section>
