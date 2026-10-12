---
title: Morphologies
description: The five excitatory teacher morphologies, the inhibitory population teacher, and leave-one-morphology-out partitions.
section: AxoBench
order: 135
---

## Excitatory teachers

The single-neuron and intervention releases use five dendrite-only reconstructions of mouse layer-5 spiny neurons from the Allen Cell Types Database. The population release uses the same five as its excitatory teachers. `specimen_488683425` is the reconstruction bundled with AxoBench as the template; the other four were ranked by a compatibility score against it, where lower is closer.

| Morphology | Cre line | Role | Branches | Total length | Radial extent | Apical fraction | Score |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `specimen_488683425` | Rbp4-Cre_KL100 | `reference_control` | 99 | 1.000 | 1.000 | 0.000 | 0.000 |
| `specimen_487664663` | Rbp4-Cre_KL100 | `closest_heldout_control` | 98 | 0.930 | 1.022 | +0.053 | 0.203 |
| `specimen_479770916` | Rorb-IRES2-Cre | `intermediate_line_shift` | 110 | 1.116 | 0.930 | −0.029 | 0.247 |
| `specimen_589427435` | Sim1-Cre_KJ18 | `line_diversity_shift` | 120 | 1.187 | 0.975 | +0.054 | 0.284 |
| `specimen_488679042` | Rorb-IRES2-Cre | `stronger_sane_length_shift` | 132 | 1.325 | 0.986 | +0.019 | 0.405 |

Total length and radial extent are ratios to the reference, and the apical fraction is a difference from it. The score adds the absolute logarithms of the total-length, routed-length, and radial-extent ratios, the absolute apical-fraction difference, and the branch-count difference of the routed representation divided by its 45 branches. The values come from the dataset manifest and `axobench.benchmark.v1_morphologies()`; `axobench benchmark-v1` writes them as routing QC rows.

The morphologies also differ in how many of the 639 source channels per sign reach a synapse; see [channel coverage](/axobench/single-neuron/#channel-coverage).

## Inhibitory teacher

The [population release](/axobench/population/) adds one inhibitory teacher, the Allen SST cell `allen_sst_specimen_482690728`. It supplies all 10,000 inhibitory population traces and appears in no other release.

## Morphology identity in the data

The text before the first colon of a sample ID identifies the morphology, and shard file names begin with it. AxoBench uses this prefix in three places:

- `evaluate_model(..., morphology_id="specimen_488679042")` evaluates one morphology. Without `morphology_id`, single-morphology mode uses the alphabetically first identity, `specimen_479770916`.
- `multiple_morphologies=True` interleaves the morphologies, so the default 120 traces contain 24 of each and the calibration block contains all five.
- Paired bootstrap intervals resample traces within each morphology, and the subthreshold RMSE fixes its action-potential window per morphology.

AxoSim models that condition on morphology need the same identity as an index into their declared morphology vocabulary. The [AxoSim prediction adapter](/api/axobench/) maps sample-ID prefixes to that index and rejects identities outside the vocabulary, so a held-out morphology must be declared before the model can be evaluated on it.

## Hold out a morphology

No released split withholds a morphology: `train`, `val`, and `test` each contain all five. To test transfer, build a leave-one-morphology-out partition. The [technical report](/report/main.pdf) uses five such comparisons: each source model is trained on the other four morphologies, and target adaptation and evaluation use separate traces of the omitted one.

Every shard contains a single morphology, so a source directory can link the shards of four morphologies together with the original manifest. AxoBench and the AxoSim trainer read only the manifest entries whose shards are present:

```bash
held_out=specimen_488679042
mkdir -p data/lomo-$held_out/train
ln -s "$PWD/data/axobench/train/manifest.json" data/lomo-$held_out/train/
for shard in data/axobench/train/specimen_*.npz; do
  case "$shard" in
    *"$held_out"_*) ;;
    *) ln -s "$PWD/$shard" data/lomo-$held_out/train/ ;;
  esac
done
```

The source directory then holds 80,000 traces. Adapt to the held-out morphology on its training traces, select on its validation traces, and report the final result on its test traces, for example with `evaluate_model(predict, dataset_root="data/axobench", morphology_id=held_out)` during selection. Selecting the adaptation recipe on the evaluation traces would make the comparison optimistic.

## Compare morphologies

The attention row `morphology_error_disparity` reports the worst morphology's voltage RMSE relative to the median morphology whenever an evaluation contains at least two. For a fuller comparison, run the evaluator once per `morphology_id` with the same sample limit, or derive `morphology_contrast` rows from per-morphology diagnostic rows as described in [diagnostics](/axobench/diagnostics/).

## Next steps

Use a held-out partition with [inference-time adaptation](/adaptation/), or [benchmark](/axobench/benchmarking/) each morphology separately.
