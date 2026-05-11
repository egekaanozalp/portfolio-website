import datetime
from django.db import models

MONTH_CHOICES = [
    (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
    (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
    (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December'),
]
_MONTH_ABBR = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def _current_year():
    return datetime.date.today().year

def _fmt_month_year(month, year):
    return f"{_MONTH_ABBR[month - 1]} {year}"

def _calc_duration(start_year, start_month, end_year, end_month):
    start = datetime.date(start_year, start_month, 1)
    end = datetime.date(end_year, end_month, 1) if (end_year and end_month) else datetime.date.today()
    total_months = (end.year - start.year) * 12 + (end.month - start.month) + 1
    if total_months < 1:
        return "< 1 mo"
    years, months = divmod(total_months, 12)
    parts = []
    if years:
        parts.append(f"{years} yr{'s' if years > 1 else ''}")
    if months:
        parts.append(f"{months} mo")
    return " · ".join(parts)


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


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("in_progress", "In Progress"),
        ("archived", "Archived"),
    ]

    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    title = models.CharField(max_length=200)
    short_description = models.CharField(
        max_length=300, blank=True, default="",
        help_text="Brief summary shown on the portfolio card.",
    )
    description = models.TextField(blank=True, default="", help_text="Full description for the project detail page.")
    image = models.ImageField(upload_to="portfolio/")
    featured = models.BooleanField(default=False, help_text="Pin to the top of the portfolio.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="completed")

    # Detail page
    tech_stack = models.CharField(
        max_length=500, blank=True, default="",
        verbose_name="Tech stack",
        help_text="Comma-separated technologies, e.g. Python,Django,React",
    )
    live_url = models.URLField(blank=True, verbose_name="Live URL", help_text="Link to the deployed project.")
    github_url = models.URLField(blank=True, verbose_name="GitHub URL", help_text="Link to the source code repository.")
    role = models.CharField(max_length=200, blank=True, default="", help_text="Your role, e.g. Full Stack Developer.")
    highlights = models.TextField(blank=True, default="", help_text="Key features or highlights, one per line.")

    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class SkillCategory(models.Model):
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]


class Skill(models.Model):
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name="skills",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=3, choices=RATING_CHOICES)
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


class Experience(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Software Engineer")
    company = models.CharField(max_length=200)
    start_month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, default=1, verbose_name="Start month")
    start_year = models.PositiveIntegerField(default=_current_year, verbose_name="Start year")
    end_month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, null=True, blank=True, verbose_name="End month")
    end_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="End year", help_text="Leave blank for 'Present'")
    description = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="resume/experience/", blank=True)
    order = models.PositiveIntegerField(default=0)

    @property
    def period(self):
        start = _fmt_month_year(self.start_month, self.start_year)
        end = _fmt_month_year(self.end_month, self.end_year) if (self.end_year and self.end_month) else "Present"
        return f"{start} – {end}"

    @property
    def duration(self):
        return _calc_duration(self.start_year, self.start_month, self.end_year, self.end_month)

    class Meta:
        ordering = ["order"]
        verbose_name = "Experience"
        verbose_name_plural = "Experience"

    def __str__(self):
        return f"{self.title} @ {self.company}"


class Education(models.Model):
    degree = models.CharField(max_length=200, help_text="e.g. B.Sc. Computer Science")
    institution = models.CharField(max_length=200)
    start_month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, default=9, verbose_name="Start month")
    start_year = models.PositiveIntegerField(default=_current_year, verbose_name="Start year")
    end_month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, null=True, blank=True, verbose_name="End month")
    end_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="End year", help_text="Leave blank for 'Present'")
    description = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="resume/education/", blank=True)
    order = models.PositiveIntegerField(default=0)

    @property
    def period(self):
        start = _fmt_month_year(self.start_month, self.start_year)
        end = _fmt_month_year(self.end_month, self.end_year) if (self.end_year and self.end_month) else "Present"
        return f"{start} – {end}"

    @property
    def duration(self):
        return _calc_duration(self.start_year, self.start_month, self.end_year, self.end_month)

    class Meta:
        ordering = ["order"]
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} – {self.institution}"


class Certificate(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, default=1, verbose_name="Issue month")
    issue_year = models.PositiveIntegerField(default=_current_year, verbose_name="Issue year")
    url = models.URLField(blank=True, help_text="Link to the certificate (optional)")
    credential_id = models.CharField(max_length=200, blank=True, help_text="Unique identifier issued by the organization (shown as 'Credential ID' on LinkedIn).")
    image = models.ImageField(upload_to="resume/certificates/", blank=True, help_text="The logo of the issuer.")
    order = models.PositiveIntegerField(default=0)

    @property
    def date(self):
        return _fmt_month_year(self.issue_month, self.issue_year)

    class Meta:
        ordering = ["order"]
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"

    def __str__(self):
        return f"{self.name} – {self.issuer}"


