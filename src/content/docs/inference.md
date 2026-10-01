---
title: Run inference
description: Load a checkpoint, submit native input traces, and interpret spike and voltage outputs.
section: Simulation
order: 31
---

## Load and execute a checkpoint

After [installation](/installation/), provide a trusted full GRU or Mamba checkpoint and select its execution device. This example uses CUDA; replace the device strings with `"cpu"` for a CPU-compatible checkpoint.

```python
import torch
from axosim.checkpoint import load_checkpoint

model, metadata = load_checkpoint(
    "runs/axosim-mamba.pt",
    map_location="cuda",
)
model = model.to("cuda").eval()
inputs = torch.zeros(8, 500, model.num_input, device="cuda")
morphology_ids = getattr(model.config, "morphology_ids", None)
morphology_indices = (
    torch.zeros(inputs.shape[0], dtype=torch.long, device=inputs.device)
    if morphology_ids else None
)

with torch.inference_mode():
    prediction = (
        model(inputs, morphology_indices=morphology_indices)
        if morphology_indices is not None else model(inputs)
    )

spike_logit = prediction[..., 0]
soma_output = prediction[..., 1]
print(prediction.shape, spike_logit.shape, soma_output.shape)
```

For a checkpoint with two output channels, the shapes are:

```text
torch.Size([8, 500, 2]) torch.Size([8, 500]) torch.Size([8, 500])
```

Start with this zero-input trace to check device placement, checkpoint reconstruction, and output channels before introducing data preprocessing. The example selects the checkpoint's first declared morphology for every batch item. For measured traces, map each trace's actual morphology ID to the index in `model.config.morphology_ids`, and load inputs in the channel order, sign convention, sampling cadence, and normalization used during training. Morphology-conditioned synaptic gains require these indices.

## Input and output contract

| Tensor | Shape | Meaning |
| --- | --- | --- |
| `inputs` | `(batch, native_timesteps, input_channels)` | Ordered native input histories |
| `morphology_indices` | `(batch,)` | Integer class indices into the checkpoint's morphology vocabulary, when configured |
| `prediction` | `(batch, native_timesteps, 2)` | Spike logit and somatic-voltage prediction |
| `spike_logit` | `(batch, native_timesteps)` | Uncalibrated spike logits |
| `soma_output` | `(batch, native_timesteps)` | Voltage in the checkpoint's target coordinates |

Released evaluations use one native timestep per millisecond. Tensor widths alone do not establish input-channel meaning or voltage units. Preserve the dataset manifest and use its conversion rule or the AxoBench prediction adapter.

## Convert voltage and calibrate spikes

In the standard NeuronIO conversion, the voltage target is `(v_mV - b) * s`, with `b = -67.7` and `s = 0.1`, after teacher voltages above −55 mV have been clipped. The inverse coordinate transform is `soma_output / s + b`; it cannot reconstruct clipped spike peaks. Other checkpoints may use different target conventions.

Calibrate the spike-logit threshold on development data, then retain it for final evaluation. The [AxoBench evaluator](/evaluation/) manages the metric protocol and calibration boundary, including morphology-aware input selection.

## Preserve temporal state when streaming

Models that implement `allocate_streaming_state` and `streaming_step` support explicit persistent state. The state belongs to a stream with fixed batch membership; allocate a fresh state when beginning an independent trace.

```python
# Continue after loading model and constructing inputs above.
if not hasattr(model, "allocate_streaming_state"):
    raise TypeError("This checkpoint does not expose streaming inference")

state = model.allocate_streaming_state(
    inputs.shape[0],
    device=inputs.device,
    dtype=inputs.dtype,
)
with torch.inference_mode():
    streamed = torch.cat(
        [model.streaming_step(
            inputs[:, t], state, morphology_indices=morphology_indices
         )
         for t in range(inputs.shape[1])],
        dim=1,
    )
print(streamed.shape)
max_difference = (streamed - prediction).abs().max().item()
```

The resulting sequence has the same batch and time dimensions. Inspect `max_difference` to compare streaming with the full-sequence prediction under the same dtype and initial state; the appropriate numerical tolerance depends on the backend and precision. This check is useful before replacing sequence execution with streaming in a service. Streaming signatures and supported options differ by implementation; consult [Mamba](/api/mamba/), [GRU temporal models](/api/temporal-core/), or [block forecasts](/api/block-forecast/). Population forward methods initialize the Lite hidden state for each supplied sequence, as described in [build populations](/populations/).

## Next steps

Use [evaluation](/evaluation/) to compute AxoBench metrics, or [training](/training/) to fit a new model.
