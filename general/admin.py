from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import GeneralSettings


@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Favicon", {
            "description": "The icon shown in the browser tab. A square .png (32×32 or 64×64) works best.",
            "fields": ["favicon"],
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
