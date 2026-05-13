from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import HomeSection, AboutSection, Project, ProjectCategory, Skill, SkillCategory, Service, Experience, Education, Certificate, Recommendation, ContactSection


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


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Profile Card", {
            "fields": ["profile_image", "name", "title", "email", "phone", "location"],
        }),
        ("About Text", {
            "fields": ["badge_text", "heading", "description"],
        }),
        ("Stats", {
            "description": "Leave the number blank to hide a stat.",
            "fields": [
                "stat1_number", "stat1_label",
                "stat2_number", "stat2_label",
                "stat3_number", "stat3_label",
            ],
        }),
        ("Info Grid", {
            "description": "Up to 6 custom rows shown in the info grid. Leave both fields blank to hide a row.",
            "fields": [
                ("info1_label", "info1_value"),
                ("info2_label", "info2_value"),
                ("info3_label", "info3_value"),
                ("info4_label", "info4_value"),
                ("info5_label", "info5_value"),
                ("info6_label", "info6_value"),
            ],
        }),
        ("Call to Action", {
            "fields": ["resume_url"],
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


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0
    fields = ["title", "status", "featured", "order"]
    readonly_fields = ["title", "status", "featured", "order"]
    show_change_link = True
    can_delete = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]
    inlines = [ProjectInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Card", {
            "fields": ["category", "title", "image", "featured", "status", "order"],
        }),
        ("Institution", {
            "description": "Link to a company (Experience) or school (Education) from your resume. Select at most one.",
            "fields": ["linked_experience", "linked_education"],
        }),
        ("Duration", {
            "description": "Leave End year blank to show 'Present'.",
            "fields": [("start_month", "start_year"), ("end_month", "end_year")],
        }),
        ("Detail Page", {
            "fields": ["description", "tech_stack", "role", "highlights", "live_url", "github_url"],
        }),
    ]
    list_display = ["title", "category", "institution_name", "status", "order"]
    list_filter = ["category", "status", "linked_experience", "linked_education"]
    search_fields = ["title", "linked_experience__company", "linked_education__institution"]


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ["name", "rating", "order"]


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "rating", "order"]
    list_editable = ["order", "rating"]
    list_filter = ["category"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "order"]
    list_editable = ["order"]


@admin.register(ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Info Card", {
            "fields": ["info_heading", "tagline", "email", "phone", "location"],
        }),
        ("Social Links", {
            "description": "Leave blank to hide.",
            "fields": ["linkedin_url", "github_url", "twitter_url"],
        }),
        ("Form", {
            "fields": ["form_heading"],
        }),
    ]

    def has_add_permission(self, request):
        return not ContactSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = ContactSection.get()
        return HttpResponseRedirect(
            reverse("admin:core_contactsection_change", args=[obj.pk])
        )


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "role", "company", "order"]
    list_editable = ["order"]
    fieldsets = [
        ("Person", {
            "fields": ["profile_image", "first_name", "last_name", "role", "company"],
        }),
        ("Content", {
            "fields": ["quote", "order"],
        }),
    ]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "order"]
    list_editable = ["order"]
    fieldsets = [
        (None, {
            "fields": ["title", "company", "image", "order"],
        }),
        ("Duration", {
            "description": "Leave End year blank to show 'Present'. Duration is calculated automatically.",
            "fields": [("start_month", "start_year"), ("end_month", "end_year")],
        }),
        ("Description", {
            "description": "Optional details about the role.",
            "fields": ["description"],
        }),
    ]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution", "order"]
    list_editable = ["order"]
    fieldsets = [
        (None, {
            "fields": ["degree", "institution", "image", "order"],
        }),
        ("Duration", {
            "description": "Leave End year blank to show 'Present'. Duration is calculated automatically.",
            "fields": [("start_month", "start_year"), ("end_month", "end_year")],
        }),
        ("Description", {
            "description": "Optional notes about the program, thesis, honours, etc.",
            "fields": ["description"],
        }),
    ]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ["name", "issuer", "order"]
    list_editable = ["order"]
    fieldsets = [
        (None, {
            "fields": ["name", "issuer", ("issue_month", "issue_year"), "url", "credential_id", "image", "order"],
        }),
    ]
