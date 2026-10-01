---
title: Setup CLI
description: Complete options and defaults for axosim-setup.
section: API reference
order: 241
---

## Command contract

The tables include parser defaults, choices, required arguments, flag actions, and compatibility options hidden from ordinary help. Every command and subcommand accepts `-h` or `--help`. Flag defaults refer to their destination value: `store_true` sets it true, while `store_false` sets it false. For example, `--blocking-transfer` changes `non_blocking` from its default true to false. Named presets may override parser defaults; explicitly supplied options take precedence. Use the installed command's `--help` when working with another revision.

The default data directory is `<project-root>/data`; raw and shard output directories are resolved by the plan. `--download-data` and `--convert-raw` are explicit actions. `--dry-run` prints the commands and directory operations without executing them.

## axosim-setup

| Argument | Type/action | Default | Required | Choices |
| --- | --- | --- | --- | --- |
| `--project-root` | `Path` / `store` | `'Path.cwd()'` | no | — |
| `--data-dir` | `Path` / `store` | `None` | no | — |
| `--dry-run` | `flag` / `store_true` | `False` | no | — |
| `--skip-install` | `flag` / `store_true` | `False` | no | — |
| `--install-kaggle` | `flag` / `store_true` | `False` | no | — |
| `--download-data` | `flag` / `store_true` | `False` | no | — |
| `--convert-raw` | `flag` / `store_true` | `False` | no | — |
| `--raw-dir` | `Path` / `store` | `None` | no | — |
| `--shard-dir` | `Path` / `store` | `None` | no | — |
| `--shard-size` | `int` / `store` | `128` | no | — |

[Parser source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L152)
