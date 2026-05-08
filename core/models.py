from django.db import models


class HomeSection(models.Model):
    # Identity
    title = models.CharField(max_length=200, blank=True, default="", help_text="Large heading, e.g. 'My Portfolio'")
    name = models.CharField(max_length=100, default="Your Name")
    typed_items = models.CharField(
        max_length=500,
        default="Developer,Designer,Engineer",
        help_text="Comma-separated list for the animated typing effect, e.g. Developer,Designer,Engineer",
    )
    description = models.TextField(blank=True, default="")
    profile_image = models.ImageField(upload_to="home/", blank=True)

    # Call-to-action buttons
    cta_primary_text = models.CharField(max_length=50, default="View My Work")
    cta_primary_url = models.CharField(max_length=200, default="#portfolio")
    cta_secondary_text = models.CharField(max_length=50, default="Get In Touch")
    cta_secondary_url = models.CharField(max_length=200, default="#contact")

    # Social links (leave blank to hide)
    social_github = models.URLField(blank=True, verbose_name="GitHub URL")
    social_linkedin = models.URLField(blank=True, verbose_name="LinkedIn URL")
    social_twitter = models.URLField(blank=True, verbose_name="Twitter / X URL")
    social_instagram = models.URLField(blank=True, verbose_name="Instagram URL")
    social_facebook = models.URLField(blank=True, verbose_name="Facebook URL")

    class Meta:
        verbose_name = "Home Section"
        verbose_name_plural = "Home Section"

    def __str__(self):
        return "Home Section"

    def save(self, *args, **kwargs):
        # Enforce singleton — always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="portfolio/")
    url = models.URLField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Bootstrap icon class, e.g. bi-code-slash")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
