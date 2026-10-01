---
title: Setup workflow
description: Signatures, parameters, return contracts, and source for setup workflow.
section: API reference
apiGroup: CLI
order: 221
---

## Overview

Setup planning separates the declared installation/download/conversion steps from execution. Default setup creates local directories and installs the checkout; downloads occur only when explicitly requested. A dry run prints the plan without executing its commands.

Source revision: `306a51ed950b`. [Public export index](/api/).

<section class="api-symbol" id="setup-workflow-datasetspec">

## DatasetSpec

<div class="api-signature">

```python
axosim.setup_workflow.DatasetSpec(name: str, slug: str)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L12-L14)

</div>

Kaggle dataset identity and its local directory name.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>name</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Local dataset subdirectory and archive name.</dd>
<dt><code>slug</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Kaggle owner/dataset identifier passed to the downloader.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="setup-workflow-setupoptions">

## SetupOptions

<div class="api-signature">

```python
axosim.setup_workflow.SetupOptions(project_root: Path, data_dir: Path, install_kaggle: bool = False, download_data: bool = False, convert_raw: bool = False, raw_dir: Path | None = None, shard_dir: Path | None = None, shard_size: int = 128, skip_install: bool = False, datasets: tuple[DatasetSpec, ...] = DEFAULT_DATASETS, python_executable: str = sys.executable)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L24-L35)

</div>

Installation, download, conversion, and path choices used to construct a setup plan.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>project_root</code> <span class="api-type">Path</span></dt>
<dd><span class="api-default">required.</span> Source checkout containing the package to install and local run directories.</dd>
<dt><code>data_dir</code> <span class="api-type">Path</span></dt>
<dd><span class="api-default">required.</span> Root of the raw-data and shard directories.</dd>
<dt><code>install_kaggle</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span> Include installation of downloader dependencies in the plan.</dd>
<dt><code>download_data</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span> Include explicit dataset downloads in the plan.</dd>
<dt><code>convert_raw</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span> Include raw NeuronIO conversion in the plan.</dd>
<dt><code>raw_dir</code> <span class="api-type">Path | None</span></dt>
<dd><span class="api-default">default=None.</span> Optional raw-data directory overriding data_dir/raw.</dd>
<dt><code>shard_dir</code> <span class="api-type">Path | None</span></dt>
<dd><span class="api-default">default=None.</span> Optional converted-data directory overriding data_dir/shards.</dd>
<dt><code>shard_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=128.</span> Maximum sample count in each converted shard.</dd>
<dt><code>skip_install</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span> Omit editable package installation from the plan.</dd>
<dt><code>datasets</code> <span class="api-type">tuple[DatasetSpec, ...]</span></dt>
<dd><span class="api-default">default=DEFAULT_DATASETS.</span> Kaggle dataset identities to download when download_data is enabled.</dd>
<dt><code>python_executable</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=sys.executable.</span> Interpreter used for planned installation, download, and conversion commands.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="setup-workflow-setupstep">

## SetupStep

<div class="api-signature">

```python
axosim.setup_workflow.SetupStep(description: str, command: str | None = None, argv: tuple[str, ...] | None = None, mkdir: Path | None = None)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L39-L43)

</div>

One directory-creation or subprocess step with a reader-facing description.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>description</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">required.</span> Reader-facing description of the setup operation.</dd>
<dt><code>command</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">default=None.</span> Shell-quoted display of the planned subprocess arguments.</dd>
<dt><code>argv</code> <span class="api-type">tuple[str, ...] | None</span></dt>
<dd><span class="api-default">default=None.</span> Argument tuple passed directly to the planned subprocess.</dd>
<dt><code>mkdir</code> <span class="api-type">Path | None</span></dt>
<dd><span class="api-default">default=None.</span> Directory created by this step, when provided.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="setup-workflow-setupplan">

## SetupPlan

<div class="api-signature">

```python
axosim.setup_workflow.SetupPlan(steps: tuple[SetupStep, ...], next_steps: tuple[str, ...] = field(default_factory=tuple))
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L47-L49)

</div>

Ordered setup operations and follow-up commands.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>steps</code> <span class="api-type">tuple[SetupStep, ...]</span></dt>
<dd><span class="api-default">required.</span> Ordered setup operations.</dd>
<dt><code>next_steps</code> <span class="api-type">tuple[str, ...]</span></dt>
<dd><span class="api-default">default=field(default_factory=tuple).</span> Follow-up instructions printed after the plan.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="setup-workflow-build-setup-plan">

## build_setup_plan

<div class="api-signature">

```python
axosim.setup_workflow.build_setup_plan(options: SetupOptions) -> SetupPlan
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L52-L128)

</div>

Construct the setup operations without executing installations, downloads, or conversions.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>options</code> <span class="api-type">SetupOptions</span></dt>
<dd><span class="api-default">required.</span> Setup flags and resolved local paths used to construct the plan.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>plan</code> <span class="api-type">SetupPlan</span></dt>
<dd>Ordered directory-creation and subprocess steps plus follow-up instructions; no steps have run.</dd>
</dl>

</section>

<section class="api-symbol" id="setup-workflow-run-setup-plan">

## run_setup_plan

<div class="api-signature">

```python
axosim.setup_workflow.run_setup_plan(plan: SetupPlan, *, dry_run: bool=False) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L131-L145)

</div>

Print and execute each planned operation; dry_run prints the same plan without filesystem or subprocess changes.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>plan</code> <span class="api-type">SetupPlan</span></dt>
<dd><span class="api-default">required.</span> Ordered setup steps and next-step instructions to execute or inspect.</dd>
<dt><code>dry_run</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Print the plan without creating directories or executing subprocesses.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>
