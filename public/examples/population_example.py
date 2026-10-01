"""Small runnable population used by the AxoSim documentation.

Run ``python population_example.py`` after installing AxoSim.
The random model and contacts demonstrate shapes, not biological fidelity.
"""

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
