---
title: Population interfaces
description: Signatures, parameters, return contracts, and source for population interfaces.
section: API reference
apiGroup: Populations
order: 201
---

## Overview

The public differentiable population combines one Lite model with persistent neuron identities, morphology assignments, contact routes, and adaptation banks. AxoSimMamba aliases AxoMamba; AxoSimLite aliases AdaptiveSupportP4Surrogate; AxoSimGRU currently aliases CausalBlockForecastModel. Named GRU profiles are built by create_axosim_profile and return AxoTemporalModel.

Source revision: `306a51ed950b`. [Public export index](/api/).

<section class="api-symbol" id="interfaces-axosimpopulation">

## AxoSimPopulation

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation(neuron: AxoSimLite, *, morphology_indices: torch.Tensor, contact_branch_indices: torch.Tensor)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L24-L470)

</div>

Differentiable AxoSim-Lite population with distinct adaptation banks.

Bases: `nn.Module`.

neuron is a Lite model. morphology_indices is integer (N,); contact_branch_indices is integer (N,K), with values in [0, neuron.config.input_dim). The morphology indices must refer to declared morphology classes. Buffers are cloned and converted to long.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>neuron</code> <span class="api-type">AxoSimLite</span></dt>
<dd><span class="api-default">required.</span> Shared Lite neuron used by every persistent population member.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
<dt><code>contact_branch_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Integer tensor (population, contacts), mapping each contact to a Lite input channel.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="interfaces-axosimpopulation-population-size"><code>AxoSimPopulation.population_size: int</code></dt>
<dd>Number of persistent neurons. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L79-L80">Source</a></dd>
<dt id="interfaces-axosimpopulation-runtime-coefficients-per-neuron"><code>AxoSimPopulation.runtime_coefficients_per_neuron: int</code></dt>
<dd>Width of the direct behavior coefficients for one neuron. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L83-L84">Source</a></dd>
<dt id="interfaces-axosimpopulation-synaptic-efficacies-per-neuron"><code>AxoSimPopulation.synaptic_efficacies_per_neuron: int</code></dt>
<dd>Number of independently mutable incoming contacts per neuron. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L87-L88">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#interfaces-axosimpopulation-adaptation-parameters"><code>AxoSimPopulation.adaptation_parameters()</code></a></li>
<li><a href="#interfaces-axosimpopulation-trainable-adaptation-parameters"><code>AxoSimPopulation.trainable_adaptation_parameters()</code></a></li>
<li><a href="#interfaces-axosimpopulation-enable-adaptation-training"><code>AxoSimPopulation.enable_adaptation_training()</code></a></li>
<li><a href="#interfaces-axosimpopulation-enable-full-training"><code>AxoSimPopulation.enable_full_training()</code></a></li>
<li><a href="#interfaces-axosimpopulation-synaptic-efficacies"><code>AxoSimPopulation.synaptic_efficacies()</code></a></li>
<li><a href="#interfaces-axosimpopulation-forward"><code>AxoSimPopulation.forward()</code></a></li>
<li><a href="#interfaces-axosimpopulation-forward-sparse-contacts"><code>AxoSimPopulation.forward_sparse_contacts()</code></a></li>
<li><a href="#interfaces-axosimpopulation-forward-batch"><code>AxoSimPopulation.forward_batch()</code></a></li>
<li><a href="#interfaces-axosimpopulation-forward-tokens"><code>AxoSimPopulation.forward_tokens()</code></a></li>
<li><a href="#interfaces-axosimpopulation-forward-token-batch"><code>AxoSimPopulation.forward_token_batch()</code></a></li>
</ul>

<p class="api-label">Examples</p>

Run independent trials through one persistent population.

Download [population_example.py](/examples/population_example.py) into your working directory first; [build populations](/populations/) explains its construction.

```python
import torch
from population_example import build_population

population = build_population()
prediction = population.forward_batch(torch.zeros(2, 3, 12, 4))
print(prediction.shape)
```

```text
torch.Size([2, 3, 12, 2])
```

<section class="api-method" id="interfaces-axosimpopulation-adaptation-parameters">

### AxoSimPopulation.adaptation_parameters

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.adaptation_parameters() -> Iterator[nn.Parameter]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L90-L93)

</div>

Yields behavior_adapter, morphology_adapter, and synaptic_log_efficacy in that order.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">Iterator[nn.Parameter]</span></dt>
<dd>Iterator over the declared parameter group.</dd>
</dl>

</section>

<section class="api-method" id="interfaces-axosimpopulation-trainable-adaptation-parameters">

### AxoSimPopulation.trainable_adaptation_parameters

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.trainable_adaptation_parameters() -> Iterator[nn.Parameter]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L95-L100)

</div>

Yields only adaptation parameters whose requires_grad flag is true.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">Iterator[nn.Parameter]</span></dt>
<dd>Iterator over the declared parameter group.</dd>
</dl>

</section>

<section class="api-method" id="interfaces-axosimpopulation-enable-adaptation-training">

### AxoSimPopulation.enable_adaptation_training

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.enable_adaptation_training(*, behavior: bool=True, morphology: bool=True, synaptic: bool=True) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L102-L113)

</div>

Freezes shared Lite parameters, then independently enables or freezes behavior_adapter, morphology_adapter, and synaptic_log_efficacy. The defaults enable all three groups.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>behavior</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Enable gradients on per-neuron behavior rows.</dd>
<dt><code>morphology</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Enable gradients on morphology-shared adaptation rows.</dd>
<dt><code>synaptic</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Enable gradients on independently mutable contact log efficacies.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-method" id="interfaces-axosimpopulation-enable-full-training">

### AxoSimPopulation.enable_full_training

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.enable_full_training() -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L115-L117)

</div>

Enable gradients on shared neuron weights and all adaptation parameters.

Enables requires_grad on every module parameter, including shared neuron weights.

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

<section class="api-method" id="interfaces-axosimpopulation-synaptic-efficacies">

### AxoSimPopulation.synaptic_efficacies

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.synaptic_efficacies(synaptic_log_efficacy: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L119-L134)

</div>

Materialize positive contact multipliers from their log parameters.

Returns exp(log_efficacy) with shape (N,K). Signed contact event amplitudes carry excitation/inhibition; efficacy remains positive.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>synaptic_log_efficacy</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">default=None.</span> Optional (N,K) log-efficacy override.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>efficacies</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Positive multipliers exp(synaptic_log_efficacy), shaped (population, contacts).</dd>
</dl>

</section>

<section class="api-method" id="interfaces-axosimpopulation-forward">

### AxoSimPopulation.forward

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.forward(contact_inputs: torch.Tensor, *, synaptic_log_efficacy: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L198-L211)

</div>

Predict native spike and soma outputs for the supplied sequence.

contact_inputs is (N,T,K). Optional synaptic_log_efficacy is (N,K) and replaces the stored efficacy values for this call. Return shape is (N,T,2); hidden state starts fresh for the sequence.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>contact_inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Dense signed contact histories; shape defined above.</dd>
<dt><code>synaptic_log_efficacy</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional (N,K) log-efficacy override.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Spike-logit and soma-target channels in the tensor shape specified above.</dd>
</dl>

</section>

<section class="api-method" id="interfaces-axosimpopulation-forward-sparse-contacts">

### AxoSimPopulation.forward_sparse_contacts

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.forward_sparse_contacts(event_summary_indices: torch.Tensor, event_contact_indices: torch.Tensor, event_values: torch.Tensor, *, time_steps: int, synaptic_log_efficacy: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L213-L327)

</div>

Run exact sparse contact events with full temporal gradients.

The three event tensors are equal-length one-dimensional arrays. Summary indices address n*T+t; contact indices address n*K+k, and both must identify the same neuron. Integer indices and floating event values must share the module device. Return shape is (N,time_steps,2). Gradients propagate through amplitudes and selected efficacies.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>event_summary_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Flattened population-time addresses n*time_steps+t, in corresponding event order.</dd>
<dt><code>event_contact_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Flattened population-contact addresses n*contacts+k; paired addresses must name the same neuron.</dd>
<dt><code>event_values</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Signed floating-point event amplitudes, one per paired address.</dd>
<dt><code>time_steps</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Native sequence horizon.</dd>
<dt><code>synaptic_log_efficacy</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional (N,K) log-efficacy override.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Spike-logit and soma-target channels in the tensor shape specified above.</dd>
</dl>

</section>

<section class="api-method" id="interfaces-axosimpopulation-forward-batch">

### AxoSimPopulation.forward_batch

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.forward_batch(contact_inputs: torch.Tensor, *, synaptic_log_efficacy: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L329-L392)

</div>

Run independent examples through one persistent population.

contact_inputs is (B,N,T,K). Independent examples share population identities and adaptation banks. Return shape is (B,N,T,2).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>contact_inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Dense signed contact histories; shape defined above.</dd>
<dt><code>synaptic_log_efficacy</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional (N,K) log-efficacy override.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Spike-logit and soma-target channels in the tensor shape specified above.</dd>
</dl>

</section>

<section class="api-method" id="interfaces-axosimpopulation-forward-tokens">

### AxoSimPopulation.forward_tokens

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.forward_tokens(tokens: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L394-L418)

</div>

Run pre-encoded P4 tokens with full temporal gradients.

tokens is (N,blocks,token_dim), already encoded at P4 cadence. Return shape is (N,blocks*4,2). This path decodes supplied tokens directly rather than adding the dense-input path's initial padding.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>tokens</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Sequence of encoded P4 tokens.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Spike-logit and soma-target channels in the tensor shape specified above.</dd>
</dl>

</section>

<section class="api-method" id="interfaces-axosimpopulation-forward-token-batch">

### AxoSimPopulation.forward_token_batch

<div class="api-signature">

```python
axosim.interfaces.AxoSimPopulation.forward_token_batch(tokens: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/interfaces.py#L420-L470)

</div>

Run batched pre-encoded P4 tokens with full temporal gradients.

tokens is (B,N,blocks,token_dim). Return shape is (B,N,blocks*4,2).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>tokens</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Sequence of encoded P4 tokens.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Spike-logit and soma-target channels in the tensor shape specified above.</dd>
</dl>

</section>

</section>
