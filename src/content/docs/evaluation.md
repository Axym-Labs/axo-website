---
title: Evaluate models
description: Compute AxoBench core metrics and make paired comparisons on identical traces.
section: Evaluation and deployment
order: 90
---

## Use the AxoBench metric protocol

AxoBench defines the metric protocol used to evaluate AxoSim checkpoints. Its core metrics in version 0.2.0 are Voltage SERA, spike Mean F1 over 0–5 ms tolerances, the subthreshold voltage RMSE, and Response SERA; SERA is the IRon-default squared error-relevance area per teacher spike, in mV²/spike. Dynamics SERA remains a secondary row. [Core metrics](/axobench/metrics/) gives the definitions and [benchmarking](/axobench/benchmarking/) the protocol. AxoBench owns calibration, diagnostics, and paired comparisons, while AxoSim supplies the checkpoint loader and prediction adapter.

Install AxoBench 0.2.0 or newer in the same environment as AxoSim, as described in [benchmarking](/axobench/benchmarking/#install-axobench). Provide an evaluation root with the single-neuron `val` split and, optionally, the paired interventions under `interventions/`, as assembled in [choose a dataset](/datasets/#assemble-an-evaluation-root), and a trusted checkpoint.

## Evaluate and save a cache

```bash
axosim-evaluate-model runs/axosim-mamba.pt \
  --dataset-root data/axobench \
  --multiple-morphologies \
  --device cuda \
  --save-cache runs/axosim-mamba-axobench-cache.npz \
  --output runs/axosim-mamba-axobench.json
```

The evaluator prints a formatted report, writes the requested report, and saves a reusable prediction cache. The cache includes trace identities, target hash, metric protocol, and calibration boundary. The exact report fields come from your installed AxoBench version; retain that version or commit with the result. [Read the report](/axobench/benchmarking/#read-the-report) lists the metric rows, and [diagnostics](/axobench/diagnostics/#read-the-attention-panel) explains the 24 attention rows.

## Compare on the same traces

First evaluate the baseline with `--save-cache`, then provide its cache to the candidate:

```bash
axosim-evaluate-model runs/candidate.pt \
  --baseline-cache runs/baseline-axobench-cache.npz \
  --dataset-root data/axobench \
  --multiple-morphologies \
  --device cuda \
  --output runs/candidate-vs-baseline.json
```

A saved baseline cache fixes the reference predictions and avoids rerunning that model for every candidate. Pairing still requires matching target hashes and ordered trace identities, along with the same calibration and metric configuration. Matching only the dataset directory or sample count does not establish pairing. Alternatively, supply `--baseline-checkpoint` to construct the baseline predictions during the comparison.

## Calibration and interventions

The evaluator defaults to 120 validation traces and 40 pairs per intervention condition, a 25% calibration fraction, a 500-step initial exclusion, and bootstrap comparisons with 250 replicates. `--multiple-morphologies` balances evaluation over available morphologies; `--morphology-id` chooses one morphology for the default single-morphology path, which otherwise uses the alphabetically first. Use `--interventions` to select names explicitly and preserve their identities in the report. [Calibration and scoring](/axobench/benchmarking/#calibration-and-scoring) describes how the threshold and scored traces are separated, and [paired interventions](/axobench/interventions/) describes the conditions.

`--save-cache` cannot be combined with a baseline comparison, and `--baseline-cache` and `--baseline-checkpoint` are mutually exclusive. See the [AxoBench CLI reference](/api/axobench-cli/) for all options and the [prediction adapter](/api/axobench/) for voltage and morphology handling.

## Measure inference throughput

`axosim inference-benchmark` measures a matrix of batch sizes, horizons, and precision choices for a supplied checkpoint. Record warmup, repetition count, device, included operations, and the input contract. Single-model sequence timing and complete connected-population execution cover different work, so label throughput by what was actually timed.

## Next steps

Preserve the cache, report, checkpoint hash, and dataset manifest using [reproducibility](/reproducibility/).
