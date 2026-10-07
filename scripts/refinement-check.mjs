import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const base = process.env.AXO_TEST_URL || 'http://127.0.0.1:4321';
const artifacts = resolve(process.env.AXO_ARTIFACTS || '../axo-website-internal/documentation-migration/artifacts/refinement');
mkdirSync(artifacts, { recursive: true });
const browser = await chromium.launch({headless: true, ...(process.env.CHROMIUM_PATH ? {executablePath: process.env.CHROMIUM_PATH} : {})});
const context = await browser.newContext({viewport: {width: 1440, height: 1050}, colorScheme: 'light'});
const page = await context.newPage();
const errors = [];
page.on('pageerror', error => errors.push(error.message));
const results = [];
try {
  await page.goto(base + '/', {waitUntil: 'networkidle'});
  await page.evaluate(() => document.fonts.ready);
  assert.equal(await page.locator('.site-navbar').count(), 1, 'Documentation needs one full-width navbar');
  const navbar = await page.locator('.site-navbar').boundingBox();
  assert.equal(navbar.x, 0);
  assert.equal(navbar.width, 1440);
  assert(await page.locator('.site-navbar .theme-toggle').isVisible());
  assert.equal(await page.locator('.site-navbar a.source-code').innerText(), 'Source Code');
  assert.equal(await page.locator('.site-navbar a.source-code').getAttribute('href'), 'https://github.com/Axym-Labs/axosim');
  assert.equal(await page.locator('.site-navbar img').count(), 0, 'Navbar must remain text-only');
  const firstGroup = page.locator('.nav-group').first();
  assert.equal(await firstGroup.locator('h2').count(), 0, 'Getting-started links should not have a category heading');
  assert(await firstGroup.locator('a[href="/models/"]').isVisible());
  assert.equal(await firstGroup.locator('a.demo-link').getAttribute('href'), 'https://axym.org/work/axosim-fly-geometry/');
  assert.equal(await page.locator('.resource-links a').filter({hasText: 'Demo'}).getAttribute('href'), 'https://axym.org/work/axosim-fly-geometry/');
  results.push('Full-width navbar, right-side source/theme controls, unheaded start links, model selection and published demo.');

  const compatibility = page.locator('.api-group').filter({has: page.locator('summary', {hasText: /^Compatibility$/})});
  assert.equal(await compatibility.count(), 1);
  assert(!(await compatibility.locator('a[href="/api/model/"]').isVisible()));
  await compatibility.locator('summary').focus();
  await page.keyboard.press('Enter');
  assert(await compatibility.locator('a[href="/api/model/"]').isVisible());
  await compatibility.locator('a[href="/api/neuronio/"]').click();
  await page.waitForURL(base + '/api/neuronio/');
  assert(await page.locator('.api-group[open]').filter({has: page.locator('summary', {hasText: /^Compatibility$/})}).count());
  assert.equal(await page.locator('.api-group .api-group').count(), 0, 'API navigation should be exactly one level deep');
  assert(await page.locator('.api-symbol').count() > 0, 'API pages should have symbol-oriented contracts');
  assert(await page.locator('.api-signature').count() > 0);
  assert.equal(await page.locator('.api-signature pre code').first().evaluate(el => getComputedStyle(el).whiteSpace), 'pre-wrap', 'Reference signatures should wrap instead of hiding arguments offscreen');
  await page.screenshot({path: join(artifacts, 'api-desktop-dark.png'), fullPage: false});
  results.push('API groups expand by keyboard, current subgroup opens after navigation, and symbol contracts are structured.');

  await page.goto(base + '/models/', {waitUntil: 'networkidle'});
  const cards = page.locator('.model-card');
  assert.equal(await cards.count(), 3);
  const cardBoxes = await cards.evaluateAll(nodes => nodes.map(node => {const r = node.getBoundingClientRect(); return {x: r.x, y: r.y, width: r.width};}));
  assert.equal(cardBoxes[0].y, cardBoxes[1].y);
  assert.equal(cardBoxes[1].y, cardBoxes[2].y);
  for (const hero of await page.locator('.model-art').all()) {
    assert.equal(await hero.evaluate(el => getComputedStyle(el).color), 'rgb(255, 255, 255)');
    assert(await hero.evaluate(el => getComputedStyle(el).backgroundImage !== 'none'));
  }
  assert(await page.locator('.model-card code').count() >= 5, 'Catalog should show actual model IDs and API entry points');
  await page.screenshot({path: join(artifacts, 'models-desktop-dark.png'), fullPage: true});
  await page.locator('.theme-toggle').click();
  await page.waitForTimeout(200);
  await page.screenshot({path: join(artifacts, 'models-desktop-light.png'), fullPage: true});
  results.push('Three-column illustrated model catalog with real model IDs, API guidance, and light/dark styling.');

  await page.goto(base + '/', {waitUntil: 'networkidle'});
  assert.equal(await page.locator('.overview-figure figcaption').count(), 0, 'Caption should be normal prose outside the graphic');
  assert(await page.locator('.figure-caption').innerText().then(text => text.includes('technical report')));
  for (const [theme, expected] of [['light', 'central-comparison.svg'], ['dark', 'central-comparison-dark.svg']]) {
    if (await page.locator('html').getAttribute('data-theme') !== theme) await page.locator('.theme-toggle').click();
    await page.waitForTimeout(200);
    const visibleImage = page.locator('.overview-figure img:visible');
    assert.equal(await visibleImage.count(), 1);
    assert((await visibleImage.getAttribute('src')).endsWith(expected));
    assert(await visibleImage.evaluate(img => img.naturalWidth > 0));
    await page.screenshot({path: join(artifacts, `overview-desktop-${theme}.png`), fullPage: false});
  }
  assert((await page.locator('.prose').innerText()).includes('Jonathan Schäfer'));
  results.push('Correct light/dark radar assets, normal-text caption, and consistent coauthor citation.');

  await page.goto(base + '/troubleshooting/', {waitUntil: 'networkidle'});
  const issueSections = await page.locator('.prose h2').count();
  assert(await page.locator('.error-callout').count() >= issueSections, 'Each issue needs its own error-template callout');
  for (const callout of await page.locator('.error-callout').all()) {
    assert.equal(await callout.locator('li').count(), 0);
    assert(await callout.locator('code').count() > 0);
  }
  await page.screenshot({path: join(artifacts, 'troubleshooting-desktop-dark.png'), fullPage: true});
  results.push('Troubleshooting uses separate highlighted error-template callouts.');

  for (const width of [768, 390, 320]) {
    await page.setViewportSize({width, height: 1000});
    await page.goto(base + '/models/', {waitUntil: 'networkidle'});
    assert(await page.locator('.site-navbar .theme-toggle').isVisible());
    assert(await page.locator('.site-navbar .labs-link').isVisible(), 'Keep the Axym link available on mobile');
    assert(!(await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)));
    await page.screenshot({path: join(artifacts, `models-${width}-dark.png`), fullPage: true});
    await page.goto(base + '/', {waitUntil: 'networkidle'});
    assert(!(await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)));
    await page.screenshot({path: join(artifacts, `overview-${width}-dark.png`), fullPage: false});
  }
  assert.equal(errors.length, 0, errors.join('\n'));
  writeFileSync(join(artifacts, 'refinement-verification.json'), JSON.stringify({base, results, errors}, null, 2) + '\n');
  console.log(results.join('\n'));
} finally {
  await browser.close();
}
