---
title: IRon relevance
description: Signatures, parameters, return values, and source for iRon relevance.
section: AxoBench API
apiGroup: Metrics
order: 305
---

## Overview

The relevance function and squared error-relevance area of the IRon R package (Ribeiro and Moniz, 2020) with its default settings: adjusted-boxplot fences (Hubert and Vandervieren, 2008) with an exact medcouple, relevance 1 at the fences and 0 at the median, and a trapezoidal area over thresholds with step 0.001.

Source revision: `496e0c1a2dfd`. [Export index](/axobench-api/).

<section class="api-symbol" id="relevance-iron-relevance">

## iron_relevance

<div class="api-signature">

```python
axobench.relevance.iron_relevance(target: np.ndarray, *, reference: np.ndarray | None=None) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/relevance.py#L167-L178)

</div>

IRon default relevance phi of each value, with control points from the reference values: 1 at the lower adjusted-boxplot fence, 0 at the median, 1 at the upper fence, monotone cubic in between and constant beyond.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Values to score.</dd>
<dt><code>reference</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Values that define the control points; None uses target.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>relevance</code> <span class="api-type">np.ndarray</span></dt>
<dd>Relevance in [0, 1] with the shape of target.</dd>
</dl>

</section>

<section class="api-symbol" id="relevance-iron-threshold-weights">

## iron_threshold_weights

<div class="api-signature">

```python
axobench.relevance.iron_threshold_weights(relevance: np.ndarray, *, step: float=0.001) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/relevance.py#L194-L206)

</div>

Per-sample weights A(phi) such that iron_sera(e, phi) equals the sum of e**2 * A(phi): the trapezoidal area of the thresholds a sample passes, and 1 for phi >= 1.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>relevance</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Relevance values.</dd>
<dt><code>step</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.001.</span> Threshold grid step.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>weights</code> <span class="api-type">np.ndarray</span></dt>
<dd>Weights in [0, 1].</dd>
</dl>

</section>

<section class="api-symbol" id="relevance-iron-sera">

## iron_sera

<div class="api-signature">

```python
axobench.relevance.iron_sera(error: np.ndarray, relevance: np.ndarray, *, step: float=0.001) -> float
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/relevance.py#L181-L191)

</div>

IRon sera: the trapezoidal area over thresholds t of SER(t), the summed squared error of samples with relevance at least t.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>error</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Prediction errors.</dd>
<dt><code>relevance</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Relevance of each sample.</dd>
<dt><code>step</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.001.</span> Threshold grid step.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>sera</code> <span class="api-type">float</span></dt>
<dd>Squared error-relevance area, not normalized.</dd>
</dl>

</section>

<section class="api-symbol" id="relevance-adjusted-box-fences">

## adjusted_box_fences

<div class="api-signature">

```python
axobench.relevance.adjusted_box_fences(values: np.ndarray, *, coef: float=1.5, a: float=-4.0, b: float=3.0) -> tuple[float, float, float]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/relevance.py#L113-L124)

</div>

Lower fence, median, and upper fence of the adjusted boxplot, as robustbase::adjboxStats: Q1 - coef exp(a mc) IQR and Q3 + coef exp(b mc) IQR for mc >= 0, mirrored for mc < 0.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>values</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Sample values; flattened.</dd>
<dt><code>coef</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.5.</span> Whisker coefficient.</dd>
<dt><code>a</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-4.0.</span> Lower exponent coefficient.</dd>
<dt><code>b</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=3.0.</span> Upper exponent coefficient.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>fences</code> <span class="api-type">tuple[float, float, float]</span></dt>
<dd>(lower fence, median, upper fence).</dd>
</dl>

</section>

<section class="api-symbol" id="relevance-medcouple">

## medcouple

<div class="api-signature">

```python
axobench.relevance.medcouple(values: np.ndarray) -> float
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/relevance.py#L36-L90)

</div>

Exact medcouple, a robust skewness measure (Brys, Hubert and Struyf, 2004), computed in O(n log n).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>values</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Sample values; flattened.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>mc</code> <span class="api-type">float</span></dt>
<dd>Medcouple in [-1, 1]; 0 for fewer than three values or zero spread.</dd>
</dl>

</section>

<section class="api-symbol" id="relevance-fivenum">

## fivenum

<div class="api-signature">

```python
axobench.relevance.fivenum(values: np.ndarray) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/relevance.py#L25-L33)

</div>

Tukey's five-number summary, as R's fivenum.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>values</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Sample values; flattened. At least one is required.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>summary</code> <span class="api-type">np.ndarray</span></dt>
<dd>Minimum, lower hinge, median, upper hinge, and maximum.</dd>
</dl>

</section>
