---
title: Overview
description: Learned neuron models for fast population simulation and inference-time adaptation.
section: Get started
order: 0
---

AxoSim approximates the response of detailed biological neurons to synaptic input histories. You can load trained GRU and Mamba models, construct populations with explicit dendritic contacts, and adapt neuronal and synaptic parameters through a complete temporal sequence.

<figure class="overview-figure">
  <img class="figure-light" src="/figures/central-comparison.svg" width="38724" height="18203" alt="AxoSim-GRU Small and Mamba Medium in color, alongside Branch-ELM models and the CoreNEURON reference in gray, compared on inference and history throughput, voltage and dynamics fidelity, and spike Mean F1." fetchpriority="high" />
  <img class="figure-dark" src="/figures/central-comparison-dark.svg" width="38724" height="18203" alt="AxoSim-GRU Small and Mamba Medium in color, alongside Branch-ELM models and the CoreNEURON reference in gray, compared on inference and history throughput, voltage and dynamics fidelity, and spike Mean F1." fetchpriority="high" />
</figure>

<p class="figure-caption">The axes show (i) inference throughput, counting 1-ms neuron predictions per second; (ii) voltage fidelity from somatic-voltage SERA; (iii) dynamics fidelity from native-time voltage-change SERA; (iv) spike Mean F1, averaged over 0–5 ms matching tolerances; and (v) history throughput, counting input milliseconds processed per second for one supplied 2-second history. CoreNEURON is the ground-truth detailed simulator, and Branch-ELM is the learned-surrogate predecessor of AxoSim. AxoSim–GRU Small and Mamba Medium are compared with three released Branch-ELM sizes; larger radii indicate better performance. Raw measurements, fixed mappings and runtime contracts appear in the appendix of the <a href="/report/main.pdf">technical report</a>.</p>

<div class="resource-links">
  <a href="/installation/">Get started →</a>
  <a href="/report/main.pdf">Technical report</a>
  <a href="https://github.com/Axym-Labs/axosim">Code ↗</a>
  <a href="https://axym.org/work/axosim-fly-geometry/">Demo ↗</a>
  <a href="https://huggingface.co/datasets/Axym-Labs/axobench-population">Population data ↗</a>
  <a href="https://huggingface.co/datasets/Axym-Labs/axobench-interventions">Interventions ↗</a>
</div>

## Start with a neuron model

Use [model selection](/models/) to choose a temporal architecture and backend, then [load a checkpoint](/inference/) to predict spike logits and somatic voltage. The common single-neuron contract is an input tensor shaped `(batch, time, input channels)` and an output tensor shaped `(batch, time, 2)`.

The trained architectures extend the branching mechanism of Branch-ELM. Signed input events preserve their dendritic destinations, while GRU or Mamba temporal cores model the response history. Use [history processing](/history-scan/) when complete input histories are available, or [streaming inference](/inference/#preserve-temporal-state-when-streaming) when inputs arrive over time.

## Connect and adapt populations

The [population interface](/populations/) combines a compact AxoSim-Lite neuron model with morphology identities, dendritic contact routes, and independently mutable synaptic efficacies. [Sparse events](/sparse-events/) preserve contact identity without allocating a dense contact history. [Inference-time adaptation](/adaptation/) selects behavior, morphology, and synaptic parameter groups while differentiating through the supplied sequence.

The optimized runtime evaluated in the report simulates **65,536 neurons with 4,000 retained contacts per neuron at 3.38× real time** on an RTX 5090. Full BPTT reaches real time for **20,000 neurons with 2,000 retained contacts**. These measurements describe the frozen benchmark implementation. Use [`create_population`](/connected-populations/) for connected rollout, or [`AxoSimPopulation`](/populations/) to fit supplied Lite histories. [Reproducibility and deployment](/reproducibility/) explains how to recover the reported evidence and which execution paths are covered by the measurements.

## Follow the lifecycle

1. [Install AxoSim](/installation/) and inspect the model presets.
2. [Choose a model](/models/), [run inference](/inference/), and [train on your data](/training/).
3. [Build a population](/populations/), then use [sparse contact events](/sparse-events/) for sparse inputs.
4. [Adapt parameter groups](/adaptation/) and [capture repeated CUDA updates](/cuda-graphs/) when shapes are fixed.
5. [Evaluate on AxoBench](/evaluation/), obtain the [datasets](/datasets/), and preserve [reproducibility records](/reproducibility/).
6. Use the [API reference](/api/) for exact signatures, defaults, and source links.

## Cite AxoSim

The technical report is by Davide Wiest and Jonathan Schäfer, Axym Labs. AxoBench introduces the core metric set used throughout the report: spike Mean F1, Voltage SERA, and Dynamics SERA. SERA denotes the squared error metric; Root-SERA is its square root.

```bibtex
@techreport{wiest2026axosim,
  title = {AxoSim: Learned Neuron Models for Population Simulation at Scale},
  author = {Wiest, Davide and Schäfer, Jonathan},
  institution = {Axym Labs},
  year = {2026},
  url = {https://axo.axym.org/report/main.pdf}
}
```
