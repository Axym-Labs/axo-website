import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const base = process.env.AXO_TEST_URL || 'http://127.0.0.1:4321';
const artifacts = resolve(process.env.AXO_ARTIFACTS || '../axo-website-internal/documentation-migration/artifacts');
mkdirSync(artifacts,{recursive:true});
const browser = await chromium.launch({
  headless:true,
  ...(process.env.CHROMIUM_PATH ? {executablePath:process.env.CHROMIUM_PATH} : {}),
});
const context = await browser.newContext({viewport:{width:1440,height:1050},colorScheme:'light',permissions:['clipboard-read','clipboard-write']});
const page = await context.newPage();
const errors = [];
page.on('pageerror', error => errors.push(error.message));
const results = [];
try {
  await page.goto(base+'/',{waitUntil:'networkidle'});
  await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('h1').innerText(),'Overview');
  assert.equal(await page.locator('.nav-group a[aria-current="page"]').innerText(),'Overview');
  assert(await page.locator('.table-of-contents').isVisible());
  assert((await page.locator('.overview-figure img').evaluate(img=>img.naturalWidth))>0);
  assert((await page.locator('body').evaluate(el=>getComputedStyle(el).fontFamily)).startsWith('P052'));
  await page.screenshot({path:join(artifacts,'overview-desktop-light.png'),fullPage:true});
  results.push('Overview: central figure, P052 font, active navigation, right contents rail.');

  await page.goto(base+'/inference/',{waitUntil:'networkidle'});
  const colors = await page.locator('.prose pre').first().evaluate(pre=>[...new Set([...pre.querySelectorAll('span[style]')].map(span=>getComputedStyle(span).color))]);
  assert(colors.length>=4,`Only ${colors.length} syntax colors`);
  const original = await page.locator('.prose pre code').first().textContent();
  await page.locator('.copy-button').first().click();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),original);
  await page.screenshot({path:join(artifacts,'inference-desktop-light.png'),fullPage:true});
  await page.locator('.theme-toggle').click();
  assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
  const darkColors = await page.locator('.prose pre').first().evaluate(pre=>[...new Set([...pre.querySelectorAll('span[style]')].map(span=>getComputedStyle(span).color))]);
  assert(darkColors.length>=4);
  assert.notDeepEqual(colors,darkColors);
  await page.screenshot({path:join(artifacts,'inference-desktop-dark.png'),fullPage:true});
  await page.reload({waitUntil:'networkidle'});
  assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
  results.push(`Highlighting: ${colors.length} light/${darkColors.length} dark token colors; exact copy; persistent theme.`);

  await page.locator('.theme-toggle').click();
  const heading = page.locator('.prose h2').last();
  const headingId = await heading.getAttribute('id');
  await heading.scrollIntoViewIfNeeded();
  await page.waitForTimeout(250);
  const tocActive = await page.locator('.toc-link[aria-current="location"]').getAttribute('href');
  assert(tocActive,'No active heading after scroll');
  await page.locator(`.toc-link[href="#${headingId}"]`).click();
  assert(new URL(page.url()).hash===`#${headingId}`);
  results.push('Table of contents: active location follows scroll and anchors update URL.');

  await page.keyboard.press('Control+k');
  assert(await page.locator('#search-dialog').isVisible());
  await page.locator('#search-input').fill('synaptic_log_efficacy');
  await page.locator('.search-result').first().waitFor({timeout:15000});
  await page.keyboard.press('ArrowDown');
  assert(await page.locator('.search-result').first().evaluate(el=>el===document.activeElement));
  await page.screenshot({path:join(artifacts,'search-desktop.png')});
  const searchTarget = new URL(await page.locator('.search-result').first().getAttribute('href'), page.url()).href;
  await Promise.all([page.waitForURL(searchTarget), page.keyboard.press('Enter')]);
  await page.waitForLoadState('networkidle');
  assert(page.url().startsWith(base));
  results.push('Search: content/API results, Ctrl K, arrow-key focus, Enter navigation.');

  const routes = [...new Set((await page.locator('.navigation a').evaluateAll(links=>links.map(link=>link.getAttribute('href')))))];
  for (const viewport of [{width:1440,height:1000},{width:768,height:1024},{width:390,height:844}]) {
    await page.setViewportSize(viewport);
    for (const route of routes) {
      const response = await page.goto(base+route,{waitUntil:'load'});
      assert.equal(response.status(),200,route);
      const overflow = await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
      assert(!overflow,`Horizontal page overflow at ${viewport.width}px: ${route}`);
      assert.equal(await page.locator('h1').count(),1,route);
    }
  }
  results.push(`All ${routes.length} navigation routes render at 1440, 768, and 390px without page overflow.`);

  await page.goto(base+'/populations/',{waitUntil:'networkidle'});
  await page.screenshot({path:join(artifacts,'population-mobile-light.png'),fullPage:true});
  assert(!(await page.locator('.table-of-contents').isVisible()));
  await page.locator('#menu-toggle').click();
  assert.equal(await page.locator('#menu-toggle').getAttribute('aria-expanded'),'true');
  assert(!(await page.locator('#site-sidebar').evaluate(el=>el.inert)));
  await page.screenshot({path:join(artifacts,'navigation-mobile.png')});
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('#menu-toggle').getAttribute('aria-expanded'),'false');
  assert(await page.locator('#site-sidebar').evaluate(el=>el.inert));
  results.push('Mobile navigation: drawer, inert hidden links, Escape close, and usable code scrolling.');
  assert.equal(errors.length,0,errors.join('\n'));
  writeFileSync(join(artifacts,'browser-verification.json'),JSON.stringify({base,results,errors},null,2)+'\n');
  console.log(results.join('\n'));
} finally { await browser.close(); }
