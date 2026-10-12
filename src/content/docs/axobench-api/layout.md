---
title: Dataset layout and schema
description: Signatures, parameters, return values, and source for dataset layout and schema.
section: AxoBench API
apiGroup: Data
order: 307
---

## Overview

V1DatasetLayout resolves the split and intervention directories of an evaluation root. The schema module records the v1 split names, intervention conditions, morphology registry, target views, and diagnostic suite catalog.

Source revision: `22e52ec6c023`. [Export index](/axobench-api/).

<section class="api-symbol" id="benchmark-selectors-v1datasetlayout">

## V1DatasetLayout

<div class="api-signature">

```python
axobench.benchmark.selectors.V1DatasetLayout(root: str | Path)
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/selectors.py#L29-L79)

</div>

Resolver for the v1 layout: <root>/<split> for ordinary splits and <root>/interventions/<name> for conditions. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>root</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Dataset or evaluation root.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#benchmark-selectors-v1datasetlayout-split"><code>V1DatasetLayout.split()</code></a></li>
<li><a href="#benchmark-selectors-v1datasetlayout-intervention"><code>V1DatasetLayout.intervention()</code></a></li>
<li><a href="#benchmark-selectors-v1datasetlayout-default-validation"><code>V1DatasetLayout.default_validation()</code></a></li>
<li><a href="#benchmark-selectors-v1datasetlayout-available-interventions"><code>V1DatasetLayout.available_interventions()</code></a></li>
<li><a href="#benchmark-selectors-v1datasetlayout-validate-minimal"><code>V1DatasetLayout.validate_minimal()</code></a></li>
</ul>

<section class="api-method" id="benchmark-selectors-v1datasetlayout-split">

### V1DatasetLayout.split

<div class="api-signature">

```python
axobench.benchmark.selectors.V1DatasetLayout.split(name: DatasetCategory='val') -> DatasetSelector
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/selectors.py#L35-L38)

</div>

Selector for an ordinary split.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>name</code> <span class="api-type">DatasetCategory</span></dt>
<dd><span class="api-default">default=&#x27;val&#x27;.</span> One of ORDINARY_SPLITS.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>selector</code> <span class="api-type">DatasetSelector</span></dt>
<dd>Split selector.</dd>
</dl>

</section>

<section class="api-method" id="benchmark-selectors-v1datasetlayout-intervention">

### V1DatasetLayout.intervention

<div class="api-signature">

```python
axobench.benchmark.selectors.V1DatasetLayout.intervention(name: str) -> DatasetSelector
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/selectors.py#L40-L53)

</div>

Selector for an intervention condition; unknown names are accepted if their directory exists.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Condition name.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>selector</code> <span class="api-type">DatasetSelector</span></dt>
<dd>Condition selector.</dd>
</dl>

</section>

<section class="api-method" id="benchmark-selectors-v1datasetlayout-default-validation">

### V1DatasetLayout.default_validation

<div class="api-signature">

```python
axobench.benchmark.selectors.V1DatasetLayout.default_validation() -> DatasetSelector
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/selectors.py#L55-L56)

</div>

Selector for val.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>selector</code> <span class="api-type">DatasetSelector</span></dt>
<dd>Validation selector.</dd>
</dl>

</section>

<section class="api-method" id="benchmark-selectors-v1datasetlayout-available-interventions">

### V1DatasetLayout.available_interventions

<div class="api-signature">

```python
axobench.benchmark.selectors.V1DatasetLayout.available_interventions() -> tuple[str, ...]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/selectors.py#L58-L65)

</div>

Condition directories present, known conditions first in INTERVENTION_CONDITIONS order.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>names</code> <span class="api-type">tuple[str, ...]</span></dt>
<dd>Condition names.</dd>
</dl>

</section>

<section class="api-method" id="benchmark-selectors-v1datasetlayout-validate-minimal">

### V1DatasetLayout.validate_minimal

<div class="api-signature">

```python
axobench.benchmark.selectors.V1DatasetLayout.validate_minimal(*, require_interventions: bool=False) -> None
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/selectors.py#L67-L79)

</div>

Raise FileNotFoundError unless every ordinary split, and optionally every condition, has a manifest or shards.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>require_interventions</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Also require the five conditions.</dd>
</dl>

</section>

</section>

<section class="api-symbol" id="benchmark-selectors-datasetselector">

## DatasetSelector

<div class="api-signature">

```python
axobench.benchmark.selectors.DatasetSelector(root: Path, split: str | None, condition: str, intervention: str | None = None)
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/selectors.py#L17-L26)

</div>

A resolved split or intervention directory. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>root</code> <span class="api-type">Path</span></dt>
<dd><span class="api-default">required.</span> Directory of the split or condition.</dd>
<dt><code>split</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">required.</span> Split name, or None for a condition.</dd>
<dt><code>condition</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Split name or interventions/&lt;name&gt;.</dd>
<dt><code>intervention</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">default=None.</span> Condition name, or None for a split.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#benchmark-selectors-datasetselector-load"><code>DatasetSelector.load()</code></a></li>
</ul>

<section class="api-method" id="benchmark-selectors-datasetselector-load">

### DatasetSelector.load

<div class="api-signature">

```python
axobench.benchmark.selectors.DatasetSelector.load(*, cache_shards: int=1) -> ShardedNeuronIODataset
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/selectors.py#L25-L26)

</div>

Open the directory as a dataset.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>cache_shards</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=1.</span> Decoded shards kept in memory.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>dataset</code> <span class="api-type">ShardedNeuronIODataset</span></dt>
<dd>Reader for the directory.</dd>
</dl>

</section>

</section>

<section class="api-symbol" id="benchmark-dataset-schema-constants">

## Constants

<dl class="api-attributes">
<dt id="benchmark-dataset-schema-ordinary-splits"><code>ORDINARY_SPLITS = (&#x27;train&#x27;, &#x27;val&#x27;, &#x27;test&#x27;, &#x27;private-test&#x27;)</code></dt>
<dd>Ordinary split names of the v1 layout; private-test is not released. <a href="https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L13-L13">Source</a></dd>
<dt id="benchmark-dataset-schema-intervention-conditions"><code>INTERVENTION_CONDITIONS = (&#x27;event_dropout&#x27;, &#x27;exc_dropout&#x27;, &#x27;inh_dropout&#x27;, &#x27;temporal_jitter&#x27;, &#x27;site_silence&#x27;)</code></dt>
<dd>Released intervention conditions. <a href="https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L14-L20">Source</a></dd>
<dt id="benchmark-dataset-schema-v1-morphology-count"><code>V1_MORPHOLOGY_COUNT = 5</code></dt>
<dd>Morphologies in the v1 single-neuron release. <a href="https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L9-L9">Source</a></dd>
<dt id="benchmark-dataset-schema-v1-train-traces-per-morphology"><code>V1_TRAIN_TRACES_PER_MORPHOLOGY = 20000</code></dt>
<dd>Training traces per morphology in v1. <a href="https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L10-L10">Source</a></dd>
<dt id="benchmark-dataset-schema-diagnostic-suites"><code>DIAGNOSTIC_SUITES = (&#x27;teacher-qc&#x27;, &#x27;trace-core&#x27;, &#x27;state-dynamics&#x27;, &#x27;spike-behavior&#x27;, &#x27;feature-fidelity&#x27;, &#x27;mechanistic-response&#x27;, &#x27;morphology-contrast&#x27;, &#x27;intervention-response&#x27;, &#x27;metric-decoupling&#x27;, &#x27;target-view-audit&#x27;, &#x27;robustness-directionality&#x27;, &#x27;protocol-coverage&#x27;, &#x27;adapter-fairness&#x27;, &#x27;paper-summary&#x27;, &#x27;full&#x27;)</code></dt>
<dd>Suite names accepted by diagnostic contexts. <a href="https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L22-L38">Source</a></dd>
<dt id="benchmark-dataset-schema-diagnostic-row-columns"><code>DIAGNOSTIC_ROW_COLUMNS = (&#x27;diagnostic&#x27;, &#x27;suite&#x27;, &#x27;model_id&#x27;, &#x27;teacher_id&#x27;, &#x27;morphology_id&#x27;, &#x27;split&#x27;, &#x27;condition&#x27;, &#x27;intervention&#x27;, &#x27;trace_id&#x27;, &#x27;state&#x27;, &#x27;metric&#x27;, &#x27;value&#x27;, &#x27;unit&#x27;, &#x27;n&#x27;)</code></dt>
<dd>Columns required in every diagnostic row. <a href="https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L40-L55">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-dataset-schema-v1-morphologies">

## v1_morphologies

<div class="api-signature">

```python
axobench.benchmark.dataset_schema.v1_morphologies() -> tuple[MorphologySpec, ...]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L227-L306)

</div>

The frozen five-morphology v1 registry. Exported from `axobench.benchmark`.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>morphologies</code> <span class="api-type">tuple[MorphologySpec, ...]</span></dt>
<dd>Specimen, role, Cre line, and shape ratios per morphology.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-dataset-schema-morphologyspec">

## MorphologySpec

<div class="api-signature">

```python
axobench.benchmark.dataset_schema.MorphologySpec(specimen_id: int, role: str, swc_path: str, line_name: str, reconstruction_type: str, compatibility_score_lower_better: float, extracted_branches: int, routed_branches: int, total_length_ratio_vs_reference: float, routed_length_ratio_vs_reference: float, apical_fraction_delta_vs_reference: float, radial_extent_ratio_vs_reference: float, routing_shape_match: bool, caveat: str = 'Allen metadata marks this reconstruction dendrite-only.')
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L96-L115)

</div>

One registry entry of v1_morphologies; ratios and differences are relative to the reference specimen.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>specimen_id</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Allen specimen ID.</dd>
<dt><code>role</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Role in the morphology set.</dd>
<dt><code>swc_path</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> SWC path used at generation.</dd>
<dt><code>line_name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Cre line.</dd>
<dt><code>reconstruction_type</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Allen reconstruction type.</dd>
<dt><code>compatibility_score_lower_better</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span> Compatibility score against the reference.</dd>
<dt><code>extracted_branches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Branches extracted from the reconstruction.</dd>
<dt><code>routed_branches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Branches of the routed representation.</dd>
<dt><code>total_length_ratio_vs_reference</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span> Total dendritic length ratio.</dd>
<dt><code>routed_length_ratio_vs_reference</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span> Routed length ratio.</dd>
<dt><code>apical_fraction_delta_vs_reference</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span> Apical fraction difference.</dd>
<dt><code>radial_extent_ratio_vs_reference</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span> Radial extent ratio.</dd>
<dt><code>routing_shape_match</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span> Whether the routed representation matches the reference shape.</dd>
<dt><code>caveat</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;Allen metadata marks this reconstruction dendrite-only.&#x27;.</span> Reconstruction caveat.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="benchmark-dataset-schema-default-target-views">

## default_target_views

<div class="api-signature">

```python
axobench.benchmark.dataset_schema.default_target_views() -> tuple[TargetViewSpec, ...]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L315-L332)

</div>

Declared target views: neuronio_clipped_normalized for training and historical comparison, and raw_soma_mv for clipping diagnostics and spike-shape analysis. Exported from `axobench.benchmark`.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>views</code> <span class="api-type">tuple[TargetViewSpec, ...]</span></dt>
<dd>Target view declarations.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-dataset-schema-targetviewspec">

## TargetViewSpec

<div class="api-signature">

```python
axobench.benchmark.dataset_schema.TargetViewSpec(name: str, columns: tuple[str, ...], units: str, description: str, default_for_training: bool = False, default_for_historical_comparison: bool = False)
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L59-L70)

</div>

One stored view of the spike and soma target.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> View name.</dd>
<dt><code>columns</code> <span class="api-type">tuple[str, ...]</span></dt>
<dd><span class="api-default">required.</span> Column names.</dd>
<dt><code>units</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Column units.</dd>
<dt><code>description</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Definition of the view.</dd>
<dt><code>default_for_training</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span> Whether training uses this view by default.</dd>
<dt><code>default_for_historical_comparison</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span> Whether historical comparisons use this view.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="benchmark-dataset-schema-build-v1-dataset-manifest-template">

## build_v1_dataset_manifest_template

<div class="api-signature">

```python
axobench.benchmark.dataset_schema.build_v1_dataset_manifest_template(*, morphology_count: int=V1_MORPHOLOGY_COUNT, train_traces_per_morphology: int=V1_TRAIN_TRACES_PER_MORPHOLOGY) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L148-L224)

</div>

The v1 manifest contract as JSON-like data: categories, morphologies, target views, trace shape, and default diagnostic selectors. Non-training splits hold one eighth of the training traces per morphology. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>morphology_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=V1_MORPHOLOGY_COUNT = 5.</span> Number of morphologies.</dd>
<dt><code>train_traces_per_morphology</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=V1_TRAIN_TRACES_PER_MORPHOLOGY = 20000.</span> Training traces per morphology; at least 8.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>manifest</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>Manifest template.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-dataset-schema-validate-v1-manifest-template">

## validate_v1_manifest_template

<div class="api-signature">

```python
axobench.benchmark.dataset_schema.validate_v1_manifest_template(manifest: dict[str, Any]) -> None
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L704-L726)

</div>

Validate a manifest against the v1 contract without reading shards; raises ValueError on a mismatch. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>manifest</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Manifest dictionary.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-dataset-schema-build-diagnostic-suite-catalog">

## build_diagnostic_suite_catalog

<div class="api-signature">

```python
axobench.benchmark.dataset_schema.build_diagnostic_suite_catalog() -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/dataset_schema.py#L684-L701)

</div>

Suites, diagnostic specifications with their attached plotters, and the row columns, as printed by axobench dataset-schema --kind diagnostics. Exported from `axobench.benchmark`.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>catalog</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>suites, diagnostics, plotter_policy, and row_columns.</dd>
</dl>

</section>
