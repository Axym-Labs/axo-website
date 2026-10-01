---
title: AxoBench evaluation CLI
description: Complete options and defaults for axosim-evaluate-model.
section: API reference
order: 242
---

## Command contract

The tables include parser defaults, choices, required arguments, flag actions, and compatibility options hidden from ordinary help. Every command and subcommand accepts `-h` or `--help`. Flag defaults refer to their destination value: `store_true` sets it true, while `store_false` sets it false. For example, `--blocking-transfer` changes `non_blocking` from its default true to false. Named presets may override parser defaults; explicitly supplied options take precedence. Use the installed command's `--help` when working with another revision.

`--baseline-cache` and `--baseline-checkpoint` are mutually exclusive. `--output` and the compatibility alias `--output-json` are mutually exclusive. `--save-cache` cannot be combined with either baseline comparison path. The current AxoBench package is required for execution.

## axosim-evaluate-model

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `checkpoint` | `str` / `store` | `None` | yes | — |
| `--baseline-checkpoint` | `str` / `store` | `None` | no | — |
| `--baseline-cache` | `str` / `store` | `None` | no | — |
| `--save-cache` | `str` / `store` | `None` | no | — |
| `--dataset-root` | `str` / `store` | `None` | yes | — |
| `--model-id` | `str` / `store` | `None` | no | — |
| `--device` | `str` / `store` | `'auto'` | no | — |
| `--batch-size` | `int` / `store` | `128` | no | — |
| `--max-samples` | `int` / `store` | `None` | no | — |
| `--max-intervention-samples` | `int` / `store` | `None` | no | — |
| `--max-interventions` | `int` / `store` | `8` | no | — |
| `--intervention-workers` | `int` / `store` | `4` | no | — |
| `--interventions` | `str` / `store` | `None` | no | — |
| `--multiple-morphologies` | `flag` / `store_true` | `False` | no | — |
| `--morphology-id` | `str` / `store` | `None` | no | — |
| `--ignore-start` | `int` / `store` | `500` | no | — |
| `--calibration-fraction` | `float` / `store` | `0.25` | no | — |
| `--default-spike-threshold` | `float` / `store` | `0.0` | no | — |
| `--bootstrap-replicates` | `int` / `store` | `250` | no | — |
| `--bootstrap-seed` | `int` / `store` | `20260711` | no | — |
| `--output` | `str` / `store` | `None` | no | — |
| `--output-json` | `str` / `store` | `None` | no | — |

`--interventions`: comma-separated intervention names; default discovers all

`--multiple-morphologies`: balance the 120/40 evaluation profile across available morphologies

`--morphology-id`: specific morphology for the default single-morphology evaluation

`--output`: optional .json or .csv report path

`--output-json`: Compatibility option hidden from default help.

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/axobench_iteration.py#L205)
