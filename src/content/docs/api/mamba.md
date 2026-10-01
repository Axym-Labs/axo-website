---
title: Mamba models and configuration
description: Signatures, parameters, return contracts, and source for mamba models and configuration.
section: API reference
apiGroup: Models
order: 204
---

## Overview

AxoMamba is the public Mamba implementation and inherits BranchOfficialMamba. AxoMambaConfig inherits all BranchOfficialMambaConfig fields. The default_axomamba_config factory supplies the promoted recipe, which differs from the dataclass's raw field defaults. AxoPyTorchMamba is a test-oriented fallback with a different checkpoint format.

Source revision: `856207f6de56`. [Public export index](/api/).

<section class="api-symbol" id="axomamba-axomambaconfig">

## AxoMambaConfig

<div class="api-signature">

```python
axosim.axomamba.AxoMambaConfig(num_input: int = 1278, num_output: int = 2, num_branch: int = 45, num_synapse_per_branch: int = 100, input_to_synapse_routing: str | None = 'neuronio_routing', model_dim: int = 64, num_layers: int = 2, block_repeats: int = 1, state_dim: int = 16, conv_kernel: int = 4, expansion: int = 2, block_type: str = 'mamba1', head_dim: int = 64, num_groups: int = 1, chunk_size: int = 256, block_norm: bool = True, final_norm: bool = True, dropout: float = 0.0, residual_scale_init: float = 0.1, mamba_update_normalization: str = 'none', separate_heads: bool = False, soma_filter: bool = False, soma_filter_tau: float = 25.0, soma_filter_kernel: int = 129, learn_soma_filter_decay: bool = True, soma_multiplicative_gate: bool = False, soma_multiplicative_scale_init: float = 0.1, soma_peak_correction: bool = False, soma_peak_correction_scale_init: float = 0.1, soma_highpass_correction: bool = False, soma_highpass_correction_scale_init: float = 0.1, spike_voltage_coupling_scale: float = 0.0, morphology_ids: list[str] | None = None, morphology_embedding_scale: float | None = None, population_adapter_morphology_id: str | None = None, synapse_gain_scale: float | None = None, morphology_synapse_gain_scale: float | None = None, share_morphology_synapse_gain: bool = False, morphology_synapse_gain_rank: int = 0, morphology_synapse_feature_dim: int = 0, morphology_synapse_feature_hidden: int = 0, morphology_synapse_feature_scale: float | None = None, morphology_synapse_feature_storage_dtype: str = 'float32', local_tcn_scale: float | None = None, local_tcn_mode: str = 'dilated', local_tcn_position: str = 'parallel', share_local_tcn_pointwise: bool = False, local_tcn_pointwise_adapter_rank: int = 0, local_tcn_pointwise_rank: int = 0, local_tcn_output_rank: int = 0, mamba_projection_rank: int = 0, branch_gain: bool = False, branch_nonlinearity: str = 'none', branch_nonlinearity_scale_init: float = 0.1, branch_subunits: int = 0, branch_subunit_routing: str = 'contiguous', branch_subunit_scale: float = 1.0, branch_bilinear_rank: int = 0, branch_bilinear_scale: float | None = None, branch_trace_taus: list[float] | None = None, branch_trace_kernel: int = 65, hidden_trace_taus: list[float] | None = None, hidden_trace_kernel: int = 129, temporal_refine_kernel: int = 0, integrative_mixer: bool = False, integrative_mixer_short_kernel: int = 9, integrative_mixer_long_kernel: int = 65, integrative_mixer_position: str = 'pre', integrative_mixer_long_path_bias: float = 0.5)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L20-L21)

</div>

Named config for the current best compact AxoSim Mamba surrogate.

Bases: `BranchOfficialMambaConfig`.

Inherits all fields and raw defaults from `BranchOfficialMambaConfig`. `default_axomamba_config` applies the AxoSim recipe over those raw defaults.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>num_input</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1278.</span> Input-channel count.</dd>
<dt><code>num_output</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=2.</span> Output-channel count.</dd>
<dt><code>num_branch</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=45.</span> Branched input-feature count.</dd>
<dt><code>num_synapse_per_branch</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=100.</span> Contact slots per branch.</dd>
<dt><code>input_to_synapse_routing</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">default=&#x27;neuronio_routing&#x27;.</span></dd>
<dt><code>model_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=64.</span> Temporal hidden-feature width.</dd>
<dt><code>num_layers</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=2.</span> Number of temporal layers.</dd>
<dt><code>block_repeats</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1.</span></dd>
<dt><code>state_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=16.</span> Temporal state width.</dd>
<dt><code>conv_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=4.</span></dd>
<dt><code>expansion</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=2.</span></dd>
<dt><code>block_type</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;mamba1&#x27;.</span></dd>
<dt><code>head_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=64.</span> Configured head width of the backbone.</dd>
<dt><code>num_groups</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1.</span></dd>
<dt><code>chunk_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=256.</span> Chunk length for the supported Mamba or streaming execution path.</dd>
<dt><code>block_norm</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>final_norm</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>dropout</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.0.</span></dd>
<dt><code>residual_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span> Initial learned multiplier on the residual update.</dd>
<dt><code>mamba_update_normalization</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;none&#x27;.</span> Normalize residual updates when the supported fixed_rms mode is selected.</dd>
<dt><code>separate_heads</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_filter</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_filter_tau</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=25.0.</span></dd>
<dt><code>soma_filter_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=129.</span></dd>
<dt><code>learn_soma_filter_decay</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>soma_multiplicative_gate</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_multiplicative_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span></dd>
<dt><code>soma_peak_correction</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_peak_correction_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span></dd>
<dt><code>soma_highpass_correction</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_highpass_correction_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span></dd>
<dt><code>spike_voltage_coupling_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.0.</span></dd>
<dt><code>morphology_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">default=None.</span> Ordered morphology identity vocabulary.</dd>
<dt><code>morphology_embedding_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>population_adapter_morphology_id</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>synapse_gain_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>morphology_synapse_gain_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>share_morphology_synapse_gain</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>morphology_synapse_gain_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>morphology_synapse_feature_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>morphology_synapse_feature_hidden</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>morphology_synapse_feature_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>morphology_synapse_feature_storage_dtype</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;float32&#x27;.</span></dd>
<dt><code>local_tcn_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>local_tcn_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;dilated&#x27;.</span></dd>
<dt><code>local_tcn_position</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;parallel&#x27;.</span></dd>
<dt><code>share_local_tcn_pointwise</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>local_tcn_pointwise_adapter_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>local_tcn_pointwise_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>local_tcn_output_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>mamba_projection_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>branch_gain</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>branch_nonlinearity</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;none&#x27;.</span></dd>
<dt><code>branch_nonlinearity_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span></dd>
<dt><code>branch_subunits</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>branch_subunit_routing</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;contiguous&#x27;.</span></dd>
<dt><code>branch_subunit_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=1.0.</span></dd>
<dt><code>branch_bilinear_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>branch_bilinear_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>branch_trace_taus</code> <span class="api-type">list[float] | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>branch_trace_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=65.</span></dd>
<dt><code>hidden_trace_taus</code> <span class="api-type">list[float] | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>hidden_trace_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=129.</span></dd>
<dt><code>temporal_refine_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>integrative_mixer</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>integrative_mixer_short_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=9.</span></dd>
<dt><code>integrative_mixer_long_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=65.</span></dd>
<dt><code>integrative_mixer_position</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;pre&#x27;.</span></dd>
<dt><code>integrative_mixer_long_path_bias</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.5.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="axomamba-default-axomamba-config">

## default_axomamba_config

<div class="api-signature">

```python
axosim.axomamba.default_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L24-L83)

</div>

Build the default AxoSim Mamba recipe and apply keyword overrides.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>overrides</code> <span class="api-type">Any</span></dt>
<dd><span class="api-default">variadic.</span> Keyword fields that replace values in the selected architecture recipe.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig</span></dt>
<dd>Architecture recipe with the supplied keyword overrides applied.</dd>
</dl>

</section>

<section class="api-symbol" id="axomamba-structured-compact-axomamba-config">

## structured_compact_axomamba_config

<div class="api-signature">

```python
axosim.axomamba.structured_compact_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L86-L96)

</div>

Build the structured compact recipe and apply keyword overrides.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>overrides</code> <span class="api-type">Any</span></dt>
<dd><span class="api-default">variadic.</span> Keyword fields that replace values in the selected architecture recipe.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig</span></dt>
<dd>Architecture recipe with the supplied keyword overrides applied.</dd>
</dl>

</section>

<section class="api-symbol" id="axomamba-regression-axomamba-config">

## regression_axomamba_config

<div class="api-signature">

```python
axosim.axomamba.regression_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L99-L108)

</div>

Build the voltage-focused recipe and apply keyword overrides.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>overrides</code> <span class="api-type">Any</span></dt>
<dd><span class="api-default">variadic.</span> Keyword fields that replace values in the selected architecture recipe.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig</span></dt>
<dd>Architecture recipe with the supplied keyword overrides applied.</dd>
</dl>

</section>

<section class="api-symbol" id="axomamba-population-axomamba-config">

## population_axomamba_config

<div class="api-signature">

```python
axosim.axomamba.population_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L111-L125)

</div>

Build the population-domain recipe and apply keyword overrides.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>overrides</code> <span class="api-type">Any</span></dt>
<dd><span class="api-default">variadic.</span> Keyword fields that replace values in the selected architecture recipe.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig</span></dt>
<dd>Architecture recipe with the supplied keyword overrides applied.</dd>
</dl>

</section>

<section class="api-symbol" id="axomamba-spike-axomamba-config">

## spike_axomamba_config

<div class="api-signature">

```python
axosim.axomamba.spike_axomamba_config(**overrides: Any) -> AxoMambaConfig
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L128-L139)

</div>

Build the spike-focused recipe and apply keyword overrides.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>overrides</code> <span class="api-type">Any</span></dt>
<dd><span class="api-default">variadic.</span> Keyword fields that replace values in the selected architecture recipe.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig</span></dt>
<dd>Architecture recipe with the supplied keyword overrides applied.</dd>
</dl>

</section>

<section class="api-symbol" id="axomamba-load-axomamba-config">

## load_axomamba_config

<div class="api-signature">

```python
axosim.axomamba.load_axomamba_config(path: str | Path | None=None, **overrides: Any) -> AxoMambaConfig
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L142-L148)

</div>

Read a JSON architecture configuration and apply keyword overrides; without a path, use the default AxoSim Mamba recipe.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>path</code> <span class="api-type">str | Path | None</span></dt>
<dd><span class="api-default">default=None.</span> Filesystem location to read or write; see the operation&#x27;s persistence contract.</dd>
<dt><code>overrides</code> <span class="api-type">Any</span></dt>
<dd><span class="api-default">variadic.</span> Keyword fields that replace values in the selected architecture recipe.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig</span></dt>
<dd>Configuration loaded from JSON with the requested overrides, or the default recipe when path is None.</dd>
</dl>

</section>

<section class="api-symbol" id="axomamba-coerce-axomamba-config">

## coerce_axomamba_config

<div class="api-signature">

```python
axosim.axomamba.coerce_axomamba_config(config: AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None) -> AxoMambaConfig
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L151-L158)

</div>

Convert a configuration object or mapping to AxoMambaConfig; None selects the default recipe.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None</span></dt>
<dd><span class="api-default">required.</span> Model configuration; use the defaults and constraints documented for its configuration class.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig</span></dt>
<dd>Converted configuration; an existing AxoMambaConfig is returned unchanged.</dd>
</dl>

</section>

<section class="api-symbol" id="axomamba-axomamba">

## AxoMamba

<div class="api-signature">

```python
axosim.axomamba.AxoMamba(config: AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None=None, *, mamba_classes: tuple[type, type | None] | None=None)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L161-L170)

</div>

Reusable named AxoSim Mamba surrogate built on the official Mamba backend.

Bases: `BranchOfficialMamba`.

Full-sequence and streaming methods are inherited from `BranchOfficialMamba` below. Preserve the recorded fused/fallback backend when loading weights.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None</span></dt>
<dd><span class="api-default">default=None.</span> Model configuration; use the defaults and constraints documented for its configuration class.</dd>
<dt><code>mamba_classes</code> <span class="api-type">tuple[type, type | None] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional backend class pair used when constructing the Mamba implementation.</dd>
</dl>

</section>

<section class="api-symbol" id="axomamba-axopytorchmamba">

## AxoPyTorchMamba

<div class="api-signature">

```python
axosim.axomamba.AxoPyTorchMamba(config: AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None=None)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L173-L182)

</div>

AxoMamba with the dependency-free PyTorch Mamba block, for tests/smokes.

Bases: `AxoMamba`.

Full-sequence and streaming methods are inherited from `BranchOfficialMamba` below. Preserve the recorded fused/fallback backend when loading weights.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None</span></dt>
<dd><span class="api-default">default=None.</span> Model configuration; use the defaults and constraints documented for its configuration class.</dd>
</dl>

</section>

<section class="api-symbol" id="axomamba-create-axomamba">

## create_axomamba

<div class="api-signature">

```python
axosim.axomamba.create_axomamba(config: AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None=None, *, use_pytorch_fallback: bool=False) -> AxoMamba
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/axomamba.py#L185-L192)

</div>

Construct a newly initialized AxoMamba, using the fused backend unless the PyTorch fallback is requested.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">AxoMambaConfig | BranchOfficialMambaConfig | Mapping[str, Any] | None</span></dt>
<dd><span class="api-default">default=None.</span> Model configuration; use the defaults and constraints documented for its configuration class.</dd>
<dt><code>use_pytorch_fallback</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=False.</span> Construct the CPU/test-compatible backend. Its checkpoint format differs from the fused backend.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>model</code> <span class="api-type">AxoMamba</span></dt>
<dd>Newly initialized AxoMamba or AxoPyTorchMamba, according to use_pytorch_fallback.</dd>
</dl>

</section>

<section class="api-symbol" id="mamba-official-branchofficialmambaconfig">

## BranchOfficialMambaConfig

<div class="api-signature">

```python
axosim.mamba_official.BranchOfficialMambaConfig(num_input: int = 1278, num_output: int = 2, num_branch: int = 45, num_synapse_per_branch: int = 100, input_to_synapse_routing: str | None = 'neuronio_routing', model_dim: int = 64, num_layers: int = 2, block_repeats: int = 1, state_dim: int = 16, conv_kernel: int = 4, expansion: int = 2, block_type: str = 'mamba1', head_dim: int = 64, num_groups: int = 1, chunk_size: int = 256, block_norm: bool = True, final_norm: bool = True, dropout: float = 0.0, residual_scale_init: float = 0.1, mamba_update_normalization: str = 'none', separate_heads: bool = False, soma_filter: bool = False, soma_filter_tau: float = 25.0, soma_filter_kernel: int = 129, learn_soma_filter_decay: bool = True, soma_multiplicative_gate: bool = False, soma_multiplicative_scale_init: float = 0.1, soma_peak_correction: bool = False, soma_peak_correction_scale_init: float = 0.1, soma_highpass_correction: bool = False, soma_highpass_correction_scale_init: float = 0.1, spike_voltage_coupling_scale: float = 0.0, morphology_ids: list[str] | None = None, morphology_embedding_scale: float | None = None, population_adapter_morphology_id: str | None = None, synapse_gain_scale: float | None = None, morphology_synapse_gain_scale: float | None = None, share_morphology_synapse_gain: bool = False, morphology_synapse_gain_rank: int = 0, morphology_synapse_feature_dim: int = 0, morphology_synapse_feature_hidden: int = 0, morphology_synapse_feature_scale: float | None = None, morphology_synapse_feature_storage_dtype: str = 'float32', local_tcn_scale: float | None = None, local_tcn_mode: str = 'dilated', local_tcn_position: str = 'parallel', share_local_tcn_pointwise: bool = False, local_tcn_pointwise_adapter_rank: int = 0, local_tcn_pointwise_rank: int = 0, local_tcn_output_rank: int = 0, mamba_projection_rank: int = 0, branch_gain: bool = False, branch_nonlinearity: str = 'none', branch_nonlinearity_scale_init: float = 0.1, branch_subunits: int = 0, branch_subunit_routing: str = 'contiguous', branch_subunit_scale: float = 1.0, branch_bilinear_rank: int = 0, branch_bilinear_scale: float | None = None, branch_trace_taus: list[float] | None = None, branch_trace_kernel: int = 65, hidden_trace_taus: list[float] | None = None, hidden_trace_kernel: int = 129, temporal_refine_kernel: int = 0, integrative_mixer: bool = False, integrative_mixer_short_kernel: int = 9, integrative_mixer_long_kernel: int = 65, integrative_mixer_position: str = 'pre', integrative_mixer_long_path_bias: float = 0.5)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/mamba_official.py#L29-L98)

</div>

Architecture and optional branch, morphology, temporal-correction, and readout settings for the fused Mamba model.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>num_input</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1278.</span> Input-channel count.</dd>
<dt><code>num_output</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=2.</span> Output-channel count.</dd>
<dt><code>num_branch</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=45.</span> Branched input-feature count.</dd>
<dt><code>num_synapse_per_branch</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=100.</span> Contact slots per branch.</dd>
<dt><code>input_to_synapse_routing</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">default=&#x27;neuronio_routing&#x27;.</span></dd>
<dt><code>model_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=64.</span> Temporal hidden-feature width.</dd>
<dt><code>num_layers</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=2.</span> Number of temporal layers.</dd>
<dt><code>block_repeats</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1.</span></dd>
<dt><code>state_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=16.</span> Temporal state width.</dd>
<dt><code>conv_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=4.</span></dd>
<dt><code>expansion</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=2.</span></dd>
<dt><code>block_type</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;mamba1&#x27;.</span></dd>
<dt><code>head_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=64.</span> Configured head width of the backbone.</dd>
<dt><code>num_groups</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=1.</span></dd>
<dt><code>chunk_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=256.</span> Chunk length for the supported Mamba or streaming execution path.</dd>
<dt><code>block_norm</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>final_norm</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>dropout</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.0.</span></dd>
<dt><code>residual_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span> Initial learned multiplier on the residual update.</dd>
<dt><code>mamba_update_normalization</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;none&#x27;.</span> Normalize residual updates when the supported fixed_rms mode is selected.</dd>
<dt><code>separate_heads</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_filter</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_filter_tau</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=25.0.</span></dd>
<dt><code>soma_filter_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=129.</span></dd>
<dt><code>learn_soma_filter_decay</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=True.</span></dd>
<dt><code>soma_multiplicative_gate</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_multiplicative_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span></dd>
<dt><code>soma_peak_correction</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_peak_correction_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span></dd>
<dt><code>soma_highpass_correction</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>soma_highpass_correction_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span></dd>
<dt><code>spike_voltage_coupling_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.0.</span></dd>
<dt><code>morphology_ids</code> <span class="api-type">list[str] | None</span></dt>
<dd><span class="api-default">default=None.</span> Ordered morphology identity vocabulary.</dd>
<dt><code>morphology_embedding_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>population_adapter_morphology_id</code> <span class="api-type">str | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>synapse_gain_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>morphology_synapse_gain_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>share_morphology_synapse_gain</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>morphology_synapse_gain_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>morphology_synapse_feature_dim</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>morphology_synapse_feature_hidden</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>morphology_synapse_feature_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>morphology_synapse_feature_storage_dtype</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;float32&#x27;.</span></dd>
<dt><code>local_tcn_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>local_tcn_mode</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;dilated&#x27;.</span></dd>
<dt><code>local_tcn_position</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;parallel&#x27;.</span></dd>
<dt><code>share_local_tcn_pointwise</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>local_tcn_pointwise_adapter_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>local_tcn_pointwise_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>local_tcn_output_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>mamba_projection_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>branch_gain</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>branch_nonlinearity</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;none&#x27;.</span></dd>
<dt><code>branch_nonlinearity_scale_init</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.1.</span></dd>
<dt><code>branch_subunits</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>branch_subunit_routing</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;contiguous&#x27;.</span></dd>
<dt><code>branch_subunit_scale</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=1.0.</span></dd>
<dt><code>branch_bilinear_rank</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>branch_bilinear_scale</code> <span class="api-type">float | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>branch_trace_taus</code> <span class="api-type">list[float] | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>branch_trace_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=65.</span></dd>
<dt><code>hidden_trace_taus</code> <span class="api-type">list[float] | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
<dt><code>hidden_trace_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=129.</span></dd>
<dt><code>temporal_refine_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=0.</span></dd>
<dt><code>integrative_mixer</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">default=False.</span></dd>
<dt><code>integrative_mixer_short_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=9.</span></dd>
<dt><code>integrative_mixer_long_kernel</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">default=65.</span></dd>
<dt><code>integrative_mixer_position</code> <span class="api-type">str</span></dt>
<dd><span class="api-default">default=&#x27;pre&#x27;.</span></dd>
<dt><code>integrative_mixer_long_path_bias</code> <span class="api-type">float</span></dt>
<dd><span class="api-default">default=0.5.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as read-only attributes.

</section>

<section class="api-symbol" id="mamba-official-branchmambastreamingstate">

## BranchMambaStreamingState

<div class="api-signature">

```python
axosim.mamba_official.BranchMambaStreamingState(mamba_states: list[tuple[torch.Tensor, torch.Tensor]], local_tcn_histories: list[torch.Tensor], morphology_feature_gains: torch.Tensor | None = None)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/mamba_official.py#L102-L107)

</div>

Mutable recurrent state for exact one-timestep AxoMamba inference.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>mamba_states</code> <span class="api-type">list[tuple[torch.Tensor, torch.Tensor]]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>local_tcn_histories</code> <span class="api-type">list[torch.Tensor]</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>morphology_feature_gains</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">default=None.</span></dd>
</dl>

<p class="api-label">Attributes</p>

Constructor fields are retained as attributes.

</section>

<section class="api-symbol" id="mamba-official-branchofficialmamba">

## BranchOfficialMamba

<div class="api-signature">

```python
axosim.mamba_official.BranchOfficialMamba(config: BranchOfficialMambaConfig, *, mamba_classes: tuple[type[nn.Module], type[nn.Module] | None] | None=None)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/mamba_official.py#L110-L1808)

</div>

Branch-routed wrapper around the official mamba-ssm Mamba module.

Bases: `nn.Module`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">BranchOfficialMambaConfig</span></dt>
<dd><span class="api-default">required.</span> Model configuration; use the defaults and constraints documented for its configuration class.</dd>
<dt><code>mamba_classes</code> <span class="api-type">tuple[type[nn.Module], type[nn.Module] | None] | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional backend class pair used when constructing the Mamba implementation.</dd>
</dl>

<p class="api-label">Methods</p>

<ul class="api-method-list">
<li><a href="#mamba-official-branchofficialmamba-forward"><code>BranchOfficialMamba.forward()</code></a></li>
<li><a href="#mamba-official-branchofficialmamba-allocate-streaming-state"><code>BranchOfficialMamba.allocate_streaming_state()</code></a></li>
<li><a href="#mamba-official-branchofficialmamba-streaming-step"><code>BranchOfficialMamba.streaming_step()</code></a></li>
<li><a href="#mamba-official-branchofficialmamba-streaming-step-events"><code>BranchOfficialMamba.streaming_step_events()</code></a></li>
</ul>

<section class="api-method" id="mamba-official-branchofficialmamba-forward">

### BranchOfficialMamba.forward

<div class="api-signature">

```python
axosim.mamba_official.BranchOfficialMamba.forward(x: torch.Tensor, *, morphology_indices: torch.Tensor | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/mamba_official.py#L678-L689)

</div>

Predict native spike and soma outputs for the supplied sequence.

x is (B,T,num_input), and optional morphology_indices is integer (B,). Morphology-conditioned synaptic gains require valid morphology indices. Returns (B,T,num_output) in the checkpoint's spike-logit and soma-target coordinates.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>x</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Input tensor for the full-sequence or streaming operation.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>Spike-logit and soma-target channels in the tensor shape specified above.</dd>
</dl>

</section>

<section class="api-method" id="mamba-official-branchofficialmamba-allocate-streaming-state">

### BranchOfficialMamba.allocate_streaming_state

<div class="api-signature">

```python
axosim.mamba_official.BranchOfficialMamba.allocate_streaming_state(batch_size: int, *, device: torch.device | str | None=None, dtype: torch.dtype | None=None) -> BranchMambaStreamingState
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/mamba_official.py#L954-L994)

</div>

Allocate state that advances a population without replaying history.

Allocates a persistent streaming-state record for the requested batch_size, device, and dtype. Allocate a fresh state for independent traces or changed batch membership.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>batch_size</code> <span class="api-type">int</span></dt>
<dd><span class="api-default">required.</span> Examples processed per batch.</dd>
<dt><code>device</code> <span class="api-type">torch.device | str | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Execution or allocation device.</dd>
<dt><code>dtype</code> <span class="api-type">torch.dtype | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Floating-point execution or allocation dtype.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>state</code> <span class="api-type">BranchMambaStreamingState</span></dt>
<dd>Fresh recurrent buffers and local-filter histories for the selected batch, device, and dtype.</dd>
</dl>

</section>

<section class="api-method" id="mamba-official-branchofficialmamba-streaming-step">

### BranchOfficialMamba.streaming_step

<div class="api-signature">

```python
axosim.mamba_official.BranchOfficialMamba.streaming_step(x: torch.Tensor, state: BranchMambaStreamingState, *, morphology_indices: torch.Tensor | None=None, chunk_size: int | None=None) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/mamba_official.py#L996-L1087)

</div>

Advance one timestep and return `(batch, 1, output)` predictions.

Advances the supplied mutable streaming state by one native input step. The guide supplies x as (B,num_input), with one morphology index per item when configured. Returns (B,1,num_output).

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>x</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Input tensor for the full-sequence or streaming operation.</dd>
<dt><code>state</code> <span class="api-type">BranchMambaStreamingState</span></dt>
<dd><span class="api-default">required.</span> Temporal state returned by the matching initial-state or allocation method.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
<dt><code>chunk_size</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Chunk length for the supported Mamba or streaming execution path.</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-parameters">
<dt><code>prediction</code> <span class="api-type">torch.Tensor</span></dt>
<dd>One native output step (batch,1,num_output); the supplied state is updated in place.</dd>
</dl>

</section>

<section class="api-method" id="mamba-official-branchofficialmamba-streaming-step-events">

### BranchOfficialMamba.streaming_step_events

<div class="api-signature">

```python
axosim.mamba_official.BranchOfficialMamba.streaming_step_events(event_indices: torch.Tensor, event_values: torch.Tensor, state: BranchMambaStreamingState, *, morphology_indices: torch.Tensor | None=None, chunk_size: int | None=None, output_buffer: torch.Tensor | None=None, retain_base_soma_prediction: bool=True) -> torch.Tensor
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/mamba_official.py#L1310-L1451)

</div>

Advance one timestep from padded sparse channel/value event rows.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>event_indices</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span></dd>
<dt><code>event_values</code> <span class="api-type">torch.Tensor</span></dt>
<dd><span class="api-default">required.</span> Signed floating-point event amplitudes, one per paired address.</dd>
<dt><code>state</code> <span class="api-type">BranchMambaStreamingState</span></dt>
<dd><span class="api-default">required.</span> Temporal state returned by the matching initial-state or allocation method.</dd>
<dt><code>morphology_indices</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Integer class assignments into the model&#x27;s ordered morphology vocabulary; one per batch item or persistent neuron.</dd>
<dt><code>chunk_size</code> <span class="api-type">int | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Chunk length for the supported Mamba or streaming execution path.</dd>
<dt><code>output_buffer</code> <span class="api-type">torch.Tensor | None</span></dt>
<dd><span class="api-default">keyword-only, default=None.</span> Optional preallocated output tensor for the operation.</dd>
<dt><code>retain_base_soma_prediction</code> <span class="api-type">bool</span></dt>
<dd><span class="api-default">keyword-only, default=True.</span> Keep the base soma readout available for inspection.</dd>
</dl>

<p class="api-label">Returns</p>

`torch.Tensor`

</section>

</section>

<section class="api-symbol" id="mamba-official-branchpytorchmamba">

## BranchPyTorchMamba

<div class="api-signature">

```python
axosim.mamba_official.BranchPyTorchMamba(config: BranchOfficialMambaConfig)
```

[Source](https://github.com/Axym-Labs/axosim/blob/856207f6de56dbf8e3f754a142581a7c050eeac6/src/axosim/mamba_official.py#L1810-L1818)

</div>

Branch-routed Mamba wrapper using the differentiable PyTorch fallback block.

Bases: `BranchOfficialMamba`.

<p class="api-label">Parameters</p>

<dl class="api-parameters">
<dt><code>config</code> <span class="api-type">BranchOfficialMambaConfig</span></dt>
<dd><span class="api-default">required.</span> Model configuration; use the defaults and constraints documented for its configuration class.</dd>
</dl>

</section>
