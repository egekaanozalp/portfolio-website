from django.db import models


class GeneralSettings(models.Model):
    favicon = models.ImageField(
        upload_to="general/",
        blank=True,
        help_text="Browser tab icon. A square .png (32×32 or 64×64) works best.",
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
