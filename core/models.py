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


class AboutSection(models.Model):
    # Profile card (left column)
    profile_image = models.ImageField(upload_to="about/", blank=True)
    name = models.CharField(max_length=100, default="Your Name")
    title = models.CharField(max_length=200, blank=True, default="", help_text="Subtitle shown below name, e.g. 'Creative Director & Developer'")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")
    location = models.CharField(max_length=200, blank=True, default="")

    # Right column content
    badge_text = models.CharField(max_length=100, blank=True, default="Get to Know Me")
    heading = models.CharField(max_length=300, blank=True, default="Passionate About Creating Digital Experiences")
    description = models.TextField(blank=True, default="")
    resume_url = models.CharField(max_length=200, blank=True, default="#", help_text="Link to downloadable CV/resume file")

    # Stats — leave number blank to hide a stat
    stat1_number = models.CharField(max_length=20, blank=True, default="")
    stat1_label = models.CharField(max_length=100, blank=True, default="")
    stat2_number = models.CharField(max_length=20, blank=True, default="")
    stat2_label = models.CharField(max_length=100, blank=True, default="")
    stat3_number = models.CharField(max_length=20, blank=True, default="")
    stat3_label = models.CharField(max_length=100, blank=True, default="")

    # Detail grid — leave label blank to hide a row
    detail1_label = models.CharField(max_length=100, blank=True, default="")
    detail1_value = models.CharField(max_length=200, blank=True, default="")
    detail2_label = models.CharField(max_length=100, blank=True, default="")
    detail2_value = models.CharField(max_length=200, blank=True, default="")
    detail3_label = models.CharField(max_length=100, blank=True, default="")
    detail3_value = models.CharField(max_length=200, blank=True, default="")
    detail4_label = models.CharField(max_length=100, blank=True, default="")
    detail4_value = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About Section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


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
