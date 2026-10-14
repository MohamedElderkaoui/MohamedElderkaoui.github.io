
from pathlib import Path
from html import escape
import streamlit as st

# ============================================================
# MOHAMED ELDERKAOUI — PORTFOLIO STATIC HTML GENERATOR
# Streamlit -> index.html -> GitHub Pages
# ============================================================

st.set_page_config(
    page_title="Portfolio Builder | Mohamed Elderkaoui",
    page_icon="💻",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.resolve().parent / "docs"
OUTPUT_FILE = OUTPUT_DIR / "index.html"

PROFILE = {
    "name": "Mohamed Merzouk Bendoukha",
    "username": "MohamedElderkaoui",
    "location": "Ejea de los Caballeros, Zaragoza, Spain",
    "email": "mderkaoui10@gmail.com",
    "github": "https://github.com/MohamedElderkaoui",
    "linkedin": (
        "https://www.linkedin.com/in/"
        "mohamed-merzouk-bendoukh-ejea-aragon"
    ),
    "title": (
        "Web Developer | Artificial Intelligence "
        "| Cybersecurity"
    ),
    "description": (
        "Técnico Superior en Desarrollo de Aplicaciones Web "
        "con formación complementaria en inteligencia artificial, "
        "Python y ciberseguridad defensiva."
    ),
}

SKILLS = {
    "Web Development": [
        "HTML5", "CSS3", "JavaScript", "Bootstrap",
        "Python", "PHP", "SQL", "REST APIs", "Git", "GitHub",
    ],
    "Artificial Intelligence": [
        "Python", "YOLO", "OpenCV", "PyTorch",
        "Streamlit", "pandas", "NumPy", "scikit-learn",
        "Computer Vision", "Machine Learning",
    ],
    "Cybersecurity": [
        "Blue Team", "Splunk", "Nessus", "Sigma Rules",
        "Digital Forensics", "Incident Response",
        "IDS", "Vulnerability Management",
    ],
}

PROJECTS = [
    {
        "name": "AccessAI",
        "category": "Artificial Intelligence",
        "description": (
            "Prototipo de visión artificial para detectar elementos "
            "urbanos relacionados con la accesibilidad en imágenes "
            "y vídeos."
        ),
        "technologies": [
            "Python", "YOLO", "OpenCV", "PyTorch", "Streamlit"
        ],
        "github": (
            "https://github.com/MohamedElderkaoui"
        ),
    },
    {
        "name": "Web Development Portfolio",
        "category": "Web Development",
        "description": (
            "Portfolio personal para presentar proyectos, "
            "competencias técnicas y formación profesional."
        ),
        "technologies": ["HTML5", "CSS3", "JavaScript", "GitHub Pages"],
        "github": (
            "https://github.com/MohamedElderkaoui"
        ),
    },
    {
        "name": "Cybersecurity Learning",
        "category": "Cybersecurity",
        "description": (
            "Formación en seguridad defensiva, análisis forense "
            "digital, monitorización y respuesta a incidentes."
        ),
        "technologies": [
            "Blue Team", "Splunk", "Sigma", "Nessus"
        ],
        "github": (
            "https://github.com/MohamedElderkaoui"
        ),
    },
]

EDUCATION = [
    {
        "date": "2025–2026",
        "name": (
            "III Diploma de Extensión Universitaria "
            "en Inteligencia Artificial Avanzada"
        ),
        "institution": (
            "Samsung Innovation Campus · Universidad de Málaga "
            "· Fundación ONCE · Samsung"
        ),
    },
    {
        "date": "2025–2026",
        "name": (
            "III Microcredencial Universitaria en Introducción "
            "a la Programación en Python para Inteligencia Artificial"
        ),
        "institution": (
            "Universidad de Málaga · Fundación ONCE · Samsung"
        ),
    },
    {
        "date": "2025",
        "name": "Experto en Blue Team — 250 horas",
        "institution": "Inserta · INCIBE · Arelance",
    },
    {
        "date": "2025",
        "name": "Digital Forensic and Incident Response — 300 horas",
        "institution": "Inserta · INCIBE · Arelance",
    },
    {
        "date": "2019–2024",
        "name": "Técnico Superior en Desarrollo de Aplicaciones Web",
        "institution": "CPIFP Los Enlaces / IES Río Arba",
    },
]

def build_html(profile, skills, projects, education, theme):
    name = escape(profile["name"])
    title = escape(profile["title"])
    description = escape(profile["description"])
    location = escape(profile["location"])
    email = escape(profile["email"])
    github = escape(profile["github"], quote=True)
    linkedin = escape(profile["linkedin"], quote=True)

    skill_sections = ""

    for category, values in skills.items():
        tags = "".join(
            f'<span class="tag">{escape(skill)}</span>'
            for skill in values
        )

        skill_sections += f"""
        <div class="skill-group">
            <h3>{escape(category)}</h3>
            <div class="tags">{tags}</div>
        </div>
        """

    project_cards = ""

    for project in projects:
        tags = "".join(
            f'<span class="tag">{escape(item)}</span>'
            for item in project["technologies"]
        )

        project_cards += f"""
        <article class="project-card">
            <span class="eyebrow">
                {escape(project["category"])}
            </span>

            <h3>{escape(project["name"])}</h3>

            <p>{escape(project["description"])}</p>

            <div class="tags">{tags}</div>

            <a class="text-link"
               href="{escape(project["github"], quote=True)}"
               target="_blank"
               rel="noopener noreferrer">
                View GitHub ↗
            </a>
        </article>
        """

    education_cards = ""

    for item in education:
        education_cards += f"""
        <article class="timeline-item">
            <span class="date">{escape(item["date"])}</span>
            <div>
                <h3>{escape(item["name"])}</h3>
                <p>{escape(item["institution"])}</p>
            </div>
        </article>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{name} | Developer Portfolio</title>

<meta name="description" content="{description}">
<meta name="author" content="{name}">
<meta name="theme-color" content="{theme}">
<meta property="og:title" content="{name} | Portfolio">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">

<style>
:root {{
    --bg: #0b1120;
    --surface: #111b2e;
    --surface-light: #18243a;
    --text: #e7edf7;
    --muted: #a6b3c8;
    --accent: {theme};
    --border: rgba(255,255,255,.10);
    --radius: 18px;
    --max-width: 1120px;
}}

* {{
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
    scroll-padding-top: 85px;
}}

body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: Inter, "Segoe UI", Arial, sans-serif;
    line-height: 1.7;
}}

a {{
    color: inherit;
    text-decoration: none;
}}

a:focus-visible,
button:focus-visible {{
    outline: 3px solid var(--accent);
    outline-offset: 4px;
}}

.container {{
    width: min(92%, var(--max-width));
    margin-inline: auto;
}}

nav {{
    position: sticky;
    top: 0;
    z-index: 10;
    background: rgba(11,17,32,.92);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border);
}}

.nav-inner {{
    min-height: 72px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}}

.logo {{
    font-weight: 800;
    letter-spacing: -.5px;
}}

.logo span {{
    color: var(--accent);
}}

.nav-links {{
    display: flex;
    flex-wrap: wrap;
    gap: 22px;
    font-size: .9rem;
    color: var(--muted);
}}

.nav-links a:hover,
.text-link:hover {{
    color: var(--accent);
}}

.hero {{
    min-height: 75vh;
    display: flex;
    align-items: center;
    padding: 90px 0;
}}

.eyebrow {{
    color: var(--accent);
    font-size: .8rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
}}

h1 {{
    max-width: 900px;
    margin: 18px 0;
    font-size: clamp(2.7rem, 7vw, 5.7rem);
    line-height: 1.04;
    letter-spacing: -3px;
}}

h1 span {{
    color: var(--accent);
}}

.hero p {{
    max-width: 720px;
    color: var(--muted);
    font-size: 1.12rem;
}}

.actions {{
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin-top: 30px;
}}

.button {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 19px;
    border: 1px solid var(--border);
    border-radius: 10px;
    font-weight: 700;
    transition: transform .2s, background .2s;
}}

.button:hover {{
    transform: translateY(-3px);
}}

.button.primary {{
    background: var(--accent);
    color: #07111d;
    border-color: transparent;
}}

section {{
    padding: 75px 0;
    border-top: 1px solid var(--border);
}}

.section-heading {{
    margin-bottom: 34px;
}}

h2 {{
    font-size: clamp(2rem, 4vw, 3.2rem);
    line-height: 1.15;
    margin: 8px 0;
    letter-spacing: -1px;
}}

.muted {{
    color: var(--muted);
}}

.project-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 20px;
}}

.project-card,
.skill-group {{
    padding: 25px;
    border: 1px solid var(--border);
    background: var(--surface);
    border-radius: var(--radius);
    transition: transform .2s, border-color .2s;
}}

.project-card:hover {{
    transform: translateY(-5px);
    border-color: var(--accent);
}}

.project-card h3,
.skill-group h3,
.timeline-item h3 {{
    line-height: 1.35;
}}

.project-card p,
.timeline-item p {{
    color: var(--muted);
    font-size: .94rem;
}}

.tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 18px 0;
}}

.tag {{
    display: inline-block;
    padding: 5px 9px;
    border: 1px solid var(--border);
    border-radius: 7px;
    color: var(--muted);
    font-size: .76rem;
}}

.text-link {{
    color: var(--accent);
    font-weight: 800;
}}

.skills-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
}}

.timeline {{
    display: grid;
    gap: 16px;
}}

.timeline-item {{
    display: grid;
    grid-template-columns: 115px 1fr;
    gap: 20px;
    padding: 20px 0;
    border-bottom: 1px solid var(--border);
}}

.timeline-item h3 {{
    margin: 0;
    font-size: 1rem;
}}

.timeline-item p {{
    margin-bottom: 0;
}}

.date {{
    color: var(--accent);
    font-weight: 800;
}}

.contact-panel {{
    padding: clamp(25px, 6vw, 55px);
    border: 1px solid var(--border);
    border-radius: 25px;
    background: linear-gradient(135deg, var(--surface), #111a2b);
}}

footer {{
    padding: 30px 0;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: .85rem;
}}

.footer-inner {{
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 15px;
}}

@media (max-width: 800px) {{
    .project-grid {{
        grid-template-columns: 1fr;
    }}

    .skills-grid {{
        grid-template-columns: 1fr;
    }}

    .hero {{
        min-height: auto;
        padding: 90px 0;
    }}

    h1 {{
        letter-spacing: -1.5px;
    }}
}}

@media (max-width: 520px) {{
    .nav-inner {{
        align-items: flex-start;
        flex-direction: column;
        padding: 15px 0;
    }}

    .nav-links {{
        gap: 14px;
    }}

    .timeline-item {{
        grid-template-columns: 1fr;
        gap: 3px;
    }}
}}

@media (prefers-reduced-motion: reduce) {{
    *,
    *::before,
    *::after {{
        scroll-behavior: auto !important;
        transition: none !important;
    }}
}}
</style>
</head>

<body>
<nav aria-label="Main navigation">
    <div class="container nav-inner">
        <a class="logo" href="#home">ME<span>.</span></a>
        <div class="nav-links">
            <a href="#about">About</a>
            <a href="#projects">Projects</a>
            <a href="#skills">Skills</a>
            <a href="#education">Education</a>
            <a href="#contact">Contact</a>
        </div>
    </div>
</nav>

<main>
    <header class="hero container" id="home">
        <div>
            <span class="eyebrow">Available for opportunities</span>
            <h1>Building digital<br>
                <span>solutions that matter.</span>
            </h1>
            <p>{description}</p>
            <p>📍 {location}</p>
            <div class="actions">
                <a class="button primary" href="#projects">
                    Explore my work
                </a>
                <a class="button"
                   href="mailto:{email}">
                    Contact me
                </a>
                <a class="button"
                   href="{github}"
                   target="_blank"
                   rel="noopener noreferrer">
                    GitHub ↗
                </a>
            </div>
        </div>
    </header>

    <section id="about">
        <div class="container">
            <div class="section-heading">
                <span class="eyebrow">01 / About</span>
                <h2>{title}</h2>
            </div>
            <p class="muted">{description}</p>
            <p class="muted">
                Interested in software development, computer vision,
                technical problem-solving and defensive cybersecurity.
                Focused on continuous learning and building practical
                projects.
            </p>
        </div>
    </section>

    <section id="projects">
        <div class="container">
            <div class="section-heading">
                <span class="eyebrow">02 / Selected work</span>
                <h2>Projects</h2>
                <p class="muted">
                    Projects and technical areas I am developing.
                </p>
            </div>
            <div class="project-grid">
                {project_cards}
            </div>
        </div>
    </section>

    <section id="skills">
        <div class="container">
            <div class="section-heading">
                <span class="eyebrow">03 / Technical toolkit</span>
                <h2>Skills & technologies</h2>
            </div>
            <div class="skills-grid">
                {skill_sections}
            </div>
        </div>
    </section>

    <section id="education">
        <div class="container">
            <div class="section-heading">
                <span class="eyebrow">04 / Learning journey</span>
                <h2>Education & training</h2>
            </div>
            <div class="timeline">
                {education_cards}
            </div>
        </div>
    </section>

    <section id="contact">
        <div class="container">
            <div class="contact-panel">
                <span class="eyebrow">05 / Contact</span>
                <h2>Let's build something useful.</h2>
                <p class="muted">
                    Interested in junior opportunities in web development,
                    AI or cybersecurity? Get in touch.
                </p>
                <div class="actions">
                    <a class="button primary"
                       href="mailto:{email}">
                        Send an email
                    </a>
                    <a class="button"
                       href="{linkedin}"
                       target="_blank"
                       rel="noopener noreferrer">
                        LinkedIn ↗
                    </a>
                    <a class="button"
                       href="{github}"
                       target="_blank"
                       rel="noopener noreferrer">
                        GitHub ↗
                    </a>
                </div>
            </div>
        </div>
    </section>
</main>

<footer>
    <div class="container footer-inner">
        <span>© <span id="year"></span> {name}</span>
        <span>Designed with HTML, CSS and JavaScript.</span>
    </div>
</footer>

<script>
document.getElementById("year").textContent =
    new Date().getFullYear();
</script>
</body>
</html>
"""


st.title("💻 Portfolio HTML Generator")
st.caption(
    "Generate a static portfolio for GitHub Pages. "
    "The output is HTML, CSS and JavaScript — no Streamlit server required."
)

with st.sidebar:
    st.header("Portfolio settings")
    name = st.text_input("Full name", PROFILE["name"])
    headline = st.text_input("Headline", PROFILE["title"])
    email = st.text_input("Email", PROFILE["email"])
    location = st.text_input("Location", PROFILE["location"])
    github = st.text_input("GitHub URL", PROFILE["github"])
    linkedin = st.text_input("LinkedIn URL", PROFILE["linkedin"])
    theme = st.color_picker("Accent color", "#35D0BA")

    st.divider()
    st.caption("Output folder: docs/")
    st.caption("Output file: docs/index.html")

edited_profile = {
    **PROFILE,
    "name": name,
    "title": headline,
    "email": email,
    "location": location,
    "github": github,
    "linkedin": linkedin,
}

html_content = build_html(
    edited_profile,
    SKILLS,
    PROJECTS,
    EDUCATION,
    theme,
)

preview_tab, source_tab, deploy_tab = st.tabs(
    ["Preview", "HTML source", "GitHub Pages"]
)

with preview_tab:
    st.components.v1.html(
        html_content,
        height=650,
        scrolling=True,
    )

with source_tab:
    st.code(html_content, language="html")
    st.download_button(
        "⬇️ Download index.html",
        data=html_content.encode("utf-8"),
        file_name="index.html",
        mime="text/html",
        use_container_width=True,
    )

with deploy_tab:
    st.markdown(
        """
        ### Publish your static portfolio

        1. Save `index.html` in the `docs` directory.
        2. Push the repository to GitHub.
        3. Open repository **Settings → Pages**.
        4. Select **Deploy from a branch**.
        5. Choose your branch and the `/docs` folder.
        6. Save and wait for GitHub Pages to publish.
        """
    )

    if st.button("Generate docs/index.html", type="primary"):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(
            html_content,
            encoding="utf-8",
        )
        st.success(f"Generated: {OUTPUT_FILE}")
        st.code(
            f'git add docs/index.html\n'
            f'git commit -m "Build static portfolio"\n'
            f'git push',
            language="powershell",
        )

st.divider()
st.caption(
    "Before publishing, verify project links and personal contact details. "
    "GitHub Pages hosts static files; it does not run Streamlit or Python."
)
