---
title: Defect injection
description: Signatures, parameters, return values, and source for defect injection.
section: AxoBench API
apiGroup: Diagnostics
order: 310
---

## Overview

Controlled defects injected into teacher traces, for testing whether a metric responds to a known error as it should. Spike-timing defects move the action-potential waveform with the spike; voltage defects leave the spike train exact. Import from axobench.benchmark.defect_injection. See [test metric sensitivity](/axobench/diagnostics/#test-metric-sensitivity).

Source revision: `22e52ec6c023`. [Export index](/axobench-api/).

<section class="api-symbol" id="benchmark-defect-injection-constants">

## Constants

<dl class="api-attributes">
<dt id="benchmark-defect-injection-defects"><code>DEFECTS = {&#x27;spike_jitter&#x27;, &#x27;spike_deletion&#x27;, &#x27;spike_insertion&#x27;, &#x27;global_lag&#x27;, &#x27;ap_clip&#x27;, &#x27;ap_smoothing&#x27;, &#x27;voltage_lowpass&#x27;, &#x27;voltage_offset&#x27;, &#x27;voltage_gain&#x27;, &#x27;post_spike&#x27;}</code></dt>
<dd>Defect names and the unit of their dose. <a href="https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/defect_injection.py#L36-L47">Source</a></dd>
<dt id="benchmark-defect-injection-default-doses"><code>DEFAULT_DOSES = {&#x27;spike_jitter&#x27;, &#x27;spike_deletion&#x27;, &#x27;spike_insertion&#x27;, &#x27;global_lag&#x27;, &#x27;ap_clip&#x27;, &#x27;ap_smoothing&#x27;, &#x27;voltage_lowpass&#x27;, &#x27;voltage_offset&#x27;, &#x27;voltage_gain&#x27;, &#x27;post_spike&#x27;}</code></dt>
<dd>Doses scored by defect_dose_rows when none are given. <a href="https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/defect_injection.py#L49-L60">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-defect-injection-inject-defect">

## inject_defect

<div class="api-signature">

```python
axobench.benchmark.defect_injection.inject_defect(spikes: np.ndarray, soma_mv: np.ndarray, defect: str, dose: float, *, rng: np.random.Generator | None=None) -> tuple[np.ndarray, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/defect_injection.py#L63-L110)

</div>

Corrupt teacher spikes and voltage with one defect at a dose; dose 0 returns copies.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Binary teacher spikes, (trace, time).</dd>
<dt><code>soma_mv</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher voltage in millivolts, same shape.</dd>
<dt><code>defect</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> A key of DEFECTS.</dd>
<dt><code>dose</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span> Defect strength in the unit of DEFECTS.</dd>
<dt><code>rng</code> <span class="api-type">np.random.Generator | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Random generator for the random defects; None creates an unseeded one.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd>Corrupted spikes.</dd>
<dt><code>soma_mv</code> <span class="api-type">np.ndarray</span></dt>
<dd>Corrupted voltage.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-defect-injection-defect-dose-rows">

## defect_dose_rows

<div class="api-signature">

```python
axobench.benchmark.defect_injection.defect_dose_rows(spikes: np.ndarray, soma_mv: np.ndarray, doses: Mapping[str, Iterable[float]] | None=None, *, seed: int=0, ignore_start: int=0) -> list[dict[str, Any]]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/defect_injection.py#L187-L216)

</div>

Score every defect at every dose against the uncorrupted teacher with both the historical NeuronIO scores and the AxoBench scores. Each defect's generator is seeded from seed and the defect name.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Binary teacher spikes, (trace, time).</dd>
<dt><code>soma_mv</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher voltage in millivolts.</dd>
<dt><code>doses</code> <span class="api-type">Mapping[str, Iterable[float]] | None</span></dt>
<dd><span class="api-default">default=None.</span> Doses per defect; None uses DEFAULT_DOSES.</dd>
<dt><code>seed</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Base seed.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial steps excluded after the defect is applied.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>rows</code> <span class="api-type">list[dict[str, Any]]</span></dt>
<dd>defect, dose, spike counts, historical_scores fields, and axobench_scores fields per defect and dose.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-defect-injection-axobench-scores">

## axobench_scores

<div class="api-signature">

```python
axobench.benchmark.defect_injection.axobench_scores(pred_spikes: np.ndarray, pred_soma_mv: np.ndarray, target_spikes: np.ndarray, target_soma_mv: np.ndarray) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/defect_injection.py#L141-L184)

</div>

AxoBench scores of a prediction against unclipped teacher voltage and spikes: Voltage and Dynamics SERA with skill against the per-trace teacher mean, subthreshold RMSE and skill, the F1 curve at 0 to 5 steps with Mean F1, and the coincidence factor at 2 steps. Predicted spikes are used as events directly.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>pred_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Predicted binary spikes, (trace, time).</dd>
<dt><code>pred_soma_mv</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Predicted voltage in millivolts.</dd>
<dt><code>target_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher spikes.</dd>
<dt><code>target_soma_mv</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Unclipped teacher voltage in millivolts.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>scores</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>voltage_sera, voltage_skill, dynamics_sera, dynamics_skill, subthreshold_rmse_mv, subthreshold_skill, f1_curve, mean_f1, and gamma_2.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-defect-injection-historical-scores">

## historical_scores

<div class="api-signature">

```python
axobench.benchmark.defect_injection.historical_scores(pred_spikes: np.ndarray, pred_soma_mv: np.ndarray, target_spikes: np.ndarray, target_soma_mv: np.ndarray) -> dict[str, float]
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/defect_injection.py#L118-L138)

</div>

NeuronIO-protocol scores: timestep AUC of the Gaussian-smoothed predicted spike train, and the RMSE of voltages clipped at -55 mV with and without rescaling the prediction to the target's mean and standard deviation.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>pred_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Predicted binary spikes.</dd>
<dt><code>pred_soma_mv</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Predicted voltage in millivolts.</dd>
<dt><code>target_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher spikes.</dd>
<dt><code>target_soma_mv</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher voltage in millivolts.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>scores</code> <span class="api-type">dict[str, float]</span></dt>
<dd>auc, clipped_rmse_aligned_mv, and clipped_rmse_mv.</dd>
</dl>

</section>

<section class="api-symbol" id="benchmark-defect-injection-smoothed-spike-score">

## smoothed_spike_score

<div class="api-signature">

```python
axobench.benchmark.defect_injection.smoothed_spike_score(spikes: np.ndarray, sigma_steps: float=1.0) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/benchmark/defect_injection.py#L113-L115)

</div>

Spike train smoothed with a Gaussian, used as the ranking score of the historical AUC.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Binary spikes.</dd>
<dt><code>sigma_steps</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=1.0.</span> Gaussian standard deviation in steps.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>score</code> <span class="api-type">np.ndarray</span></dt>
<dd>Smoothed score, (trace, time).</dd>
</dl>

</section>
