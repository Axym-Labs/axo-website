---
title: Simulate a connected population
description: Supply a trained Lite neuron, define exact recurrent contacts, and stream selected signals with persistent state.
section: Simulation
order: 30
---

## Run the complete lifecycle

After [installation](/installation/), use `create_population` to construct a connected Lite simulator. The simulator retains each neuron's learned state, thresholds, pending deliveries and native clock, so events emitted by one neuron become delayed inputs to its targets. A second `run` continues the same simulation.

Download [connected_population_example.py](/examples/connected_population_example.py) into your working directory and run it:

```bash
python connected_population_example.py
```

```text
t=4 ms: source spikes [True, False, False]
t=8 ms: target input_features [[2.5]]
continued to 16 ms; saved-state replay matched; reset restored 0 ms
```

This self-contained example uses a tiny hand-set model to verify wiring, delayed recurrence, selected observations, continuation and replay. It is a functional example, not a trained biological model or an accuracy result. For an application, supply trained Lite weights and their input/morphology metadata as follows.

## Supply trained weights and an exact graph

Provide a trusted Lite checkpoint, the checkpoint's channel-role vector and input convention, and a development-calibrated spike-logit threshold. The manifest in this mixed E/I example is your own JSON file with `channel_roles` (+1 or −1 per input channel, with at least one channel for each role), `input_encoding` (`"signed"` or `"channel"`), `morphology_id`, and `spike_threshold`; these fields must describe the weights and channel order actually used in training.

```python
import json
import torch
from axosim import AxoSimLite, ExplicitConnectome, InputEvents, create_population
from axosim.checkpoint import load_checkpoint

trained_lite, metadata = load_checkpoint("path/to/trained-lite.pt", map_location="cpu")
if not isinstance(trained_lite, AxoSimLite):
    raise TypeError("This connected backend requires trained AxoSimLite weights")
with open("path/to/input-manifest.json") as source:
    manifest = json.load(source)

roles = torch.tensor(manifest["channel_roles"], dtype=torch.long)
exc_channel = int((roles == 1).nonzero()[0])
inh_channel = int((roles == -1).nonzero()[0])
morphology = trained_lite.config.morphology_ids.index(manifest["morphology_id"])
connectome = ExplicitConnectome(
    sources=[0, 0, 1], targets=[1, 1, 2],
    channels=[exc_channel, exc_channel, inh_channel],
    source_roles=[1, 1, -1], delays=[4, 7, 4], efficacies=[0.5, 2.0, 1.0],
)

def stimulus(time_ms):
    if time_ms == 0:
        return InputEvents(neurons=[0], channels=[exc_channel], values=[1.0])
    return None

population = create_population(
    model=trained_lite.eval(), n=3, connectome=connectome,
    morphology_indices=[morphology] * 3,
    input_encoding=manifest["input_encoding"], channel_roles=roles,
    spike_threshold=manifest["spike_threshold"], stream_inputs=stimulus,
    stream_outputs={"spikes": "all", "soma_target": [1], "hidden_state": [1]},
)
for frame in population.run(duration_ms=16):
    if frame.valid:
        print(frame.time_ms, frame.signals["spikes"].shape)
assert population.time_ms == 16
```

The two edges from neuron 0 to neuron 1 have separate delays and efficacies despite sharing a destination channel. Their identities remain distinct; a source may have any number of outgoing edges, and a destination may have any number of incoming edges. Every outgoing edge of a neuron must declare the same source role. The graph is validated without dropping edges or changing delays.

Choose the input convention deliberately. With `input_encoding="signed"`, an inhibitory recurrent event has a negative amplitude; with `"channel"`, both roles use nonnegative event counts because channel identity and trained route features encode inhibition. External values already use that convention and receive no additional source sign. When `channel_roles` is supplied, signed values must agree with the channel role; channel-encoded external values must always be nonnegative. Neither convention applies inhibition twice.

## Interpret timestamps and selected signals

One native simulation step is 1 ms. Lite accumulates four input samples, updates its learned state, and forecasts the next four output samples; recurrent delays must therefore be at least 4 ms. Frames at 0–3 ms have `valid=False` and emit no spikes, even with a zero or negative threshold. Exclude these causal-padding outputs from metrics.

| Signal | Shape for L selected neurons | Units and meaning |
| --- | --- | --- |
| `spikes` | `(L,)` | Boolean event, `spike_logit > threshold`, false during warmup |
| `spike_logit` | `(L,)` | Native uncalibrated logit |
| `soma_target` | `(L,)` | Checkpoint's soma target coordinate |
| `soma_mv` | `(L,)` | Millivolts, only with explicit `soma_transform=(scale_mv, offset_mv)` |
| `hidden_state` | `(L, state_dim)` | Learned Lite state, not a membrane or channel measurement |
| `input_features` | `(L, route_feature_dim)` | Current external plus delivered recurrent input after morphology routing |

At timestamps 3, 7, 11, …, `hidden_state` reflects the input patch just completed, while the spike and soma values are the current sample from the preceding forecast. Between these boundaries, learned state is held. Thus native output timestamps do not imply a separate learned-state transition every millisecond.

Each frame includes `neuron_ids` for every selected signal. Selection occurs on the simulation device before copying, and frames own their tensors: later execution or edits to a returned frame cannot change the runtime. Transfer only what you need, for example `frame.signals["soma_target"].cpu()`. With `sample_every_ms=4`, `run` copies observations only at native timestamps 0, 4, 8, … while still simulating every intervening sample. `step()` always returns the native frame it advances.

For standard NeuronIO targets, `soma_transform=(10.0, -67.7)` reverses the affine training coordinate. Use it only when the checkpoint's conversion metadata confirms that normalization; clipped teacher spike peaks cannot be recovered by this transform.

## Continue, inspect and replay

The following continuation uses the downloaded functional example; the same methods apply to the trained population above. `observe` does not advance time, and its returned tensors remain unchanged after the next run.

```python
from connected_population_example import build_demo_population

population = build_demo_population()
first = list(population.run(duration_ms=9))
snapshot = population.observe(neurons=[1], signals=("soma_target", "hidden_state"))
saved = population.state_dict()
continued = list(population.run(duration_ms=7))
assert continued[0].time_ms == 9
assert population.time_ms == 16
assert snapshot.time_ms == 8

population.load_state_dict(saved)
replayed = list(population.run(duration_ms=7))
assert replayed[0].time_ms == 9
population.reset()
assert population.time_ms == 0
```

For disk persistence, save the runtime snapshot and restore it into a population constructed from the same trained model, topology, morphology assignment, input convention and backend:

```python
import torch

torch.save(saved, "population-state.pt")
population.load_state_dict(torch.load("population-state.pt", weights_only=True))
```

Snapshots contain the partial input patch, forecasts, learned state, pending deliveries, native clock, thresholds, direct runtime coefficients and exact edge efficacies. A model/topology fingerprint prevents incompatible restoration, and malformed snapshots are rejected before runtime mutation. Weights and topology are supplied separately. Replay also requires the same external input at each timestamp: deterministic native-time callbacks and timestamp mappings support this contract, whereas arbitrary input iterators are rejected because their hidden position cannot be restored. `reset` restores construction-time thresholds and efficacies as well as the initial clock, state and empty queue.

Consuming `run` advances simulation; constructing its iterator does nothing. The simulator retains no unbounded history or background export queue, so pausing the consumer pauses simulation. `run(duration_ms=0)` performs no work. Preserve complete spike events with `sample_every_ms=1`; a coarser cadence samples boolean activity rather than accumulating skipped spike events.

## Edit individual contacts

An efficacy is a nonnegative magnitude independent of E/I role. Update exact edge IDs, including parallel edges, without changing their topology:

```python
from connected_population_example import build_demo_population

population = build_demo_population()
population.set_efficacies(edge_ids=[0], values=[3.0])
print(population.efficacies.tolist())
```

```text
[3.0, 2.0, 1.0]
```

Each emitted event uses the efficacy present at emission time; already queued arrivals keep their scheduled amplitudes. Setting an efficacy to zero disables future deliveries on that edge while preserving its identity. Efficacies and queue accumulation use float32 even when the Lite neuron uses FP16, so the facade does not silently quantize contacts.

## Select a supported backend

| Backend | Model and device | Topology and precision |
| --- | --- | --- |
| `reference` | Supplied Lite; CPU or CUDA | Explicit ragged/parallel graph or deterministic procedural fan-out; model dtype for neuron execution, float32 edge efficacies and feature queue |
| `fused` | Supplied CUDA FP16 Lite; Triton required | Same exact graph lifecycle; installed fused Lite recurrence/decoder kernel, direct FP16 runtime coefficients and float32 contacts/queue |

The fused backend accelerates the neuron recurrence and decoder. Routing remains the exact-edge scheduler described here; it is separate from the specialized tiled, quantized procedural runtime used for published large-population timings. Those measurements are not speed claims for arbitrary graphs constructed by this facade. FP16 arithmetic can shift logits near a threshold, so compare native outputs with numerical tolerances and evaluate event sensitivity at your calibrated threshold.

For an implicit deterministic fan-out graph, choose source roles and destination channel roles explicitly. This complete CPU example uses the downloadable functional model. Each source has three retained edges; targets and matching-role channels are computed for active sources, while all nine efficacies remain independently stored.

```python
from axosim import ProceduralConnectome, create_population
from connected_population_example import build_demo_model, stimulus

graph = ProceduralConnectome(
    n=3, out_degree=3, input_dim=2, neuron_roles=[1, -1, 1],
    channel_roles=[1, -1], delay_ms=4, seed=7, efficacy=0.5,
)
population = create_population(
    model=build_demo_model(), n=3, connectome=graph,
    morphology_indices=[0, 0, 0], input_encoding="channel",
    stream_inputs=stimulus, stream_outputs={"spikes": "all"}, spike_threshold=0.5,
)
assert len(list(population.run(duration_ms=12))) == 12
assert population.efficacies.shape == (9,)
```

This topology permits self and parallel edges and any positive population size; it is not an imported empirical connectome. `graph.materialize()` produces the equivalent explicit graph for small inspections. To use fused neuron execution with either supported graph, pass `model=trained_lite.to("cuda").half().eval()` and `backend="fused"`; model conversion is explicit and does not change the CPU model already owned by a different population.

## Fit supplied histories separately

Use [supplied population histories](/populations/) when fitting shared/adaptive parameters with full temporal gradients. For Mamba predictions from complete recorded native inputs, use [supplied-history scan](/history-scan/), with the same interface for one neuron or a population sharing weights. The fused temporal scan applies after all inputs are known; future recurrent inputs in a live connected simulation still require causal rollout.

`AxoSimPopulation` runs externally supplied contact histories and starts sequence state afresh; `ConnectedPopulation` owns delayed closed-loop inference state and discrete thresholded events. The [connected API reference](/api/connected-population/) provides exact constructor, graph, observation and replay signatures.
