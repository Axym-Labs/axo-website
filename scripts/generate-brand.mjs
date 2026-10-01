/** Reproduce the original Axym A/X/Y/M mark. No network or raster library required. */
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { deflateSync } from 'node:zlib';

// MNIST test-image archive, sample 61 (zero-based), handwritten digit 8.
// Source: https://storage.googleapis.com/cvdf-datasets/mnist/t10k-images-idx3-ubyte.gz
// Archive SHA-256: 8d422c7b0a1c1c79245a5bcf07fe86e33eeafee792b84584aec276f5a2dbc4e6
// Credit: Yann LeCun, Corinna Cortes, Christopher J. C. Burges.
const sample = Buffer.from(
  [
    '00000000000000000000000000000000000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
    '000000000000000000000000002b2f2f000000000000000000000000',
    '0000000000000000000000096cf9fdfdd0cfcfcf95410d0000000000',
    '0000000000000000000009b8fefdfdfdfefdfdfdfefdd51900000000',
    '00000000000000000037cbfefec77f7f3c5d544497defea100000000',
    '0000000000000000008afdfdc713000000000000009bfdd300000000',
    '0000000000000000008afdfd11000000000000004af1fdd300000000',
    '00000000000000000069fdfd6600000000000022e5fdfda000000000',
    '0000000000000000000095fee5280000002699fefefeb41900000000',
    '0000000000000000000013c6fecf092248ebfdfde08b0d0000000000',
    '000000000000000000000011d3fdd7f0fefdea801100000000000000',
    '000000000000000000000066e5fdfdfde44d0d000000000000000000',
    '000000000000000046aafefefefefefe770000000000000000000000',
    '00000000001a82e6fefdfdb97340d3fdf81500000000000000000000',
    '00000000a6e8fdfdf7a22e0d075bf5fdfe3800000000000000000000',
    '0000000080fdfdfdd25d7f9fccfdfdfde40f00000000000000000000',
    '000000000086f1fefffefefefefefee4220000000000000000000000',
    '0000000000001b738ccecececfce7b0f000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
    '00000000000000000000000000000000000000000000000000000000',
  ].join(''),
  'hex',
);
if (sample.length !== 28 * 28) throw new Error('MNIST sample must contain exactly 784 pixels');

// Original 7 × 7 glyphs, each occupying a square 14 × 14-pixel quadrant interior.
const glyphs = [
  ['0111110', '1100011', '1100011', '1111111', '1100011', '1100011', '1100011'],
  ['1100011', '0110110', '0011100', '0001000', '0011100', '0110110', '1100011'],
  ['1100011', '1100011', '0110110', '0011100', '0001000', '0001000', '0001000'],
  ['1100011', '1110111', '1111111', '1101011', '1100011', '1100011', '1100011'],
];

function ink(x, y) {
  const sx = Math.max(0, Math.min(27, Math.round(x)));
  const sy = Math.max(0, Math.min(27, Math.round(y)));
  return sample[sy * 28 + sx] / 255;
}

// Clockwise rotation, 2× enlargement, plus an offset reflection of the same sample.
// A faint deterministic stipple extends the digit's rich local structure into its margins.
function field(x, y) {
  const first = ink(6 + y / 2, 22 - x / 2);
  const second = ink(21 - y / 1.8, 6 + x / 1.8);
  const stipple = ((x * 73 + y * 151 + x * y * 29) % 101) / 101;
  return Math.min(1, 0.08 + 0.73 * first + 0.36 * second + 0.12 * stipple);
}

const grid = Array.from({ length: 32 }, (_, y) => Array.from({ length: 32 }, (_, x) => {
  const quadrant = Math.floor(y / 16) * 2 + Math.floor(x / 16);
  const gx = Math.floor(((x % 16) - 1) / 2);
  const gy = Math.floor(((y % 16) - 1) / 2);
  if (gx >= 0 && gx < 7 && gy >= 0 && gy < 7 && glyphs[quadrant][gy][gx] === '1') {
    return [255, 255, 255];
  }
  return [63, 33, 182].map(channel => Math.round(channel * field(x, y)));
}));

const groups = new Map();
grid.forEach((row, y) => row.forEach((rgb, x) => {
  const color = `#${rgb.map(channel => channel.toString(16).padStart(2, '0')).join('')}`;
  groups.set(color, `${groups.get(color) ?? ''}M${x} ${y}h1v1h-1z`);
}));
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" role="img" aria-labelledby="title" shape-rendering="crispEdges"><title id="title">Axym Labs — A X Y M</title><desc>Four square white pixel letters over a clockwise-rotated MNIST-derived black and Axym-purple pixel field.</desc>${[...groups].map(([color, d]) => `<path fill="${color}" d="${d}"/>`).join('')}</svg>\n`;

function crc32(buffer) {
  let crc = 0xffffffff;
  for (const byte of buffer) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit++) crc = (crc >>> 1) ^ (0xedb88320 & -(crc & 1));
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function pngChunk(type, data) {
  const label = Buffer.from(type);
  const result = Buffer.alloc(data.length + 12);
  result.writeUInt32BE(data.length, 0);
  label.copy(result, 4);
  data.copy(result, 8);
  result.writeUInt32BE(crc32(Buffer.concat([label, data])), data.length + 8);
  return result;
}

function png(size) {
  const header = Buffer.alloc(13);
  header.writeUInt32BE(size, 0);
  header.writeUInt32BE(size, 4);
  header[8] = 8;
  header[9] = 2;
  const rows = Buffer.alloc(size * (size * 3 + 1));
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const source = grid[Math.floor(y * 32 / size)][Math.floor(x * 32 / size)];
      source.forEach((channel, c) => { rows[y * (size * 3 + 1) + 1 + x * 3 + c] = channel; });
    }
  }
  return Buffer.concat([Buffer.from('89504e470d0a1a0a', 'hex'), pngChunk('IHDR', header), pngChunk('IDAT', deflateSync(rows)), pngChunk('IEND', Buffer.alloc(0))]);
}

function ico() {
  const sizes = [16, 32, 48];
  const images = sizes.map(png);
  const header = Buffer.alloc(6 + 16 * sizes.length);
  header.writeUInt16LE(1, 2);
  header.writeUInt16LE(sizes.length, 4);
  let offset = header.length;
  sizes.forEach((size, i) => {
    const position = 6 + 16 * i;
    header[position] = size;
    header[position + 1] = size;
    header.writeUInt16LE(1, position + 4);
    header.writeUInt16LE(24, position + 6);
    header.writeUInt32LE(images[i].length, position + 8);
    header.writeUInt32LE(offset, position + 12);
    offset += images[i].length;
  });
  return Buffer.concat([header, ...images]);
}

const docsRoot = resolve(fileURLToPath(new URL('..', import.meta.url)));
const roots = process.argv.slice(2);
if (!roots.length) roots.push(docsRoot);
for (const root of roots) {
  const publicDirectory = resolve(root, 'public');
  mkdirSync(resolve(publicDirectory, 'brand'), { recursive: true });
  writeFileSync(resolve(publicDirectory, 'brand/axym-logo.svg'), svg);
  writeFileSync(resolve(publicDirectory, 'favicon.svg'), svg);
  writeFileSync(resolve(publicDirectory, 'favicon.ico'), ico());
  writeFileSync(resolve(publicDirectory, 'brand/axym-logo-192.png'), png(192));
  console.log(`Generated Axym SVG, 16/32/48px ICO, and 192px PNG in ${publicDirectory}`);
}
