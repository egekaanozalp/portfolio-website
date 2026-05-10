from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import HomeSection, Project, Skill, Service


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Identity", {
            "fields": ["title", "name", "typed_items", "description", "profile_image"],
        }),
        ("ID Badge Card", {
            "description": "Content shown on the floating ID card on the right side of the hero.",
            "fields": ["card_first_name", "card_last_name", "card_role", "card_email"],
        }),
        ("Tech Stack Chips", {
            "description": "Comma-separated labels shown as tags below the hero text, e.g. Python,Django,React",
            "fields": ["tech_chips"],
        }),
        ("Call-to-Action Buttons", {
            "fields": ["cta_primary_text", "cta_primary_url", "cta_secondary_text", "cta_secondary_url"],
        }),
        ("Social Links", {
            "description": "Leave blank to hide a social link.",
            "fields": ["social_github", "social_linkedin", "social_twitter", "social_instagram", "social_facebook"],
        }),
    ]

    def has_add_permission(self, request):
        return not HomeSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Skip the list and go straight to the single record
        obj = HomeSection.get()
        return HttpResponseRedirect(
            reverse("admin:core_homesection_change", args=[obj.pk])
        )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "order"]
    list_editable = ["order"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "percentage", "order"]
    list_editable = ["order", "percentage"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    list_editable = ["order"]
