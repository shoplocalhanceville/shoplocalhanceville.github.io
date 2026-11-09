# ---------- Spanish pages, written natively in Spanish ----------
ES_SEO={
 'es':("Hanceville, Alabama: servicios de la ciudad, Alcaldía y contactos en español","Guía en español de Hanceville, Alabama 35077: teléfonos de la Alcaldía, departamentos de la ciudad, reuniones del Concejo, cómo pagar el agua, refugios contra tornados y cómo reportar un problema."),
 'es-servicios':("Servicios de la ciudad de Hanceville, AL: agua, permisos, parques y refugios","Servicios de la Ciudad de Hanceville en español: pagar el recibo del agua, permisos y licencias, placas de auto, parques, biblioteca, refugios contra tornados y alertas de la ciudad."),
 'es-departamentos':("Departamentos de la Ciudad de Hanceville: teléfonos, correos y horarios","Cada departamento de la Ciudad de Hanceville con la persona de contacto, su cargo, teléfono, correo, dirección y horario, tal como los publica la ciudad."),
 'es-concejo':("Concejo Municipal de Hanceville: miembros, alcalde y reuniones","Conozca al alcalde y a los cinco miembros del Concejo Municipal de Hanceville, Alabama, y vea las próximas reuniones en la Alcaldía con enlaces para agregarlas a su calendario."),
 'es-reportar':("Reportar un problema en Hanceville: baches, luces de la calle y fugas de agua","Reporte un bache, una luz de la calle apagada, una fuga de agua o un problema en un parque de Hanceville. Le preparamos un correo para el departamento correcto."),
}
for k,(t,d) in ES_SEO.items():SEO[k]=(E(t),E(d))
ES_NOTE_TOP='<p class="es-note">'+I('info')+' Estas páginas están escritas en español. El resto del sitio está en inglés, y los enlaces marcados <span lang="en">(en inglés)</span> llevan a páginas en inglés.</p>'
CHM=CH_MAP
ES_DEP={
 "Mayor's Office":("Oficina del Alcalde","Alcalde","De lunes a viernes. La ciudad publica dos horarios distintos en sus páginas, así que le recomendamos llamar antes de ir.","El alcalde dirige el trabajo diario de los departamentos de la ciudad, colabora con el Concejo en las políticas y el presupuesto, y también vota como miembro del Concejo."),
 "City Clerk":("Secretaría Municipal","Secretaria municipal",None,"La Secretaría Municipal guarda los registros oficiales de la ciudad y prepara las agendas y actas del Concejo. Teja McIntyre juró el cargo el 23 de julio de 2026."),
 "Permits, Business Licenses and Facility Rentals":("Permisos, licencias de negocio y alquiler de instalaciones","Permisos, licencias y alquileres",None,"Llame o escriba aquí para permisos de construcción, licencias de negocio, solicitudes de licencia de bebidas alcohólicas y preguntas sobre el alquiler de un edificio de la ciudad."),
 "Accounts Payable and Receivable":("Cuentas por pagar y por cobrar","Cuentas por pagar y por cobrar",None,"Esta oficina maneja los pagos que la ciudad hace y recibe. Si usted es proveedor o tiene una pregunta de facturación, empiece aquí."),
 "Human Resources":("Recursos Humanos","Directora de Recursos Humanos",None,"Recursos Humanos atiende los empleos de la ciudad y las preguntas de los empleados. El 17 de octubre de 2026 la página de empleos de la ciudad no mostraba vacantes."),
 "Hanceville Fire and Rescue":("Bomberos y Rescate de Hanceville","Línea de la estación, no emergencias",None,"Los bomberos responden llamadas a toda hora. Use la línea que no es de emergencia para permisos de quema, el programa gratuito de detectores de humo y preguntas generales. En una emergencia, llame al 911. El Concejo confirmó la destitución del jefe de bomberos el 8 de octubre de 2026, y cuando revisamos todavía no se había nombrado a un reemplazo."),
 "Law Enforcement":("Seguridad pública y policía","Oficina del Alguacil del Condado de Cullman, línea que no es de emergencia",None,"La ciudad disolvió su departamento de policía y su tribunal municipal en febrero de 2026. Desde entonces, los alguaciles del Condado de Cullman patrullan Hanceville. El Concejo trabaja en las normas para volver a tener un departamento de policía propio. En cualquier emergencia, llame al 911."),
 "Storm Shelters":("Refugios contra tornados","Obras Públicas los abre durante una vigilancia de tornado",None,"Obras Públicas abre tres refugios de la ciudad durante una vigilancia de tornado (Tornado Watch). Cada uno tiene cupo para 90 personas. Están detrás de la biblioteca en 202 Bangor Avenue SE, en el parque C.W. Day en 203 Michelle Street NW y en Steppville en 1407 Commercial Street SE."),
 "Public Works":("Obras Públicas","Gerente de operaciones de la ciudad",None,"Obras Públicas repara las calles, recoge ramas y maleza y arregla las luces de la calle. Para reportar un bache, un árbol caído o una luz apagada, llame a la Alcaldía."),
 "Hanceville Water and Sewer Board":("Junta de Agua y Alcantarillado de Hanceville","Gerente",None,"La junta de agua da el servicio de agua y alcantarillado en el área de Hanceville. Llame aquí para iniciar o cancelar el servicio, reportar una fuga o preguntar por su recibo. También puede pagar en línea."),
 "Parks and Recreation":("Parques y Recreación","Director de parques",None,"Parques y Recreación maneja los cuatro parques de la ciudad, la piscina municipal y los deportes juveniles. Puede reservar y pagar instalaciones de los parques en línea con el sistema de alquiler Jarvis de la ciudad."),
 "Shirley Burden Public Library":("Biblioteca Pública Shirley Burden","Gerente de la biblioteca","Martes a viernes de 8 AM a 5 PM (cerrado de 12 a 1 PM), sábado de 9 AM a 1 PM. Cerrado domingo y lunes.","La biblioteca de la ciudad ofrece libros, horas de cuentos y actividades para todas las edades, además de una pequeña tienda de libros usados que apoya los programas para niños."),
 "Planning Commission":("Comisión de Planificación","Contacto para entrar en la agenda","Se reúne el cuarto lunes de cada mes a las 6 PM en el Centro Cívico.","La Comisión de Planificación se encarga de la zonificación, la división de terrenos y el plan maestro de la ciudad. La ciudad pide que quien quiera estar en la agenda le escriba al alcalde."),
 "Events and Community Development Committee":("Comité de Eventos y Desarrollo Comunitario","Presidenta","Se reúne el primer lunes de cada mes a las 6 PM en la biblioteca.","Este comité asesor ayuda a planear los eventos de la ciudad, a crear lazos con los negocios locales y a recomendar mejoras para la vida en Hanceville. Las reuniones están abiertas al público."),
 "Cullman County Satellite Office":("Oficina satélite del Condado de Cullman","Placas, títulos e impuestos a la propiedad",None,"Una oficina satélite del condado dentro de la Alcaldía tramita placas de auto, títulos, renovaciones de casas móviles e impuestos a la propiedad, así que no tiene que manejar hasta Cullman."),
}
ES_GROUP={'City Hall Offices':'Oficinas de la Alcaldía','Public Safety':'Seguridad pública','Streets, Water and Utilities':'Calles, agua y servicios','Parks, Library and Recreation':'Parques, biblioteca y recreación','Boards and Committees':'Juntas y comités','County Office at City Hall':'Oficina del condado en la Alcaldía'}
ES_CONTACT={"Fire station, non emergency line":"Estación de bomberos","Cullman County Sheriff's Office":"Oficina del Alguacil del Condado de Cullman","Public Works":"Obras Públicas","Cullman County":"Condado de Cullman"}
def es_dep_card(e):
  nm,title,hours,summ=ES_DEP[e['name']];n=E(nm)
  dl=[]
  if e.get('phone'):dl.append(f'<dt>Teléfono</dt><dd><a href="{_tel(e["phone"])}">{E(e["phone"])}</a></dd>')
  if e.get('emergency'):dl.append('<dt>Emergencias</dt><dd><a href="tel:911">911</a></dd>')
  if e.get('email'):dl.append(f'<dt>Correo</dt><dd><a href="mailto:{E(e["email"])}">{E(e["email"])}</a></dd>')
  if e.get('fax'):dl.append(f'<dt>Fax</dt><dd>{E(e["fax"])}</dd>')
  if e.get('address'):dl.append(f'<dt>Dirección</dt><dd>{E(e["address"])}</dd>')
  if hours:dl.append(f'<dt>Horario</dt><dd>{E(hours)}</dd>')
  a=[]
  if e.get('phone'):a.append(f'<a class="btn" href="{_tel(e["phone"])}" aria-label="Llamar a {n}">{I("phone")}Llamar</a>')
  if e.get('email'):a.append(f'<a class="btn alt3" href="mailto:{E(e["email"])}" aria-label="Escribir a {n}">{I("mail")}Correo</a>')
  if e.get('address'):a.append(f'<a class="btn alt2" href="{E(_map(e["address"]))}" target="_blank" rel="noopener noreferrer" aria-label="Cómo llegar a {n}">{I("navigation")}Cómo llegar</a>')
  if e.get('website'):a.append(f'<a class="btn alt3" href="{E(e["website"])}" target="_blank" rel="noopener noreferrer" aria-label="Sitio web de {n} (en inglés)">{I("globe")}Sitio web</a>')
  who=ES_CONTACT.get(e.get('contact'),e.get('contact',''))
  return f'<article class="dep" id="{_slug(e["name"])}"><div class="dep-head"><span class="ini dep-ic">{I(DEP_IC.get(e["name"],"landmark"))}</span><div><h3>{n}</h3><p class="dep-who"><b>{E(who)}</b>{", "+E(title) if title else ""}</p></div></div><dl class="dep-dl">{"".join(dl)}</dl><p class="sum">{E(summ)}</p><div class="acts">{"".join(a)}</div></article>'
def es_page(k,body,crumb,extra=''):
  f=k+'.html';t,d=SEO[k]
  open(f,'w').write(head(t,d,f,crumb_ld(crumb,f,'es')+extra,'es')+f'\n<body data-page="{k}" data-lang="es">\n'+header(f,True,'es')+body+foot('es'))
# ---- es-departamentos ----
secs=''.join(f'<section class="page-sec{" alt-bg" if n%2 else ""}" id="{_slug(g)}"><div class="wrap"><h2>{E(ES_GROUP[g])}</h2><div class="dep-grid">'+''.join(es_dep_card(e) for e in DEPS if e['group']==g)+'</div></div></section>' for n,g in enumerate(DEP_ORDER))
es_page('es-departamentos',f'''
<main id="main">{crumbs(['Servicios','Departamentos y contactos'],'es')}<div class="page-head"><div class="wrap"><h1>Departamentos y contactos de la ciudad</h1><p>Todos los departamentos de la Ciudad de Hanceville en un solo lugar, con la persona a quien preguntar, su cargo y el teléfono, el correo, la dirección y el horario que publica la ciudad. Toque un botón para llamar, escribir o ver cómo llegar.</p></div></div>
<section class="page-sec" style="padding-bottom:0"><div class="wrap">{ES_NOTE_TOP}
<div class="infogrid"><div class="info"><h2>Alcaldía</h2><p>112 Main Street SE</p></div><div class="info"><h2>Teléfono principal</h2><p><a href="tel:2563529830">(256) 352-9830</a></p></div><div class="info"><h2>Fax</h2><p>(256) 352-1200</p></div><div class="info"><h2>Emergencias</h2><p><a href="tel:911">Llame al 911</a></p></div></div>
<p class="note">¿No sabe a quién llamar? Empiece por la Alcaldía al <a href="tel:2563529830">(256) 352-9830</a> y el personal le indicará con quién hablar. Los empleados de la ciudad atienden principalmente en inglés.</p>
</div></section>
{secs}
<section class="page-sec"><div class="wrap"><p class="official-src">Los nombres, cargos, teléfonos, correos, direcciones y horarios vienen de la <a href="https://www.cityofhanceville.net/o/coh/page/city-departments" target="_blank" rel="noopener noreferrer">página de departamentos de la Ciudad de Hanceville</a> (en inglés) y de la página de cada departamento, revisadas el 17 de octubre de 2026. ¿Ve algo desactualizado? Escríbanos a <a href="mailto:{EMAIL}?subject=Correcci%C3%B3n">{EMAIL}</a>.</p><p><a href="departments.html" hreflang="en" lang="en">See this page in English</a></p></div></section>
</main>''','Departamentos y contactos')
# ---- es-concejo ----
ES_CM={
 "Jana Shelton":("Puesto 1, alcaldesa suplente (Mayor Pro Tem)","Elegida en agosto de 2025. Su periodo empezó en noviembre de 2025.","Jana Shelton ocupa el Puesto 1 del Concejo y es Mayor Pro Tem, es decir, sustituye al alcalde cuando él no está. Los votantes la eligieron en agosto de 2025, y el Concejo la nombró Mayor Pro Tem en febrero de 2026, cuando Nolan Bradford pasó a ser alcalde."),
 "Robert Powell":("Puesto 2, concejal","Elegido sin oposición en 2025. Su periodo empezó en noviembre de 2025.","Robert Powell ocupa el Puesto 2. Antes de llegar al Concejo sirvió en la Comisión de Planificación y enseñó gobierno y economía en una escuela de Hanceville. Ha dicho que quiere modernizar los registros de la ciudad y publicar las ordenanzas en línea."),
 "Kim Brown":("Puesto 3, concejal","Reelegida en agosto de 2025 para su quinto periodo.","Kim Brown ocupa el Puesto 3 y cumple su quinto periodo en el Concejo. En febrero de 2026 fue el único voto en contra de disolver el departamento de policía y el tribunal municipal de la ciudad."),
 "Cameron Rowe":("Puesto 4, concejal","Elegido en agosto de 2025. Su periodo empezó en noviembre de 2025.","Cameron Rowe ocupa el Puesto 4. Ganó el puesto en agosto de 2025 y dijo que sus metas eran recuperar la confianza en el Concejo y hacer el pueblo más acogedor. El 8 de octubre de 2026, el Concejo lo nombró a la Comisión de Planificación."),
 "Carla Cain":("Puesto 5, concejal","Nombrada el 12 de marzo de 2026 para terminar el periodo actual.","Carla Whittaker Cain ocupa el Puesto 5. El Concejo la nombró el 12 de marzo de 2026 para llenar el puesto que quedó libre cuando Nolan Bradford llegó a la alcaldía, y juró el cargo esa misma noche."),
}
def es_member(m):
  role,term,summ=ES_CM[m['name']];ph=m['photo']
  return f'<article class="member" id="{_slug(m["name"])}"><picture><source type="image/webp" srcset="img/council/{ph}-600.webp 600w, img/council/{ph}-1200.webp 1200w" sizes="(min-width:1000px) 340px, (min-width:620px) 45vw, 92vw"><img src="img/council/{ph}-600.jpg" width="600" height="400" alt="Retrato oficial de {E(m["name"])}, miembro del Concejo Municipal de Hanceville" loading="lazy" decoding="async"></picture><div class="mb"><span class="place">{E(role.split(",")[0])}</span><h3>{E(m["name"])}</h3><p class="role">{E(role.split(", ",1)[1])}</p><p class="mterm">{E(term)}</p><p class="mbio">{E(summ)}</p><p class="mcontact"><b>Contacto:</b> por medio de la Alcaldía al <a href="tel:2563529830">(256) 352-9830</a>.</p></div></article>'
MESES=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];DIAS=['lunes','martes','miércoles','jueves','viernes','sábado','domingo']
def es_date(d):return f"{DIAS[d.weekday()]} {d.day} de {MESES[d.month-1]}"
def es_cal(ics,g,label):return f'<div class="acts cal-acts"><a class="btn alt3" href="{ics}" download aria-label="Descargar archivo de calendario para {E(label)}">{I("download")} Agregar al calendario (.ics)</a><a class="btn alt3" href="{E(g)}" target="_blank" rel="noopener noreferrer" aria-label="Agregar {E(label)} a Google Calendar">{I("calendar-plus")} Google Calendar</a></div>'
ES_HOL={"Thanksgiving Day":"el Día de Acción de Gracias","Christmas Eve":"Nochebuena","Christmas Day":"Navidad","New Year's Day":"Año Nuevo","Independence Day":"el Día de la Independencia"}
def es_mtg(d):
  hol=_holiday(d);st=("Cae en "+ES_HOL[hol]+". La ciudad suele cambiar las reuniones en días festivos, así que revise el calendario de la ciudad antes de ir.") if hol else ("Confirmada en el calendario de la ciudad." if d.isoformat() in CONFIRMED else "Horario regular. Revise el calendario de la ciudad por si hay cambios.")
  return f'<li><span class="datebadge" aria-hidden="true"><span class="m">{MESES[d.month-1][:3]}</span><span class="d">{d.day}</span></span><div><b>{es_date(d).capitalize()}</b><small>Sesión de trabajo a las 6:00 PM y la reunión regular justo después, en la Alcaldía</small><small>{E(st)}</small>{es_cal(mtg_ics_name(d),council_gcal(d),"la reunión del Concejo del "+es_date(d))}</div></li>'
es_page('es-concejo',f'''
<main id="main">{crumbs(['Alcaldía','Concejo Municipal'],'es')}<div class="page-head"><div class="wrap"><h1>Concejo Municipal de Hanceville</h1><p>Hanceville tiene un alcalde y cinco miembros del Concejo Municipal. Cada uno es elegido por cuatro años, y juntos aprueban las leyes de la ciudad, fijan el presupuesto y deciden el rumbo de Hanceville.</p></div></div>
<section class="page-sec" id="council_members"><div class="wrap">{ES_NOTE_TOP}
<h2>Miembros del Concejo</h2><p class="lede">Cada asiento del Concejo se llama Puesto (Place). Esta es la persona en cada puesto, según la Ciudad de Hanceville.</p>
<div class="member-grid">{''.join(es_member(m) for m in MEM)}</div>
<div class="mayor-card" id="nolan_bradford"><div><h3>Alcalde {E(MAYOR['name'])}</h3><p class="mterm">Nombrado alcalde el 12 de febrero de 2026.</p><p>Nolan Bradford es alcalde desde febrero de 2026, cuando el Concejo lo nombró tras la renuncia del alcalde Paul Campbell. Había sido elegido al Concejo en 2025. En Hanceville el alcalde también vota como miembro del Concejo.</p><p class="mcontact"><b>Oficina del Alcalde:</b> <a href="tel:2563529811">(256) 352-9811</a> &middot; <a href="mailto:mayor@cityofhanceville.net">mayor@cityofhanceville.net</a> &middot; 112 Main Street SE</p></div></div>
</div></section>
<section class="page-sec alt-bg" id="meeting_schedule"><div class="wrap"><h2>Reuniones del Concejo</h2>
<p class="lede">El Concejo se reúne el <b>segundo y cuarto jueves de cada mes</b> en la Alcaldía de Hanceville, 112 Main Street SE. La sesión de trabajo empieza a las 6:00 PM y la reunión regular sigue justo después. Todas las reuniones regulares son abiertas al público y hay tiempo para comentarios. Las reuniones se hacen en inglés.</p>
<ul class="meetings">{''.join(es_mtg(d) for d in MEETINGS)}</ul>
<div class="acts"><a class="btn alt2" href="{CHM}" target="_blank" rel="noopener noreferrer">{I("navigation")}Cómo llegar a la Alcaldía</a><a class="btn alt3" href="https://www.youtube.com/@OfficialCityofHancevilleAL" target="_blank" rel="noopener noreferrer">{I("video")}Ver las reuniones en YouTube (en inglés)</a><a class="btn alt3" href="{AG}" target="_blank" rel="noopener noreferrer">{I("file-text")}Agendas de 2026 (en inglés)</a></div>
</div></section>
<section class="page-sec"><div class="wrap"><p class="official-src">Los nombres, puestos y fotos vienen de la <a href="{COUNCIL_URL}" target="_blank" rel="noopener noreferrer">página oficial del Concejo Municipal</a> (en inglés), revisada el 17 de octubre de 2026. Los perfiles se basan en las páginas de la ciudad y en reportajes de medios locales, citados en la <a href="council.html#council_members" hreflang="en">versión en inglés</a>.</p></div></section>
</main>''','Concejo Municipal')
# ---- es-servicios ----
ES_SVC=[
 ("Pagar el recibo del agua","droplet","La Junta de Agua y Alcantarillado de Hanceville tiene un sistema para pagar el recibo en línea. Para iniciar o cancelar el servicio, reportar una fuga o preguntar por un cobro, llame a la junta.",[("Pagar en línea","https://hancevillewwsb.epayub.com/"),("Llamar (256) 352-9229","tel:2563529229")],"203 Main Street, Hanceville"),
 ("Alcaldía de Hanceville","landmark","La Alcaldía es la oficina principal para trámites de la ciudad. Llame aquí para la Secretaría Municipal, permisos, licencias de negocio, alquiler de instalaciones y preguntas generales.",[("Llamar (256) 352-9830","tel:2563529830"),("Cómo llegar",CHM)],"112 Main Street SE, Hanceville"),
 ("Permisos y licencias de negocio","clipboard-list","Los permisos de construcción, las licencias de negocio y las solicitudes de licencia de bebidas alcohólicas se tramitan en la Alcaldía. Puede descargar los formularios en la página de documentos de la ciudad (en inglés).",[("Formularios de permisos","https://www.cityofhanceville.net/documents/permits/25555107"),("Escribir a Becky Hinkle","mailto:bhinkle@cityofhanceville.net")],None),
 ("Placas, títulos e impuestos a la propiedad","building-2","Una oficina satélite del Condado de Cullman dentro de la Alcaldía tramita placas de auto, títulos, renovaciones de casas móviles e impuestos a la propiedad. También puede renovar la placa en línea.",[("Llamar (256) 352-6036","tel:2563526036"),("Renovar en línea","https://cullmantagrenewals.countygovservices.com/Home/Requirements")],"112 Main Street SE, Hanceville"),
 ("Refugios contra tornados","tornado","Obras Públicas abre tres refugios de la ciudad durante una vigilancia de tornado. Cada uno tiene cupo para 90 personas: detrás de la biblioteca en 202 Bangor Avenue SE, en el parque C.W. Day en 203 Michelle Street NW y en Steppville en 1407 Commercial Street SE.",[("Página de refugios","https://www.cityofhanceville.net/o/coh/page/storm-shelters")],None),
 ("Alertas de la ciudad por texto, llamada o correo","megaphone","Inscríbase en el sitio de la ciudad para recibir avisos oficiales sobre cierres de calles, trabajos en los servicios, refugios y eventos.",[("Inscribirme (en inglés)","https://www.cityofhanceville.net/forms/signup-for-alerts")],None),
 ("Bomberos y Rescate","flame","Los bomberos responden llamadas a toda hora. Use la línea que no es de emergencia para permisos de quema y el programa de detectores de humo. En una emergencia, llame al 911.",[("Línea no de emergencia (256) 352-5544","tel:2563525544"),("Emergencia 911","tel:911")],"119 Collins Avenue, Hanceville"),
 ("Policía y seguridad","shield","Desde febrero de 2026, los alguaciles del Condado de Cullman patrullan Hanceville. Para algo que no es una emergencia, llame a la Oficina del Alguacil.",[("Alguacil (256) 734-0342","tel:2567340342"),("Emergencia 911","tel:911")],None),
 ("Obras Públicas","construction","Obras Públicas repara las calles, recoge ramas y maleza y arregla las luces de la calle.",[("Reportar un problema","es-reportar.html"),("Llamar a la Alcaldía","tel:2563529830")],None),
 ("Parques y piscina","tree-pine","La ciudad tiene cuatro parques, la piscina municipal en el parque C.W. Day y deportes juveniles. Puede reservar instalaciones en línea con el sistema Jarvis de la ciudad.",[("Escribir al director de parques","mailto:parkdirector@cityofhanceville.net"),("Página de parques (en inglés)","https://www.cityofhanceville.net/o/coh/page/parks-recreation")],None),
 ("Biblioteca Pública Shirley Burden","book-open","Libros, horas de cuentos, computadoras y actividades para todas las edades. Abierta de martes a viernes de 8 AM a 5 PM (cerrada de 12 a 1 PM) y el sábado de 9 AM a 1 PM.",[("Llamar (256) 352-0685","tel:2563520685"),("Cómo llegar",_map("201 Commercial Street, Hanceville, AL 35077"))],"201 Commercial Street, Hanceville"),
 ("Centro Cívico","users","El Centro Cívico tiene salas de reuniones, cocina y un auditorio para eventos grandes. Llame a la Alcaldía para precios y fechas disponibles.",[("Llamar (256) 352-9830","tel:2563529830")],"902 Commercial Street, Hanceville"),
 ("Luz y gas","lightbulb","Cullman Electric Cooperative da el servicio de luz en el área, y Cullman Jefferson Gas da el servicio de gas natural. Las dos empresas aceptan pagos en línea.",[("Pagar la luz","https://billing.cullmanec.com/mcp/"),("Pagar el gas","https://www.cjgas.com/pay-bill")],None),
 ("Empleos de la ciudad","users","La ciudad publica sus vacantes en su página de empleos. El 17 de octubre de 2026 no había vacantes publicadas.",[("Página de empleos (en inglés)","https://www.cityofhanceville.net/o/coh/page/job-opportunities")],None),
]
def es_svc(t,ic,s,links,addr):
  a=''.join(f'<a class="btn{" alt3" if n else ""}" href="{E(u)}"'+('' if u.startswith(('tel:','mailto:')) or u.endswith('.html') else ' target="_blank" rel="noopener noreferrer"')+f'>{E(l)}</a>' for n,(l,u) in enumerate(links))
  return f'<article class="dep" id="{_slug(_h.unescape(t).encode("ascii","ignore").decode())}"><div class="dep-head"><span class="ini dep-ic">{I(ic)}</span><div><h3>{E(t)}</h3>{f"<p class=dep-who>{E(addr)}</p>" if addr else ""}</div></div><p class="sum">{E(s)}</p><div class="acts">{a}</div></article>'
es_page('es-servicios',f'''
<main id="main">{crumbs(['Servicios de la ciudad'],'es')}<div class="page-head"><div class="wrap"><h1>Servicios de la Ciudad de Hanceville</h1><p>Lo que más buscan los vecinos de Hanceville: cómo pagar el agua, a quién llamar en la Alcaldía, permisos, placas de auto, parques, la biblioteca y los refugios contra tornados.</p></div></div>
<section class="page-sec"><div class="wrap">{ES_NOTE_TOP}<div class="dep-grid">{''.join(es_svc(*x) for x in ES_SVC)}</div>
<p class="official-src">La información viene de la Ciudad de Hanceville, la Junta de Agua y Alcantarillado y el Condado de Cullman, revisada el 17 de octubre de 2026. Vea la lista completa en la <a href="city.html" hreflang="en">página de servicios en inglés</a>.</p></div></section>
</main>''','Servicios de la ciudad')
# ---- es-reportar ----
es_page('es-reportar',f'''
<main id="main" data-rp-lang="es">{crumbs(['Servicios','Reportar un problema'],'es')}<div class="page-head"><div class="wrap"><h1>Reportar un problema en Hanceville</h1><p>¿Vio un bache, una luz de la calle apagada o una fuga de agua? Elija el problema, diga dónde está y le abrimos un correo para el departamento correcto de la ciudad.</p></div></div>
{report_body(True)}
<section class="page-sec"><div class="wrap">{ES_NOTE_TOP}<p>Los departamentos de la ciudad atienden principalmente en inglés. Si puede, escriba su reporte en inglés o pida ayuda a alguien de confianza.</p></div></section>
</main>''','Reportar un problema')
# ---- es (home) ----
es_page('es',f'''
<main id="main"><div class="page-head city-hero"><div class="wrap"><h1>Hanceville, Alabama en español</h1><p>Una guía sencilla de los servicios de la ciudad de Hanceville: a quién llamar, cómo pagar el agua, cuándo se reúne el Concejo y qué hacer en una emergencia.</p></div></div>
<section class="page-sec"><div class="wrap">{ES_NOTE_TOP}
<nav class="qlinks" aria-label="Enlaces r&aacute;pidos"><ul>
<li><a href="es-departamentos.html">{I("phone")}Departamentos y contactos</a></li>
<li><a href="es-servicios.html">{I("clipboard-list")}Servicios de la ciudad</a></li>
<li><a href="es-concejo.html">{I("landmark")}Concejo Municipal</a></li>
<li><a href="es-reportar.html">{I("wrench")}Reportar un problema</a></li>
<li><a href="https://hancevillewwsb.epayub.com/" target="_blank" rel="noopener noreferrer">{I("droplet")}Pagar el agua</a></li>
<li><a href="map.html" hreflang="en">{I("map")}Mapa (en inglés)</a></li>
</ul></nav></div></section>
<section class="page-sec alt-bg"><div class="wrap"><h2>Teléfonos importantes</h2>
<div class="infogrid"><div class="info"><h3>Emergencias</h3><p><a href="tel:911">911</a></p></div><div class="info"><h3>Alcaldía</h3><p><a href="tel:2563529830">(256) 352-9830</a></p></div><div class="info"><h3>Agua y alcantarillado</h3><p><a href="tel:2563529229">(256) 352-9229</a></p></div><div class="info"><h3>Bomberos, no emergencias</h3><p><a href="tel:2563525544">(256) 352-5544</a></p></div><div class="info"><h3>Alguacil, no emergencias</h3><p><a href="tel:2567340342">(256) 734-0342</a></p></div><div class="info"><h3>Biblioteca</h3><p><a href="tel:2563520685">(256) 352-0685</a></p></div></div>
<p>La Alcaldía está en 112 Main Street SE, Hanceville, AL 35077. <a href="{CHM}" target="_blank" rel="noopener noreferrer">Cómo llegar</a>.</p></div></section>
<section class="page-sec"><div class="wrap"><h2>Próximas reuniones del Concejo</h2><p>El Concejo se reúne el segundo y cuarto jueves de cada mes a las 6:00 PM en la Alcaldía. Las reuniones son abiertas al público.</p><ul class="meetings">{''.join(es_mtg(d) for d in MEETINGS[:2])}</ul><p><a class="btn alt3" href="es-concejo.html">{I("users")} Conozca al Concejo</a></p></div></section>
<section class="page-sec alt-bg"><div class="wrap"><h2>Tiempo severo y tornados</h2><p>Cuando hay una vigilancia de tornado, Obras Públicas abre tres refugios de la ciudad con cupo para 90 personas cada uno. Si hay una alerta activa del Servicio Nacional de Meteorología para el Condado de Cullman, la verá arriba en esta página.</p><p><a class="btn" href="es-servicios.html#refugios_contra_tornados">{I("tornado")} Dónde están los refugios</a></p></div></section>
<section class="page-sec"><div class="wrap"><h2>Más en inglés</h2><p>El resto del sitio está en inglés: <a href="events.html" hreflang="en">eventos y cosas que hacer</a>, <a href="news.html" hreflang="en">noticias locales</a>, <a href="eats.html" hreflang="en">restaurantes</a>, <a href="businesses.html" hreflang="en">negocios</a> y <a href="resources.html" hreflang="en">ayuda estatal y federal</a>.</p></div></section>
</main>''','Inicio')
ES_SEARCH=[(k+'.html',_h.unescape(SEO[k][0]),_h.unescape(SEO[k][1])) for k in ES_SEO]
