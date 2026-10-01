"""Run the complete connected lifecycle on CPU with a functional wiring oracle.

The tiny hand-set model is NOT trained and supplies no biological evidence.
For an application, replace it with a trained Lite model and use its manifest's
channel order, E/I encoding, morphology identities and calibrated thresholds.
"""

from __future__ import annotations

import torch

from axosim import AxoSimLite, ExplicitConnectome, InputEvents, create_population
from axosim.support_surrogate import SupportP4Config


def build_demo_model():
    config = SupportP4Config(
        input_dim=2,
        route_feature_dim=1,
        token_dim=1,
        state_dim=1,
        morphology_ids=("functional-oracle",),
        behavior_adaptation=False,
    )
    model = AxoSimLite(config, torch.tensor([[[1.0], [-1.0]]]))
    with torch.no_grad():
        for parameter in model.parameters():
            parameter.zero_()
        model.input_projection.weight.fill_(1.0)
        model.skip_head.weight[::2].fill_(1.0)
    return model.eval()


def stimulus(time_ms):
    return (
        InputEvents(neurons=[0], channels=[0], values=[1.0]) if time_ms == 0 else None
    )


def build_demo_population():
    # Two independent parallel excitatory edges, then an inhibitory edge.
    connectome = ExplicitConnectome(
        sources=[0, 0, 1],
        targets=[1, 1, 2],
        channels=[0, 0, 1],
        source_roles=[1, 1, -1],
        delays=[4, 4, 4],
        efficacies=[0.5, 2.0, 1.0],
    )
    return create_population(
        model=build_demo_model(),
        n=3,
        connectome=connectome,
        morphology_indices=[0, 0, 0],
        input_encoding="channel",
        channel_roles=[1, -1],
        stream_inputs=stimulus,
        stream_outputs={
            "spikes": "all",
            "soma_target": [1],
            "hidden_state": [1],
            "input_features": [1],
        },
        spike_threshold=0.5,
    )


def main():
    sim = build_demo_population()
    first = list(sim.run(duration_ms=9))
    assert first[4].signals["spikes"].tolist() == [True, False, False]
    assert first[8].signals["input_features"].item() == 2.5
    frozen = sim.observe(neurons=[1], signals=("soma_target", "hidden_state"))
    saved = sim.state_dict()
    expected = list(sim.run(duration_ms=7))
    sim.load_state_dict(saved)
    replay = list(sim.run(duration_ms=7))
    for before, after in zip(expected, replay, strict=True):
        for signal in before.signals:
            assert torch.equal(before.signals[signal], after.signals[signal])
    assert frozen.time_ms == 8
    sim.set_efficacies([0], [3.0])
    assert sim.efficacies.tolist() == [3.0, 2.0, 1.0]
    sim.reset()
    assert sim.time_ms == 0
    assert sim.efficacies.tolist() == [0.5, 2.0, 1.0]
    print("t=4 ms: source spikes [True, False, False]")
    print("t=8 ms: target input_features [[2.5]]")
    print("continued to 16 ms; saved-state replay matched; reset restored 0 ms")


if __name__ == "__main__":
    main()
