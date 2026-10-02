# Axym mark

The mark places four smooth white Inter capitals in reading order across a
square: A/X above Y/M. The letter outlines use weight 650 and balanced optical
centers; they render independently of browser fonts. The capitals have room to
breathe and retain their shapes at favicon and navbar sizes.

Axym purple (`#3F21B6`) is the background’s base color. An enlarged,
clockwise-rotated MNIST handwritten eight and an offset reflection create an
interlaced pattern of dark purple and near-black shadows. A 24-cell texture
makes the interpolation visible without pixelating the lettering. Small corner
radii retain the square character of the mark.

Regenerate the exact same SVG, 16/32/48px favicon, and 192px PNG for both sites:

```sh
npm ci
node scripts/generate-brand.mjs /path/to/axo-website /path/to/axym-website
```

The SVG favicon and navbar mark are identical. Sharp (pinned in dev dependencies)
renders the PNGs with antialiasing. No font lookup or network access is needed
by the generator; it embeds the four outlines and 784 source image pixels.

Inter outlines come from `@fontsource-variable/inter` 5.3.0, Latin weight axis,
instantiated at 650 with fontTools. Copyright 2016 The Inter Project Authors,
licensed under SIL Open Font License 1.1. These four outlines are artwork,
not a redistributed font. Source: https://github.com/rsms/inter.

MNIST sample: test image 61 (zero-based), digit 8. Credit: Yann LeCun, Corinna
Cortes, and Christopher J. C. Burges. Source archive:
https://storage.googleapis.com/cvdf-datasets/mnist/t10k-images-idx3-ubyte.gz;
SHA-256 `8d422c7b0a1c1c79245a5bcf07fe86e33eeafee792b84584aec276f5a2dbc4e6`.
