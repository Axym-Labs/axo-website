---
title: Setup workflow
description: Signatures, parameters, return contracts, and source for setup workflow.
section: API reference
order: 221
---

## Module contract

Setup planning separates the declared installation/download/conversion steps from execution. Default setup creates local directories and installs the checkout; downloads occur only when explicitly requested. A dry run prints the plan without executing its commands.

Source revision: `306a51ed950b`. [Public export index](/api/).

## DatasetSpec

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L12-L14)

```python
DatasetSpec(name: str, slug: str) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `name` | `str` | required |
| `slug` | `str` | required |

## SetupOptions

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L24-L35)

```python
SetupOptions(project_root: Path, data_dir: Path, install_kaggle: bool = False, download_data: bool = False, convert_raw: bool = False, raw_dir: Path | None = None, shard_dir: Path | None = None, shard_size: int = 128, skip_install: bool = False, datasets: tuple[DatasetSpec, ...] = DEFAULT_DATASETS, python_executable: str = sys.executable) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `project_root` | `Path` | required |
| `data_dir` | `Path` | required |
| `install_kaggle` | `bool` | `False` |
| `download_data` | `bool` | `False` |
| `convert_raw` | `bool` | `False` |
| `raw_dir` | `Path \| None` | `None` |
| `shard_dir` | `Path \| None` | `None` |
| `shard_size` | `int` | `128` |
| `skip_install` | `bool` | `False` |
| `datasets` | `tuple[DatasetSpec, ...]` | `DEFAULT_DATASETS` |
| `python_executable` | `str` | `sys.executable` |

## SetupStep

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L39-L43)

```python
SetupStep(description: str, command: str | None = None, argv: tuple[str, ...] | None = None, mkdir: Path | None = None) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `description` | `str` | required |
| `command` | `str \| None` | `None` |
| `argv` | `tuple[str, ...] \| None` | `None` |
| `mkdir` | `Path \| None` | `None` |

## SetupPlan

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L47-L49)

```python
SetupPlan(steps: tuple[SetupStep, ...], next_steps: tuple[str, ...] = field(default_factory=tuple)) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `steps` | `tuple[SetupStep, ...]` | required |
| `next_steps` | `tuple[str, ...]` | `field(default_factory=tuple)` |

## build_setup_plan

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L52-L128)

```python
build_setup_plan(options: SetupOptions) -> SetupPlan
```

| Parameter | Type | Default |
| --- | --- | --- |
| `options` | `SetupOptions` | required |

Returns `SetupPlan`.

## run_setup_plan

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/setup_workflow.py#L131-L145)

```python
run_setup_plan(plan: SetupPlan, *, dry_run: bool=False) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `plan` | `SetupPlan` | required |
| `dry_run` | `bool` | `False` |

Returns `None`.
