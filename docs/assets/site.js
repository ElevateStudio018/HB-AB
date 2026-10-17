(function () {
  "use strict";

  // Menu on small screens: opens under the header.
  var btn = document.getElementById("menuBtn");
  var menu = document.getElementById("menu");
  if (btn && menu) {
    function setOpen(open) {
      menu.hidden = !open;
      btn.setAttribute("aria-expanded", String(open));
      btn.setAttribute("aria-label", open ? "Stäng menyn" : "Meny");
    }
    btn.addEventListener("click", function () { setOpen(menu.hidden); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !menu.hidden) { setOpen(false); btn.focus(); }
    });
  }

  // Home page: the header is transparent over the full-screen hero and turns white once the page scrolls.
  var head = document.getElementById("head");
  if (head && head.classList.contains("head-over")) {
    var onScroll = function () { head.classList.toggle("solid", window.scrollY > 40 || (menu && !menu.hidden)); };
    window.addEventListener("scroll", onScroll, { passive: true });
    if (btn) btn.addEventListener("click", onScroll);
    onScroll();
  }

  document.querySelectorAll("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });

  // Project filter.
  var tabs = document.querySelectorAll(".tab");
  tabs.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var cat = chip.getAttribute("data-filter");
      tabs.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
      document.querySelectorAll(".pcard").forEach(function (p) {
        p.hidden = !!cat && p.getAttribute("data-cat") !== cat;
      });
    });
  });

  // Quote form: checked here, e-mailed through FormSubmit, then a thank-you in its place.
  var form = document.getElementById("qform");
  if (!form) return;
  var done = document.getElementById("qdone");
  var sendErr = document.getElementById("send-err");
  var f = {
    namn: document.getElementById("f-namn"),
    tel: document.getElementById("f-tel"),
    epost: document.getElementById("f-epost"),
    typ: document.getElementById("f-typ"),
    start: document.getElementById("f-start"),
    adress: document.getElementById("f-adress"),
    besk: document.getElementById("f-besk"),
    web: document.getElementById("f-web")
  };

  // "Begär offert" on a service page arrives with ?typ=… and that type chosen.
  var typ = new URLSearchParams(location.search).get("typ");
  if (typ) {
    for (var i = 0; i < f.typ.options.length; i++) if (f.typ.options[i].text === typ) f.typ.selectedIndex = i;
  }

  function mark(key, input, bad) {
    document.getElementById("e-" + key).hidden = !bad;
    input.setAttribute("aria-invalid", bad ? "true" : "false");
    if (bad) input.setAttribute("aria-describedby", "e-" + key); else input.removeAttribute("aria-describedby");
  }
  function validate() {
    var bad = [];
    var tel = f.tel.value.trim(), ep = f.epost.value.trim();
    var namnBad = !f.namn.value.trim();
    var contactBad = !tel && !ep;
    var epBad = !!ep && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(ep);
    mark("namn", f.namn, namnBad); if (namnBad) bad.push(f.namn);
    mark("tel", f.tel, contactBad); if (contactBad) bad.push(f.tel);
    mark("epost", f.epost, epBad); if (epBad) bad.push(f.epost);
    return bad;
  }
  form.addEventListener("input", function (e) {
    if (e.target.getAttribute("aria-invalid") === "true" || e.target === f.tel || e.target === f.epost) validate();
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = validate();
    if (bad.length) { bad[0].focus(); return; }
    var submit = form.querySelector("button[type=submit]");
    submit.disabled = true;
    submit.textContent = "Skickar …";
    sendErr.hidden = true;
    var payload = {
      _subject: "Offertförfrågan från hemsidan – " + f.namn.value.trim(),
      _template: "table",
      _captcha: "false",
      _honey: f.web.value,
      Namn: f.namn.value.trim(),
      Telefon: f.tel.value.trim() || "–",
      "E-post": f.epost.value.trim() || "–",
      Kundtyp: (form.querySelector("input[name=kund]:checked") || {}).value || "–",
      "Typ av uppdrag": f.typ.value || "–",
      "Önskad start": f.start.value || "–",
      "Adress/ort": f.adress.value.trim() || "–",
      Beskrivning: f.besk.value.trim() || "–",
      Sida: location.pathname
    };
    if (f.epost.value.trim()) payload._replyto = f.epost.value.trim();
    fetch(form.getAttribute("data-endpoint"), {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().catch(function () { return null; }).then(function (j) {
        if (!r.ok || !j || String(j.success) !== "true") throw new Error("not sent");
      });
    }).then(function () {
      form.reset();
      form.hidden = true;
      done.hidden = false;
      done.focus();
    }).catch(function () {
      // Kept as typed, so it can be sent again or read out over the phone.
      sendErr.hidden = false;
    }).then(function () {
      submit.disabled = false;
      submit.textContent = "Skicka offertförfrågan";
    });
  });

  document.getElementById("qagain").addEventListener("click", function () {
    done.hidden = true;
    form.hidden = false;
    f.namn.focus();
  });
})();
