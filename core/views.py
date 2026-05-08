from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import HomeSection, Project, Skill, Service


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

    context = {
        "home": HomeSection.get(),
        "projects": Project.objects.all(),
        "skills": Skill.objects.all(),
        "services": Service.objects.all(),
    }
    return render(request, "core/index.html", context)


def portfolio_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "core/portfolio_detail.html", {"project": project})
