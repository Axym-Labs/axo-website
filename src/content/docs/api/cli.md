---
title: AxoSim CLI
description: Complete options and defaults for axosim.
section: API reference
apiGroup: CLI
order: 240
---

## Usage

```bash
axosim --help
```

Every command and subcommand accepts `-h` or `--help`. The option reference below includes exact parser defaults, choices, required arguments, and compatibility options hidden from ordinary help.

A subcommand is required. Named presets replace their declared defaults, while explicitly supplied flags take precedence. Boolean defaults refer to the destination value: for example, `--blocking-transfer` sets `non_blocking=False`.

## axosim make-demo-data

write deterministic demo NPZ shards

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: output.</dd>
<dt><code>--samples</code> <span class="api-type">int</span> · default=8</dt>
<dd>Destination: samples.</dd>
<dt><code>--shards</code> <span class="api-type">int</span> · default=1</dt>
<dd>Destination: shards.</dd>
<dt><code>--time-steps</code> <span class="api-type">int</span> · default=32</dt>
<dd>Native sequence horizon.</dd>
<dt><code>--input-dim</code> <span class="api-type">int</span> · default=64</dt>
<dd>Native input-channel count.</dd>
<dt><code>--seed</code> <span class="api-type">int</span> · default=0</dt>
<dd>Random seed for the declared operation.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L61)

## axosim convert-neuronio

convert raw NeuronIO pickle files to deterministic shards

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>--input</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: input.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: output.</dd>
<dt><code>--shard-size</code> <span class="api-type">int</span> · default=128</dt>
<dd>Maximum sample count in each converted shard.</dd>
<dt><code>--window-size</code> <span class="api-type">int</span> · default=None</dt>
<dd>Native timesteps per extracted window.</dd>
<dt><code>--window-stride</code> <span class="api-type">int</span> · default=None</dt>
<dd>Native timestep distance between successive window starts.</dd>
<dt><code>--ignore-start</code> <span class="api-type">int</span> · default=0</dt>
<dd>Initial native timesteps excluded by the declared path.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L69)

## axosim repack-shards

repack shards as sliceable .npy arrays

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>--input</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: input.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: output.</dd>
<dt><code>--input-dtype</code> <span class="api-type">str</span> · default=&#x27;int8&#x27;</dt>
<dd>Stored NumPy dtype of the converted input arrays. Choices: [&#x27;int8&#x27;, &#x27;float32&#x27;].</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L77)

## axosim list-presets

list named train/evaluate presets

No additional arguments are required; this command prints the named recipes as JSON.

## axosim evaluate

evaluate a model with the corrected full-trace metric path

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>--preset</code> <span class="api-type">str</span> · default=None</dt>
<dd>Choices: [&#x27;fulltrace-paper-metric&#x27;, &#x27;legacy-baseline-smoke&#x27;].</dd>
<dt><code>--data</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: data.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: output.</dd>
<dt><code>--input-dim</code> <span class="api-type">int</span> · default=1278</dt>
<dd>Native input-channel count.</dd>
<dt><code>--memory-units</code> <span class="api-type">int</span> · default=30</dt>
<dd>Width of the recurrent memory state.</dd>
<dt><code>--branches</code> <span class="api-type">int</span> · default=32</dt>
<dd>Number of routed branch features in the adapter.</dd>
<dt><code>--model-kind</code> <span class="api-type">str</span> · default=&#x27;baseline&#x27;</dt>
<dd>use &#x27;official&#x27; for the paper-style model, &#x27;axomamba&#x27; for the promoted Mamba surrogate, &#x27;mamba-official&#x27; for the generic official mamba-ssm backend, or &#x27;branch-trace-rnn&#x27; for the RNN comparison path; &#x27;baseline&#x27; is legacy/debug Choices: [&#x27;baseline&#x27;, &#x27;official&#x27;, &#x27;axomamba&#x27;, &#x27;mamba-official&#x27;, &#x27;mamba-pytorch&#x27;, &#x27;branch-mamba-pytorch&#x27;, &#x27;branch-trace-rnn&#x27;].</dd>
<dt><code>--model-config</code> <span class="api-type">str</span> · default=&#x27;configs/branch_elm_30_official.json&#x27;</dt>
<dd>Destination: model_config.</dd>
<dt><code>--batch-size</code> <span class="api-type">int</span> · default=8</dt>
<dd>Examples processed per batch.</dd>
<dt><code>--seed</code> <span class="api-type">int</span> · default=0</dt>
<dd>Random seed for the declared operation.</dd>
<dt><code>--device</code> <span class="api-type">str</span> · default=&#x27;cpu&#x27;</dt>
<dd>Execution or allocation device.</dd>
<dt><code>--checkpoint</code> <span class="api-type">str</span> · default=None</dt>
<dd>Upstream baseline checkpoint file.</dd>
<dt><code>--window-size</code> <span class="api-type">int</span> · default=None</dt>
<dd>Native timesteps per extracted window.</dd>
<dt><code>--window-stride</code> <span class="api-type">int</span> · default=None</dt>
<dd>Native timestep distance between successive window starts.</dd>
<dt><code>--ignore-start</code> <span class="api-type">int</span> · default=0</dt>
<dd>Initial native timesteps excluded by the declared path.</dd>
<dt><code>--cache-shards</code> <span class="api-type">int</span> · default=1</dt>
<dd>Maximum cached shards; zero disables the cache.</dd>
<dt><code>--soma-units</code> <span class="api-type">str</span> · default=&#x27;millivolts&#x27;</dt>
<dd>Coordinate convention used when computing the local soma metric. Choices: [&#x27;millivolts&#x27;, &#x27;normalized&#x27;].</dd>
<dt><code>--metric-ignore-start</code> <span class="api-type">int</span> · default=0</dt>
<dd>Destination: metric_ignore_start.</dd>
<dt><code>--metric-mask-mode</code> <span class="api-type">str</span> · default=&#x27;ignore-start&#x27;</dt>
<dd>Compatibility option hidden from default help. Choices: [&#x27;ignore-start&#x27;, &#x27;official-overlap&#x27;].</dd>
<dt><code>--metric-stitch-burn-in</code> <span class="api-type">int</span> · default=150</dt>
<dd>Compatibility option hidden from default help.</dd>
<dt><code>--soma-affine-calibration</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Rescale predictions to the evaluation targets&#x27; mean and standard deviation; declare this calibration when comparing metrics. Sets soma_affine_calibration=True.</dd>
<dt><code>--pin-memory</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Stage CPU arrays in pinned memory before a CUDA transfer. Sets pin_memory=True.</dd>
<dt><code>--blocking-transfer</code> <span class="api-type">flag</span> · default=True</dt>
<dd>Request asynchronous tensor transfers where supported. Sets non_blocking=False.</dd>
<dt><code>--registry</code> <span class="api-type">str</span> · default=None</dt>
<dd>append a one-line JSONL record; defaults to &lt;output-dir&gt;/experiment-registry.jsonl</dd>
<dt><code>--no-registry</code> <span class="api-type">flag</span> · default=None</dt>
<dd>Sets registry=&#x27;off&#x27;.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L84)

## axosim diagnose

write biology-oriented surrogate fidelity diagnostics

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>--preset</code> <span class="api-type">str</span> · default=None</dt>
<dd>Choices: [&#x27;fulltrace-paper-metric&#x27;, &#x27;legacy-baseline-smoke&#x27;].</dd>
<dt><code>--data</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: data.</dd>
<dt><code>--output-dir</code> <span class="api-type">str</span> · required</dt>
<dd>Directory receiving converted shards and their manifest.</dd>
<dt><code>--input-dim</code> <span class="api-type">int</span> · default=1278</dt>
<dd>Native input-channel count.</dd>
<dt><code>--memory-units</code> <span class="api-type">int</span> · default=30</dt>
<dd>Width of the recurrent memory state.</dd>
<dt><code>--branches</code> <span class="api-type">int</span> · default=32</dt>
<dd>Number of routed branch features in the adapter.</dd>
<dt><code>--model-kind</code> <span class="api-type">str</span> · default=&#x27;baseline&#x27;</dt>
<dd>Checkpoint architecture/backend discriminator. Choices: [&#x27;baseline&#x27;, &#x27;official&#x27;, &#x27;axomamba&#x27;, &#x27;mamba-official&#x27;, &#x27;mamba-pytorch&#x27;, &#x27;branch-mamba-pytorch&#x27;, &#x27;branch-trace-rnn&#x27;].</dd>
<dt><code>--model-config</code> <span class="api-type">str</span> · default=&#x27;configs/branch_elm_30_official.json&#x27;</dt>
<dd>Destination: model_config.</dd>
<dt><code>--batch-size</code> <span class="api-type">int</span> · default=8</dt>
<dd>Examples processed per batch.</dd>
<dt><code>--seed</code> <span class="api-type">int</span> · default=0</dt>
<dd>Random seed for the declared operation.</dd>
<dt><code>--device</code> <span class="api-type">str</span> · default=&#x27;cpu&#x27;</dt>
<dd>Execution or allocation device.</dd>
<dt><code>--checkpoint</code> <span class="api-type">str</span> · default=None</dt>
<dd>Upstream baseline checkpoint file.</dd>
<dt><code>--window-size</code> <span class="api-type">int</span> · default=None</dt>
<dd>Native timesteps per extracted window.</dd>
<dt><code>--window-stride</code> <span class="api-type">int</span> · default=None</dt>
<dd>Native timestep distance between successive window starts.</dd>
<dt><code>--ignore-start</code> <span class="api-type">int</span> · default=0</dt>
<dd>Initial native timesteps excluded by the declared path.</dd>
<dt><code>--cache-shards</code> <span class="api-type">int</span> · default=1</dt>
<dd>Maximum cached shards; zero disables the cache.</dd>
<dt><code>--metric-ignore-start</code> <span class="api-type">int</span> · default=0</dt>
<dd>Destination: metric_ignore_start.</dd>
<dt><code>--metric-mask-mode</code> <span class="api-type">str</span> · default=&#x27;ignore-start&#x27;</dt>
<dd>Compatibility option hidden from default help. Choices: [&#x27;ignore-start&#x27;, &#x27;official-overlap&#x27;].</dd>
<dt><code>--metric-stitch-burn-in</code> <span class="api-type">int</span> · default=150</dt>
<dd>Compatibility option hidden from default help.</dd>
<dt><code>--soma-affine-calibration</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Rescale predictions to the evaluation targets&#x27; mean and standard deviation; declare this calibration when comparing metrics. Sets soma_affine_calibration=True.</dd>
<dt><code>--max-samples</code> <span class="api-type">int</span> · default=None</dt>
<dd>Destination: max_samples.</dd>
<dt><code>--pin-memory</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Stage CPU arrays in pinned memory before a CUDA transfer. Sets pin_memory=True.</dd>
<dt><code>--blocking-transfer</code> <span class="api-type">flag</span> · default=True</dt>
<dd>Request asynchronous tensor transfers where supported. Sets non_blocking=False.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L112)

## axosim train

train a model with the current experiment workflow

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>--preset</code> <span class="api-type">str</span> · default=None</dt>
<dd>Choices: [&#x27;axomamba-probe&#x27;, &#x27;legacy-baseline-smoke&#x27;, &#x27;mamba-official-probe&#x27;, &#x27;mamba2-official-probe&#x27;, &#x27;official-fulltrace-reference&#x27;, &#x27;paper-random-fulltrace&#x27;].</dd>
<dt><code>--data</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: data.</dd>
<dt><code>--checkpoint</code> <span class="api-type">str</span> · required</dt>
<dd>Upstream baseline checkpoint file.</dd>
<dt><code>--metrics</code> <span class="api-type">str</span> · required</dt>
<dd>Metrics dictionary to serialize.</dd>
<dt><code>--input-dim</code> <span class="api-type">int</span> · default=1278</dt>
<dd>Native input-channel count.</dd>
<dt><code>--memory-units</code> <span class="api-type">int</span> · default=30</dt>
<dd>Width of the recurrent memory state.</dd>
<dt><code>--branches</code> <span class="api-type">int</span> · default=32</dt>
<dd>Number of routed branch features in the adapter.</dd>
<dt><code>--model-kind</code> <span class="api-type">str</span> · default=&#x27;baseline&#x27;</dt>
<dd>use &#x27;official&#x27; for the paper-style model, &#x27;axomamba&#x27; for the promoted Mamba surrogate, &#x27;mamba-official&#x27; for the generic official mamba-ssm backend, or &#x27;branch-trace-rnn&#x27; for the RNN comparison path; &#x27;baseline&#x27; is legacy/debug Choices: [&#x27;baseline&#x27;, &#x27;official&#x27;, &#x27;axomamba&#x27;, &#x27;mamba-official&#x27;, &#x27;mamba-pytorch&#x27;, &#x27;branch-mamba-pytorch&#x27;, &#x27;branch-trace-rnn&#x27;].</dd>
<dt><code>--model-config</code> <span class="api-type">str</span> · default=&#x27;configs/branch_elm_30_official.json&#x27;</dt>
<dd>Destination: model_config.</dd>
<dt><code>--epochs</code> <span class="api-type">int</span> · default=1</dt>
<dd>Number of passes over the declared epoch sampling budget.</dd>
<dt><code>--batch-size</code> <span class="api-type">int</span> · default=8</dt>
<dd>Examples processed per batch.</dd>
<dt><code>--learning-rate</code> <span class="api-type">float</span> · default=0.0005</dt>
<dd>Optimizer step size.</dd>
<dt><code>--burn-in</code> <span class="api-type">int</span> · default=0</dt>
<dd>Initial timesteps excluded from training losses.</dd>
<dt><code>--seed</code> <span class="api-type">int</span> · default=0</dt>
<dd>Random seed for the declared operation.</dd>
<dt><code>--device</code> <span class="api-type">str</span> · default=&#x27;cpu&#x27;</dt>
<dd>Execution or allocation device.</dd>
<dt><code>--window-size</code> <span class="api-type">int</span> · default=None</dt>
<dd>Native timesteps per extracted window.</dd>
<dt><code>--window-stride</code> <span class="api-type">int</span> · default=None</dt>
<dd>Native timestep distance between successive window starts.</dd>
<dt><code>--ignore-start</code> <span class="api-type">int</span> · default=0</dt>
<dd>Initial native timesteps excluded by the declared path.</dd>
<dt><code>--window-sampling</code> <span class="api-type">str</span> · default=&#x27;random-full-trace&#x27;</dt>
<dd>Choices: [&#x27;deterministic&#x27;, &#x27;random-full-trace&#x27;, &#x27;official-full-trace&#x27;].</dd>
<dt><code>--epoch-samples</code> <span class="api-type">int</span> · default=None</dt>
<dd>Destination: epoch_samples.</dd>
<dt><code>--shard-reuse-batches</code> <span class="api-type">int</span> · default=1</dt>
<dd>Number of consecutive batches sampled before advancing to another shard.</dd>
<dt><code>--file-load-fraction</code> <span class="api-type">float</span> · default=0.3</dt>
<dd>Fraction of each shard made available to the sampling path.</dd>
<dt><code>--full-trace-length</code> <span class="api-type">int</span> · default=None</dt>
<dd>Destination: full_trace_length.</dd>
<dt><code>--sample-window-reads</code> <span class="api-type">flag</span> · default=False</dt>
<dd>read random/official windows by sample instead of caching full compressed shards Sets sample_window_reads=True.</dd>
<dt><code>--shuffle-mode</code> <span class="api-type">str</span> · default=&#x27;shard&#x27;</dt>
<dd>Choose sample-level or shard-level reordering. Choices: [&#x27;sample&#x27;, &#x27;shard&#x27;, &#x27;none&#x27;].</dd>
<dt><code>--cache-shards</code> <span class="api-type">int</span> · default=1</dt>
<dd>Maximum cached shards; zero disables the cache.</dd>
<dt><code>--val-data</code> <span class="api-type">str</span> · default=None</dt>
<dd>Destination: val_data.</dd>
<dt><code>--val-batch-size</code> <span class="api-type">int</span> · default=None</dt>
<dd>Destination: val_batch_size.</dd>
<dt><code>--val-cache-shards</code> <span class="api-type">int</span> · default=1</dt>
<dd>Destination: val_cache_shards.</dd>
<dt><code>--val-window-size</code> <span class="api-type">int</span> · default=None</dt>
<dd>Destination: val_window_size.</dd>
<dt><code>--val-window-stride</code> <span class="api-type">int</span> · default=None</dt>
<dd>Destination: val_window_stride.</dd>
<dt><code>--val-ignore-start</code> <span class="api-type">int</span> · default=0</dt>
<dd>Destination: val_ignore_start.</dd>
<dt><code>--val-soma-units</code> <span class="api-type">str</span> · default=&#x27;millivolts&#x27;</dt>
<dd>Choices: [&#x27;millivolts&#x27;, &#x27;normalized&#x27;].</dd>
<dt><code>--val-metric-ignore-start</code> <span class="api-type">int</span> · default=500</dt>
<dd>Destination: val_metric_ignore_start.</dd>
<dt><code>--val-metric-mask-mode</code> <span class="api-type">str</span> · default=&#x27;ignore-start&#x27;</dt>
<dd>Compatibility option hidden from default help. Choices: [&#x27;ignore-start&#x27;, &#x27;official-overlap&#x27;].</dd>
<dt><code>--val-metric-stitch-burn-in</code> <span class="api-type">int</span> · default=150</dt>
<dd>Compatibility option hidden from default help.</dd>
<dt><code>--val-soma-affine-calibration</code> <span class="api-type">flag</span> · default=True</dt>
<dd>Sets val_soma_affine_calibration=True.</dd>
<dt><code>--no-val-soma-affine-calibration</code> <span class="api-type">flag</span> · default=True</dt>
<dd>Sets val_soma_affine_calibration=False.</dd>
<dt><code>--best-checkpoint</code> <span class="api-type">str</span> · default=None</dt>
<dd>Destination: best_checkpoint.</dd>
<dt><code>--max-train-batches</code> <span class="api-type">int</span> · default=None</dt>
<dd>Optional cap on batches in each training epoch.</dd>
<dt><code>--lr-schedule</code> <span class="api-type">str</span> · default=&#x27;constant&#x27;</dt>
<dd>Learning-rate schedule selection. Choices: [&#x27;constant&#x27;, &#x27;cosine&#x27;].</dd>
<dt><code>--lr-schedule-steps</code> <span class="api-type">int</span> · default=None</dt>
<dd>Number of optimizer steps used to parameterize the schedule.</dd>
<dt><code>--optimizer</code> <span class="api-type">str</span> · default=&#x27;adam&#x27;</dt>
<dd>Optimizer attached to the selected parameters. Choices: [&#x27;adam&#x27;, &#x27;adamw&#x27;].</dd>
<dt><code>--weight-decay</code> <span class="api-type">float</span> · default=0.0</dt>
<dd>Optimizer regularization coefficient.</dd>
<dt><code>--l1-lambda</code> <span class="api-type">float</span> · default=0.0</dt>
<dd>Coefficient of the L1 penalty on model parameters.</dd>
<dt><code>--spike-loss-weight</code> <span class="api-type">float</span> · default=0.5</dt>
<dd>Multiplier applied to the spike training loss.</dd>
<dt><code>--soma-loss-weight</code> <span class="api-type">float</span> · default=0.5</dt>
<dd>Multiplier applied to the soma training loss.</dd>
<dt><code>--sparse-soma-loss-weight</code> <span class="api-type">float</span> · default=0.0</dt>
<dd>Coefficient of auxiliary soma MSE over teacher-defined high-importance timesteps.</dd>
<dt><code>--sparse-soma-high-voltage-quantile</code> <span class="api-type">float</span> · default=0.9</dt>
<dd>Teacher-voltage quantile used to select high-voltage timesteps.</dd>
<dt><code>--sparse-soma-high-dvdt-quantile</code> <span class="api-type">float</span> · default=0.9</dt>
<dd>Absolute teacher-voltage difference quantile used to select rapidly changing timesteps.</dd>
<dt><code>--sparse-soma-input-event-quantile</code> <span class="api-type">float</span> · default=0.95</dt>
<dd>Positive input-activity quantile used to select event-adjacent timesteps.</dd>
<dt><code>--sparse-soma-spike-window</code> <span class="api-type">int</span> · default=5</dt>
<dd>Symmetric native-timestep radius around reference spikes in the auxiliary mask.</dd>
<dt><code>--sparse-soma-post-event-window</code> <span class="api-type">int</span> · default=5</dt>
<dd>Causal native-timestep window after selected input events.</dd>
<dt><code>--sera-soma-loss-weight</code> <span class="api-type">float</span> · default=0.0</dt>
<dd>Coefficient of the relevance-weighted auxiliary soma loss.</dd>
<dt><code>--sera-soma-min-weight</code> <span class="api-type">float</span> · default=0.05</dt>
<dd>Minimum timestep weight in the relevance-weighted soma loss.</dd>
<dt><code>--sera-soma-relevance-power</code> <span class="api-type">float</span> · default=1.0</dt>
<dd>Exponent applied to the teacher-derived relevance weights.</dd>
<dt><code>--soma-slope-loss-weight</code> <span class="api-type">float</span> · default=0.0</dt>
<dd>Coefficient of squared error in adjacent-timestep soma differences.</dd>
<dt><code>--grad-clip-norm</code> <span class="api-type">float</span> · default=0.0</dt>
<dd>Maximum gradient norm when clipping is enabled.</dd>
<dt><code>--train-update-log-interval</code> <span class="api-type">int</span> · default=0</dt>
<dd>Destination: train_update_log_interval.</dd>
<dt><code>--train-update-log</code> <span class="api-type">str</span> · default=None</dt>
<dd>Destination: train_update_log.</dd>
<dt><code>--prefetch-batches</code> <span class="api-type">int</span> · default=0</dt>
<dd>Number of dataset batches prepared ahead of consumption.</dd>
<dt><code>--pin-memory</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Stage CPU arrays in pinned memory before a CUDA transfer. Sets pin_memory=True.</dd>
<dt><code>--blocking-transfer</code> <span class="api-type">flag</span> · default=True</dt>
<dd>Request asynchronous tensor transfers where supported. Sets non_blocking=False.</dd>
<dt><code>--registry</code> <span class="api-type">str</span> · default=None</dt>
<dd>append a one-line JSONL record; defaults to &lt;metrics-dir&gt;/experiment-registry.jsonl</dd>
<dt><code>--no-registry</code> <span class="api-type">flag</span> · default=None</dt>
<dd>Sets registry=&#x27;off&#x27;.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L138)

## axosim benchmark

time model forward passes on random input

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>--input-dim</code> <span class="api-type">int</span> · default=1278</dt>
<dd>Native input-channel count.</dd>
<dt><code>--memory-units</code> <span class="api-type">int</span> · default=30</dt>
<dd>Width of the recurrent memory state.</dd>
<dt><code>--branches</code> <span class="api-type">int</span> · default=32</dt>
<dd>Number of routed branch features in the adapter.</dd>
<dt><code>--model-kind</code> <span class="api-type">str</span> · default=&#x27;baseline&#x27;</dt>
<dd>use &#x27;official&#x27; for the paper-style model, &#x27;mamba-official&#x27; for the official mamba-ssm backend, or &#x27;branch-trace-rnn&#x27; for the RNN comparison path; &#x27;baseline&#x27; is legacy/debug Choices: [&#x27;baseline&#x27;, &#x27;official&#x27;, &#x27;axomamba&#x27;, &#x27;mamba-official&#x27;, &#x27;mamba-pytorch&#x27;, &#x27;branch-mamba-pytorch&#x27;, &#x27;branch-trace-rnn&#x27;].</dd>
<dt><code>--model-config</code> <span class="api-type">str</span> · default=&#x27;configs/branch_elm_30_official.json&#x27;</dt>
<dd>Destination: model_config.</dd>
<dt><code>--batch-size</code> <span class="api-type">int</span> · default=1</dt>
<dd>Examples processed per batch.</dd>
<dt><code>--time-steps</code> <span class="api-type">int</span> · default=500</dt>
<dd>Native sequence horizon.</dd>
<dt><code>--runs</code> <span class="api-type">int</span> · default=10</dt>
<dd>Measured repetitions after the declared warmup.</dd>
<dt><code>--device</code> <span class="api-type">str</span> · default=&#x27;cpu&#x27;</dt>
<dd>Execution or allocation device.</dd>
<dt><code>--compile</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Enable the benchmark&#x27;s compilation path. Sets compile_model=True.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · default=None</dt>
<dd>Destination: output.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L214)

## axosim inference-benchmark

benchmark deployment-oriented inference throughput across batch and sequence scales

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>--input-dim</code> <span class="api-type">int</span> · default=1278</dt>
<dd>Native input-channel count.</dd>
<dt><code>--memory-units</code> <span class="api-type">int</span> · default=30</dt>
<dd>Width of the recurrent memory state.</dd>
<dt><code>--branches</code> <span class="api-type">int</span> · default=32</dt>
<dd>Number of routed branch features in the adapter.</dd>
<dt><code>--model-kind</code> <span class="api-type">str</span> · default=&#x27;baseline&#x27;</dt>
<dd>Checkpoint architecture/backend discriminator. Choices: [&#x27;baseline&#x27;, &#x27;official&#x27;, &#x27;axomamba&#x27;, &#x27;mamba-official&#x27;, &#x27;mamba-pytorch&#x27;, &#x27;branch-mamba-pytorch&#x27;, &#x27;branch-trace-rnn&#x27;].</dd>
<dt><code>--model-config</code> <span class="api-type">str</span> · default=&#x27;configs/branch_elm_30_official.json&#x27;</dt>
<dd>Destination: model_config.</dd>
<dt><code>--checkpoint</code> <span class="api-type">str</span> · default=None</dt>
<dd>Upstream baseline checkpoint file.</dd>
<dt><code>--batch-sizes</code> <span class="api-type">str</span> · default=&#x27;1,8,32,128&#x27;</dt>
<dd>Batch sizes included in the benchmark matrix.</dd>
<dt><code>--time-steps</code> <span class="api-type">str</span> · default=&#x27;500,1000,6000&#x27;</dt>
<dd>Native sequence horizon.</dd>
<dt><code>--runs</code> <span class="api-type">int</span> · default=20</dt>
<dd>Measured repetitions after the declared warmup.</dd>
<dt><code>--warmup-runs</code> <span class="api-type">int</span> · default=5</dt>
<dd>Unmeasured iterations before the timing repetitions.</dd>
<dt><code>--precision</code> <span class="api-type">str</span> · default=&#x27;float32&#x27;</dt>
<dd>Floating-point execution precision. Choices: [&#x27;float32&#x27;, &#x27;float16&#x27;, &#x27;bfloat16&#x27;].</dd>
<dt><code>--device</code> <span class="api-type">str</span> · default=&#x27;cpu&#x27;</dt>
<dd>Execution or allocation device.</dd>
<dt><code>--compile</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Enable the benchmark&#x27;s compilation path. Sets compile_model=True.</dd>
<dt><code>--accuracy-metrics</code> <span class="api-type">str</span> · default=None</dt>
<dd>Destination: accuracy_metrics.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: output.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L230)
