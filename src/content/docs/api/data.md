---
title: Trace datasets
description: Signatures, parameters, return contracts, and source for trace datasets.
section: API reference
order: 215
---

## Module contract

NeuronIO shards store inputs (samples, time, channels), targets (samples, time, 2), and sample identities. Dataset samples expose one (time, channels) input and one (time, 2) target. get_batch returns batched NumPy arrays. Window datasets preserve sample identity while selecting native time windows; preserve context boundaries when splitting data.

Source revision: `306a51ed950b`. [Public export index](/api/).

## NeuronIOSample

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L14-L17)

```python
NeuronIOSample(sample_id: str, inputs: np.ndarray, targets: np.ndarray) -> None
```

### Fields

| Parameter | Type | Default |
| --- | --- | --- |
| `sample_id` | `str` | required |
| `inputs` | `np.ndarray` | required |
| `targets` | `np.ndarray` | required |

## ShardedNeuronIODataset

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L29-L222)

Deterministic reader for pre-sharded NeuronIO-style NPZ files.

### ShardedNeuronIODataset.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L32-L67)

```python
__init__(self, root: str | Path, *, shuffle: bool=False, seed: int=0, shuffle_mode: Literal['sample', 'shard']='sample', cache_shards: int=0) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `root` | `str \| Path` | required |
| `shuffle` | `bool` | `False` |
| `seed` | `int` | `0` |
| `shuffle_mode` | `Literal['sample', 'shard']` | `'sample'` |
| `cache_shards` | `int` | `0` |

`seed`: Random seed for the declared operation.

Returns `None`.

### ShardedNeuronIODataset.__len__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L69-L70)

```python
__len__(self) -> int
```

Returns `int`.

### ShardedNeuronIODataset.reshuffle

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L72-L80)

```python
reshuffle(self, seed: int) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `seed` | `int` | required |

`seed`: Random seed for the declared operation.

Returns `None`.

### ShardedNeuronIODataset.__getitem__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L82-L91)

```python
__getitem__(self, index: int) -> NeuronIOSample
```

Returns NeuronIOSample with sample_id, inputs (T,C), and targets (T,2).

| Parameter | Type | Default |
| --- | --- | --- |
| `index` | `int` | required |

Returns `NeuronIOSample`.

### ShardedNeuronIODataset.get_batch

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L93-L101)

```python
get_batch(self, indices: range | list[int]) -> tuple[np.ndarray, np.ndarray]
```

Returns (inputs,targets) NumPy arrays with shapes (B,T,C) and (B,T,2). Selected shard windows must have compatible lengths for stacking.

| Parameter | Type | Default |
| --- | --- | --- |
| `indices` | `range \| list[int]` | required |

Returns `tuple[np.ndarray, np.ndarray]`.

### ShardedNeuronIODataset.get_sample_ids

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L103-L104)

```python
get_sample_ids(self, indices: range | list[int]) -> list[str]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `indices` | `range \| list[int]` | required |

Returns `list[str]`.

### ShardedNeuronIODataset.get_optional_array_batch

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L106-L115)

```python
get_optional_array_batch(self, name: str, indices: range | list[int]) -> np.ndarray | None
```

Return an optional per-sample array from NPZ shards when present.

| Parameter | Type | Default |
| --- | --- | --- |
| `name` | `str` | required |
| `indices` | `range \| list[int]` | required |

Returns `np.ndarray \| None`.

### ShardedNeuronIODataset.get_shard_sequence_length

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L117-L130)

```python
get_shard_sequence_length(self, shard_idx: int) -> int
```

Read the input time dimension without materializing a shard array.

| Parameter | Type | Default |
| --- | --- | --- |
| `shard_idx` | `int` | required |

Returns `int`.

## DeterministicWindowDataset

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L225-L280)

Enumerate fixed-size windows from another NeuronIO-style dataset.

### DeterministicWindowDataset.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L228-L257)

```python
__init__(self, base: ShardedNeuronIODataset, *, window_size: int, stride: int | None=None, start_offset: int=0) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `base` | `ShardedNeuronIODataset` | required |
| `window_size` | `int` | required |
| `stride` | `int \| None` | `None` |
| `start_offset` | `int` | `0` |

Returns `None`.

### DeterministicWindowDataset.__len__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L259-L260)

```python
__len__(self) -> int
```

Returns `int`.

### DeterministicWindowDataset.__getitem__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L262-L270)

```python
__getitem__(self, index: int) -> NeuronIOSample
```

| Parameter | Type | Default |
| --- | --- | --- |
| `index` | `int` | required |

Returns `NeuronIOSample`.

### DeterministicWindowDataset.get_batch

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L272-L277)

```python
get_batch(self, indices: range | list[int]) -> tuple[np.ndarray, np.ndarray]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `indices` | `range \| list[int]` | required |

Returns `tuple[np.ndarray, np.ndarray]`.

### DeterministicWindowDataset.get_sample_ids

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L279-L280)

```python
get_sample_ids(self, indices: range | list[int]) -> list[str]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `indices` | `range \| list[int]` | required |

Returns `list[str]`.

## RandomFullTraceWindowDataset

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L283-L399)

Sample deterministic random windows from cached full-trace shards.

### RandomFullTraceWindowDataset.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L286-L326)

```python
__init__(self, base: ShardedNeuronIODataset, *, window_size: int=500, start_offset: int=500, samples_per_epoch: int | None=None, batch_size: int=8, shard_reuse_batches: int=1, sequence_length: int | None=None, seed: int=0, cache_full_shards: bool=True) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `base` | `ShardedNeuronIODataset` | required |
| `window_size` | `int` | `500` |
| `start_offset` | `int` | `500` |
| `samples_per_epoch` | `int \| None` | `None` |
| `batch_size` | `int` | `8` |
| `shard_reuse_batches` | `int` | `1` |
| `sequence_length` | `int \| None` | `None` |
| `seed` | `int` | `0` |
| `cache_full_shards` | `bool` | `True` |

`batch_size`: Examples processed per batch. `seed`: Random seed for the declared operation.

Returns `None`.

### RandomFullTraceWindowDataset.__len__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L328-L329)

```python
__len__(self) -> int
```

Returns `int`.

### RandomFullTraceWindowDataset.reshuffle

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L331-L354)

```python
reshuffle(self, seed: int) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `seed` | `int` | required |

`seed`: Random seed for the declared operation.

Returns `None`.

### RandomFullTraceWindowDataset.__getitem__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L356-L364)

```python
__getitem__(self, index: int) -> NeuronIOSample
```

| Parameter | Type | Default |
| --- | --- | --- |
| `index` | `int` | required |

Returns `NeuronIOSample`.

### RandomFullTraceWindowDataset.get_batch

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L366-L383)

```python
get_batch(self, indices: range | list[int]) -> tuple[np.ndarray, np.ndarray]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `indices` | `range \| list[int]` | required |

Returns `tuple[np.ndarray, np.ndarray]`.

### RandomFullTraceWindowDataset.get_sample_ids

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L385-L386)

```python
get_sample_ids(self, indices: range | list[int]) -> list[str]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `indices` | `range \| list[int]` | required |

Returns `list[str]`.

## OfficialStyleFullTraceWindowDataset

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L402-L543)

Deterministic port of the official NeuronIO file/simulation/time sampling policy.

### OfficialStyleFullTraceWindowDataset.__init__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L405-L449)

```python
__init__(self, base: ShardedNeuronIODataset, *, window_size: int=500, start_offset: int=500, samples_per_epoch: int | None=None, batch_size: int=8, file_load_fraction: float=0.3, source_simulations: int=128, sequence_length: int | None=None, seed: int=0, cache_full_shards: bool=True) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `base` | `ShardedNeuronIODataset` | required |
| `window_size` | `int` | `500` |
| `start_offset` | `int` | `500` |
| `samples_per_epoch` | `int \| None` | `None` |
| `batch_size` | `int` | `8` |
| `file_load_fraction` | `float` | `0.3` |
| `source_simulations` | `int` | `128` |
| `sequence_length` | `int \| None` | `None` |
| `seed` | `int` | `0` |
| `cache_full_shards` | `bool` | `True` |

`batch_size`: Examples processed per batch. `seed`: Random seed for the declared operation.

Returns `None`.

### OfficialStyleFullTraceWindowDataset.__len__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L451-L452)

```python
__len__(self) -> int
```

Returns `int`.

### OfficialStyleFullTraceWindowDataset.reshuffle

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L454-L482)

```python
reshuffle(self, seed: int) -> None
```

| Parameter | Type | Default |
| --- | --- | --- |
| `seed` | `int` | required |

`seed`: Random seed for the declared operation.

Returns `None`.

### OfficialStyleFullTraceWindowDataset.__getitem__

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L484-L492)

```python
__getitem__(self, index: int) -> NeuronIOSample
```

| Parameter | Type | Default |
| --- | --- | --- |
| `index` | `int` | required |

Returns `NeuronIOSample`.

### OfficialStyleFullTraceWindowDataset.get_batch

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L494-L511)

```python
get_batch(self, indices: range | list[int]) -> tuple[np.ndarray, np.ndarray]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `indices` | `range \| list[int]` | required |

Returns `tuple[np.ndarray, np.ndarray]`.

### OfficialStyleFullTraceWindowDataset.get_sample_ids

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L513-L514)

```python
get_sample_ids(self, indices: range | list[int]) -> list[str]
```

| Parameter | Type | Default |
| --- | --- | --- |
| `indices` | `range \| list[int]` | required |

Returns `list[str]`.

## write_demo_shards

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L546-L571)

```python
write_demo_shards(root: str | Path, *, shard_count: int=2, samples_per_shard: int=8, time_steps: int=32, input_dim: int=64, seed: int=0) -> None
```

Create small deterministic NeuronIO-style shards for smoke tests.

Creates deterministic synthetic shard files for pipeline checks. The generated targets are not biological reference data. Returns written shard paths.

| Parameter | Type | Default |
| --- | --- | --- |
| `root` | `str \| Path` | required |
| `shard_count` | `int` | `2` |
| `samples_per_shard` | `int` | `8` |
| `time_steps` | `int` | `32` |
| `input_dim` | `int` | `64` |
| `seed` | `int` | `0` |

`time_steps`: Native sequence horizon. `input_dim`: Native input-channel count. `seed`: Random seed for the declared operation.

Returns `None`.

## repack_shards_as_npy

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/data.py#L574-L617)

```python
repack_shards_as_npy(input_root: str | Path, output_root: str | Path, *, input_dtype: np.dtype | type=np.int8) -> list[Path]
```

Repack existing shards as sliceable `.npy` arrays with identical sample order.

| Parameter | Type | Default |
| --- | --- | --- |
| `input_root` | `str \| Path` | required |
| `output_root` | `str \| Path` | required |
| `input_dtype` | `np.dtype \| type` | `np.int8` |

Returns `list[Path]`.
