---
title: AxoSim CLI
description: Complete options and defaults for axosim.
section: API reference
order: 240
---

## Command contract

The tables include parser defaults, choices, required arguments, flag actions, and compatibility options hidden from ordinary help. Every command and subcommand accepts `-h` or `--help`. Flag defaults refer to their destination value: `store_true` sets it true, while `store_false` sets it false. For example, `--blocking-transfer` changes `non_blocking` from its default true to false. Named presets may override parser defaults; explicitly supplied options take precedence. Use the installed command's `--help` when working with another revision.

## axosim make-demo-data

write deterministic demo NPZ shards

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `--output` | `str` / `store` | `None` | yes | — |
| `--samples` | `int` / `store` | `8` | no | — |
| `--shards` | `int` / `store` | `1` | no | — |
| `--time-steps` | `int` / `store` | `32` | no | — |
| `--input-dim` | `int` / `store` | `64` | no | — |
| `--seed` | `int` / `store` | `0` | no | — |

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L61)

## axosim convert-neuronio

convert raw NeuronIO pickle files to deterministic shards

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `--input` | `str` / `store` | `None` | yes | — |
| `--output` | `str` / `store` | `None` | yes | — |
| `--shard-size` | `int` / `store` | `128` | no | — |
| `--window-size` | `int` / `store` | `None` | no | — |
| `--window-stride` | `int` / `store` | `None` | no | — |
| `--ignore-start` | `int` / `store` | `0` | no | — |

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L69)

## axosim repack-shards

repack shards as sliceable .npy arrays

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `--input` | `str` / `store` | `None` | yes | — |
| `--output` | `str` / `store` | `None` | yes | — |
| `--input-dtype` | `str` / `store` | `'int8'` | no | `['int8', 'float32']` |

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L77)

## axosim list-presets

list named train/evaluate presets

No additional arguments are required; this command prints the named recipes as JSON.

## axosim evaluate

evaluate a model with the corrected full-trace metric path

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `--preset` | `str` / `store` | `None` | no | `['fulltrace-paper-metric', 'legacy-baseline-smoke']` |
| `--data` | `str` / `store` | `None` | yes | — |
| `--output` | `str` / `store` | `None` | yes | — |
| `--input-dim` | `int` / `store` | `1278` | no | — |
| `--memory-units` | `int` / `store` | `30` | no | — |
| `--branches` | `int` / `store` | `32` | no | — |
| `--model-kind` | `str` / `store` | `'baseline'` | no | `['baseline', 'official', 'axomamba', 'mamba-official', 'mamba-pytorch', 'branch-mamba-pytorch', 'branch-trace-rnn']` |
| `--model-config` | `str` / `store` | `'configs/branch_elm_30_official.json'` | no | — |
| `--batch-size` | `int` / `store` | `8` | no | — |
| `--seed` | `int` / `store` | `0` | no | — |
| `--device` | `str` / `store` | `'cpu'` | no | — |
| `--checkpoint` | `str` / `store` | `None` | no | — |
| `--window-size` | `int` / `store` | `None` | no | — |
| `--window-stride` | `int` / `store` | `None` | no | — |
| `--ignore-start` | `int` / `store` | `0` | no | — |
| `--cache-shards` | `int` / `store` | `1` | no | — |
| `--soma-units` | `str` / `store` | `'millivolts'` | no | `['millivolts', 'normalized']` |
| `--metric-ignore-start` | `int` / `store` | `0` | no | — |
| `--metric-mask-mode` | `str` / `store` | `'ignore-start'` | no | `['ignore-start', 'official-overlap']` |
| `--metric-stitch-burn-in` | `int` / `store` | `150` | no | — |
| `--soma-affine-calibration` | `flag` / `store_true` | `False` | no | — |
| `--pin-memory` | `flag` / `store_true` | `False` | no | — |
| `--blocking-transfer` | `flag` / `store_false` | `True` | no | — |
| `--registry` | `str` / `store` | `None` | no | — |
| `--no-registry` | `flag` / `store_const` | `None` | no | — |

`--model-kind`: use 'official' for the paper-style model, 'axomamba' for the promoted Mamba surrogate, 'mamba-official' for the generic official mamba-ssm backend, or 'branch-trace-rnn' for the RNN comparison path; 'baseline' is legacy/debug

`--metric-mask-mode`: Compatibility option hidden from default help.

`--metric-stitch-burn-in`: Compatibility option hidden from default help.

`--registry`: append a one-line JSONL record; defaults to <output-dir>/experiment-registry.jsonl

`--no-registry`:  When selected, sets `registry` to `'off'`.

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L84)

## axosim diagnose

write biology-oriented surrogate fidelity diagnostics

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `--preset` | `str` / `store` | `None` | no | `['fulltrace-paper-metric', 'legacy-baseline-smoke']` |
| `--data` | `str` / `store` | `None` | yes | — |
| `--output-dir` | `str` / `store` | `None` | yes | — |
| `--input-dim` | `int` / `store` | `1278` | no | — |
| `--memory-units` | `int` / `store` | `30` | no | — |
| `--branches` | `int` / `store` | `32` | no | — |
| `--model-kind` | `str` / `store` | `'baseline'` | no | `['baseline', 'official', 'axomamba', 'mamba-official', 'mamba-pytorch', 'branch-mamba-pytorch', 'branch-trace-rnn']` |
| `--model-config` | `str` / `store` | `'configs/branch_elm_30_official.json'` | no | — |
| `--batch-size` | `int` / `store` | `8` | no | — |
| `--seed` | `int` / `store` | `0` | no | — |
| `--device` | `str` / `store` | `'cpu'` | no | — |
| `--checkpoint` | `str` / `store` | `None` | no | — |
| `--window-size` | `int` / `store` | `None` | no | — |
| `--window-stride` | `int` / `store` | `None` | no | — |
| `--ignore-start` | `int` / `store` | `0` | no | — |
| `--cache-shards` | `int` / `store` | `1` | no | — |
| `--metric-ignore-start` | `int` / `store` | `0` | no | — |
| `--metric-mask-mode` | `str` / `store` | `'ignore-start'` | no | `['ignore-start', 'official-overlap']` |
| `--metric-stitch-burn-in` | `int` / `store` | `150` | no | — |
| `--soma-affine-calibration` | `flag` / `store_true` | `False` | no | — |
| `--max-samples` | `int` / `store` | `None` | no | — |
| `--pin-memory` | `flag` / `store_true` | `False` | no | — |
| `--blocking-transfer` | `flag` / `store_false` | `True` | no | — |

`--metric-mask-mode`: Compatibility option hidden from default help.

`--metric-stitch-burn-in`: Compatibility option hidden from default help.

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L112)

## axosim train

train a model with the current experiment workflow

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `--preset` | `str` / `store` | `None` | no | `['axomamba-probe', 'legacy-baseline-smoke', 'mamba-official-probe', 'mamba2-official-probe', 'official-fulltrace-reference', 'paper-random-fulltrace']` |
| `--data` | `str` / `store` | `None` | yes | — |
| `--checkpoint` | `str` / `store` | `None` | yes | — |
| `--metrics` | `str` / `store` | `None` | yes | — |
| `--input-dim` | `int` / `store` | `1278` | no | — |
| `--memory-units` | `int` / `store` | `30` | no | — |
| `--branches` | `int` / `store` | `32` | no | — |
| `--model-kind` | `str` / `store` | `'baseline'` | no | `['baseline', 'official', 'axomamba', 'mamba-official', 'mamba-pytorch', 'branch-mamba-pytorch', 'branch-trace-rnn']` |
| `--model-config` | `str` / `store` | `'configs/branch_elm_30_official.json'` | no | — |
| `--epochs` | `int` / `store` | `1` | no | — |
| `--batch-size` | `int` / `store` | `8` | no | — |
| `--learning-rate` | `float` / `store` | `0.0005` | no | — |
| `--burn-in` | `int` / `store` | `0` | no | — |
| `--seed` | `int` / `store` | `0` | no | — |
| `--device` | `str` / `store` | `'cpu'` | no | — |
| `--window-size` | `int` / `store` | `None` | no | — |
| `--window-stride` | `int` / `store` | `None` | no | — |
| `--ignore-start` | `int` / `store` | `0` | no | — |
| `--window-sampling` | `str` / `store` | `'random-full-trace'` | no | `['deterministic', 'random-full-trace', 'official-full-trace']` |
| `--epoch-samples` | `int` / `store` | `None` | no | — |
| `--shard-reuse-batches` | `int` / `store` | `1` | no | — |
| `--file-load-fraction` | `float` / `store` | `0.3` | no | — |
| `--full-trace-length` | `int` / `store` | `None` | no | — |
| `--sample-window-reads` | `flag` / `store_true` | `False` | no | — |
| `--shuffle-mode` | `str` / `store` | `'shard'` | no | `['sample', 'shard', 'none']` |
| `--cache-shards` | `int` / `store` | `1` | no | — |
| `--val-data` | `str` / `store` | `None` | no | — |
| `--val-batch-size` | `int` / `store` | `None` | no | — |
| `--val-cache-shards` | `int` / `store` | `1` | no | — |
| `--val-window-size` | `int` / `store` | `None` | no | — |
| `--val-window-stride` | `int` / `store` | `None` | no | — |
| `--val-ignore-start` | `int` / `store` | `0` | no | — |
| `--val-soma-units` | `str` / `store` | `'millivolts'` | no | `['millivolts', 'normalized']` |
| `--val-metric-ignore-start` | `int` / `store` | `500` | no | — |
| `--val-metric-mask-mode` | `str` / `store` | `'ignore-start'` | no | `['ignore-start', 'official-overlap']` |
| `--val-metric-stitch-burn-in` | `int` / `store` | `150` | no | — |
| `--val-soma-affine-calibration` | `flag` / `store_true` | `True` | no | — |
| `--no-val-soma-affine-calibration` | `flag` / `store_false` | `True` | no | — |
| `--best-checkpoint` | `str` / `store` | `None` | no | — |
| `--max-train-batches` | `int` / `store` | `None` | no | — |
| `--lr-schedule` | `str` / `store` | `'constant'` | no | `['constant', 'cosine']` |
| `--lr-schedule-steps` | `int` / `store` | `None` | no | — |
| `--optimizer` | `str` / `store` | `'adam'` | no | `['adam', 'adamw']` |
| `--weight-decay` | `float` / `store` | `0.0` | no | — |
| `--l1-lambda` | `float` / `store` | `0.0` | no | — |
| `--spike-loss-weight` | `float` / `store` | `0.5` | no | — |
| `--soma-loss-weight` | `float` / `store` | `0.5` | no | — |
| `--sparse-soma-loss-weight` | `float` / `store` | `0.0` | no | — |
| `--sparse-soma-high-voltage-quantile` | `float` / `store` | `0.9` | no | — |
| `--sparse-soma-high-dvdt-quantile` | `float` / `store` | `0.9` | no | — |
| `--sparse-soma-input-event-quantile` | `float` / `store` | `0.95` | no | — |
| `--sparse-soma-spike-window` | `int` / `store` | `5` | no | — |
| `--sparse-soma-post-event-window` | `int` / `store` | `5` | no | — |
| `--sera-soma-loss-weight` | `float` / `store` | `0.0` | no | — |
| `--sera-soma-min-weight` | `float` / `store` | `0.05` | no | — |
| `--sera-soma-relevance-power` | `float` / `store` | `1.0` | no | — |
| `--soma-slope-loss-weight` | `float` / `store` | `0.0` | no | — |
| `--grad-clip-norm` | `float` / `store` | `0.0` | no | — |
| `--train-update-log-interval` | `int` / `store` | `0` | no | — |
| `--train-update-log` | `str` / `store` | `None` | no | — |
| `--prefetch-batches` | `int` / `store` | `0` | no | — |
| `--pin-memory` | `flag` / `store_true` | `False` | no | — |
| `--blocking-transfer` | `flag` / `store_false` | `True` | no | — |
| `--registry` | `str` / `store` | `None` | no | — |
| `--no-registry` | `flag` / `store_const` | `None` | no | — |

`--model-kind`: use 'official' for the paper-style model, 'axomamba' for the promoted Mamba surrogate, 'mamba-official' for the generic official mamba-ssm backend, or 'branch-trace-rnn' for the RNN comparison path; 'baseline' is legacy/debug

`--sample-window-reads`: read random/official windows by sample instead of caching full compressed shards

`--val-metric-mask-mode`: Compatibility option hidden from default help.

`--val-metric-stitch-burn-in`: Compatibility option hidden from default help.

`--registry`: append a one-line JSONL record; defaults to <metrics-dir>/experiment-registry.jsonl

`--no-registry`:  When selected, sets `registry` to `'off'`.

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L138)

## axosim benchmark

time model forward passes on random input

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `--input-dim` | `int` / `store` | `1278` | no | — |
| `--memory-units` | `int` / `store` | `30` | no | — |
| `--branches` | `int` / `store` | `32` | no | — |
| `--model-kind` | `str` / `store` | `'baseline'` | no | `['baseline', 'official', 'axomamba', 'mamba-official', 'mamba-pytorch', 'branch-mamba-pytorch', 'branch-trace-rnn']` |
| `--model-config` | `str` / `store` | `'configs/branch_elm_30_official.json'` | no | — |
| `--batch-size` | `int` / `store` | `1` | no | — |
| `--time-steps` | `int` / `store` | `500` | no | — |
| `--runs` | `int` / `store` | `10` | no | — |
| `--device` | `str` / `store` | `'cpu'` | no | — |
| `--compile` | `flag` / `store_true` | `False` | no | — |
| `--output` | `str` / `store` | `None` | no | — |

`--model-kind`: use 'official' for the paper-style model, 'mamba-official' for the official mamba-ssm backend, or 'branch-trace-rnn' for the RNN comparison path; 'baseline' is legacy/debug

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L214)

## axosim inference-benchmark

benchmark deployment-oriented inference throughput across batch and sequence scales

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `--input-dim` | `int` / `store` | `1278` | no | — |
| `--memory-units` | `int` / `store` | `30` | no | — |
| `--branches` | `int` / `store` | `32` | no | — |
| `--model-kind` | `str` / `store` | `'baseline'` | no | `['baseline', 'official', 'axomamba', 'mamba-official', 'mamba-pytorch', 'branch-mamba-pytorch', 'branch-trace-rnn']` |
| `--model-config` | `str` / `store` | `'configs/branch_elm_30_official.json'` | no | — |
| `--checkpoint` | `str` / `store` | `None` | no | — |
| `--batch-sizes` | `str` / `store` | `'1,8,32,128'` | no | — |
| `--time-steps` | `str` / `store` | `'500,1000,6000'` | no | — |
| `--runs` | `int` / `store` | `20` | no | — |
| `--warmup-runs` | `int` / `store` | `5` | no | — |
| `--precision` | `str` / `store` | `'float32'` | no | `['float32', 'float16', 'bfloat16']` |
| `--device` | `str` / `store` | `'cpu'` | no | — |
| `--compile` | `flag` / `store_true` | `False` | no | — |
| `--accuracy-metrics` | `str` / `store` | `None` | no | — |
| `--output` | `str` / `store` | `None` | yes | — |

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/cli.py#L230)
