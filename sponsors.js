/*
 * sponsors.js - WS2 sponsor data file (STAGED, NOT LIVE).
 *
 * Format follows the site's existing data conventions (compare data.js,
 * which exposes window.SLH_LISTINGS): one global object, plain data,
 * no build step, edited by hand when a sponsor package is approved.
 *
 * STATE OF THIS FILE: the inventory below is real (slots, sizes, tiers,
 * prices approved 2026-11-03). The sponsors array is EMPTY. No business
 * has been offered, sold, or promised anything. Do not add an entry here
 * until Charles Adams has approved the sponsor package and its offer
 * wording, the creative has passed intake (exact size, 60 KB cap,
 * English and Spanish text alternatives, rights verified), and the
 * publishing pause has been lifted for the WS2 package.
 *
 * Sponsor entry shape (one object per sponsor):
 * {
 *   id: "unique-short-id",
 *   business: "Business name as verified on its listing",
 *   profile: "place-<slug>.html",          // sponsor's page on this site
 *   tier: "spotlight" | "premium",
 *   start: "YYYY-MM-DD",                    // first day the creative runs
 *   end: "YYYY-MM-DD",                      // last day the creative runs
 *   href: "place-<slug>.html",              // default: the profile page.
 *                                           // An outside website only if
 *                                           // it already passes the site's
 *                                           // normal link verification.
 *   creatives: {
 *     "728x90":  { en: "img/sponsors/<file>.webp", es: "img/sponsors/<file>.webp" },
 *     "320x50":  { en: "img/sponsors/<file>.webp", es: "img/sponsors/<file>.webp" },
 *     "300x250": { en: "img/sponsors/<file>.webp", es: "img/sponsors/<file>.webp" }
 *   },
 *   alt: {
 *     en: "Sponsored: <Business>, view profile",   // names sponsor + action
 *     es: "Patrocinado: <Business>, ver perfil"
 *   }
 * }
 * A spotlight entry needs the "728x90", "320x50", and "300x250" creatives.
 * A premium entry needs the same three; its "300x250" also serves its
 * fixed H-2 card and its P-1 page-sponsor placement.
 */
window.SLH_SPONSORS = {
  version: 1,
  updated: "2026-11-08",

  /* Fixed furniture strings, shipped with the slots per the WS2 design
     section 8 (Spanish parity is a build requirement, not a follow-up). */
  strings: {
    sponsoredLabel: { en: "Sponsored", es: "Patrocinado" },
    houseLabel: {
      en: "From Hanceville Entertainment and Shopping",
      es: "De Hanceville Entertainment and Shopping"
    },
    ourSponsors: { en: "Our Sponsors", es: "Nuestros patrocinadores" },
    sponsorsPageName: { en: "Sponsors", es: "Patrocinadores" }
  },

  /* Approved pricing, 2026-11-03. Recorded here so the sponsors section
     page and any future offer render from one source of truth. Nothing
     in this file is an offer; offer wording is a separate approval. */
  tiers: {
    spotlight: {
      priceMonthly: 175,
      slots: ["H-1", "C-1"],
      sponsorsPageCard: true,
      fixedCard: false,
      ownProfileSlot: false
    },
    premium: {
      priceMonthly: 350,
      slots: ["H-1", "C-1", "H-2", "P-1"],
      sponsorsPageCard: true,
      fixedCard: true,
      ownProfileSlot: true
    }
  },

  /* Slot inventory per WS2 design section 2. Sizes are IAB units.
     fallback "house" means an unsold slot renders the house creative at
     the same reserved size; per design section 3 the box never changes
     size and never collapses on the homepage strip. */
  slots: {
    "H-1": {
      page: "home",
      position: "Between the lead news block and the Community Guide rails",
      sizes: { desktop: [728, 90], mobile: [320, 50] },
      houseCreative: {
        desktop: { en: "img/sponsors/house-leaderboard-728x90.webp", es: "img/sponsors/house-leaderboard-728x90.webp" },
        mobile: { en: "img/sponsors/house-banner-320x50.webp", es: "img/sponsors/house-banner-320x50.webp" }
      },
      houseAlt: {
        en: "Hanceville Entertainment and Shopping Community Guide: find local businesses, news, and events",
        es: "Guía comunitaria de Hanceville Entertainment and Shopping: encuentre negocios locales, noticias y eventos"
      },
      houseHref: "places.html"
    },
    "H-2": {
      page: "home",
      position: "One card inside the dedicated Our Sponsors row",
      sizes: { desktop: [300, 250], mobile: [300, 250] },
      houseCreative: {
        desktop: { en: "img/sponsors/house-rectangle-300x250.webp", es: "img/sponsors/house-rectangle-300x250.webp" },
        mobile: { en: "img/sponsors/house-rectangle-300x250.webp", es: "img/sponsors/house-rectangle-300x250.webp" }
      },
      houseAlt: {
        en: "Hanceville Entertainment and Shopping: register or update your business listing",
        es: "Hanceville Entertainment and Shopping: registre o actualice la ficha de su negocio"
      },
      houseHref: "places.html"
    },
    "C-1": {
      page: "category",
      position: "After the first group of listing tiles, in the tile flow",
      sizes: { desktop: [300, 250], mobile: [300, 250] },
      houseCreative: {
        desktop: { en: "img/sponsors/house-rectangle-300x250.webp", es: "img/sponsors/house-rectangle-300x250.webp" },
        mobile: { en: "img/sponsors/house-rectangle-300x250.webp", es: "img/sponsors/house-rectangle-300x250.webp" }
      },
      houseAlt: {
        en: "Hanceville Entertainment and Shopping Community Guide: find local businesses, news, and events",
        es: "Guía comunitaria de Hanceville Entertainment and Shopping: encuentre negocios locales, noticias y eventos"
      },
      houseHref: "places.html"
    },
    "P-1": {
      page: "profile",
      position: "Below the profile facts, hours, and action buttons",
      sizes: { desktop: [300, 250], mobile: [300, 250] },
      houseCreative: {
        desktop: { en: "img/sponsors/house-rectangle-300x250.webp", es: "img/sponsors/house-rectangle-300x250.webp" },
        mobile: { en: "img/sponsors/house-rectangle-300x250.webp", es: "img/sponsors/house-rectangle-300x250.webp" }
      },
      houseAlt: {
        en: "Hanceville Entertainment and Shopping Community Guide: find local businesses, news, and events",
        es: "Guía comunitaria de Hanceville Entertainment and Shopping: encuentre negocios locales, noticias y eventos"
      },
      houseHref: "places.html"
    }
  },

  /* EMPTY. No sponsors exist. See the entry shape documented above. */
  sponsors: []
};
