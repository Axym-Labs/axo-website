---
title: Capture CUDA updates
description: Capture forward, loss, backward, clipping, and optimization for fixed-shape adaptation.
section: Inference-time adaptation
order: 80
---

## Prepare a fixed-shape update

CUDA Graph replay reduces repeated launch overhead for a fixed update. Begin with the verified eager path in [inference-time adaptation](/adaptation/). The module, optimizer groups, static buffer allocation, tensor shapes, dtypes, and execution device must remain compatible with the captured graph.

The helper captures forward execution, the loss, backward propagation, an optional gradient transform, and the optimizer step. Warmup and graph construction temporarily execute updates; the helper restores module and optimizer state before returning, so capture consumes no hidden optimizer update.

## Capture and replay

Download [population_example.py](/examples/population_example.py) into the directory where you run this script. This example imports that helper, explained in [build populations](/populations/), and uses a capturable Adam optimizer:

```python
import torch
from axosim import CudaGraphAdaptationStep
from population_example import build_population

def causal_mse(prediction, target):
    return torch.nn.functional.mse_loss(
        prediction[:, 4:], target[:, 4:]
    )

population = build_population("cuda")
contacts = torch.randn(3, 12, 4, device="cuda")
target = torch.randn(3, 12, 2, device="cuda")
population.enable_adaptation_training(
    behavior=True,
    morphology=True,
    synaptic=True,
)
trainable = list(population.trainable_adaptation_parameters())
optimizer = torch.optim.Adam(
    trainable,
    lr=1e-3,
    capturable=True,
)
step = CudaGraphAdaptationStep.capture(
    population,
    optimizer,
    contacts,
    target,
    causal_mse,
    gradient_transform=lambda: torch.nn.utils.clip_grad_norm_(
        trainable, 1.0
    ),
)
loss = step(contacts, target, synchronize=True)
print(loss.shape)
```

```text
torch.Size([])
```

Each call copies the supplied inputs and targets into captured static buffers, replays the update, and returns a detached cloned loss tensor. New input tensors may have different addresses because they are copied; the graph's internal static buffers and parameter allocations must remain valid.

## Verify and measure replay

Compare several eager and captured updates from identical initial states before relying on replay. Recapture after changing shapes, dtypes, parameter groups, or allocations. Variable-length sequences and changing objectives are easier to debug in the eager path.

Report capture latency separately from steady-state update latency. State whether timing includes input transfer, loss, backward, gradient clipping, optimizer execution, and synchronization. A forward-plus-backward measurement without the optimizer is a narrower quantity than a complete adaptation update.

## Next steps

See [adaptation API](/api/adaptation/) for the complete capture and replay signatures, and [reproducibility](/reproducibility/) for timing metadata.
