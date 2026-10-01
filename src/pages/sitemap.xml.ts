import { getCollection } from 'astro:content';

export async function GET() {
  const entries = await getCollection('docs');
  const urls = entries.map(entry => {
    const path = entry.id === 'overview' ? '/' : entry.id === 'api/index' ? '/api/' : `/${entry.id}/`;
    return `<url><loc>https://axo.axym.org${path}</loc></url>`;
  }).join('');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${urls}</urlset>`, {
    headers: { 'Content-Type': 'application/xml' },
  });
}
