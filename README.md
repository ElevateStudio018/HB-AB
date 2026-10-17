# Haninge Byggteam AB – webbplats

Ny webbplats för Haninge Byggteam AB (bygg och renovering i Stockholm och på Södertörn) i stram koncernstil, i samma
anda som de stora byggbolagens sajter: ett typsnitt (Poppins, samma som gamla sajten), raka hörn, tunna linjer, stora bilder, mycket luft
och marinblått som enda färg. Startsidan öppnar med en helskärmsbild under ett genomskinligt sidhuvud. Inga betyg,
stjärnor, ikoner, bockar eller säljlöften – bara verksamhet, projekt, företagsfakta, vanliga frågor och offertformulär.

## Sidor

Allt ligger i [`docs/`](docs/) och kräver inga verktyg – öppna `docs/index.html` i en webbläsare.

- `index.html` – start: helskärmsbild, företagspresentation, verksamhet (tre områden), utvalt projekt, projekt,
  arbetssätt, kunder/karriär, vanliga frågor och offertformulär
- `tjanster/index.html` (Verksamhet) + tio tjänstesidor i `tjanster/` – **samma adresser som gamla sajten**
  (`/tjanster/badrumsrenovering` osv.), så befintliga länkar och Google-träffar fortsätter fungera
- `projekt.html` (filtrerbart), `kunder.html`, `om-oss.html` (värderingar, arbetssätt, företagsfakta), `karriar.html`,
  `kontakt.html` (offertformulär, vanliga frågor, kontaktuppgifter och karta)
- `404.html`, `sitemap.xml`, `robots.txt`

## Ändra text

Sidorna genereras av `scripts/build.py`, där all text, alla tjänster, projekt och kontaktuppgifter finns. Ändra där och kör:

```bash
python3 scripts/build.py docs
```

Stil och skript: `docs/assets/site.css` och `docs/assets/site.js` (redigeras direkt).

## Fakta och förslag – gå igenom före lansering

**Från haningebyggteam.se:** namn, org.nr 559229-1115, telefon 072-002 22 00, info@haningebyggteam.se,
Albybergsringen 105, 137 69, öppettider mån–fre 07:00–16:30, områdena (Haninge, Stockholm, Tyresö, Huddinge, Nacka),
”Kvalitet som håller”, om-texten, alla tio tjänster med sina texter, arbetsgången i fyra steg, de fem vanliga frågorna,
Google-betyget 5,0 (2 recensioner) och omdömet från Ihtik AlimJanov (ordagrant), samt projekten
”Modern köksrenovering – Haninge”, ”Totalrenovering av villa – Stockholm” och ”Ny altan i trä – Tyresö”.

**Från internet:** Eniro anger orten Österhaninge för adressen. Servicebilen visar även haningebyggteamab@gmail.com –
sajten använder info@-adressen.

**Förslag (ny text) som Haninge Byggteam bör bekräfta eller ändra:**

- Indelningen i tre affärsområden (Renovering & ytskikt, Bygg & snickeri, Grund & installation) och deras ingresser.
- Listorna ”Omfattning” på tjänstesidorna, värderingarna och texterna på sidan Kunder.
- Sidan **Karriär** – ta bort om de inte tar emot ansökningar.
- Projektnamnen ”Fasad” och ”Hall och trappa”, samt den sjätte frågan i FAQ (företag och BRF) – de fem första
  frågorna kommer från gamla sajten.

Inga certifieringar, garantier, priser, årtal eller antal anställda anges.

## Offertformuläret

Offertformuläret (startsidan och Kontakt) frågar efter kundtyp, typ av uppdrag, önskad start, beskrivning,
kontaktuppgifter och adress. Det skickar e-post via [FormSubmit](https://formsubmit.co) och visar
ett tackmeddelande. Under förhandsvisningen går förfrågningarna till Elevate Studio; byt `FORM_EMAIL` i
`scripts/build.py` till info@haningebyggteam.se vid lansering. Första förfrågan till en ny adress skickar bara ett
aktiveringsmejl. ”Kontakta oss” på en tjänstesida fyller i ärendet automatiskt (`kontakt.html?typ=…#formular`).

## Bilder

- **Egna foton från haningebyggteam.se** (riktiga jobb): `fasad-team`, `malning-pagar`, `badrum-klart`, `servicebil`.
- **Bilder från gamla sajten** (ser ut som visualiseringar – kontrollera att de får användas som egna projekt):
  `hero-villa`, `kok-ljust`, `kok-ek`, `badrum-modern`, `hall-trappa`, `altan`.
- **Stockfoton från [Pexels](https://www.pexels.com)** (används bara på tjänste-, kund- och karriärsidor, aldrig som projekt):

| Fil | Pexels-ID |
| --- | --- |
| `rivning.jpg` | [3990359](https://www.pexels.com/photo/3990359/) |
| `stomme.jpg` | [4642437](https://www.pexels.com/photo/4642437/) |
| `takstol.jpg` | [8830259](https://www.pexels.com/photo/8830259/) |
| `dorr.jpg` | [5691502](https://www.pexels.com/photo/5691502/) |
| `snickeri.jpg` | [6790094](https://www.pexels.com/photo/6790094/) |
| `inredning.jpg` | [5974396](https://www.pexels.com/photo/5974396/) |
| `betong.jpg` | [9964624](https://www.pexels.com/photo/9964624/) |
| `vvs.jpg` | [29301874](https://www.pexels.com/photo/29301874/) |
| `projektledning.jpg` | [8961030](https://www.pexels.com/photo/8961030/) |
| `kok-vitt.jpg` | [4682120](https://www.pexels.com/photo/4682120/) |

Byt mot egna bilder genom att ersätta filerna med samma namn (både `namn.jpg`, 1800 px bred, och `namn-s.jpg`, 800 px).
Fler egna jobbfoton i hög upplösning skulle lyfta sajten mest.

## Logga

Ingen vektorlogga fanns, så sidhuvudet använder en typografisk ordbild, HANINGE / BYGGTEAM (`logo()` i
`scripts/build.py`). Favicon är HB-ikonen (`docs/img/favicon.svg`). Byt mot den riktiga loggan när den finns.

## Publicera

Sidan publiceras av `.github/workflows/deploy-pages.yml` vid varje push (GitHub Pages, källa *GitHub Actions*).
Byt `SITE_URL` i `scripts/build.py` till `https://haningebyggteam.se/` när domänen pekas om, och bygg om.
