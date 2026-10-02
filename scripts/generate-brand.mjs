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

// Original square glyphs: each segment is rasterized at exactly one native
// pixel in the 32 × 32 mark, with a 14 × 14-pixel quadrant interior.
const letterPaths = [
  [[[1, 13], [1, 3], [4, 0], [9, 0], [12, 3], [12, 13]], [[1, 7], [12, 7]]],
  [[[0, 0], [13, 13]], [[13, 0], [0, 13]]],
  [[[0, 0], [6, 6], [13, 0]], [[6, 6], [6, 13]]],
  [[[0, 13], [0, 0], [6, 6], [13, 0], [13, 13]]],
];
function pixelLine(mask, start, end) {
  let [x, y] = start;
  const [endX, endY] = end;
  const dx = Math.abs(endX - x), dy = -Math.abs(endY - y);
  const stepX = x < endX ? 1 : -1, stepY = y < endY ? 1 : -1;
  let error = dx + dy;
  for (;;) {
    mask[y][x] = true;
    if (x === endX && y === endY) break;
    const twiceError = 2 * error;
    if (twiceError >= dy) { error += dy; x += stepX; }
    if (twiceError <= dx) { error += dx; y += stepY; }
  }
}
const glyphs = letterPaths.map(paths => {
  const mask = Array.from({ length: 14 }, () => Array(14).fill(false));
  for (const path of paths) {
    for (let i = 1; i < path.length; i++) pixelLine(mask, path[i - 1], path[i]);
  }
  return mask;
});

function ink(x, y) {
  const sx = Math.max(0, Math.min(27, Math.round(x)));
  const sy = Math.max(0, Math.min(27, Math.round(y)));
  return sample[sy * 28 + sx] / 255;
}

// Clockwise rotation, 2× enlargement, plus an offset reflection of the same sample.
// Deterministic pixel stipple extends the rotated digit into its margins.
// A gamma lift makes most of the black–purple interpolation visibly purple.
function field(x, y) {
  const first = ink(6 + y / 2, 22 - x / 2);
  const second = ink(21 - y / 1.8, 6 + x / 1.8);
  const stipple = ((x * 73 + y * 151 + x * y * 29) % 101) / 101;
  const pattern = Math.min(1, 0.50 * first + 0.30 * second + 0.20 * stipple);
  return 0.15 + 0.85 * Math.pow(pattern, 0.35);
}

const grid = Array.from({ length: 32 }, (_, y) => Array.from({ length: 32 }, (_, x) => {
  const quadrant = Math.floor(y / 16) * 2 + Math.floor(x / 16);
  const gx = (x % 16) - 1;
  const gy = (y % 16) - 1;
  if (gx >= 0 && gx < 14 && gy >= 0 && gy < 14 && glyphs[quadrant][gy][gx]) {
    return [255, 255, 255];
  }
  return [63, 33, 182].map(channel => Math.round(channel * field(x, y)));
}));

const groups = new Map();
grid.forEach((row, y) => row.forEach((rgb, x) => {
  const color = `#${rgb.map(channel => channel.toString(16).padStart(2, '0')).join('')}`;
  groups.set(color, `${groups.get(color) ?? ''}M${x} ${y}h1v1h-1z`);
}));
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" role="img" aria-labelledby="title" shape-rendering="crispEdges"><title id="title">Axym Labs — A X Y M</title><desc>Four square white letters with one-pixel strokes over a purple-biased, a clockwise-rotated MNIST-derived black and Axym-purple pixel field.</desc>${[...groups].map(([color, d]) => `<path fill="${color}" d="${d}"/>`).join('')}</svg>\n`;

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
  // At 16px, rasterize the same paths on its own grid; decimating 32px
  // would erase odd-column one-pixel stems in the favicon.
  let sourceGrid = grid;
  if (size === 16) {
    const smallGlyphs = letterPaths.map(paths => {
      const mask = Array.from({ length: 7 }, () => Array(7).fill(false));
      for (const path of paths) {
        const scaled = path.map(point => point.map(value => Math.round(value * 6 / 13)));
        for (let i = 1; i < scaled.length; i++) pixelLine(mask, scaled[i - 1], scaled[i]);
      }
      return mask;
    });
    sourceGrid = Array.from({ length: 16 }, (_, y) => Array.from({ length: 16 }, (_, x) => {
      const quadrant = Math.floor(y / 8) * 2 + Math.floor(x / 8);
      const gx = x % 8, gy = y % 8;
      if (gx < 7 && gy < 7 && smallGlyphs[quadrant][gy][gx]) return [255, 255, 255];
      return [63, 33, 182].map(channel => Math.round(channel * field(x * 2, y * 2)));
    }));
  }
  const header = Buffer.alloc(13);
  header.writeUInt32BE(size, 0);
  header.writeUInt32BE(size, 4);
  header[8] = 8;
  header[9] = 2;
  const rows = Buffer.alloc(size * (size * 3 + 1));
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const source = sourceGrid[Math.floor(y * sourceGrid.length / size)][Math.floor(x * sourceGrid.length / size)];
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
