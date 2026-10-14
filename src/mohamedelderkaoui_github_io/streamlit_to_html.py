
# streamlit_to_html.py
# Convierte una aplicación Streamlit en un portafolio HTML/CSS/JavaScript
# para publicar en GitHub Pages: MohamedElderkaoui.github.io
#
# Instalación:
#   uv init --python 3.11
#   uv add streamlit beautifulsoup4
#
# Ejecución:
#   uv run python streamlit_to_html.py --source streamlit_app.py
#
# Salida:
#   dist/index.html
#
# IMPORTANTE:
# GitHub Pages solo publica archivos estáticos. Este script exporta la
# estructura y el contenido visible de Streamlit a HTML; no convierte
# automáticamente la ejecución Python, los modelos YOLO ni las funciones
# interactivas de Streamlit en JavaScript funcional.

from __future__ import annotations

import argparse
import ast
import html
import json
import logging
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


LOG = logging.getLogger("streamlit_to_html")

DEFAULT_TITLE = "Mohamed Merzouk Bendoukha"
DEFAULT_SUBTITLE = (
    "Desarrollo de aplicaciones web · Inteligencia artificial · Ciberseguridad"
)
DEFAULT_GITHUB = "https://github.com/MohamedElderkaoui"
DEFAULT_REPOSITORY = "https://github.com/MohamedElderkaoui/MohamedElderkaoui.github.io"

NAVY = "#13243A"
TEAL = "#1E7A83"
INK = "#202B36"
MUTED = "#596675"
LIGHT = "#F3F6F9"
WHITE = "#FFFFFF"


@dataclass
class PortfolioData:
    title: str = DEFAULT_TITLE
    subtitle: str = DEFAULT_SUBTITLE
    location: str = "Ejea de los Caballeros, Zaragoza, España"
    email: str = "mderkaoui10@gmail.com"
    github: str = DEFAULT_GITHUB
    linkedin: str = (
        "https://www.linkedin.com/in/"
        "mohamed-merzouk-bendoukh-ejea-aragon"
    )
    website: str = "https://MohamedElderkaoui.github.io"
    summary: str = (
        "Técnico Superior en Desarrollo de Aplicaciones Web con formación "
        "complementaria en inteligencia artificial avanzada, programación "
        "en Python y ciberseguridad defensiva. Interesado en crear "
        "soluciones web, integrar herramientas de IA y mejorar la "
        "accesibilidad digital."
    )
    skills: list[str] = field(default_factory=lambda: [
        "Python",
        "JavaScript",
        "HTML5",
        "CSS3",
        "Bootstrap",
        "SQL",
        "Git",
        "GitHub",
        "YOLO",
        "OpenCV",
        "PyTorch",
        "Streamlit",
        "pandas",
        "NumPy",
        "Machine Learning",
        "Blue Team",
        "Splunk",
        "Sigma Rules",
        "Nessus",
        "Análisis forense digital",
        "Respuesta a incidentes",
    ])
    projects: list[dict[str, Any]] = field(default_factory=lambda: [
        {
            "name": "AccessAI",
            "category": "Inteligencia artificial",
            "description": (
                "Prototipo de visión artificial para detectar elementos "
                "urbanos relacionados con la accesibilidad en imágenes "
                "y vídeos."
            ),
            "technologies": [
                "Python", "YOLO", "OpenCV", "PyTorch", "Streamlit"
            ],
            "url": DEFAULT_GITHUB,
        },
        {
            "name": "Desarrollo web",
            "category": "Desarrollo web",
            "description": (
                "Mantenimiento, actualización, pruebas de usabilidad "
                "y revisión de rendimiento de aplicaciones web."
            ),
            "technologies": [
                "HTML5", "CSS3", "JavaScript", "Python", "SQL"
            ],
            "url": DEFAULT_GITHUB,
        },
        {
            "name": "Ciberseguridad defensiva",
            "category": "Ciberseguridad",
            "description": (
                "Formación en Blue Team, análisis forense digital, "
                "monitorización y respuesta a incidentes."
            ),
            "technologies": [
                "Blue Team", "Splunk", "Sigma", "Nessus"
            ],
            "url": DEFAULT_GITHUB,
        },
    ])
    education: list[dict[str, str]] = field(default_factory=lambda: [
        {
            "date": "2025–2026",
            "title": "Diploma de Extensión Universitaria en IA Avanzada",
            "institution": (
                "Samsung Innovation Campus · Universidad de Málaga · "
                "Fundación ONCE"
            ),
        },
        {
            "date": "2025–2026",
            "title": "Microcredencial Universitaria: Python para IA",
            "institution": (
                "Universidad de Málaga · Samsung Innovation Campus · "
                "Fundación ONCE"
            ),
        },
        {
            "date": "2019–2024",
            "title": "Técnico Superior en Desarrollo de Aplicaciones Web",
            "institution": "CPIFP Los Enlaces / IES Río Arba",
        },
        {
            "date": "2015–2019",
            "title": "Bachillerato Científico-Tecnológico",
            "institution": "IES Cinco Villas",
        },
    ])
    experience: list[dict[str, Any]] = field(default_factory=lambda: [
        {
            "date": "2024",
            "title": "Técnico de Desarrollo de Aplicaciones Web",
            "company": "FTC DAM Servicios Informáticos · Tauste",
            "type": "Prácticas no laborales",
            "tasks": [
                "Mantenimiento y actualización de páginas web.",
                "Pruebas funcionales y revisión de usabilidad.",
                "Actualización de plugins y desarrollo web a medida.",
                "Revisión de seguridad, rendimiento y velocidad de carga.",
                "Detección y comunicación de posibles vulnerabilidades.",
            ],
        },
    ])
    courses: list[dict[str, str]] = field(default_factory=lambda: [
        {
            "title": "Experto en Blue Team — 250 horas",
            "date": "2025",
            "institution": "Inserta · INCIBE · Arelance",
        },
        {
            "title": "Digital Forensic and Incident Response — 300 horas",
            "date": "2025",
            "institution": "Inserta · INCIBE · Arelance",
        },
        {
            "title": "Junior Cybersecurity Analyst Career Path",
            "date": "2025",
            "institution": "Insignia de formación",
        },
    ])


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def safe_url(value: str) -> str:
    value = value.strip()
    if value.startswith(("https://", "http://", "mailto:")):
        return value
    return "#"


def read_streamlit_source(source: Path) -> dict[str, Any]:
    """Extrae llamadas simples a st.title, st.header y st.write del código."""
    result: dict[str, Any] = {
        "titles": [],
        "headers": [],
        "subheaders": [],
        "texts": [],
        "warnings": [],
    }

    if not source.is_file():
        result["warnings"].append(
            f"No se encontró el archivo de origen: {source}"
        )
        return result

    try:
        code = source.read_text(encoding="utf-8-sig")
        tree = ast.parse(code, filename=str(source))
    except (OSError, SyntaxError, UnicodeError) as exc:
        result["warnings"].append(
            f"No se pudo analizar el archivo Python: {exc}"
        )
        return result

    streamlit_functions = {
        "title": "titles",
        "header": "headers",
        "subheader": "subheaders",
        "write": "texts",
        "markdown": "texts",
        "caption": "texts",
    }

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        function = node.func
        if not isinstance(function, ast.Attribute):
            continue

        owner = function.value
        if not (
            isinstance(owner, ast.Name)
            and owner.id in {"st", "streamlit"}
        ):
            continue

        destination = streamlit_functions.get(function.attr)
        if not destination or not node.args:
            continue

        try:
            value = ast.literal_eval(node.args[0])
        except (ValueError, TypeError):
            continue

        if isinstance(value, (str, int, float)):
            result[destination].append(str(value))

    return result


def render_tags(tags: list[str]) -> str:
    return "".join(
        f'<span class="tag">{esc(tag)}</span>'
        for tag in tags
    )


def render_projects(data: PortfolioData) -> str:
    cards = []

    for project in data.projects:
        technologies = render_tags(project.get("technologies", []))
        url = safe_url(project.get("url", data.github))

        cards.append(f"""
        <article class="project-card reveal"
                 data-category="{esc(project.get('category', 'Otros'))}">
            <div class="project-top">
                <span class="project-mark" aria-hidden="true">✦</span>
                <span class="project-category">
                    {esc(project.get('category', 'Proyecto'))}
                </span>
            </div>
            <h3>{esc(project.get('name', 'Proyecto'))}</h3>
            <p>{esc(project.get('description', ''))}</p>
            <div class="tags">{technologies}</div>
            <a class="text-link"
               href="{esc(url)}"
               target="_blank"
               rel="noopener noreferrer">
                Ver proyecto <span aria-hidden="true">↗</span>
            </a>
        </article>
        """)

    return "\n".join(cards)


def render_education(data: PortfolioData) -> str:
    entries = []

    for item in data.education:
        entries.append(f"""
        <article class="timeline-item reveal">
            <span class="timeline-date">{esc(item.get('date', ''))}</span>
            <div>
                <h3>{esc(item.get('title', ''))}</h3>
                <p>{esc(item.get('institution', ''))}</p>
            </div>
        </article>
        """)

    return "\n".join(entries)


def render_experience(data: PortfolioData) -> str:
    entries = []

    for item in data.experience:
        tasks = "".join(
            f"<li>{esc(task)}</li>"
            for task in item.get("tasks", [])
        )
        entries.append(f"""
        <article class="experience-card reveal">
            <span class="timeline-date">{esc(item.get('date', ''))}</span>
            <h3>{esc(item.get('title', ''))}</h3>
            <p class="muted">{esc(item.get('company', ''))}</p>
            <p class="experience-type">{esc(item.get('type', ''))}</p>
            <ul>{tasks}</ul>
        </article>
        """)

    return "\n".join(entries)


def render_courses(data: PortfolioData) -> str:
    entries = []

    for item in data.courses:
        entries.append(f"""
        <article class="course-card reveal">
            <span class="course-year">{esc(item.get('date', ''))}</span>
            <h3>{esc(item.get('title', ''))}</h3>
            <p>{esc(item.get('institution', ''))}</p>
        </article>
        """)

    return "\n".join(entries)


def render_streamlit_summary(source_data: dict[str, Any]) -> str:
    """Muestra un aviso y los textos estáticos recuperados del archivo .py."""
    if not any(source_data.get(key) for key in ("titles", "headers", "subheaders", "texts")):
        return ""

    blocks = []

    for key, label in (
        ("titles", "Títulos encontrados en Streamlit"),
        ("headers", "Encabezados"),
        ("subheaders", "Subencabezados"),
        ("texts", "Textos estáticos"),
    ):
        values = source_data.get(key, [])
        if values:
            items = "".join(f"<li>{esc(value)}</li>" for value in values[:20])
            blocks.append(f"<h4>{esc(label)}</h4><ul>{items}</ul>")

    return f"""
    <section class="source-summary">
        <h3>Contenido estático detectado en la aplicación</h3>
        <p>
            Estos textos se han leído del código fuente.
            No representan una ejecución de Streamlit.
        </p>
        {''.join(blocks)}
    </section>
    """


def build_html(data: PortfolioData, source_data: dict[str, Any]) -> str:
    projects = render_projects(data)
    education = render_education(data)
    experience = render_experience(data)
    courses = render_courses(data)
    skills = render_tags(data.skills)
    streamlit_summary = render_streamlit_summary(source_data)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description"
          content="{esc(data.title)} — Portafolio de desarrollo web, IA y ciberseguridad.">
    <meta name="theme-color" content="{NAVY}">
    <title>{esc(data.title)} | Portfolio</title>
    <link rel="canonical" href="{esc(data.website)}">
    <style>
        :root {{
            --navy: {NAVY};
            --teal: {TEAL};
            --ink: {INK};
            --muted: {MUTED};
            --light: {LIGHT};
            --white: {WHITE};
            --radius: 18px;
            --shadow: 0 14px 40px rgba(19,36,58,.08);
            --max-width: 1120px;
        }}
        * {{ box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; scroll-padding-top: 90px; }}
        body {{
            margin: 0;
            color: var(--ink);
            background: var(--white);
            font-family: Inter, "Segoe UI", Arial, sans-serif;
            line-height: 1.65;
        }}
        a {{ color: inherit; }}
        a:focus-visible, button:focus-visible {{
            outline: 3px solid var(--teal);
            outline-offset: 4px;
        }}
        .container {{ width: min(var(--max-width), 90%); margin: 0 auto; }}
        .skip-link {{
            position: absolute; left: -9999px; top: 0;
            background: white; color: var(--navy); padding: 12px;
        }}
        .skip-link:focus {{ left: 12px; z-index: 1000; }}
        .navbar {{
            position: sticky; top: 0; z-index: 100;
            background: rgba(255,255,255,.92);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid #e6ebef;
        }}
        .nav-inner {{
            min-height: 72px; display: flex; align-items: center;
            justify-content: space-between; gap: 24px;
        }}
        .brand {{
            color: var(--navy); font-weight: 850;
            text-decoration: none; letter-spacing: -.04em;
        }}
        .nav-links {{
            display: flex; align-items: center; gap: 22px;
            flex-wrap: wrap;
        }}
        .nav-links a {{
            font-size: .9rem; font-weight: 650;
            text-decoration: none; color: var(--muted);
        }}
        .nav-links a:hover, .text-link:hover {{ color: var(--teal); }}
        .hero {{
            overflow: hidden; position: relative;
            padding: clamp(80px, 12vw, 145px) 0 105px;
            color: white;
            background:
                radial-gradient(ellipse at 80% 20%, rgba(30,122,131,.38), transparent 38%),
                linear-gradient(135deg, #13243a, #203c55 65%, #1e7a83);
        }}
        .hero::before {{
            content: ""; position: absolute; width: 360px; height: 360px;
            right: -120px; bottom: -200px; border: 1px solid rgba(255,255,255,.15);
            border-radius: 50%; box-shadow: 0 0 0 45px rgba(255,255,255,.025),
            0 0 0 90px rgba(255,255,255,.025);
        }}
        .hero-content {{ position: relative; z-index: 1; max-width: 850px; }}
        .eyebrow {{
            display: inline-flex; align-items: center; gap: 10px;
            color: #bce7e5; font-size: .82rem; font-weight: 800;
            letter-spacing: .12em; text-transform: uppercase;
        }}
        .eyebrow::before {{
            content: ""; width: 25px; height: 2px; background: #77cfca;
        }}
        h1 {{
            max-width: 900px; margin: 22px 0;
            font-size: clamp(2.6rem, 7vw, 5.7rem);
            letter-spacing: -.065em; line-height: 1.03;
        }}
        .hero p {{
            max-width: 760px; color: #e0e9ef;
            font-size: clamp(1rem, 2vw, 1.22rem);
        }}
        .hero-actions {{
            display: flex; flex-wrap: wrap; gap: 12px; margin-top: 30px;
        }}
        .button {{
            display: inline-flex; align-items: center; justify-content: center;
            min-height: 48px; padding: 12px 20px; border-radius: 999px;
            text-decoration: none; font-weight: 800; transition: transform .2s ease;
        }}
        .button:hover {{ transform: translateY(-2px); }}
        .button-primary {{ background: white; color: var(--navy); }}
        .button-outline {{ color: white; border: 1px solid rgba(255,255,255,.45); }}
        .section {{ padding: 86px 0; }}
        .section-soft {{ background: var(--light); }}
        .section-heading {{ max-width: 760px; margin-bottom: 34px; }}
        .kicker {{
            color: var(--teal); font-size: .78rem; font-weight: 850;
            letter-spacing: .13em; text-transform: uppercase;
        }}
        h2 {{
            margin: 8px 0 12px; color: var(--navy);
            font-size: clamp(2rem, 4vw, 3.2rem);
            line-height: 1.12; letter-spacing: -.045em;
        }}
        .section-heading p, .muted {{ color: var(--muted); }}
        .about-grid {{
            display: grid; grid-template-columns: 1.2fr .8fr;
            gap: 42px; align-items: start;
        }}
        .about-panel {{
            padding: 28px; border: 1px solid #e5ebef;
            border-radius: var(--radius); background: white; box-shadow: var(--shadow);
        }}
        .about-panel h3 {{ margin-top: 0; color: var(--navy); }}
        .tags {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .tag {{
            display: inline-flex; align-items: center; padding: 6px 10px;
            border: 1px solid #dfe8eb; border-radius: 999px;
            background: #f5f9fa; color: #28515a; font-size: .78rem;
            font-weight: 750;
        }}
        .project-grid {{
            display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
        }}
        .project-card {{
            display: flex; flex-direction: column; align-items: flex-start;
            padding: 26px; border: 1px solid #e5ebef; border-radius: var(--radius);
            background: white; box-shadow: 0 8px 24px rgba(19,36,58,.04);
            transition: transform .25s ease, box-shadow .25s ease;
        }}
        .project-card:hover {{
            transform: translateY(-5px); box-shadow: var(--shadow);
        }}
        .project-top {{
            display: flex; align-items: center; gap: 10px; margin-bottom: 12px;
        }}
        .project-mark {{
            width: 38px; height: 38px; display: grid; place-items: center;
            border-radius: 12px; background: #e6f3f2; color: var(--teal);
            font-size: 1.3rem;
        }}
        .project-category {{
            color: var(--teal); font-size: .75rem; font-weight: 800;
        }}
        .project-card h3, .timeline-item h3, .course-card h3 {{
            margin: 5px 0 8px; color: var(--navy); line-height: 1.3;
        }}
        .project-card p {{ color: var(--muted); font-size: .93rem; }}
        .project-card .tags {{ margin: 10px 0 20px; }}
        .text-link {{
            margin-top: auto; color: var(--navy);
            font-size: .9rem; font-weight: 850; text-decoration: none;
        }}
        .timeline {{ display: grid; gap: 14px; }}
        .timeline-item {{
            display: grid; grid-template-columns: 120px 1fr;
            gap: 22px; padding: 24px;
            background: white; border: 1px solid #e4eaee; border-radius: 14px;
        }}
        .timeline-date, .course-year {{
            color: var(--teal); font-size: .82rem; font-weight: 850;
        }}
        .timeline-item p, .course-card p {{ margin-bottom: 0; color: var(--muted); }}
        .experience-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 20px;
        }}
        .experience-card {{
            padding: 28px; background: white; border: 1px solid #e4eaee;
            border-radius: var(--radius);
        }}
        .experience-card h3 {{ color: var(--navy); }}
        .experience-type {{ color: var(--teal); font-weight: 750; font-size: .88rem; }}
        .experience-card li {{ margin: 8px 0; }}
        .courses-grid {{
            display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px;
        }}
        .course-card {{
            padding: 22px; border: 1px solid #e4eaee; border-radius: 15px;
            background: white;
        }}
        .contact-panel {{
            display: flex; justify-content: space-between; align-items: center;
            gap: 28px; padding: clamp(28px, 5vw, 54px);
            border-radius: 24px; color: white;
            background: linear-gradient(135deg, var(--navy), #20545d);
        }}
        .contact-panel h2 {{ color: white; }}
        .contact-panel p {{ max-width: 650px; color: #dce8ef; }}
        .contact-links {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .contact-links .button-outline {{ white-space: nowrap; }}
        .footer {{
            padding: 28px 0; color: var(--muted);
            font-size: .85rem; border-top: 1px solid #e5ebef;
        }}
        .footer-inner {{
            display: flex; justify-content: space-between; gap: 15px; flex-wrap: wrap;
        }}
        .source-summary {{
            margin-top: 35px; padding: 20px;
            border: 1px dashed #b7c8cf; border-radius: 14px;
            background: #fff;
        }}
        .source-summary h3 {{ color: var(--navy); }}
        .source-summary h4 {{ margin-bottom: 6px; }}
        .source-summary li {{ overflow-wrap: anywhere; }}
        .reveal {{ opacity: 0; transform: translateY(18px); }}
        .reveal.visible {{
            opacity: 1; transform: translateY(0);
            transition: opacity .6s ease, transform .6s ease;
        }}
        @media (max-width: 900px) {{
            .project-grid, .courses-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .about-grid {{ grid-template-columns: 1fr; }}
            .contact-panel {{ align-items: flex-start; flex-direction: column; }}
        }}
        @media (max-width: 650px) {{
            .nav-inner {{ align-items: flex-start; flex-direction: column; padding: 15px 0; gap: 10px; }}
            .nav-links {{ gap: 12px; }}
            .nav-links a {{ font-size: .82rem; }}
            .hero {{ padding: 75px 0; }}
            .section {{ padding: 62px 0; }}
            .project-grid, .courses-grid, .experience-grid {{ grid-template-columns: 1fr; }}
            .timeline-item {{ grid-template-columns: 1fr; gap: 7px; }}
            .contact-links {{ align-items: stretch; flex-direction: column; width: 100%; }}
            .contact-links .button {{ width: 100%; }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                scroll-behavior: auto !important;
                transition-duration: .01ms !important;
                animation-duration: .01ms !important;
            }}
            .reveal {{ opacity: 1; transform: none; }}
        }}
    </style>
</head>
<body>
    <a class="skip-link" href="#main">Saltar al contenido</a>

    <nav class="navbar" aria-label="Navegación principal">
        <div class="container nav-inner">
            <a class="brand" href="#inicio">ME.</a>
            <div class="nav-links">
                <a href="#sobre-mi">Sobre mí</a>
                <a href="#proyectos">Proyectos</a>
                <a href="#experiencia">Experiencia</a>
                <a href="#formacion">Formación</a>
                <a href="#contacto">Contacto</a>
            </div>
        </div>
    </nav>

    <main id="main">
        <section class="hero" id="inicio">
            <div class="container hero-content">
                <span class="eyebrow">Portfolio profesional</span>
                <h1>{esc(data.title)}</h1>
                <p><strong>{esc(data.subtitle)}</strong></p>
                <p>{esc(data.summary)}</p>
                <div class="hero-actions">
                    <a class="button button-primary" href="#proyectos">
                        Explorar proyectos <span aria-hidden="true">&nbsp;↘</span>
                    </a>
                    <a class="button button-outline"
                       href="{esc(data.github)}"
                       target="_blank" rel="noopener noreferrer">
                        GitHub ↗
                    </a>
                </div>
            </div>
        </section>

        <section class="section" id="sobre-mi">
            <div class="container">
                <div class="section-heading">
                    <span class="kicker">Perfil</span>
                    <h2>Tecnología con propósito.</h2>
                    <p>
                        Desarrollo de software, visión artificial y seguridad
                        desde una perspectiva práctica, accesible y orientada
                        a la mejora continua.
                    </p>
                </div>
                <div class="about-grid">
                    <div>
                        <p>{esc(data.summary)}</p>
                        <p><strong>Ubicación:</strong> {esc(data.location)}</p>
                        <p>
                            <strong>Intereses:</strong> desarrollo de aplicaciones,
                            automatización, inteligencia artificial y ciberseguridad
                            defensiva.
                        </p>
                    </div>
                    <div class="about-panel">
                        <h3>Competencias técnicas</h3>
                        <div class="tags">{skills}</div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section section-soft" id="proyectos">
            <div class="container">
                <div class="section-heading">
                    <span class="kicker">Trabajo seleccionado</span>
                    <h2>Proyectos destacados.</h2>
                    <p>
                        Proyectos y áreas técnicas que muestran mi formación,
                        intereses y experiencia práctica.
                    </p>
                </div>
                <div class="project-grid">{projects}</div>
            </div>
        </section>

        <section class="section" id="experiencia">
            <div class="container">
                <div class="section-heading">
                    <span class="kicker">Trayectoria</span>
                    <h2>Experiencia profesional.</h2>
                </div>
                <div class="experience-grid">{experience}</div>
            </div>
        </section>

        <section class="section section-soft" id="formacion">
            <div class="container">
                <div class="section-heading">
                    <span class="kicker">Aprendizaje continuo</span>
                    <h2>Formación académica.</h2>
                </div>
                <div class="timeline">{education}</div>

                <div class="section-heading" style="margin-top:48px">
                    <span class="kicker">Especialización</span>
                    <h2>Formación complementaria.</h2>
                </div>
                <div class="courses-grid">{courses}</div>
                {streamlit_summary}
            </div>
        </section>

        <section class="section" id="contacto">
            <div class="container">
                <div class="contact-panel">
                    <div>
                        <span class="kicker">Contacto</span>
                        <h2>¿Hablamos de tecnología?</h2>
                        <p>
                            Estoy interesado en oportunidades relacionadas con
                            desarrollo web, inteligencia artificial y
                            ciberseguridad. Puedes contactar conmigo o consultar
                            mi código en GitHub.
                        </p>
                        <p>{esc(data.location)}</p>
                    </div>
                    <div class="contact-links">
                        <a class="button button-primary"
                           href="mailto:{esc(data.email)}">Enviar email ↗</a>
                        <a class="button button-outline"
                           href="{esc(data.linkedin)}"
                           target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
                        <a class="button button-outline"
                           href="{esc(data.github)}"
                           target="_blank" rel="noopener noreferrer">GitHub ↗</a>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container footer-inner">
            <span>© <span id="year"></span> {esc(data.title)}</span>
            <span>Desarrollado con HTML, CSS y JavaScript.</span>
            <a href="#inicio">Volver arriba ↑</a>
        </div>
    </footer>

    <script>
        "use strict";

        // Año dinámico.
        document.getElementById("year").textContent =
            String(new Date().getFullYear());

        // Aparición progresiva al desplazarse.
        // Se respeta la preferencia de movimiento reducido.
        const revealItems = document.querySelectorAll(".reveal");
        const reduceMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        if ("IntersectionObserver" in window && !reduceMotion) {{
            const observer = new IntersectionObserver(
                (entries, activeObserver) => {{
                    entries.forEach((entry) => {{
                        if (entry.isIntersecting) {{
                            entry.target.classList.add("visible");
                            activeObserver.unobserve(entry.target);
                        }}
                    }});
                }},
                {{ threshold: 0.12 }}
            );

            revealItems.forEach((item) => observer.observe(item));
        }} else {{
            revealItems.forEach((item) => item.classList.add("visible"));
        }}

        // Menú activo según la sección visible.
        const sections = document.querySelectorAll("main section[id]");
        const navLinks = document.querySelectorAll(".nav-links a");

        if ("IntersectionObserver" in window) {{
            const sectionObserver = new IntersectionObserver(
                (entries) => {{
                    entries.forEach((entry) => {{
                        if (!entry.isIntersecting) return;

                        navLinks.forEach((link) => {{
                            const active =
                                link.getAttribute("href") ===
                                "#" + entry.target.id;

                            if (active) {{
                                link.setAttribute("aria-current", "location");
                            }} else {{
                                link.removeAttribute("aria-current");
                            }}
                        }});
                    }});
                }},
                {{ rootMargin: "-25% 0px -60% 0px" }}
            );

            sections.forEach((section) => sectionObserver.observe(section));
        }}
    </script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exporta contenido estático de Streamlit a un portafolio HTML."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("streamlit_app.py"),
        help="Archivo Python de Streamlit que se analizará.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("dist"),
        help="Carpeta de salida para GitHub Pages.",
    )
    parser.add_argument(
        "--title",
        default=DEFAULT_TITLE,
        help="Nombre que aparece en el portafolio.",
    )
    parser.add_argument(
        "--email",
        default="mderkaoui10@gmail.com",
        help="Correo de contacto.",
    )
    parser.add_argument(
        "--github",
        default=DEFAULT_GITHUB,
        help="URL del perfil GitHub.",
    )
    parser.add_argument(
        "--linkedin",
        default=(
            "https://www.linkedin.com/in/"
            "mohamed-merzouk-bendoukh-ejea-aragon"
        ),
        help="URL de LinkedIn.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostrar mensajes de diagnóstico.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    data = PortfolioData(
        title=args.title,
        email=args.email,
        github=args.github,
        linkedin=args.linkedin,
        website="https://MohamedElderkaoui.github.io",
    )

    source_data = read_streamlit_source(args.source.resolve())
    for warning in source_data["warnings"]:
        LOG.warning(warning)

    html_document = build_html(data, source_data)
    output_file = output_dir / "index.html"
    temp_file = output_dir / "index.html.tmp"

    try:
        temp_file.write_text(html_document, encoding="utf-8")
        temp_file.replace(output_file)
    except OSError as exc:
        LOG.error("No se pudo guardar el HTML: %s", exc)
        try:
            temp_file.unlink(missing_ok=True)
        except OSError:
            pass
        return 1

    # Validación básica del HTML producido.
    if not output_file.is_file() or output_file.stat().st_size < 1000:
        LOG.error("El HTML generado parece incompleto.")
        return 1

    if BeautifulSoup is not None:
        try:
            soup = BeautifulSoup(
                output_file.read_text(encoding="utf-8"),
                "html.parser",
            )
            if soup.find("html") is None or soup.find("main") is None:
                LOG.error("La validación HTML no encontró las etiquetas principales.")
                return 1
            LOG.info("Validación HTML correcta.")
        except (OSError, ValueError) as exc:
            LOG.warning("No se pudo validar el HTML: %s", exc)

    print("PORTAFOLIO HTML GENERADO")
    print("=" * 45)
    print(f"Archivo: {output_file}")
    print(f"Tamaño: {output_file.stat().st_size:,} bytes")
    print(f"Origen Streamlit: {args.source.resolve()}")
    print()
    print("Siguiente paso:")
    print("1. Publica el contenido de la carpeta dist en GitHub Pages.")
    print("2. Usa la rama y carpeta configuradas en Settings > Pages.")
    print("3. Recuerda: el backend Python/YOLO de Streamlit no se ejecuta en Pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())