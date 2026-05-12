import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F
from .models import HomeSection, AboutSection, Project, ProjectCategory, Skill, SkillCategory, Service, Experience, Education, Certificate, Recommendation


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
    if request.method == "POST" and request.POST.get("contact_form"):
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")
        send_mail(
            subject=f"[Portfolio Contact] {subject}",
            message=f"From: {name} <{email}>\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, "DEFAULT_FROM_EMAIL") else email,
            recipient_list=[settings.CONTACT_EMAIL] if hasattr(settings, "CONTACT_EMAIL") else [],
            fail_silently=True,
        )
        messages.success(request, "Your message has been sent. Thank you!")
        return redirect("home")

    home = HomeSection.get()
    context = {
        "home": home,
        "about": AboutSection.get(),
        "projects": Project.objects.select_related("category").order_by(
            F("end_year").desc(nulls_first=True),
            F("end_month").desc(nulls_first=True),
        ),
        "project_categories": ProjectCategory.objects.order_by('name'),
        "skill_categories": SkillCategory.objects.prefetch_related("skills").all(),
        "recommendations": Recommendation.objects.all(),
        "experiences": Experience.objects.all(),
        "total_experience": _total_experience_label(Experience.objects.all()),
        "educations": Education.objects.all(),
        "certificates": Certificate.objects.all(),
        "tech_chips": [c.strip() for c in home.tech_chips.split(",") if c.strip()],
    }
    return render(request, "core/index.html", context)


def portfolio_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "core/portfolio_detail.html", {"project": project})
