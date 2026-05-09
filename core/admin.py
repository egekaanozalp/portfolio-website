from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import HomeSection, AboutSection, Project, Skill, Service


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Identity", {
            "fields": ["title", "name", "typed_items", "description", "profile_image"],
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


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Profile Card", {
            "fields": ["profile_image", "name", "title", "email", "phone", "location"],
        }),
        ("Content", {
            "fields": ["badge_text", "heading", "description", "resume_url"],
        }),
        ("Stats", {
            "description": "Leave a number blank to hide that stat.",
            "fields": [
                ("stat1_number", "stat1_label"),
                ("stat2_number", "stat2_label"),
                ("stat3_number", "stat3_label"),
            ],
        }),
        ("Detail Grid", {
            "description": "Leave a label blank to hide that row.",
            "fields": [
                ("detail1_label", "detail1_value"),
                ("detail2_label", "detail2_value"),
                ("detail3_label", "detail3_value"),
                ("detail4_label", "detail4_value"),
            ],
        }),
    ]

    def has_add_permission(self, request):
        return not AboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = AboutSection.get()
        return HttpResponseRedirect(
            reverse("admin:core_aboutsection_change", args=[obj.pk])
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
