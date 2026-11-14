"""Bygger koncern/forslag/sida/sektioner.html: 10 designförslag för "Haninge Byggteam i siffror" och 10 för
"Vad kan vi hjälpa dig med? + Våra bolag". Byggskriptet kopierar sidan till docs/forslag/sektioner.html.

Kör:  python3 scripts/sektionsforslag.py
"""
import html
import json
import pathlib

ROT = pathlib.Path(__file__).resolve().parent.parent
B = json.loads((ROT / "koncern" / "brief.json").read_text(encoding="utf-8"))
E = html.escape
RIV = "https://www.haningeriv.se/"

TAL = [(x["varde"], x["etikett"]) for x in B["nyckeltal"]]
TJ = [t for t in B["tjanster"] if "omr-" in t["href"]]
OMR = B["affarsomraden"]
BOLAG = [dict(namn="Haninge Byggteam AB", seg="Bygg och renovering", bild="hb-villa", href="../bolag.html",
              text="Totalrenovering, kök, badrum, ytskikt, snickeri, tillbyggnad, betong och VVS."),
         dict(namn="Haninge Riv & Sanering AB", seg="Rivning, sanering och håltagning", bild="hrs-sanering", href=RIV,
              text="Rivning, sanering, betonghåltagning, friläggning av rör, byggkonsult och bemanning.")]

ICON = {
    "hus": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/>', "hem": '<path d="M3 11 12 4l9 7"/><path d="M6 10v10h12V10"/><path d="M10 20v-5h4v5"/>',
    "vatten": '<path d="M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z"/>', "pensel": '<path d="M14 4l6 6-9 9H5v-6z"/>',
    "ritning": '<rect x="4" y="4" width="16" height="16"/><path d="M4 12h8V4M12 12v8"/>', "hamare": '<path d="M14 5l5 5-3 3-5-5zM11 8l-7 7 3 3 7-7"/>',
    "nyckel": '<circle cx="8" cy="15" r="4"/><path d="m11 12 8-8M16 7l2 2"/>', "kran": '<path d="M6 21V4h12M6 8l12-4M14 4v6"/><path d="M4 21h6"/>',
    "sten": '<path d="M4 18 8 9l5 3 4-6 3 12z"/>', "ror": '<path d="M4 8h8v8h8M4 5v6M17 13v6"/>',
}


def ikon(n):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{ICON.get(n, ICON["hus"])}</svg>')


PIL = '<svg class="pil" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def img(n, cls=""):
    return f'<img class="{cls}" src="../img/{n}.webp" alt="" loading="lazy">'


def tal_li(cls=""):
    return "".join(f'<li class="{cls}"><b>{E(v)}</b><span>{E(e)}</span></li>' for v, e in TAL)


def tj_li(med_ikon=True):
    return "".join(f'<li><a href="../{t["href"]}">{ikon(t["ikon"]) if med_ikon else ""}<span>{E(t["titel"])}</span>{PIL}</a></li>' for t in TJ)


def bolag_kort(cls="bk"):
    return "".join(f'<a class="{cls}" href="{x["href"]}">{img(x["bild"])}<span><small>{E(x["seg"])}</small><b>{E(x["namn"])}</b>'
                   f'<i>{"haningeriv.se" if x["href"] == RIV else "Läs mer"} {PIL}</i></span></a>' for x in BOLAG)


RUB = "Byggföretag med verksamhet i Stockholm"
ETI = "Haninge Byggteam i siffror"

# --- 10 förslag: siffror -----------------------------------------------------------------------------------------------
S = [
    ("Mörkblått band", "Rubrik centrerad, fyra stora gula siffror med tunna skiljelinjer.",
     f'<section class="s1"><div class="w"><p class="et">{ETI}</p><h2>{RUB}</h2><ul>{tal_li()}</ul></div></section>'),
    ("Text + rutnät", "Rubrik och text till vänster, siffrorna i fyra grå kort till höger.",
     f'<section class="s2"><div class="w"><div><p class="et">{ETI}</p><h2>{RUB}</h2><p>Kompletta bygg- och renoveringslösningar för privatpersoner, företag och bostadsrättsföreningar.</p>'
     f'<a class="btn" href="../om-oss.html">Om företaget {PIL}</a></div><ul>{tal_li()}</ul></div></section>'),
    ("Bild + panel", "Rundad bild till vänster, mörkblå panel med siffrorna som en lista.",
     f'<section class="s3"><div class="w">{img("hb-fasad")}<div class="pan"><p class="et">{ETI}</p><h2>{RUB}</h2><ul>{tal_li()}</ul></div></div></section>'),
    ("Flytande kort", "Bred bild med ett vitt kort som ligger över bildens nederkant.",
     f'<section class="s4">{img("hb-kok-ek", "bg")}<div class="w"><div class="kort"><div><p class="et">{ETI}</p><h2>{RUB}</h2></div><ul>{tal_li()}</ul></div></div></section>'),
    ("Gult band", "Kraftigt gult band med marinblå siffror – syns på långt håll.",
     f'<section class="s5"><div class="w"><h2>{RUB}</h2><ul>{tal_li()}</ul></div></section>'),
    ("Bildrutor", "Varje siffra på en egen bild med mörk ton.",
     f'<section class="s6"><div class="w"><p class="et">{ETI}</p><h2>{RUB}</h2><ul>'
     + "".join(f'<li>{img(n)}<b>{E(v)}</b><span>{E(e)}</span></li>' for (v, e), n in zip(TAL, ["hb-badrum", "hb-altan", "hb-malning", "hb-villa"]))
     + '</ul></div></section>'),
    ("Luftig och stram", "Ljusgrå yta, jättestora siffror med tunn linje ovanför – Skanska-känsla.",
     f'<section class="s7"><div class="w"><div class="h"><p class="et">{ETI}</p><h2>{RUB}</h2></div><ul>{tal_li()}</ul></div></section>'),
    ("Märken", "Siffrorna i mörkblå cirklar med gul ring.",
     f'<section class="s8"><div class="w"><p class="et">{ETI}</p><h2>{RUB}</h2><ul>{tal_li()}</ul></div></section>'),
    ("Smal remsa", "Kompakt mörk remsa direkt under en sektion – tar lite plats.",
     f'<section class="s9"><div class="w"><p>{ETI}</p><ul>{tal_li()}</ul></div></section>'),
    ("Bento", "Ett stort mörkblått kort med rubrik och tre kort i gult, bild och grått.",
     f'<section class="s10"><div class="w"><div class="b1"><p class="et">{ETI}</p><h2>{RUB}</h2><p class="stor"><b>{E(TAL[0][0])}</b> {E(TAL[0][1].lower())}</p></div>'
     f'<div class="b2"><b>{E(TAL[3][0])}</b><span>{E(TAL[3][1])}</span></div>'
     f'<div class="b3">{img("hb-kok-ljust")}<b>{E(TAL[1][0])}</b><span>{E(TAL[1][1])}</span></div>'
     f'<div class="b4"><b>{E(TAL[2][0])}</b><span>{E(TAL[2][1])}</span></div></div></section>'),
]

# --- 10 förslag: tjänster + bolag --------------------------------------------------------------------------------------
H = '<p class="et">Tjänster</p><h2>Vad kan vi hjälpa dig med?</h2>'
HB = '<p class="et">Koncernen</p><h2>Våra bolag</h2>'
T = [
    ("Kortrutnät + bolag", "Tjänsterna som små vita kort med ikon, bolagen som stora bildkort bredvid.",
     f'<section class="t1"><div class="w"><div>{H}<ul>{tj_li()}</ul></div><aside>{HB}{bolag_kort("bk-stor")}</aside></div></section>'),
    ("Chips + banderoller", "Tjänsterna som runda chips, bolagen som två breda banderoller under.",
     f'<section class="t2"><div class="w">{H}<ul class="chips">{tj_li(False)}</ul><div class="ban">'
     + "".join(f'<a href="{x["href"]}">{img(x["bild"])}<span><small>{E(x["seg"])}</small><b>{E(x["namn"])}</b></span></a>' for x in BOLAG)
     + '</div></div></section>'),
    ("Mörk sektion", "Mörkblå bakgrund, gula ikoner i tre spalter och vita bolagskort till höger.",
     f'<section class="t3"><div class="w"><div>{H}<ul>{tj_li()}</ul></div><aside>{HB}{bolag_kort()}</aside></div></section>'),
    ("Ikonrutor + delad banner", "Tio ikonrutor i två rader, bolagen som en delad bildbanner under.",
     f'<section class="t4"><div class="w">{H}<ul>{tj_li()}</ul><div class="split">'
     + "".join(f'<a href="{x["href"]}">{img(x["bild"])}<span><small>{E(x["seg"])}</small><b>{E(x["namn"])}</b><i>{PIL}</i></span></a>' for x in BOLAG)
     + '</div></div></section>'),
    ("Per affärsområde", "Tjänsterna grupperade under de fyra affärsområdena, bolagen som rad under.",
     f'<section class="t5"><div class="w">{H}<div class="kol">'
     + "".join(f'<div><b>{E(a["titel"])}</b><ul>' + "".join(f'<li><a href="../{t["href"]}">{E(t["titel"])}</a></li>' for t in TJ if t["href"].endswith(f"omr-{i}")) + '</ul></div>' for i, a in enumerate(OMR))
     + f'</div><div class="rad"><span>{HB.replace("<h2>", "<h3>").replace("</h2>", "</h3>")}</span>{bolag_kort()}</div></div></section>'),
    ("Bild med lista", "Stor bild med tjänstelistan i en vit ruta ovanpå, bolagen bredvid.",
     f'<section class="t6"><div class="w"><div class="bild">{img("px-4642437")}<div class="ruta">{H}<ul>{tj_li(False)}</ul></div></div><aside>{HB}{bolag_kort()}</aside></div></section>'),
    ("Höga bolagskort", "Tjänsterna i en tunn lista till vänster, bolagen som två höga bildkort till höger.",
     f'<section class="t7"><div class="w"><div>{H}<ul>{tj_li()}</ul></div><div class="hoga">'
     + "".join(f'<a href="{x["href"]}">{img(x["bild"])}<span><small>{E(x["seg"])}</small><b>{E(x["namn"])}</b><i>{"haningeriv.se" if x["href"] == RIV else "Läs mer"} {PIL}</i></span></a>' for x in BOLAG)
     + '</div></div></section>'),
    ("Bento", "Bolagen som två stora rutor, tjänsterna som små rutor runt omkring.",
     f'<section class="t8"><div class="w">{H}<div class="grid">'
     + "".join(f'<a class="stor" href="{x["href"]}">{img(x["bild"])}<span><small>{E(x["seg"])}</small><b>{E(x["namn"])}</b></span></a>' for x in BOLAG)
     + "".join(f'<a class="liten" href="../{t["href"]}">{ikon(t["ikon"])}<span>{E(t["titel"])}</span></a>' for t in TJ)
     + '</div></div></section>'),
    ("Numrerad lista", "Stram numrerad lista 01–10 i två spalter, bolagen i en grå ruta.",
     f'<section class="t9"><div class="w"><div>{H}<ol>'
     + "".join(f'<li><a href="../{t["href"]}"><em>{i:02d}</em><span>{E(t["titel"])}</span>{PIL}</a></li>' for i, t in enumerate(TJ, 1))
     + f'</ol></div><aside>{HB}' + "".join(f'<a href="{x["href"]}"><b>{E(x["namn"])}</b><span>{E(x["text"])}</span><i>{PIL}</i></a>' for x in BOLAG) + '</aside></div></section>'),
    ("Områdeskort med bild", "Fyra bildkort med tjänsterna listade i varje, bolagen som remsa under.",
     f'<section class="t10"><div class="w">{H}<div class="kort">'
     + "".join(f'<div>{img(OMR_BILD)}<b>{E(a["titel"])}</b><ul>' + "".join(f'<li><a href="../{t["href"]}">{E(t["titel"])}</a></li>' for t in TJ if t["href"].endswith(f"omr-{i}")) + '</ul></div>'
               for i, (a, OMR_BILD) in enumerate(zip(OMR, ["hb-kok-ljust", "hb-malning", "hb-altan", "hb-fasad"])))
     + '</div><div class="remsa">' + "".join(f'<a href="{x["href"]}"><small>{E(x["seg"])}</small><b>{E(x["namn"])}</b>{PIL}</a>' for x in BOLAG) + '</div></div></section>'),
]

CSS = """
*{box-sizing:border-box}body{margin:0;font-family:var(--font-t);color:var(--c-ink);background:#fff;font-size:16px;line-height:1.55}
a{color:inherit;text-decoration:none}img{display:block;max-width:100%}ul,ol{list-style:none;margin:0;padding:0}h2,h3{font-weight:700;letter-spacing:-.025em;line-height:1.1;margin:8px 0 22px}
h2{font-size:clamp(28px,3.2vw,44px)}.w{max-width:1360px;margin:0 auto;padding:0 clamp(20px,4vw,56px)}
.et{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--c-p);margin:0}
.pil{width:18px;height:18px;flex:none}svg{flex:none}
.top{background:var(--c-p);color:#fff;padding:56px 0 40px}.top h1{margin:0 0 8px;font-size:clamp(30px,4vw,48px)}.top p{margin:0;opacity:.8;max-width:60em}
.toc{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}.toc a{background:#f6c30f;color:#14171b;padding:8px 16px;border-radius:999px;font-weight:600;font-size:14px}
.del{padding:48px 0 8px}.del h2{font-size:30px}
.fs{border-top:1px solid var(--c-line);padding:28px 0 0;margin-top:28px}.fs-h{display:flex;gap:14px;align-items:baseline;margin-bottom:18px}
.fs-h b{background:var(--c-p);color:#f6c30f;border-radius:999px;min-width:44px;height:44px;display:inline-grid;place-items:center;font-size:17px}
.fs-h strong{font-size:20px}.fs-h span{color:var(--c-mut)}.ram{border-radius:18px;overflow:hidden;box-shadow:0 10px 40px rgba(14,42,71,.12)}
.ram section{padding:72px 0}.btn{display:inline-flex;align-items:center;gap:8px;background:var(--c-p);color:#fff;padding:13px 24px;border-radius:999px;font-weight:600;margin-top:10px}
/* siffror */
.s1{background:var(--c-p);color:#fff;text-align:center}.s1 .et{color:#f6c30f}.s1 ul{display:grid;grid-template-columns:repeat(4,1fr);margin-top:36px}
.s1 li{border-left:1px solid rgba(255,255,255,.2);padding:8px 16px}.s1 li:first-child{border:0}.s1 b{display:block;font-size:clamp(44px,5vw,72px);color:#f6c30f;line-height:1}.s1 span{opacity:.85}
.s2 .w{display:grid;grid-template-columns:1fr 1.2fr;gap:56px;align-items:center}.s2 ul{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.s2 li{background:var(--c-yta);border-radius:16px;padding:28px}.s2 b{display:block;font-size:48px;color:var(--c-p);line-height:1;margin-bottom:8px}.s2 p{color:var(--c-mut)}
.s3 .w{display:grid;grid-template-columns:1fr 1fr;gap:0;border-radius:16px;overflow:hidden;padding:0;max-width:1260px}.s3 img{width:100%;height:100%;object-fit:cover;min-height:440px}
.s3 .pan{background:var(--c-p);color:#fff;padding:48px}.s3 .et{color:#f6c30f}.s3 li{display:flex;align-items:baseline;gap:18px;border-top:1px solid rgba(255,255,255,.18);padding:14px 0}
.s3 b{font-size:38px;color:#f6c30f;min-width:2.4em}
.s4{position:relative;padding:0!important}.s4 .bg{width:100%;height:440px;object-fit:cover}.s4 .w{margin-top:-140px;position:relative;padding-bottom:64px}
.s4 .kort{background:#fff;border-radius:18px;box-shadow:0 24px 60px rgba(14,42,71,.18);padding:40px;display:grid;grid-template-columns:1fr 1.6fr;gap:40px;align-items:center}
.s4 ul{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.s4 b{display:block;font-size:44px;color:var(--c-p);line-height:1}.s4 span{font-size:14px;color:var(--c-mut)}
.s5{background:#f6c30f}.s5 .w{display:grid;grid-template-columns:1fr 2fr;gap:40px;align-items:center}.s5 h2{color:var(--c-p);margin:0}
.s5 ul{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}.s5 b{display:block;font-size:56px;color:var(--c-p);line-height:1}.s5 span{font-weight:600;color:var(--c-p);font-size:14px}
.s6 ul{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.s6 li{position:relative;border-radius:16px;overflow:hidden;aspect-ratio:3/3.6;color:#fff;display:flex;flex-direction:column;justify-content:flex-end;padding:22px}
.s6 li img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}.s6 li::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(10,31,54,.9),rgba(10,31,54,.15))}
.s6 li{isolation:isolate}.s6 b{font-size:56px;line-height:1;color:#f6c30f}
.s7{background:var(--c-yta)}.s7 .h{display:block}.s7 ul{display:grid;grid-template-columns:repeat(4,1fr);gap:32px;margin-top:40px}
.s7 li{border-top:2px solid var(--c-p);padding-top:20px}.s7 b{display:block;font-size:clamp(56px,6vw,96px);font-weight:300;letter-spacing:-.04em;color:var(--c-p);line-height:1}.s7 span{color:var(--c-mut)}
.s8{text-align:center}.s8 ul{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:36px}.s8 b{display:grid;place-items:center;width:150px;height:150px;margin:0 auto 14px;border-radius:50%;background:var(--c-p);color:#fff;font-size:44px;box-shadow:0 0 0 8px #fff,0 0 0 12px #f6c30f}
.s8 span{font-weight:600}
.ram .s9{padding:26px 0}.s9{background:var(--c-dark);color:#fff}.s9 .w{display:flex;align-items:center;gap:36px}.s9 p{margin:0;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#f6c30f;max-width:9em}
.s9 ul{display:flex;flex:1;justify-content:space-between;gap:24px}.s9 li{display:flex;align-items:baseline;gap:10px}.s9 b{font-size:34px}.s9 span{opacity:.75;font-size:14px;max-width:11em;line-height:1.3}
.s10 .w{display:grid;grid-template-columns:1.4fr 1fr 1fr;grid-template-rows:auto auto;gap:16px}.s10 .w>div{border-radius:18px;padding:30px;position:relative;overflow:hidden;isolation:isolate}
.s10 .b1{grid-row:span 2;background:var(--c-p);color:#fff}.s10 .b1 .et{color:#f6c30f}.s10 .stor b{font-size:96px;color:#f6c30f;display:block;line-height:1}
.s10 .b2{background:#f6c30f}.s10 .b3{color:#fff}.s10 .b3 img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}.s10 .b3::after{content:"";position:absolute;inset:0;z-index:-1;background:rgba(10,31,54,.55)}
.s10 .b4{background:var(--c-yta);grid-column:span 2}.s10 .w>div:not(.b1) b{display:block;font-size:56px;line-height:1;margin-bottom:6px}
/* tjänster + bolag */
.t1 .w,.t3 .w,.t6 .w,.t7 .w,.t9 .w{display:grid;grid-template-columns:1.5fr 1fr;gap:56px;align-items:start}
.t1{background:var(--c-yta)}.t1 ul{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.t1 li a{display:flex;align-items:center;gap:12px;background:#fff;border-radius:14px;padding:16px 18px;font-weight:600}
.t1 li a svg:first-child{width:24px;height:24px;color:var(--c-p)}.t1 li a span{flex:1}.t1 li a .pil{color:var(--c-p)}
.bk-stor,.bk{display:flex;gap:14px;align-items:center;background:#fff;border-radius:16px;padding:12px;margin-bottom:12px;box-shadow:0 6px 20px rgba(14,42,71,.06)}
.bk-stor{flex-direction:column;align-items:stretch;padding:0;overflow:hidden}.bk-stor img{height:170px;object-fit:cover;width:100%}.bk-stor>span{padding:4px 20px 20px}
.bk img{width:96px;height:84px;object-fit:cover;border-radius:12px}.bk span,.bk-stor span{display:grid;gap:3px}.bk small,.bk-stor small{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--c-mut)}
.bk b,.bk-stor b{font-size:18px}.bk i,.bk-stor i{font-style:normal;font-weight:600;font-size:14px;color:var(--c-p);display:inline-flex;align-items:center;gap:6px}
.t2 .chips{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:40px}.t2 .chips a{display:inline-flex;align-items:center;gap:8px;border:1.5px solid var(--c-p);border-radius:999px;padding:11px 20px;font-weight:600;color:var(--c-p)}
.t2 .chips a:hover{background:var(--c-p);color:#fff}.t2 .chips .pil{width:15px}
.t2 .ban{display:grid;grid-template-columns:1fr 1fr;gap:16px}.t2 .ban a{position:relative;border-radius:18px;overflow:hidden;height:220px;color:#fff;isolation:isolate;display:flex;align-items:flex-end;padding:26px}
.t2 .ban img,.t4 .split img,.t7 .hoga img,.t8 .stor img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}
.t2 .ban a::after,.t4 .split a::after,.t7 .hoga a::after,.t8 .stor::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(10,31,54,.9),rgba(10,31,54,.1))}
.t2 .ban span,.t4 .split span,.t7 .hoga span,.t8 .stor span{display:grid;gap:4px}.t2 small,.t4 small,.t7 small,.t8 small{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#f6c30f}
.t2 .ban b,.t4 .split b,.t7 .hoga b,.t8 .stor b{font-size:24px}
.t3{background:var(--c-p);color:#fff}.t3 .et{color:#f6c30f}.t3 ul{display:grid;grid-template-columns:repeat(3,1fr);gap:4px 24px}.t3 li a{display:flex;gap:12px;align-items:center;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.14);font-weight:600}
.t3 li a svg:first-child{width:22px;height:22px;color:#f6c30f}.t3 li a span{flex:1}.t3 li a .pil{opacity:.5}.t3 aside{background:rgba(255,255,255,.06);border-radius:18px;padding:28px}.t3 .bk{color:var(--c-ink)}
.t4 ul{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:28px}.t4 li a{display:flex;flex-direction:column;gap:12px;background:var(--c-yta);border-radius:16px;padding:22px;font-weight:600;min-height:130px}
.t4 li a svg:first-child{width:30px;height:30px;color:var(--c-p)}.t4 li a .pil{margin-top:auto;color:var(--c-p)}.t4 li a:hover{background:var(--c-p);color:#fff}.t4 li a:hover svg{color:#f6c30f}
.t4 .split{display:grid;grid-template-columns:1fr 1fr;border-radius:18px;overflow:hidden}.t4 .split a{position:relative;height:200px;color:#fff;isolation:isolate;display:flex;align-items:flex-end;padding:28px}
.t4 .split i{position:absolute;right:24px;bottom:28px;width:44px;height:44px;border-radius:50%;background:#f6c30f;color:var(--c-p);display:grid;place-items:center}
.t5 .kol{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:40px}.t5 .kol>div{border-top:3px solid var(--c-p);padding-top:16px}.t5 .kol b{font-size:18px;display:block;margin-bottom:10px}
.t5 .kol a{display:block;padding:7px 0;color:var(--c-mut);font-weight:500}.t5 .kol a:hover{color:var(--c-p)}
.t5 .rad{display:grid;grid-template-columns:auto 1fr 1fr;gap:16px;align-items:center;background:var(--c-yta);border-radius:18px;padding:22px}.t5 .rad h3{margin:4px 0 0;font-size:26px}.t5 .rad .bk{margin:0}
.t6 .bild{position:relative;border-radius:18px;overflow:hidden;min-height:560px}.t6 .bild>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.t6 .ruta{position:relative;margin:28px;max-width:440px;background:#fff;border-radius:16px;padding:28px}.t6 .ruta h2{font-size:30px}.t6 .ruta li a{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--c-line);font-weight:600}
.t6 aside{padding-top:40px}
.t7 li a{display:flex;align-items:center;gap:14px;padding:15px 0;border-bottom:1px solid var(--c-line);font-weight:600}.t7 li a svg:first-child{width:22px;height:22px;color:var(--c-p)}.t7 li a span{flex:1}
.t7 .hoga{display:grid;grid-template-columns:1fr 1fr;gap:14px}.t7 .hoga a{position:relative;border-radius:18px;overflow:hidden;min-height:520px;color:#fff;isolation:isolate;display:flex;align-items:flex-end;padding:24px}
.t7 .hoga i{font-style:normal;font-weight:600;display:inline-flex;gap:6px;align-items:center;margin-top:8px}
.t8 .grid{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:130px;gap:12px}.t8 .stor{grid-column:span 2;grid-row:span 2;position:relative;border-radius:18px;overflow:hidden;color:#fff;isolation:isolate;display:flex;align-items:flex-end;padding:26px}
.t8 .liten{display:flex;flex-direction:column;justify-content:space-between;background:var(--c-yta);border-radius:16px;padding:20px;font-weight:600}.t8 .liten svg{width:28px;height:28px;color:var(--c-p)}.t8 .liten:hover{background:#f6c30f}
.t9 ol{display:grid;grid-template-columns:1fr 1fr;column-gap:32px}.t9 li a{display:flex;align-items:center;gap:16px;padding:16px 0;border-bottom:1px solid var(--c-line);font-size:18px;font-weight:600}
.t9 em{font-style:normal;color:#c79d00;font-weight:700;font-size:14px;width:2em}.t9 li a span{flex:1}.t9 aside{background:var(--c-yta);border-radius:18px;padding:30px}
.t9 aside a{display:grid;grid-template-columns:1fr auto;gap:4px 16px;background:#fff;border-radius:14px;padding:20px;margin-bottom:12px}.t9 aside a span{color:var(--c-mut);font-size:14px;grid-column:1}
.t9 aside a i{grid-row:1/span 2;grid-column:2;align-self:center;width:42px;height:42px;border-radius:50%;background:var(--c-p);color:#fff;display:grid;place-items:center}
.t10 .kort{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:20px}.t10 .kort>div{background:var(--c-yta);border-radius:18px;overflow:hidden}.t10 .kort img{height:150px;width:100%;object-fit:cover}
.t10 .kort b{display:block;font-size:19px;padding:18px 20px 6px}.t10 .kort ul{padding:0 20px 20px}.t10 .kort a{display:block;padding:6px 0;color:var(--c-mut);font-weight:500;border-bottom:1px solid var(--c-line)}
.t10 .remsa{display:grid;grid-template-columns:1fr 1fr;gap:16px}.t10 .remsa a{display:flex;align-items:center;gap:16px;background:var(--c-p);color:#fff;border-radius:16px;padding:22px 26px}.t10 .remsa small{color:#f6c30f;font-weight:700;font-size:12px;letter-spacing:.08em;text-transform:uppercase;flex:1}
.t10 .remsa b{font-size:19px}
@media(max-width:900px){.s1 ul,.s4 ul,.s5 ul,.s6 ul,.s7 ul,.s8 ul{grid-template-columns:1fr 1fr;gap:24px}.s2 .w,.s3 .w,.s4 .kort,.s5 .w,.s10 .w,.t1 .w,.t3 .w,.t6 .w,.t7 .w,.t9 .w{grid-template-columns:1fr}
.s9 .w,.s9 ul{flex-wrap:wrap}.s10 .b1{grid-row:auto}.s10 .b4{grid-column:auto}.t3 ul,.t9 ol,.t2 .ban,.t4 .split,.t7 .hoga,.t10 .remsa{grid-template-columns:1fr}.t4 ul,.t5 .kol,.t10 .kort,.t8 .grid{grid-template-columns:1fr 1fr}.t5 .rad{grid-template-columns:1fr}}
"""


def block(rub, n, f):
    items = "".join(f'<div class="fs" id="{n}{i}"><div class="w fs-h"><b>{n}{i}</b><strong>{E(t)}</strong><span>{E(d)}</span></div><div class="w"><div class="ram">{h}</div></div></div>'
                    for i, (t, d, h) in enumerate(f, 1))
    return f'<div class="del" id="{n}"><div class="w"><h2>{rub}</h2></div>{items}</div>'


doc = f'''<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Sektionsförslag – Haninge Byggteam</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap">
<link rel="stylesheet" href="../assets/tokens.css"><style>{CSS}</style></head><body>
<header class="top"><div class="w"><h1>Sektionsförslag</h1><p>10 förslag på "Haninge Byggteam i siffror" (S1–S10) och 10 på "Vad kan vi hjälpa dig med? + Våra bolag" (T1–T10), i sajtens färger och typsnitt. Svara med numret, till exempel S7 och T3.</p>
<nav class="toc"><a href="#S">Siffror S1–S10</a><a href="#T">Tjänster + bolag T1–T10</a><a href="../index.html">Till sajten</a></nav></div></header>
{block("Haninge Byggteam i siffror", "S", S)}{block("Vad kan vi hjälpa dig med? + Våra bolag", "T", T)}
<div style="height:80px"></div></body></html>'''
out = ROT / "koncern" / "forslag" / "sida" / "sektioner.html"
out.write_text(doc, encoding="utf-8")
print("skrev", out.relative_to(ROT))
