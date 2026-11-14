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
