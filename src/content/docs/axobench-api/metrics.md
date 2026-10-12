---
title: Core metric functions
description: Signatures, parameters, return values, and source for core metric functions.
section: AxoBench API
apiGroup: Metrics
order: 303
---

## Overview

Array-level implementations of Voltage SERA, the subthreshold voltage RMSE, Response SERA, Dynamics SERA, and the SERA skill scores. Predictions and targets are (trace, time, 2) arrays in the AxoBench target coordinate; voltages are converted to millivolts as soma/soma_scale + soma_bias_mv, and raw_soma_mv replaces the reconstructed teacher voltage when supplied. [Core metrics](/axobench/metrics/) gives the definitions.

Source revision: `496e0c1a2dfd`. [Export index](/axobench-api/).

<section class="api-symbol" id="metrics-compute-core-metric-set">

## compute_core_metric_set

<div class="api-signature">

```python
axobench.metrics.compute_core_metric_set(prediction: np.ndarray, target: np.ndarray, *, raw_soma_mv: np.ndarray | None=None, trace_ids: list[str] | None=None, soma_scale: float=0.1, soma_bias_mv: float=-67.7, ignore_start: int=0, spike_threshold: float | None=None, spike_threshold_policy: str='prevalence', spike_tolerances_steps: tuple[int, ...] | list[int]=(0, 1, 2, 3, 4, 5), spike_refractory_steps: int | None=2, timestep_ms: float=1.0, intervention_prediction: np.ndarray | None=None, intervention_target: np.ndarray | None=None, intervention_raw_soma_mv: np.ndarray | None=None) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L759-L872)

</div>

Compute the core metrics on aligned arrays without a calibration split. Without spike_threshold, the default policy chooses the threshold on the same traces so that the predicted event count equals the teacher spike count.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs shaped (trace, time, 2).</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets shaped (trace, time, 2): spike indicator and soma target coordinate.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher soma voltage in millivolts, shaped (trace, time); replaces the voltage reconstructed from the target.</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale of the soma target coordinate; millivolts are soma / soma_scale + soma_bias_mv.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from scoring.</dd>
<dt><code>spike_threshold</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Fixed spike threshold; recommended when calibrated on other traces.</dd>
<dt><code>spike_threshold_policy</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;prevalence&#x27;.</span> &#x27;prevalence&#x27; for the event-count-matched threshold or &#x27;zero&#x27; for 0, used when spike_threshold is None.</dd>
<dt><code>spike_tolerances_steps</code> <span class="api-type">tuple[int, ...] | list[int]</span></dt>
<dd><span class="api-default">keyword-only, default=(0, 1, 2, 3, 4, 5).</span> F1 timing tolerances in steps.</dd>
<dt><code>spike_refractory_steps</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=2.</span> Suppression radius of spike events; None treats every supra-threshold step as an event.</dd>
<dt><code>timestep_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span> Duration of one timestep in milliseconds.</dd>
<dt><code>intervention_prediction</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional model outputs for edited inputs; target and prediction then act as the baseline.</dd>
<dt><code>intervention_target</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Teacher targets for the edited inputs; required with intervention_prediction.</dd>
<dt><code>intervention_raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher voltage for the edited inputs.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>voltage, dynamics, subthreshold, spike, and optionally response sub-results, plus voltage_sera_iron_per_spike_mv2, subthreshold_rmse_mv, subthreshold_skill, dynamics_sera_iron_per_spike_mv2_per_ms2, spike_mean_f1, spike_f1_area, spike_threshold, spike_threshold_kind, and response_sera_iron_per_spike_mv2 when available.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-iron-voltage-sera">

## iron_voltage_sera

<div class="api-signature">

```python
axobench.metrics.iron_voltage_sera(prediction: np.ndarray, target: np.ndarray, *, raw_soma_mv: np.ndarray | None=None, soma_scale: float=0.1, soma_bias_mv: float=-67.7, ignore_start: int=0) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L286-L316)

</div>

IRon-default Voltage SERA per teacher spike, with relevance fitted on the pooled scored teacher voltage.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs shaped (trace, time, 2).</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets shaped (trace, time, 2): spike indicator and soma target coordinate.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher soma voltage in millivolts, shaped (trace, time); replaces the voltage reconstructed from the target.</dd>
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale of the soma target coordinate; millivolts are soma / soma_scale + soma_bias_mv.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from scoring.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>voltage_sera_iron_mv2 (area), voltage_sera_iron_per_spike_mv2 (None without teacher spikes), teacher_spikes, and relevance_mean.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-sera-skill-trace-terms">

## sera_skill_trace_terms

<div class="api-signature">

```python
axobench.metrics.sera_skill_trace_terms(prediction: np.ndarray, target: np.ndarray, *, reference_mv: float, raw_soma_mv: np.ndarray | None=None, soma_scale: float=0.1, soma_bias_mv: float=-67.7, timestep_ms: float=1.0, ignore_start: int=0) -> dict[str, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L357-L400)

</div>

Per-trace IRon SERA areas behind the SERA skill scores. Relevance is fitted once on the pooled scored teacher, as in iron_voltage_sera and iron_dynamics_sera, so sums over any subset of traces give that subset's skills.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Scored model outputs shaped (trace, time, 2).</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Scored teacher targets of the same shape.</dd>
<dt><code>reference_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Constant reference voltage in mV, usually sera_reference_voltage of the calibration traces.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher voltage (trace, time); replaces the voltage reconstructed from the target.</dd>
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale of the soma target coordinate; millivolts are soma / soma_scale + soma_bias_mv.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>timestep_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span> Duration of one timestep in milliseconds.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from scoring.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>terms</code> <span class="api-type">dict[str, np.ndarray]</span></dt>
<dd>Per trace: voltage (prediction area), voltage_reference (constant reference), voltage_ceiling (teacher clipped at -55 mV), dynamics and dynamics_reference (dV/dt areas of the prediction and of the constant, whose rate is zero), and teacher_spikes.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-sera-skills">

## sera_skills

<div class="api-signature">

```python
axobench.metrics.sera_skills(terms: dict[str, np.ndarray], indices: np.ndarray | None=None) -> dict[str, float | None]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L403-L428)

</div>

SERA skill scores from sera_skill_trace_terms, pooled over all or selected traces. Each skill is 1 - area / reference area; prediction and reference share relevance and spike count, so this equals 1 - SERA / SERA(reference).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>terms</code> <span class="api-type">dict[str, np.ndarray]</span></dt>
<dd><span class="api-default">required.</span> Result of sera_skill_trace_terms.</dd>
<dt><code>indices</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">default=None.</span> Trace indices to pool; None pools all, and repeated indices count repeatedly as in a bootstrap draw.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>skills</code> <span class="api-type">dict[str, float | None]</span></dt>
<dd>voltage_sera_skill, voltage_sera_ceiling_skill (the skill of the teacher clipped at -55 mV, the best prediction without action potentials), voltage_sera_skill_of_ceiling (their ratio), and dynamics_sera_skill; None where a reference area or the ceiling is zero.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-subthreshold-voltage-error">

## subthreshold_voltage_error

<div class="api-signature">

```python
axobench.metrics.subthreshold_voltage_error(prediction: np.ndarray, target: np.ndarray, *, predicted_spikes: np.ndarray, raw_soma_mv: np.ndarray | None=None, trace_ids: list[str] | None=None, ap_post_steps: np.ndarray | None=None, soma_scale: float=0.1, soma_bias_mv: float=-67.7, ignore_start: int=0, timestep_ms: float=1.0) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L599-L649)

</div>

Somatic voltage RMSE outside action-potential windows of teacher and predicted spikes, with both voltages clipped at -55 mV, and its skill against the per-trace mean clipped teacher voltage.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs covering the whole trace, (trace, time, 2).</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets covering the whole trace.</dd>
<dt><code>predicted_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Predicted spike events of the scored steps only, (trace, time - ignore_start).</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher voltage covering the whole trace.</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
<dt><code>ap_post_steps</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Per-trace window ends; None computes them with ap_window_ends from the scored teacher steps.</dd>
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale of the soma target coordinate; millivolts are soma / soma_scale + soma_bias_mv.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from scoring.</dd>
<dt><code>timestep_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span> Duration of one timestep in milliseconds.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>subthreshold_rmse_mv, subthreshold_skill, null_subthreshold_rmse_mv, and retained_points.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-subthreshold-voltage-point-terms">

## subthreshold_voltage_point_terms

<div class="api-signature">

```python
axobench.metrics.subthreshold_voltage_point_terms(prediction: np.ndarray, target: np.ndarray, *, predicted_spikes: np.ndarray, raw_soma_mv: np.ndarray | None=None, trace_ids: list[str] | None=None, ap_post_steps: np.ndarray | None=None, soma_scale: float=0.1, soma_bias_mv: float=-67.7, ignore_start: int=0, timestep_ms: float=1.0) -> dict[str, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L515-L576)

</div>

Per-step terms of the subthreshold voltage error on the scored steps, for breaking the error down by time or frequency. Steps in the action-potential windows of teacher or predicted spikes are excluded and both voltages are clipped at -55 mV.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs covering the whole trace, (trace, time, 2).</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets covering the whole trace.</dd>
<dt><code>predicted_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Predicted spike events of the scored steps only, (trace, time - ignore_start).</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher voltage covering the whole trace.</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
<dt><code>ap_post_steps</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Per-trace window ends; None computes them with ap_window_ends from the scored teacher steps.</dd>
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale of the soma target coordinate; millivolts are soma / soma_scale + soma_bias_mv.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from scoring.</dd>
<dt><code>timestep_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span> Duration of one timestep in milliseconds.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>terms</code> <span class="api-type">dict[str, np.ndarray]</span></dt>
<dd>keep (boolean mask of retained steps), error (clipped prediction minus clipped teacher), and deviation (clipped teacher minus its per-trace mean over retained steps), each (trace, time - ignore_start) and zero where not kept.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-subthreshold-voltage-trace-terms">

## subthreshold_voltage_trace_terms

<div class="api-signature">

```python
axobench.metrics.subthreshold_voltage_trace_terms(prediction: np.ndarray, target: np.ndarray, **kwargs: Any) -> dict[str, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L579-L596)

</div>

Per-trace sums behind subthreshold_voltage_error, so that subsets of traces can be pooled with fixed windows, as the paired bootstrap does. Keyword arguments are those of subthreshold_voltage_point_terms.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs covering the whole trace, (trace, time, 2).</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets covering the whole trace.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>terms</code> <span class="api-type">dict[str, np.ndarray]</span></dt>
<dd>squared_error, null_squared_error, and retained_points per trace.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-ap-window-ends">

## ap_window_ends

<div class="api-signature">

```python
axobench.metrics.ap_window_ends(raw_soma_mv: np.ndarray | None, teacher_spikes: np.ndarray, *, trace_ids: list[str] | None=None, timestep_ms: float=1.0) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L454-L512)

</div>

Cell-type-specific end of the action-potential window. For each trace-ID prefix, the mean waveform of isolated teacher spikes (lags -6 to +30, no other spike in the next 30 steps) is computed, and the end is the first lag >= 1 at which it changes by less than 1 mV per ms. Groups with fewer than 20 isolated spikes, no flat lag, or no voltage use 4.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">required.</span> Unclipped teacher voltage (trace, time), or None to use the fallback for every group.</dd>
<dt><code>teacher_spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher spike indicators, (trace, time).</dd>
<dt><code>trace_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Sample IDs, one per trace; the text before the first &#x27;:&#x27; is the morphology or cell-type group.</dd>
<dt><code>timestep_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span> Duration of one timestep in milliseconds.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>post_steps per trace, end_steps_by_cell_type, and fallback_cell_types.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-ap-window-mask">

## ap_window_mask

<div class="api-signature">

```python
axobench.metrics.ap_window_mask(spikes: np.ndarray, post_steps: np.ndarray | None=None) -> np.ndarray
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L431-L451)

</div>

Boolean mask of the steps from 2 before to post_steps after each spike, inclusive.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>spikes</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Spike indicators, (trace, time).</dd>
<dt><code>post_steps</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">default=None.</span> Window end per trace; None uses AP_POST_STEPS.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>mask</code> <span class="api-type">np.ndarray</span></dt>
<dd>Boolean (trace, time) mask.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-response-sera">

## response_sera

<div class="api-signature">

```python
axobench.metrics.response_sera(baseline_prediction: np.ndarray, intervention_prediction: np.ndarray, baseline_target: np.ndarray, intervention_target: np.ndarray, *, baseline_raw_soma_mv: np.ndarray | None=None, intervention_raw_soma_mv: np.ndarray | None=None, soma_scale: float=0.1, soma_bias_mv: float=-67.7, ignore_start: int=0) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L713-L756)

</div>

IRon-default Response SERA per teacher spike. The error is the predicted minus the teacher voltage change (intervention minus baseline); relevance is fitted on the pooled teacher change, and the area is divided by the teacher spikes of baseline and intervention traces.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>baseline_prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs for the baseline inputs, (pair, time, 2).</dd>
<dt><code>intervention_prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs for the edited inputs.</dd>
<dt><code>baseline_target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets for the baseline inputs.</dd>
<dt><code>intervention_target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets for the edited inputs.</dd>
<dt><code>baseline_raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped baseline teacher voltage.</dd>
<dt><code>intervention_raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped intervention teacher voltage.</dd>
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale of the soma target coordinate; millivolts are soma / soma_scale + soma_bias_mv.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from scoring.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>response_sera_iron_mv2, response_sera_iron_per_spike_mv2, the zero-response control in both forms, teacher_spikes, response_rmse_mv, teacher_response_abs_mean_mv, and relevance_mean.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-response-sera-trace-terms">

## response_sera_trace_terms

<div class="api-signature">

```python
axobench.metrics.response_sera_trace_terms(baseline_prediction: np.ndarray, intervention_prediction: np.ndarray, baseline_target: np.ndarray, intervention_target: np.ndarray, *, baseline_raw_soma_mv: np.ndarray | None=None, intervention_raw_soma_mv: np.ndarray | None=None, soma_scale: float=0.1, soma_bias_mv: float=-67.7, ignore_start: int=0) -> dict[str, np.ndarray]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L652-L710)

</div>

Per-pair terms of Response SERA with the relevance fitted once on all supplied pairs, so that subsets can be pooled with fixed relevance.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>baseline_prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs for the baseline inputs, (pair, time, 2).</dd>
<dt><code>intervention_prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs for the edited inputs.</dd>
<dt><code>baseline_target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets for the baseline inputs.</dd>
<dt><code>intervention_target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets for the edited inputs.</dd>
<dt><code>baseline_raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped baseline teacher voltage.</dd>
<dt><code>intervention_raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped intervention teacher voltage.</dd>
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale of the soma target coordinate; millivolts are soma / soma_scale + soma_bias_mv.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from scoring.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>terms</code> <span class="api-type">dict[str, np.ndarray]</span></dt>
<dd>area, zero_response_area, and teacher_spikes per pair, plus the error, teacher_delta, and weights arrays.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-iron-dynamics-sera">

## iron_dynamics_sera

<div class="api-signature">

```python
axobench.metrics.iron_dynamics_sera(prediction: np.ndarray, target: np.ndarray, *, raw_soma_mv: np.ndarray | None=None, soma_scale: float=0.1, soma_bias_mv: float=-67.7, timestep_ms: float=1.0, ignore_start: int=0) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L319-L354)

</div>

IRon-default SERA of the one-step voltage change per teacher spike, with relevance fitted on the teacher's rate of change. Requires at least two scored steps.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Model outputs shaped (trace, time, 2).</dd>
<dt><code>target</code> <span class="api-type">np.ndarray</span></dt>
<dd><span class="api-default">required.</span> Teacher targets shaped (trace, time, 2): spike indicator and soma target coordinate.</dd>
<dt><code>raw_soma_mv</code> <span class="api-type">np.ndarray | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional unclipped teacher soma voltage in millivolts, shaped (trace, time); replaces the voltage reconstructed from the target.</dd>
<dt><code>soma_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=0.1.</span> Scale of the soma target coordinate; millivolts are soma / soma_scale + soma_bias_mv.</dd>
<dt><code>soma_bias_mv</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=-67.7.</span> Millivolt offset of the soma target coordinate.</dd>
<dt><code>timestep_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span> Duration of one timestep in milliseconds.</dd>
<dt><code>ignore_start</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=0.</span> Initial timesteps excluded from scoring.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>dynamics_sera_iron_mv2_per_ms2, dynamics_sera_iron_per_spike_mv2_per_ms2, teacher_spikes, and relevance_mean.</dd>
</dl>

</section>

<section class="api-symbol" id="metrics-constants">

## Constants

<dl class="api-attributes">
<dt id="metrics-ap-pre-steps"><code>AP_PRE_STEPS = 2</code></dt>
<dd>Steps before a spike included in its action-potential window. <a href="https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L10-L10">Source</a></dd>
<dt id="metrics-ap-post-steps"><code>AP_POST_STEPS = 4</code></dt>
<dd>Fallback window end after a spike. <a href="https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L11-L11">Source</a></dd>
<dt id="metrics-ap-flat-slope-mv-per-ms"><code>AP_FLAT_SLOPE_MV_PER_MS = 1.0</code></dt>
<dd>Slope below which the mean spike waveform counts as flat. <a href="https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L12-L12">Source</a></dd>
<dt id="metrics-ap-waveform-pre-steps"><code>AP_WAVEFORM_PRE_STEPS = 6</code></dt>
<dd>Steps before a spike in the averaged waveform. <a href="https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L13-L13">Source</a></dd>
<dt id="metrics-ap-isolation-steps"><code>AP_ISOLATION_STEPS = 30</code></dt>
<dd>Steps after a spike that must be free of other spikes, and the waveform length after the spike. <a href="https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L14-L14">Source</a></dd>
<dt id="metrics-ap-min-isolated-spikes"><code>AP_MIN_ISOLATED_SPIKES = 20</code></dt>
<dd>Isolated spikes required to estimate a cell type&#x27;s window end. <a href="https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L15-L15">Source</a></dd>
<dt id="metrics-soma-clip-mv"><code>SOMA_CLIP_MV = -55.0</code></dt>
<dd>Clipping level of the subthreshold RMSE and the NeuronIO target, in mV. <a href="https://github.com/Axym-Labs/axobench/blob/496e0c1a2dfd829cf91f4496f47a1bf8796c1bca/src/axobench/metrics.py#L16-L16">Source</a></dd>
</dl>

</section>
