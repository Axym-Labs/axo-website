# AxoSim documentation

Documentation for AxoSim at **https://axo.axym.org**. The site uses Astro,
static Markdown pages, Shiki highlighting, and Pagefind search. Self-hosted Inter
and Axym purple match the Axym website. Dark mode is the default; explicit theme
choices persist. Subtle hover transitions follow the reference documentation
and respect reduced-motion preferences.

The documentation order follows installation, model selection, inference and
training, population construction, inference-time adaptation, evaluation and
deployment, then the complete API reference. The technical report's former
practitioner part has moved here.

## Develop and verify

Use Node 22.12+ and npm 9.6.5+:

```sh
npm ci
npm run dev
```

Build complete static routes and a search index, then verify every internal
link, anchor, canonical URL, highlighted code block, and required asset:

```sh
npm run check
npm run build
npm run preview
```

Search is indexed during the production build. Test it through `preview`.
The browser verification checks search, keyboard interaction, theme persistence,
code copy, the section indicator, and every navigation route at desktop,
tablet, and mobile widths:

```sh
npx playwright install chromium
npm run test:browser
```

Browser verification stores screenshots in the sibling internal project by
default. Set `AXO_ARTIFACTS` for another output directory, `AXO_TEST_URL` for
another server, and `CHROMIUM_PATH` to reuse a local Chromium installation.

## Maintain the documentation

Edit lifecycle guides in `src/content/docs/`. Frontmatter specifies the page
title, description, navigation category, and explicit order. The navigation,
previous/next links, table of contents, and sitemap use this metadata. API
reference is deliberately the final category.

API pages are generated from a pinned AxoSim revision. They cover every
`axosim.__all__` export, the public functions/classes/methods in the guide
modules, dataclass defaults, and every declared command-line option. The
generator includes hand-maintained explanations of shape, state, and adaptation
contracts. It parses source without importing PyTorch:

```sh
python scripts/generate-api.py --source ../AxoSim
```

The generator's `--help` lists its exact options. The public
`api-inventory.json` records symbol and CLI coverage. Inherited PyTorch methods
use PyTorch's normal interface rather than duplicated framework documentation.

To refresh the downloadable report and export its original TikZ central figure
as SVG and PNG, install Tectonic and Poppler, rebuild the sibling report, and run:

```sh
npm run sync:report
```

`public/report/provenance.json` records the source and output hashes. Normal
website builds use checked-in assets and need neither TeX nor private repositories.

## GitHub Pages and the custom domain

The repository is **Axym-Labs/axo-website**. Internal requirements, migration
audits, original report documentation, and screenshots are kept in the private
**Axym-Labs/axo-website-internal** repository.

The workflow builds and indexes the site on pushes to `main`, uploads the static
artifact, and deploys through GitHub Pages. This follows the Axym website's
build-and-publish arrangement, using GitHub's current Pages actions and
temporary workflow credentials. No copied personal-token secret is needed.

1. Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**.
2. Add **axo.axym.org** as the custom domain. `public/CNAME` records the same domain.
3. In the DNS service for **axym.org**, add a CNAME with name **axo** and target
   **Axym-Labs.github.io**. Leave the apex and existing subdomains unchanged.
4. Run the deployment workflow, wait for GitHub's domain check and certificate,
   and enable **Enforce HTTPS** when available.
5. Verify the home page, a nested guide, `/api/`, search, fonts, and the report at
   **https://axo.axym.org**.

The AxoSim and AxoBench source repositories currently require repository access.
Their visibility is independent of this public documentation repository. The
guides state that installation prerequisite rather than implying a PyPI release.
