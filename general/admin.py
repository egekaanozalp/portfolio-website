from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import GeneralSettings


@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Site Identity", {
            "fields": ["site_name"],
        }),
        ("Favicon", {
            "description": "The icon shown in the browser tab. A square .png (32×32 or 64×64) works best.",
            "fields": ["favicon"],
        }),
        ("Social Preview", {
            "description": "Shown when the site is shared on WhatsApp, Twitter, iMessage, etc. Recommended size: 1200×630 px. Falls back to the favicon if left blank.",
            "fields": ["og_image"],
        }),
    ]

    def has_add_permission(self, request):
        return not GeneralSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = GeneralSettings.get()
        return HttpResponseRedirect(
            reverse("admin:general_generalsettings_change", args=[obj.pk])
        )
