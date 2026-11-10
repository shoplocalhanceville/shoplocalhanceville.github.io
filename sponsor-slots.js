/*
 * sponsor-slots.js - WS2 sponsor slot engine (STAGED, NOT LIVE).
 *
 * Raw JavaScript, no libraries, no cookies, no tracking, no external
 * requests. Reads window.SLH_SPONSORS (see data/sponsors.js) and fills
 * the reserved slot boxes declared in markup:
 *
 *   <div class="sp-slot sp-slot--leaderboard" data-sp-slot="H-1">
 *     <p class="sp-label" data-sp-label></p>
 *     <div class="sp-box sp-box--728x90" data-sp-box></div>
 *   </div>
 *
 * Behavior, per WS2 design sections 3, 4.2, 4.3, 5, 7, 8:
 * - The box geometry and the label line are fixed by CSS before this
 *   script runs, so filling a slot never moves page content.
 * - Rotation is the site's daily pattern: the day index (local calendar
 *   day) selects from the slot's active sponsor pool, so every visitor
 *   sees the same creative on a given day and rotation is even across
 *   a billing month. No server, no cookies, no per-person anything.
 * - P-1 on a profile page whose own business holds a premium package
 *   shows that sponsor fixed for the month; otherwise P-1 rotates from
 *   the general pool like the other rotating slots.
 * - H-2 is a fixed row, not a rotation: one card per active premium
 *   sponsor. In production the page generator emits the month's cards
 *   into the static markup; this script's H-2 path is the fallback and
 *   demo route, and it replaces the markup's house card.
 * - An unsold or out-of-date slot renders the house creative at the
 *   same reserved size, with the house attribution as its label. House
 *   messages never carry the Sponsored label.
 * - Paid slots always render the Sponsored label (Spanish:
 *   Patrocinado) as real text above the creative.
 * - Language comes from window.SLH_LANG, the same boot value the
 *   site's language mode sets ("en" or "es").
 */
(function () {
  "use strict";

  var DATA = window.SLH_SPONSORS;
  if (!DATA || !DATA.slots) { return; }

  function lang() {
    if (window.SLH_LANG === "es") { return "es"; }
    if (window.SLH_LANG === "en") { return "en"; }
    return (document.documentElement.getAttribute("lang") || "en").slice(0, 2) === "es" ? "es" : "en";
  }

  function pick(obj, key) {
    if (!obj) { return ""; }
    return obj[key] || obj.en || "";
  }

  function dayIndex() {
    var d = new Date();
    return Math.floor(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 86400000);
  }

  function todayISO() {
    var d = new Date();
    function p(n) { return (n < 10 ? "0" : "") + n; }
    return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
  }

  function isMobile() {
    return window.matchMedia("(max-width: 760px)").matches;
  }

  function activeSponsors() {
    var t = todayISO();
    return (DATA.sponsors || []).filter(function (s) {
      return s.start <= t && t <= s.end;
    });
  }

  function poolFor(slotId, active) {
    return active.filter(function (s) {
      var tier = DATA.tiers[s.tier];
      return tier && tier.slots.indexOf(slotId) !== -1;
    });
  }

  function creativeFor(entry, slotId, sponsor) {
    var slot = DATA.slots[slotId];
    var bp = isMobile() ? "mobile" : "desktop";
    var size = slot.sizes[bp];
    var sizeKey = size[0] + "x" + size[1];
    if (sponsor) {
      var c = sponsor.creatives && sponsor.creatives[sizeKey];
      if (c) {
        return {
          src: pick(c, lang()),
          href: sponsor.href || sponsor.profile || "#",
          alt: pick(sponsor.alt, lang()),
          w: size[0], h: size[1], paid: true
        };
      }
      return null; /* sponsor lacks this size: intake failure, fall to house */
    }
    var hc = slot.houseCreative[bp];
    return {
      src: pick(hc, lang()),
      href: slot.houseHref || "#",
      alt: pick(slot.houseAlt, lang()),
      w: size[0], h: size[1], paid: false
    };
  }

  function renderInto(slotEl, slotId, creative) {
    var label = slotEl.querySelector("[data-sp-label]");
    var box = slotEl.querySelector("[data-sp-box]");
    if (!box) { return; }
    if (label) {
      label.textContent = creative.paid
        ? pick(DATA.strings.sponsoredLabel, lang())
        : pick(DATA.strings.houseLabel, lang());
      label.classList.toggle("sp-label--house", !creative.paid);
    }
    var a = document.createElement("a");
    a.className = "sp-creative";
    a.href = creative.href;
    var img = document.createElement("img");
    img.src = creative.src;
    img.alt = creative.alt;
    img.width = creative.w;
    img.height = creative.h;
    img.loading = "lazy";
    img.decoding = "async";
    a.appendChild(img);
    box.textContent = "";
    box.appendChild(a);
  }

  function fillRotating(slotEl) {
    var slotId = slotEl.getAttribute("data-sp-slot");
    var active = activeSponsors();
    var sponsor = null;

    if (slotId === "P-1") {
      var profile = slotEl.getAttribute("data-sp-profile");
      if (profile) {
        for (var i = 0; i < active.length; i++) {
          if (active[i].tier === "premium" && active[i].profile === profile) {
            sponsor = active[i];
            break;
          }
        }
      }
    }
    if (!sponsor) {
      var pool = poolFor(slotId, active);
      if (pool.length) { sponsor = pool[dayIndex() % pool.length]; }
    }
    var creative = sponsor && creativeFor(slotEl, slotId, sponsor);
    if (!creative) { creative = creativeFor(slotEl, slotId, null); }
    renderInto(slotEl, slotId, creative);
  }

  function fillRow(rowEl) {
    var slotId = rowEl.getAttribute("data-sp-row");
    var heading = rowEl.querySelector("[data-sp-row-heading]");
    if (heading) { heading.textContent = pick(DATA.strings.ourSponsors, lang()); }
    var active = poolFor(slotId, activeSponsors()).filter(function (s) {
      return DATA.tiers[s.tier].fixedCard;
    });
    var cardsHost = rowEl.querySelector("[data-sp-row-cards]");
    if (!cardsHost) { return; }
    var template = cardsHost.querySelector("[data-sp-slot]");
    if (!template) { return; }
    if (!active.length) {
      renderInto(template, slotId, creativeFor(template, slotId, null));
      return;
    }
    active.forEach(function (sponsor, i) {
      var el = i === 0 ? template : template.cloneNode(true);
      if (i > 0) { cardsHost.appendChild(el); }
      renderInto(el, slotId, creativeFor(el, slotId, sponsor));
    });
  }

  function fillAll() {
    var rows = document.querySelectorAll("[data-sp-row]");
    for (var r = 0; r < rows.length; r++) { fillRow(rows[r]); }
    var slots = document.querySelectorAll("[data-sp-slot]");
    for (var i = 0; i < slots.length; i++) {
      if (!slots[i].closest("[data-sp-row]")) { fillRotating(slots[i]); }
    }
  }

  var resizeTimer = null;
  window.addEventListener("resize", function () {
    if (resizeTimer) { return; }
    resizeTimer = window.setTimeout(function () {
      resizeTimer = null;
      fillAll();
    }, 200);
  });

  /* If the language mode changes without a reload, refill so labels
     and language-matched creatives follow. */
  if (window.MutationObserver) {
    var lastLang = lang();
    new MutationObserver(function () {
      if (lang() !== lastLang) { lastLang = lang(); fillAll(); }
    }).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fillAll);
  } else {
    fillAll();
  }
})();
