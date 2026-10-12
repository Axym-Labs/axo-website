---
title: axobench CLI
description: Every subcommand, option, and default of the axobench command.
section: AxoBench API
apiGroup: CLI
order: 320
---

## Usage

```bash
axobench <command> --help
```

The `axobench` command converts and inspects data and writes diagnostic rows; it does not load models. AxoSim checkpoints are evaluated with [`axosim-evaluate-model`](/api/axobench-cli/), and other models through the [Python evaluator](/axobench-api/evaluation/). Errors in file paths or values exit with status 2 and print the message.

## make-demo-data

Write deterministic synthetic shards for smoke tests.

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Output directory.</dd>
<dt><code>--samples</code> <span class="api-type">int</span> · default=8</dt>
<dd>Traces per shard.</dd>
<dt><code>--shards</code> <span class="api-type">int</span> · default=1</dt>
<dd>Number of shards.</dd>
<dt><code>--time-steps</code> <span class="api-type">int</span> · default=32</dt>
<dd>Steps per trace.</dd>
<dt><code>--input-dim</code> <span class="api-type">int</span> · default=64</dt>
<dd>Input channels.</dd>
<dt><code>--seed</code> <span class="api-type">int</span> · default=0</dt>
<dd>Random seed.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L41)

## make-arbor-hetero-data

Simulate heterogeneous Arbor cable cells into shards; requires the sim extra (Arbor 0.11).

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--config</code> <span class="api-type">str</span> · default=None</dt>
<dd>JSON file whose keys are option names of this command; explicit flags take precedence.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · default=None</dt>
<dd>Output directory; required unless set in --config.</dd>
<dt><code>--samples</code> <span class="api-type">int</span> · default=128</dt>
<dd>Traces when --splits is not given.</dd>
<dt><code>--shards</code> <span class="api-type">int</span> · default=1</dt>
<dd>Shards when --splits is not given.</dd>
<dt><code>--splits</code> <span class="api-type">str</span> · default=None</dt>
<dd>Comma-separated NAME:SAMPLES pairs written as separate split directories.</dd>
<dt><code>--shards-per-split</code> <span class="api-type">int</span> · default=1</dt>
<dd>Shards per split with --splits.</dd>
<dt><code>--time-steps</code> <span class="api-type">int</span> · default=6000</dt>
<dd>Steps per trace.</dd>
<dt><code>--input-dim</code> <span class="api-type">int</span> · default=1278</dt>
<dd>Input channels.</dd>
<dt><code>--branches</code> <span class="api-type">int</span> · default=45</dt>
<dd>Dendritic branches of the cable cell.</dd>
<dt><code>--integration-dt-ms</code> <span class="api-type">float</span> · default=0.025</dt>
<dd>Simulator integration step in ms.</dd>
<dt><code>--input-protocol</code> <span class="api-type">str</span> · default=&#x27;arbor_poisson&#x27;</dt>
<dd>Input event generator. Choices: arbor_poisson, neuronio_smoothed.</dd>
<dt><code>--synapse-routing</code> <span class="api-type">str</span> · default=&#x27;branch&#x27;</dt>
<dd>Synapse placement: one site per branch, or distributed sites. Choices: branch, distributed.</dd>
<dt><code>--distributed-sites-per-polarity</code> <span class="api-type">int</span> · default=None</dt>
<dd>Sites per sign with distributed routing.</dd>
<dt><code>--spike-label-mode</code> <span class="api-type">str</span> · default=&#x27;threshold_crossing&#x27;</dt>
<dd>How output spikes are labeled. Choices: threshold_crossing, local_peak.</dd>
<dt><code>--spike-peak-threshold-mv</code> <span class="api-type">float</span> · default=-25.0</dt>
<dd>Voltage threshold of spike labels in mV.</dd>
<dt><code>--base-event-rate-hz</code> <span class="api-type">float</span> · default=2.0</dt>
<dd>Baseline input event rate in Hz.</dd>
<dt><code>--burst-probability</code> <span class="api-type">float</span> · default=0.015</dt>
<dd>Probability of an input burst.</dd>
<dt><code>--burst-event-rate-hz</code> <span class="api-type">float</span> · default=35.0</dt>
<dd>Input event rate during bursts in Hz.</dd>
<dt><code>--arbor-gpu-id</code> <span class="api-type">int</span> · default=0</dt>
<dd>GPU used by Arbor.</dd>
<dt><code>--cpu-only</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Use Arbor&#x27;s CPU context.</dd>
<dt><code>--arbor-threads</code> <span class="api-type">int</span> · default=1</dt>
<dd>Arbor CPU threads.</dd>
<dt><code>--sim-batch-size</code> <span class="api-type">int</span> · default=32</dt>
<dd>Independent cells per Arbor simulation.</dd>
<dt><code>--seed</code> <span class="api-type">int</span> · default=0</dt>
<dd>Random seed.</dd>
<dt><code>--param-overrides</code> <span class="api-type">str</span> · default=None</dt>
<dd>JSON object, or a path to one, overriding heterogeneity parameters for all traces.</dd>
<dt><code>--report</code> <span class="api-type">str</span> · default=None</dt>
<dd>Optional path for a copy of the generation report.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L49)

## convert-neuronio

Convert raw NeuronIO pickles to deterministic shards.

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--input</code> <span class="api-type">str</span> · required</dt>
<dd>Raw file or directory searched for *sim__* files.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Output directory.</dd>
<dt><code>--shard-size</code> <span class="api-type">int</span> · default=128</dt>
<dd>Traces per shard.</dd>
<dt><code>--window-size</code> <span class="api-type">int</span> · default=None</dt>
<dd>Optional window length.</dd>
<dt><code>--window-stride</code> <span class="api-type">int</span> · default=None</dt>
<dd>Window stride; defaults to the window length.</dd>
<dt><code>--ignore-start</code> <span class="api-type">int</span> · default=0</dt>
<dd>First window start when windowing.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L82)

## repack-shards

Repack shards as sliceable .npy arrays with a manifest.

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--input</code> <span class="api-type">str</span> · required</dt>
<dd>Source split directory.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Destination directory.</dd>
<dt><code>--input-dtype</code> <span class="api-type">str</span> · default=&#x27;int8&#x27;</dt>
<dd>Storage dtype of the inputs; values must be preserved. Choices: int8, float32.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L90)

## benchmark-profile

Print an axis/default profile as JSON.

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--name</code> <span class="api-type">str</span> · default=&#x27;paper-default&#x27;</dt>
<dd>Profile name. Choices: smoke, paper-default, teacher-screen.</dd>
<dt><code>--plan</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Print the expanded axis-composition plan.</dd>
<dt><code>--cost</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Print only the local capacity estimate.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L95)

## dataset-schema

Print the v1 manifest template or the diagnostic suite catalog as JSON.

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--kind</code> <span class="api-type">str</span> · default=&#x27;manifest&#x27;</dt>
<dd>manifest for the template, diagnostics for the suite catalog. Choices: manifest, diagnostics.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L100)

## benchmark-rows

Write teacher QC or teacher intervention rows for an evaluation root.

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--mode</code> <span class="api-type">str</span> · default=&#x27;teacher-qc&#x27;</dt>
<dd>teacher-qc rows or intervention rows. Choices: teacher-qc, intervention.</dd>
<dt><code>--dataset-root</code> <span class="api-type">str</span> · required</dt>
<dd>Evaluation root.</dd>
<dt><code>--selector</code> <span class="api-type">str</span> · default=&#x27;val&#x27;</dt>
<dd>Read val or an intervention condition. Choices: val, intervention.</dd>
<dt><code>--intervention</code> <span class="api-type">str</span> · default=&#x27;event_dropout&#x27;</dt>
<dd>Condition name with --selector intervention.</dd>
<dt><code>--pair-path</code> <span class="api-type">str</span> · default=None</dt>
<dd>Pair file outside the v1 layout; used with --mode intervention.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Rows file: .json, .jsonl, or .csv.</dd>
<dt><code>--summary-output</code> <span class="api-type">str</span> · default=None</dt>
<dd>Optional summary: .md or .json.</dd>
<dt><code>--suites</code> <span class="api-type">str</span> · default=&#x27;teacher-qc&#x27;</dt>
<dd>Comma-separated suites.</dd>
<dt><code>--morphology-id</code> <span class="api-type">str</span> · default=&#x27;unknown&#x27;</dt>
<dd>Morphology label of the rows.</dd>
<dt><code>--teacher-id</code> <span class="api-type">str</span> · default=&#x27;teacher&#x27;</dt>
<dd>Teacher label.</dd>
<dt><code>--max-samples</code> <span class="api-type">int</span> · default=None</dt>
<dd>Maximum traces or pairs, read from the start.</dd>
<dt><code>--cache-shards</code> <span class="api-type">int</span> · default=1</dt>
<dd>Decoded shards kept in memory.</dd>
<dt><code>--ignore-start</code> <span class="api-type">int</span> · default=500</dt>
<dd>Initial steps excluded.</dd>
<dt><code>--soma-scale</code> <span class="api-type">float</span> · default=0.1</dt>
<dd>Scale of the soma target coordinate.</dd>
<dt><code>--soma-bias-mv</code> <span class="api-type">float</span> · default=-67.7</dt>
<dd>Millivolt offset of the soma target coordinate.</dd>
<dt><code>--calibrated-spike-threshold</code> <span class="api-type">float</span> · default=None</dt>
<dd>Spike threshold recorded with the rows.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L106)

## diagnostic-audits

Derive audit rows from saved comparison artifacts.

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--teacher-grounded-rows</code> <span class="api-type">str</span> · default=None</dt>
<dd>Teacher-grounded comparison rows.</dd>
<dt><code>--local-stability-rows</code> <span class="api-type">str</span> · default=None</dt>
<dd>Local stability rows.</dd>
<dt><code>--perturbation-rows</code> <span class="api-type">str</span> · default=None</dt>
<dd>Perturbation rows.</dd>
<dt><code>--pretrained-summary-rows</code> <span class="api-type">str</span> · default=None</dt>
<dd>Pretrained-model summary rows.</dd>
<dt><code>--teacher-protocol</code> <span class="api-type">str</span> · default=None</dt>
<dd>Teacher protocol JSON.</dd>
<dt><code>--output</code> <span class="api-type">str</span> · required</dt>
<dd>Rows file: .json, .jsonl, or .csv.</dd>
<dt><code>--summary-output</code> <span class="api-type">str</span> · default=None</dt>
<dd>Optional summary: .md or .json.</dd>
<dt><code>--suites</code> <span class="api-type">str</span> · default=&#x27;metric-decoupling,target-view-audit,robustness-directionality,protocol-coverage,adapter-fairness,paper-summary&#x27;</dt>
<dd>Comma-separated audit suites.</dd>
<dt><code>--model-id</code> <span class="api-type">str</span> · default=&#x27;analysis&#x27;</dt>
<dd>Model label.</dd>
<dt><code>--teacher-id</code> <span class="api-type">str</span> · default=&#x27;teacher&#x27;</dt>
<dd>Teacher label.</dd>
<dt><code>--morphology-id</code> <span class="api-type">str</span> · default=&#x27;mixed&#x27;</dt>
<dd>Morphology label.</dd>
<dt><code>--split</code> <span class="api-type">str</span> · default=&#x27;analysis&#x27;</dt>
<dd>Split label.</dd>
<dt><code>--condition</code> <span class="api-type">str</span> · default=&#x27;analysis&#x27;</dt>
<dd>Condition label.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L127)

## diagnostic-plots

Write the audit figures and tables from saved audit summaries.

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--canonical-summary</code> <span class="api-type">str</span> · required</dt>
<dd>Canonical audit summary JSON.</dd>
<dt><code>--mechanistic-summary</code> <span class="api-type">str</span> · required</dt>
<dd>Mechanistic response summary JSON.</dd>
<dt><code>--sparse-event-summary</code> <span class="api-type">str</span> · required</dt>
<dd>Sparse-event sensitivity summary JSON.</dd>
<dt><code>--point-rows</code> <span class="api-type">str</span> · required</dt>
<dd>Point metric rows.</dd>
<dt><code>--tcn-summary</code> <span class="api-type">str, repeatable</span> · required</dt>
<dd>TCN preprocessing summary JSON; repeatable.</dd>
<dt><code>--morphology-contrast-rows</code> <span class="api-type">str</span> · default=None</dt>
<dd>Optional morphology contrast rows.</dd>
<dt><code>--neuronio-intervention-rows</code> <span class="api-type">str</span> · default=None</dt>
<dd>Optional NeuronIO intervention rows.</dd>
<dt><code>--neuronio-intervention-root</code> <span class="api-type">str</span> · default=None</dt>
<dd>Optional NeuronIO intervention directory.</dd>
<dt><code>--output-dir</code> <span class="api-type">str</span> · required</dt>
<dd>Output directory.</dd>
<dt><code>--formats</code> <span class="api-type">str</span> · default=&#x27;svg,pdf,png&#x27;</dt>
<dd>Comma-separated figure formats.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L148)

## benchmark-v1

Run the teacher bundle on an evaluation root: QC, routing, intervention, and morphology-contrast rows.

<p class="api-label">Options</p>

<dl class="api-parameters">
<dt><code>--dataset-root</code> <span class="api-type">str</span> · required</dt>
<dd>Evaluation root.</dd>
<dt><code>--output-dir</code> <span class="api-type">str</span> · required</dt>
<dd>Output directory.</dd>
<dt><code>--suite</code> <span class="api-type">str</span> · default=&#x27;paper-summary&#x27;</dt>
<dd>Suite profile. Choices: teacher-qc, paper-summary, full.</dd>
<dt><code>--intervention-pair-glob</code> <span class="api-type">str, repeatable</span> · default=[]</dt>
<dd>Glob of pair files outside the v1 layout; repeatable.</dd>
<dt><code>--morphology-id</code> <span class="api-type">str</span> · default=&#x27;unknown&#x27;</dt>
<dd>Morphology label of the val rows.</dd>
<dt><code>--teacher-id</code> <span class="api-type">str</span> · default=&#x27;teacher&#x27;</dt>
<dd>Teacher label.</dd>
<dt><code>--max-val-samples</code> <span class="api-type">int</span> · default=None</dt>
<dd>Maximum validation traces.</dd>
<dt><code>--max-intervention-samples</code> <span class="api-type">int</span> · default=None</dt>
<dd>Maximum pairs per condition and morphology.</dd>
<dt><code>--cache-shards</code> <span class="api-type">int</span> · default=1</dt>
<dd>Decoded shards kept in memory.</dd>
<dt><code>--ignore-start</code> <span class="api-type">int</span> · default=500</dt>
<dd>Initial steps excluded.</dd>
<dt><code>--soma-scale</code> <span class="api-type">float</span> · default=0.1</dt>
<dd>Scale of the soma target coordinate.</dd>
<dt><code>--soma-bias-mv</code> <span class="api-type">float</span> · default=-67.7</dt>
<dd>Millivolt offset of the soma target coordinate.</dd>
<dt><code>--calibrated-spike-threshold</code> <span class="api-type">float</span> · default=None</dt>
<dd>Spike threshold recorded with the rows.</dd>
<dt><code>--no-summaries</code> <span class="api-type">flag</span> · default=True</dt>
<dd>Write only machine-readable rows and the manifest.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axobench/blob/22e52ec6c0230edccf608076a9a1cdfd0011d5d8/src/axobench/cli.py#L163)
