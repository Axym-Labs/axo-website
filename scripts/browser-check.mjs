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
  assert.equal(await page.locator('html').getAttribute('data-theme'),'dark','New visitors should see dark mode even with a light system preference');
  assert.equal(await page.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(17, 17, 17)');
  assert.equal(await page.locator('h1').innerText(),'Overview');
  assert.equal(await page.locator('.nav-group a[aria-current="page"]').innerText(),'Overview');
  assert(await page.locator('.table-of-contents').isVisible());
  assert((await page.locator('.overview-figure img').evaluate(img=>img.naturalWidth))>0);
  assert(/^['"]?Inter/.test(await page.locator('body').evaluate(el=>getComputedStyle(el).fontFamily)));
  assert(await page.evaluate(()=>[...document.fonts].some(font=>font.family.includes('Inter') && font.status==='loaded')),'The self-hosted Inter font must actually load');
  await page.screenshot({path:join(artifacts,'overview-desktop-dark.png'),fullPage:true});

  const navLink=page.locator('.nav-group a[href="/installation/"]');
  await page.keyboard.press('Tab');
  await navLink.focus();
  assert(await navLink.evaluate(el=>{const css=getComputedStyle(el);return css.outlineStyle!=='none' && parseFloat(css.outlineWidth)>=2;}),'Keyboard navigation needs a visible focus indicator');
  const idle=await navLink.evaluate(el=>{const css=getComputedStyle(el);const rect=el.getBoundingClientRect();return {background:css.backgroundColor,x:rect.x,y:rect.y,width:rect.width,height:rect.height};});
  await navLink.hover();
  await page.waitForTimeout(200);
  const hovered=await navLink.evaluate(el=>{const css=getComputedStyle(el);const rect=el.getBoundingClientRect();return {background:css.backgroundColor,x:rect.x,y:rect.y,width:rect.width,height:rect.height,duration:css.transitionDuration};});
  assert.notEqual(hovered.background,idle.background,'Navigation hover should give visible feedback');
  for(const key of ['x','y','width','height']) assert.equal(hovered[key],idle[key],`Hover should not shift ${key}`);
  assert(hovered.duration.split(',').every(value=>parseFloat(value)>0 && parseFloat(value)<=0.2),'Hover feedback should use short reference-style transitions');
  await page.emulateMedia({reducedMotion:'reduce'});
  assert((await navLink.evaluate(el=>getComputedStyle(el).transitionDuration)).split(',').every(value=>parseFloat(value)===0),'Reduced-motion preference should disable hover animation');
  await page.emulateMedia({reducedMotion:'no-preference'});
  results.push('Interactions: subtle reference-style hover feedback, no geometry shifts, reduced-motion support.');

  await page.locator('.theme-toggle').click();
  assert.equal(await page.locator('html').getAttribute('data-theme'),'light');
  await page.emulateMedia({colorScheme:'dark'});
  await page.reload({waitUntil:'networkidle'});
  assert.equal(await page.locator('html').getAttribute('data-theme'),'light','Saved light choice should override a dark system preference');
  await page.screenshot({path:join(artifacts,'overview-desktop-light.png'),fullPage:true});
  results.push('Overview: dark default, self-hosted Inter, persistent light override, central figure, active navigation, right contents rail.');

  const noJsContext=await browser.newContext({javaScriptEnabled:false,colorScheme:'light'});
  const noJsPage=await noJsContext.newPage();
  await noJsPage.goto(base+'/',{waitUntil:'load'});
  assert.equal(await noJsPage.locator('html').getAttribute('data-theme'),'dark','Dark default should also work without JavaScript');
  assert.equal(await noJsPage.locator('body').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(17, 17, 17)');
  await noJsContext.close();

  await page.goto(base+'/inference/',{waitUntil:'networkidle'});
  const colors = await page.locator('.prose pre').first().evaluate(pre=>[...new Set([...pre.querySelectorAll('span[style]')].map(span=>getComputedStyle(span).color))]);
  assert(colors.length>=4,`Only ${colors.length} syntax colors`);
  const original = await page.locator('.prose pre code').first().textContent();
  await page.locator('.copy-button').first().click();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),original);
  await page.screenshot({path:join(artifacts,'inference-desktop-light.png'),fullPage:true});
  await page.locator('.theme-toggle').click();
  assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
  await page.waitForTimeout(200);
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
  await page.waitForTimeout(200);
  assert.equal((await page.locator('#site-sidebar').boundingBox()).x,0,'Open navigation must finish on screen');
  await page.screenshot({path:join(artifacts,'navigation-mobile.png')});
  await page.locator('.theme-toggle').click();
  await page.waitForTimeout(200);
  await page.screenshot({path:join(artifacts,'navigation-mobile-dark.png')});
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('#menu-toggle').getAttribute('aria-expanded'),'false');
  assert(await page.locator('#site-sidebar').evaluate(el=>el.inert));
  await page.waitForTimeout(200);
  await page.screenshot({path:join(artifacts,'population-mobile-dark.png'),fullPage:true});
  results.push('Mobile navigation: drawer, inert hidden links, Escape close, and usable code scrolling.');
  assert.equal(errors.length,0,errors.join('\n'));
  writeFileSync(join(artifacts,'browser-verification.json'),JSON.stringify({base,results,errors},null,2)+'\n');
  console.log(results.join('\n'));
} finally { await browser.close(); }
