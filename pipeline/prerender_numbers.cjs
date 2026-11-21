// Writes the live record numbers into the static HTML so phones, crawlers and link previews never see stale
// or zero counts before the script runs (Nov 20 audit: /results showed 0/6 and 26-35 next to 21-44).
// Usage (repo root): node pipeline/prerender_numbers.cjs   -> patches pipeline/bettordays-hq.html, then run buildsite.py
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const SRC = path.join(__dirname, 'bettordays-hq.html'); const IDS = ['tlTk', 'tlTkS', 'tl70', 'tl70S', 'tlAll', 'tlAllS', 'homeProof'];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.route('**/*', r => /^file:|^data:/.test(r.request().url()) ? r.continue() : r.abort());
  await p.goto('file://' + path.join(__dirname, '..', 'index.html')); await p.waitForTimeout(2500);
  const got = await p.evaluate(ids => Object.fromEntries(ids.map(i => [i, document.getElementById(i)?.innerHTML ?? null])), IDS);
  await b.close();
  let s = fs.readFileSync(SRC, 'utf8'); let n = 0;
  for (const [id, html] of Object.entries(got)) {
    if (html == null) continue;
    const re = new RegExp(`(<(\\w+)[^>]*\\bid="${id}"[^>]*>)([\\s\\S]*?)(</\\2>)`);
    s = s.replace(re, (m, open, tag, old, close) => { if (old !== html) n++; return open + html + close; });
  }
  // counters show their real number before the count-up runs
  s = s.replace(/<span data-count="(\d+)">0<\/span>/g, (m, v) => { n++; return `<span data-count="${v}">${v}</span>`; });
  fs.writeFileSync(SRC, s); console.log('prerendered', n, got);
})();
