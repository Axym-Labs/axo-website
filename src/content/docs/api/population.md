---
title: Behavior banks and population runners
description: Signatures, parameters, return contracts, and source for behavior banks and population runners.
section: API reference
apiGroup: Populations
order: 211
---

## Overview

Behavior-bank quantization stores component scales and W4/W8 values separately from the shared model. Quantization is a deployment transformation, while training uses floating-point parameters. The low-level GRU population runners and deployment records expose the contracts used for direct runtime construction.

Source revision: `306a51ed950b`. [Public export index](/api/).

<section class="api-symbol" id="population-quantizedneuronbehaviorbank">

## QuantizedNeuronBehaviorBank

<div class="api-signature">

```python
axosim.population.QuantizedNeuronBehaviorBank(values: torch.Tensor, scales: torch.Tensor, bits: int, logical_parameters_per_neuron: int)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L20-L33)

</div>

Physical low-bit storage for a logical behavior-adaptation bank.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>values</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Physical quantized values, interpreted using the bank&#x27;s scale and layout metadata.</dd>
<dt><code>scales</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Floating-point reconstruction scales for the stored quantized values.</dd>
<dt><code>bits</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Quantization precision, restricted to the supported bit widths.</dd>
<dt><code>logical_parameters_per_neuron</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="population-quantizedneuronbehaviorbank-storage-bytes"><code>QuantizedNeuronBehaviorBank.storage_bytes: int</code></dt>
<dd>Physical bank storage, including quantized values and reconstruction scales. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L29-L33">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="population-mixedquantizedneuronbehaviorbank">

## MixedQuantizedNeuronBehaviorBank

<div class="api-signature">

```python
axosim.population.MixedQuantizedNeuronBehaviorBank(values: torch.Tensor, scales: torch.Tensor, byte_slices: dict[str, slice], component_bits: dict[str, int], logical_parameters_per_neuron: int)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L37-L51)

</div>

Component-wise W4/W8 storage for a logical adaptation bank.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>values</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Physical quantized values, interpreted using the bank&#x27;s scale and layout metadata.</dd>
<dt><code>scales</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Floating-point reconstruction scales for the stored quantized values.</dd>
<dt><code>byte_slices</code> <span class="api-type">dict[str, slice]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>component_bits</code> <span class="api-type">dict[str, int]</span></dt>
<dd><span class="api-default">required.</span> Mapping from adaptation component names to supported W4/W8 storage widths.</dd>
<dt><code>logical_parameters_per_neuron</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="population-mixedquantizedneuronbehaviorbank-storage-bytes"><code>MixedQuantizedNeuronBehaviorBank.storage_bytes: int</code></dt>
<dd>Physical bank storage, including quantized values and reconstruction scales. <a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L47-L51">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="population-quantize-neuron-behavior-parameters">

## quantize_neuron_behavior_parameters

<div class="api-signature">

```python
axosim.population.quantize_neuron_behavior_parameters(parameters: torch.Tensor, *, adaptation: NeuronBehaviorAdaptation, bits: int) -> QuantizedNeuronBehaviorBank
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L54-L108)

</div>

Quantize each adaptation component with one symmetric scale.

parameters is floating-point (N,adaptation.parameter_count). bits is 4 or 8. W4 requires even logical width and packs two values per byte. Returns physical values and one scale per adaptation component.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>parameters</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Floating-point adaptation rows before quantization.</dd>
<dt><code>adaptation</code> <span class="api-type">NeuronBehaviorAdaptation</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Descriptor defining named behavior components and their logical shapes.</dd>
<dt><code>bits</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Quantization precision, restricted to the supported bit widths.</dd>
</dl>

<p class="api-label">Returns</p>

`QuantizedNeuronBehaviorBank`

</section>

<section class="api-symbol" id="population-quantize-mixed-neuron-behavior-parameters">

## quantize_mixed_neuron_behavior_parameters

<div class="api-signature">

```python
axosim.population.quantize_mixed_neuron_behavior_parameters(parameters: torch.Tensor, *, adaptation: NeuronBehaviorAdaptation, component_bits: dict[str, int]) -> MixedQuantizedNeuronBehaviorBank
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L111-L183)

</div>

Quantize each adaptation component to its declared W4/W8 tier.

parameters is floating-point (N,adaptation.parameter_count). component_bits declares W4/W8 for each named adaptation component. Returns packed byte slices and scale metadata needed for reconstruction.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>parameters</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Floating-point adaptation rows before quantization.</dd>
<dt><code>adaptation</code> <span class="api-type">NeuronBehaviorAdaptation</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Descriptor defining named behavior components and their logical shapes.</dd>
<dt><code>component_bits</code> <span class="api-type">dict[str, int]</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Mapping from adaptation component names to supported W4/W8 storage widths.</dd>
</dl>

<p class="api-label">Returns</p>

`MixedQuantizedNeuronBehaviorBank`

</section>

<section class="api-symbol" id="population-dequantize-neuron-behavior-parameters">

## dequantize_neuron_behavior_parameters

<div class="api-signature">

```python
axosim.population.dequantize_neuron_behavior_parameters(bank: QuantizedNeuronBehaviorBank, *, adaptation: NeuronBehaviorAdaptation) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L186-L215)

</div>

Materialize a low-bit behavior bank for validation or export.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>bank</code> <span class="api-type">QuantizedNeuronBehaviorBank</span></dt>
<dd><span class="api-default">required.</span> Quantized bank including its scale and layout metadata.</dd>
<dt><code>adaptation</code> <span class="api-type">NeuronBehaviorAdaptation</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Descriptor defining named behavior components and their logical shapes.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>parameters</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Floating-point behavior rows (population,adaptation.parameter_count), reconstructed component by component.</dd>
</dl>

</section>

<section class="api-symbol" id="population-dequantize-mixed-neuron-behavior-parameters">

## dequantize_mixed_neuron_behavior_parameters

<div class="api-signature">

```python
axosim.population.dequantize_mixed_neuron_behavior_parameters(bank: MixedQuantizedNeuronBehaviorBank, *, adaptation: NeuronBehaviorAdaptation) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L218-L251)

</div>

Materialize a component-wise W4/W8 adaptation bank.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>bank</code> <span class="api-type">MixedQuantizedNeuronBehaviorBank</span></dt>
<dd><span class="api-default">required.</span> Quantized bank including its scale and layout metadata.</dd>
<dt><code>adaptation</code> <span class="api-type">NeuronBehaviorAdaptation</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Descriptor defining named behavior components and their logical shapes.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>parameters</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Floating-point behavior rows (population,adaptation.parameter_count), reconstructed from each component&#x27;s W4/W8 slice.</dd>
</dl>

</section>

<section class="api-symbol" id="population-pack-neuron-behavior-adapter">

## pack_neuron_behavior_adapter

<div class="api-signature">

```python
axosim.population.pack_neuron_behavior_adapter(adapter: NeuronBehaviorAdapter, *, adaptation: NeuronBehaviorAdaptation) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L341-L393)

</div>

Pack a trained behavior adapter into the population ABI.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>adapter</code> <span class="api-type">NeuronBehaviorAdapter</span></dt>
<dd><span class="api-default">required.</span> Behavior adapter whose named components define the population bank.</dd>
<dt><code>adaptation</code> <span class="api-type">NeuronBehaviorAdaptation</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Descriptor defining named behavior components and their logical shapes.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-symbol" id="population-grupopulationrunner">

## GRUPopulationRunner

<div class="api-signature">

```python
axosim.population.GRUPopulationRunner(model: AxoTemporalModel, *, population: int, chunk_size: int, compile_step: bool=True, compile_mode: str='reduce-overhead', population_embedding_adapters: torch.Tensor | None=None)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1344-L1556)

</div>

Compiled persistent-state inference for a shared-weight GRU population.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">AxoTemporalModel</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
<dt><code>population</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Number of neurons represented by the population runner or record.</dd>
<dt><code>chunk_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Chunk length for the supported Mamba or streaming execution path.</dd>
<dt><code>compile_step</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Compile the population step implementation.</dd>
<dt><code>compile_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;reduce-overhead&#x27;.</span> Mode passed to torch.compile for the selected step.</dd>
<dt><code>population_embedding_adapters</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Population-group embedding corrections for the backbone.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="population-grupopulationrunner-recurrent-state"><code>GRUPopulationRunner.recurrent_state: torch.Tensor</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1444-L1447">Source</a></dd>
<dt id="population-grupopulationrunner-patch-sum"><code>GRUPopulationRunner.patch_sum: torch.Tensor | None</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1450-L1451">Source</a></dd>
<dt id="population-grupopulationrunner-patch-correction"><code>GRUPopulationRunner.patch_correction: torch.Tensor | None</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1454-L1455">Source</a></dd>
<dt id="population-grupopulationrunner-patch-position"><code>GRUPopulationRunner.patch_position: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1458-L1459">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#population-grupopulationrunner-step"><code>GRUPopulationRunner.step()</code></a></li>
</ul>

<section class="api-method" id="population-grupopulationrunner-step">

### GRUPopulationRunner.step

<div class="api-signature">

```python
axosim.population.GRUPopulationRunner.step(event_indices: torch.Tensor, event_values: torch.Tensor, morphology_indices: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1461-L1526)

</div>

Advance the population runner by one declared simulation step.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>event_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>event_values</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Signed floating-point event amplitudes, one per paired address.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="population-grubranchpopulationrunner">

## GRUBranchPopulationRunner

<div class="api-signature">

```python
axosim.population.GRUBranchPopulationRunner(model: AxoTemporalModel, *, population: int, chunk_size: int, compile_step: bool=True, compile_mode: str='reduce-overhead', population_embedding_adapters: torch.Tensor | None=None)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1559-L1701)

</div>

Compiled GRU inference from pre-aggregated raw branch inputs.

Bases: `GRUPopulationRunner`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">AxoTemporalModel</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
<dt><code>population</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Number of neurons represented by the population runner or record.</dd>
<dt><code>chunk_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Chunk length for the supported Mamba or streaming execution path.</dd>
<dt><code>compile_step</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Compile the population step implementation.</dd>
<dt><code>compile_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;reduce-overhead&#x27;.</span> Mode passed to torch.compile for the selected step.</dd>
<dt><code>population_embedding_adapters</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Population-group embedding corrections for the backbone.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#population-grubranchpopulationrunner-step"><code>GRUBranchPopulationRunner.step()</code></a></li>
</ul>

<section class="api-method" id="population-grubranchpopulationrunner-step">

### GRUBranchPopulationRunner.step

<div class="api-signature">

```python
axosim.population.GRUBranchPopulationRunner.step(branch_inputs: torch.Tensor, morphology_indices: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1619-L1701)

</div>

Advance the population runner by one declared simulation step.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>branch_inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Current population branch-feature tensor.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="population-adaptedgrubranchpopulationrunner">

## AdaptedGRUBranchPopulationRunner

<div class="api-signature">

```python
axosim.population.AdaptedGRUBranchPopulationRunner(model: AxoTemporalModel, *, population: int, chunk_size: int, behavior_parameters: torch.Tensor | QuantizedNeuronBehaviorBank | MixedQuantizedNeuronBehaviorBank, adaptation: NeuronBehaviorAdaptation, compile_step: bool=True, compile_mode: str='max-autotune-no-cudagraphs')
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1704-L1995)

</div>

Packed per-neuron behavior adaptation around one shared GRU base.

Bases: `GRUBranchPopulationRunner`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">AxoTemporalModel</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
<dt><code>population</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Number of neurons represented by the population runner or record.</dd>
<dt><code>chunk_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Chunk length for the supported Mamba or streaming execution path.</dd>
<dt><code>behavior_parameters</code> <span class="api-type">torch.Tensor | QuantizedNeuronBehaviorBank | MixedQuantizedNeuronBehaviorBank</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Logical behavior coefficients to compile into the model&#x27;s deployed coefficient width.</dd>
<dt><code>adaptation</code> <span class="api-type">NeuronBehaviorAdaptation</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Descriptor defining named behavior components and their logical shapes.</dd>
<dt><code>compile_step</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Compile the population step implementation.</dd>
<dt><code>compile_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;max-autotune-no-cudagraphs&#x27;.</span> Mode passed to torch.compile for the selected step.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#population-adaptedgrubranchpopulationrunner-step"><code>AdaptedGRUBranchPopulationRunner.step()</code></a></li>
</ul>

<section class="api-method" id="population-adaptedgrubranchpopulationrunner-step">

### AdaptedGRUBranchPopulationRunner.step

<div class="api-signature">

```python
axosim.population.AdaptedGRUBranchPopulationRunner.step(branch_inputs: torch.Tensor, morphology_indices: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1920-L1995)

</div>

Advance the population runner by one declared simulation step.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>branch_inputs</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Current population branch-feature tensor.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="population-groupedgrupopulationrunner">

## GroupedGRUPopulationRunner

<div class="api-signature">

```python
axosim.population.GroupedGRUPopulationRunner(model: AxoTemporalModel, *, population: int, groups: int, chunk_size: int, compile_step: bool=True, compile_mode: str='reduce-overhead')
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L1998-L2270)

</div>

Compiled GRU inference with one recurrent parameter set per group.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">AxoTemporalModel</span></dt>
<dd><span class="api-default">required.</span> Model to execute, optimize, count, or serialize for this operation.</dd>
<dt><code>population</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Number of neurons represented by the population runner or record.</dd>
<dt><code>groups</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Population parameter-group count.</dd>
<dt><code>chunk_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">keyword-only, required.</span> Chunk length for the supported Mamba or streaming execution path.</dd>
<dt><code>compile_step</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Compile the population step implementation.</dd>
<dt><code>compile_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">keyword-only, default=&#x27;reduce-overhead&#x27;.</span> Mode passed to torch.compile for the selected step.</dd>
</dl>

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="population-groupedgrupopulationrunner-resident-parameter-count"><code>GroupedGRUPopulationRunner.resident_parameter_count: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L2112-L2116">Source</a></dd>
<dt id="population-groupedgrupopulationrunner-patch-position"><code>GroupedGRUPopulationRunner.patch_position: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L2119-L2120">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#population-groupedgrupopulationrunner-step"><code>GroupedGRUPopulationRunner.step()</code></a></li>
<li><a href="#population-groupedgrupopulationrunner-load-group-recurrent-parameters"><code>GroupedGRUPopulationRunner.load_group_recurrent_parameters()</code></a></li>
</ul>

<section class="api-method" id="population-groupedgrupopulationrunner-step">

### GroupedGRUPopulationRunner.step

<div class="api-signature">

```python
axosim.population.GroupedGRUPopulationRunner.step(event_indices: torch.Tensor, event_values: torch.Tensor, morphology_indices: torch.Tensor) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L2122-L2191)

</div>

Advance the population runner by one declared simulation step.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>event_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>event_values</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Signed floating-point event amplitudes, one per paired address.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

<section class="api-method" id="population-groupedgrupopulationrunner-load-group-recurrent-parameters">

### GroupedGRUPopulationRunner.load_group_recurrent_parameters

<div class="api-signature">

```python
axosim.population.GroupedGRUPopulationRunner.load_group_recurrent_parameters(group: int, source: AxoTemporalModel) -> None
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/population.py#L2193-L2229)

</div>

Load one group's recurrent weights from a compatible GRU model.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>group</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Index of the population parameter group to load.</dd>
<dt><code>source</code> <span class="api-type">AxoTemporalModel</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>result</code> <span class="api-type">None</span></dt>
<dd>No return value.</dd>
</dl>

</section>

</section>

<section class="api-symbol" id="deployment-neuronbehavioradaptation">

## NeuronBehaviorAdaptation

<div class="api-signature">

```python
axosim.deployment.NeuronBehaviorAdaptation(width: int, branches: int, outputs: int, matrix_rank: int, adapt_recurrent: bool, branch_token_offset: bool = False)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L7-L135)

</div>

Mechanism-level parameters that remain unique to each neuron.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>width</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Feature width of the behavior adapter or population recurrence.</dd>
<dt><code>branches</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Number of routed branch features in the adapter.</dd>
<dt><code>outputs</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Number of readout channels.</dd>
<dt><code>matrix_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>adapt_recurrent</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>branch_token_offset</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span> Include adaptation offsets for encoded branch tokens.</dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="deployment-neuronbehavioradaptation-tensor-shapes"><code>NeuronBehaviorAdaptation.tensor_shapes: dict[str, tuple[int, ...]]</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L18-L77">Source</a></dd>
<dt id="deployment-neuronbehavioradaptation-tensor-slices"><code>NeuronBehaviorAdaptation.tensor_slices: dict[str, slice]</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L80-L89">Source</a></dd>
<dt id="deployment-neuronbehavioradaptation-parameter-counts"><code>NeuronBehaviorAdaptation.parameter_counts: dict[str, int]</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L92-L116">Source</a></dd>
<dt id="deployment-neuronbehavioradaptation-parameter-count"><code>NeuronBehaviorAdaptation.parameter_count: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L119-L120">Source</a></dd>
<dt id="deployment-neuronbehavioradaptation-adapted-components"><code>NeuronBehaviorAdaptation.adapted_components: frozenset[str]</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L123-L124">Source</a></dd>
<dt id="deployment-neuronbehavioradaptation-shared-components"><code>NeuronBehaviorAdaptation.shared_components: frozenset[str]</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L127-L135">Source</a></dd>
</dl>

</section>

<section class="api-symbol" id="deployment-populationdeploymentmeasurement">

## PopulationDeploymentMeasurement

<div class="api-signature">

```python
axosim.deployment.PopulationDeploymentMeasurement(population: int, adapted_parameters_per_neuron: int, adapted_components: tuple[str, ...], shared_components: tuple[str, ...], unique_adaptation_per_neuron: bool, adaptation_quality_validated: bool, shared_frozen_base: bool, output_materialized: bool, routing_feeds_model: bool, model_latency_ms: float, routing_latency_ms: float | None, complete_stack_latency_ms: float | None, model_peak_bytes: int, routing_peak_bytes: int | None, complete_stack_peak_bytes: int | None, local_source_identity_retained: bool = False, long_range_source_identity_retained: bool = False, morphology_assignment_independent: bool = False, activity_generation_mode: str = 'unknown', activity_dynamics_validated: bool = False, adaptation_execution_mode: str = 'direct', adaptation_reference_envelope_validated: bool = False, forecast_block_size: int = 1, complete_block_latency_ms: float | None = None)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L139-L165)

</div>

One complete population-simulation measurement.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>population</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Number of neurons represented by the population runner or record.</dd>
<dt><code>adapted_parameters_per_neuron</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>adapted_components</code> <span class="api-type">tuple[str, ...]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>shared_components</code> <span class="api-type">tuple[str, ...]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>unique_adaptation_per_neuron</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>adaptation_quality_validated</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>shared_frozen_base</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>output_materialized</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>routing_feeds_model</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>model_latency_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>routing_latency_ms</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>complete_stack_latency_ms</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>model_peak_bytes</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>routing_peak_bytes</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>complete_stack_peak_bytes</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>local_source_identity_retained</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>long_range_source_identity_retained</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>morphology_assignment_independent</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>activity_generation_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;unknown&#x27;.</span></dd>
<dt><code>activity_dynamics_validated</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>adaptation_execution_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;direct&#x27;.</span></dd>
<dt><code>adaptation_reference_envelope_validated</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>forecast_block_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1.</span></dd>
<dt><code>complete_block_latency_ms</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="deployment-populationdeploymenttarget">

## PopulationDeploymentTarget

<div class="api-signature">

```python
axosim.deployment.PopulationDeploymentTarget(headline_population: int, benchmark_population: int, biological_step_ms: float, adaptation: NeuronBehaviorAdaptation, shared_frozen_base: bool, output_materialization_required: bool, network_routing_required: bool, local_source_identity_required: bool, long_range_source_identity_required: bool, independent_morphology_assignment_required: bool, activity_dynamics_validation_required: bool, quota_activity_allowed: bool, forecast_block_size: int, firing_rate: float, fanout: int)
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L169-L376)

</div>

Requirements for a defensible real-time population claim.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>headline_population</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>benchmark_population</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>biological_step_ms</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>adaptation</code> <span class="api-type">NeuronBehaviorAdaptation</span></dt>
<dd><span class="api-default">required.</span> Descriptor defining named behavior components and their logical shapes.</dd>
<dt><code>shared_frozen_base</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>output_materialization_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>network_routing_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>local_source_identity_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>long_range_source_identity_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>independent_morphology_assignment_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>activity_dynamics_validation_required</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>quota_activity_allowed</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>forecast_block_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>firing_rate</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>fanout</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

<p class="api-label">Read-only attributes</p>

<dl class="api-attributes">
<dt id="deployment-populationdeploymenttarget-adapted-parameters-per-neuron"><code>PopulationDeploymentTarget.adapted_parameters_per_neuron: int</code></dt>
<dd><a href="https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L189-L190">Source</a></dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#deployment-populationdeploymenttarget-validation-errors"><code>PopulationDeploymentTarget.validation_errors()</code></a></li>
<li><a href="#deployment-populationdeploymenttarget-evaluate"><code>PopulationDeploymentTarget.evaluate()</code></a></li>
</ul>

<section class="api-method" id="deployment-populationdeploymenttarget-validation-errors">

### PopulationDeploymentTarget.validation_errors

<div class="api-signature">

```python
axosim.deployment.PopulationDeploymentTarget.validation_errors(measurement: PopulationDeploymentMeasurement) -> tuple[str, ...]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L192-L340)

</div>

Return violated deployment requirements for the supplied measurement.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>measurement</code> <span class="api-type">PopulationDeploymentMeasurement</span></dt>
<dd><span class="api-default">required.</span> Measured deployment record to compare with the target requirements.</dd>
</dl>

<p class="api-label">Returns</p>

`tuple[str, ...]`

</section>

<section class="api-method" id="deployment-populationdeploymenttarget-evaluate">

### PopulationDeploymentTarget.evaluate

<div class="api-signature">

```python
axosim.deployment.PopulationDeploymentTarget.evaluate(measurement: PopulationDeploymentMeasurement) -> dict[str, int | float | bool]
```

[Source](https://github.com/Axym-Labs/axosim/blob/306a51ed950b411e8858af622d48062b28e4fbfe/src/axosim/deployment.py#L342-L376)

</div>

Compare a deployment measurement with the declared target requirements.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>measurement</code> <span class="api-type">PopulationDeploymentMeasurement</span></dt>
<dd><span class="api-default">required.</span> Measured deployment record to compare with the target requirements.</dd>
</dl>

<p class="api-label">Returns</p>

`dict[str, int \| float \| bool]`

</section>

</section>
