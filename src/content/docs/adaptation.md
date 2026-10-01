---
title: Inference-time adaptation
description: Optimize behavior, morphology, and synaptic parameters through the full temporal horizon.
section: Training and adaptation
order: 70
---

## Choose adaptation parameters

An adapted Lite population has three parameter groups. Behavior rows are specific to individual neurons; morphology rows are shared by neurons with the same morphology index; synaptic log efficacies are specific to incoming contacts. The shared Lite model supplies the trained response map.

Behavior coefficients modify encoded-input offset and gain, state decay, recurrent-proposal offset and gain, and native-output offset and gain. They specialize temporal responses and output calibration. Synaptic parameters scale exact contact amplitudes, and morphology parameters add the shared structural context.

## Run an eager update

Download [population_example.py](/examples/population_example.py) into the directory where you run this script; [build populations](/populations/) explains its construction. This example creates a controlled target by increasing every contact efficacy in an otherwise identical teacher population. It then uses all three adaptation banks to fit the changed responses:

```python
import torch
from copy import deepcopy
from math import log
from population_example import build_population

torch.manual_seed(7)
population = build_population()
contacts = torch.randn(3, 12, 4)
teacher = deepcopy(population)
with torch.no_grad():
    teacher.synaptic_log_efficacy.add_(log(1.25))
    target = teacher(contacts).detach()
population.enable_adaptation_training(
    behavior=True,
    morphology=True,
    synaptic=True,
)
trainable = list(population.trainable_adaptation_parameters())
optimizer = torch.optim.Adam(trainable, lr=1e-3)

def causal_mse(prediction, target):
    return torch.nn.functional.mse_loss(
        prediction[:, 4:],
        target[:, 4:],
    )

before = causal_mse(population(contacts), target).item()
for _ in range(20):
    optimizer.zero_grad(set_to_none=True)
    loss = causal_mse(population(contacts), target)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(trainable, 1.0)
    optimizer.step()
after = causal_mse(population(contacts), target).item()
print(loss.shape, len(trainable))
print(after < before)
```

```text
torch.Size([]) 3
True
```

The final Boolean tests whether the controlled response discrepancy decreased. It does not identify the teacher's contact efficacies, because behavior and morphology adjustments can compensate for synaptic changes. If contact recovery is the question, enable only `synaptic=True`; enable additional banks when the task requires response or morphology calibration.

The learning rate and twenty-step budget make this a bounded interface example; select both on development data for a scientific adaptation study. Norm clipping limits unusually large gradients. `enable_adaptation_training` freezes the shared neuron weights, and gradients span the complete temporal horizon unless you explicitly truncate the graph. Use measured targets and a task-appropriate objective for biological or downstream accuracy claims.

## Validate an adaptation recipe

Select the objective, optimizer, step budget, learning rate, and bank choices on development data, then evaluate once on an untouched final split. Mask Lite's first four causal padding outputs. If independent samples share persistent neuron identities, use `forward_batch` with shape `(batch, population, time, contacts)`.

## Save and resume the adapted population

Continue the eager example above and save both module and optimizer states:

```python
from pathlib import Path

Path("runs").mkdir(exist_ok=True)
torch.save(
    {
        "population": population.state_dict(),
        "optimizer": optimizer.state_dict(),
    },
    "runs/adapted-population.pt",
)

# Reconstruct the same population and optimizer before a later session.
payload = torch.load(
    "runs/adapted-population.pt",
    map_location="cpu",
)
population.load_state_dict(payload["population"], strict=True)
optimizer.load_state_dict(payload["optimizer"])
```

Reconstruct the same Lite configuration, morphology assignments, contact routes, and enabled groups before loading. Saving only the Lite neuron omits the population's banks; saving only the population omits optimizer moments and update counts. Include scheduler, random, and data-order states when your continuation requires them. Load trusted PyTorch artifacts, and ensure restored optimizer tensors use the intended device before updating.

## Next steps

Capture the verified eager update with [CUDA Graphs](/cuda-graphs/) when shapes stay fixed. See [population interfaces](/api/interfaces/) and [adaptation API](/api/adaptation/) for exact signatures.
