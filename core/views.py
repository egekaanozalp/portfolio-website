import datetime
import json
import urllib.parse
import urllib.request
from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from .models import HomeSection, AboutSection, Project, ProjectCategory, Skill, SkillCategory, Service, Experience, Education, Certificate, Recommendation, ContactSection
from general.models import GeneralSettings


def _verify_turnstile(token, remote_ip):
    if not token:
        return False
    try:
        data = urllib.parse.urlencode({
            "secret": settings.TURNSTILE_SECRET_KEY,
            "response": token,
            "remoteip": remote_ip,
        }).encode()
        with urllib.request.urlopen(
            urllib.request.Request(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                data=data,
            ),
            timeout=5,
        ) as resp:
            return json.loads(resp.read()).get("success", False)
    except Exception:
        return True  # fail open if Cloudflare is unreachable


def _total_experience_label(experiences):
    today = datetime.date.today()
    total_months = 0
    for exp in experiences:
        start = datetime.date(exp.start_year, exp.start_month, 1)
        end = datetime.date(exp.end_year, exp.end_month, 1) if (exp.end_year and exp.end_month) else today
        total_months += max((end.year - start.year) * 12 + (end.month - start.month) + 1, 0)
    if not total_months:
        return ""
    years, months = divmod(total_months, 12)
    parts = []
    if years:
        parts.append(f"{years} yr{'s' if years > 1 else ''}")
    if months:
        parts.append(f"{months} mo")
    return " ".join(parts)


def home(request):
    home = HomeSection.get()
    context = {
        "home": home,
        "about": AboutSection.get(),
        "projects": Project.objects.select_related("category", "linked_experience", "linked_education").order_by(
            F("end_year").desc(nulls_first=True),
            F("end_month").desc(nulls_first=True),
        ),
        "project_categories": ProjectCategory.objects.order_by('name'),
        "skill_categories": SkillCategory.objects.prefetch_related("skills").all(),
        "recommendations": Recommendation.objects.all(),
        "contact": ContactSection.get(),
        "general": GeneralSettings.get(),
        "experiences": Experience.objects.prefetch_related("projects__category").all(),
        "total_experience": _total_experience_label(Experience.objects.all()),
        "educations": Education.objects.prefetch_related("projects__category").all(),
        "certificates": Certificate.objects.all(),
        "tech_chips": [c.strip() for c in home.tech_chips.split(",") if c.strip()],
        "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
    }
    return render(request, "core/index.html", context)


@csrf_exempt
def contact_submit(request):
    import logging
    log = logging.getLogger(__name__)
    if request.method != "POST":
        return JsonResponse({"ok": False, "msg": "Method not allowed."}, status=405)
    try:
        token = request.POST.get("cf-turnstile-response", "")
        if not _verify_turnstile(token, request.META.get("REMOTE_ADDR", "")):
            return JsonResponse({"ok": False, "msg": "Security check failed. Please try again."})
        name    = request.POST.get("name", "")
        email   = request.POST.get("email", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")
        general  = GeneralSettings.get()
        logo_url = general.favicon.url if general.favicon else None
        site_url = request.build_absolute_uri('/').rstrip('/')
        html_body = render_to_string('email/contact_notification.html', {
            'sender_name':  name,
            'sender_email': email,
            'subject':      subject,
            'message':      message,
            'logo_url':     logo_url,
            'site_url':     site_url,
        })
        msg = EmailMultiAlternatives(
            subject=f"[Portfolio Contact] {subject}",
            body=f"From: {name} <{email}>\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL] if settings.CONTACT_EMAIL else [],
            reply_to=[f"{name} <{email}>"],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
    except Exception as exc:
        log.error("Contact form error: %s", exc, exc_info=True)
        return JsonResponse({"ok": False, "msg": f"Error: {exc}"})
    return JsonResponse({"ok": True})


def portfolio_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "core/portfolio_detail.html", {
        "project": project,
        "general": GeneralSettings.get(),
    })
