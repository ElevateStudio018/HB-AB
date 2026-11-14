// Samma kontroller som Elevate Studios djupanalys (worker/crawl.js, worker/sitecheck.js, assets/js/sitetest-deep.js)
const unescape = (s) => String(s || '').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;|&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').trim();

function analysePage(html) {
  const title = unescape((html.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1]);
  const desc = unescape((html.match(/<meta[^>]+name=["']description["'][^>]*content=["']([^"']*)["']/i) ||
    html.match(/<meta[^>]+content=["']([^"']*)["'][^>]+name=["']description["']/i) || [])[1]);
  const h1 = (html.match(/<h1[\s>]/gi) || []).length;
  const imgs = [...html.matchAll(/<img\b[^>]*>/gi)].map((m) => m[0]);
  const noAlt = imgs.filter((t) => !/\balt\s*=/i.test(t)).length;
  const hrefs = [...html.matchAll(/<a\b[^>]*\shref=["']([^"'#]+)["']/gi)].map((m) => m[1]);
  // a form that can be filled in: an e-mail or text field and a send button
  // the form must contain its own field and send button (buttons in the menu do not count)
  // a contact form has a message box or more than one field; the newsletter box in the footer has only an e-mail field
  const form = [...html.matchAll(/<form\b[\s\S]*?<\/form>/gi)].some((m) => {
    // the hidden trap field (name _honey) and buttons do not count
    const fields = (m[0].match(/<(input|textarea|select)\b(?![^>]*type=["'](hidden|submit|button)["'])(?![^>]*name=["']_honey["'])/gi) || []).length;
    return (/<textarea\b/i.test(m[0]) || fields >= 2) && /type=["']submit["']|<button\b/i.test(m[0]);
  });
  const attr = (name, re) => (html.match(re) || [])[1] || '';
  const lang = attr('lang', /<html[^>]*\blang=["']([^"']+)["']/i);
  const viewport = /<meta[^>]+name=["']viewport["']/i.test(html);
  const canonical = attr('canonical', /<link[^>]+rel=["']canonical["'][^>]*href=["']([^"']+)["']/i);
  const ogImage = /<meta[^>]+property=["']og:image["']/i.test(html);
  const noindex = /<meta[^>]+name=["']robots["'][^>]*noindex/i.test(html);
  const ldBlocks = [...html.matchAll(/<script[^>]+application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]);
  const ldBad = ldBlocks.filter((b) => { try { JSON.parse(b); return false; } catch { return true; } }).length;
  // http:// resources on a page that is https (mixed content)
  const mixed = [...html.matchAll(/(?:src|href)=["']http:\/\/[^"']+["']/gi)].length;
  return { title, titleLen: title.length, desc, descLen: desc.length, h1, imgs: imgs.length, noAlt, hrefs, form,
    lang, viewport, canonical, ogImage, noindex, ld: ldBlocks.length, ldBad, mixed };
}


function deepPage(html) {
  const f = {};
  f.doctype = /<!doctype html/i.test(html);
  f.charset = /<meta[^>]+charset/i.test(html);
  const heads = [...html.matchAll(/<h([1-6])\b[^>]*>([\s\S]*?)<\/h\1>/gi)];
  f.emptyHeadings = heads.filter((m) => !m[2].replace(/<[^>]+>/g, '').trim()).length;
  let skipped = 0, prev = 0;
  heads.forEach((m) => { const l = +m[1]; if (prev && l > prev + 1) skipped++; prev = l; });
  f.headingSkips = skipped;
  f.emptyLinks = [...html.matchAll(/<a\b([^>]*)>([\s\S]*?)<\/a>/gi)]
    .filter((m) => !m[2].replace(/<[^>]+>/g, '').trim() && !/aria-label=|title=|<img[^>]+alt=["'][^"']+/i.test(m[0])).length;
  f.emptyButtons = [...html.matchAll(/<button\b([^>]*)>([\s\S]*?)<\/button>/gi)]
    .filter((m) => !m[2].replace(/<[^>]+>/g, '').trim() && !/aria-label=/i.test(m[1])).length;
  f.genericLinks = [...html.matchAll(/<a\b[^>]*>([\s\S]*?)<\/a>/gi)]
    .filter((m) => /^(läs mer|klicka här|här|mer|läs mer här|se mer)\.?$/i.test(m[1].replace(/<[^>]+>/g, '').trim())).length;
  // a field is labelled if it sits inside a <label>, has aria-label, or a <label for> points at its id.
  // Honeypot fields (name _honey, aria-hidden) are for robots and do not count.
  const labelled = (html.match(/<label[\s\S]*?<\/label>/gi) || []).join('');
  f.unlabeledInputs = [...html.matchAll(/<input\b([^>]*)>/gi)]
    .filter((m) => !/type=["'](hidden|submit|button|checkbox|radio)["']/i.test(m[1]) && !/aria-label=|aria-hidden=["']true|name=["']_honey["']/i.test(m[1]) && !labelled.includes(m[0]) &&
      !(m[1].match(/\bid=["']([^"']+)["']/i) && new RegExp('for=["\']' + m[1].match(/\bid=["']([^"']+)["']/i)[1] + '["\']', 'i').test(html))).length;
  f.blankTarget = [...html.matchAll(/<a\b([^>]*target=["']_blank["'][^>]*)>/gi)].filter((m) => !/rel=["'][^"']*noopener/i.test(m[1])).length;
  f.deprecated = (html.match(/<(font|center|marquee|frameset|applet)\b/gi) || []).length;
  f.imgNoSize = [...html.matchAll(/<img\b[^>]*>/gi)].filter((m) => !/\bwidth=/i.test(m[0]) || !/\bheight=/i.test(m[0])).length;
  f.imgNoLazy = [...html.matchAll(/<img\b[^>]*>/gi)].filter((m) => !/loading=["']lazy["']/i.test(m[0]) && !/fetchpriority=["']high/i.test(m[0])).length;
  const head = (html.match(/<head[\s\S]*?<\/head>/i) || [''])[0];
  f.blockingScripts = [...head.matchAll(/<script\b([^>]*)>/gi)].filter((m) => /\bsrc=/i.test(m[1]) && !/\b(defer|async)\b/i.test(m[1])).length;
  f.bytes = html.length;
  f.inlineStyles = (html.match(/\sstyle=["']/gi) || []).length;
  f.inlineScripts = [...html.matchAll(/<script\b(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].filter((m) => m[1].trim()).length;
  f.metaRefresh = /<meta[^>]+http-equiv=["']refresh["']/i.test(html);
  f.hreflang = [...html.matchAll(/<link[^>]+hreflang=["']([^"']+)["']/gi)].map((m) => m[1]);
  f.ogComplete = /property=["']og:title["']/i.test(html) && /property=["']og:description["']/i.test(html) && /property=["']og:url["']/i.test(html);
  f.favicon = /rel=["'](icon|shortcut icon)["']/i.test(html);
  f.appleTouch = /rel=["']apple-touch-icon["']/i.test(html);
  // visible text, for thin pages and duplicate content
  const body = (html.match(/<body[\s\S]*?<\/body>/i) || [html])[0].replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ');
  const text = body.replace(/&[a-z#0-9]+;/gi, ' ').replace(/\s+/g, ' ').trim();
  f.words = text ? text.split(' ').length : 0;
  let hash = 0; for (let i = 0; i < text.length; i++) hash = (Math.imul(31, hash) + text.charCodeAt(i)) | 0;
  f.textHash = String(hash);
  // structured data types
  f.ldTypes = [];
  [...html.matchAll(/<script[^>]+application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi)].forEach((m) => {
    try {
      const walk = (x) => { if (Array.isArray(x)) x.forEach(walk); else if (x && typeof x === 'object') { if (x['@type']) [].concat(x['@type']).forEach((t) => f.ldTypes.push(String(t))); Object.values(x).forEach(walk); } };
      walk(JSON.parse(m[1]));
    } catch { /* counted as broken structured data */ }
  });
  return f;
}


const SEVERE = { 'seo|title-missing': 1, 'seo|h1-missing': 1, 'seo|noindex': 1, 'seo|robots-block': 1, 'practice|mixed': 1 };
const kb = (b) => Math.round(b / 1024) + ' KB';
const path = (u) => String(u).replace(/^https?:\/\/[^/]+/, '') || '/';
const base = process.argv[2].replace(/\/$/, '');
const sm = await (await fetch(base + '/sitemap.xml')).text().catch(() => '');
let urls = [...sm.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map((m) => m[1]);
if (process.argv[3]) urls = urls.map((u) => u.replace(process.argv[3], base + '/'));
if (process.env.URLS) urls = process.env.URLS.split(',').map((x) => base + x);
if (!urls.length) urls = [base + '/'];
const ok = [];
for (const url of urls) { const r = await fetch(url); const t = await r.text(); ok.push({ url, a: analysePage(t), d: deepPage(t) }); }
const F = {}; const pageBad = { seo: {}, access: {}, practice: {}, perf: {} };
const add = (cat, id, label, where) => { const k = cat + '|' + id; F[k] = F[k] || { label, where: [] }; F[k].where.push(where); };
ok.forEach(function (p) {
      var a = p.a, d = p.d, u = p.url, lab = path(u);
      // a serious fault costs the page 30 points, a small one 8; the score is the average over all pages
      var t = function (cat, id, label) { pageBad[cat][u] = (pageBad[cat][u] || 0) + (SEVERE[cat + '|' + id] ? 30 : 8); add(cat, id, label, lab); };
      if (!a.titleLen) t('seo', 'title-missing', 'Sidan saknar titel');
      if (a.titleLen > 60) t('seo', 'title-long', 'Titeln är för lång (över 60 tecken)');
      if (a.titleLen && a.titleLen < 25) t('seo', 'title-short', 'Titeln är för kort (under 25 tecken)');
      if (!a.descLen) t('seo', 'desc-missing', 'Saknar metabeskrivning');
      if (a.descLen > 160) t('seo', 'desc-long', 'Beskrivningen är för lång (över 160 tecken)');
      if (a.descLen && a.descLen < 70) t('seo', 'desc-short', 'Beskrivningen är för kort (under 70 tecken)');
      if (a.h1 === 0) t('seo', 'h1-missing', 'Saknar rubrik h1');
      if (a.h1 > 1) t('seo', 'h1-multi', 'Har flera rubriker h1');
      if (d.headingSkips) t('seo', 'heading-skip', 'Rubriknivåerna hoppar (till exempel h2 direkt till h4)');
      if (d.emptyHeadings) t('seo', 'heading-empty', 'Tomma rubriker');
      if (!a.canonical) t('seo', 'canonical', 'Saknar canonical-länk');
      if (!d.ogComplete) t('seo', 'og', 'Saknar fullständig information för delning i sociala medier (Open Graph)');
      if (a.noindex) t('seo', 'noindex', 'Markerad noindex, Google visar inte sidan');
      if (a.ldBad) t('seo', 'ld-bad', 'Strukturerad data (JSON-LD) är trasig, Google ignorerar den');
      if (d.genericLinks) t('seo', 'generic', 'Länktext som "läs mer" eller "klicka här"');
      if (d.words < 150) t('seo', 'thin', 'Tunn text, under 150 ord på sidan (' + d.words + ' ord)');
      if (d.metaRefresh) t('practice', 'refresh', 'Använder meta refresh för omdirigering');
      if (!a.lang) t('access', 'lang', 'Språket är inte angivet (lang)');
      if (!a.viewport) t('access', 'viewport', 'Saknar viewport, sidan skalas fel på mobil');
      if (a.noAlt) t('access', 'alt', 'Bilder saknar alt-text (' + a.noAlt + ' st)');
      if (d.emptyLinks) t('access', 'link-empty', 'Länkar utan text eller etikett');
      if (d.emptyButtons) t('access', 'button-empty', 'Knappar utan text eller etikett');
      if (d.unlabeledInputs) t('access', 'input-label', 'Fält utan etikett');
      if (!d.doctype) t('practice', 'doctype', 'Saknar doctype');
      if (!d.charset) t('practice', 'charset', 'Saknar teckenuppsättning (charset)');
      if (a.mixed) t('practice', 'mixed', 'Laddar innehåll över http i stället för https');
      if (d.blankTarget) t('practice', 'blank', 'Länk som öppnar ny flik utan rel="noopener" (' + d.blankTarget + ' st)');
      if (d.deprecated) t('practice', 'deprecated', 'Föråldrade HTML-taggar (font, center m.fl.)');
      if (d.blockingScripts) t('perf', 'blocking', 'Skript i sidhuvudet blockerar visningen (' + d.blockingScripts + ' st)');
      if (d.imgNoSize) t('perf', 'img-size', 'Bilder utan width och height (' + d.imgNoSize + ' st), ger layoutskift');
      if (d.bytes > 150 * 1024) t('perf', 'heavy', 'Stor HTML-fil (' + kb(d.bytes) + ')');
      if (d.inlineStyles > 200) t('perf', 'inline-styles', 'Många inline-stilar (' + d.inlineStyles + ')');
      if (d.inlineScripts > 5) t('perf', 'inline-scripts', 'Många inline-skript (' + d.inlineScripts + ')');
    });

const titles = {}, texts = {};
ok.forEach((p) => { if (p.a.title) (titles[p.a.title] ||= []).push(p.url); if (p.d.words >= 30) (texts[p.d.textHash] ||= []).push(p.url); });
Object.keys(titles).forEach((t) => { if (titles[t].length > 1) titles[t].forEach((u) => add('seo', 'dup-title', 'Samma titel på flera sidor', path(u))); });
Object.keys(texts).forEach((h) => { if (texts[h].length > 1) texts[h].forEach((u) => add('seo', 'dup-text', 'Samma innehåll på flera sidor', path(u))); });
const r404 = await fetch(base + '/finns-inte-' + Date.now()); if (r404.status !== 404) add('seo', 'soft404', 'Okänd adress svarar ' + r404.status, 'sajten');
const rob = await fetch(base + '/robots.txt'); if (rob.status !== 200) add('seo', 'robots', 'robots.txt saknas', 'sajten');
const pct = (cat) => { let lost = 0; Object.keys(pageBad[cat]).forEach((u) => lost += Math.min(100, pageBad[cat][u])); return Math.max(0, Math.round(100 - lost / ok.length)); };
console.log(JSON.stringify({ sidor: ok.length, betyg: { seo: pct('seo'), tillganglighet: pct('access'), praxis: pct('practice'), prestanda: pct('perf') }, fynd: Object.fromEntries(Object.entries(F).map(([k, v]) => [k, v.label + ' – ' + v.where.length + ' st: ' + v.where.slice(0, 6).join(', ')])) }, null, 1));
