---
title: Submit sparse events
description: Address exact contact events without allocating dense population-by-time-by-contact histories.
section: Build populations
order: 60
---

## Address an event

For neuron `n`, timestep `t`, contact `k`, horizon `T`, and contacts per neuron `K`, use flattened indices `n*T + t` and `n*K + k`. Both indices must recover the same target neuron by integer division. An event value is a signed floating-point amplitude attached to that exact contact.

| Tensor | Shape | Dtype |
| --- | --- | --- |
| `event_summary_indices` | `(events,)` | `int32` or `int64` |
| `event_contact_indices` | `(events,)` | `int32` or `int64` |
| `event_values` | `(events,)` | Floating point |

Keep the tensors in corresponding event order, on the population's device, and within the declared horizon and contact range.

## Execute sparse contact histories

Download [population_example.py](/examples/population_example.py) into the directory where you run this script; [build populations](/populations/) explains its construction. The example below uses its three-neuron, four-contact population on CUDA:

```python
import torch
from population_example import build_population

population = build_population("cuda")
summary_indices = torch.tensor([0, 7, 16, 35], device="cuda")
contact_indices = torch.tensor([1, 3, 6, 8], device="cuda")
event_values = torch.tensor(
    [1.0, -0.5, 0.75, 0.25],
    device="cuda",
    requires_grad=True,
)

prediction = population.forward_sparse_contacts(
    summary_indices,
    contact_indices,
    event_values,
    time_steps=12,
)
prediction[:, 4:].square().mean().backward()
print(prediction.shape, event_values.grad.shape)
```

```text
torch.Size([3, 12, 2]) torch.Size([4])
```

Replace `"cuda"` with `"cpu"` throughout for a CPU run. This example masks the first four causal padding positions before computing the loss.

## Gradients and memory

Gradients propagate to event amplitudes, selected contact efficacies, and enabled adaptation banks. Repeated events accumulate in their population-time bins. Dense and sparse paths have an explicit equivalence test in the source repository.

Sparse inputs avoid the dense `N*T*K` contact-history allocation. Output tensors and the temporal autograd graph still scale with `N*T`, so increase population size and horizon with their memory cost in mind. Quantized deployment banks have separate interfaces in the [synaptic reference](/api/synapse/) and [behavior-bank reference](/api/population/).

## Next steps

Follow [inference-time adaptation](/adaptation/) to select the banks you want to optimize, or inspect the complete [`forward_sparse_contacts` contract](/api/interfaces/).
