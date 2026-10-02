import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { resolve, join } from 'node:path';
import assert from 'node:assert/strict';

const root = resolve(import.meta.dirname, '..');
const dist = join(root, 'dist');
function files(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap(item => item.isDirectory() ? files(join(dir, item.name)) : [join(dir, item.name)]);
}
const pages = files(dist).filter(path => path.endsWith('.html') && !path.endsWith('/404.html'));
const required = ['/', '/installation/', '/models/', '/connected-populations/', '/inference/', '/history-scan/', '/training/', '/populations/', '/sparse-events/', '/adaptation/', '/cuda-graphs/', '/evaluation/', '/datasets/', '/reproducibility/', '/troubleshooting/', '/api/', '/api/connected-population/', '/api/history-scan/'];
for (const path of required) assert(existsSync(join(dist, path, 'index.html')), `Missing page: ${path}`);
assert.equal(readFileSync(join(dist, 'CNAME'), 'utf8').trim(), 'axo.axym.org');
assert(existsSync(join(dist, 'pagefind/pagefind.js')), 'Search index missing');
assert(statSync(join(dist, 'report/main.pdf')).size > 100000, 'Report missing or empty');
assert(existsSync(join(dist, 'figures/central-comparison.svg')), 'Comparison figure missing');
assert(readFileSync(join(dist, 'sitemap.xml'), 'utf8').includes('https://axo.axym.org/api/'), 'API omitted from sitemap');
const inventory = JSON.parse(readFileSync(join(dist, 'api-inventory.json'), 'utf8'));
const expectedExports = [
  'AXOSIM_POPULATION_PROFILE', 'MILLION_NEURON_REALTIME_CONTRACT', 'AxoMamba', 'AxoMambaConfig',
  'AxoSimGRU', 'AxoSimLite', 'AxoSimMamba', 'AxoSimModelProfile', 'AxoSimPopulation',
  'CudaGraphAdaptationStep', 'HomeostaticThresholdController', 'AXOSIM_MODEL_PROFILES',
  'BranchELM', 'BranchELMConfig', 'LargePopulationSimulationContract',
  'MixedQuantizedNeuronBehaviorBank', 'PopulationInferenceProfile',
  'ProceduralMorphologyConnectomeRouter', 'QuantizedSynapticEfficacyBank',
  'compact_active_sources', 'dequantize_synaptic_efficacies',
  'dequantize_mixed_neuron_behavior_parameters', 'quantize_synaptic_efficacies',
  'quantize_mixed_neuron_behavior_parameters', 'create_axosim_profile',
  'ConnectedPopulation', 'ExplicitConnectome', 'InputEvents', 'PopulationFrame',
  'ProceduralConnectome', 'create_population',
  'HistoryScanBackend', 'HistoryScanResult', 'scan_histories',
];
assert.deepEqual(inventory.exports.map(item => item.name).sort(), expectedExports.sort(), 'Public export inventory differs from the supported source surface');
assert.equal(new Set(inventory.exports.map(item => item.name)).size, expectedExports.length, 'Duplicate export entries');
assert(/^[a-f0-9]{40}$/.test(inventory.source.commit), 'API source revision is not pinned');
assert.equal(inventory.source.repository, 'https://github.com/Axym-Labs/axosim', 'Stale API source repository');
for (const item of inventory.exports) assert(existsSync(join(dist,item.page,'index.html')), `Export reference missing: ${item.name}`);
assert.deepEqual(inventory.cli.map(item=>item.command).sort(), ['axosim','axosim-evaluate-model','axosim-setup'].sort());
const provenance = JSON.parse(readFileSync(join(dist, 'report/provenance.json'), 'utf8'));
const { createHash } = await import('node:crypto');
const digest = file => createHash('sha256').update(readFileSync(file)).digest('hex');
assert.equal(digest(join(dist,'report/main.pdf')),provenance.report_sha256,'Report provenance mismatch');
assert.equal(digest(join(dist,'figures/central-comparison.svg')),provenance.svg_sha256,'Figure provenance mismatch');
assert.equal(digest(join(dist,'figures/central-comparison-dark.svg')),provenance.svg_dark_sha256,'Dark figure provenance mismatch');
assert.equal(digest(join(dist,'report/central-figure-values.json')),provenance.figure_values_sha256,'Figure measurement manifest mismatch');
for (const variant of Object.values(provenance.variants)) {
  assert.equal(digest(join(dist,variant.png)),variant.png_sha256,'Figure PNG provenance mismatch');
}
assert.equal(digest(join(dist,'favicon.svg')),digest(join(dist,'brand/axym-logo.svg')),'Navbar and favicon must use the same mark');
assert(existsSync(join(dist,'favicon.ico')), 'Multi-size favicon missing');
let codeBlocks = 0;
const errors = [];
for (const file of pages) {
  const html = readFileSync(file, 'utf8');
  const route = '/' + file.slice(dist.length+1).replace(/index\.html$/, '');
  assert.equal((html.match(/<h1\b/g)||[]).length, 1, `${route}: expected one h1`);
  assert(html.includes('data-pagefind-body'), `${route}: not indexed`);
  assert(html.includes(`href="https://axo.axym.org${route}"`), `${route}: canonical mismatch`);
  for (const match of html.matchAll(/(?:href|src)="(\/[^"<>]*)"/g)) {
    const raw = match[1].replaceAll('&amp;', '&');
    const url = new URL(raw, 'https://axo.axym.org');
    let destination = join(dist, decodeURIComponent(url.pathname));
    if (url.pathname.endsWith('/')) destination = join(destination, 'index.html');
    if (!existsSync(destination)) { errors.push(`${route}: missing ${raw}`); continue; }
    if (url.hash && destination.endsWith('.html')) {
      const target = readFileSync(destination, 'utf8');
      const id = decodeURIComponent(url.hash.slice(1));
      if (!target.includes(`id="${id}"`)) errors.push(`${route}: missing anchor ${raw}`);
    }
  }
  const pres = [...html.matchAll(/<pre\b[^>]*>([\s\S]*?)<\/pre>/g)];
  codeBlocks += pres.length;
  for (const pre of pres) {
    if (!pre[0].includes('astro-code')) errors.push(`${route}: unhighlighted code block`);
  }
}
assert.equal(errors.length, 0, errors.join('\n'));
assert(codeBlocks >= 25, `Only ${codeBlocks} code blocks; lifecycle documentation incomplete`);
console.log(`Verified ${pages.length} routes, ${codeBlocks} highlighted code blocks, internal links/anchors, canonical URLs, report, figure, and search index.`);
