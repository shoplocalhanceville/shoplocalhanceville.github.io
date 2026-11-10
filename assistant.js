/*
 * WS5 directory assistant (raw code, no dependencies).
 * Built to WS5_INTELLIGENCE_DESIGN.md section 3.
 *
 * Answer discipline, enforced by construction: the assistant answers ONLY
 * by matching a question to a small whitelist of intents (phone, address,
 * hours, website, facebook, category, about) plus a named record or a
 * service-plus-town search, and then stating values copied from that
 * record's own verified fields. There is no code path that composes a
 * factual sentence from anything else. A question that matches no
 * whitelist intent, matches no record, or asks for a field the matched
 * record does not carry gets the fixed refusal, word for word. Crisis
 * intents bypass ranking and lead with the Crisis & Emergency records.
 *
 * The pure core (createAssistant) runs in Node for the test battery and
 * in the browser. The dialog wiring at the bottom runs only in a browser
 * and only when initAssistant() is called, which the page does lazily on
 * the first activation of the Ask button (design section 5).
 */
(function (global) {
  'use strict';

  var REFUSAL = {
    en: 'I don\'t have that in the verified listings. Try the search above, ' +
        'or browse the Community Guide. Every listing there shows exactly ' +
        'what we have confirmed.',
    es: 'No tengo ese dato en los listados verificados. Pruebe la búsqueda ' +
        'o explore la Guía de la Comunidad; cada listado muestra exactamente ' +
        'lo que hemos confirmado.'
  };

  var LABELS = {
    en: { phone: 'Phone', address: 'Address', hours: 'Hours', website: 'Website',
          facebook: 'Facebook', category: 'Category', description: 'Listing text',
          noHours: 'I do not have confirmed hours for this listing. ' +
                   'The listing shows a phone number you can call.',
          crisis: 'If this is an emergency, call 911 now. ' +
                  'These verified help lines are answered day and night:' },
    es: { phone: 'Teléfono', address: 'Dirección', hours: 'Horario', website: 'Sitio web',
          facebook: 'Facebook', category: 'Categoría', description: 'Texto del listado',
          noHours: 'No tengo un horario confirmado para este listado. ' +
                   'El listado muestra un número de teléfono al que puede llamar.',
          crisis: 'Si esto es una emergencia, llame al 911 ahora. ' +
                  'Estas líneas de ayuda verificadas atienden día y noche:' }
  };

  /* Intent vocabularies, English and Spanish. A question earns an answer
   * only if it hits one of these AND resolves to a record that carries
   * the asked field. Anything else falls through to the refusal. */
  var INTENT_TOKENS = {
    phone: ['phone', 'number', 'call', 'telefono', 'numero', 'llamar'],
    address: ['address', 'where', 'located', 'location', 'directions',
              'direccion', 'donde', 'ubicado', 'ubicacion', 'llegar'],
    hours: ['hours', 'hour', 'open', 'close', 'closes', 'closing', 'when',
            'horario', 'hora', 'abierto', 'abierta', 'cierra', 'cuando'],
    website: ['website', 'web', 'site', 'online', 'sitio'],
    facebook: ['facebook'],
    category: ['category', 'kind', 'type', 'categoria', 'tipo'],
    about: ['about', 'tell', 'describe', 'sobre', 'cuentame']
  };

  /* Hard refusal guards. Prices, opinions, private personal data, and
   * professional advice are never carried in verified listing fields,
   * so any question carrying one of these tokens refuses outright,
   * before intent matching. This is what makes the refusal rate a
   * property of the code rather than of phrasing luck. */
  var GUARD_TOKENS = [
    /* price */ 'cost', 'costs', 'price', 'prices', 'pricing', 'charge',
      'cuesta', 'cuestan', 'precio', 'precios', 'cuanto',
    /* opinion */ 'best', 'worst', 'recommend', 'recommended', 'favorite',
      'mejor', 'peor', 'recomienda', 'recomiendas', 'favorito',
    /* private data */ 'owner', 'owners', 'propietario', 'personal',
      'private', 'privado', 'cellphone',
    /* advice domains */ 'doctor', 'symptom', 'symptoms', 'sick', 'rash',
      'diagnose', 'lawyer', 'legal', 'sue', 'court', 'invest', 'stocks',
      'abogado', 'medico', 'sintomas', 'enfermo'
  ];
  var FIELD_OF_INTENT = { phone: 'phone', address: 'address', hours: 'hours',
    website: 'website', facebook: 'facebook', category: 'category', about: 'description' };

  var CRISIS_TOKENS = ['suicide', 'kill', 'hurt', 'emergency', 'danger',
    'abuse', 'crisis', '911', 'suicidio', 'emergencia', 'peligro', 'ayuda'];
  var CRISIS_PHRASES = ['help right now', 'need help', 'hurt myself',
    'necesito ayuda', 'ayuda ahora'];

  function normalize(text) {
    if (!text) return [];
    var clean = String(text).toLowerCase().normalize('NFD')
      .replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
    return clean ? clean.split(' ') : [];
  }

  function hasField(record, field) {
    var v = record[field];
    return v !== undefined && v !== null && String(v).trim() !== '';
  }

  /* Stopwords are stripped before the question reaches the search
   * engine. The engine is tuned for keyword queries; sentence words
   * like "where" and "can" otherwise match description prose across
   * hundreds of records and swamp the ranking. Intent detection and
   * the guards still run on the full token stream. */
  var STOPWORDS = ['where', 'what', 'when', 'which', 'who', 'whom', 'can',
    'could', 'would', 'should', 'is', 'are', 'was', 'were', 'do', 'does',
    'did', 'the', 'a', 'an', 'in', 'on', 'at', 'of', 'for', 'to', 'me',
    'my', 'i', 'you', 'please', 'tell', 'get', 'got', 'find', 'show',
    'que', 'cual', 'cuales', 'donde', 'como', 'cuando', 'quien', 'es',
    'son', 'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'en',
    'por', 'para', 'me', 'mi', 'hay', 'puedo', 'quiero'];

  function createAssistant(records, searchEngine, opts) {
    opts = opts || {};
    var lang = opts.lang === 'es' ? 'es' : 'en';
    var labels = LABELS[lang];

    function refusal(recs) {
      return { type: 'refusal', text: REFUSAL[lang], records: recs || [] };
    }

    function detectIntent(tokens) {
      var found = null;
      Object.keys(INTENT_TOKENS).forEach(function (intent) {
        if (found) return;
        for (var i = 0; i < tokens.length; i++) {
          if (INTENT_TOKENS[intent].indexOf(tokens[i]) !== -1) { found = intent; return; }
        }
      });
      return found;
    }

    var STRONG_CRISIS = ['suicide', 'suicidio', '911'];
    function isCrisis(rawLower, tokens) {
      for (var i = 0; i < CRISIS_PHRASES.length; i++) {
        if (rawLower.indexOf(CRISIS_PHRASES[i]) !== -1) return true;
      }
      if (tokens.some(function (t) { return STRONG_CRISIS.indexOf(t) !== -1; })) return true;
      return tokens.some(function (t) { return CRISIS_TOKENS.indexOf(t) !== -1; }) &&
             tokens.some(function (t) {
               return ['help', 'need', 'hurt', 'myself', 'ayuda', 'necesito'].indexOf(t) !== -1;
             });
    }

    function ask(question) {
      var rawLower = ' ' + String(question || '').toLowerCase() + ' ';
      var tokens = normalize(question);

      /* Crisis bypass: leads with the emergency records, unranked. */
      if (isCrisis(rawLower, tokens)) {
        var crisis = records.filter(function (r) {
          return r.category === 'Crisis & Emergency';
        });
        crisis.sort(function (a, b) { return a.name < b.name ? -1 : 1; });
        /* 911 first, then the rest by name, per the design example. */
        crisis.sort(function (a, b) {
          var aE = a.name.indexOf('911') !== -1 ? 0 : 1;
          var bE = b.name.indexOf('911') !== -1 ? 0 : 1;
          return aE - bE;
        });
        return { type: 'crisis', text: labels.crisis, records: crisis };
      }

      for (var g = 0; g < tokens.length; g++) {
        if (GUARD_TOKENS.indexOf(tokens[g]) !== -1) return refusal();
      }

      var intent = detectIntent(tokens);
      if (!intent) return refusal();

      var field = FIELD_OF_INTENT[intent];
      var searchQuery = tokens.filter(function (t) {
        return STOPWORDS.indexOf(t) === -1;
      }).join(' ');
      var results = searchEngine.search(searchQuery || question, 5);
      if (!results.length) return refusal();

      /* Score band: only records scoring at least 60 percent of the top
       * hit may answer. This stops a question about one listing from
       * being answered out of a different listing's fields. */
      var topScore = results[0].score;
      var band = results.filter(function (x) { return x.score >= 0.6 * topScore; });

      if (intent === 'hours') {
        for (var i = 0; i < band.length; i++) {
          var rec = band[i].record;
          if (hasField(rec, 'hours') || hasField(rec, 'hs')) {
            var val = hasField(rec, 'hours') ? rec.hours : JSON.stringify(rec.hs);
            return { type: 'answer',
              text: labels.hours + ': ' + val + ' (' + rec.name + ')',
              records: [rec] };
          }
        }
        /* Matched a listing, but no verified hours on it: the design's
         * fact-form refusal, showing the card and its phone if carried. */
        return { type: 'refusal', text: labels.noHours + ' ' + REFUSAL[lang],
          records: [band[0].record] };
      }

      for (var j = 0; j < band.length; j++) {
        var r = band[j].record;
        if (hasField(r, field)) {
          var value = field === 'description' ? r.description : r[field];
          return { type: 'answer',
            text: labels[field] + ': ' + value + ' (' + r.name + ')',
            records: [r] };
          }
      }
      /* Service-plus-town questions ("where can I get a haircut in
       * Hanceville") resolve to the matched listings themselves; the
       * cards carry the verified fields the visitor needs. */
      if ((intent === 'address' || intent === 'about') && band.length > 1) {
        var cards = band.slice(0, 3).map(function (x) { return x.record; });
        var lead = cards.map(function (c) {
          return c.name + (hasField(c, 'address') ? ', ' + c.address : '') +
                 (hasField(c, 'phone') ? ', ' + c.phone : '');
        }).join('; ');
        return { type: 'answer', text: lead, records: cards };
      }
      return refusal([band[0].record]);
    }

    return { ask: ask, REFUSAL: REFUSAL };
  }

  /* ---------------- Browser dialog wiring (never runs in Node) -------- */
  function initAssistant(cfg) {
    var dialog = document.getElementById('ws5-assistant');
    if (!dialog) return;
    var form = dialog.querySelector('form');
    var input = dialog.querySelector('input');
    var out = dialog.querySelector('[data-ws5-out]');
    var cards = dialog.querySelector('[data-ws5-cards]');
    var assistant = createAssistant(cfg.records, cfg.searchEngine, { lang: cfg.lang });
    document.querySelectorAll('[data-ws5-ask]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (typeof dialog.showModal === 'function') dialog.showModal();
        else dialog.setAttribute('open', '');
        input.focus();
      });
    });
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var res = assistant.ask(input.value);
      out.textContent = res.text;
      cards.innerHTML = '';
      res.records.forEach(function (r) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.textContent = r.name;
        a.href = cfg.profileUrl ? cfg.profileUrl(r) : '#';
        li.appendChild(a);
        if (r.phone) li.appendChild(document.createTextNode(' · ' + r.phone));
        if (r.address) li.appendChild(document.createTextNode(' · ' + r.address));
        cards.appendChild(li);
      });
    });
  }

  var api = { createAssistant: createAssistant, initAssistant: initAssistant, REFUSAL: REFUSAL };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.WS5Assistant = api;
})(typeof window !== 'undefined' ? window : globalThis);
