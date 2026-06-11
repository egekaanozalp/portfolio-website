from django.db import models


class GeneralSettings(models.Model):
    site_name = models.CharField(
        max_length=100,
        default="Portfolio",
        help_text="Name shown in the browser tab title and page headings.",
    )
    favicon = models.ImageField(
        upload_to="general/",
        blank=True,
        help_text="Browser tab icon. A square .png (32×32 or 64×64) works best.",
    )
    og_image = models.ImageField(
        upload_to="general/",
        blank=True,
        verbose_name="Social preview image (OG image)",
        help_text="Image shown when sharing on WhatsApp, Twitter, etc. Recommended: 1200×630 px. Falls back to the favicon if left blank.",
    )

    class Meta:
        verbose_name = "General Settings"
        verbose_name_plural = "General Settings"

    def __str__(self):
        return "General Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
