#!/usr/bin/env python3
"""Monta el sitio estático: une cada fragmento de src/ con la plantilla común."""
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

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,700;1,400&family=Bricolage+Grotesque:opsz,wght@12..96,500..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/estilos.css">
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
<script src="assets/sitio.js"></script>
</body>
</html>
"""


def menu(actual: str) -> str:
    filas = []
    for archivo, corta, larga, _, _ in PAGINAS:
        marca = ' aria-current="page"' if archivo == actual else ""
        filas.append(f'      <li><a href="{archivo}"{marca}><small>{corta}</small>{larga}</a></li>')
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


def main() -> None:
    for i, (archivo, _, _, titulo, descripcion) in enumerate(PAGINAS):
        cuerpo = (SRC / archivo).read_text(encoding="utf-8")
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
        )
        (SITIO / archivo).write_text(html, encoding="utf-8")
        print("ok", archivo, len(html))
    (SITIO / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()
