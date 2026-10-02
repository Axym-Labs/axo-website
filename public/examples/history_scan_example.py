"""CPU examples of supplied-history execution with the sequential Mamba fallback.

The small untrained model checks shape, row independence and autograd. It is not
an accuracy result or a fused selective-scan performance measurement. Use an
official trained CUDA AxoMamba for require_parallel=True execution.
"""

from __future__ import annotations

import torch

from axosim import scan_histories
from axosim.axomamba import AxoMambaConfig, AxoPyTorchMamba


def build_reference_model():
    torch.manual_seed(7)
    config = AxoMambaConfig(
        num_input=8,
        num_output=2,
        num_branch=2,
        num_synapse_per_branch=4,
        model_dim=4,
        num_layers=1,
        state_dim=2,
        conv_kernel=2,
        expansion=1,
        morphology_ids=["m0", "m1"],
        morphology_embedding_scale=0.15,
    )
    return AxoPyTorchMamba(config).eval()


def make_histories(neurons=3):
    inputs = torch.zeros(neurons, 12, 8)
    inputs[:, [0, 4, 8], 0] = 1.0
    if neurons > 1:
        inputs[1, [2, 6], 4] = -0.5
    if neurons > 2:
        inputs[2, [1, 7], 2] = 0.75
    return inputs


def main():
    model = build_reference_model()
    single = make_histories(neurons=1)
    single_ids = torch.tensor([0])
    with torch.no_grad():
        one = scan_histories(
            model, single, morphology_indices=single_ids, require_parallel=False,
        )
        torch.testing.assert_close(
            one.prediction, model(single, morphology_indices=single_ids),
            atol=1e-6, rtol=1e-5,
        )
    assert one.prediction.shape == (1, 12, 2)
    assert one.backend.name == "pytorch-sequential-reference"
    assert not one.backend.parallel

    inputs = make_histories()
    ids = torch.tensor([0, 1, 0])
    with torch.no_grad():
        population = scan_histories(
            model, inputs, morphology_indices=ids,
            neuron_batch_size=2, require_parallel=False,
        )
        direct = model(inputs, morphology_indices=ids)
        torch.testing.assert_close(population.prediction, direct, atol=1e-6, rtol=1e-5)
        changed = inputs.clone()
        changed[0, :, 0] += 0.5
        altered = scan_histories(
            model, changed, morphology_indices=ids, require_parallel=False,
        ).prediction
    torch.testing.assert_close(altered[1:], population.prediction[1:], atol=1e-6, rtol=1e-5)
    assert not torch.allclose(altered[0], population.prediction[0])

    scanned_inputs = inputs.clone().requires_grad_()
    direct_inputs = inputs.clone().requires_grad_()
    scanned = scan_histories(
        model, scanned_inputs, morphology_indices=ids,
        neuron_batch_size=2, require_parallel=False,
    ).prediction
    direct = model(direct_inputs, morphology_indices=ids)
    # Compare both supplied-input derivatives and a real model-weight derivative.
    parameters = (model.readout.weight,)
    scanned_grad = torch.autograd.grad(scanned.square().mean(), (scanned_inputs, *parameters))
    direct_grad = torch.autograd.grad(direct.square().mean(), (direct_inputs, *parameters))
    for actual, expected in zip(scanned_grad, direct_grad, strict=True):
        assert torch.isfinite(actual).all()
        assert actual.abs().sum() > 0
        torch.testing.assert_close(actual, expected, atol=1e-6, rtol=1e-5)

    print(one.backend.name, one.backend.parallel)
    print("single", tuple(one.prediction.shape))
    print("population", tuple(population.prediction.shape))
    print("direct outputs, untouched neuron rows and input/model gradients agree")


if __name__ == "__main__":
    main()
