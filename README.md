# Portfolio Website

A full-stack personal portfolio built with Django and a glassmorphism dark UI. All content — projects, experience, skills, certificates — is managed through a custom Django admin panel.

![Django](https://img.shields.io/badge/Django-6.0-0c4b33?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.12-3776ab?style=flat-square&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952b3?style=flat-square&logo=bootstrap)
![Render](https://img.shields.io/badge/Deploy-Render-46e3b7?style=flat-square)

---

## Features at a Glance

- Single-page layout with animated section transitions
- Contact form with Cloudflare Turnstile bot protection
- Portfolio grid with live category filtering (Isotope)
- Full Django admin with custom glassmorphic dark theme
- Production-ready: PostgreSQL, WhiteNoise, Gunicorn

---

## Frontend

### Design
The UI follows a **glassmorphism** design language — frosted glass cards, backdrop-blur surfaces, and a dark palette with purple gradient accents. All defined via CSS custom properties for easy theming.

### Canvas Animations
Three custom canvas effects built with vanilla JS:

| Section | Effect |
|---|---|
| Hero | Neural network graph with pulsing nodes and animated edges |
| About | Three-layer wavy lines with independent phase offsets |
| Resume | Particle system with distance-based connection lines |

All animations use `requestAnimationFrame` and `IntersectionObserver` — they pause when off-screen.

### Libraries
- **Typed.js** — rotating typed text in the hero
- **AOS** — scroll-triggered entrance animations
- **Isotope** — filterable, animated portfolio grid
- **GLightbox** — project image lightbox
- **PureCounter** — animated stat counters
- **Bootstrap Icons** — icon set throughout

---

## Backend

### Stack
- **Django 6.0.5** — routing, ORM, admin, email
- **SQLite** (local dev) / **PostgreSQL** (production via `DATABASE_URL`)
- **WhiteNoise** — compressed static file serving, no separate CDN needed
- **Gunicorn** — WSGI server for production

### Content Models

| Model | Description |
|---|---|
| `HomeSection` | Hero content — headline, bio, CTA buttons, social links |
| `AboutSection` | Profile card, stats, bio, resume URL |
| `Project` | Portfolio items with slug routing, tech stack, links, highlights |
| `Experience` / `Education` | Resume entries, linkable to projects |
| `Skill` / `SkillCategory` | Skills with 1–5 rating scale |
| `Certificate` | Certificates with issuer and verification URL |
| `Recommendation` | Testimonials with author info |
| `GeneralSettings` | Site name and favicon |

Singleton models (`HomeSection`, `AboutSection`, etc.) enforce a single instance — the admin redirects their list view directly to the edit form.

### Admin Panel
The Django admin is fully reskinned to match the main site: glassmorphic dark theme, gradient header, custom form and file upload styling, and scoped CSS so it doesn't bleed into the public-facing pages.

---

## Security

### Contact Form
- **Cloudflare Turnstile** — bot protection rendered on form interaction, verified server-side before any email is sent
- **CSRF protection** — Django's built-in middleware, enforced on all POST routes
- **AJAX submission** — form data sent asynchronously; a toast notification delivers feedback without a page reload
- Turnstile verification fails open (still delivers message) if Cloudflare is unreachable

### Environment Variables
All secrets are kept out of the codebase via `.env` (local) and platform environment variables (production):

```
SECRET_KEY, DEBUG, ALLOWED_HOSTS
EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, CONTACT_EMAIL
TURNSTILE_SITE_KEY, TURNSTILE_SECRET_KEY
DATABASE_URL
```

---

## Deployment

Deployed on **Render** using the included `render.yaml` (web service + free PostgreSQL).

### First-time setup
```bash
# Render runs build.sh automatically on every deploy:
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

After the first deploy, create your admin user via the Render shell:
```bash
python manage.py createsuperuser
```

### Local development
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in your values
python manage.py migrate
python manage.py runserver
```

---

## Project Structure

```
portfolio_website/
├── core/               # Main app — models, views, URLs, template tags
├── general/            # Site-wide settings (name, favicon)
├── portfolio/          # Django project config — settings, wsgi, urls
├── templates/          # HTML templates + custom admin overrides
├── frontend/assets/    # CSS, JS, images, vendor libraries
├── render.yaml         # Render deployment config
└── build.sh            # Render build script
```
