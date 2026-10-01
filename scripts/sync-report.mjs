import { readFileSync, writeFileSync, copyFileSync, mkdtempSync, mkdirSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';

const root = resolve(import.meta.dirname, '..');
const report = resolve(process.argv[2] || join(root, '../AxoSim-paper'));
const figure = join(report, 'figures/central-comparison.tex');
const temp = mkdtempSync(join(tmpdir(), 'axo-docs-figure-'));
mkdirSync(join(root,'public/report'), { recursive:true });
mkdirSync(join(root,'public/figures'), { recursive:true });
copyFileSync(figure, join(temp, 'figure.tex'));
writeFileSync(join(temp, 'main.tex'), String.raw`\documentclass[tikz,border=9pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{mathpazo}
\usepackage{xcolor}
\definecolor{AxymPrimary}{HTML}{3F21B6}
\definecolor{AxymInk}{HTML}{111827}
\definecolor{AxymMuted}{HTML}{4B5563}
\begin{document}
\input{figure.tex}
\end{document}
`);
execFileSync('tectonic', ['-X','compile','main.tex'], { cwd:temp, stdio:'inherit' });
execFileSync('pdftocairo', ['-svg',join(temp,'main.pdf'),join(root,'public/figures/central-comparison.svg')]);
execFileSync('pdftocairo', ['-png','-singlefile','-scale-to','1800',join(temp,'main.pdf'),join(root,'public/figures/central-comparison')]);
copyFileSync(join(report,'main.pdf'),join(root,'public/report/main.pdf'));
const hash = path => createHash('sha256').update(readFileSync(path)).digest('hex');
writeFileSync(join(root,'public/report/provenance.json'), JSON.stringify({
  report_sha256:hash(join(report,'main.pdf')),
  central_figure_source_sha256:hash(figure),
  svg_sha256:hash(join(root,'public/figures/central-comparison.svg')),
  report_repository:'https://github.com/Axym-Labs/AxoSim-paper',
},null,2)+'\n');
console.log('Synced report PDF and vector central figure.');
