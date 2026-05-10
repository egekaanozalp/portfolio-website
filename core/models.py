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

    # ID Badge card fields
    card_first_name = models.CharField(max_length=100, blank=True, default="", verbose_name="First name")
    card_last_name = models.CharField(max_length=100, blank=True, default="", verbose_name="Last name")
    card_role = models.CharField(max_length=100, blank=True, default="", verbose_name="Role / Title", help_text="e.g. Software Engineer")
    card_email = models.EmailField(blank=True, default="", verbose_name="Contact email")

    # Tech stack chips
    tech_chips = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="Tech stack chips",
        help_text="Comma-separated labels shown as tags, e.g. Python,Django,React",
    )

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


class AboutSection(models.Model):
    # Profile card
    profile_image = models.ImageField(upload_to="about/", blank=True)
    name = models.CharField(max_length=100, blank=True, default="")
    title = models.CharField(max_length=100, blank=True, default="", verbose_name="Title / Role")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    location = models.CharField(max_length=100, blank=True, default="")

    # About text
    badge_text = models.CharField(max_length=60, blank=True, default="Get to Know Me")
    heading = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")

    # Stats — leave number blank to hide
    stat1_number = models.CharField(max_length=20, blank=True, default="", verbose_name="Stat 1 number", help_text="e.g. 10+")
    stat1_label  = models.CharField(max_length=50,  blank=True, default="", verbose_name="Stat 1 label",  help_text="e.g. Projects Completed")
    stat2_number = models.CharField(max_length=20, blank=True, default="", verbose_name="Stat 2 number")
    stat2_label  = models.CharField(max_length=50,  blank=True, default="", verbose_name="Stat 2 label")
    stat3_number = models.CharField(max_length=20, blank=True, default="", verbose_name="Stat 3 number")
    stat3_label  = models.CharField(max_length=50,  blank=True, default="", verbose_name="Stat 3 label")

    # Info grid — up to 6 custom label/value pairs; leave both blank to hide a row
    info1_label = models.CharField(max_length=100, blank=True, default="", verbose_name="Item 1 label")
    info1_value = models.CharField(max_length=200, blank=True, default="", verbose_name="Item 1 value")
    info2_label = models.CharField(max_length=100, blank=True, default="", verbose_name="Item 2 label")
    info2_value = models.CharField(max_length=200, blank=True, default="", verbose_name="Item 2 value")
    info3_label = models.CharField(max_length=100, blank=True, default="", verbose_name="Item 3 label")
    info3_value = models.CharField(max_length=200, blank=True, default="", verbose_name="Item 3 value")
    info4_label = models.CharField(max_length=100, blank=True, default="", verbose_name="Item 4 label")
    info4_value = models.CharField(max_length=200, blank=True, default="", verbose_name="Item 4 value")
    info5_label = models.CharField(max_length=100, blank=True, default="", verbose_name="Item 5 label")
    info5_value = models.CharField(max_length=200, blank=True, default="", verbose_name="Item 5 value")
    info6_label = models.CharField(max_length=100, blank=True, default="", verbose_name="Item 6 label")
    info6_value = models.CharField(max_length=200, blank=True, default="", verbose_name="Item 6 value")

    @property
    def info_items(self):
        pairs = [
            (self.info1_label, self.info1_value),
            (self.info2_label, self.info2_value),
            (self.info3_label, self.info3_value),
            (self.info4_label, self.info4_value),
            (self.info5_label, self.info5_value),
            (self.info6_label, self.info6_value),
        ]
        return [(l, v) for l, v in pairs if l and v]

    # Resume download
    resume_url = models.CharField(max_length=200, blank=True, default="#", verbose_name="Resume URL", help_text="URL or path to downloadable resume file")

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


