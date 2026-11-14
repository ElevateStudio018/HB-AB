(function () {
  "use strict";

  // Siffrorna: ringarna fylls och talen räknar upp när sektionen kommer in i bild.
  function rakna(el) {
    var till = parseFloat(el.dataset.till), dec = +el.dataset.dec, t0 = null, d = 1600;
    function steg(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / d, 1), v = till * (1 - Math.pow(1 - p, 3));
      el.textContent = dec ? v.toFixed(1).replace(".", ",") : Math.round(v);
      if (p < 1) requestAnimationFrame(steg);
    }
    requestAnimationFrame(steg);
  }
  var anim = document.querySelectorAll(".hb-anim");
  if (anim.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("syns");
        e.target.querySelectorAll("[data-till]").forEach(rakna);
        io.unobserve(e.target);
      });
    }, { threshold: 0.35 });
    anim.forEach(function (s) {
      s.querySelectorAll("[data-till]").forEach(function (el) { el.textContent = "0"; });
      io.observe(s);
    });
  } else {
    anim.forEach(function (s) {
      s.classList.add("syns");
      s.querySelectorAll("[data-till]").forEach(function (el) { el.textContent = el.dataset.slut; });
    });
  }

  // Projektlistan: filterknappar.
  document.querySelectorAll("[data-pf]").forEach(function (sek) {
    var knappar = sek.querySelectorAll(".pf-chips button"), rader = sek.querySelectorAll(".pf-lista li");
    knappar.forEach(function (k) {
      k.addEventListener("click", function () {
        var typ = k.dataset.typ;
        knappar.forEach(function (b) { b.setAttribute("aria-pressed", String(b === k)); });
        rader.forEach(function (r) { r.hidden = !!typ && r.dataset.typ !== typ; });
      });
    });
  });
})();

(function () {
  "use strict";
  // Sök: ett sökfönster över sidan som söker i assets/sok.json (sidor, tjänster, projekt och vanliga frågor).
  var knappar = document.querySelectorAll("a.sok, [data-sok]");
  if (!knappar.length) return;
  var bas = (document.querySelector('script[src$="hb.js"]') || {}).getAttribute ? document.querySelector('script[src$="hb.js"]').getAttribute("src").replace(/assets\/hb\.js$/, "") : "";
  var data = null, dlg, inp, lista, tom;

  function bygg() {
    dlg = document.createElement("div");
    dlg.className = "sok-fonster";
    dlg.setAttribute("role", "dialog");
    dlg.setAttribute("aria-modal", "true");
    dlg.setAttribute("aria-label", "Sök på webbplatsen");
    dlg.hidden = true;
    dlg.innerHTML = '<div class="sok-ruta"><div class="sok-falt"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>' +
      '<input type="search" placeholder="Sök tjänster, projekt och frågor …" aria-label="Sök" autocomplete="off"><button type="button" class="sok-stang" aria-label="Stäng sökningen">Esc</button></div>' +
      '<ul class="sok-res" role="listbox"></ul><p class="sok-tom"></p></div>';
    document.body.appendChild(dlg);
    inp = dlg.querySelector("input"); lista = dlg.querySelector(".sok-res"); tom = dlg.querySelector(".sok-tom");
    dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.closest(".sok-stang")) stang(); });
    inp.addEventListener("input", sok);
    inp.addEventListener("keydown", function (e) {
      var akt = lista.querySelector("[aria-selected=true]"), alla = [].slice.call(lista.querySelectorAll("a"));
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        var i = alla.indexOf(akt) + (e.key === "ArrowDown" ? 1 : -1);
        i = Math.max(0, Math.min(alla.length - 1, i));
        alla.forEach(function (a, j) { a.setAttribute("aria-selected", String(j === i)); });
        if (alla[i]) alla[i].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter" && (akt || alla[0])) {
        location.href = (akt || alla[0]).href;
      }
    });
  }

  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function sok() {
    var q = norm(inp.value.trim());
    lista.innerHTML = "";
    if (!q) { tom.textContent = "Till exempel: badrum, kök, altan, offert, ROT"; return; }
    var ord = q.split(/\s+/), res = [];
    (data || []).forEach(function (d) {
      var t = norm(d.t), x = norm(d.x || ""), p = 0;
      for (var i = 0; i < ord.length; i++) {
        if (t.indexOf(ord[i]) > -1) p += 3; else if (x.indexOf(ord[i]) > -1) p += 1; else return;
      }
      res.push([p, d]);
    });
    res.sort(function (a, b) { return b[0] - a[0]; });
    tom.textContent = res.length ? "" : "Inga träffar. Ring 072-002 22 00 så hjälper vi dig.";
    lista.innerHTML = res.slice(0, 12).map(function (r, i) {
      var d = r[1];
      return '<li><a href="' + bas + d.u + '" aria-selected="' + (i === 0) + '"><small>' + esc(d.k) + '</small><b>' + esc(d.t) + '</b>' +
        (d.x ? '<span>' + esc(d.x.slice(0, 120)) + (d.x.length > 120 ? " …" : "") + '</span>' : "") + '</a></li>';
    }).join("");
  }

  function oppna(e) {
    if (e) e.preventDefault();
    if (!dlg) bygg();
    dlg.hidden = false;
    document.documentElement.classList.add("sok-oppen");
    setTimeout(function () { inp.focus(); }, 30);
    if (!data) fetch(bas + "assets/sok.json").then(function (r) { return r.json(); }).then(function (j) { data = j; sok(); }).catch(function () { data = []; sok(); });
    else sok();
  }
  function stang() {
    dlg.hidden = true;
    document.documentElement.classList.remove("sok-oppen");
  }
  knappar.forEach(function (k) { k.addEventListener("click", oppna); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && dlg && !dlg.hidden) stang();
    if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName))) { e.preventDefault(); oppna(); }
  });
})();
