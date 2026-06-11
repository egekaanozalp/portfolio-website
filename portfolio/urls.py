from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping", lambda request: HttpResponse("ok", content_type="text/plain"), name="ping"),
    path("", include("core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
