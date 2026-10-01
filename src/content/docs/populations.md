---
title: Build populations
description: Construct persistent Lite populations with morphology identities and mutable contact efficacies.
section: Build populations
order: 50
---

## Construct a Lite population

`AxoSimPopulation` wraps one Lite neuron with persistent morphology assignments, incoming contact routes, and adaptation banks. Download [population_example.py](/examples/population_example.py), or save the following code under that name, so later examples can import `build_population`:

```python
import torch
from axosim import AxoSimLite, AxoSimPopulation
from axosim.support_surrogate import SupportP4Config

def build_population(device="cpu"):
    config = SupportP4Config(
        input_dim=6,
        route_feature_dim=3,
        token_dim=4,
        state_dim=3,
        morphology_ids=("m0", "m1"),
    )
    route_features = torch.randn(2, 6, 3)
    neuron = AxoSimLite(config, route_features)
    population = AxoSimPopulation(
        neuron,
        morphology_indices=torch.tensor([0, 0, 1]),
        contact_branch_indices=torch.tensor([
            [0, 1, 2, 3],
            [0, 1, 2, 3],
            [2, 3, 4, 5],
        ]),
    )
    return population.to(device)

if __name__ == "__main__":
    population = build_population()
    contacts = torch.randn(3, 12, 4)
    prediction = population(contacts)
    assert prediction.shape == (3, 12, 2)
    print(prediction.shape)
```

```text
torch.Size([3, 12, 2])
```

Run the downloaded file from your working directory:

```bash
python population_example.py
```

This small randomly initialized model verifies the interface. For scientific use, initialize the shared Lite model from trained weights and supply route features appropriate to the declared morphologies. Constructing this PyTorch module does not invoke the fused AxoRuntime execution path used in the large connected benchmarks.

## Shapes and persistent identities

Let `N` be the persistent neuron count, `T` the horizon, `K` the incoming contacts per neuron, `M` the morphology count, `C` the Lite input width, and `R` the route-feature width.

| Value | Shape | Meaning |
| --- | --- | --- |
| `route_features` | `(M, C, R)` | Fixed morphology-conditioned input route features |
| `morphology_indices` | `(N,)` | Morphology-class index for each neuron |
| `contact_branch_indices` | `(N, K)` | Lite input-channel index for each incoming contact |
| `contact_inputs` | `(N, T, K)` | Signed native contact histories |
| `prediction` | `(N, T, 2)` | Spike logits and somatic-voltage coordinates |

Each contact has an independently mutable positive efficacy, `exp(synaptic_log_efficacy[n, k])`. The signed event carries excitation or inhibition; the efficacy scales its magnitude while retaining its sign. Morphology indices, contact routes, and adapter values persist in the module.

## Causal padding and sequence boundaries

Lite predicts each four-step block from preceding inputs. The first four output positions are causal padding, so mask them in losses and metrics. Each forward call initializes temporal hidden state for the supplied sequence; hidden state does not continue automatically into the next call.

Contact count affects memory and execution cost. Include `N`, `T`, and `K` when reporting a population measurement. The [population interface reference](/api/interfaces/) provides complete signatures and checks.

## Batch independent examples through shared neurons

Independent examples can share one population's neuron identities and adaptation banks:

```python
import torch
from population_example import build_population

population = build_population()
examples = torch.randn(2, 3, 12, 4)
prediction = population.forward_batch(examples)
assert prediction.shape == (2, 3, 12, 2)
print(prediction.shape)
```

```text
torch.Size([2, 3, 12, 2])
```

The batch axis represents independent examples rather than newly created neurons. `forward_tokens` and `forward_token_batch` expose pre-encoded four-step tokens when your input encoder already satisfies the Lite token contract.

## Next steps

Submit [sparse contact events](/sparse-events/) to avoid dense contact histories, or enable the adaptation banks in [inference-time adaptation](/adaptation/).
