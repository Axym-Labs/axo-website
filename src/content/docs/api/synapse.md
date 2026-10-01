---
title: Synaptic efficacy banks
description: Signatures, parameters, return contracts, and source for synaptic efficacy banks.
section: API reference
apiGroup: Populations
order: 213
---

## Overview

An efficacy bank contains one positive multiplier for each retained incoming E/I contact slot. The retained width is 2*ceil(channels_per_role/recurrent_stride). W8 storage quantizes deviation around a positive baseline with one shared scale; dequantization reconstructs floating-point multipliers.

Source revision: `856207f6de56`. [Public export index](/api/).

<section class="api-symbol" id="synapse-quantizedsynapticefficacybank">

## QuantizedSynapticEfficacyBank

<div class="api-signature">

```python
axosim.synapse.QuantizedSynapticEfficacyBank(values: torch.Tensor, scale: torch.Tensor, channels_per_role: int, recurrent_stride: int, baseline: float = 1.0)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/synapse.py#L11-L33)

</div>

One W8 multiplicative efficacy for every retained incoming contact.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>values</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Physical quantized values, interpreted using the bank&#x27;s scale and layout metadata.</dd>
<dt><code>scale</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Multiplicative normalization or reconstruction scale.</dd>
<dt><code>channels_per_role</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Available contact-channel slots for each E/I role.</dd>
<dt><code>recurrent_stride</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Stride selecting retained contact slots.</dd>
<dt><code>baseline</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=1.0.</span> Positive shared reference efficacy for deviation quantization.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="synapse-quantizedsynapticefficacybank-population-size"><code>QuantizedSynapticEfficacyBank.population_size: int</code></dt>
<dd>Number of persistent neurons. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/synapse.py#L21-L22">Source</a></dd>
<dt id="synapse-quantizedsynapticefficacybank-values-per-neuron"><code>QuantizedSynapticEfficacyBank.values_per_neuron: int</code></dt>
<dd>Logical retained-contact multiplier count per neuron. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/synapse.py#L25-L26">Source</a></dd>
<dt id="synapse-quantizedsynapticefficacybank-storage-bytes"><code>QuantizedSynapticEfficacyBank.storage_bytes: int</code></dt>
<dd>Physical bank storage, including quantized values and reconstruction scales. <a href="https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/synapse.py#L29-L33">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="synapse-retained-synaptic-efficacies-per-neuron">

## retained_synaptic_efficacies_per_neuron

<div class="api-signature">

```python
axosim.synapse.retained_synaptic_efficacies_per_neuron(*, channels_per_role: int, recurrent_stride: int) -> int
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/synapse.py#L36-L50)

</div>

Return compact E/I contact slots for the declared routed topology.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>channels_per_role</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Available contact-channel slots for each E/I role.</dd>
<dt><code>recurrent_stride</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Stride selecting retained contact slots.</dd>
</dl>

<p class="api-label">Returns</p>

`int`

</section>

<section class="api-symbol" id="synapse-quantize-synaptic-efficacies">

## quantize_synaptic_efficacies

<div class="api-signature">

```python
axosim.synapse.quantize_synaptic_efficacies(efficacies: torch.Tensor, *, channels_per_role: int, recurrent_stride: int, baseline: float=1.0) -> QuantizedSynapticEfficacyBank
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/synapse.py#L53-L97)

</div>

Quantize positive per-contact multipliers around a shared baseline.

efficacies is floating-point (N,2*ceil(channels_per_role/recurrent_stride)) with all values positive. Returns a W8 bank containing int8 values, one colocated floating scale, topology metadata, and positive baseline.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>efficacies</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Positive floating-point contact multipliers, shaped by the retained topology.</dd>
<dt><code>channels_per_role</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Available contact-channel slots for each E/I role.</dd>
<dt><code>recurrent_stride</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Stride selecting retained contact slots.</dd>
<dt><code>baseline</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">keyword-only, default=1.0.</span> Positive shared reference efficacy for deviation quantization.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>bank</code> <span class="api-type">QuantizedSynapticEfficacyBank</span></dt>
<dd>W8 values, one shared scale, positive baseline, and retained topology metadata.</dd>
</dl>

<p class="api-label">Examples</p>

Quantize a unit-efficacy bank with four retained slots per E/I role.

```python
import torch
from axosim.synapse import quantize_synaptic_efficacies

bank = quantize_synaptic_efficacies(
    torch.ones(2, 8), channels_per_role=4, recurrent_stride=1
)
print(bank.values.shape, bank.values.dtype)
```

```text
torch.Size([2, 8]) torch.int8
```

</section>

<section class="api-symbol" id="synapse-dequantize-synaptic-efficacies">

## dequantize_synaptic_efficacies

<div class="api-signature">

```python
axosim.synapse.dequantize_synaptic_efficacies(bank: QuantizedSynapticEfficacyBank) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/synapse.py#L100-L109)

</div>

Materialize a W8 efficacy bank for training checks or export.

Returns floating-point (N,K) values reconstructed as bank.values*bank.scale+bank.baseline. Validates the bank's layout and scale device.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>bank</code> <span class="api-type">QuantizedSynapticEfficacyBank</span></dt>
<dd><span class="api-default">required.</span> Quantized bank including its scale and layout metadata.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>efficacies</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Reconstructed floating-point contact multipliers with shape (population, retained_contacts).</dd>
</dl>

</section>
