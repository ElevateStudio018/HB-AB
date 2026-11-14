# Haninge Byggteam AB – webbplats

Ny webbplats för Haninge Byggteam AB (bygg och renovering i Stockholm och på Södertörn), byggd med Elevate Studios
**koncern-agent** och generator från [Ohan-entreprenad](https://github.com/ElevateStudio018/Ohan-entreprenad)
(`.claude/agents/koncern.md`, `koncern/`). Grafiskt paket: profil *bygg*, helskärmshero med texten nere till vänster (`herotext: nere`), arketyp finans, minsta avstånd 12.3; marinblått `#0e2a47` och gult
`#f6c30f` från företagets profil, Poppins i fet vikt. Helskärmshero, vägval, kunder, projekt i bento, arbetsgång,
vanliga frågor, kundomdöme och offertformulär.

Förhandsvisning: https://raw.githack.com/ElevateStudio018/HB-AB/claude/sleepy-planck-gklneu/docs/index.html

## Sidor (`docs/`)

`index.html`, `verksamhet.html` (tjänster), `bolag.html` (kunder), `projekt.html`, `hallbarhet.html` (kvalitet),
`faq.html`, `karriar.html`, `om-oss.html` (med kontakt och offertformulär). Gamla adresser (`/tjanster/<tjänst>`,
`kontakt.html`, `kunder.html`, `foretag.html`) leder vidare till rätt sida.

## Bygga

```bash
git clone https://github.com/ElevateStudio018/Ohan-entreprenad ../Ohan-entreprenad
npm install                                # purgecss + lightningcss: rensar generatorns CSS från ca 600 kB till ca 50 kB
python3 scripts/bygg_koncern.py            # eller: python3 scripts/bygg_koncern.py <sökväg till Ohan-entreprenad>
```

- `koncern/brief.json` – allt innehåll (redigera här)
- `koncern/paket.json` – det grafiska paketet (registrerat i koncern-registret så att nästa sajt blir annorlunda)
- `koncern/bilder/` – företagets egna bilder (taggar `hb-*`)
- `scripts/bygg_koncern.py` – kör generatorn och byter sedan exempelformuläret mot det riktiga offertformuläret
  (`scripts/offert.js`), tar bort platshållarlänkar i sidfoten och skapar omdirigeringar, sitemap och robots.txt

## Fakta och förslag – gå igenom före lansering

**Från haningebyggteam.se:** namn, org.nr 559229-1115, telefon, e-post, adress, öppettider, områden, ”Kvalitet som håller”,
om-texten, de tio tjänsterna och deras texter, arbetsgången, fem av sex vanliga frågor, Google-betyget 5,0 och omdömet från
Ihtik AlimJanov, samt projekten i Haninge, Stockholm och Tyresö.

**Från haningeriv.se:** systerbolaget Haninge Riv & Sanering (HRS AB) – samma telefon och Albybergsringen, tjänsterna
rivning, sanering, betonghåltagning, friläggning av rör, byggkonsult och bemanning – och saneringsbilden på sidan Våra bolag.
Bekräfta att bolagen ska presenteras som en koncern.

**Förslag som kunden bör bekräfta:** indelningen i fyra affärsområden, kundgrupperna (privat, företag, BRF), nyckeltalen
”4 affärsområden” och ”10 tjänsteområden”, kvalitetsrutorna, karriärtexten, den sjätte frågan i FAQ och orten
”Stockholm” på projekten utan känd ort. Inga årtal, priser, certifieringar eller antal anställda anges.

## Bilder

Heron och kvalitetsavsnittet använder stockfoton från Pexels: [4642437](https://www.pexels.com/photo/4642437/) (hero), [7031408](https://www.pexels.com/photo/7031408/), [8829896](https://www.pexels.com/photo/8829896/),
[8821542](https://www.pexels.com/photo/8821542/) och [4642437](https://www.pexels.com/photo/4642437/) (`px-*` i `koncern/bilder/`).
Övriga bilder kommer från haningebyggteam.se. `hb-fasad`, `hb-malning`, `hb-badrum-klart` och `hb-bil` är riktiga jobbfoton;
villan, köken, badrummet, hallen och altanen från gamla sajten ser ut som visualiseringar och märks som illustrationsbilder
där generatorn gör det. Fler egna foton i hög upplösning skulle lyfta sajten mest.

## Offertformuläret

Skickar via [FormSubmit](https://formsubmit.co). Under förhandsvisningen går förfrågningarna till Elevate Studio – byt
`FORM_EMAIL` i `scripts/bygg_koncern.py` till info@haningebyggteam.se vid lansering och bygg om.

## Publicera

`.github/workflows/deploy-pages.yml` publicerar `docs/` med GitHub Pages när Pages är aktiverat
(Settings → Pages → Source: GitHub Actions).

## Fem redesignförslag

`docs/forslag/` innehåller fem kompletta varianter av sajten, gjorda med koncern-agentens fem arketyper (monument,
koncernband, ramad, industriell, skandinavisk). Paketen ligger i `koncern/forslag/paket-<n>.json` och är registrerade i
koncern-registret. Översikt: `docs/forslag/index.html`. När ett förslag är valt: kopiera dess paket till
`koncern/paket.json` och bygg om.

## SEO och tester

Byggsteget `scripts/seo.py` gör landningssidor för alla tio tjänster (`tjanster/<tjänst>.html`), sätter titlar,
beskrivningar, canonical, Open Graph och strukturerad data, rättar rubrikordning och länktexter, gör bilder i flera
storlekar och bygger in rensad CSS och egna typsnitt i varje sida (`scripts/rensa-css.mjs`, kräver `npm install`).

- `node scripts/test/djupanalys.mjs <adress>` – samma kontroller som Elevate Studios djupanalys
- `scripts/test/lighthouse.sh <adress> <namn>` – Googles Lighthouse (mobil)
- Jämförelse mot nuvarande haningebyggteam.se: `docs/forslag/seo-rapport.html`

Resultat: djupanalysen 100 i SEO, tillgänglighet, bästa praxis och prestanda på alla 18 sidor; Lighthouse 100/100/100/100
på alla tio testade sidor. Säkerhetsrubriker kräver Cloudflare Pages eller Netlify (`docs/_headers`); mejlposter
(MX, SPF, DMARC) saknas på domänen och rättas hos domänleverantören.
