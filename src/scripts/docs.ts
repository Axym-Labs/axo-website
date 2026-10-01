const root = document.documentElement;
const themeButtons = document.querySelectorAll<HTMLButtonElement>('.theme-toggle');
function updateThemeLabel() {
  const dark = root.dataset.theme === 'dark';
  themeButtons.forEach(button => button.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} mode`));
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', dark ? '#111111' : '#ffffff');
}
updateThemeLabel();
themeButtons.forEach(button => button.addEventListener('click', () => {
  root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem('axo-theme', root.dataset.theme); } catch {}
  updateThemeLabel();
}));

const sidebar = document.querySelector<HTMLElement>('.sidebar')!;
const menuButton = document.querySelector<HTMLButtonElement>('#menu-toggle')!;
const mobile = matchMedia('(max-width: 900px)');
function closeMenu() {
  root.classList.remove('menu-open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open navigation');
  sidebar.inert = mobile.matches;
  document.querySelector<HTMLElement>('.reading-layout')!.inert = false;
}
closeMenu();
mobile.addEventListener('change', closeMenu);
menuButton.addEventListener('click', () => {
  const open = !root.classList.contains('menu-open');
  root.classList.toggle('menu-open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  sidebar.inert = !open;
  document.querySelector<HTMLElement>('.reading-layout')!.inert = open;
  if (open) sidebar.querySelector<HTMLAnchorElement>('[aria-current="page"]')?.focus();
});
document.querySelector('.sidebar-scrim')?.addEventListener('click', closeMenu);
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && root.classList.contains('menu-open')) {
    closeMenu();
    menuButton.focus();
  }
  if (event.key === 'Tab' && root.classList.contains('menu-open')) {
    const controls = [...sidebar.querySelectorAll<HTMLElement>('a,button')];
    const first = controls[0];
    const last = controls.at(-1)!;
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }
});

document.querySelectorAll<HTMLPreElement>('.prose pre').forEach(pre => {
  const wrapper = document.createElement('div');
  wrapper.className = 'code-example';
  pre.before(wrapper);
  wrapper.append(pre);
  const header = document.createElement('div');
  header.className = 'code-header';
  const language = document.createElement('span');
  const languageName = pre.dataset.language || pre.querySelector('code')?.className.replace('language-', '') || 'Code';
  language.textContent = ({ python: 'Python', bash: 'Shell', shell: 'Shell', json: 'JSON', text: 'Output' } as Record<string, string>)[languageName] || languageName;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'copy-button';
  button.setAttribute('aria-label', `Copy ${language.textContent} code`);
  button.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M15 8V4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h4"/></svg><span>Copy</span>';
  const status = document.createElement('span');
  status.className = 'visually-hidden';
  status.setAttribute('aria-live', 'polite');
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(pre.querySelector('code')?.textContent || pre.textContent || '');
      button.querySelector('span')!.textContent = 'Copied';
      status.textContent = 'Code copied to clipboard.';
      setTimeout(() => { button.querySelector('span')!.textContent = 'Copy'; status.textContent = ''; }, 2000);
    } catch {
      status.textContent = 'Copy unavailable. Select the code and copy it manually.';
    }
  });
  header.append(language, button, status);
  wrapper.prepend(header);
  pre.tabIndex = 0;
});

const tocLinks = [...document.querySelectorAll<HTMLAnchorElement>('.toc-link')];
const sections = tocLinks.map(link => document.getElementById(decodeURIComponent(link.hash.slice(1)))).filter((element): element is HTMLElement => !!element);
function setActiveHeading() {
  let active = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= 120) active = section;
  }
  tocLinks.forEach(link => {
    if (link.hash.slice(1) === active?.id) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}
let scheduled = false;
window.addEventListener('scroll', () => {
  if (scheduled) return;
  scheduled = true;
  requestAnimationFrame(() => { setActiveHeading(); scheduled = false; });
}, { passive: true });
setActiveHeading();

interface SearchResult { url: string; meta: { title?: string }; excerpt: string }
interface SearchIndex { search: (query: string) => Promise<{ results: { data: () => Promise<SearchResult> }[] }> }
const dialog = document.querySelector<HTMLDialogElement>('#search-dialog')!;
const searchInput = document.querySelector<HTMLInputElement>('#search-input')!;
const searchResults = document.querySelector<HTMLElement>('#search-results')!;
const searchStatus = document.querySelector<HTMLElement>('#search-status')!;
let searchIndex: Promise<SearchIndex> | undefined;
let queryVersion = 0;
let timer: ReturnType<typeof setTimeout>;
let searchOpener: HTMLElement | null;
function openSearch() {
  searchOpener = document.activeElement as HTMLElement;
  dialog.showModal();
  searchInput.focus();
}
document.querySelectorAll('.search-trigger').forEach(button => button.addEventListener('click', openSearch));
document.querySelector('#search-close')?.addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => searchOpener?.focus());
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
document.addEventListener('keydown', event => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    if (dialog.open) dialog.close(); else openSearch();
  }
});
searchInput.addEventListener('input', () => {
  clearTimeout(timer);
  const version = ++queryVersion;
  const query = searchInput.value.trim();
  if (!query) {
    searchResults.replaceChildren();
    searchStatus.textContent = 'Search guides, examples, and API signatures.';
    return;
  }
  timer = setTimeout(async () => {
    searchStatus.textContent = 'Searching…';
    try {
      const modulePath = '/pagefind/pagefind.js';
      searchIndex ??= import(/* @vite-ignore */ modulePath) as Promise<SearchIndex>;
      const index = await searchIndex;
      const response = await index.search(query);
      const results = await Promise.all(response.results.slice(0, 12).map(result => result.data()));
      if (version !== queryVersion) return;
      searchResults.replaceChildren();
      searchStatus.textContent = results.length ? `${response.results.length} results` : 'No results. Try a model name, method, or parameter.';
      for (const result of results) {
        const link = document.createElement('a');
        link.className = 'search-result';
        link.href = result.url;
        const title = document.createElement('strong');
        title.textContent = result.meta.title || result.url;
        const excerpt = document.createElement('span');
        // Pagefind only emits mark tags. Strip all markup before inserting as text.
        excerpt.textContent = result.excerpt.replace(/<[^>]*>/g, '');
        link.append(title, excerpt);
        searchResults.append(link);
      }
    } catch {
      if (version === queryVersion) searchStatus.textContent = 'Search is unavailable. Use the page navigation or try again after reloading.';
    }
  }, 150);
});
dialog.addEventListener('keydown', event => {
  const results = [...searchResults.querySelectorAll<HTMLAnchorElement>('a')];
  const focused = results.indexOf(document.activeElement as HTMLAnchorElement);
  if (event.key === 'ArrowDown' && results.length) {
    event.preventDefault(); results[Math.min(focused + 1, results.length - 1)].focus();
  } else if (event.key === 'ArrowUp' && results.length) {
    event.preventDefault(); if (focused <= 0) searchInput.focus(); else results[focused - 1].focus();
  } else if (event.key === 'Enter' && document.activeElement === searchInput && results.length) {
    event.preventDefault(); results[0].click();
  }
});

if (/Macintosh|iPhone|iPad/.test(navigator.userAgent)) {
  document.querySelectorAll('.search-trigger kbd').forEach(element => element.textContent = '⌘ K');
}
