/*
 * WS5 deterministic recommendation rails (raw code, no dependencies).
 * Built to WS5_INTELLIGENCE_DESIGN.md section 2.
 *
 * Rules, in order, all computed from verified fields on the records
 * themselves. No cookies, no behavioral data, no visitor history: the
 * same listing always produces the same rail, byte for byte.
 *
 *   Rule 1. Same service, same town: records sharing the viewed record's
 *           category and derived town.
 *   Rule 2. Same service, nearby towns: if rule 1 returns fewer than
 *           three, fill from the same category in other towns.
 *   Rule 3. Same town, related errands: records in the viewed record's
 *           town whose categories the static pairing table below links
 *           to the viewed record's category, capped at four.
 *   Rule 4. Official and emergency neighbors: when the viewed record is
 *           in a government, safety, or help category, same-set records
 *           are offered as their own rail.
 *
 * Town derivation is shared with search.js when it is loaded first;
 * a local copy of the same derivation is kept here so this file also
 * works standalone. The two implementations are the same rules and are
 * covered by the same determinism test.
 */
(function (global) {
  'use strict';

  /* Curated static pairing table (design rule 3). One line per link,
   * reviewed like any other listing fact. Keys and values are category
   * names exactly as they appear in the data. */
  var PAIRINGS = {
    'Barbers & Salons': ['Downtown Shops', 'Shopping & Retail'],
    'Downtown Shops': ['Barbers & Salons', 'Drinks & Coffee', 'Shopping & Retail'],
    'Drinks & Coffee': ['Downtown Shops', 'More Places to Eat', 'Markets'],
    'More Places to Eat': ['Drinks & Coffee', 'Markets'],
    'Tires': ['Auto Repair & Mechanics', 'Towing', 'Auto Sales'],
    'Auto Repair & Mechanics': ['Tires', 'Towing', 'Auto Sales'],
    'Towing': ['Auto Repair & Mechanics', 'Tires'],
    'Auto Sales': ['Auto Repair & Mechanics', 'Finance & Insurance'],
    'Churches & Faith': ['Community Groups', 'Feeding Neighbors'],
    'Feeding Neighbors': ['Churches & Faith', 'Food & SNAP', 'Help & Resources'],
    'Food & SNAP': ['Feeding Neighbors', 'Finance & Insurance'],
    'Lodging': ['More Places to Eat', 'Local Landmarks'],
    'Pets & Child Care': ['Child Care', 'Health, Safety and Support'],
    'Child Care': ['Pets & Child Care', 'Schools'],
    'Schools': ['Government & Schools', 'Jobs & Education'],
    'Shopping & Retail': ['Downtown Shops', 'Markets', 'Local Businesses'],
    'Markets': ['Shopping & Retail', 'Makers'],
    'Health, Safety and Support': ['Help & Resources', 'Seniors & Elderly'],
    'Seniors & Elderly': ['Health, Safety and Support', 'Help & Resources'],
    'Local Businesses': ['Shopping & Retail', 'Home Services'],
    'Home Services': ['Local Businesses', 'Utilities & Public Works']
  };

  var OFFICIAL_SET = ['City Hall & Government', 'Government & Schools',
    'Public Safety', 'Help & Resources', 'Crisis & Emergency',
    'Boards and Committees', 'Utilities & Public Works', 'Federal Programs'];

  function townFromAddress(address) {
    if (!address) return '';
    var parts = String(address).split(',');
    for (var i = parts.length - 1; i >= 0; i--) {
      var seg = parts[i].trim();
      if (/^AL\b/i.test(seg) || /^\d{5}/.test(seg)) continue;
      if (/suite|ste\.?|building|room|apt|unit|#/i.test(seg)) continue;
      if (!seg || /\d/.test(seg)) continue;
      return seg;
    }
    return '';
  }

  var EXTRA_TOWNS = ['garden city', 'dodge city', 'crane hill', 'jones chapel',
    'fairview', 'baileyton', 'west point', 'battleground', 'cold springs',
    'berlin', 'logan', 'bremen', 'trimble', 'arkadelphia', 'walter'];

  function normTokens(text) {
    if (!text) return [];
    var clean = String(text).toLowerCase().normalize('NFD')
      .replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
    return clean ? clean.split(' ') : [];
  }

  function buildTownSet(records) {
    var set = {};
    records.forEach(function (r) {
      var t = townFromAddress(r.address);
      if (t) set[t.toLowerCase()] = t;
    });
    records.forEach(function (r) {
      var m = /\(([^)]+)\)\s*$/.exec(r.name || '');
      if (m) {
        var cand = m[1].trim();
        for (var i = 0; i < EXTRA_TOWNS.length; i++) {
          if (cand.toLowerCase() === EXTRA_TOWNS[i]) set[cand.toLowerCase()] = cand;
        }
      }
    });
    return set;
  }

  function deriveTown(record, townSet) {
    var fromAddr = townFromAddress(record.address);
    if (fromAddr) return fromAddr;
    var m = /\(([^)]+)\)\s*$/.exec(record.name || '');
    if (m) {
      var cand = m[1].trim();
      if (townSet[cand.toLowerCase()]) return cand;
    }
    var akaTokens = normTokens(record.aka);
    for (var j = 0; j < akaTokens.length; j++) {
      if (townSet[akaTokens[j]]) return townSet[akaTokens[j]];
    }
    return '';
  }

  function byName(a, b) { return a.name < b.name ? -1 : (a.name > b.name ? 1 : 0); }

  function createRecommender(records) {
    var townSet = buildTownSet(records);
    var towns = records.map(function (r) { return deriveTown(r, townSet); });
    var indexOf = new Map();
    records.forEach(function (r, i) { indexOf.set(r.name, i); });

    function recommend(nameOrRecord, perRail) {
      perRail = perRail || 6;
      var idx = typeof nameOrRecord === 'string'
        ? indexOf.get(nameOrRecord) : records.indexOf(nameOrRecord);
      if (idx === undefined || idx < 0) return [];
      var me = records[idx];
      var myTown = towns[idx];
      var rails = [];

      /* Rule 1 and 2: same category, same town first, then other towns. */
      var sameCat = [];
      records.forEach(function (r, i) {
        if (i !== idx && r.category === me.category) {
          sameCat.push({ record: r, town: towns[i] });
        }
      });
      var sameTown = sameCat.filter(function (e) {
        return myTown && e.town === myTown;
      }).sort(function (a, b) { return byName(a.record, b.record); });
      var rail1 = sameTown.slice(0, perRail).map(function (e) { return e.record; });
      if (rail1.length) {
        rails.push({
          rule: 'same-category-same-town',
          heading: { en: 'More in ' + me.category + (myTown ? ' in ' + myTown : ''),
                     es: 'Más en ' + me.category + (myTown ? ' en ' + myTown : '') },
          items: rail1
        });
      }
      if (sameTown.length < 3) {
        var others = sameCat.filter(function (e) {
          return !myTown || e.town !== myTown;
        }).sort(function (a, b) {
          if (a.town !== b.town) return a.town < b.town ? -1 : 1;
          return byName(a.record, b.record);
        });
        var fill = others.slice(0, Math.max(0, perRail - rail1.length))
          .map(function (e) { return e.record; });
        if (fill.length) {
          rails.push({
            rule: 'same-category-other-towns',
            heading: { en: 'More in ' + me.category + ' nearby',
                       es: 'Más en ' + me.category + ' cerca' },
            items: fill
          });
        }
      }

      /* Rule 3: same town, paired categories, capped at four. */
      var paired = PAIRINGS[me.category] || [];
      if (myTown && paired.length) {
        var errands = [];
        records.forEach(function (r, i) {
          if (i !== idx && towns[i] === myTown &&
              paired.indexOf(r.category) !== -1) errands.push(r);
        });
        errands.sort(byName);
        errands = errands.slice(0, 4);
        if (errands.length) {
          rails.push({
            rule: 'same-town-paired',
            heading: { en: 'While you are in ' + myTown,
                       es: 'Mientras está en ' + myTown },
            items: errands
          });
        }
      }

      /* Rule 4: official and emergency neighbors. */
      if (OFFICIAL_SET.indexOf(me.category) !== -1) {
        var officials = [];
        records.forEach(function (r, i) {
          if (i !== idx && r.category !== me.category &&
              OFFICIAL_SET.indexOf(r.category) !== -1) officials.push(r);
        });
        officials.sort(byName);
        officials = officials.slice(0, perRail);
        if (officials.length) {
          rails.push({
            rule: 'official-neighbors',
            heading: { en: 'Related offices and help',
                       es: 'Oficinas y ayuda relacionadas' },
            items: officials
          });
        }
      }
      return rails;
    }

    return { recommend: recommend, towns: towns };
  }

  var api = { createRecommender: createRecommender, PAIRINGS: PAIRINGS, OFFICIAL_SET: OFFICIAL_SET };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.WS5Recommend = api;
})(typeof window !== 'undefined' ? window : globalThis);
