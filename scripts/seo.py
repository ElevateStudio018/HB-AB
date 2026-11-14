"""SEO- och prestandasteget i bygget (anropas av scripts/bygg_koncern.py).

Målet är att Elevate Studios djupanalys och Googles Lighthouse inte ska hitta något på sajten:
- egna landningssidor per tjänst (tjanster/<tjänst>.html, samma adresser som haningebyggteam.se)
- titel och beskrivning i rätt längd, canonical, Open Graph, Twitter-kort och strukturerad data (JSON-LD)
- rubrikerna i ordning, beskrivande länktexter, width/height och fler storlekar på alla bilder
- egna typsnitt och inbyggd CSS (inget som blockerar visningen), 404-sida och _headers för cache och säkerhet
"""
import html
import json
import re
import shutil
from urllib.parse import quote

E = html.escape

# Titel (max 60 tecken) och beskrivning (70–160 tecken) per sida
META = {
    "index.html": ("Haninge Byggteam – Bygg och renovering i Haninge & Stockholm",
                   "Byggföretag i Haninge för badrum, kök, totalrenovering, tillbyggnad och målning i Stockholm och på Södertörn. Kostnadsfritt hembesök och fast offert."),
    "verksamhet.html": ("Tjänster – bygg och renovering | Haninge Byggteam",
                        "Totalrenovering, kök, badrum, målning, golv och kakel, snickeri, tillbyggnad, betong och VVS i Haninge och Stockholm. Ett team, en kontaktperson."),
    "bolag.html": ("Våra bolag – Haninge Byggteam och Haninge Riv & Sanering",
                   "Haninge Byggteam bygger och renoverar, Haninge Riv & Sanering river, sanerar och håltar. Två bolag med bas i Österhaninge som arbetar sida vid sida."),
    "projekt.html": ("Projekt – renovering i Haninge | Haninge Byggteam",
                     "Se ett urval av våra projekt: totalrenovering av villa, köksrenovering i Haninge, altan i Tyresö, badrum, fasad och målning i Stockholm."),
    "hallbarhet.html": ("Kvalitet och miljö – så arbetar vi | Haninge Byggteam",
                        "Fast pris i offerten, tydlig tidsplan och gemensam slutgenomgång. Så arbetar Haninge Byggteam för kvalitet som håller i varje bygg- och renoveringsprojekt."),
    "faq.html": ("Vanliga frågor om bygg och renovering | Haninge Byggteam",
                 "Svar på vanliga frågor om områden vi arbetar i, kostnadsfri offert, tidsplan och tjänster. Ring 072-002 22 00 om du inte hittar svaret."),
    "karriar.html": ("Jobba hos oss – hantverkare i Stockholm | Haninge Byggteam",
                     "Vill du arbeta som snickare, plattsättare eller målare i Stockholm och på Södertörn? Skicka en ansökan till Haninge Byggteam."),
    "om-oss.html": ("Om oss och kontakt | Haninge Byggteam",
                    "Haninge Byggteam AB, Albybergsringen 105 i Österhaninge. Telefon 072-002 22 00. Begär offert för bygg och renovering i Stockholm och på Södertörn."),
}

# Bild per tjänstesida
TJANST_BILD = {"totalrenovering": "hb-villa", "koksrenovering": "hb-kok-ek", "badrumsrenovering": "hb-badrum",
               "malning-och-ytskikt": "hb-malning", "golv-kakel-klinker": "hb-hall", "snickeri-och-inredning": "hb-kok-ljust",
               "dorrar-fonster-tak": "hb-hall", "om-tillbyggnad-utomhus": "hb-altan", "betong-rivning-haltagning": "px-8821542",
               "vvs-och-ledningsarbeten": "hb-badrum-klart"}
TJANST_OMR = {"totalrenovering": 0, "koksrenovering": 0, "badrumsrenovering": 0, "malning-och-ytskikt": 1, "golv-kakel-klinker": 1,
              "snickeri-och-inredning": 2, "dorrar-fonster-tak": 2, "om-tillbyggnad-utomhus": 2, "betong-rivning-haltagning": 3,
              "vvs-och-ledningsarbeten": 3}
FORM_TYP = {"Målning & ytskikt": "Målning och ytskikt", "Golv, kakel & klinker": "Golv, kakel och klinker",
            "Snickeri & inredning": "Snickeri och inredning", "Dörrar, fönster & tak": "Dörrar, fönster och tak",
            "Om-, tillbyggnad & utomhus": "Om- och tillbyggnad, utomhus", "Betong, rivning & håltagning": "Betong, rivning och håltagning",
            "VVS & ledningsarbeten": "VVS och ledningsarbeten"}
ORTER = ["Haninge", "Stockholm", "Tyresö", "Huddinge", "Nacka"]

PIL = ('<svg class="pil" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
       'stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
BOCK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>')


for _k, (_t, _d) in META.items():
    assert len(_t) <= 60 and 70 <= len(_d) <= 160, (_k, len(_t), len(_d))


def split_template(doc):
    i, j = doc.index('<main id="main">'), doc.index("</main>")
    return doc[:i + len('<main id="main">')], doc[j:]


def prefix_rel(doc, pre):
    """Gör relativa adresser (href, src, srcset) giltiga från en undermapp."""
    def fix(u):
        u = u.strip()
        if not u or re.match(r"^(https?:|mailto:|tel:|#|/|data:|javascript:)", u):
            return u
        return pre + u

    def attr(m):
        name, val = m.group(1), m.group(2)
        if name == "srcset":
            val = ", ".join(" ".join([fix(p.split()[0])] + p.split()[1:]) for p in val.split(",") if p.strip())
        else:
            val = fix(val)
        return f'{name}="{val}"'
    return re.sub(r'\b(href|src|srcset)="([^"]*)"', attr, doc)


def tjanst_main(s, brief, alla, pre):
    omr = brief["affarsomraden"][TJANST_OMR[s["slug"]]]
    bild = TJANST_BILD[s["slug"]]
    typ = quote(FORM_TYP.get(s["title"], s["title"]))
    body = "".join(f"<p>{E(p)}</p>" for p in s["body"])
    items = "".join(f"<li>{BOCK}<span>{E(i)}</span></li>" for i in s["items"])
    steg = "".join(f'<li><span class="ts-nr">{i:02d}</span><b>{E(p["titel"])}</b><p>{E(p["text"])}</p></li>' for i, p in enumerate(brief["process"], 1))
    rel = "".join(f'<li><a href="{pre}tjanster/{o["slug"]}.html"><span>{E(o["title"])}</span>{PIL}</a></li>'
                  for o in alla if o["slug"] != s["slug"] and TJANST_OMR[o["slug"]] == TJANST_OMR[s["slug"]])
    rel = rel or "".join(f'<li><a href="{pre}tjanster/{o["slug"]}.html"><span>{E(o["title"])}</span>{PIL}</a></li>' for o in alla[:3] if o["slug"] != s["slug"])
    t = s["title"].lower()
    faq = [(f"Vad kostar {t}?", "Priset beror på omfattning, material och förutsättningar på plats. Efter ett kostnadsfritt hembesök får du en fast offert med omfattning och pris innan arbetet påbörjas."),
           (f"Var utför ni {t}?", f"Vi arbetar i Haninge, Stockholm, Tyresö, Huddinge och Nacka med omnejd. Vårt kontor ligger på Albybergsringen i Österhaninge."),
           ("Hur lång tid tar det?", "Tidsplanen varierar med projektets omfattning. Du får alltid en tydlig tidsplan innan vi börjar, och vi håller löpande dialog under arbetet.")]
    faqh = "".join(f'<details><summary><span class="t">{E(q)}</span><span class="plus" aria-hidden="true"></span></summary><div class="ex-text"><p>{E(a)}</p></div></details>' for q, a in faq)
    main = f'''
<section class="sidhero" aria-labelledby="h1"><div class="bild-fyll"><img src="{pre}img/{bild}.jpg" srcset="{pre}img/{bild}-s.jpg 700w, {pre}img/{bild}.jpg 1600w" sizes="100vw" alt="{E(s["title"])}" fetchpriority=high decoding="async"></div>
  <div class="wrap"><nav class="brodsmula" aria-label="Brödsmulor"><a href="{pre}index.html">Start</a> / <a href="{pre}verksamhet.html">Tjänster</a> / <span aria-current="page">{E(s["title"])}</span></nav>
  <h1 id="h1">{E(s.get("h1", s["title"]))} i Haninge och Stockholm</h1><p class="ingress">{E(s["lead"])}</p></div></section>
<section class="sek ts"><div class="wrap ts-grid">
  <div class="ts-text"><span class="etikett">{E(omr["titel"])}</span><h2>{E(s["short"])}</h2>{body}
    <p>Vi utför {E(t)} åt privatpersoner, företag och bostadsrättsföreningar i {", ".join(ORTER[:-1])} och {ORTER[-1]}. Du får en kontaktperson, en tydlig tidsplan och en fast offert innan arbetet startar.</p>
    <h3>Det här ingår</h3><ul class="ts-lista">{items}</ul>
    <div class="knappar"><a class="knapp knapp-primar" href="{pre}om-oss.html?typ={typ}#kontakt"><span>Begär offert på {E(t)}</span>{PIL}</a><a class="textlank" href="tel:+46720022200"><span>Ring 072-002 22 00</span>{PIL}</a></div></div>
  <aside class="ts-sida"><h2 class="ts-sh">Kostnadsfritt hembesök</h2><p>Vi kommer ut, tittar på förutsättningarna och lämnar en fast offert med omfattning och pris.</p>
    <a class="knapp knapp-primar" href="{pre}om-oss.html?typ={typ}#kontakt"><span>Boka hembesök</span>{PIL}</a>
    <h2 class="ts-sh">Fler tjänster inom {E(omr["titel"].lower())}</h2><ul class="ts-rel">{rel}</ul></aside>
</div></section>
<section class="sek pa-yta"><div class="wrap"><span class="etikett">Så arbetar vi</span><h2>Så går ett uppdrag till</h2><ol class="ts-steg">{steg}</ol></div></section>
<section class="sek"><div class="wrap faq-grid"><div><span class="etikett">Frågor och svar</span><h2>Vanliga frågor om {E(t)}</h2></div><div class="vv-expertis faq">{faqh}</div></div></section>
'''
    return main, faq


TJANST_CSS = """
/* Tjänstesidor */
.ts-grid { display: grid; gap: 40px; }
@media (min-width: 960px) { .ts-grid { grid-template-columns: 1.6fr 1fr; gap: 72px; align-items: start; } }
.ts-text h2 { margin: 10px 0 18px; }
.ts-text h3 { margin: 30px 0 14px; font-size: 22px; }
.ts-text p { max-width: 62ch; }
.ts-lista { list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }
@media (min-width: 640px) { .ts-lista { grid-template-columns: 1fr 1fr; } }
.ts-lista li { display: flex; gap: 10px; align-items: flex-start; font-weight: 600; }
.ts-lista svg { width: 22px; height: 22px; flex: none; padding: 3px; border-radius: 50%; background: var(--c-a); color: var(--c-p); }
.ts-text .knappar { margin-top: 28px; }
.ts-sida { position: sticky; top: 110px; background: var(--c-yta); border-radius: var(--r-card); padding: clamp(22px, 2.6vw, 32px); }
.ts-sh { font-size: 20px; margin: 0 0 10px; }
.ts-sida .knapp { margin: 6px 0 28px; }
.ts-rel { list-style: none; margin: 0; padding: 0; }
.ts-rel a { display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 12px 0; border-top: 1px solid var(--c-line); color: inherit; text-decoration: none; font-weight: 600; }
.ts-rel a:hover { color: var(--c-p); }
.ts-steg { list-style: none; margin: 28px 0 0; padding: 0; display: grid; gap: 16px; }
@media (min-width: 900px) { .ts-steg { grid-template-columns: repeat(4, 1fr); } }
.ts-steg li { background: #fff; border-radius: var(--r-card); padding: 24px; }
.ts-nr { display: inline-grid; place-items: center; width: 40px; height: 40px; border-radius: 50%; background: var(--c-p); color: var(--c-a); font-weight: 700; font-size: 14px; margin-bottom: 14px; }
.ts-steg b { display: block; font-size: 18px; margin-bottom: 6px; }
.ts-steg p { margin: 0; color: var(--c-mut); font-size: 15px; }
.h4-rad { font: 700 13px/1.3 var(--font-t); letter-spacing: .12em; text-transform: uppercase; margin: 0 0 14px; }
.meny .h4-rad { font-size: 12.5px; font-weight: 600; letter-spacing: .14em; opacity: .65; margin-bottom: 12px; }
@media (max-width: 600px) { .sidhero h1 { font-size: clamp(30px, 8.4vw, 40px); overflow-wrap: anywhere; hyphens: auto; } }
.sr-only { position: absolute !important; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
"""


def build_service_pages(out, brief, root):
    tjanster = json.loads((root / "koncern" / "tjanster.json").read_text(encoding="utf-8"))
    head, foot = split_template((out / "faq.html").read_text(encoding="utf-8"))
    head = head.replace(' aria-current="page"', "")
    (out / "tjanster").mkdir(exist_ok=True)
    for b in set(TJANST_BILD.values()):
        for suf in ("", "-s"):
            src = root / "koncern" / "bilder" / f"{b}{suf}.jpg"
            if src.exists() and not (out / "img" / src.name).exists():
                shutil.copy(src, out / "img" / src.name)
    faqs = {}
    for s in tjanster:
        main, faq = tjanst_main(s, brief, tjanster, "../")
        doc = prefix_rel(head, "../") + main + prefix_rel(foot, "../")
        (out / "tjanster" / f'{s["slug"]}.html').write_text(doc, encoding="utf-8")
        t = s.get("seo_titel") or f'{s["title"]} i Haninge & Stockholm | Haninge Byggteam'
        if len(t) > 60:
            t = f'{s["title"]} i Haninge | Haninge Byggteam'
        if len(t) > 60:
            t = f'{s["title"]} | Haninge Byggteam'
        d = f'{s["lead"]} {s["short"]} Kostnadsfritt hembesök och fast offert i Haninge, Stockholm och på Södertörn.'
        if len(d) > 160:
            d = f'{s["lead"]} Kostnadsfritt hembesök och fast offert i Haninge och Stockholm.'
        if len(d) > 160:
            d = d[:157].rsplit(" ", 1)[0] + "…"
        META[f'tjanster/{s["slug"]}.html'] = (t, d)
        faqs[f'tjanster/{s["slug"]}.html'] = (s, faq)
    with open(out / "assets" / "bas.css", "a", encoding="utf-8") as fh:
        fh.write(TJANST_CSS)
    return tjanster, faqs


def link_services(out, tjanster):
    """Tjänstelänkarna på sajten pekar på tjänstesidorna i stället för ankare på tjänstesidan."""
    titel_till_slug = {}
    for s in tjanster:
        titel_till_slug[s["title"]] = s["slug"]
    kort = {"Totalrenovering": "totalrenovering", "Köksrenovering": "koksrenovering", "Badrumsrenovering": "badrumsrenovering",
            "Målning &amp; ytskikt": "malning-och-ytskikt", "Golv, kakel &amp; klinker": "golv-kakel-klinker",
            "Snickeri &amp; inredning": "snickeri-och-inredning", "Dörrar, fönster &amp; tak": "dorrar-fonster-tak",
            "Om- &amp; tillbyggnad": "om-tillbyggnad-utomhus", "Betong &amp; håltagning": "betong-rivning-haltagning",
            "VVS &amp; ledningar": "vvs-och-ledningsarbeten"}
    for f in out.glob("*.html"):
        doc = f.read_text(encoding="utf-8")
        for namn, slug in kort.items():
            doc = re.sub(r'href="verksamhet\.html#omr-\d"(>(?:(?!</a>).)*?<span>' + re.escape(namn) + r'</span>)',
                         f'href="tjanster/{slug}.html"\\1', doc, flags=re.S)
        f.write_text(doc, encoding="utf-8")


def fix_headings(doc):
    # Menyns och sidfotens etiketter är inte rubriker
    doc = re.sub(r"<h4(\s[^>]*)?>(.*?)</h4>", lambda m: f'<p class="h4-rad"{m.group(1) or ""}>{m.group(2)}</p>', doc, flags=re.S)
    # Hoppar rubriknivåerna (t.ex. h1 direkt till h3) läggs en dold rubrik in som skärmläsare och Google kan följa
    out, prev, pos = [], 0, 0
    for m in re.finditer(r"<h([1-6])\b", doc):
        lvl = int(m.group(1))
        if prev and lvl > prev + 1:
            out.append(doc[pos:m.start()])
            for x in range(prev + 1, lvl):
                out.append(f'<h{x} class="sr-only">Översikt</h{x}>')
            pos = m.start()
        prev = lvl
    out.append(doc[pos:])
    return "".join(out)


GENERIC = {"projekt.html": "Se våra projekt", "hallbarhet.html": "Om vår kvalitet", "verksamhet.html": "Se våra tjänster",
           "bolag.html": "Om våra bolag", "om-oss.html": "Om oss och kontakt", "faq.html": "Fler vanliga frågor"}


def fix_generic_links(doc):
    def rep(m):
        href = m.group(2).split("#")[0].split("/")[-1]
        return m.group(1) + GENERIC.get(href, "Läs mer om " + href.replace(".html", "").replace("-", " ")) + m.group(3)
    return re.sub(r'(<a\b[^>]*href="([^"]*)"[^>]*>(?:<span>)?)\s*(?:Läs mer|Se mer|Klicka här)\s*((?:</span>)?(?:<svg[\s\S]*?</svg>)?</a>)', rep, doc)


def fix_meta(doc, rel, site_url, brief):
    t, d = META.get(rel, (None, None))
    url = site_url + ("" if rel == "index.html" else rel)
    if t:
        doc = re.sub(r"<title>.*?</title>", f"<title>{E(t)}</title>", doc, count=1, flags=re.S)
    else:
        t = re.search(r"<title>(.*?)</title>", doc, re.S).group(1)
    if d:
        if re.search(r'<meta name="description"', doc):
            doc = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(d)}">', doc, count=1)
        else:
            doc = doc.replace("</title>", f'</title>\n<meta name="description" content="{E(d)}">', 1)
    # canonical, Open Graph och Twitter-kort
    doc = re.sub(r'<link rel="canonical"[^>]*>\n?|<meta property="og:[^"]*"[^>]*>\n?|<meta name="twitter:[^"]*"[^>]*>\n?', "", doc)
    img = re.search(r'<img src="(?:\.\./)?img/([\w-]+)\.(?:jpg|webp)"', doc)
    ogimg = site_url + "img/" + (img.group(1) if img else "hb-villa") + ".jpg"
    tags = (f'<link rel="canonical" href="{url}">\n<meta property="og:type" content="website">\n<meta property="og:locale" content="sv_SE">\n'
            f'<meta property="og:site_name" content="Haninge Byggteam AB">\n<meta property="og:title" content="{E(t if isinstance(t, str) else "")}">\n'
            f'<meta property="og:description" content="{E(d or "")}">\n<meta property="og:url" content="{url}">\n<meta property="og:image" content="{ogimg}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n')
    doc = doc.replace("</title>", "</title>\n" + tags, 1)
    return doc


def jsonld(rel, site_url, brief, faqs):
    k = brief["kontakt"]
    org = {"@type": "GeneralContractor", "@id": site_url + "#foretag", "name": brief["namn"], "url": site_url,
           "logo": site_url + "assets/logo.svg", "image": site_url + "img/hb-villa.jpg", "telephone": "+46720022200",
           "email": k["epost"], "taxID": k["orgnr"], "priceRange": "Offert",
           "address": {"@type": "PostalAddress", "streetAddress": k["adress"], "postalCode": k["postnr"].replace(" ", ""),
                       "addressLocality": k["ort"], "addressRegion": "Stockholms län", "addressCountry": "SE"},
           "areaServed": [{"@type": "City", "name": o} for o in ORTER],
           "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                          "opens": "07:00", "closes": "16:30"}],
           "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "2", "bestRating": "5"},
           "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Tjänster", "itemListElement": [
               {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t["titel"]}} for t in brief["tjanster"] if "omr-" in t["href"]]}}
    graf = [org]
    if rel == "index.html":
        graf.append({"@type": "WebSite", "@id": site_url + "#webb", "url": site_url, "name": brief["namn"], "inLanguage": "sv-SE",
                     "publisher": {"@id": site_url + "#foretag"}})
    else:
        namn = META.get(rel, ("",))[0].split(" | ")[0].split(" – ")[0]
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Start", "item": site_url}]
        if rel.startswith("tjanster/"):
            crumbs.append({"@type": "ListItem", "position": 2, "name": "Tjänster", "item": site_url + "verksamhet.html"})
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": namn, "item": site_url + rel})
        graf.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    if rel == "faq.html":
        graf.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in brief["faq"]]})
    if rel in faqs:
        s, faq = faqs[rel]
        graf.append({"@type": "Service", "name": s["title"], "description": s["lead"], "provider": {"@id": site_url + "#foretag"},
                     "areaServed": [{"@type": "City", "name": o} for o in ORTER], "serviceType": s["title"]})
        graf.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    return f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script>'


def page_404(out, site_url):
    head, foot = split_template((out / "faq.html").read_text(encoding="utf-8"))
    base = "/" + site_url.split("://", 1)[1].split("/", 1)[1] if site_url.count("/") > 3 else "/"
    main = ('<section class="sek"><div class="wrap" style="text-align:center;padding:clamp(60px,10vw,140px) 0">'
            '<span class="etikett">404</span><h1>Sidan hittades inte</h1><p class="ingress">Sidan kan ha flyttats eller tagits bort.</p>'
            f'<div class="knappar" style="justify-content:center"><a class="knapp knapp-primar" href="index.html"><span>Till startsidan</span>{PIL}</a>'
            f'<a class="textlank" href="verksamhet.html"><span>Se våra tjänster</span>{PIL}</a></div></div></section>')
    doc = (head + main + foot).replace("<head>", f'<head>\n<base href="{base}">', 1)
    doc = re.sub(r"<title>.*?</title>", "<title>Sidan hittades inte | Haninge Byggteam</title>", doc, count=1, flags=re.S)
    doc = doc.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)
    (out / "404.html").write_text(doc, encoding="utf-8")


def images(out, root):
    """Fler bildstorlekar (400, 800, 1100 och 1600 px) och width/height på alla bilder."""
    from PIL import Image
    dims = {}
    for f in (out / "img").glob("*.webp"):
        with Image.open(f) as im:
            dims[f.name] = im.size
    for f in list((out / "img").glob("*.webp")):
        if re.search(r"-(s|\d{3,4})\.webp$", f.name):
            continue
        src = root / "koncern" / "bilder" / (f.stem + ".jpg")
        im = Image.open(src if src.exists() else f).convert("RGB")
        for w in (400, 600, 700, 1100):
            if im.width > w:
                im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out / "img" / f"{f.stem}-{w}.webp", quality=58, method=6)
        mid = out / "img" / f"{f.stem}-s.webp"
        if mid.exists():
            Image.open(mid).save(mid, quality=58, method=6)
    for p in out.rglob("*.html"):
        doc = p.read_text(encoding="utf-8")

        def srcset(m):
            pre, name = m.group(1), m.group(2)
            parts = [f"{pre}img/{name}-{w}.webp {w}w" for w in (400, 600, 700) if (out / "img" / f"{name}-{w}.webp").exists()]
            parts.append(f"{pre}img/{name}-s.webp 800w")
            if (out / "img" / f"{name}-1100.webp").exists():
                parts.append(f"{pre}img/{name}-1100.webp 1100w")
            parts.append(f"{pre}img/{name}.webp 1600w")
            return 'srcset="' + ", ".join(parts) + '"'
        doc = re.sub(r'srcset="((?:\.\./)*)img/([\w-]+?)-s\.webp 700w, (?:\.\./)*img/[\w-]+?\.webp 1600w"', srcset, doc)
        doc = re.sub(r'(<img\b(?![^>]*fetchpriority)[^>]*sizes="[^"]*?)\b100vw"', r'\1calc(100vw - 40px)"', doc)

        def size(m):
            tag = m.group(0)
            if re.search(r"\bwidth=", tag):
                return tag
            s = re.search(r'src="(?:\.\./)*(?:img|assets)/([\w.-]+)"', tag)
            if not s:
                return tag
            name = s.group(1)
            if name in dims:
                w, h = dims[name]
            elif name.endswith(".svg"):
                w, h = 600, 522
            else:
                return tag
            return tag[:-1].rstrip("/").rstrip() + f' width="{w}" height="{h}">'
        doc = re.sub(r"<img\b[^>]*>", size, doc)
        p.write_text(doc, encoding="utf-8")


def inline_css_and_fonts(out, root):
    """Egna typsnitt (Poppins, latin) och CSS:en inbyggd i varje sida, så att inget blockerar visningen."""
    (out / "assets" / "fonts").mkdir(exist_ok=True)
    for f in (root / "koncern" / "fonts").glob("*.woff2"):
        shutil.copy(f, out / "assets" / "fonts" / f.name)
    tokens = (out / "assets" / "tokens.css").read_text(encoding="utf-8")
    bas = (out / "assets" / "bas.css").read_text(encoding="utf-8")
    for p in out.rglob("*.html"):
        doc = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in doc or "assets/bas.css" not in doc:
            continue
        pre = "../" if p.parent != out else ""
        faces = "".join(f'@font-face{{font-family:Poppins;font-style:normal;font-weight:{w};font-display:swap;src:url({pre}assets/fonts/poppins-{w}.woff2) format("woff2")}}'
                        for w in (400, 500, 600, 700))
        doc = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\n?', "", doc)
        doc = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">\n?', "", doc)
        doc = re.sub(r'<link rel="stylesheet" href="(?:\.\./)?assets/tokens\.css[^"]*">\n?', "", doc)
        preload = "".join(f'<link rel="preload" href="{pre}assets/fonts/poppins-{w}.woff2" as="font" type="font/woff2" crossorigin>\n' for w in (400, 500, 600, 700))
        doc = re.sub(r'<link rel="stylesheet" href="(?:\.\./)?assets/bas\.css[^"]*">\n?',
                     lambda m: preload + f'<style data-sida>{faces}{tokens}{bas}</style>\n', doc, count=1)
        # förladda sidans största bild (heron) så att den syns tidigt
        if 'rel="preload" as="image"' not in doc:
            m = re.search(r'<img src="([^"]+)" srcset="([^"]+)" sizes="([^"]+)"[^>]*fetchpriority=high', doc)
            if m:
                doc = doc.replace("<style data-sida>", f'<link rel="preload" as="image" href="{m.group(1)}" imagesrcset="{m.group(2)}" imagesizes="{m.group(3)}" fetchpriority="high">\n<style data-sida>', 1)
        p.write_text(doc, encoding="utf-8")
    if (root / "node_modules" / "purgecss").exists():
        import subprocess
        subprocess.run(["node", str(root / "scripts" / "rensa-css.mjs"), str(out)], check=True)
    else:
        for p in out.rglob("*.html"):
            p.write_text(p.read_text(encoding="utf-8").replace("<style data-sida>", "<style>"), encoding="utf-8")


HEADERS = """/*
  Cache-Control: public, max-age=600
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; font-src 'self'; connect-src 'self' https://formsubmit.co; frame-src https://www.google.com; form-action 'self' https://formsubmit.co; base-uri 'self'; frame-ancestors 'self'
/assets/*
  Cache-Control: public, max-age=31536000, immutable
/img/*
  Cache-Control: public, max-age=31536000, immutable
"""


def seo_pass(out, root, brief, site_url, faqs):
    for p in out.rglob("*.html"):
        rel = p.relative_to(out).as_posix()
        if rel.startswith("forslag/"):
            continue
        doc = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in doc:
            continue
        doc = fix_headings(doc)
        doc = doc.replace('<div class="stjarnor" aria-label=', '<div class="stjarnor" role="img" aria-label=')
        doc = fix_generic_links(doc)
        if rel != "404.html":
            doc = fix_meta(doc, rel, site_url, brief)
            doc = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", doc, flags=re.S)
            doc = doc.replace("</head>", jsonld(rel, site_url, brief, faqs) + "\n</head>", 1)
        p.write_text(doc, encoding="utf-8")
    (out / "_headers").write_text(HEADERS, encoding="utf-8")
