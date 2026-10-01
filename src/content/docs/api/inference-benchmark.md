---
title: Inference benchmarking
description: Signatures, parameters, return contracts, and source for inference benchmarking.
section: API reference
apiGroup: Training and evaluation
order: 219
---

## Overview

The benchmark measures model sequence execution across batch sizes, horizons, and precision choices. It does not include the complete connected population runtime. Preserve the warmup, repetitions, synchronization, compilation mode, device, and shape contract with every reported timing.

Source revision: `306a51ed950b`. [Public export index](/api/).

<section class="api-symbol" id="inference-benchmark-benchmark-inference-matrix">

## benchmark_inference_matrix

<div class="api-signature">

```python
axosim.inference_benchmark.benchmark_inference_matrix(model: torch.nn.Module, *, batch_sizes: Iterable[int], time_steps: Iterable[int], input_dim: int, device: str='cpu', precision: str='float32', warmup_runs: int=5, runs: int=20, compile_model: bool=False, accuracy_metrics_path: str | Path | None=None) -> dict[str, Any]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/inference_benchmark.py#L12-L103)

</div>

Benchmark dense full-window inference for deployment-oriented comparisons.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">torch.nn.Module</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
<dt><code>batch_sizes</code> <span class="api-type">Iterable[int]</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Batch sizes included in the benchmark matrix.</dd>
<dt><code>time_steps</code> <span class="api-type">Iterable[int]</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Native sequence horizon.</dd>
<dt><code>input_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Native input-channel count.</dd>
<dt><code>device</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;cpu&#x27;.</span> Execution or allocation device.</dd>
<dt><code>precision</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;float32&#x27;.</span> Floating-point execution precision.</dd>
<dt><code>warmup_runs</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=5.</span> Unmeasured iterations before the timing repetitions.</dd>
<dt><code>runs</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, default=20.</span> Measured repetitions after the declared warmup.</dd>
<dt><code>compile_model</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Enable the benchmark&#x27;s compilation path.</dd>
<dt><code>accuracy_metrics_path</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional metrics JSON included with the inference timing report.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>report</code> <span class="api-type">dict[str, Any]</span></dt>
<dd>Timing rows for each batch/horizon pair, device/precision and repetition settings, resident parameter count, optional accuracy metadata, and the fastest successful row. Out-of-memory rows contain error details.</dd>
</dl>

</section>

<section class="api-symbol" id="inference-benchmark-count-parameters">

## count_parameters

<div class="api-signature">

```python
axosim.inference_benchmark.count_parameters(model: torch.nn.Module) -> int
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/inference_benchmark.py#L106-L107)

</div>

Count all resident model parameter elements, including frozen parameters.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">torch.nn.Module</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>count</code> <span class="api-type">int</span></dt>
<dd>Sum of numel() over every model parameter, independent of requires_grad.</dd>
</dl>

</section>

<section class="api-symbol" id="inference-benchmark-write-inference-benchmark">

## write_inference_benchmark

<div class="api-signature">

```python
axosim.inference_benchmark.write_inference_benchmark(report: dict[str, Any], path: str | Path) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/inference_benchmark.py#L110-L113)

</div>

Write the inference timing report as JSON, creating the parent directory when needed.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>report</code> <span class="api-type">dict[str, Any]</span></dt>
<dd><span class="api-default">required.</span> Inference benchmark report to serialize.</dd>
<dt><code>path</code> <span class="api-type">str | Path</span></dt>
<dd><span class="api-default">required.</span> Filesystem location to read or write; see the operation&#x27;s persistence contract.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-symbol" id="inference-benchmark-parse-int-list">

## parse_int_list

<div class="api-signature">

```python
axosim.inference_benchmark.parse_int_list(value: str) -> list[int]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/inference_benchmark.py#L116-L120)

</div>

Parse a comma-separated integer list, ignoring empty entries and rejecting an empty result.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>value</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Comma-separated string of integer values.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>values</code> <span class="api-type">list[int]</span></dt>
<dd>Parsed integers in their original order.</dd>
</dl>

</section>
