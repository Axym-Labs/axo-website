---
title: Setup CLI
description: Complete options and defaults for axosim-setup.
section: API reference
apiGroup: CLI
order: 241
---

## Usage

```bash
axosim-setup --help
```

Every command and subcommand accepts `-h` or `--help`. The option reference below includes exact parser defaults, choices, required arguments, and compatibility options hidden from ordinary help.

The default data directory is `<project-root>/data`; raw and shard output directories are resolved by the plan. `--download-data` and `--convert-raw` are explicit actions. `--dry-run` prints the commands and directory operations without executing them.

## axosim-setup

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>--project-root</code> <span class="api-type">Path</span> · default=&#x27;Path.cwd()&#x27;</dt>
<dd>Source checkout containing the package to install and local run directories.</dd>
<dt><code>--data-dir</code> <span class="api-type">Path</span> · default=None</dt>
<dd>Root of the raw-data and shard directories.</dd>
<dt><code>--dry-run</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Print the plan without creating directories or executing subprocesses. Sets dry_run=True.</dd>
<dt><code>--skip-install</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Omit editable package installation from the plan. Sets skip_install=True.</dd>
<dt><code>--install-kaggle</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Include installation of downloader dependencies in the plan. Sets install_kaggle=True.</dd>
<dt><code>--download-data</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Include explicit dataset downloads in the plan. Sets download_data=True.</dd>
<dt><code>--convert-raw</code> <span class="api-type">flag</span> · default=False</dt>
<dd>Include raw NeuronIO conversion in the plan. Sets convert_raw=True.</dd>
<dt><code>--raw-dir</code> <span class="api-type">Path</span> · default=None</dt>
<dd>Optional raw-data directory overriding data_dir/raw.</dd>
<dt><code>--shard-dir</code> <span class="api-type">Path</span> · default=None</dt>
<dd>Optional converted-data directory overriding data_dir/shards.</dd>
<dt><code>--shard-size</code> <span class="api-type">int</span> · default=128</dt>
<dd>Maximum sample count in each converted shard.</dd>
</dl>

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L152)
