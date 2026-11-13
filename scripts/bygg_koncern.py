"""Bygger Haninge Byggteams sajt till docs/ med koncern-generatorn från Ohan-entreprenad.

Kör:  python3 scripts/bygg_koncern.py [sökväg till Ohan-entreprenad]

Standard är ../Ohan-entreprenad bredvid det här repot (git clone https://github.com/ElevateStudio018/Ohan-entreprenad).
Innehållet ligger i koncern/brief.json, det grafiska paketet i koncern/paket.json och företagets egna bilder i
koncern/bilder/. Efter generatorn byter skriptet ut exempelformuläret mot det riktiga offertformuläret, tar bort
platshållarlänkarna i sidfoten och lägger till omdirigeringar från den gamla sajtens adresser.
"""
import html
import json
import pathlib
import re
import shutil
import sys

ROT = pathlib.Path(__file__).resolve().parent.parent
OHAN = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROT.parent / "Ohan-entreprenad").resolve()
DOCS = ROT / "docs"
SITE_URL = "https://elevatestudio018.github.io/HB-AB/"

# Offertförfrågningarna mejlas via FormSubmit. Under förhandsvisningen går de till Elevate Studio; byt till
# info@haningebyggteam.se vid lansering. Första förfrågan till en ny adress skickar bara ett aktiveringsmejl.
FORM_EMAIL = "elevate.studio018@gmail.com"

WORK_TYPES = ["Totalrenovering", "Köksrenovering", "Badrumsrenovering", "Målning och ytskikt", "Golv, kakel och klinker",
              "Snickeri och inredning", "Dörrar, fönster och tak", "Om- och tillbyggnad, utomhus",
              "Betong, rivning och håltagning", "VVS och ledningsarbeten", "Annat"]
START_OPTIONS = ["Så snart som möjligt", "Inom 1–3 månader", "Inom 3–6 månader", "Senare / vet inte"]

# Den gamla sajtens adresser (haningebyggteam.se och förra versionen här) pekar vidare till rätt sida.
OLD_SERVICES = {"totalrenovering": 0, "koksrenovering": 0, "badrumsrenovering": 0, "malning-och-ytskikt": 1,
                "golv-kakel-klinker": 1, "snickeri-och-inredning": 2, "dorrar-fonster-tak": 2, "om-tillbyggnad-utomhus": 2,
                "betong-rivning-haltagning": 3, "vvs-och-ledningsarbeten": 3}
REDIRECTS = {"tjanster/index.html": "../verksamhet.html", "kunder.html": "bolag.html", "foretag.html": "bolag.html",
             "kontakt.html": "om-oss.html#kontakt", **{f"tjanster/{s}.html": f"../verksamhet.html#omr-{n}" for s, n in OLD_SERVICES.items()}}

E = html.escape


def prepare_bank():
    """Lägger företagets egna bilder i generatorns bildbank (taggar hb-*), om de inte redan finns där."""
    bank, tsv = OHAN / "koncern" / "bildbank", OHAN / "koncern" / "bildbank.tsv"
    rows = (ROT / "koncern" / "bilder" / "bilder.tsv").read_text(encoding="utf-8").splitlines()
    have = tsv.read_text(encoding="utf-8")
    for f in (ROT / "koncern" / "bilder").glob("hb-*.jpg"):
        shutil.copy(f, bank / f.name)
    missing = [r for r in rows if r.strip() and r.split("\t")[0] + "\t" not in have]
    if missing:
        tsv.write_text(have.rstrip("\n") + "\n" + "\n".join(missing) + "\n", encoding="utf-8")


def load_generator():
    sys.path.insert(0, str(OHAN / "koncern"))
    import generera

    orig = generera.Bilder.ta

    def ta(self, tagg=None):
        # Företaget har bara några egna bilder per motiv: återanvänd dem hellre än att falla tillbaka på stockbilder.
        if tagg and tagg.startswith("hb-"):
            ids = {x["id"] for x in self.bank if x["tagg"] == tagg}
            if ids and ids <= self.anvanda:
                self.anvanda -= ids
        return orig(self, tagg)

    generera.Bilder.ta = ta
    return generera


def quote_form():
    types = "".join(f"<option>{E(t)}</option>" for t in WORK_TYPES)
    start = "".join(f"<option>{E(t)}</option>" for t in START_OPTIONS)
    return f'''<form class="boka-form" id="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{FORM_EMAIL}">
<label><span>Namn *</span><input id="f-namn" name="namn" autocomplete="name" required><small class="fel" id="e-namn" hidden>Ange ditt namn.</small></label>
<label><span>Telefon *</span><input id="f-tel" name="tel" type="tel" autocomplete="tel"><small class="fel" id="e-tel" hidden>Ange telefon eller e-post.</small></label>
<label><span>E-post</span><input id="f-epost" name="epost" type="email" autocomplete="email"><small class="fel" id="e-epost" hidden>Kontrollera e-postadressen.</small></label>
<label><span>Adress eller ort för uppdraget</span><input id="f-adress" name="adress" autocomplete="street-address"></label>
<label><span>Typ av uppdrag</span><select id="f-typ" name="typ"><option value="">Välj</option>{types}</select></label>
<label><span>Önskad start</span><select id="f-start" name="start"><option value="">Välj</option>{start}</select></label>
<label class="hel"><span>Beskriv projektet</span><textarea id="f-besk" name="besk" rows="4"></textarea></label>
<div class="hp" aria-hidden="true"><label>Lämna tomt<input id="f-web" name="web" tabindex="-1" autocomplete="off"></label></div>
<button class="knapp knapp-primar" type="submit"><span>Skicka offertförfrågan</span></button>
<p class="hel boka-fin">Hembesök och offert är kostnadsfria. Uppgifterna används endast för att besvara din förfrågan.</p>
<p class="hel fel" id="send-err" role="alert" hidden>Förfrågan kunde inte skickas. Försök igen eller ring 072-002 22 00.</p>
</form>
<div class="boka-form boka-klar" id="qdone" tabindex="-1" hidden><h3>Tack för din förfrågan</h3><p>Vi kontaktar dig för att boka ett hembesök.</p>
<button class="knapp" type="button" id="qagain"><span>Skicka en ny förfrågan</span></button></div>'''


EXTRA_CSS = """
/* Haninge Byggteam: offertformulär */
.boka-form select { width: 100%; font: inherit; font-weight: 400; font-size: 16px; padding: 13px 14px; border: 1px solid var(--c-line); border-radius: min(var(--r-card), 8px); background: var(--c-yta); color: inherit; }
.boka-form select:focus { outline: 2px solid var(--c-p); outline-offset: 1px; }
.boka-form [aria-invalid="true"] { border-color: #b3261e; }
.boka-form .fel { color: #b3261e; font-weight: 500; font-size: 13px; }
.boka-form .hp { position: absolute; left: -9999px; }
.boka-fin { margin: 0; font-size: 13px; font-weight: 400; opacity: .7; }
.boka-klar { display: block; }
.boka-klar[hidden] { display: none; }
.boka-klar h3 { margin: 0 0 8px; }
"""


def postprocess(out):
    for f in out.rglob("*.html"):
        doc = f.read_text(encoding="utf-8")
        doc = re.sub(r'<form class="boka-form".*?</form>', lambda m: quote_form(), doc, flags=re.S)
        doc = re.sub(r'<nav aria-label="Juridiskt">.*?</nav>', "", doc, flags=re.S)
        if 'id="qform"' in doc and "offert.js" not in doc:
            doc = doc.replace("</body>", '<script src="assets/offert.js" defer></script>\n</body>')
        f.write_text(doc, encoding="utf-8")
    with open(out / "assets" / "bas.css", "a", encoding="utf-8") as fh:
        fh.write(EXTRA_CSS)
    shutil.copy(ROT / "scripts" / "offert.js", out / "assets" / "offert.js")


def redirects(out):
    for old, new in REDIRECTS.items():
        p = out / old
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f'<!doctype html><meta charset="utf-8"><title>Haninge Byggteam AB</title>'
                     f'<meta http-equiv="refresh" content="0; url={new}"><link rel="canonical" href="{new}">'
                     f'<p>Sidan har flyttat: <a href="{new}">{new}</a></p>\n', encoding="utf-8")


def meta(out):
    pages = [p.name for p in sorted(out.glob("*.html")) if p.name not in REDIRECTS and p.name != "404.html"]
    urls = "".join(f"<url><loc>{SITE_URL}{'' if p == 'index.html' else p}</loc></url>" for p in pages)
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    (out / "paket.json").unlink(missing_ok=True)


def main():
    if not (OHAN / "koncern" / "generera.py").exists():
        sys.exit(f"Hittar inte koncern-generatorn i {OHAN}. Klona: git clone https://github.com/ElevateStudio018/Ohan-entreprenad")
    prepare_bank()
    generera = load_generator()
    brief = json.loads((ROT / "koncern" / "brief.json").read_text(encoding="utf-8"))
    paket = json.loads((ROT / "koncern" / "paket.json").read_text(encoding="utf-8"))
    generera.Sajt(brief, paket, DOCS).bygg()
    postprocess(DOCS)
    redirects(DOCS)
    meta(DOCS)
    print(f"Byggde {brief['namn']} -> {DOCS.relative_to(ROT)}/")


if __name__ == "__main__":
    main()
