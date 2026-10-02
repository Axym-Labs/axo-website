import { readFileSync, writeFileSync, copyFileSync, mkdtempSync, mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';

const root = resolve(import.meta.dirname, '..');
const report = resolve(process.argv[2] || join(root, '../AxoSim-paper'));
const figure = join(report, 'figures/central-comparison.tex');
const temp = mkdtempSync(join(tmpdir(), 'axo-docs-figure-'));
const deterministicEnv = { ...process.env, SOURCE_DATE_EPOCH:'1788134400' };
const hash = path => createHash('sha256').update(readFileSync(path)).digest('hex');
const figureSource = readFileSync(figure, 'utf8');
const fontDir = join(report, 'assets/fonts');
const publicEvidence = join(report, 'reproducibility/evidence/population-platform-publication/runs');
const axosimEvidence = join(publicEvidence, 'iteration-1283-1287-five-model-training/summary.json');
const branchEvidence = join(publicEvidence, 'iteration-1324-published-branch-elm-final-panel/summary.json');
const axosim = JSON.parse(readFileSync(axosimEvidence, 'utf8'));
const branch = JSON.parse(readFileSync(branchEvidence, 'utf8'));
const coreCsv = join(report, 'data/central-comparison.csv');
const coreRate = Number(readFileSync(coreCsv, 'utf8').split('\n')
  .find(line => line.startsWith('CoreNEURON,Hay L5PC reference,Inference throughput,')).split(',')[3]);
assert(Number.isFinite(coreRate) && coreRate > 0, 'CoreNEURON recorded rate is missing');
const historyEvidence = join(report, 'reproducibility/evidence/history-throughput/learned-model-timings.json');
const coreHistoryEvidence = join(report, 'reproducibility/evidence/history-throughput/coreneuron-timing.json');
const history = JSON.parse(readFileSync(historyEvidence, 'utf8'));
const coreHistory = JSON.parse(readFileSync(coreHistoryEvidence, 'utf8'));
assert(history.contract.batch_size === 1 && history.contract.history_steps === 2000 &&
  history.contract.input_contacts === 1278 && history.contract.dtype === 'float32' &&
  history.contract.timing_repeats === 40 && history.contract.gpu_isolation_checked,
  'History timing contract changed');
assert(coreHistory.model_id === 'coreneuron' && coreHistory.contract.batch_size === 1 &&
  coreHistory.contract.history_steps === 2000 && coreHistory.contract.native_dt_ms === 1,
  'CoreNEURON history timing contract changed');
assert(coreHistory.contract.input_sha256 === history.contract.input_sha256 &&
  coreHistory.contract.input_exactly_matches_learned_history &&
  coreHistory.execution_verification.coreneuron_enabled &&
  coreHistory.execution_verification.coreneuron_gpu &&
  coreHistory.repeat_voltage_tolerance_passed &&
  coreHistory.diagnostics.every(row => row.initial_nonzero_synaptic_states === 0 &&
    row.nonzero_final_excitatory_B_NMDA_states > 0 &&
    row.nonzero_final_inhibitory_B_states > 0 && row.spike_labels_identical_to_first),
  'CoreNEURON input, execution or replay verification failed');
const historyRows = new Map(history.results.map(row => [row.model_id, row]));
assert.equal(historyRows.size,7,'Seven distinct learned history timings are required');
for (const row of [...history.results,coreHistory]) {
  const samples = [...row.latency_samples_ms].sort((a,b) => a-b);
  assert(samples.length >= 3 && samples.every(value => Number.isFinite(value) && value > 0),
    'History latency samples must be positive actual measurements');
  const median = samples.length % 2 ? samples[(samples.length-1)/2] :
    (samples[samples.length/2-1]+samples[samples.length/2])/2;
  assert(Math.abs(median-row.latency_median_ms) < 1e-6,'History latency median disagrees with samples');
  assert(Math.abs(row.history_steps_per_second-2000000/median) < 1e-6,
    'History rate disagrees with measured latency');
}
for (const row of [...axosim.results,...branch.results]) {
  const measured = historyRows.get(row.profile_id || row.candidate_id);
  if (measured) assert.equal(measured.checkpoint_sha256,row.checkpoint_sha256,
    'History throughput must use the existing plotted checkpoint');
}
const values = row => ({
  inference_neuron_steps_per_second:row.benchmark.inference.neuron_steps_per_second,
  voltage_sera_mv2:row.metrics.voltage_sera_mv2,
  dynamics_sera_mv2_per_ms2:row.metrics.dynamics_sera_mv2_per_ms2,
  mean_f1_0_5ms:row.metrics.spike_mean_f1_0_5ms,
  f1_5ms:row.metrics.spike_f1_5ms,
  ...(historyRows.has(row.profile_id || row.candidate_id) ? {
    history_steps_per_second:historyRows.get(row.profile_id || row.candidate_id).history_steps_per_second,
  } : {}),
});
const raw = Object.fromEntries([
  ...axosim.results.map(row => [row.profile_id, values(row)]),
  ...branch.results.map(row => [row.candidate_id, values(row)]),
  ['coreneuron', {
    inference_neuron_steps_per_second:coreRate, voltage_sera_mv2:0,
    dynamics_sera_mv2_per_ms2:0, mean_f1_0_5ms:1, f1_5ms:1,
    history_steps_per_second:coreHistory.history_steps_per_second,
  }],
]);
const mapped = value => [
  1-Math.exp(-value.inference_neuron_steps_per_second/1e7),
  Math.exp(-value.voltage_sera_mv2/350),
  Math.exp(-value.dynamics_sera_mv2_per_ms2/450),
  value.mean_f1_0_5ms, value.f1_5ms,
  1-Math.exp(-value.history_steps_per_second/1e6),
];
// Fail closed on stale or invented coordinates before rendering either theme.
const plotted = [];
for (const match of figureSource.matchAll(/% series: (\S+)\s+\\RadarPolygon[^\n]+\n\s+\{([^\n]+)\}/g)) {
  const [,id,path] = match;
  assert(raw[id], `No frozen evidence for plotted series ${id}`);
  const coordinates = [...path.matchAll(/\((-?\d+):([\d.]+)\)/g)];
  assert.deepEqual(coordinates.map(point => Number(point[1])),[90,30,-30,-90,-150,150],
    `${id}: six evenly spaced axis angles are required`);
  const radii = coordinates.map(point => Number(point[2]));
  const expected = mapped(raw[id]);
  assert.equal(radii.length,6,`${id}: six axis values are required`);
  radii.forEach((value,i) => assert(Math.abs(value-expected[i]) <= 0.00000501,
    `${id}: axis ${i} has ${value}, expected ${expected[i]}`));
  plotted.push(id);
}
assert.deepEqual([...plotted].sort(), [
  'axosim-gru-small','axosim-mamba-medium','branch-elm-memory-1',
  'branch-elm-memory-30','branch-elm-memory-100','coreneuron',
].sort(), 'Central figure series coverage changed');
const learnedRows = [...axosim.results,...branch.results];
assert(learnedRows.every(row => row.benchmark.contract.batch_size === 32 &&
  row.benchmark.contract.window_steps === 500 &&
  row.benchmark.contract.input_contacts === 1278 &&
  row.benchmark.contract.dtype === 'float32'), 'Learned-model timing contracts disagree');
const evaluationTraces = [...axosim.results[0].evaluation_trace_ids].sort();
assert.equal(evaluationTraces.length,120,'Expected 120 confirmation traces');
for (const row of learnedRows) {
  assert.deepEqual([...row.evaluation_trace_ids].sort(),evaluationTraces,
    'Central figure metrics must use the same held-out confirmation traces');
}
// This command is an explicit publication sync, not part of the static site
// build. Recompile first so the downloadable PDF cannot retain stale authors,
// figure labels, or scientific content while the vector export has moved on.
execFileSync('tectonic',['-X','compile','main.tex'], {
  cwd:report,env:deterministicEnv,stdio:'inherit',
});
mkdirSync(join(root,'public/report'), { recursive:true });
mkdirSync(join(root,'public/figures'), { recursive:true });
mkdirSync(join(temp,'assets/fonts'), { recursive:true });
copyFileSync(figure, join(temp, 'figure.tex'));
for (const name of ['Inter-Regular.ttf','Inter-SemiBold.ttf','OFL.txt']) {
  copyFileSync(join(fontDir,name),join(temp,'assets/fonts',name));
}
const themes = {
  light:{primary:'3F21B6',secondary:'8C7AD3',ink:'171717',grid:'D9D9DF',reference:'919191'},
  dark:{primary:'B3A0FF',secondary:'8C7AD3',ink:'EEEEEE',grid:'414145',reference:'A3A3A3'},
};
const variants = {};
for (const [theme,palette] of Object.entries(themes)) {
  writeFileSync(join(temp,'main.tex'), String.raw`\documentclass[tikz,border=8pt]{standalone}
\usepackage{xcolor}
\definecolor{AxymPrimary}{HTML}{${palette.primary}}
\definecolor{AxymSecondary}{HTML}{${palette.secondary}}
\definecolor{AxymInk}{HTML}{${palette.ink}}
\definecolor{RadarGridInk}{HTML}{${palette.grid}}
\definecolor{RadarReferenceInk}{HTML}{${palette.reference}}
\begin{document}
\input{figure.tex}
\end{document}
`);
  execFileSync('tectonic',['-X','compile','main.tex'], { cwd:temp,env:deterministicEnv,stdio:'inherit' });
  const stem = theme === 'light' ? 'central-comparison' : 'central-comparison-dark';
  const svg = join(root,'public/figures',`${stem}.svg`);
  const png = join(root,'public/figures',`${stem}.png`);
  execFileSync('pdftocairo',['-svg',join(temp,'main.pdf'),svg]);
  execFileSync('pdftocairo',['-png','-transp','-singlefile','-scale-to','1800',join(temp,'main.pdf'),join(root,'public/figures',stem)]);
  let vector = readFileSync(svg,'utf8');
  const dimensions = vector.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
  // Cairo outlines the actual Inter glyphs. No page-sized background is drawn.
  vector = vector.replace(/(<svg\b[^>]*>)/, `$1\n<title>AxoSim and baseline comparison (${theme} theme)</title>\n<desc>GRU Small and Mamba Medium, three released Branch-ELM sizes, and CoreNEURON; axes show inference throughput, voltage and dynamics fidelity, Mean F1 0–5 ms, F1 at 5 ms, and history throughput. Axis mappings and measurements are documented in the technical report appendix.</desc>`);
  writeFileSync(svg,vector);
  variants[theme] = {svg:`/figures/${stem}.svg`,png:`/figures/${stem}.png`,svg_sha256:hash(svg),png_sha256:hash(png),viewBox:dimensions};
}
copyFileSync(join(report,'main.pdf'),join(root,'public/report/main.pdf'));
const data = {
  axis_order:['Inference throughput','Voltage fidelity','Dynamics fidelity','Mean F1 0–5 ms','F1 @ 5 ms','History throughput'],
  mappings:['1-exp(-rate/10000000)','exp(-Voltage SERA/350)','exp(-Dynamics SERA/450)','identity','identity','1-exp(-history rate/1000000)'],
  plotted_series:plotted,
  raw_values:raw,
  history_timing_contracts:{learned:history.contract,coreneuron:coreHistory.contract},
  evidence:[
    {path:axosimEvidence.slice(report.length+1),sha256:hash(axosimEvidence)},
    {path:branchEvidence.slice(report.length+1),sha256:hash(branchEvidence)},
    {path:coreCsv.slice(report.length+1),sha256:hash(coreCsv)},
    {path:historyEvidence.slice(report.length+1),sha256:hash(historyEvidence)},
    {path:coreHistoryEvidence.slice(report.length+1),sha256:hash(coreHistoryEvidence)},
  ],
};
writeFileSync(join(root,'public/report/central-figure-values.json'),JSON.stringify(data,null,2)+'\n');
writeFileSync(join(root,'public/report/provenance.json'), JSON.stringify({
  report_sha256:hash(join(report,'main.pdf')),
  report_source_sha256:hash(join(report,'main.tex')),
  central_figure_source_sha256:hash(figure),
  svg_sha256:variants.light.svg_sha256,
  svg_dark_sha256:variants.dark.svg_sha256,
  variants,
  figure_values_sha256:hash(join(root,'public/report/central-figure-values.json')),
  font:{family:'Inter',source:'@fontsource-variable/inter 5.3.0 (latin wght normal)',weights:[400,600],regular_sha256:hash(join(fontDir,'Inter-Regular.ttf')),semibold_sha256:hash(join(fontDir,'Inter-SemiBold.ttf')),license:'SIL Open Font License 1.1'},
  report_authors:['Davide Wiest','Jonathan Schäfer'],
  report_repository:'https://github.com/Axym-Labs/AxoSim-paper',
},null,2)+'\n');
console.log(`Synced report PDF and light/dark Inter vectors; verified ${plotted.length} plotted series against frozen measurements.`);
