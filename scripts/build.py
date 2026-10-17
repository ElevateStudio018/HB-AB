"""Builds the Haninge Byggteam AB website into docs/.

Run:  python3 scripts/build.py docs

All text, services, projects and contact details live in this file. Edit here and rebuild; never edit the generated
HTML in docs/ by hand. Text marked "förslag" in README.md is suggested copy that Haninge Byggteam should confirm.
"""
import html
import json
import pathlib
import sys
from urllib.parse import quote_plus

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs")

# --- Company details (from haningebyggteam.se and the company van) ----------------------------------------------------
NAME = "Haninge Byggteam AB"
ORG_NR = "559229-1115"
PHONE, TEL = "072-002 22 00", "+46720022200"
EMAIL = "info@haningebyggteam.se"
STREET, POSTAL, CITY = "Albybergsringen 105", "137 69", "Österhaninge"
ADDR = f"{STREET}, {POSTAL} {CITY}"
HOURS = "Måndag–fredag 07.00–16.30"
AREAS = ["Haninge", "Stockholm", "Tyresö", "Huddinge", "Nacka"]
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{NAME}, {STREET}, {POSTAL}")
MAP_EMBED = "https://www.google.com/maps?q=" + quote_plus(f"{STREET}, {POSTAL} Haninge") + "&z=14&hl=sv&output=embed"

# The contact form e-mails through FormSubmit. Elevate Studio receives the requests during the preview; at launch this
# becomes Haninge Byggteam's own address. The first request to a new address only sends an activation e-mail.
FORM_EMAIL = "elevate.studio018@gmail.com"

SITE_URL = "https://elevatestudio018.github.io/HB-AB/"

# --- Business areas and services --------------------------------------------------------------------------------------
# The ten services and their texts come from haningebyggteam.se. The grouping into business areas is new (see README).
DIVISIONS = [
    dict(id="renovering", title="Renovering och ytskikt", photo="kok-ljust",
         lead="Totalrenoveringar, kök och badrum, målning, golv och plattsättning i bostäder och lokaler."),
    dict(id="bygg", title="Bygg och snickeri", photo="altan",
         lead="Snickeri och inredning, dörrar, fönster och tak, ombyggnader, tillbyggnader och utvändiga arbeten."),
    dict(id="teknik", title="Grund och installation", photo="betong",
         lead="Betongarbeten, rivning och håltagning samt vatten och avlopp i samband med byggprojekt."),
]

SERVICES = [
    dict(slug="totalrenovering", div="renovering", title="Totalrenovering", photo="rivning",
         lead="Kompletta totalrenoveringar från idé till färdigt resultat.",
         body=["Vi hjälper dig med totalrenovering av bostäder, villor och andra fastigheter i hela projektets omfattning. Från rivning och grundarbete till målning, golvläggning, snickeri och färdiga ytskikt – vi samordnar arbetet för en smidig renoveringsprocess och ett resultat som håller över tid."],
         items=["Rivning och grundarbete", "Planlösning och innerväggar", "Kök och badrum", "Golv, kakel och klinker", "Målning och ytskikt", "Snickeri"]),
    dict(slug="koksrenovering", div="renovering", title="Köksrenovering", photo="kok-ek",
         lead="Ge köket ett nytt liv med en genomtänkt köksrenovering.",
         body=["Vi erbjuder kompletta köksrenoveringar där vi hjälper till med rivning, montering av kök och inredning samt målning, golv och andra ytskikt. Målet är att skapa ett funktionellt, modernt och hållbart kök som passar både bostaden och dina behov."],
         items=["Rivning", "Montering av kök och inredning", "Målning", "Golv och ytskikt"]),
    dict(slug="badrumsrenovering", div="renovering", title="Badrumsrenovering", photo="badrum-modern",
         lead="Professionell badrumsrenovering med fokus på kvalitet och hållbarhet.",
         body=["Vi utför kompletta badrumsrenoveringar med allt från rivning och förberedande arbeten till tätskikt, kakel, klinker och montering. Oavsett om du vill renovera ett mindre badrum eller skapa ett helt nytt modernt badrum hjälper vi dig genom hela projektet."],
         items=["Rivning och förberedande arbeten", "Tätskikt", "Kakel och klinker", "Montering"]),
    dict(slug="malning-och-ytskikt", div="renovering", title="Målning och ytskikt", photo="malning-pagar",
         lead="Jämna och hållbara ytor i hela bostaden.",
         body=["Vi utför professionell målning, spackling, gipsarbeten och andra ytskiktsarbeten för både mindre och större renoveringar. Med noggrant underarbete och rätt material skapar vi jämna och hållbara ytor. En ny färg eller nya ytskikt kan ge hela bostaden ett fräscht och modernt uttryck."],
         items=["Målning", "Spackling", "Gipsarbeten", "Övriga ytskikt"]),
    dict(slug="golv-kakel-klinker", div="renovering", title="Golv, kakel och klinker", photo="hall-trappa",
         lead="Golvläggning och plattsättning för bostäder och lokaler.",
         body=["Vi erbjuder professionell golvläggning samt kakel- och klinkerarbeten för bostäder och andra lokaler. Vi lägger bland annat parkett, laminat och vinyl samt sätter kakel och klinker i kök, badrum och andra utrymmen. Noggranna förberedelser och ett professionellt utförande ger ett snyggt och hållbart resultat."],
         items=["Parkett", "Laminat", "Vinyl", "Kakel och klinker"]),
    dict(slug="snickeri-och-inredning", div="bygg", title="Snickeri och inredning", photo="snickeri",
         lead="Snickeriarbeten och inredning för små och stora projekt.",
         body=["Vi utför snickeriarbeten och monterar inredning för både små och stora renoveringsprojekt. Det kan handla om allt från köksmontering och dörrar till fönster, specialanpassade lösningar och andra snickeridetaljer. Vi arbetar noggrant med detaljerna för att skapa funktionella och stilrena resultat."],
         items=["Köksmontering", "Dörrar och fönster", "Specialanpassade lösningar", "Snickeridetaljer"]),
    dict(slug="dorrar-fonster-tak", div="bygg", title="Dörrar, fönster och tak", photo="dorr",
         lead="Byte och montering anpassat efter fastighetens förutsättningar.",
         body=["Vi hjälper dig med byte och montering av dörrar och fönster samt arbeten med innertak och undertak. Genom att uppdatera dessa delar kan du förbättra både bostadens utseende och funktion. Vi utför arbetet noggrant och anpassar lösningen efter fastighetens förutsättningar och dina önskemål."],
         items=["Dörrar", "Fönster", "Innertak", "Undertak"]),
    dict(slug="om-tillbyggnad-utomhus", div="bygg", title="Om- och tillbyggnad, utomhus", photo="altan",
         lead="Vi utvecklar både bostaden och utemiljön.",
         body=["Vi hjälper dig att utveckla och förbättra både bostaden och utemiljön genom ombyggnationer, tillbyggnader och utvändiga snickeriarbeten. Vi utför bland annat altaner, trädäck, staket och fasadarbeten. Varje projekt anpassas efter fastighetens förutsättningar och dina önskemål för ett funktionellt och hållbart resultat."],
         items=["Ombyggnationer", "Tillbyggnader", "Altaner och trädäck", "Staket", "Fasadarbeten"]),
    dict(slug="betong-rivning-haltagning", div="teknik", title="Betong, rivning och håltagning", photo="betong",
         lead="Rätt förutsättningar för det fortsatta byggprojektet.",
         body=["Vi utför betongarbeten, gjutning, bilning, håltagning samt rivnings- och återställningsarbeten. Dessa arbeten är ofta viktiga delar av större renoveringar och ombyggnationer. Med ett effektivt och noggrant utförande skapar vi rätt förutsättningar för det fortsatta byggprojektet."],
         items=["Betongarbeten och gjutning", "Bilning", "Håltagning", "Rivning och återställning"]),
    dict(slug="vvs-och-ledningsarbeten", div="teknik", title="VVS och ledningsarbeten", photo="vvs",
         lead="Vatten och avlopp, samordnat med projektets övriga moment.",
         body=["Vi utför arbeten inom vatten och avlopp i samband med renoveringar, ombyggnationer och andra byggprojekt. Det kan bland annat innebära byte och anpassning av vatten- och avloppsledningar. Vi hjälper till att skapa funktionella lösningar och samordnar arbetet med projektets övriga moment."],
         items=["Vattenledningar", "Avloppsledningar", "Anpassning vid ombyggnad"]),
]
WORK_TYPES = [s["title"] for s in SERVICES] + ["Annat"]

# --- Projects (names, categories and places from haningebyggteam.se/projekt) -------------------------------------------
PROJECTS = [
    dict(title="Totalrenovering av villa", cat="Totalrenovering", place="Stockholm", photo="hero-villa"),
    dict(title="Modern köksrenovering", cat="Kök", place="Haninge", photo="kok-ljust"),
    dict(title="Ny altan i trä", cat="Utomhus", place="Tyresö", photo="altan"),
    dict(title="Badrum", cat="Badrum", place="", photo="badrum-modern"),
    dict(title="Kök", cat="Kök", place="", photo="kok-ek"),
    dict(title="Fasad", cat="Tillbyggnad", place="", photo="fasad-team"),
    dict(title="Badrum", cat="Badrum", place="", photo="badrum-klart"),
    dict(title="Målning", cat="Målning", place="", photo="malning-pagar"),
    dict(title="Hall och trappa", cat="Målning", place="", photo="hall-trappa"),
]
PROJECT_CATS = ["Totalrenovering", "Kök", "Badrum", "Utomhus", "Målning", "Tillbyggnad"]

STEPS = [
    ("Kontakt", "Du kontaktar oss och berättar om ditt projekt eller dina önskemål. Vi går igenom dina behov och bokar nästa steg."),
    ("Hembesök", "Vi träffas på plats för att titta på projektet och diskutera olika lösningar. Besöket ger ett bra underlag inför offert."),
    ("Offert", "Du får en tydlig offert med omfattning och pris innan arbetet påbörjas. Eventuella frågor besvaras innan beslut fattas."),
    ("Genomförande", "Arbetet utförs enligt överenskommelse och med löpande dialog under projektets gång. När arbetet är klart görs en gemensam genomgång."),
]

VALUES = [
    ("Kvalitet", "Vi levererar hållbara resultat som motsvarar kundens förväntningar."),
    ("Kommunikation", "Tydlig och löpande dialog med kunden genom hela projektet."),
    ("Professionalism", "Ett professionellt arbetssätt i varje uppdrag, stort som litet."),
    ("Planering", "Varje uppdrag planeras noggrant innan arbetet påbörjas."),
]

E = html.escape
ARROW = '<svg class="ar" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'


def img(root, src, alt="", sizes="100vw", lazy=True, pos="50% 50%"):
    return (f'<img src="{root}img/{src}.jpg" srcset="{root}img/{src}-s.jpg 800w, {root}img/{src}.jpg 1800w" sizes="{sizes}" '
            f'alt="{E(alt)}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async" style="object-position:{pos}">')


def link(href, text, cls="lnk"):
    return f'<a class="{cls}" href="{href}"><span>{text}</span>{ARROW}</a>'


def button(href, text, cls="btn"):
    return f'<a class="{cls}" href="{href}">{text}</a>'


def logo():
    return '<span class="logo-a">HANINGE</span><span class="logo-b">BYGGTEAM</span>'


# --- Header and footer -------------------------------------------------------------------------------------------------
NAV = [("verksamhet", "Verksamhet", "tjanster/index.html"), ("projekt", "Projekt", "projekt.html"),
       ("kunder", "Kunder", "kunder.html"), ("om-oss", "Om oss", "om-oss.html"),
       ("karriar", "Karriär", "karriar.html"), ("kontakt", "Kontakt", "kontakt.html")]


def header(root, active):
    cols = "".join(
        f'<div><a class="mega-h" href="{root}tjanster/index.html#{d["id"]}">{d["title"]}</a><ul>'
        + "".join(f'<li><a href="{root}tjanster/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES if s["div"] == d["id"])
        + "</ul></div>" for d in DIVISIONS)
    items = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        if key == "verksamhet":
            items.append(f'<li class="has-mega"><a href="{root}{href}"{cur}>{label}</a>'
                         f'<div class="mega"><div class="wrap mega-in"><div class="mega-intro"><p class="mega-t">Verksamhet</p>'
                         f'<p>Bygg- och renoveringstjänster för privatpersoner, företag och bostadsrättsföreningar i Stockholm.</p>'
                         f'{link(root + href, "Alla tjänster")}</div>{cols}</div></div></li>')
        else:
            items.append(f'<li><a href="{root}{href}"{cur}>{label}</a></li>')
    menu = "".join(f'<li><a href="{root}{h}">{l}</a></li>' for _, l, h in NAV)
    return f'''<a class="skip" href="#main">Till innehållet</a>
<header class="head">
  <div class="wrap bar">
    <a class="logo" href="{root}index.html" aria-label="{NAME}, startsidan">{logo()}</a>
    <nav aria-label="Huvudmeny"><ul class="nav">{"".join(items)}</ul></nav>
    <button class="burger" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu">Meny</button>
  </div>
  <nav class="menu" id="menu" aria-label="Meny" hidden><div class="wrap"><ul>{menu}</ul>
    <p class="menu-c"><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></nav>
</header>'''


def footer(root):
    def col(d):
        return "".join(f'<li><a href="{root}tjanster/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES if s["div"] == d["id"])

    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="logo logo-light" href="{root}index.html" aria-label="{NAME}, startsidan">{logo()}</a>
        <p>{NAME}<br>{STREET}<br>{POSTAL} {CITY}</p>
        <p><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><p class="foot-h">{DIVISIONS[0]["title"]}</p><ul>{col(DIVISIONS[0])}</ul></div>
      <div><p class="foot-h">{DIVISIONS[1]["title"]}</p><ul>{col(DIVISIONS[1])}</ul>
        <p class="foot-h foot-h2">{DIVISIONS[2]["title"]}</p><ul>{col(DIVISIONS[2])}</ul></div>
      <div><p class="foot-h">Företaget</p><ul>{"".join(f'<li><a href="{root}{h}">{l}</a></li>' for _, l, h in NAV)}</ul></div>
    </div>
    <div class="foot-end">
      <span>© <span data-year>2026</span> {NAME}</span>
      <span>Org.nr {ORG_NR}</span>
      <a href="https://www.elevatestudio.nu" target="_blank" rel="noopener">Webbplats: Elevate Studio</a>
    </div>
  </div>
</footer>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
'''


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "GeneralContractor", "name": NAME, "url": SITE_URL,
        "telephone": TEL, "email": EMAIL, "image": SITE_URL + "img/hero-villa.jpg", "taxID": ORG_NR,
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": POSTAL.replace(" ", ""),
                    "addressLocality": CITY, "addressCountry": "SE"},
        "areaServed": [{"@type": "City", "name": a} for a in AREAS],
        "openingHours": "Mo-Fr 07:00-16:30",
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def page(name, title, desc, main, active="", image="hero-villa"):
    root = "../" * name.count("/")
    url = SITE_URL + ("" if name == "index.html" else name.removesuffix("index.html"))
    doc = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}img/{image}.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e2a47">
<link rel="icon" href="{root}img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{root}img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{root}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="{root}assets/site.css">
{jsonld() if name == "index.html" else ""}
</head>
<body>
{header(root, active)}
<main id="main">
{main.replace("{root}", root)}
</main>
{footer(root)}'''
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")


# --- Shared blocks -----------------------------------------------------------------------------------------------------
def crumbs(trail):
    li = "".join(f'<li><a href="{{root}}{h}">{t}</a></li>' for t, h in trail)
    return f'<nav aria-label="Brödsmulor"><ol class="crumbs"><li><a href="{{root}}index.html">Start</a></li>{li}</ol></nav>'


def page_head(trail, title, lead, photo_name=None):
    """Title block on white, then a full-width photo – the way the large contractors open their sub-pages."""
    pic = f'<div class="banner">{img("{root}", photo_name, "", lazy=False)}</div>' if photo_name else ""
    return f'''<section class="phead">
  <div class="wrap">
    {crumbs(trail)}
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
{pic}'''


def tile(href, photo_name, title, text, sizes="(min-width: 960px) 33vw, 100vw"):
    return (f'<a class="tile" href="{href}"><span class="tile-img">{img("{root}", photo_name, "", sizes)}</span>'
            f'<span class="tile-t">{title}</span><span class="tile-p">{text}</span><span class="tile-l">Läs mer{ARROW}</span></a>')


def project_card(p):
    meta = p["cat"] + (", " + p["place"] if p["place"] else "")
    return (f'<figure class="pcard" data-cat="{p["cat"]}"><span class="pcard-img">{img("{root}", p["photo"], p["title"], "(min-width: 960px) 33vw, (min-width: 600px) 50vw, 100vw")}</span>'
            f'<figcaption><span class="pcard-m">{meta}</span><span class="pcard-t">{p["title"]}</span></figcaption></figure>')


def section_head(title, text=None, href=None, label=None):
    right = link(href, label) if href else ""
    p = f'<p>{text}</p>' if text else ""
    return f'<div class="shead"><div><h2>{title}</h2>{p}</div>{right}</div>'


def contact_block(title="Kontakta oss"):
    return f'''<section class="sec sec-grey">
  <div class="wrap split">
    <h2>{title}</h2>
    <div class="contact-cols">
      <div><p class="k">Telefon</p><p><a href="tel:{TEL}">{PHONE}</a></p></div>
      <div><p class="k">E-post</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div><p class="k">Besöksadress</p><p>{STREET}<br>{POSTAL} {CITY}</p></div>
      <div><p class="k">Öppettider</p><p>{HOURS}</p></div>
    </div>
  </div>
</section>'''


def form():
    opts = "".join(f"<option>{E(t)}</option>" for t in WORK_TYPES)
    return f'''<form id="qform" class="form" novalidate data-endpoint="https://formsubmit.co/ajax/{FORM_EMAIL}">
  <div class="row2">
    <div class="field"><label for="f-namn">Namn</label><input id="f-namn" name="namn" autocomplete="name" required>
      <p class="err" id="e-namn" hidden>Ange ditt namn.</p></div>
    <div class="field"><label for="f-tel">Telefon</label><input id="f-tel" name="tel" type="tel" autocomplete="tel">
      <p class="err" id="e-tel" hidden>Ange telefon eller e-post.</p></div>
  </div>
  <div class="row2">
    <div class="field"><label for="f-epost">E-post</label><input id="f-epost" name="epost" type="email" autocomplete="email">
      <p class="err" id="e-epost" hidden>Kontrollera e-postadressen.</p></div>
    <div class="field"><label for="f-typ">Ärende</label><select id="f-typ" name="typ"><option value="">Välj</option>{opts}</select></div>
  </div>
  <div class="field"><label for="f-ort">Ort</label><input id="f-ort" name="ort" autocomplete="address-level2"></div>
  <div class="field"><label for="f-besk">Meddelande</label><textarea id="f-besk" name="besk" rows="5"></textarea></div>
  <div class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="web" tabindex="-1" autocomplete="off"></div>
  <button class="btn" type="submit">Skicka</button>
  <p class="err" id="send-err" role="alert" hidden>Meddelandet kunde inte skickas. Försök igen eller ring {PHONE}.</p>
</form>
<div class="done" id="qdone" tabindex="-1" hidden>
  <h3>Tack för ditt meddelande</h3>
  <p>Vi återkommer så snart vi kan.</p>
  <button class="btn btn-line" type="button" id="qagain">Skicka ett nytt meddelande</button>
</div>'''


# --- Pages -------------------------------------------------------------------------------------------------------------
def build_index():
    divs = "".join(tile(f'{{root}}tjanster/index.html#{d["id"]}', d["photo"], d["title"], d["lead"]) for d in DIVISIONS)
    projects = "".join(project_card(p) for p in (PROJECTS[0], PROJECTS[2], PROJECTS[3]))
    main = f'''<section class="hero">
  {img("{root}", "hero-villa", "Villa i Stockholmsområdet", lazy=False)}
  <div class="wrap hero-in">
    <h1>Kvalitet som håller</h1>
    <p>Bygg och renovering för hem, fastigheter och företag i Stockholm.</p>
    {link("{root}tjanster/index.html", "Vår verksamhet", "lnk lnk-light")}
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <p class="statement">{NAME} är ett byggföretag med verksamhet i Stockholm. Vi hjälper privatpersoner och företag med allt från mindre renoveringar till större byggprojekt.</p>
    <div class="split-r">
      <p>Med fokus på kvalitet, tydlig kommunikation och ett professionellt arbetssätt strävar vi efter att leverera hållbara resultat och en smidig upplevelse genom hela projektet. Varje uppdrag planeras noggrant för att säkerställa ett slutresultat som motsvarar kundens förväntningar.</p>
      {link("{root}om-oss.html", "Om företaget")}
    </div>
  </div>
</section>

<section class="sec sec-top0">
  <div class="wrap">
    {section_head("Verksamhet", None, "{root}tjanster/index.html", "Alla tjänster")}
    <div class="tiles">{divs}</div>
  </div>
</section>

<section class="feature">
  <div class="feature-img">{img("{root}", "kok-ljust", "Renoverat kök i ljusa färger", "(min-width: 960px) 60vw, 100vw")}</div>
  <div class="feature-txt">
    <p class="k">Projekt, Haninge</p>
    <h2>Modern köksrenovering</h2>
    <p>Rivning, montering av kök och inredning samt målning, golv och ytskikt – ett funktionellt, modernt och hållbart kök som passar både bostaden och familjens behov.</p>
    {link("{root}projekt.html", "Se våra projekt")}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {section_head("Projekt", None, "{root}projekt.html", "Alla projekt")}
    <div class="pgrid">{projects}</div>
  </div>
</section>

<section class="sec sec-navy">
  <div class="wrap split">
    <h2>Så arbetar vi</h2>
    <ol class="steps">{"".join(f'<li><span class="n">{i:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS, 1))}</ol>
  </div>
</section>

<section class="duo">
  <a class="duo-it" href="{{root}}kunder.html">{img("{root}", "projektledning", "", "(min-width: 960px) 50vw, 100vw")}
    <span class="duo-txt"><span class="k">Kunder</span><span class="duo-t">För företag, fastighetsägare och bostadsrättsföreningar</span><span class="tile-l">Läs mer{ARROW}</span></span></a>
  <a class="duo-it" href="{{root}}karriar.html">{img("{root}", "stomme", "", "(min-width: 960px) 50vw, 100vw")}
    <span class="duo-txt"><span class="k">Karriär</span><span class="duo-t">Bygg din framtid hos Haninge Byggteam</span><span class="tile-l">Läs mer{ARROW}</span></span></a>
</section>

{contact_block()}'''
    page("index.html", f"{NAME} – bygg och renovering i Stockholm",
         f"{NAME} är ett byggföretag med verksamhet i Stockholm. Totalrenovering, kök, badrum, målning, golv, snickeri, tillbyggnad, betong och VVS för privatpersoner, företag och bostadsrättsföreningar.",
         main, "")


def build_services_index():
    blocks = []
    for i, d in enumerate(DIVISIONS):
        rows = "".join(f'<li><a href="{{root}}tjanster/{s["slug"]}.html"><span class="row-t">{s["title"]}</span><span class="row-p">{s["lead"]}</span>{ARROW}</a></li>'
                       for s in SERVICES if s["div"] == d["id"])
        blocks.append(f'''<section class="sec{" sec-grey" if i % 2 else ""}" id="{d["id"]}">
  <div class="wrap split">
    <div><h2>{d["title"]}</h2><p class="muted">{d["lead"]}</p></div>
    <ul class="rows">{rows}</ul>
  </div>
</section>''')
    main = f'''{page_head([("Verksamhet", "tjanster/index.html")], "Verksamhet", "Haninge Byggteam erbjuder bygg- och renoveringstjänster inom tre områden – för privatpersoner, företag och bostadsrättsföreningar i Stockholm och på Södertörn.", "stomme")}
{"".join(blocks)}
{contact_block()}'''
    page("tjanster/index.html", f"Verksamhet | {NAME}",
         "Renovering och ytskikt, bygg och snickeri, grund och installation. Haninge Byggteams tjänster i Stockholm och på Södertörn.",
         main, "verksamhet", "stomme")


def build_service(s):
    d = next(x for x in DIVISIONS if x["id"] == s["div"])
    body = "".join(f"<p>{p}</p>" for p in s["body"])
    scope = "".join(f"<li>{i}</li>" for i in s["items"])
    rel = "".join(f'<li><a href="{o["slug"]}.html"><span class="row-t">{o["title"]}</span>{ARROW}</a></li>' for o in SERVICES if o["div"] == s["div"] and o is not s)
    typ = quote_plus(s["title"])
    main = f'''{page_head([("Verksamhet", "tjanster/index.html"), (s["title"], "tjanster/" + s["slug"] + ".html")], s["title"], s["lead"], s["photo"])}
<section class="sec">
  <div class="wrap split">
    <div class="side">
      <p class="k">Område</p><p><a href="{{root}}tjanster/index.html#{d["id"]}">{d["title"]}</a></p>
      <p class="k">Omfattning</p><ul class="plain">{scope}</ul>
    </div>
    <div class="body">
      {body}
      <div class="contact-card">
        <p class="k">Kontakt</p>
        <p>Vill du veta mer eller boka ett hembesök? Kontakta oss på <a href="tel:{TEL}">{PHONE}</a> eller <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
        {button("{root}kontakt.html?typ=" + typ + "#formular", "Kontakta oss")}
      </div>
    </div>
  </div>
</section>
<section class="sec sec-grey">
  <div class="wrap split">
    <h2>Mer inom {d["title"].lower()}</h2>
    <ul class="rows">{rel}</ul>
  </div>
</section>'''
    page(f"tjanster/{s['slug']}.html", f"{s['title']} | {NAME}",
         f"{s['lead']} {NAME} utför {s['title'].lower()} i Stockholm, Haninge, Tyresö, Huddinge och Nacka.", main, "verksamhet", s["photo"])


def build_projects():
    tabs = "".join(f'<button type="button" class="tab" data-filter="{c}" aria-pressed="false">{c}</button>' for c in PROJECT_CATS)
    main = f'''{page_head([("Projekt", "projekt.html")], "Projekt", "Ett urval av våra uppdrag – totalrenoveringar, kök, badrum, målning och utvändiga arbeten i Stockholm och på Södertörn.")}
<section class="sec sec-top0">
  <div class="wrap">
    <div class="tabs" role="group" aria-label="Filtrera projekt"><button type="button" class="tab" data-filter="" aria-pressed="true">Alla</button>{tabs}</div>
    <div class="pgrid">{"".join(project_card(p) for p in PROJECTS)}</div>
  </div>
</section>
{contact_block()}'''
    page("projekt.html", f"Projekt | {NAME}",
         "Ett urval av Haninge Byggteams projekt: totalrenovering av villa, köksrenoveringar, badrum, altaner, målning och fasadarbeten.", main, "projekt")


def build_about():
    facts = [("Bolagsnamn", NAME), ("Organisationsnummer", ORG_NR), ("Säte", "Haninge"), ("Adress", f"{STREET}, {POSTAL} {CITY}"),
             ("Verksamhetsområde", ", ".join(AREAS)), ("Kunder", "Privatpersoner, företag och bostadsrättsföreningar")]
    rows = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in facts)
    vals = "".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in VALUES)
    main = f'''{page_head([("Om oss", "om-oss.html")], "Om Haninge Byggteam", "Ett byggföretag med verksamhet i Stockholm och på Södertörn.", "hero-villa")}
<section class="sec">
  <div class="wrap split">
    <p class="statement">Vi hjälper privatpersoner och företag med allt från mindre renoveringar till större byggprojekt.</p>
    <div class="split-r">
      <p>{NAME} är ett byggföretag med verksamhet i Stockholm som erbjuder bygg- och renoveringstjänster för privatpersoner och företag.</p>
      <p>Med fokus på kvalitet, tydlig kommunikation och ett professionellt arbetssätt strävar teamet efter att leverera hållbara resultat och en smidig upplevelse genom hela projektet. Varje uppdrag planeras noggrant för att säkerställa ett slutresultat som motsvarar kundens förväntningar.</p>
    </div>
  </div>
</section>
<section class="sec sec-grey">
  <div class="wrap split">
    <h2>Värderingar</h2>
    <ul class="values">{vals}</ul>
  </div>
</section>
<section class="sec">
  <div class="wrap split">
    <h2>Arbetssätt</h2>
    <ol class="steps steps-dark">{"".join(f'<li><span class="n">{i:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS, 1))}</ol>
  </div>
</section>
<section class="sec sec-grey" id="fakta">
  <div class="wrap split">
    <h2>Företagsfakta</h2>
    <dl class="facts">{rows}</dl>
  </div>
</section>
{contact_block()}'''
    page("om-oss.html", f"Om oss | {NAME}",
         f"{NAME} (org.nr {ORG_NR}) är ett byggföretag med verksamhet i Stockholm och på Södertörn.", main, "om-oss")


def build_customers():
    segs = [
        ("privat", "Privatpersoner", "Villa, radhus och bostadsrätt. Vi utför allt från enskilda badrum och kök till totalrenoveringar, tillbyggnader och altaner.", "badrum-modern"),
        ("foretag", "Företag och fastighetsägare", "Renovering av lokaler och lägenheter, ytskikt, håltagning och VVS. En kontaktperson och en tydlig offert med omfattning och pris.", "projektledning"),
        ("brf", "Bostadsrättsföreningar", "Badrum, målning, golv och åtgärder i gemensamma utrymmen, planerat i dialog med styrelsen och med hänsyn till de boende.", "malning-pagar"),
    ]
    blocks = "".join(f'''<section class="sec{" sec-grey" if i % 2 else ""}" id="{k}">
  <div class="wrap media{" media-rev" if i % 2 else ""}">
    <div class="media-img">{img("{root}", ph, "", "(min-width: 960px) 50vw, 100vw")}</div>
    <div class="media-txt"><h2>{t}</h2><p>{d}</p>{link("{root}kontakt.html#formular", "Kontakta oss")}</div>
  </div>
</section>''' for i, (k, t, d, ph) in enumerate(segs))
    main = f'''{page_head([("Kunder", "kunder.html")], "Kunder", "Vi arbetar för privatpersoner, företag, fastighetsägare och bostadsrättsföreningar i Stockholm och på Södertörn.")}
{blocks}
{contact_block()}'''
    page("kunder.html", f"Kunder | {NAME}",
         "Haninge Byggteam utför bygg- och renoveringsarbeten för privatpersoner, företag, fastighetsägare och bostadsrättsföreningar i Stockholm.", main, "kunder")


def build_career():
    main = f'''{page_head([("Karriär", "karriar.html")], "Karriär", "Vill du arbeta i ett byggteam där kvalitet och planering kommer först?", "stomme")}
<section class="sec">
  <div class="wrap split">
    <p class="statement">Vi tar gärna emot ansökningar från hantverkare inom bygg, snickeri, målning och plattsättning.</p>
    <div class="split-r">
      <p>Hos oss arbetar du med varierade uppdrag i Stockholm och på Södertörn – totalrenoveringar, kök, badrum och tillbyggnader – tillsammans med kollegor från flera yrkesgrupper.</p>
      <p>Skicka en kort presentation av dig själv och din erfarenhet till <a href="mailto:{EMAIL}?subject=Ans%C3%B6kan">{EMAIL}</a>.</p>
      {button("mailto:" + EMAIL + "?subject=Ans%C3%B6kan", "Skicka ansökan")}
    </div>
  </div>
</section>
<section class="sec sec-grey">
  <div class="wrap split">
    <h2>Våra värderingar</h2>
    <ul class="values">{"".join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in VALUES)}</ul>
  </div>
</section>'''
    page("karriar.html", f"Karriär | {NAME}",
         "Arbeta hos Haninge Byggteam. Vi tar emot ansökningar från hantverkare inom bygg, snickeri, målning och plattsättning.", main, "karriar", "stomme")


def build_contact():
    main = f'''{page_head([("Kontakt", "kontakt.html")], "Kontakt", "Kontakta oss för frågor, offert eller ett hembesök.")}
<section class="sec sec-top0">
  <div class="wrap split">
    <div class="side">
      <p class="k">Telefon</p><p><a href="tel:{TEL}">{PHONE}</a></p>
      <p class="k">E-post</p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="k">Besöksadress</p><p>{NAME}<br>{STREET}<br>{POSTAL} {CITY}</p>
      <p class="k">Öppettider</p><p>{HOURS}</p>
      <p class="k">Organisationsnummer</p><p>{ORG_NR}</p>
    </div>
    <div id="formular"><h2>Skicka ett meddelande</h2>{form()}</div>
  </div>
</section>
<div class="map"><iframe title="Karta: {E(ADDR)}" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'''
    page("kontakt.html", f"Kontakt | {NAME}", f"Kontakta {NAME}: {PHONE}, {EMAIL}, {ADDR}.", main, "kontakt")


def build_404():
    main = f'''<section class="phead nf"><div class="wrap"><h1>Sidan hittades inte</h1>
<p class="lead">Sidan kan ha flyttats eller tagits bort.</p>{link("{root}index.html", "Till startsidan")}</div></section>'''
    page("404.html", f"Sidan hittades inte | {NAME}", "Sidan finns inte.", main)
    # 404 can be served at any depth, so resolve its links from the site root.
    p = OUT / "404.html"
    base = SITE_URL.split("github.io")[-1] if "github.io" in SITE_URL else "/"
    p.write_text(p.read_text(encoding="utf-8").replace("<head>", f'<head>\n<base href="{base}">', 1), encoding="utf-8")


def build_meta():
    pages = ["", "tjanster/", "projekt.html", "kunder.html", "om-oss.html", "karriar.html", "kontakt.html"] + [f"tjanster/{s['slug']}.html" for s in SERVICES]
    urls = "".join(f"<url><loc>{SITE_URL}{p}</loc></url>" for p in pages)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    for f in OUT.rglob("*.html"):
        f.unlink()
    build_index()
    build_services_index()
    for s in SERVICES:
        build_service(s)
    build_projects()
    build_about()
    build_customers()
    build_career()
    build_contact()
    build_404()
    build_meta()
    print(f"Byggde {len(list(OUT.rglob('*.html')))} sidor i {OUT}/")
