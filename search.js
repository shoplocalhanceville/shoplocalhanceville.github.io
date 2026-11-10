/*
 * WS5 typo-tolerant search (raw code, no dependencies).
 * Built to WS5_INTELLIGENCE_DESIGN.md section 1.
 *
 * Staged matching, cheapest first, over a prebuilt-in-memory token index:
 *   1. normalize (lowercase, strip diacritics, split on non-alphanumerics)
 *   2. exact token match with field boosts: name > town > category > aka > description
 *   3. prefix match for query tokens of length 3 or more
 *   4. bounded Levenshtein fuzzy match, only for query tokens with no exact
 *      or prefix hit: distance 1 for length 4 to 6, distance 2 for length 7+
 *   5. multi-token queries sum per-token scores; a recognized town token
 *      filters rather than ranks
 *
 * Works in the browser (window.WS5Search) and in Node (module.exports)
 * so the validation lane can run the same file the site ships.
 */
(function (global) {
  'use strict';

  var FIELD_WEIGHT = { name: 8, town: 4, category: 5, aka: 3, description: 1 };
  var FIELD_ORDER = ['name', 'category', 'town', 'aka', 'description'];

  function normalize(text) {
    if (!text) return [];
    var clean = String(text)
      .toLowerCase()
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9]+/g, ' ')
      .trim();
    return clean ? clean.split(' ') : [];
  }

  function normalizeOne(token) {
    var parts = normalize(token);
    return parts.length ? parts[0] : '';
  }

  /* Town derivation, per design section 1: address parse first, then the
   * name parenthetical, then an aka token. Returns '' when no town is
   * derivable; nothing is guessed. */
  var EXTRA_TOWNS = ['garden city', 'dodge city', 'crane hill', 'jones chapel',
    'fairview', 'baileyton', 'west point', 'battleground', 'cold springs',
    'berlin', 'logan', 'bremen', 'trimble', 'arkadelphia', 'walter'];

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

  function deriveTown(record, townSet) {
    var fromAddr = townFromAddress(record.address);
    if (fromAddr) return fromAddr;
    var m = /\(([^)]+)\)\s*$/.exec(record.name || '');
    if (m) {
      var cand = m[1].trim();
      if (townSet[cand.toLowerCase()]) return cand;
      for (var i = 0; i < EXTRA_TOWNS.length; i++) {
        if (cand.toLowerCase() === EXTRA_TOWNS[i]) return cand;
      }
    }
    var akaTokens = normalize(record.aka);
    for (var j = 0; j < akaTokens.length; j++) {
      if (townSet[akaTokens[j]]) return townSet[akaTokens[j]];
    }
    return '';
  }

  function buildTownSet(records) {
    var set = {};
    records.forEach(function (r) {
      var t = townFromAddress(r.address);
      if (t) set[t.toLowerCase()] = t;
    });
    records.forEach(function (r) {
      var m = /\(([^)]+)\)\s*$/.exec(r.name || '');
      if (m && set[m[1].trim().toLowerCase()]) return;
      if (m) {
        var cand = m[1].trim();
        for (var i = 0; i < EXTRA_TOWNS.length; i++) {
          if (cand.toLowerCase() === EXTRA_TOWNS[i]) set[cand.toLowerCase()] = cand;
        }
      }
    });
    return set;
  }

  /* Bounded Levenshtein with early exit: returns true when the edit
   * distance between a and b is at most maxDist. */
  function withinDistance(a, b, maxDist) {
    if (Math.abs(a.length - b.length) > maxDist) return false;
    var prev = [], cur = [], i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur[0] = i;
      var rowMin = cur[0];
      for (j = 1; j <= b.length; j++) {
        var cost = a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1;
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
        if (cur[j] < rowMin) rowMin = cur[j];
      }
      if (rowMin > maxDist) return false;
      var tmp = prev; prev = cur; cur = tmp;
    }
    return prev[b.length] <= maxDist;
  }

  function createSearch(records) {
    var townSet = buildTownSet(records);
    var towns = records.map(function (r) { return deriveTown(r, townSet); });

    /* index: token -> Map(recordIndex -> best field weight) */
    var index = new Map();
    var coreTokens = new Set(); /* name + category + aka + town, the design count */

    function addToken(token, idx, field) {
      if (!token) return;
      var postings = index.get(token);
      if (!postings) { postings = new Map(); index.set(token, postings); }
      var w = FIELD_WEIGHT[field];
      if (!postings.has(idx) || postings.get(idx) < w) postings.set(idx, w);
      if (field !== 'description') coreTokens.add(token);
    }

    records.forEach(function (r, idx) {
      normalize(r.name).forEach(function (t) { addToken(t, idx, 'name'); });
      /* Possessive squash: "Pop's" normalizes to "pop" + "s", but visitors
       * type "pops". Index the joined form for name tokens too. */
      var rawParts = String(r.name || '').toLowerCase()
        .normalize('NFD').replace(/[̀-ͯ]/g, '').split(/\s+/);
      rawParts.forEach(function (p) {
        var sq = p.replace(/[^a-z0-9]/g, '');
        if (sq.length >= 3 && sq !== p) addToken(sq, idx, 'name');
      });
      normalize(r.category).forEach(function (t) { addToken(t, idx, 'category'); });
      normalize(r.aka).forEach(function (t) { addToken(t, idx, 'aka'); });
      normalize(towns[idx]).forEach(function (t) { addToken(t, idx, 'town'); });
      normalize(r.description).forEach(function (t) { addToken(t, idx, 'description'); });
    });

    var vocab = Array.from(index.keys());

    function maxDistFor(len) {
      if (len < 4) return 0;
      if (len <= 6) return 1;
      return 2;
    }

    function scoreToken(qToken, scores) {
      var matched = false;
      /* exact */
      var postings = index.get(qToken);
      if (postings) {
        matched = true;
        postings.forEach(function (w, idx) {
          scores.set(idx, (scores.get(idx) || 0) + w * 1.0);
        });
      }
      /* prefix, query tokens of length 3 or more */
      if (qToken.length >= 3) {
        for (var i = 0; i < vocab.length; i++) {
          var tok = vocab[i];
          if (tok.length > qToken.length && tok.indexOf(qToken) === 0) {
            matched = true;
            index.get(tok).forEach(function (w, idx) {
              scores.set(idx, (scores.get(idx) || 0) + w * 0.7);
            });
          }
        }
      }
      if (matched) return true;
      /* fuzzy, only when nothing above hit */
      var maxDist = maxDistFor(qToken.length);
      if (maxDist === 0) return false;
      for (var j = 0; j < vocab.length; j++) {
        var cand = vocab[j];
        if (Math.abs(cand.length - qToken.length) > maxDist) continue;
        if (withinDistance(qToken, cand, maxDist)) {
          index.get(cand).forEach(function (w, idx) {
            scores.set(idx, (scores.get(idx) || 0) + w * 0.5);
          });
        }
      }
      return true;
    }

    function isTownToken(token) {
      if (townSet[token]) return townSet[token];
      /* two-word towns handled by the caller token stream check below */
      return null;
    }

    function search(query, limit) {
      limit = limit || 20;
      var qTokens = normalize(query);
      if (!qTokens.length) return [];
      var scores = new Map();
      var townFilter = null;

      /* recognize a town phrase (one or two tokens) anywhere in the query */
      for (var i = 0; i < qTokens.length; i++) {
        if (i + 1 < qTokens.length) {
          var pair = qTokens[i] + ' ' + qTokens[i + 1];
          if (townSet[pair]) { townFilter = townSet[pair]; qTokens.splice(i, 2); break; }
        }
        if (townSet[qTokens[i]]) {
          townFilter = townSet[qTokens[i]];
          qTokens.splice(i, 1);
          break;
        }
      }
      /* a token that fuzzy-matches a town also filters, per design rule 4 */
      if (!townFilter) {
        for (var k = 0; k < qTokens.length; k++) {
          var qt = qTokens[k];
          var md = maxDistFor(qt.length);
          if (!md) continue;
          var hit = null;
          Object.keys(townSet).forEach(function (t) {
            if (t.indexOf(' ') === -1 && withinDistance(qt, t, md)) hit = townSet[t];
          });
          if (hit) { townFilter = hit; qTokens.splice(k, 1); break; }
        }
      }

      qTokens.forEach(function (t) { scoreToken(t, scores); });

      var results = [];
      scores.forEach(function (score, idx) {
        if (townFilter && towns[idx] !== townFilter) return;
        results.push({ index: idx, record: records[idx], town: towns[idx], score: score });
      });
      /* if every query token was the town itself, return the town's listings */
      if (!results.length && townFilter && !qTokens.length) {
        records.forEach(function (r, idx) {
          if (towns[idx] === townFilter) {
            results.push({ index: idx, record: r, town: towns[idx], score: 1 });
          }
        });
      }
      results.sort(function (a, b) {
        if (b.score !== a.score) return b.score - a.score;
        return a.record.name < b.record.name ? -1 : 1;
      });
      return results.slice(0, limit);
    }

    return {
      search: search,
      towns: towns,
      stats: {
        records: records.length,
        coreTokens: coreTokens.size,
        totalTokens: index.size,
        townsDeriving: towns.filter(function (t) { return !!t; }).length
      }
    };
  }

  var api = { createSearch: createSearch, normalize: normalize, deriveTown: deriveTown, buildTownSet: buildTownSet };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.WS5Search = api;
})(typeof window !== 'undefined' ? window : globalThis);
