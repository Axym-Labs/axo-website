---
title: Choose a dataset
description: Match the single-neuron, population, and intervention releases to training, selection, and evaluation questions.
section: Get started
order: 25
---

AxoBench releases three datasets on Hugging Face. They share one input and target contract: native 1 ms samples, 1,278 signed event channels (639 excitatory, then 639 inhibitory), and a `(time, 2)` target of spike indicator and normalized somatic voltage. They differ in where the inputs come from and therefore in the question they answer.

## Compare the releases

<div class="model-catalog dataset-catalog">
  <section class="model-card">
    <a class="model-art dataset-art single" href="/axobench/single-neuron/" aria-label="Explore Single-neuron traces"><svg viewBox="0 0 300 160" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path class="trace" d="M0.0 136 L3.0 136.8 L6.0 137.5 L9.0 138.2 L12.0 138.7 L15.0 139.1 L18.0 139.4 L21.0 139.5 L24.0 139.5 L27.0 139.4 L30.0 139.2 L33.0 138.8 L36.0 137.9 L39.0 136.7 L42.0 135.4 L45.0 134.2 L48.0 133 L51.0 131.8 L52.0 131.5 L53.2 90 L54.6 136.9 L57.0 134.5 L60.0 135.8 L63.0 135.9 L66.0 136 L69.0 136.2 L72.0 136.4 L75.0 136.8 L78.0 137.1 L81.0 137.4 L84.0 137.7 L87.0 138 L90.0 138.1 L93.0 138.2 L96.0 138.2 L99.0 138.1 L102.0 137.8 L105.0 136.9 L108.0 135.7 L111.0 134.3 L114.0 132.9 L117.0 131.4 L120.0 130 L121.0 129.5 L122.2 90 L123.6 134.9 L126.0 132.5 L129.0 132.7 L132.0 132.3 L135.0 131.9 L138.0 131.8 L141.0 131.7 L144.0 131.8 L147.0 132 L150.0 132.4 L153.0 132.1 L156.0 131.9 L159.0 131.7 L162.0 131.6 L165.0 131.5 L168.0 131.3 L169.2 90 L170.6 136.70000000000002 L173.0 134.3 L176.0 137.6 L179.0 138 L182.0 138.3 L185.0 138.4 L188.0 138.4 L191.0 138.3 L194.0 138.1 L197.0 137.8 L200.0 137.4 L203.0 136.9 L206.0 136.5 L209.0 136.1 L212.0 135.7 L215.0 135.3 L218.0 135.1 L221.0 134.9 L224.0 134.8 L227.0 134.9 L230.0 134.8 L233.0 134.3 L236.0 133.8 L239.0 133.5 L242.0 133.1 L245.0 132.8 L247.0 132.6 L248.2 90 L249.6 138 L252.0 135.6 L255.0 138.5 L258.0 138.8 L261.0 139 L264.0 139.1 L267.0 139 L270.0 138.8 L273.0 138.5 L276.0 138.1 L279.0 137.6 L282.0 137 L285.0 136.4 L288.0 135.7 L291.0 135.1 L294.0 134.5 L297.0 134 L300.0 133.6"/></svg><span>Single neuron</span></a>
    <h3><a href="/axobench/single-neuron/">Single-neuron traces</a></h3>
    <p>CoreNEURON traces from five layer-5 pyramidal morphologies in <code>train</code>, <code>val</code>, and <code>test</code> splits. Use them for pretraining, recipe selection, and the ordinary AxoBench evaluation.</p>
    <dl>
      <div><dt>Repository</dt><dd><a href="https://huggingface.co/datasets/Axym-Labs/axobench"><code>Axym-Labs/axobench</code></a></dd></div>
      <div><dt>Traces</dt><dd>125,000 × 6,000 ms<span class="data-bar" style="--share: 100%"><span>208 h simulated</span></span></dd></div>
      <div><dt>Inputs</dt><dd>A seeded event sample per trace</dd></div>
      <div><dt>Download</dt><dd>26.5 GB<span class="data-bar" style="--share: 100%"></span></dd></div>
      <div><dt>Use it</dt><dd><a href="/axobench/single-neuron/#use-the-splits">Train and select a model →</a></dd></div>
    </dl>
  </section>
  <section class="model-card">
    <a class="model-art dataset-art population" href="/axobench/population/" aria-label="Explore Population contexts"><svg viewBox="0 0 300 160" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path class="trace thin" d="M0.0 110.2 L4.0 110.4 L8.0 110.6 L12.0 110.8 L16.0 111 L20.0 111.3 L24.0 111.2 L28.0 110.9 L32.0 110.5 L36.0 110 L40.0 109.5 L41.2 93 L42.6 112.2 L45.0 111 L48.0 111.8 L52.0 111.6 L56.0 111.4 L60.0 111.1 L64.0 110.8 L68.0 110.5 L72.0 110.1 L76.0 109.7 L80.0 109.4 L84.0 109.1 L88.0 108.8 L92.0 108.5 L96.0 108.4 L100.0 108.3 L104.0 108.3 L108.0 108.3 L112.0 108.4 L116.0 108.6 L120.0 108.8 L124.0 109.1 L128.0 109.4 L132.0 109.7 L136.0 109.9 L140.0 110.2 L144.0 110.5 L148.0 110.7 L152.0 110.8 L156.0 110.9 L160.0 111 L164.0 110.9 L168.0 110.9 L172.0 110.8 L176.0 110.1 L180.0 109.4 L184.0 108.7 L188.0 108 L190.0 107.6 L191.2 93 L192.6 110.3 L195.0 109.1 L198.0 109.7 L202.0 109.6 L206.0 109.5 L210.0 109.5 L214.0 109.5 L218.0 109.5 L222.0 109.6 L226.0 109.7 L230.0 109.8 L234.0 109.9 L238.0 110 L242.0 110.1 L246.0 110.2 L250.0 110.3 L254.0 110.3 L258.0 110.3 L262.0 110.2 L266.0 110.1 L270.0 109.9 L274.0 109.8 L278.0 109.6 L282.0 109.4 L286.0 109.2 L290.0 109 L294.0 108.8 L298.0 108.7"/><path class="trace thin" d="M0.0 127.1 L4.0 127 L8.0 127 L12.0 126.9 L16.0 126.9 L20.0 126.8 L24.0 126.8 L28.0 126.8 L32.0 126.8 L36.0 126.8 L40.0 126.8 L44.0 126.8 L48.0 126.9 L52.0 126.9 L56.0 127 L60.0 127 L64.0 127.1 L68.0 127.2 L72.0 127.3 L76.0 127.5 L80.0 127.6 L84.0 127.7 L88.0 127.9 L92.0 128.1 L96.0 127.7 L100.0 127.3 L104.0 127 L108.0 126.6 L110.0 126.5 L111.2 111 L112.6 129.2 L115.0 128 L118.0 129.2 L122.0 129.4 L126.0 129.5 L130.0 129.6 L134.0 129.8 L138.0 129.9 L142.0 129.9 L146.0 130 L150.0 130 L154.0 130 L158.0 130 L162.0 130 L166.0 129.9 L170.0 129.9 L174.0 129.7 L178.0 129.6 L182.0 129.5 L186.0 129.3 L190.0 129.1 L194.0 128.9 L198.0 128.6 L202.0 128.4 L206.0 128.2 L210.0 127.9 L214.0 127.6 L218.0 127.4 L222.0 127.1 L226.0 126.9 L230.0 126.7 L234.0 126.2 L238.0 125.5 L242.0 124.8 L246.0 124.1 L250.0 123.4 L251.2 111 L252.6 126.10000000000001 L255.0 124.9 L258.0 125.6 L262.0 125.6 L266.0 125.6 L270.0 125.6 L274.0 125.6 L278.0 125.7 L282.0 125.8 L286.0 125.9 L290.0 126.1 L294.0 126.3 L298.0 126.5"/><path class="trace thin" d="M0.0 146.2 L4.0 146 L8.0 145.8 L12.0 145.6 L16.0 145.4 L20.0 145.3 L24.0 145.2 L28.0 145.2 L32.0 145.2 L36.0 145.2 L40.0 145.2 L44.0 145.3 L48.0 145.3 L52.0 145.4 L56.0 144.9 L60.0 144.5 L64.0 144 L68.0 143.5 L70.0 143.2 L71.2 129 L72.6 145.89999999999998 L75.0 144.7 L78.0 145.6 L82.0 145.6 L86.0 145.5 L90.0 145.4 L94.0 145.4 L98.0 145.3 L102.0 145.2 L106.0 145.1 L110.0 145 L114.0 144.9 L118.0 144.9 L122.0 144.8 L126.0 144.9 L130.0 144.9 L134.0 145 L138.0 145.1 L142.0 145.3 L146.0 145 L150.0 144.7 L154.0 144.4 L158.0 144.1 L160.0 144 L161.2 129 L162.6 146.7 L165.0 145.5 L168.0 147 L172.0 147.2 L176.0 147.5 L180.0 147.7 L184.0 147.8 L188.0 148 L192.0 148 L196.0 148.1 L200.0 148 L204.0 148 L208.0 147.8 L212.0 147.6 L216.0 146.9 L220.0 146.1 L224.0 145.3 L228.0 144.5 L230.0 144 L231.2 129 L232.6 146.7 L235.0 145.5 L238.0 145.8 L242.0 145.5 L246.0 145.3 L250.0 145.1 L254.0 144.9 L258.0 144.7 L262.0 144.6 L266.0 144.6 L270.0 144.6 L274.0 144.6 L278.0 144.7 L282.0 144.8 L286.0 145 L290.0 145.2 L294.0 145.3 L298.0 145.5"/></svg><span>Population</span></a>
    <h3><a href="/axobench/population/">Population contexts</a></h3>
    <p>Teacher responses to input histories recorded in 100 connected AxoSim networks, with five excitatory teachers and one inhibitory teacher. Use them to fine-tune and evaluate under recurrent input statistics.</p>
    <dl>
      <div><dt>Repository</dt><dd><a href="https://huggingface.co/datasets/Axym-Labs/axobench-population"><code>Axym-Labs/axobench-population</code></a></dd></div>
      <div><dt>Traces</dt><dd>50,000 × 1,200 ms<span class="data-bar" style="--share: 8%"><span>16.7 h simulated</span></span></dd></div>
      <div><dt>Inputs</dt><dd>Recorded in connected networks</dd></div>
      <div><dt>Download</dt><dd>1.59 GB<span class="data-bar" style="--share: 6%"></span></dd></div>
      <div><dt>Use it</dt><dd><a href="/axobench/population/#split-by-context">Split by network context →</a></dd></div>
    </dl>
  </section>
  <section class="model-card">
    <a class="model-art dataset-art interventions" href="/axobench/interventions/" aria-label="Explore Paired interventions"><svg viewBox="0 0 300 160" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path class="trace" d="M0.0 137.3 L3.0 137.3 L6.0 137.2 L9.0 137.2 L12.0 137.2 L15.0 137.1 L18.0 137.1 L21.0 137 L24.0 136.9 L27.0 136.8 L30.0 136.7 L33.0 135.8 L36.0 134.9 L39.0 134 L42.0 133.1 L45.0 132.2 L48.0 131.3 L49.2 90 L50.6 136.70000000000002 L53.0 134.3 L56.0 135.9 L59.0 135.8 L62.0 135.7 L65.0 135.6 L68.0 135.6 L71.0 135.5 L74.0 135.5 L77.0 135.4 L80.0 135.4 L83.0 135.4 L86.0 135.3 L89.0 134.5 L92.0 133.7 L95.0 132.9 L98.0 132.1 L101.0 131.3 L104.0 130.5 L105.2 90 L106.6 135.9 L109.0 133.5 L112.0 135.3 L115.0 135.3 L118.0 135.3 L121.0 135.3 L124.0 135.3 L127.0 135.3 L130.0 135.3 L133.0 135.4 L136.0 135.4 L139.0 135.4 L142.0 135.4 L145.0 135.5 L148.0 135.5 L151.0 135.6 L154.0 135.7 L157.0 135.7 L160.0 135.3 L163.0 134.6 L166.0 133.9 L169.0 133.2 L172.0 132.5 L175.0 131.8 L176.0 131.6 L177.2 90 L178.6 137 L181.0 134.6 L184.0 136.7 L187.0 136.8 L190.0 136.9 L193.0 137 L196.0 137.1 L199.0 137.2 L202.0 137.3 L205.0 137.4 L208.0 137.4 L211.0 137.5 L214.0 137.5 L217.0 137.5 L220.0 137.5 L223.0 136.6 L226.0 135.8 L229.0 134.9 L232.0 134 L235.0 133.1 L238.0 132.1 L239.2 90 L240.6 137.5 L243.0 135.1 L246.0 136.4 L249.0 136.2 L252.0 136 L255.0 135.8 L258.0 135.6 L261.0 135.4 L264.0 135.1 L267.0 134.9 L270.0 134.7 L273.0 134.5 L276.0 134.3 L279.0 134.2 L282.0 134 L285.0 133.9 L288.0 133.9 L291.0 133.8 L294.0 133.8 L297.0 133.8 L300.0 133.8"/><path class="trace edit" d="M0.0 137.3 L3.0 137.3 L6.0 137.2 L9.0 137.2 L12.0 137.2 L15.0 137.1 L18.0 137.1 L21.0 137 L24.0 136.9 L27.0 136.8 L30.0 136.7 L33.0 135.8 L36.0 134.9 L39.0 134 L42.0 133.1 L45.0 132.2 L48.0 131.3 L49.2 90 L50.6 136.70000000000002 L53.0 134.3 L56.0 135.9 L59.0 135.8 L62.0 135.7 L65.0 135.6 L68.0 135.6 L71.0 135.5 L74.0 135.5 L77.0 135.4 L80.0 135.4 L83.0 135.4 L86.0 135.3 L89.0 134.5 L92.0 133.7 L95.0 132.9 L98.0 132.1 L101.0 131.3 L104.0 130.5 L105.2 90 L106.6 135.9 L109.0 133.5 L112.0 135.3 L115.0 135.3 L118.0 135.3 L121.0 135.5 L124.0 136.3 L127.0 137.1 L130.0 137.8 L133.0 138.6 L136.0 139.4 L139.0 140.2 L142.0 140.4 L145.0 140.5 L148.0 140.5 L151.0 140.6 L154.0 140.7 L157.0 140.7 L160.0 140.8 L163.0 140.9 L166.0 141 L169.0 141.1 L172.0 141.2 L175.0 141.3 L178.0 141.4 L181.0 141.6 L184.0 141.7 L187.0 141.8 L190.0 141.9 L193.0 142 L196.0 142.1 L199.0 141.4 L202.0 140.7 L205.0 140 L208.0 139.2 L211.0 138.5 L214.0 137.7 L215.2 90 L216.6 143.1 L219.0 140.7 L222.0 142.5 L225.0 142.4 L228.0 142.3 L231.0 142.2 L234.0 142.1 L237.0 142 L240.0 141.8 L243.0 141.6 L246.0 141.4 L249.0 141.2 L252.0 141 L255.0 140.8 L258.0 140.6 L261.0 140.4 L264.0 140.1 L267.0 139.9 L270.0 139.7 L273.0 139.5 L276.0 139.3 L279.0 139.2 L282.0 139 L285.0 138.9 L288.0 138.9 L291.0 138.8 L294.0 138.8 L297.0 138.8 L300.0 138.8"/></svg><span>Interventions</span></a>
    <h3><a href="/axobench/interventions/">Paired interventions</a></h3>
    <p>Each input sample is simulated twice: unchanged and after one of five defined edits. Use the pairs to measure response fidelity and for mechanistic analysis.</p>
    <dl>
      <div><dt>Repository</dt><dd><a href="https://huggingface.co/datasets/Axym-Labs/axobench-interventions"><code>Axym-Labs/axobench-interventions</code></a></dd></div>
      <div><dt>Traces</dt><dd>12,500 pairs × 6,000 ms<span class="data-bar" style="--share: 20%"><span>41.7 h simulated</span></span></dd></div>
      <div><dt>Inputs</dt><dd>A baseline sample and its edit</dd></div>
      <div><dt>Download</dt><dd>5.86 GB<span class="data-bar" style="--share: 22%"></span></dd></div>
      <div><dt>Use it</dt><dd><a href="/axobench/interventions/#add-the-pairs-to-an-evaluation">Add pairs to an evaluation →</a></dd></div>
    </dl>
  </section>
</div>

<p class="figure-caption">Bars scale each release to the largest. Simulated time is the trace count times the trace length and counts both simulations of an intervention pair; download sizes are the compressed shards of all splits.</p>

AxoBench follows the packaging and target coordinate of [NeuronIO](/axobench/neuronio/), an earlier single-neuron corpus, which can be converted to the same shard format. These pages describe the current v1 releases.

## Match the dataset to the question

**Train a single-neuron model.** Fit on the single-neuron `train` split. Select the architecture, recipe, checkpoint, and spike threshold on `val`, and evaluate the final choice once on `test`. An unreleased confirmation set is held separately from the public splits.

**Compare a candidate with a baseline.** Use the [AxoBench evaluator](/axobench/benchmarking/) on `val`. It scores the [core metrics](/axobench/metrics/), calibrates the spike threshold on a separate part of the selected traces, and reports paired differences with bootstrap intervals.

**Measure the response to an input change.** Add the intervention pairs to the evaluation root. The evaluator then reports Response SERA, which compares the predicted change in voltage with the teacher's change.

**Prepare a model for recurrent deployment.** Fine-tune and evaluate on the population contexts, splitting by context. Trace metrics on these inputs do not establish recurrent validity; connected-population measurements remain necessary.

**Test transfer to an unseen morphology.** No split withholds a morphology: every split contains all five. Build leave-one-morphology-out partitions from the sample IDs as described in [morphologies](/axobench/morphologies/).

## Assemble an evaluation root

The evaluator reads `<root>/val` and, if present, every condition directory under `<root>/interventions`. Download only the validation split of the single-neuron release, then place the intervention release inside the same root:

```bash
python -m pip install -U huggingface_hub
hf download Axym-Labs/axobench --repo-type dataset \
  --include "val/*" \
  --local-dir data/axobench
hf download Axym-Labs/axobench-interventions --repo-type dataset \
  --local-dir data/axobench/interventions
```

The first command transfers 2.65 GB of validation shards and the second 5.86 GB of intervention files. The complete single-neuron release adds 21.2 GB for `train` and 2.65 GB for `test`; the population release is 1.59 GB. Download a split with `--include "train/*"` or `--include "test/*"` when you need it.

## Preserve the conventions

Single-neuron inputs use `(batch, time, input_channels)` and targets use `(batch, time, 2)`. AxoSim's population interface uses contact inputs shaped `(population, time, contacts)`, which are a different representation from the 1,278-channel dataset inputs. Preserve channel identity, event sign, sampling cadence, morphology identity, target coordinate conversion, and causal padding rules through preprocessing. The [data reference](/api/data/) documents AxoSim's sharded and windowed readers; the [conversion reference](/api/neuronio/) documents the voltage and spike conversion path.

Population contexts, ordinary traces, and intervention pairs represent different input distributions. Report which release and split you use, and retain the manifest and shard hashes with derived results.

## Next steps

Read the page for the selected dataset, then [benchmark a model](/axobench/benchmarking/). AxoSim users can continue with [training](/training/), [inference-time adaptation](/adaptation/), or [evaluation](/evaluation/).
