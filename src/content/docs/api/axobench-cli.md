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
<dd>Second checkpoint evaluated on the same traces as the paired baseline.</dd>
<dt><code>--baseline-cache</code> <span class="api-type">str</span> · default=None</dt>
<dd>Baseline cache written by --save-cache; its protocol, trace IDs, and target hash must match.</dd>
<dt><code>--save-cache</code> <span class="api-type">str</span> · default=None</dt>
<dd>Write this model&#x27;s predictions and protocol as a reusable .npz baseline cache.</dd>
<dt><code>--dataset-root</code> <span class="api-type">str</span> · required</dt>
<dd>AxoBench evaluation root containing val/ and optionally interventions/&lt;condition&gt;/.</dd>
<dt><code>--model-id</code> <span class="api-type">str</span> · default=None</dt>
<dd>Model name in the report; defaults to the checkpoint file stem.</dd>
<dt><code>--device</code> <span class="api-type">str</span> · default=&#x27;auto&#x27;</dt>
<dd>Execution or allocation device.</dd>
<dt><code>--batch-size</code> <span class="api-type">int</span> · default=128</dt>
<dd>Examples processed per batch.</dd>
<dt><code>--max-samples</code> <span class="api-type">int</span> · default=None</dt>
<dd>Validation traces to select; AxoBench defaults to 120.</dd>
<dt><code>--max-intervention-samples</code> <span class="api-type">int</span> · default=None</dt>
<dd>Pairs per intervention condition; AxoBench defaults to 40.</dd>
<dt><code>--max-interventions</code> <span class="api-type">int</span> · default=8</dt>
<dd>Maximum number of intervention conditions read in sorted order.</dd>
<dt><code>--intervention-workers</code> <span class="api-type">int</span> · default=4</dt>
<dd>Parallel CPU loaders for intervention shards.</dd>
<dt><code>--interventions</code> <span class="api-type">str</span> · default=None</dt>
<dd>comma-separated intervention names; default discovers all</dd>
<dt><code>--multiple-morphologies</code> <span class="api-type">flag</span> · default=False</dt>
<dd>balance the 120/40 evaluation profile across available morphologies Sets multiple_morphologies=True.</dd>
<dt><code>--morphology-id</code> <span class="api-type">str</span> · default=None</dt>
<dd>specific morphology for the default single-morphology evaluation</dd>
<dt><code>--ignore-start</code> <span class="api-type">int</span> · default=500</dt>
<dd>Initial native timesteps excluded by the declared path.</dd>
<dt><code>--calibration-fraction</code> <span class="api-type">float</span> · default=0.25</dt>
<dd>Share of the selected traces used only to calibrate the spike threshold.</dd>
<dt><code>--default-spike-threshold</code> <span class="api-type">float</span> · default=0.0</dt>
<dd>Uncalibrated threshold checked by the default_threshold_count diagnostic; it does not set the scoring threshold.</dd>
<dt><code>--bootstrap-replicates</code> <span class="api-type">int</span> · default=250</dt>
<dd>Replicates of the morphology-stratified paired bootstrap.</dd>
<dt><code>--bootstrap-seed</code> <span class="api-type">int</span> · default=20260711</dt>
<dd>Random seed of the paired bootstrap.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · default=None</dt>
<dd>optional .json or .csv report path</dd>
<dt><code>--output-json</code> <span class="api-type">str</span> · default=None</dt>
<dd>Compatibility option hidden from default help.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/caef7be03abdbde76ab00080ba7c4866da81278e/src/axosim/axobench_iteration.py#L205)
