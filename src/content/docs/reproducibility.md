---
title: Reproduce results
description: Preserve model, data, timing, and evidence identities and regenerate the report's frozen numerical bundle.
section: Evaluation and deployment
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

Use these commands to check that the report's tables and figures follow from the distributed evidence bundle. They regenerate publication assets without repeating training or GPU benchmarks. To investigate a numerical discrepancy, begin with the source hash and measurement contract of the affected row; a fresh hardware run answers a different question from regenerating a frozen figure.

## Recompute a result

Recomputation requires the corresponding data, weights, software revisions, and hardware workload. Preserve immutable checkpoint and dataset identities when rerunning a published evaluation. For paired caches, match the target hash and ordered trace IDs before comparing values.

If optimization continues, save optimizer moments, scheduler state, update count, and relevant random and data-order states. Model-only checkpoints are sufficient for inference but do not specify a complete resumed training trajectory. The [adaptation guide](/adaptation/) demonstrates population-and-optimizer persistence.

## Share a useful issue report

Provide a minimal reproducing command or script, tensor shapes and dtypes, software versions, device, checkpoint hash, dataset manifest hash, and the observed exception or numerical discrepancy. Avoid including credentials or private dataset samples in logs. [Troubleshooting](/troubleshooting/) helps identify common interface mismatches.
