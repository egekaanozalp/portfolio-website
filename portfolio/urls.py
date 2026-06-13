from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, HttpResponseRedirect
from general.models import GeneralSettings


def favicon_redirect(request):
    general = GeneralSettings.get()
    if general.favicon:
        return HttpResponseRedirect(general.favicon.url)
    return HttpResponseRedirect(settings.STATIC_URL + "img/favicon.png")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.ico", favicon_redirect),
    path("robots.txt", lambda request: HttpResponse(
        "User-agent: *\nAllow: /\n", content_type="text/plain"
    )),
    path("ping", lambda request: HttpResponse("ok", content_type="text/plain"), name="ping"),
    path("", include("core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
