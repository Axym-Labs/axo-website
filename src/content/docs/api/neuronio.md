---
title: NeuronIO conversion
description: Signatures, parameters, return contracts, and source for neuronio conversion.
section: API reference
order: 216
---

## Module contract

The converter reads raw NeuronIO teacher traces and creates deterministic shards. Standard soma normalization clips at -55 mV and applies (v_mV-bias)*scale with bias=-67.7 and scale=0.1. Preserve conversion metadata: normalized targets cannot recover clipped spike peaks.

Source revision: `306a51ed950b`. [Public export index](/api/).

## RawNeuronIO

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/neuronio_raw.py#L17-L21)

```python
RawNeuronIO(inputs: np.ndarray, spikes: np.ndarray, soma: np.ndarray, metadata: dict[str, object]) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `inputs` | `np.ndarray` | required |
| `spikes` | `np.ndarray` | required |
| `soma` | `np.ndarray` | required |
| `metadata` | `dict[str, object]` | required |

`metadata`: Caller metadata stored with model state.

## parse_neuronio_pickle

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/neuronio_raw.py#L24-L64)

```python
parse_neuronio_pickle(path: str | Path) -> RawNeuronIO
```

Parse a public NeuronIO simulation pickle into `(sim, time, channel)` arrays.

| Parameter | Type | Default |
| --- | --- | --- |
| `path` | `str \| Path` | required |

Returns `RawNeuronIO`.

## convert_neuronio_pickles

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/neuronio_raw.py#L67-L132)

```python
convert_neuronio_pickles(input_path: str | Path, output_dir: str | Path, *, shard_size: int=128, window_size: int | None=None, window_stride: int | None=None, ignore_start: int=0, y_soma_threshold: float=DEFAULT_Y_SOMA_THRESHOLD, y_train_soma_bias: float=DEFAULT_Y_TRAIN_SOMA_BIAS, y_train_soma_scale: float=DEFAULT_Y_TRAIN_SOMA_SCALE) -> list[Path]
```

Convert raw NeuronIO pickle files to deterministic `.npz` shards.

| Parameter | Type | Default |
| --- | --- | --- |
| `input_path` | `str \| Path` | required |
| `output_dir` | `str \| Path` | required |
| `shard_size` | `int` | `128` |
| `window_size` | `int \| None` | `None` |
| `window_stride` | `int \| None` | `None` |
| `ignore_start` | `int` | `0` |
| `y_soma_threshold` | `float` | `DEFAULT_Y_SOMA_THRESHOLD` = `-55.0` |
| `y_train_soma_bias` | `float` | `DEFAULT_Y_TRAIN_SOMA_BIAS` = `-67.7` |
| `y_train_soma_scale` | `float` | `DEFAULT_Y_TRAIN_SOMA_SCALE` = `0.1` |

`ignore_start`: Initial native timesteps excluded by the declared path.

Returns `list[Path]`.

## create_neuronio_input_type

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/neuronio_raw.py#L135-L139)

```python
create_neuronio_input_type(num_input: int) -> np.ndarray
```

| Parameter | Type | Default |
| --- | --- | --- |
| `num_input` | `int` | required |

`num_input`: Input-channel count.

Returns `np.ndarray`.

## normalize_soma

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/neuronio_raw.py#L142-L150)

```python
normalize_soma(soma: np.ndarray, threshold: float=DEFAULT_Y_SOMA_THRESHOLD, bias: float=DEFAULT_Y_TRAIN_SOMA_BIAS, scale: float=DEFAULT_Y_TRAIN_SOMA_SCALE) -> np.ndarray
```

Returns normalized soma targets after clipping teacher voltage at threshold and applying (voltage-bias)*scale. The default threshold is -55.0 mV, bias is -67.7 mV, and scale is 0.1.

| Parameter | Type | Default |
| --- | --- | --- |
| `soma` | `np.ndarray` | required |
| `threshold` | `float` | `DEFAULT_Y_SOMA_THRESHOLD` = `-55.0` |
| `bias` | `float` | `DEFAULT_Y_TRAIN_SOMA_BIAS` = `-67.7` |
| `scale` | `float` | `DEFAULT_Y_TRAIN_SOMA_SCALE` = `0.1` |

Returns `np.ndarray`.
