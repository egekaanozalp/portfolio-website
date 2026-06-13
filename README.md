# Portfolio Website

A full-stack personal portfolio built with Django and a glassmorphism dark UI. All content — projects, experience, skills, certificates — is managed through a custom Django admin panel.

![Django](https://img.shields.io/badge/Django-6.0-0c4b33?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.12-3776ab?style=flat-square&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952b3?style=flat-square&logo=bootstrap)
![Cloudinary](https://img.shields.io/badge/Media-Cloudinary-3448c5?style=flat-square&logo=cloudinary)
![Render](https://img.shields.io/badge/Deploy-Render-46e3b7?style=flat-square)

---

## Features at a Glance

- Single-page layout with animated section transitions
- Contact form with Cloudflare Turnstile bot protection and HTML email notifications
- Portfolio grid with live category filtering (Isotope)
- Full Django admin with custom glassmorphic dark theme and brute-force lockout
- Production-ready: PostgreSQL, Cloudinary media storage, Resend email, WhiteNoise, Gunicorn

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
- **Cloudinary** — media file storage in production (images, favicon, OG image)
- **WhiteNoise** — compressed static file serving
- **Resend** (via `django-anymail`) — transactional email over HTTPS API, no SMTP ports needed
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
| `GeneralSettings` | Site name, favicon, and Open Graph image for social sharing |

Singleton models (`HomeSection`, `AboutSection`, etc.) enforce a single instance — the admin redirects their list view directly to the edit form.

### Admin Panel
The Django admin is fully reskinned to match the main site: glassmorphic dark theme, gradient header, custom form and file upload styling, and scoped CSS so it doesn't bleed into the public-facing pages.

---

## Security

### Contact Form
- **Cloudflare Turnstile** — bot protection rendered on form interaction, verified server-side before any email is sent
- The contact endpoint is **CSRF-exempt** — Turnstile token verification is the sole security layer (eliminates Safari ITP cookie-blocking issues on mobile)
- **AJAX submission** — form data sent asynchronously; a toast notification delivers feedback without a page reload
- Field values are captured before the Turnstile iframe renders to prevent iOS Safari autofill clearing
- Turnstile verification fails open (still delivers the message) if Cloudflare is unreachable

### Admin Brute-Force Protection
**django-axes** locks out an IP after 5 consecutive failed login attempts for 1 hour. The lockout counter resets automatically on a successful login.

| Setting | Value |
|---|---|
| Max attempts | 5 |
| Lockout duration | 1 hour |
| Lockout scope | IP address |

All access attempts and lockout events are logged and visible in the Django admin under **Axes → Access Attempts**.

### Environment Variables
All secrets are kept out of the codebase via `.env` (local) and platform environment variables (production):

```
SECRET_KEY, DEBUG, ALLOWED_HOSTS

# Database
DATABASE_URL

# Email (Resend)
RESEND_API_KEY
DEFAULT_FROM_EMAIL
CONTACT_EMAIL

# Cloudflare Turnstile
TURNSTILE_SITE_KEY
TURNSTILE_SECRET_KEY

# Cloudinary media storage (production only)
# Format: cloudinary://api_key:api_secret@cloud_name
CLOUDINARY_URL
```

When `CLOUDINARY_URL` is set, media files are stored and served via Cloudinary. When `RESEND_API_KEY` is set, email is sent via Resend. Both fall back to local behaviour (filesystem / console) in development.

---

## Deployment

Deployed on **Render** using the included `render.yaml` (web service + free PostgreSQL).

### First-time setup
```bash
# Render runs build.sh automatically on every deploy:
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --noinput || true
python manage.py axes_reset
```

The following environment variables must be set manually in the Render dashboard (they are not in `render.yaml` to keep secrets out of source control):

```
RESEND_API_KEY, DEFAULT_FROM_EMAIL, CONTACT_EMAIL
TURNSTILE_SITE_KEY, TURNSTILE_SECRET_KEY
CLOUDINARY_URL
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

In local dev, leave `CLOUDINARY_URL` and `RESEND_API_KEY` unset — media files are served from the local `media/` directory and emails are printed to the console.

---

## Project Structure

```
portfolio_website/
├── core/               # Main app — models, views, URLs, template tags
├── general/            # Site-wide settings (name, favicon, OG image)
├── portfolio/          # Django project config — settings, wsgi, urls
├── templates/          # HTML templates + custom admin overrides
│   └── email/          # HTML email templates
├── frontend/assets/    # CSS, JS, images, vendor libraries
├── render.yaml         # Render deployment config
└── build.sh            # Render build script
```
