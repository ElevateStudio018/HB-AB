// Rensar den inbyggda CSS:en per sida (<style data-sida>), så att varje sida bara har de regler den använder.
// Anropas av scripts/seo.py:  node scripts/rensa-css.mjs docs
import { PurgeCSS } from 'purgecss';
import { transform } from 'lightningcss';
import fs from 'fs';
import path from 'path';

const root = process.argv[2];
const js = ['assets/sajt.js', 'assets/hb.js', 'assets/offert.js'].map((f) => path.join(root, f)).filter(fs.existsSync).map((f) => fs.readFileSync(f, 'utf8')).join('\n');
const sidor = [];
(function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); if (fs.statSync(p).isDirectory()) { if (f !== 'forslag') walk(p); } else if (f.endsWith('.html')) sidor.push(p); } })(root);
for (const p of sidor) {
  const doc = fs.readFileSync(p, 'utf8');
  const m = doc.match(/<style data-sida>([\s\S]*?)<\/style>/);
  if (!m) continue;
  const [res] = await new PurgeCSS().purge({
    content: [{ raw: doc.replace(m[0], ''), extension: 'html' }, { raw: js, extension: 'js' }],
    css: [{ raw: m[1] }],
    fontFace: false, keyframes: true, variables: false,
    safelist: { standard: ['syns', 'aktiv', 'fast', 'bak', 'oppen', 'sok-oppen', 'hp', 'fel'], greedy: [/^sok-/, /^boka-/, /hidden/, /^r5/, /^pf-/] },
  });
  const min = transform({ filename: 'x.css', code: Buffer.from(res.css), minify: true }).code.toString();
  fs.writeFileSync(p, doc.replace(m[0], () => `<style>${min}</style>`));
}
console.log('Rensade CSS på', sidor.length, 'sidor');
