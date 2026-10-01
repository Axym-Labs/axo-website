# Axym mark

The mark has original square A/X/Y/M pixel glyphs in reading order across four
quadrants. Its pixel field interpolates black and Axym purple (`#3F21B6`), using
an enlarged clockwise-rotated MNIST handwritten eight, an offset reflection,
and a low-amplitude deterministic stipple.

Regenerate the exact same SVG, 16/32/48-pixel favicon, and PNG for both sites:

```sh
node scripts/generate-brand.mjs /path/to/axo-website /path/to/axym-website
```

The generator embeds the 784 pixels needed for the mark and requires no network
access. The sample is MNIST test image 61 (zero-based), digit 8. Dataset credit:
Yann LeCun, Corinna Cortes, and Christopher J. C. Burges. Source archive:
https://storage.googleapis.com/cvdf-datasets/mnist/t10k-images-idx3-ubyte.gz;
SHA-256 `8d422c7b0a1c1c79245a5bcf07fe86e33eeafee792b84584aec276f5a2dbc4e6`.
Blacksmith's square-ended pixel typography informed the stroke style; its
wordmark or logo geometry is not reused.
