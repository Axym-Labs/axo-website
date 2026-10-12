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

## Start with a neuron model

Use [model selection](/models/) to choose a temporal architecture and backend, then [load a checkpoint](/inference/) to predict spike logits and somatic voltage. The common single-neuron contract is an input tensor shaped `(batch, time, input channels)` and an output tensor shaped `(batch, time, 2)`.

The trained architectures extend the branching mechanism of Branch-ELM. Signed input events preserve their dendritic destinations, while GRU or Mamba temporal cores model the response history. Use [history processing](/history-scan/) when complete input histories are available, or [streaming inference](/inference/#preserve-temporal-state-when-streaming) when inputs arrive over time.

## Connect and adapt populations

The [population interface](/populations/) combines a compact AxoSim-Lite neuron model with morphology identities, dendritic contact routes, and independently mutable synaptic efficacies. [Sparse events](/sparse-events/) preserve contact identity without allocating a dense contact history. [Inference-time adaptation](/adaptation/) selects behavior, morphology, and synaptic parameter groups while differentiating through the supplied sequence.

The optimized runtime evaluated in the report simulates **65,536 neurons with 4,000 retained contacts per neuron at 3.38× real time** on an RTX 5090. Full BPTT reaches real time for **20,000 neurons with 2,000 retained contacts**. These measurements describe the frozen benchmark implementation. Use [`create_population`](/connected-populations/) for connected rollout, or [`AxoSimPopulation`](/populations/) to fit supplied Lite histories. [Reproducibility and deployment](/reproducibility/) explains how to recover the reported evidence and which execution paths are covered by the measurements.

## Benchmark with AxoBench

AxoBench provides the datasets, metrics, and evaluation protocol for single-neuron fidelity. It accepts any NumPy prediction function and depends only on NumPy, Matplotlib, and Requests.

- **Datasets.** Detailed-teacher simulations in three releases: [single-neuron traces](/axobench/single-neuron/) from five layer-5 pyramidal morphologies, [population contexts](/axobench/population/) whose inputs were recorded in connected AxoSim networks, and [paired interventions](/axobench/interventions/) that change one input sample in a defined way. [NeuronIO](/axobench/neuronio/) simulations convert to the same format.
- **Metrics.** The [core metrics](/axobench/metrics/) are Voltage SERA, spike Mean F1 over 0–5 ms tolerances, the subthreshold voltage RMSE, and Response SERA.
- **Evaluation.** The [evaluator](/axobench/benchmarking/) calibrates the spike threshold on traces that are not scored and compares a candidate with a cached baseline on identical traces, with paired bootstrap intervals.
- **Diagnostics.** Every report ends with a fixed 24-row [attention panel](/axobench/diagnostics/#read-the-attention-panel). Controlled defects test how each metric responds, and diagnostic rows export to JSON, JSONL, or CSV.
- **Plots.** [`axobench diagnostic-plots`](/axobench-api/cli/#diagnostic-plots) writes the diagnostic figures and tables from saved audit summaries as SVG, PDF, and PNG.

Start with [choose a dataset](/datasets/), then [benchmark a model](/axobench/benchmarking/).

## Follow the lifecycle

1. [Install AxoSim](/installation/) and inspect the model presets.
2. [Choose a model](/models/), [run inference](/inference/), and [train on your data](/training/).
3. [Build a population](/populations/), then use [sparse contact events](/sparse-events/) for sparse inputs.
4. [Adapt parameter groups](/adaptation/) and [capture repeated CUDA updates](/cuda-graphs/) when shapes are fixed.
5. [Choose an AxoBench dataset](/datasets/), [evaluate the checkpoint](/evaluation/) with the [AxoBench protocol](/axobench/benchmarking/), and preserve [reproducibility records](/reproducibility/).
6. Use the [AxoSim API reference](/api/) and the [AxoBench API reference](/axobench-api/) for exact signatures, defaults, and source links.

## Cite AxoSim

The technical report is by Davide Wiest and Jonathan Schäfer, Axym Labs. It evaluates single-neuron fidelity with AxoBench's spike Mean F1, Voltage SERA, and Dynamics SERA under the SERA definition stated in the report. AxoBench 0.2.0 redefines SERA per teacher spike and replaces Dynamics SERA in the core set with the subthreshold voltage RMSE, so its values are not comparable with the report's; see [core metrics](/axobench/metrics/#relation-to-the-technical-report).

```bibtex
@techreport{wiest2026axosim,
  title = {AxoSim: Learned Neuron Models for Population Simulation at Scale},
  author = {Wiest, Davide and Schäfer, Jonathan},
  institution = {Axym Labs},
  year = {2026},
  url = {https://axo.axym.org/report/main.pdf}
}
```
