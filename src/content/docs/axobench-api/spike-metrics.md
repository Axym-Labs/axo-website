---
title: Spike event metrics
description: Signatures, parameters, return values, and source for spike event metrics.
section: AxoBench API
apiGroup: Metrics
order: 304
---

## Overview

Spike events, thresholds, one-to-one event matching, and F1 over timing tolerances, together with the coincidence factor and the historical timestep AUC and voltage RMSE. Spike arrays are (trace, time) or (time,); values above 0.5 count as events.

Source revision: `22e52ec6c023`. [Export index](/axobench-api/).

<section class="api-symbol" id="metrics-spike-event-peaks">

## spike_event_peaks

<div class="api-signature">

```python
axobench.metrics.spike_event_peaks(scores: np.ndarray, *, refractory_steps: int=2, min_score: float=-np.inf) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L68-L95)

</div>

Candidate spike events: local maxima of each trace's score, kept greedily from the highest score down with other maxima within refractory_steps suppressed. A step is a maximum if it exceeds the previous step and is not below the next.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>scores</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Spike scores, (trace, time).</dd>
<dt><code>refractory_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Suppression radius in steps; 0 keeps every maximum.</dd>
<dt><code>min_score</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-np.inf.</span> Maxima below this score are dropped first; this does not change which higher maxima are kept.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>events</code> <span class="api-type">np.ndarray</span></dt>
<dd>Boolean (trace, time) event array.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-spike-events">

## spike_events

<div class="api-signature">

```python
axobench.metrics.spike_events(scores: np.ndarray, threshold: float, *, refractory_steps: int | None=2) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L98-L108)

</div>

Binary spike events: score peaks at or above the threshold, or every supra-threshold step when refractory_steps is None.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>scores</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Spike scores, (trace, time).</dd>
<dt><code>threshold</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span> Event threshold.</dd>
<dt><code>refractory_steps</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Suppression radius; None disables peak detection.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>events</code> <span class="api-type">np.ndarray</span></dt>
<dd>Boolean (trace, time) event array.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-prevalence-matched-threshold">

## prevalence_matched_threshold

<div class="api-signature">

```python
axobench.metrics.prevalence_matched_threshold(scores: np.ndarray, positive_count: int) -> float
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L56-L65)

</div>

Threshold at which the number of timesteps scoring at or above it reaches positive_count: the positive_count-th highest score. The evaluator calibrates with this function.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>scores</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Scores of any shape; flattened.</dd>
<dt><code>positive_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Target number of positive timesteps.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>threshold</code> <span class="api-type">float</span></dt>
<dd>The threshold; +inf for a non-positive count and -inf when the count covers every score.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-event-count-matched-threshold">

## event_count_matched_threshold

<div class="api-signature">

```python
axobench.metrics.event_count_matched_threshold(scores: np.ndarray, positive_count: int, *, refractory_steps: int | None=2) -> float
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L111-L121)

</div>

Threshold at which spike_events yields positive_count events.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>scores</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Spike scores, (trace, time).</dd>
<dt><code>positive_count</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Target number of events.</dd>
<dt><code>refractory_steps</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Suppression radius; None matches timesteps instead.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>threshold</code> <span class="api-type">float</span></dt>
<dd>The height of the positive_count-th highest score peak.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-spike-event-confusion">

## spike_event_confusion

<div class="api-signature">

```python
axobench.metrics.spike_event_confusion(predicted_spikes: np.ndarray, target_spikes: np.ndarray, *, tolerance_steps: int) -> dict[str, int]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L124-L156)

</div>

One-to-one event confusion under a symmetric timing tolerance. Within each trace, events are paired in time order when they lie within the tolerance; counts are summed over traces.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>predicted_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Predicted events, (trace, time).</dd>
<dt><code>target_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher events of the same shape.</dd>
<dt><code>tolerance_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Non-negative matching tolerance in steps.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>confusion</code> <span class="api-type">dict[str, int]</span></dt>
<dd>tp, fp, and fn.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-spike-f1-curve">

## spike_f1_curve

<div class="api-signature">

```python
axobench.metrics.spike_f1_curve(spike_scores: np.ndarray, target_spikes: np.ndarray, *, threshold: float=0.0, tolerances_steps: tuple[int, ...] | list[int]=(0, 1, 2, 3, 4, 5), refractory_steps: int | None=2) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L196-L265)

</div>

Event F1 at each timing tolerance, the arithmetic Mean F1, and the trapezoidal F1 area normalized by the tolerance span.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>spike_scores</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Spike scores, (trace, time).</dd>
<dt><code>target_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher spike indicators of the same shape.</dd>
<dt><code>threshold</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.0.</span> Event threshold applied to the scores.</dd>
<dt><code>tolerances_steps</code> <span class="api-type">tuple[int, ...] | list[int]</span></dt>
<dd><span class="api-default">keyword-only, default=(0, 1, 2, 3, 4, 5).</span> Strictly increasing non-negative tolerances.</dd>
<dt><code>refractory_steps</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Suppression radius of spike_events.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>curve</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>threshold, refractory_steps, t_min_steps, t_max_steps, mean_f1, f1_area, and rows with precision, recall, f1, tp, fp, and fn per tolerance.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-coincidence-factor">

## coincidence_factor

<div class="api-signature">

```python
axobench.metrics.coincidence_factor(predicted_spikes: np.ndarray, target_spikes: np.ndarray, *, delta_steps: int=2) -> dict[str, float | int]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L159-L193)

</div>

Coincidence factor Gamma (Kistler et al. 1997; Jolivet et al. 2008): coincidences within the tolerance minus those expected from a Poisson train at the predicted rate, normalized so that a perfect prediction scores 1 and chance about 0.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>predicted_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Predicted events, (trace, time).</dd>
<dt><code>target_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher events of the same shape.</dd>
<dt><code>delta_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Coincidence tolerance in steps.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">dict[str, float | int]</span></dt>
<dd>gamma, coincidences, expected_coincidences, predicted_spikes, target_spikes, and delta_steps.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-binary-auc">

## binary_auc

<div class="api-signature">

```python
axobench.metrics.binary_auc(scores: np.ndarray, labels: np.ndarray) -> float
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L25-L49)

</div>

Rank-based ROC AUC with averaged tied ranks over all flattened entries.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>scores</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Continuous scores.</dd>
<dt><code>labels</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Binary labels; values above 0.5 are positive.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>auc</code> <span class="api-type">float</span></dt>
<dd>ROC AUC, or NaN when a class is absent.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-spike-auc">

## spike_auc

<div class="api-signature">

```python
axobench.metrics.spike_auc(prediction: np.ndarray, target: np.ndarray) -> float
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L52-L53)

</div>

Timestep ROC AUC of channel 0 of a prediction against channel 0 of a target, the historical NeuronIO spike score.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Array whose channel 0 holds spike scores.</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Array whose channel 0 holds spike labels.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>auc</code> <span class="api-type">float</span></dt>
<dd>ROC AUC.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-soma-rmse">

## soma_rmse

<div class="api-signature">

```python
axobench.metrics.soma_rmse(prediction: np.ndarray, target: np.ndarray) -> float
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/metrics.py#L19-L22)

</div>

RMSE of channel 1 in the supplied coordinate.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Array whose channel 1 holds soma values.</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Array in the same coordinate.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rmse</code> <span class="api-type">float</span></dt>
<dd>Root-mean-square error.</dd>
</dl>

</section>
