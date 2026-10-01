---
title: Reproduce results
description: Preserve model, data, timing, and evidence identities and regenerate the report's frozen numerical bundle.
section: Evaluate and deploy
order: 110
---

## Record the result contract

For every result, save the AxoSim commit, checkpoint hash, dataset manifest and shard hashes, PyTorch and CUDA versions, GPU model, precision, and the complete command or resolved configuration. Include batch size, horizon, contact count, warmup, repetitions, synchronization, and included operations for a runtime result.

A model forward pass, a forward-plus-backward pass, a complete optimizer update, and connected-population execution have different timing boundaries. Naming the boundary makes the measurement usable to someone selecting hardware or planning a workload.

## Regenerate the numerical bundle

The [technical-report repository](https://github.com/Axym-Labs/AxoSim-paper) contains a portable reproducer. From that checkout, run:

```bash
python reproducibility/reproduce_headline_claims.py \
  --output-dir build/claims
python reproducibility/reproduce_publication.py \
  --output-dir build/publication
```

The scripts regenerate claim tables and publication assets from frozen evidence. They do not repeat model training or GPU benchmarks. Inspect the source hashes, hardware contracts, evidence domain, and availability fields associated with each generated row.

## Recompute a result

Recomputation requires the corresponding data, weights, software revisions, and hardware workload. Preserve immutable checkpoint and dataset identities when rerunning a published evaluation. For paired caches, match the target hash and ordered trace IDs before comparing values.

If optimization continues, save optimizer moments, scheduler state, update count, and relevant random and data-order states. Model-only checkpoints are sufficient for inference but do not specify a complete resumed training trajectory. The [adaptation guide](/adaptation/) demonstrates population-and-optimizer persistence.

## Share a useful issue report

Provide a minimal reproducing command or script, tensor shapes and dtypes, software versions, device, checkpoint hash, dataset manifest hash, and the observed exception or numerical discrepancy. Avoid including credentials or private dataset samples in logs. [Troubleshooting](/troubleshooting/) helps identify common interface mismatches.
