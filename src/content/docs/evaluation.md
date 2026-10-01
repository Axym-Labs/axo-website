---
title: Evaluate models
description: Compute AxoBench core metrics and make paired comparisons on identical traces.
section: Evaluate and deploy
order: 90
---

## Use the AxoBench metric protocol

[AxoBench](https://github.com/Axym-Labs/axobench) defines the core metrics used by AxoSim: spike Mean F1, Voltage SERA, and Dynamics SERA. SERA uses squared error; Root-SERA is its square-root presentation. The evaluation path also provides calibration, diagnostics, and paired comparisons, while AxoSim supplies the checkpoint loader and prediction adapter.

Install the current AxoBench package in the same environment as AxoSim; source installation currently requires access to its private repository. Provide an ordinary AxoBench dataset root and a trusted checkpoint. Population contexts and intervention releases are distinct datasets, as explained in [datasets](/datasets/).

## Evaluate and save a cache

```bash
axosim-evaluate-model runs/axosim-mamba.pt \
  --dataset-root data/v1-neuronio-like-gpu-20260611 \
  --multiple-morphologies \
  --device cuda \
  --save-cache runs/axosim-mamba-axobench-cache.npz \
  --output runs/axosim-mamba-axobench.json
```

The evaluator prints a formatted report, writes the requested report, and saves a reusable prediction cache. The cache includes trace identities, target hash, metric protocol, and calibration boundary. The exact report fields come from your installed AxoBench version; retain that version or commit with the result.

## Compare on the same traces

First evaluate the baseline with `--save-cache`, then provide its cache to the candidate:

```bash
axosim-evaluate-model runs/candidate.pt \
  --baseline-cache runs/baseline-axobench-cache.npz \
  --dataset-root data/v1-neuronio-like-gpu-20260611 \
  --multiple-morphologies \
  --device cuda \
  --output runs/candidate-vs-baseline.json
```

A paired comparison requires matching target hashes and ordered trace identities, along with the same calibration and metric configuration. Matching only the dataset directory or sample count does not establish pairing. Alternatively, supply `--baseline-checkpoint` to construct the baseline predictions during the comparison.

## Calibration and interventions

The evaluator defaults to a 25% calibration fraction, a 500-step initial exclusion, and bootstrap comparisons with 250 replicates. `--multiple-morphologies` balances evaluation over available morphologies; `--morphology-id` chooses one morphology for the default single-morphology path. Use `--interventions` to select names explicitly and preserve their identities in the report.

`--save-cache` cannot be combined with a baseline comparison, and `--baseline-cache` and `--baseline-checkpoint` are mutually exclusive. See the [AxoBench CLI reference](/api/axobench-cli/) for all options and the [prediction adapter](/api/axobench/) for voltage and morphology handling.

## Measure inference throughput

`axosim inference-benchmark` measures a matrix of batch sizes, horizons, and precision choices for a supplied checkpoint. Record warmup, repetition count, device, included operations, and the input contract. Single-model sequence timing and complete connected-population execution cover different work, so label throughput by what was actually timed.

## Next steps

Preserve the cache, report, checkpoint hash, and dataset manifest using [reproducibility](/reproducibility/).
