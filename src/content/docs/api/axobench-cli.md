---
title: AxoBench evaluation CLI
description: Complete options and defaults for axosim-evaluate-model.
section: API reference
apiGroup: CLI
order: 242
---

## Usage

```bash
axosim-evaluate-model --help
```

Every command and subcommand accepts `-h` or `--help`. The option reference below includes exact parser defaults, choices, required arguments, and compatibility options hidden from ordinary help.

`--baseline-cache` and `--baseline-checkpoint` are mutually exclusive. `--output` and the compatibility alias `--output-json` are mutually exclusive. `--save-cache` cannot be combined with either baseline comparison path. The current AxoBench package is required for execution.

## axosim-evaluate-model

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>checkpoint</code> <span class="api-type">str</span> · required</dt>
<dd>Upstream baseline checkpoint file.</dd>
<dt><code>--baseline-checkpoint</code> <span class="api-type">str</span> · default=None</dt>
<dd>Destination: baseline_checkpoint.</dd>
<dt><code>--baseline-cache</code> <span class="api-type">str</span> · default=None</dt>
<dd>Destination: baseline_cache.</dd>
<dt><code>--save-cache</code> <span class="api-type">str</span> · default=None</dt>
<dd>Destination: save_cache.</dd>
<dt><code>--dataset-root</code> <span class="api-type">str</span> · required</dt>
<dd>Destination: dataset_root.</dd>
<dt><code>--model-id</code> <span class="api-type">str</span> · default=None</dt>
<dd>Destination: model_id.</dd>
<dt><code>--device</code> <span class="api-type">str</span> · default=&#x27;auto&#x27;</dt>
<dd>Execution or allocation device.</dd>
<dt><code>--batch-size</code> <span class="api-type">int</span> · default=128</dt>
<dd>Examples processed per batch.</dd>
<dt><code>--max-samples</code> <span class="api-type">int</span> · default=None</dt>
<dd>Destination: max_samples.</dd>
<dt><code>--max-intervention-samples</code> <span class="api-type">int</span> · default=None</dt>
<dd>Destination: max_intervention_samples.</dd>
<dt><code>--max-interventions</code> <span class="api-type">int</span> · default=8</dt>
<dd>Destination: max_interventions.</dd>
<dt><code>--intervention-workers</code> <span class="api-type">int</span> · default=4</dt>
<dd>Destination: intervention_workers.</dd>
<dt><code>--interventions</code> <span class="api-type">str</span> · default=None</dt>
<dd>comma-separated intervention names; default discovers all</dd>
<dt><code>--multiple-morphologies</code> <span class="api-type">flag</span> · default=False</dt>
<dd>balance the 120/40 evaluation profile across available morphologies Sets multiple_morphologies=True.</dd>
<dt><code>--morphology-id</code> <span class="api-type">str</span> · default=None</dt>
<dd>specific morphology for the default single-morphology evaluation</dd>
<dt><code>--ignore-start</code> <span class="api-type">int</span> · default=500</dt>
<dd>Initial native timesteps excluded by the declared path.</dd>
<dt><code>--calibration-fraction</code> <span class="api-type">float</span> · default=0.25</dt>
<dd>Destination: calibration_fraction.</dd>
<dt><code>--default-spike-threshold</code> <span class="api-type">float</span> · default=0.0</dt>
<dd>Destination: default_spike_threshold.</dd>
<dt><code>--bootstrap-replicates</code> <span class="api-type">int</span> · default=250</dt>
<dd>Destination: bootstrap_replicates.</dd>
<dt><code>--bootstrap-seed</code> <span class="api-type">int</span> · default=20260711</dt>
<dd>Destination: bootstrap_seed.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · default=None</dt>
<dd>optional .json or .csv report path</dd>
<dt><code>--output-json</code> <span class="api-type">str</span> · default=None</dt>
<dd>Compatibility option hidden from default help.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axobench_iteration.py#L205)
