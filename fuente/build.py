#!/usr/bin/env python3
"""Monta el sitio estático: une cada fragmento de src/ con la plantilla común."""
import hashlib
import re
from pathlib import Path

RAIZ = Path(__file__).parent
SRC = RAIZ / "src"
SITIO = RAIZ.parent

PAGINAS = [
    # archivo, etiqueta corta del menú, título del menú, <title>, descripción
    ("index.html", "Inicio", "Contexto y objetivos", "ISR e IBEX ESG",
     "Trabajo sobre las Inversiones Socialmente Responsables y el índice IBEX ESG."),
    ("parte-1-isr.html", "Parte 1", "Marco teórico de las ISR", "Parte 1: Marco teórico de las ISR",
     "Definición, evolución, estrategias y criterios ESG de la inversión socialmente responsable."),
    ("parte-2-ibex-esg.html", "Parte 2", "Qué es el índice IBEX ESG", "Parte 2: Qué es el índice IBEX ESG",
     "Características, requisitos de inclusión y comparación del IBEX ESG con otros índices sostenibles."),
    ("parte-3-inditex.html", "Parte 3", "Análisis de empresa: Inditex", "Parte 3: Análisis de Inditex",
     "Sector, iniciativas ESG, reconocimientos y reporting de sostenibilidad de Inditex."),
    ("parte-4-reflexion.html", "Parte 4", "Reflexión crítica", "Parte 4: Reflexión crítica",
     "Ventajas y limitaciones del IBEX ESG y futuro de las ISR en España."),
    ("referencias.html", "Fuentes", "Referencias y webs", "Referencias y webs",
     "Fuentes consultadas para el trabajo sobre ISR e IBEX ESG."),
]

EQUIPO = "Marcos Ramos, Gonzalo Redondo, Jaime Ramos y Victor Cerveros"

# Ilustraciones de trazo dibujadas para este trabajo
ILUS = {
    "euro": ('0 0 48 48', '<circle cx="24" cy="24" r="19" fill="none" stroke="currentColor" stroke-width="3.5"/><text x="24" y="32" text-anchor="middle" font-size="23" font-weight="800" font-family="Arial, sans-serif" fill="currentColor">€</text>'),
    "euromundo": ('0 0 96 48', '<circle cx="20" cy="24" r="15" fill="none" stroke="currentColor" stroke-width="3"/><text x="20" y="31" text-anchor="middle" font-size="19" font-weight="800" font-family="Arial, sans-serif" fill="currentColor">€</text><path d="M43 24h10M48 19v10" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><g fill="none" stroke="currentColor" stroke-width="3"><circle cx="76" cy="24" r="15"/><ellipse cx="76" cy="24" rx="6.5" ry="15"/><path d="M61 24h30"/></g>'),
    "barras": ('0 0 48 48', '<g fill="currentColor"><rect x="7" y="27" width="9" height="15"/><rect x="20" y="17" width="9" height="25"/><rect x="33" y="6" width="9" height="36"/></g>'),
    "zigzag": ('0 0 64 48', '<polyline points="4,36 18,18 28,30 42,10 60,26" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'),
    "zigzagtermo": ('0 0 96 48', '<polyline points="4,36 16,20 26,30 38,12 52,26" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M74 6v24" stroke="currentColor" stroke-width="7" stroke-linecap="round"/><circle cx="74" cy="36" r="8" fill="currentColor"/>'),
    "ojo": ('0 0 64 48', '<path d="M4 24c8-12 18-17 28-17s20 5 28 17c-8 12-18 17-28 17S12 36 4 24z" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linejoin="round"/><circle cx="32" cy="24" r="8" fill="currentColor"/>'),
    "bocadillo": ('0 0 64 48', '<path d="M8 4h48a4 4 0 0 1 4 4v24a4 4 0 0 1-4 4H30L18 46V36H8a4 4 0 0 1-4-4V8a4 4 0 0 1 4-4z" fill="currentColor"/><path d="M20 20l8 8 16-17" fill="none" stroke="#f08c3a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'),
    "noarmas": ('0 0 64 64', '<path d="M14 24h34v8H36l-2 4h-6l-3 12h-9l4-16h-6z" fill="#2f3c8f"/><circle cx="32" cy="32" r="27" fill="none" stroke="#f08c3a" stroke-width="6"/><path d="M13 13l38 38" stroke="#f08c3a" stroke-width="6"/>'),
    "notabaco": ('0 0 64 64', '<rect x="12" y="34" width="32" height="7" fill="#2f3c8f"/><rect x="46" y="34" width="6" height="7" fill="#2f3c8f"/><path d="M28 28c-3-4 3-6 0-10M35 28c-3-4 3-6 0-10" fill="none" stroke="#2f3c8f" stroke-width="2.5" stroke-linecap="round"/><circle cx="32" cy="32" r="27" fill="none" stroke="#f08c3a" stroke-width="6"/><path d="M13 13l38 38" stroke="#f08c3a" stroke-width="6"/>'),
    "sol": ('0 0 48 48', '<circle cx="24" cy="24" r="8" fill="currentColor"/><g stroke="currentColor" stroke-width="3.5" stroke-linecap="round"><path d="M24 4v6M24 38v6M4 24h6M38 24h6M10 10l4 4M34 34l4 4M38 10l-4 4M14 34l-4 4"/></g>'),
    "gota": ('0 0 48 48', '<path d="M24 4c8 10 13 17 13 24a13 13 0 0 1-26 0c0-7 5-14 13-24z" fill="currentColor"/>'),
    "cruz": ('0 0 48 48', '<path d="M18 6h12v12h12v12H30v12H18V30H6V18h12z" fill="currentColor"/>'),
    "hoja": ('0 0 48 48', '<path d="M8 40C8 20 20 8 42 6c-2 22-14 34-34 34z" fill="currentColor"/><path d="M8 40L30 18" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>'),
    "termometro": ('0 0 48 48', '<path d="M24 6v22" stroke="currentColor" stroke-width="8" stroke-linecap="round"/><circle cx="24" cy="35" r="9" fill="currentColor"/><circle cx="24" cy="35" r="4" fill="#f08c3a"/><path d="M34 10h6M34 18h6M34 26h6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>'),
    "ciclo": ('0 0 48 48', '<g fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 22a16 16 0 0 1 28-8"/><path d="M40 26a16 16 0 0 1-28 8"/></g><path d="M38 6v10H28z" fill="#f08c3a"/><path d="M10 42V32h10z" fill="#f08c3a"/>'),
    "hojados": ('0 0 48 48', '<path d="M8 40C8 20 20 8 42 6c-2 22-14 34-34 34z" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linejoin="round"/><path d="M8 40L28 20" stroke="currentColor" stroke-width="3.5" stroke-linecap="round"/><circle cx="34" cy="14" r="3.5" fill="#f08c3a"/>'),
    "escudo": ('0 0 48 48', '<path d="M24 4l16 6v12c0 10-6 18-16 22C14 40 8 32 8 22V10z" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linejoin="round"/><path d="M16 23l6 6 11-12" fill="none" stroke="#f08c3a" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'),
    "maletin": ('0 0 48 48', '<rect x="5" y="15" width="38" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="3.5"/><path d="M17 15v-5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v5" fill="none" stroke="currentColor" stroke-width="3.5"/><path d="M5 26h38" stroke="currentColor" stroke-width="3"/><rect x="20" y="23" width="8" height="6" rx="1" fill="#f08c3a"/>'),
    "personas": ('0 0 56 48', '<g fill="currentColor"><circle cx="12" cy="16" r="6"/><path d="M2 40a10 10 0 0 1 20 0z"/><circle cx="44" cy="16" r="6"/><path d="M34 40a10 10 0 0 1 20 0z"/></g><circle cx="28" cy="12" r="7" fill="#f08c3a"/><path d="M16 42a12 12 0 0 1 24 0z" fill="#f08c3a"/>'),
    "organigrama": ('0 0 56 48', '<rect x="20" y="4" width="16" height="11" rx="2" fill="#f08c3a"/><path d="M28 15v9M9 32v-8h38v8M28 24v8" fill="none" stroke="currentColor" stroke-width="3"/><g fill="currentColor"><rect x="2" y="32" width="14" height="11" rx="2"/><rect x="21" y="32" width="14" height="11" rx="2"/><rect x="40" y="32" width="14" height="11" rx="2"/></g>'),
    "ojonaranja": ('0 0 64 48', '<path d="M4 24c8-12 18-17 28-17s20 5 28 17c-8 12-18 17-28 17S12 36 4 24z" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/><circle cx="32" cy="24" r="9" fill="#f08c3a"/><circle cx="32" cy="24" r="3.5" fill="currentColor"/>'),
    "balanza": ('0 0 56 48', '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M28 6v34M20 42h16M8 12h40M12 12L6 26M12 12l6 14M44 12l-6 14M44 12l6 14"/></g><path d="M5 26h14a7 7 0 0 1-14 0zM37 26h14a7 7 0 0 1-14 0z" fill="#f08c3a"/>'),
}


def ilu(nombre: str) -> str:
    caja, cuerpo = ILUS[nombre]
    return f'<svg class="ilu" viewBox="{caja}" aria-hidden="true">{cuerpo}</svg>'


# Fotografías. Las propias van en assets/fotos; las de Unsplash se sirven desde su servidor.
# clave: (origen, archivo o identificador, autor, página de la foto, texto alternativo, dónde se usa)
UNSPLASH = "https://images.unsplash.com/"
FOTOS = {
    "pantallas": ("unsplash", "photo-1767424412548-1a1ac7f4b9bc", "Jakub Żerdzicki",
                  "https://unsplash.com/photos/trading-charts-displayed-on-multiple-screens-and-tablet-vKNRKjSNbTo",
                  "Gráficos de cotización en varias pantallas y una tableta.", "Inicio, contextualización"),
    "monedas": ("unsplash", "photo-1579621970563-ebec7560ff3e", "Micheile Henderson",
                "https://unsplash.com/photos/green-plant-on-brown-round-coins-lZ_4nPFKcV8",
                "Una planta pequeña que crece sobre un montón de monedas.", "Parte 1, cabecera"),
    "aerogeneradores": ("unsplash", "photo-1553897597-1cdcec3d8b29", "Har",
                        "https://unsplash.com/photos/three-white-wind-turbines-on-green-field-91fBfc7B4GE",
                        "Tres aerogeneradores blancos en un campo verde.", "Parte 1, cambio climático"),
    "troncos": ("propia", "troncos", "", "", "Troncos de madera apilados tras una tala.", "Parte 1, gestión de recursos"),
    "puerto": ("propia", "puerto", "", "", "Barcas de pesca amarradas en un puerto con el agua cubierta de plásticos.", "Parte 1, biodiversidad"),
    "costura": ("unsplash", "photo-1746395592054-dc3aed101f72", "Wiktoria Skrzekotowska",
                "https://unsplash.com/photos/people-are-sewing-clothes-with-sewing-machines-6Zh87jbMSEA",
                "Manos cosiendo prendas con máquinas de coser en un taller.", "Parte 1, derechos humanos"),
    "condiciones": ("propia", "condiciones", "", "", "Una persona con traje sostiene una tarjeta con el texto «Terms and conditions».", "Parte 1, condiciones laborales"),
    "imanes": ("propia", "imanes", "", "", "Puerta de un frigorífico cubierta de imanes de recuerdo de muchos países.", "Parte 1, diversidad"),
    "consejo": ("unsplash", "photo-1431540015161-0bf868a2d407", "Benjamin Child",
                "https://unsplash.com/photos/oval-brown-wooden-conference-table-and-chairs-inside-conference-room-GWe0dlVD9e0",
                "Sala de juntas vacía con una mesa ovalada de madera y sillas alrededor.", "Parte 1, estructura directiva"),
    "lupa": ("unsplash", "photo-1609877992115-8cd060c2e9e4", "Teslariu Mihai",
             "https://unsplash.com/photos/black-magnifying-glass-on-white-printer-paper-O7LDeH0Qo_0",
             "Una lupa negra apoyada sobre hojas de papel.", "Parte 1, transparencia"),
    "balanza": ("unsplash", "photo-1587740896339-96a76170508d", "Elena Mozhvilo",
                "https://unsplash.com/photos/j06gLuKK0GM",
                "Una pequeña balanza dorada sobre una superficie de madera.", "Parte 1, ética empresarial"),
    "bolsa": ("unsplash", "photo-1639133037499-31d957fad7fd", "L’Odyssée Belle",
              "https://unsplash.com/photos/a-black-and-white-photo-of-a-building-with-columns-m1vk1Rn0my8",
              "Fachada con columnas de la Bolsa de Madrid, en blanco y negro.", "Parte 2, cabecera"),
    "ropa": ("unsplash", "photo-1632194978058-4f2f48bc68c2", "Greg Rosenke",
             "https://unsplash.com/photos/a-rack-of-shirts-hanging-on-a-rack-in-a-store-hWdzH8YY8kk",
             "Camisetas de colores colgadas en el perchero de una tienda.", "Parte 3, cabecera"),
    "reunion": ("unsplash", "photo-1573166364839-1bfe9196c23e", "Christina (wocintechchat.com)",
                "https://unsplash.com/photos/people-having-meeting-on-rectangular-brown-table-ftCWdZOFZqo",
                "Varias personas reunidas alrededor de una mesa de trabajo.", "Parte 4, cabecera"),
}


def _fuentes(clave: str, anchos: tuple, alto_por_ancho: float) -> tuple:
    """Devuelve (src, srcset) para una foto a varios anchos."""
    origen, ident = FOTOS[clave][0], FOTOS[clave][1]
    if origen == "propia":
        urls = [(f"assets/fotos/{ident}-{a}.webp", a) for a in anchos]
    else:
        urls = [(f"{UNSPLASH}{ident}?auto=format&amp;fit=crop&amp;w={a}&amp;h={round(a * alto_por_ancho)}&amp;q=70", a) for a in anchos]
    return urls[-1][0], ", ".join(f"{u} {a}w" for u, a in urls)


def foto_tarjeta(clave: str) -> str:
    """Foto de la parte alta de una tarjeta de factor (formato 2:1)."""
    src, srcset = _fuentes(clave, (480, 960), 1 / 2)
    alt = FOTOS[clave][4]
    return (f'<div class="factor__marco"><img class="factor__foto" data-foto src="{src}" srcset="{srcset}" '
            f'sizes="(max-width: 56rem) 92vw, 20rem" width="960" height="480" alt="{alt}" loading="lazy" decoding="async"></div>')


def foto_banda(clave: str, pie: str) -> str:
    """Foto ancha con pie a mano y crédito (formato 2:1)."""
    src, srcset = _fuentes(clave, (800, 1600), 1 / 2)
    _, _, autor, pagina, alt, _ = FOTOS[clave]
    return (f'<figure class="foto-banda"><img data-foto src="{src}" srcset="{srcset}" '
            f'sizes="(max-width: 50rem) 92vw, 46rem" width="1600" height="800" alt="{alt}" decoding="async">'
            f'<figcaption><span class="foto-banda__pie">{pie}</span>'
            f'<span class="foto-banda__credito">Foto: <a href="{pagina}">{autor}</a>, Unsplash</span></figcaption></figure>')


def creditos() -> str:
    """Lista de créditos de las fotos de Unsplash para la página de referencias."""
    filas = []
    for origen, _, autor, pagina, alt, donde in FOTOS.values():
        if origen == "unsplash":
            filas.append(f'    <li>{autor}. <a href="{pagina}">{alt.rstrip(".")}</a>. Unsplash.<em>{donde}.</em></li>')
    return '<ul class="refs">\n' + "\n".join(filas) + "\n  </ul>"


PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Caveat:wght@500..700&family=Open+Sans:ital,wght@0,400..800;1,400&family=Playfair+Display:ital,wght@0,500..700;1,600&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@500..700&family=Open+Sans:ital,wght@0,400..800;1,400&family=Playfair+Display:ital,wght@0,500..700;1,600&display=swap"></noscript>
<link rel="stylesheet" href="assets/estilos.css?v={v}">
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<header class="rail" data-abierto="false">
  <a class="rail__titulo" href="index.html">ISR e IBEX ESG<span>Cómo mide la Bolsa española la sostenibilidad de sus empresas</span></a>
  <button class="menu-boton" type="button" aria-expanded="false" aria-controls="menu">Menú</button>
  <nav id="menu" aria-label="Secciones del trabajo">
    <ul>
{menu}
    </ul>
  </nav>
  <p class="rail__pie"><strong>Equipo</strong><br>{equipo}<br><br>Sostenibilidad, UD1, Actividad 1<br>Datos consultados en octubre de 2026</p>
</header>
<div class="pagina">
<main class="contenido" id="contenido">
{cuerpo}
{siguiente}
<p class="pie">Trabajo de clase elaborado por {equipo}. Las cifras llevan su fecha y su fuente; la lista completa está en <a href="referencias.html">Referencias y webs</a>.</p>
</main>
</div>
<script src="assets/sitio.js?v={v}" defer></script>
</body>
</html>
"""


# Nombres breves para el menú horizontal de escritorio
BREVES = {
    "index.html": "Contexto",
    "parte-1-isr.html": "Marco teórico",
    "parte-2-ibex-esg.html": "Índice IBEX ESG",
    "parte-3-inditex.html": "Inditex",
    "parte-4-reflexion.html": "Reflexión crítica",
    "referencias.html": "Referencias",
}


def menu(actual: str) -> str:
    filas = []
    for archivo, corta, larga, _, _ in PAGINAS:
        marca = ' aria-current="page"' if archivo == actual else ""
        filas.append(f'      <li><a href="{archivo}"{marca}><small>{corta}</small><span class="largo">{larga}</span><span class="breve" aria-hidden="true">{BREVES[archivo]}</span></a></li>')
    return "\n".join(filas)


def siguiente(i: int) -> str:
    partes = []
    if i > 0:
        a = PAGINAS[i - 1]
        partes.append(f'<a href="{a[0]}"><small>Anterior</small>{a[1]}: {a[2]}</a>')
    if i < len(PAGINAS) - 1:
        s = PAGINAS[i + 1]
        partes.append(f'<a class="der" href="{s[0]}"><small>Siguiente</small>{s[1]}: {s[2]}</a>')
    return '<nav class="siguiente" aria-label="Página anterior y siguiente">' + "".join(partes) + "</nav>"


def version() -> str:
    """Huella corta del contenido de estilos y guion."""
    h = hashlib.sha1()
    for nombre in ("estilos.css", "sitio.js"):
        h.update((SITIO / "assets" / nombre).read_bytes())
    return h.hexdigest()[:8]


def main() -> None:
    v = version()
    for i, (archivo, _, _, titulo, descripcion) in enumerate(PAGINAS):
        cuerpo = (SRC / archivo).read_text(encoding="utf-8")
        # ilustraciones: {{ilu:nombre}}
        cuerpo = re.sub(r"\{\{ilu:([a-z]+)\}\}", lambda m: ilu(m.group(1)), cuerpo)
        # fotos: {{foto:clave}} en tarjetas, {{banda:clave|pie}} a lo ancho y {{creditos}}
        cuerpo = re.sub(r"\{\{foto:([a-z]+)\}\}", lambda m: foto_tarjeta(m.group(1)), cuerpo)
        cuerpo = re.sub(r"\{\{banda:([a-z]+)\|([^}]+)\}\}", lambda m: foto_banda(m.group(1), m.group(2)), cuerpo)
        cuerpo = cuerpo.replace("{{creditos}}", creditos())
        # espacio de no separación entre la cifra y el signo de porcentaje
        cuerpo = re.sub(r"(\d) %", r"\1&nbsp;%", cuerpo)
        titulo_completo = titulo if archivo == "index.html" else f"{titulo} | ISR e IBEX ESG"
        html = PLANTILLA.format(
            titulo=titulo_completo,
            descripcion=descripcion,
            menu=menu(archivo),
            equipo=EQUIPO,
            cuerpo=cuerpo,
            siguiente=siguiente(i),
            v=v,
        )
        (SITIO / archivo).write_text(html, encoding="utf-8")
        print("ok", archivo, len(html))
    (SITIO / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()
