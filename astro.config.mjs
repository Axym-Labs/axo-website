import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://axo.axym.org',
  output: 'static',
  trailingSlash: 'always',
  markdown: {
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      wrap: false,
    },
  },
});
