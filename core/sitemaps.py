from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return reverse("portfolio_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.created_at
