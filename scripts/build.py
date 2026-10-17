"""Builds the Haninge Byggteam AB website into docs/.

Run:  python3 scripts/build.py docs

All text, services, projects, the review and the contact details live in this file. Edit here and rebuild; never edit
the generated HTML in docs/ by hand. Text marked "förslag" in README.md is suggested copy that Haninge Byggteam
should confirm before launch.
"""
import html
import json
import pathlib
import sys
from urllib.parse import quote_plus

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs")

# --- Company details (from haningebyggteam.se, the Google listing and the company van) --------------------------------
NAME = "Haninge Byggteam AB"
SHORT = "Haninge Byggteam"
ORG_NR = "559229-1115"
PHONE, TEL = "072-002 22 00", "+46720022200"
EMAIL = "info@haningebyggteam.se"
STREET, POSTAL, CITY = "Albybergsringen 105", "137 69", "Österhaninge"
ADDR = f"{STREET}, {POSTAL} {CITY}"
HOURS = "Mån–fre 07:00–16:30"
RATING, REVIEW_COUNT = "5,0", 2
AREAS = ["Haninge", "Stockholm", "Tyresö", "Huddinge", "Nacka"]
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{NAME}, {STREET}, {POSTAL}")
MAP_EMBED = "https://www.google.com/maps?q=" + quote_plus(f"{STREET}, {POSTAL} Haninge") + "&z=14&hl=sv&output=embed"

# The quote form e-mails through FormSubmit. Elevate Studio receives the requests during the preview; at launch this
# becomes Haninge Byggteam's own address. The first request to a new address only sends an activation e-mail.
FORM_EMAIL = "elevate.studio018@gmail.com"

SITE_URL = "https://elevatestudio018.github.io/HB-AB/"

# --- Business areas and services --------------------------------------------------------------------------------------
# The ten services and their texts come from haningebyggteam.se. The grouping into three business areas, the
# "Det här ingår" lists and the leads are new and should be confirmed (see README).
DIVISIONS = [
    dict(id="renovering", num="01", title="Renovering & ytskikt",
         lead="Hela bostäder, kök och badrum – från rivning till sista strykningen.",
         photo="kok-ljust"),
    dict(id="bygg", num="02", title="Bygg & snickeri",
         lead="Snickeri, inredning, dörrar, fönster, tak och tillbyggnader.",
         photo="fasad-team"),
    dict(id="teknik", num="03", title="Grund & installation",
         lead="Betong, håltagning, rivning samt vatten och avlopp.",
         photo="betong"),
]

SERVICES = [
    dict(slug="totalrenovering", div="renovering", title="Totalrenovering", photo="rivning", stock=True,
         lead="Kompletta totalrenoveringar från idé till färdigt resultat.",
         short="Bostäder, villor och fastigheter – vi samordnar hela renoveringen.",
         body=["Vi hjälper dig med totalrenovering av bostäder, villor och andra fastigheter i hela projektets omfattning. Från rivning och grundarbete till målning, golvläggning, snickeri och färdiga ytskikt – vi samordnar arbetet för en smidig renoveringsprocess och ett resultat som håller över tid.",
               "Du har en kontaktperson genom hela projektet och en tydlig tidsplan innan vi börjar."],
         items=["Rivning och grundarbete", "Ny planlösning och innerväggar", "Kök och badrum", "Golv, kakel och klinker",
                "Målning och ytskikt", "Snickeri och slutfinish"]),
    dict(slug="koksrenovering", div="renovering", title="Köksrenovering", photo="kok-ek",
         lead="Ge köket ett nytt liv med en genomtänkt köksrenovering.",
         short="Rivning, montering av kök och inredning, golv och ytskikt.",
         body=["Vi erbjuder kompletta köksrenoveringar där vi hjälper till med rivning, montering av kök och inredning samt målning, golv och andra ytskikt. Målet är att skapa ett funktionellt, modernt och hållbart kök som passar både bostaden och dina behov."],
         items=["Rivning av befintligt kök", "Montering av stommar, luckor och bänkskivor", "Vatten och avlopp till disk och vitvaror",
                "Kakel och stänkskydd", "Golv, målning och lister"]),
    dict(slug="badrumsrenovering", div="renovering", title="Badrumsrenovering", photo="badrum-modern",
         lead="Professionell badrumsrenovering med fokus på kvalitet och hållbarhet.",
         short="Från rivning och tätskikt till kakel, klinker och montering.",
         body=["Vi utför kompletta badrumsrenoveringar med allt från rivning och förberedande arbeten till tätskikt, kakel, klinker och montering. Oavsett om du vill renovera ett mindre badrum eller skapa ett helt nytt modernt badrum hjälper vi dig genom hela projektet."],
         items=["Rivning och förberedande arbeten", "Tätskikt", "Kakel och klinker", "Golvbrunn och rördragning",
                "Montering av porslin, dusch och badrumsmöbler"]),
    dict(slug="malning-och-ytskikt", div="renovering", title="Målning & ytskikt", photo="malning-pagar",
         lead="Jämna, hållbara ytor och ett fräscht uttryck i hela bostaden.",
         short="Målning, spackling, gips och andra ytskikt.",
         body=["Vi utför professionell målning, spackling, gipsarbeten och andra ytskiktsarbeten för både mindre och större renoveringar. Med noggrant underarbete och rätt material skapar vi jämna och hållbara ytor.",
               "En ny färg eller nya ytskikt kan ge hela bostaden ett fräscht och modernt uttryck."],
         items=["Målning av väggar och tak", "Spackling och slipning", "Gipsarbeten", "Tapetsering", "Snickerimålning"]),
    dict(slug="golv-kakel-klinker", div="renovering", title="Golv, kakel & klinker", photo="hall-trappa",
         lead="Golv och plattsättning med noggranna förberedelser.",
         short="Parkett, laminat, vinyl samt kakel och klinker.",
         body=["Vi erbjuder professionell golvläggning samt kakel- och klinkerarbeten för bostäder och andra lokaler. Vi lägger bland annat parkett, laminat och vinyl samt sätter kakel och klinker i kök, badrum och andra utrymmen.",
               "Noggranna förberedelser och ett professionellt utförande ger ett snyggt och hållbart resultat."],
         items=["Parkett och laminat", "Vinylgolv", "Kakel på vägg", "Klinker på golv", "Avjämning och underarbete"]),
    dict(slug="snickeri-och-inredning", div="bygg", title="Snickeri & inredning", photo="snickeri", stock=True,
         lead="Funktionella och stilrena snickeridetaljer.",
         short="Köksmontering, specialanpassade lösningar och snickeridetaljer.",
         body=["Vi utför snickeriarbeten och monterar inredning för både små och stora renoveringsprojekt. Det kan handla om allt från köksmontering och dörrar till fönster, specialanpassade lösningar och andra snickeridetaljer.",
               "Vi arbetar noggrant med detaljerna för att skapa funktionella och stilrena resultat."],
         items=["Köks- och inredningsmontering", "Platsbyggd förvaring", "Lister, foder och socklar", "Innerväggar och regelverk",
                "Specialanpassade lösningar"]),
    dict(slug="dorrar-fonster-tak", div="bygg", title="Dörrar, fönster & tak", photo="dorr", stock=True,
         lead="Bättre utseende och funktion – anpassat efter fastigheten.",
         short="Byte och montering av dörrar och fönster, innertak och undertak.",
         body=["Vi hjälper dig med byte och montering av dörrar och fönster samt arbeten med innertak och undertak. Genom att uppdatera dessa delar kan du förbättra både bostadens utseende och funktion.",
               "Vi utför arbetet noggrant och anpassar lösningen efter fastighetens förutsättningar och dina önskemål."],
         items=["Byte av innerdörrar och ytterdörrar", "Fönsterbyte och montering", "Innertak och undertak", "Karmar, foder och tätning"]),
    dict(slug="om-tillbyggnad-utomhus", div="bygg", title="Om-, tillbyggnad & utomhus", photo="altan",
         lead="Utveckla både bostaden och utemiljön.",
         short="Ombyggnationer, tillbyggnader, altaner, trädäck, staket och fasad.",
         body=["Vi hjälper dig att utveckla och förbättra både bostaden och utemiljön genom ombyggnationer, tillbyggnader och utvändiga snickeriarbeten. Vi utför bland annat altaner, trädäck, staket och fasadarbeten.",
               "Varje projekt anpassas efter fastighetens förutsättningar och dina önskemål för ett funktionellt och hållbart resultat."],
         items=["Ombyggnad och ny planlösning", "Tillbyggnader", "Altaner och trädäck", "Staket och plank", "Fasadarbeten"]),
    dict(slug="betong-rivning-haltagning", div="teknik", title="Betong, rivning & håltagning", photo="betong", stock=True,
         lead="Rätt förutsättningar för resten av byggprojektet.",
         short="Gjutning, bilning, håltagning samt rivning och återställning.",
         body=["Vi utför betongarbeten, gjutning, bilning, håltagning samt rivnings- och återställningsarbeten. Dessa arbeten är ofta viktiga delar av större renoveringar och ombyggnationer.",
               "Med ett effektivt och noggrant utförande skapar vi rätt förutsättningar för det fortsatta byggprojektet."],
         items=["Betongarbeten och gjutning", "Bilning", "Håltagning", "Rivning", "Återställningsarbeten"]),
    dict(slug="vvs-och-ledningsarbeten", div="teknik", title="VVS & ledningsarbeten", photo="vvs", stock=True,
         lead="Vatten och avlopp, samordnat med resten av projektet.",
         short="Byte och anpassning av vatten- och avloppsledningar.",
         body=["Vi utför arbeten inom vatten och avlopp i samband med renoveringar, ombyggnationer och andra byggprojekt. Det kan bland annat innebära byte och anpassning av vatten- och avloppsledningar.",
               "Vi hjälper till att skapa funktionella lösningar och samordnar arbetet med projektets övriga moment."],
         items=["Byte av vatten- och avloppsledningar", "Anpassning vid ombyggnad", "Rördragning i kök och badrum",
                "Samordning med övriga moment"]),
]
SVC = {s["slug"]: s for s in SERVICES}
WORK_TYPES = ["Totalrenovering", "Köksrenovering", "Badrumsrenovering", "Målning & ytskikt", "Golv, kakel & klinker",
              "Snickeri & inredning", "Dörrar, fönster & tak", "Om-, tillbyggnad & utomhus",
              "Betong, rivning & håltagning", "VVS & ledningsarbeten", "Annat"]

# Stock photos from Pexels are captioned as illustrations. The rest come from haningebyggteam.se.
STOCK = {"rivning", "stomme", "takstol", "dorr", "snickeri", "inredning", "betong", "vvs", "projektledning", "kok-vitt"}

# --- Projects (the three named ones and the categories come from haningebyggteam.se/projekt) --------------------------
PROJECTS = [
    dict(title="Modern köksrenovering", cat="Kök", place="Haninge", photo="kok-ljust"),
    dict(title="Totalrenovering av villa", cat="Totalrenovering", place="Stockholm", photo="hero-villa"),
    dict(title="Ny altan i trä", cat="Utomhus", place="Tyresö", photo="altan"),
    dict(title="Fasadarbete", cat="Tillbyggnad", place="", photo="fasad-team"),
    dict(title="Badrum", cat="Badrum", place="", photo="badrum-klart"),
    dict(title="Målning", cat="Målning", place="", photo="malning-pagar"),
    dict(title="Badrum", cat="Badrum", place="", photo="badrum-modern"),
    dict(title="Kök", cat="Kök", place="", photo="kok-ek"),
    dict(title="Hall och trappa", cat="Målning", place="", photo="hall-trappa"),
]
PROJECT_CATS = ["Kök", "Badrum", "Totalrenovering", "Utomhus", "Målning", "Tillbyggnad"]

# --- Review (copied exactly from haningebyggteam.se) -------------------------------------------------------------------
REVIEW = dict(
    name="Ihtik AlimJanov",
    text="Jag är mycket nöjd med Haninge Byggteam AB. Arbetet utfördes professionellt, med hög kvalitet och enligt överenskommen tidsplan. Trevlig personal, bra kommunikation och ett resultat som överträffade mina förväntningar. Rekommenderas varmt till den som söker ett pålitligt byggföretag.",
)

STEPS = [
    ("Kontakt", "Du kontaktar oss och berättar om ditt projekt eller dina önskemål. Vi går igenom dina behov och bokar nästa steg."),
    ("Kostnadsfritt hembesök", "Vi träffas på plats för att titta på projektet och diskutera olika lösningar. Besöket ger ett bra underlag inför offert."),
    ("Fast offert", "Du får en tydlig offert med omfattning och pris innan arbetet påbörjas. Eventuella frågor besvaras innan beslut fattas."),
    ("Renovering", "Arbetet utförs enligt överenskommelse och med löpande dialog under projektets gång. När arbetet är klart görs en gemensam genomgång."),
]

# Values: quality, clear communication, a professional way of working and careful planning are all named on the old site.
VALUES = [
    ("Kvalitet som håller", "Rätt material, noggrant underarbete och ett utförande som ska hålla i många år."),
    ("Tydlig kommunikation", "En kontaktperson, löpande dialog och inga överraskningar under projektets gång."),
    ("Professionellt arbetssätt", "Ordning på arbetsplatsen, respekt för ditt hem och överenskomna tider."),
    ("Noggrann planering", "Varje uppdrag planeras så att slutresultatet motsvarar dina förväntningar."),
]

SEGMENTS = [
    ("Privatpersoner", "Villa, radhus och bostadsrätt – från ett nytt badrum till en totalrenovering av hela hemmet.", "index.html#offert", "Begär offert"),
    ("Företag & fastighetsägare", "Renovering av lokaler och lägenheter, ytskikt, håltagning och VVS – med en kontaktperson och fasta priser.", "foretag.html", "För företag"),
    ("Bostadsrättsföreningar", "Badrum, målning och åtgärder i gemensamma utrymmen, planerat med hänsyn till de boende.", "foretag.html#brf", "För BRF"),
]

FAQ = [
    ("Vilka områden arbetar ni i?", "Vi utför bygg- och renoveringsarbeten i Stockholm och närliggande områden – bland annat Haninge, Tyresö, Huddinge och Nacka."),
    ("Hur kontaktar jag er?", f'Ring oss på <a href="tel:{TEL}">{PHONE}</a>, mejla <a href="mailto:{EMAIL}">{EMAIL}</a> eller fyll i <a href="{{root}}kontakt.html#offert">offertformuläret</a>.'),
    ("Erbjuder ni kostnadsfri offert?", "Ja, kontakta oss så bokar vi ett kostnadsfritt möte och går igenom ditt projekt."),
    ("Vilka tjänster erbjuder ni?", "Vi erbjuder bland annat totalrenoveringar, köksrenoveringar, badrumsrenoveringar, tillbyggnader och altanbyggen – och dessutom målning, golv, snickeri, dörrar och fönster, VVS samt betong och håltagning."),
    ("Hur lång tid tar ett byggprojekt?", "Tidsplanen varierar beroende på projektets omfattning. En tydlig tidsplan presenteras alltid innan arbetet påbörjas."),
    ("Kan jag använda ROT-avdrag?", "ROT-avdraget gäller arbetskostnaden för många renoverings- och ombyggnadsarbeten i bostaden. Vi går igenom vad som gäller för ditt projekt i offerten."),
]

# --- Markup helpers ----------------------------------------------------------------------------------------------------
E = html.escape


def icon(name, cls="ic"):
    paths = {
        "phone": '<path d="M21 16.5v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.1 3.8 2 2 0 0 1 3.1 1.6h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L7.1 9.5a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
        "mail": '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/><path d="m3 6 9 7 9-7"/>',
        "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
        "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
        "home": '<path d="m3 11 9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
        "chev": '<path d="m6 9 6 6 6-6"/>',
        "building": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1M10 21v-3h4v3"/>',
        "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14a6.5 6.5 0 0 1 3.5 6"/>',
        "shield": '<path d="M12 3 4.5 6v6c0 4.5 3.2 7.8 7.5 9 4.3-1.2 7.5-4.5 7.5-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-4.5"/>',
    }
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="m10 1.6 2.6 5.4 5.9.8-4.3 4.1 1 5.9L10 15l-5.2 2.8 1-5.9L1.5 7.8l5.9-.8z"/></svg>'


def stars(n=5):
    return f'<span class="stars" role="img" aria-label="{n} av 5 stjärnor">{STAR * n}</span>'


def img(root, src, alt="", pos="50% 50%", sizes="100vw", lazy=True):
    return (f'<img src="{root}img/{src}.jpg" srcset="{root}img/{src}-s.jpg 800w, {root}img/{src}.jpg 1800w" sizes="{sizes}" '
            f'alt="{E(alt)}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async" style="object-position:{pos}">')


def photo(root, src, alt, cls="ph", pos="50% 50%", sizes="(min-width: 960px) 50vw, 100vw"):
    cap = '<figcaption>Illustrationsbild</figcaption>' if src in STOCK else ""
    return f'<figure class="{cls}">{img(root, src, alt, pos, sizes)}{cap}</figure>'


def logo(light=False):
    """Word mark after the lettering on the company van: HANINGE / BYGGTEAM AB / — CONSTRUCTION —."""
    return (f'<span class="logo-mark" aria-hidden="true">HB</span>'
            f'<span class="logo-word{" light" if light else ""}"><b>HANINGE</b><span>BYGGTEAM AB</span><i>Construction</i></span>')


def btn(href, label, cls="btn-y", ic=None):
    return f'<a class="btn {cls}" href="{href}">{icon(ic) if ic else ""}<span>{label}</span></a>'


def call(cls="btn-y", label=None):
    return btn(f"tel:{TEL}", label or PHONE, cls, "phone")


def eyebrow(text, light=False):
    return f'<p class="eyebrow{" light" if light else ""}">{text}</p>'


# --- Header and footer -------------------------------------------------------------------------------------------------
NAV = [("start", "Start", "index.html"), ("tjanster", "Tjänster", "tjanster/index.html"), ("projekt", "Projekt", "projekt.html"),
       ("foretag", "Företag & BRF", "foretag.html"), ("om-oss", "Om oss", "om-oss.html"), ("kontakt", "Kontakt", "kontakt.html")]


def header(root, active):
    def svc_col(d):
        rows = "".join(f'<li><a href="{root}tjanster/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES if s["div"] == d["id"])
        return f'<div class="mega-col"><p class="mega-h"><span>{d["num"]}</span>{d["title"]}</p><ul>{rows}</ul></div>'

    mega = "".join(svc_col(d) for d in DIVISIONS)
    links = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        if key == "tjanster":
            links.append(
                f'<div class="has-mega"><a href="{root}{href}"{cur}>{label}</a>'
                f'<button class="mega-btn" type="button" aria-expanded="false" aria-controls="mega" aria-label="Visa tjänster">{icon("chev")}</button>'
                f'<div class="mega" id="mega"><div class="mega-in">{mega}'
                f'<div class="mega-cta"><p class="mega-h">Kostnadsfritt hembesök</p><p>Vi kommer ut, tittar på projektet och lämnar en fast offert.</p>'
                f'{btn(root + "kontakt.html#offert", "Begär offert", "btn-y btn-sm")}</div></div></div></div>')
        else:
            links.append(f'<a href="{root}{href}"{cur}>{label}</a>')
    menu_main = "".join(f'<li><a href="{root}{h}">{l}</a></li>' for _, l, h in NAV)
    menu_svc = "".join(f'<li><a href="{root}tjanster/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    return f'''<a class="skip" href="#main">Hoppa till innehållet</a>
<div class="topbar">
  <div class="wrap topbar-in">
    <span>{icon("pin")}Stockholm &amp; Södertörn</span>
    <span class="tb-hide">{icon("clock")}{HOURS}</span>
    <span class="tb-hide">Org.nr {ORG_NR}</span>
    <span class="tb-right"><a href="{root}foretag.html">För företag</a><a href="{root}karriar.html">Karriär</a><a href="mailto:{EMAIL}">{EMAIL}</a></span>
  </div>
</div>
<header class="head" id="top">
  <div class="wrap bar">
    <a class="logo" href="{root}index.html" aria-label="{NAME}, till startsidan">{logo()}</a>
    <nav class="nav" aria-label="Huvudmeny">{"".join(links)}</nav>
    <div class="head-cta">
      <a class="head-phone" href="tel:{TEL}">{icon("phone")}<span><small>Ring oss</small>{PHONE}</span></a>
      {btn(root + "kontakt.html#offert", "Gratis offert", "btn-y btn-sm")}
    </div>
    <a class="round head-round" href="tel:{TEL}" aria-label="Ring {PHONE}">{icon("phone")}</a>
    <button class="burger" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Meny"><span></span><span></span></button>
  </div>
  <nav class="menu" id="menu" aria-label="Meny" hidden>
    <div class="wrap">
      <ul class="menu-main">{menu_main}</ul>
      <p class="menu-h">Tjänster</p><ul class="menu-svc">{menu_svc}</ul>
      <div class="menu-cta">{call()}{btn(root + "kontakt.html#offert", "Begär offert", "btn-navy")}</div>
    </div>
  </nav>
</header>'''


def footer(root):
    def col(d):
        return "".join(f'<li><a href="{root}tjanster/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES if s["div"] == d["id"])

    return f'''<section class="cta-band">
  <div class="wrap cta-in">
    <div><p class="cta-k">Redo att starta ditt byggprojekt?</p><p class="cta-s">Kostnadsfritt hembesök och fast offert – ring eller skicka en förfrågan.</p></div>
    <div class="cta-btns">{call("btn-navy")}{btn(root + "kontakt.html#offert", "Få gratis offert", "btn-line-navy")}</div>
  </div>
</section>
<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <a class="logo" href="{root}index.html" aria-label="{NAME}, till startsidan">{logo(light=True)}</a>
      <p class="foot-about">{NAME} är ett byggföretag med verksamhet i Stockholm som erbjuder bygg- och renoveringstjänster för privatpersoner, företag och bostadsrättsföreningar.</p>
    </div>
    <div class="foot-grid">
      <div>
        <p class="foot-h">Kontakt</p>
        <ul class="foot-contact">
          <li><a href="tel:{TEL}">{icon("phone")}{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{icon("mail")}{EMAIL}</a></li>
          <li><a href="{MAPS_LINK}" target="_blank" rel="noopener">{icon("pin")}{STREET}<br>{POSTAL} {CITY}</a></li>
          <li><span>{icon("clock")}{HOURS}</span></li>
        </ul>
      </div>
      <div><p class="foot-h">Renovering &amp; ytskikt</p><ul>{col(DIVISIONS[0])}</ul></div>
      <div><p class="foot-h">Bygg, grund &amp; installation</p><ul>{col(DIVISIONS[1])}{col(DIVISIONS[2])}</ul></div>
      <div>
        <p class="foot-h">Företaget</p>
        <ul><li><a href="{root}om-oss.html">Om oss</a></li><li><a href="{root}projekt.html">Projekt</a></li><li><a href="{root}foretag.html">Företag &amp; BRF</a></li><li><a href="{root}karriar.html">Karriär</a></li><li><a href="{root}kontakt.html">Kontakt</a></li></ul>
        <p class="foot-h foot-h2">Områden</p>
        <p class="foot-areas">{" · ".join(AREAS)}</p>
      </div>
    </div>
    <div class="foot-end">
      <span>© <span data-year>2026</span> {NAME} · Org.nr {ORG_NR}</span>
      <a href="https://www.elevatestudio.nu" target="_blank" rel="noopener">Byggd av Elevate Studio</a>
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
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": 5, "reviewCount": REVIEW_COUNT},
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..900&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
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


# --- Shared sections ---------------------------------------------------------------------------------------------------
def page_hero(crumbs, title, lead, photo_name, eyebrow_text=None, cta=True):
    trail = "".join(f'<li><a href="{{root}}{h}">{t}</a></li>' for t, h in crumbs)
    stock = '<span class="hero-cap">Illustrationsbild</span>' if photo_name in STOCK else ""
    btns = (f'<div class="hero-btns">{btn("{root}kontakt.html#offert", "Få gratis offert", "btn-y")}{call("btn-ghost")}</div>' if cta else "")
    return f'''<section class="phero">
  {img("{root}", photo_name, "", lazy=False)}{stock}
  <div class="wrap phero-in">
    <nav aria-label="Brödsmulor"><ol class="crumbs"><li><a href="{{root}}index.html">Start</a></li>{trail}</ol></nav>
    {eyebrow(eyebrow_text, True) if eyebrow_text else ""}
    <h1>{title}</h1>
    <p class="phero-lead">{lead}</p>
    {btns}
  </div>
</section>'''


def facts_strip():
    return f'''<div class="facts">
  <div class="fact"><b>{RATING}</b><span>{stars()}Google-betyg</span></div>
  <div class="fact"><b>10</b><span>tjänsteområden under ett tak</span></div>
  <div class="fact"><b>0 kr</b><span>för hembesök och offert</span></div>
  <div class="fact"><b>Fast</b><span>pris innan arbetet börjar</span></div>
</div>'''


def divisions_section(heading=True):
    cards = []
    for d in DIVISIONS:
        rows = "".join(f'<li><a href="{{root}}tjanster/{s["slug"]}.html">{s["title"]}{icon("arrow")}</a></li>' for s in SERVICES if s["div"] == d["id"])
        cards.append(f'''<article class="div-card" id="{d["id"]}">
  {photo("{root}", d["photo"], "", "div-ph", sizes="(min-width: 960px) 33vw, 100vw")}
  <div class="div-body">
    <p class="div-num">{d["num"]}</p>
    <h3>{d["title"]}</h3>
    <p>{d["lead"]}</p>
    <ul class="div-list">{rows}</ul>
  </div>
</article>''')
    head = f'''<div class="sec-head">
    {eyebrow("Affärsområden")}
    <h2>Ett byggteam – tre affärsområden</h2>
    <p>Vi samlar hantverkarna under ett tak. Du får en kontaktperson, en tidsplan och en offert – oavsett hur många yrkesgrupper projektet kräver.</p>
  </div>''' if heading else ""
    return f'''<section class="sec" id="tjanster">
  <div class="wrap">
  {head}
  <div class="div-grid">{"".join(cards)}</div>
  </div>
</section>'''


def process_section(dark=False):
    steps = "".join(f'<li><span class="step-n">{i:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS, 1))
    return f'''<section class="sec{" sec-navy" if dark else " sec-soft"}" id="arbetsgang">
  <div class="wrap">
    <div class="sec-head">{eyebrow("Så arbetar vi", dark)}<h2>Från första samtal till färdigt resultat</h2>
    <p>Samma tydliga process i varje uppdrag – stort som litet.</p></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>'''


def values_section():
    cards = "".join(f'<li>{icon("shield")}<h3>{t}</h3><p>{d}</p></li>' for t, d in VALUES)
    return f'''<section class="sec sec-navy" id="ledord">
  <div class="wrap">
    <div class="sec-head">{eyebrow("Våra ledord", True)}<h2>Det här står Haninge Byggteam för</h2></div>
    <ul class="values">{cards}</ul>
  </div>
</section>'''


def review_section():
    return f'''<section class="sec" id="omdomen">
  <div class="wrap review-wrap">
    <div class="review-score">
      {eyebrow("Vad kunderna säger")}
      <p class="score"><b>{RATING}</b><span>av 5</span></p>
      {stars()}
      <p class="muted">Snittbetyg på Google, baserat på {REVIEW_COUNT} recensioner.</p>
    </div>
    <figure class="review">
      <blockquote><p>”{REVIEW["text"]}”</p></blockquote>
      <figcaption><span class="avatar" aria-hidden="true">{REVIEW["name"][0]}</span><span><b>{REVIEW["name"]}</b><small>{stars()} Google-recension</small></span></figcaption>
    </figure>
  </div>
</section>'''


def faq_section():
    items = "".join(f'<details><summary>{q}{icon("chev")}</summary><div><p>{a}</p></div></details>' for q, a in FAQ)
    return f'''<section class="sec sec-soft" id="fragor">
  <div class="wrap faq-wrap">
    <div class="sec-head left">{eyebrow("Vanliga frågor")}<h2>Bra att veta</h2>
    <p>Hittar du inte svaret? Ring <a href="tel:{TEL}">{PHONE}</a> så hjälper vi dig.</p></div>
    <div class="faq">{items}</div>
  </div>
</section>'''


def quote_form():
    opts = "".join(f"<option>{E(t)}</option>" for t in WORK_TYPES)
    return f'''<div class="qbox">
  <form id="qform" class="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{FORM_EMAIL}">
    <p class="q-h">Begär kostnadsfri offert</p>
    <p class="q-s">Svar inom en arbetsdag. Fält märkta * är obligatoriska.</p>
    <div class="row2">
      <div class="field"><label for="f-namn">Namn *</label><input id="f-namn" name="namn" autocomplete="name" required>
        <p class="err" id="e-namn" hidden>Skriv ditt namn.</p></div>
      <div class="field"><label for="f-tel">Telefon *</label><input id="f-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel">
        <p class="err" id="e-tel" hidden>Fyll i telefon eller e-post så att vi kan nå dig.</p></div>
    </div>
    <div class="row2">
      <div class="field"><label for="f-epost">E-post</label><input id="f-epost" name="epost" type="email" autocomplete="email">
        <p class="err" id="e-epost" hidden>Kontrollera e-postadressen.</p></div>
      <div class="field"><label for="f-typ">Typ av uppdrag</label><select id="f-typ" name="typ"><option value="">Välj typ</option>{opts}</select></div>
    </div>
    <div class="field"><label for="f-ort">Ort</label><input id="f-ort" name="ort" autocomplete="address-level2" placeholder="T.ex. Haninge, Tyresö, Nacka"></div>
    <div class="field"><label for="f-besk">Kort beskrivning</label><textarea id="f-besk" name="besk" rows="4" placeholder="Berätta kort om projektet – storlek, önskemål och när du vill starta."></textarea></div>
    <div class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="web" tabindex="-1" autocomplete="off"></div>
    <button class="btn btn-y btn-full" type="submit">Skicka förfrågan</button>
    <p class="err send-err" id="send-err" role="alert" hidden>Förfrågan kunde inte skickas. Försök igen eller ring <a href="tel:{TEL}">{PHONE}</a>.</p>
    <p class="q-fine">Vi använder uppgifterna bara för att besvara din förfrågan.</p>
  </form>
  <div class="qdone" id="qdone" tabindex="-1" hidden>
    <span class="qdone-ic">{icon("check")}</span>
    <p class="q-h">Tack! Vi återkommer strax.</p>
    <p>Vi hör av oss inom en arbetsdag. Brådskar det? Ring <a href="tel:{TEL}">{PHONE}</a>.</p>
    <button class="btn btn-line-navy" type="button" id="qagain">Skicka en till</button>
  </div>
</div>'''


def contact_section(title="Kontakta oss", with_map=True):
    mp = (f'<div class="map"><iframe title="Karta: {E(ADDR)}" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
          if with_map else "")
    return f'''<section class="sec" id="offert">
  <div class="wrap contact">
    <div class="contact-info">
      {eyebrow("Kontakt")}
      <h2>{title}</h2>
      <p>Berätta om ditt projekt så bokar vi ett kostnadsfritt hembesök. Du får en fast offert med omfattning och pris innan något arbete påbörjas.</p>
      <ul class="clist">
        <li>{icon("phone")}<span><small>Telefon</small><a href="tel:{TEL}">{PHONE}</a></span></li>
        <li>{icon("mail")}<span><small>E-post</small><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
        <li>{icon("pin")}<span><small>Adress</small><a href="{MAPS_LINK}" target="_blank" rel="noopener">{ADDR}</a></span></li>
        <li>{icon("clock")}<span><small>Öppettider</small>{HOURS}</span></li>
      </ul>
      {mp}
    </div>
    {quote_form()}
  </div>
</section>'''


def gallery(items, filters=True):
    cats = "".join(f'<button type="button" class="chip" data-filter="{c}" aria-pressed="false">{c}</button>' for c in PROJECT_CATS)
    bar = (f'<div class="chips" role="group" aria-label="Filtrera projekt"><button type="button" class="chip" data-filter="" aria-pressed="true">Alla</button>{cats}</div>'
           if filters else "")
    cards = "".join(
        f'<figure class="pcard" data-cat="{p["cat"]}">{img("{root}", p["photo"], p["title"], sizes="(min-width: 960px) 33vw, (min-width: 600px) 50vw, 100vw")}'
        f'<figcaption><b>{p["title"]}</b><span>{p["cat"]}{" · " + p["place"] if p["place"] else ""}</span></figcaption></figure>'
        for p in items)
    return f'{bar}<div class="pgrid">{cards}</div>'


def seo_text():
    links = ", ".join(f'<a href="{{root}}tjanster/{s["slug"]}.html">{s["title"].lower()}</a>' for s in SERVICES[:5])
    return f'''<section class="sec seo">
  <div class="wrap seo-in">
    <h2>Byggfirma i Haninge och Stockholm</h2>
    <p>{NAME} är ett byggföretag med säte i Österhaninge och verksamhet i hela Stockholm och på Södertörn. Vi hjälper privatpersoner, företag och bostadsrättsföreningar med allt från mindre renoveringar till större byggprojekt – bland annat {links}.</p>
    <p>Vi arbetar i {", ".join(AREAS[:-1])} och {AREAS[-1]} med omnejd. Varje uppdrag planeras noggrant, och du får alltid en fast offert och en tydlig tidsplan innan vi börjar.</p>
  </div>
</section>'''


# --- Pages -------------------------------------------------------------------------------------------------------------
def build_index():
    real = [("fasad-team", "Fasadarbete med ställning"), ("malning-pagar", "Målning av ett rum"),
            ("badrum-klart", "Färdigt badrum med kakel"), ("servicebil", "Haninge Byggteams servicebil")]
    reel = "".join(f'<figure class="reel-it">{img("{root}", p, a, sizes="(min-width: 960px) 25vw, 50vw")}</figure>' for p, a in real)
    segs = "".join(f'<article class="seg">{icon(ic)}<h3>{t}</h3><p>{d}</p><a class="more" href="{{root}}{h}">{l}{icon("arrow")}</a></article>'
                   for (t, d, h, l), ic in zip(SEGMENTS, ["home", "building", "users"]))
    main = f'''<section class="hero">
  {img("{root}", "hero-villa", "Vit villa med pool och trädäck i kvällsljus", lazy=False)}
  <div class="wrap hero-in">
    <p class="hero-badge">{stars()}<span>{RATING} på Google · Stockholm &amp; Södertörn</span></p>
    <h1>Kvalitet som håller.<br><span>Ett byggteam för hela projektet.</span></h1>
    <p class="hero-lead">Kompletta bygg- och renoveringslösningar för privatpersoner, företag och bostadsrättsföreningar – från badrum och kök till totalrenoveringar och tillbyggnader.</p>
    <div class="hero-btns">{btn("{root}kontakt.html#offert", "Få gratis offert", "btn-y")}{call("btn-ghost")}</div>
  </div>
  <div class="wrap hero-facts">{facts_strip()}</div>
</section>

<section class="sec intro">
  <div class="wrap intro-grid">
    <div>
      {eyebrow("Om Haninge Byggteam")}
      <h2>Byggföretag med verksamhet i Stockholm</h2>
      <p class="big">{NAME} hjälper privatpersoner och företag med allt från mindre renoveringar till större byggprojekt.</p>
      <p>Med fokus på kvalitet, tydlig kommunikation och ett professionellt arbetssätt strävar teamet efter att leverera hållbara resultat och en smidig upplevelse genom hela projektet. Varje uppdrag planeras noggrant för att säkerställa ett slutresultat som motsvarar kundens förväntningar.</p>
      <a class="more" href="{{root}}om-oss.html">Läs mer om oss{icon("arrow")}</a>
    </div>
    <aside class="keyfacts" aria-label="Företaget i korthet">
      <p class="kf-h">Företaget i korthet</p>
      <dl>
        <div><dt>Bolag</dt><dd>{NAME}</dd></div>
        <div><dt>Org.nr</dt><dd>{ORG_NR}</dd></div>
        <div><dt>Säte</dt><dd>Österhaninge</dd></div>
        <div><dt>Marknad</dt><dd>Stockholm &amp; Södertörn</dd></div>
        <div><dt>Kunder</dt><dd>Privat, företag &amp; BRF</dd></div>
        <div><dt>Öppettider</dt><dd>{HOURS}</dd></div>
      </dl>
    </aside>
  </div>
</section>

{divisions_section()}

<section class="sec sec-soft reel-sec">
  <div class="wrap">
    <div class="sec-head">{eyebrow("På plats")}<h2>Från våra arbetsplatser</h2><p>Fasad, målning, badrum – och bilen du ser utanför när vi är på plats.</p></div>
    <div class="reel">{reel}</div>
    <div class="center"><a class="more" href="{{root}}projekt.html">Se alla projekt{icon("arrow")}</a></div>
  </div>
</section>

<section class="sec" id="kunder">
  <div class="wrap">
    <div class="sec-head">{eyebrow("Våra kunder")}<h2>För hem, fastigheter och föreningar</h2></div>
    <div class="segs">{segs}</div>
  </div>
</section>

{values_section()}

<section class="sec" id="projekt">
  <div class="wrap">
    <div class="sec-head split">{eyebrow("Referenser")}<h2>Våra projekt</h2><a class="more" href="{{root}}projekt.html">Alla projekt{icon("arrow")}</a></div>
    {gallery(PROJECTS[:6], filters=False)}
  </div>
</section>

{process_section()}
{review_section()}
{faq_section()}
{contact_section("Berätta om ditt projekt")}
{seo_text()}'''
    page("index.html", f"{NAME} – Byggfirma i Haninge & Stockholm | {RATING} på Google",
         f"{NAME} utför bygg- och renoveringsarbeten i Stockholm och på Södertörn: totalrenovering, kök, badrum, målning, golv, snickeri och tillbyggnad. {RATING} i Google-betyg. Kostnadsfri offert.",
         main, "start")


def build_services_index():
    rows = []
    for d in DIVISIONS:
        cards = "".join(
            f'<a class="svc-card" href="{{root}}tjanster/{s["slug"]}.html">{img("{root}", s["photo"], "", sizes="(min-width: 960px) 25vw, 50vw")}'
            f'<span class="svc-body"><b>{s["title"]}</b><span>{s["short"]}</span><i>Läs mer{icon("arrow")}</i></span></a>'
            for s in SERVICES if s["div"] == d["id"])
        rows.append(f'''<section class="sec svc-div" id="{d["id"]}">
  <div class="wrap">
    <div class="sec-head left"><p class="div-num">{d["num"]}</p><h2>{d["title"]}</h2><p>{d["lead"]}</p></div>
    <div class="svc-grid">{cards}</div>
  </div>
</section>''')
    main = f'''{page_hero([("Tjänster", "tjanster/index.html")], "Våra tjänster", "Tio tjänsteområden i tre affärsområden – samordnade av ett och samma team.", "stomme", "Tjänster")}
{"".join(rows)}
{process_section(dark=True)}
{faq_section()}'''
    page("tjanster/index.html", f"Tjänster – bygg och renovering i Stockholm | {NAME}",
         "Totalrenovering, köks- och badrumsrenovering, målning, golv och kakel, snickeri, dörrar och fönster, tillbyggnad, betong och VVS i Stockholm och på Södertörn.",
         main, "tjanster", "stomme")


def build_service(s):
    d = next(x for x in DIVISIONS if x["id"] == s["div"])
    body = "".join(f"<p>{p}</p>" for p in s["body"])
    items = "".join(f'<li>{icon("check")}{i}</li>' for i in s["items"])
    others = "".join(f'<li><a href="{o["slug"]}.html">{o["title"]}{icon("arrow")}</a></li>' for o in SERVICES if o["div"] == s["div"] and o is not s)
    rest = "".join(
        f'<a class="svc-card" href="{o["slug"]}.html">{img("../", o["photo"], "", sizes="(min-width: 960px) 25vw, 50vw")}'
        f'<span class="svc-body"><b>{o["title"]}</b><span>{o["short"]}</span><i>Läs mer{icon("arrow")}</i></span></a>'
        for o in SERVICES if o is not s)
    typ = quote_plus(s["title"])
    main = f'''{page_hero([("Tjänster", "tjanster/index.html"), (s["title"], "tjanster/" + s["slug"] + ".html")], s["title"], s["lead"], s["photo"], f'{d["num"]} · {d["title"]}', cta=False)}
<section class="sec">
  <div class="wrap svc-layout">
    <article class="svc-main">
      {photo("{root}", s["photo"], s["title"], "ph svc-ph", sizes="(min-width: 960px) 60vw, 100vw")}
      <p class="big">{s["short"]}</p>
      {body}
      <h2 class="h3">Det här kan ingå</h2>
      <ul class="checks">{items}</ul>
      <div class="svc-btns">{btn("{root}kontakt.html?typ=" + typ + "#offert", "Begär offert på " + s["title"].lower(), "btn-y")}{call("btn-line-navy")}</div>
    </article>
    <aside class="svc-side">
      <div class="side-card side-navy">
        <p class="side-h">Kostnadsfritt hembesök</p>
        <p>Vi kommer ut, tittar på förutsättningarna och lämnar en fast offert.</p>
        {call("btn-y btn-full")}
        <a class="side-mail" href="mailto:{EMAIL}">{icon("mail")}{EMAIL}</a>
      </div>
      {f'<div class="side-card"><p class="side-h">Mer inom {d["title"].lower()}</p><ul class="side-list">{others}</ul></div>' if others else ""}
      <div class="side-card"><p class="side-h">Därför Haninge Byggteam</p>
        <ul class="side-checks"><li>{icon("check")}Fast offert innan start</li><li>{icon("check")}En kontaktperson hela vägen</li><li>{icon("check")}{RATING} i Google-betyg</li><li>{icon("check")}Gemensam slutgenomgång</li></ul></div>
    </aside>
  </div>
</section>
{process_section()}
<section class="sec">
  <div class="wrap">
    <div class="sec-head left">{eyebrow("Andra tjänster")}<h2>Allt under ett tak</h2></div>
    <div class="svc-grid svc-scroll">{rest}</div>
  </div>
</section>'''
    page(f"tjanster/{s['slug']}.html", f"{s['title']} i Stockholm & Haninge | {NAME}",
         f"{s['lead']} {s['short']} {NAME} – kostnadsfritt hembesök och fast offert.", main, "tjanster", s["photo"])


def build_projects():
    main = f'''{page_hero([("Projekt", "projekt.html")], "Våra projekt", "Ett urval av kök, badrum, totalrenoveringar, målning och utomhusarbeten i Stockholm och på Södertörn.", "hero-villa", "Referenser")}
<section class="sec">
  <div class="wrap">{gallery(PROJECTS)}</div>
</section>
{review_section()}'''
    page("projekt.html", f"Projekt – kök, badrum och totalrenovering | {NAME}",
         "Se ett urval av Haninge Byggteams projekt: köksrenoveringar, badrum, totalrenovering av villa, altaner, målning och tillbyggnader.",
         main, "projekt")


def build_about():
    main = f'''{page_hero([("Om oss", "om-oss.html")], "Om Haninge Byggteam", "Ett byggföretag i Stockholm med fokus på kvalitet, tydlig kommunikation och ett professionellt arbetssätt.", "fasad-team", "Företaget")}
<section class="sec intro">
  <div class="wrap intro-grid">
    <div>
      {eyebrow("Vilka vi är")}
      <h2>Från mindre renoveringar till större byggprojekt</h2>
      <p class="big">{NAME} är ett byggföretag med verksamhet i Stockholm som erbjuder bygg- och renoveringstjänster för privatpersoner och företag.</p>
      <p>Vi utgår från Österhaninge och arbetar i hela Stockholm och på Södertörn. Med hantverkare inom bygg, snickeri, målning, plattsättning, betong och VVS kan vi ta helhetsansvar för projektet – eller gå in med en enskild del.</p>
      <p>Med fokus på kvalitet, tydlig kommunikation och ett professionellt arbetssätt strävar teamet efter att leverera hållbara resultat och en smidig upplevelse genom hela projektet. Varje uppdrag planeras noggrant för att säkerställa ett slutresultat som motsvarar kundens förväntningar.</p>
    </div>
    <aside class="keyfacts" aria-label="Företagsfakta">
      <p class="kf-h">Företagsfakta</p>
      <dl>
        <div><dt>Bolag</dt><dd>{NAME}</dd></div>
        <div><dt>Org.nr</dt><dd>{ORG_NR}</dd></div>
        <div><dt>Adress</dt><dd>{STREET}<br>{POSTAL} {CITY}</dd></div>
        <div><dt>Telefon</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd></div>
        <div><dt>E-post</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        <div><dt>Öppettider</dt><dd>{HOURS}</dd></div>
        <div><dt>Områden</dt><dd>{", ".join(AREAS)}</dd></div>
      </dl>
    </aside>
  </div>
</section>
<section class="sec sec-soft">
  <div class="wrap duo">
    {photo("{root}", "servicebil", "Haninge Byggteams servicebil på uppfarten till en villa", "ph ph-tall")}
    <div>
      {eyebrow("Organisation")}
      <h2>Ett team – en kontaktperson</h2>
      <p>Bakom varje projekt står ett sammansvetsat team. Du har en kontaktperson som håller i tidsplan, beställningar och samordning mellan yrkesgrupperna – så att du slipper jaga olika hantverkare.</p>
      <ul class="checks">
        <li>{icon("check")}Projektledning och samordning</li>
        <li>{icon("check")}Bygg, snickeri och inredning</li>
        <li>{icon("check")}Målning, golv, kakel och klinker</li>
        <li>{icon("check")}Betong, håltagning och VVS</li>
      </ul>
    </div>
  </div>
</section>
{values_section()}
{divisions_section()}
{process_section()}
{review_section()}'''
    page("om-oss.html", f"Om oss – byggföretag i Haninge och Stockholm | {NAME}",
         f"{NAME} (org.nr {ORG_NR}) är ett byggföretag i Österhaninge med verksamhet i Stockholm och på Södertörn. Kvalitet, tydlig kommunikation och professionellt arbetssätt.",
         main, "om-oss", "fasad-team")


def build_business():
    offers = [
        ("Lägenheter och lokaler", "Renovering mellan hyresgäster, ytskikt, kök och badrum – med fast pris och tydlig tidsplan.", "malning-och-ytskikt"),
        ("Badrum och våtrum", "Kompletta badrumsrenoveringar med tätskikt, kakel, klinker och montering.", "badrumsrenovering"),
        ("Betong och håltagning", "Bilning, håltagning, gjutning och återställning inför ombyggnad och installationer.", "betong-rivning-haltagning"),
        ("VVS och ledningar", "Byte och anpassning av vatten- och avloppsledningar, samordnat med övriga moment.", "vvs-och-ledningsarbeten"),
        ("Snickeri och inredning", "Montering av kök och inredning, dörrar, fönster, innertak och undertak.", "snickeri-och-inredning"),
        ("Utvändigt", "Fasadarbeten, staket, trädäck och tillbyggnader.", "om-tillbyggnad-utomhus"),
    ]
    cards = "".join(f'<a class="offer" href="{{root}}tjanster/{sl}.html"><h3>{t}</h3><p>{d}</p><span class="more">Läs mer{icon("arrow")}</span></a>' for t, d, sl in offers)
    main = f'''{page_hero([("Företag & BRF", "foretag.html")], "För företag, fastighetsägare och BRF", "En byggpartner med helhetsansvar – från enskilda lägenheter och lokaler till åtgärder i hela fastigheten.", "projektledning", "Företag & BRF")}
<section class="sec">
  <div class="wrap">
    <div class="sec-head">{eyebrow("Uppdrag")}<h2>Det här hjälper vi fastigheter med</h2><p>Vi tar hand om planering, utförande och samordning så att du som beställare kan fokusera på din verksamhet och dina hyresgäster.</p></div>
    <div class="offers">{cards}</div>
  </div>
</section>
<section class="sec sec-navy">
  <div class="wrap">
    <div class="sec-head">{eyebrow("Samarbete", True)}<h2>Så blir vi en trygg partner</h2></div>
    <ul class="values">
      <li>{icon("users")}<h3>En kontaktperson</h3><p>En ansvarig som håller i tidsplan, beställningar och rapportering.</p></li>
      <li>{icon("doc")}<h3>Fasta priser</h3><p>Tydlig offert med omfattning och pris innan arbetet påbörjas.</p></li>
      <li>{icon("clock")}<h3>Planerat utförande</h3><p>Arbetet läggs upp med hänsyn till hyresgäster, boende och verksamhet.</p></li>
      <li>{icon("shield")}<h3>Gemensam slutgenomgång</h3><p>Vi går igenom resultatet tillsammans när arbetet är klart.</p></li>
    </ul>
  </div>
</section>
<section class="sec" id="brf">
  <div class="wrap duo">
    {photo("{root}", "malning-pagar", "Målning av ett rum i en lägenhet", "ph")}
    <div>
      {eyebrow("Bostadsrättsföreningar")}
      <h2>För styrelser i BRF</h2>
      <p>Vi hjälper bostadsrättsföreningar med badrum, målning, golv och åtgärder i trapphus och gemensamma utrymmen. Vi kommer ut på ett kostnadsfritt möte, går igenom behoven med styrelsen och lämnar en fast offert.</p>
      <p>Under arbetet håller vi löpande dialog med styrelsen och tar hänsyn till de boende.</p>
      <div class="svc-btns">{btn("{root}kontakt.html?typ=Annat#offert", "Boka ett möte", "btn-y")}{call("btn-line-navy")}</div>
    </div>
  </div>
</section>
{contact_section("Begär offert för ert projekt", with_map=False)}'''
    page("foretag.html", f"För företag, fastighetsägare och BRF | {NAME}",
         "Bygg- och renoveringstjänster för företag, fastighetsägare och bostadsrättsföreningar i Stockholm: lägenheter, lokaler, badrum, ytskikt, håltagning och VVS.",
         main, "foretag", "projektledning")


def build_career():
    roles = ["Snickare", "Plattsättare", "Målare", "Byggarbetare", "Projektledare"]
    chips = "".join(f'<li>{r}</li>' for r in roles)
    main = f'''{page_hero([("Karriär", "karriar.html")], "Jobba hos Haninge Byggteam", "Vill du vara en del av ett byggteam som sätter kvalitet och ordning först?", "stomme", "Karriär", cta=False)}
<section class="sec">
  <div class="wrap duo">
    <div>
      {eyebrow("Spontanansökan")}
      <h2>Vi tar gärna emot din ansökan</h2>
      <p class="big">Vi är alltid intresserade av duktiga hantverkare som delar våra värderingar.</p>
      <p>Hos oss arbetar du med varierade uppdrag i Stockholm och på Södertörn – kök, badrum, totalrenoveringar och tillbyggnader – tillsammans med kollegor inom flera yrkesgrupper.</p>
      <ul class="tags">{chips}</ul>
      <p>Skicka ett kort brev om dig själv, din erfarenhet och dina eventuella behörigheter till <a href="mailto:{EMAIL}?subject=Spontanans%C3%B6kan">{EMAIL}</a>.</p>
      <div class="svc-btns">{btn("mailto:" + EMAIL + "?subject=Spontanans%C3%B6kan", "Skicka ansökan", "btn-y", "mail")}{call("btn-line-navy")}</div>
    </div>
    {photo("{root}", "fasad-team", "Två hantverkare arbetar på en ställning vid en fasad", "ph ph-tall")}
  </div>
</section>
{values_section()}'''
    page("karriar.html", f"Karriär – jobba som hantverkare i Stockholm | {NAME}",
         "Vill du jobba hos Haninge Byggteam? Vi tar gärna emot spontanansökningar från snickare, plattsättare, målare och andra hantverkare.",
         main, "", "stomme")


def build_contact():
    main = f'''{page_hero([("Kontakt", "kontakt.html")], "Kontakta oss", "Ring, mejla eller skicka en förfrågan – vi återkommer inom en arbetsdag.", "servicebil", "Kontakt", cta=False)}
{contact_section("Begär kostnadsfri offert")}
{faq_section()}'''
    page("kontakt.html", f"Kontakt – begär gratis offert | {NAME}",
         f"Kontakta {NAME}: {PHONE}, {EMAIL}, {ADDR}. Kostnadsfritt hembesök och fast offert.", main, "kontakt", "servicebil")


def build_404():
    main = f'''<section class="sec nf">
  <div class="wrap">
    <p class="div-num">404</p>
    <h1>Sidan finns inte</h1>
    <p>Sidan kan ha flyttats. Gå till startsidan eller hör av dig direkt.</p>
    <div class="hero-btns">{btn("{root}index.html", "Till startsidan", "btn-y")}{call("btn-line-navy")}</div>
  </div>
</section>'''
    page("404.html", f"Sidan hittades inte | {NAME}", "Sidan finns inte.", main)
    # 404 can be served at any depth, so make its links absolute from the site root.
    p = OUT / "404.html"
    base = SITE_URL.split("github.io")[-1] if "github.io" in SITE_URL else "/"
    p.write_text(p.read_text(encoding="utf-8").replace("<head>", f'<head>\n<base href="{base}">', 1), encoding="utf-8")


def build_meta():
    pages = ["", "tjanster/", "projekt.html", "om-oss.html", "foretag.html", "karriar.html", "kontakt.html"] + [f"tjanster/{s['slug']}.html" for s in SERVICES]
    urls = "".join(f"<url><loc>{SITE_URL}{p}</loc></url>" for p in pages)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    build_index()
    build_services_index()
    for s in SERVICES:
        build_service(s)
    build_projects()
    build_about()
    build_business()
    build_career()
    build_contact()
    build_404()
    build_meta()
    print(f"Byggde {len(list(OUT.rglob('*.html')))} sidor i {OUT}/")
