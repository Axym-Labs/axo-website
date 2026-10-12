---
title: Error anatomy
description: Signatures, parameters, return values, and source for error anatomy.
section: AxoBench API
apiGroup: Diagnostics
order: 312
---

## Overview

error_anatomy breaks a prediction's errors down by spike outcome, time from the nearest teacher spike, teacher firing rate, frequency band, and morphology, on the evaluator's scored traces with its threshold, spike events, action-potential windows, and relevance. plot_error_anatomy draws the result and writes a standalone pgfplots version. Import from axobench.benchmark.error_anatomy and axobench.benchmark.plots. [Error anatomy](/axobench/error-anatomy/) explains how to read each part.

Source revision: `496e0c1a2dfd`. [Export index](/axobench-api/).

<section class="api-symbol" id="benchmark-error-anatomy-error-anatomy">

## error_anatomy

<div class="api-signature">

```python
axobench.benchmark.error_anatomy.error_anatomy(prediction: np.ndarray, target: np.ndarray, *, raw_soma_mv: np.ndarray | None=None, trace_ids: list[str] | None=None, config: EvaluationConfig | None=None) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/error_anatomy.py#L56-L147)

</div>

Break a prediction's errors down on the scored traces of evaluate_predictions, with the same calibration, spike threshold, predicted events, action-potential windows, relevance, and subthreshold masks. Sections: spike events (hits, misses, and false spikes within HIT_TOLERANCE_STEPS, F1 per tolerance, timing errors of matched events), spike-triggered mean voltage of teacher and model around isolated hit, missed, and false spikes, subthreshold error by time since the last and until the next teacher spike (bins 0-5, 5-10, 10-25, 25-50, 50-100, 100+ ms and none), skills by teacher firing rate (0-1, 1-3, 3-6, 6+ Hz) and by morphology, and subthreshold skill by frequency band (0-1, 1-5, 5-10, 10-25, 25-50, 50-100, 100+ Hz). Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs shaped (trace, time, 2), in calibration-then-scoring order; at least two traces.</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets in the same order.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher soma voltage in millivolts, shaped (trace, time); replaces the voltage reconstructed from the target.</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
<dt><code>config</code> <span class="api-type">EvaluationConfig | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Evaluation settings; None uses EvaluationConfig().</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>anatomy</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>JSON-serializable: config, calibration_samples, scored_samples, spike_threshold, overall, spike_events, spike_triggered_average, subthreshold_by_spike_distance, by_teacher_rate, subthreshold_by_frequency, and by_morphology. Times are in steps or ms and voltages in mV.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-error-anatomy-reweight-to-rate-distribution">

## reweight_to_rate_distribution

<div class="api-signature">

```python
axobench.benchmark.error_anatomy.reweight_to_rate_distribution(anatomy: dict[str, Any], reference: dict[str, Any] | Mapping[str, float]) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/error_anatomy.py#L150-L185)

</div>

Skills of an error anatomy with its traces reweighted to another distribution over teacher firing-rate bins. Each trace is weighted by the reference share of its bin divided by the bin's own share; bins absent from the reference get weight zero, so the comparison covers the common support. Relevance and references stay those of the anatomy's own block. Exported from `axobench.benchmark`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>anatomy</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Result of error_anatomy to reweight.</dd>
<dt><code>reference</code> <span class="api-type">dict[str, Any] | Mapping[str, float]</span></dt>
<dd><span class="api-default">required.</span> Another error_anatomy result, whose scored-trace shares per rate bin are used, or a mapping from bin label (&#x27;0-1&#x27;, &#x27;1-3&#x27;, &#x27;3-6&#x27;, &#x27;6+&#x27;) to share.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>skills</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>voltage_sera_skill, voltage_sera_ceiling_skill, voltage_sera_skill_of_ceiling, subthreshold_skill, mean_f1, and the bins used. Raises ValueError when a weighted bin has no traces or no bin is shared.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-error-anatomy-constants">

## Constants

<dl class="api-attributes">
<dt id="benchmark-error-anatomy-hit-tolerance-steps"><code>HIT_TOLERANCE_STEPS = 2</code></dt>
<dd>Timing tolerance in steps within which a predicted spike counts as a hit of a teacher spike. <a href="https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/error_anatomy.py#L48-L48">Source</a></dd>
<dt id="benchmark-error-anatomy-sta-lags-steps"><code>STA_LAGS_STEPS = (-10, 40)</code></dt>
<dd>First and last lag of the spike-triggered averages, in steps; events count as isolated when no other event of the same train falls in this window. <a href="https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/error_anatomy.py#L49-L49">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-plots-plot-error-anatomy">

## plot_error_anatomy

<div class="api-signature">

```python
axobench.benchmark.plots.plot_error_anatomy(anatomy: dict[str, Any], output: str | Path, *, formats: tuple[str, ...]=PLOT_FORMATS, tikz: bool=True) -> list[str]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/plots.py#L789-L840)

</div>

Plot an error_anatomy result in four panels: spike-triggered voltage of teacher and model around hit, missed, and false spikes; share of retained steps and of squared subthreshold error by time since the last teacher spike; skill by teacher firing rate; and subthreshold skill by frequency band. Uses apply_paper_plot_style.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>anatomy</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Result of error_anatomy.</dd>
<dt><code>output</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Output path without suffix; each format is written with its own suffix.</dd>
<dt><code>formats</code> <span class="api-type">tuple[str, ...]</span></dt>
<dd><span class="api-default">keyword-only, default=PLOT_FORMATS = (&#x27;svg&#x27;, &#x27;pdf&#x27;, &#x27;png&#x27;).</span> File formats passed to Matplotlib, for example (&#x27;pdf&#x27;, &#x27;png&#x27;) or (&#x27;svg&#x27;,).</dd>
<dt><code>tikz</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Also write a standalone pgfplots .tex file of the same panels.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>paths</code> <span class="api-type">list[str]</span></dt>
<dd>Written figure paths, followed by the .tex path when tikz is set.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-plots-apply-paper-plot-style">

## apply_paper_plot_style

<div class="api-signature">

```python
axobench.benchmark.plots.apply_paper_plot_style() -> None
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/benchmark/plots.py#L44-L101)

</div>

Set the Matplotlib style of AxoBench figures: STIX serif text at 7 to 8 pt, despined axes without grid, the Okabe-Ito palette, white background, text kept as text in PDF and SVG, and 300 dpi PNG. A style file named by the AXOBENCH_PAPER_STYLE environment variable is applied first.

</section>
