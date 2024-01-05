from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("agents/", include("apps.agents.urls")),
    path("simulations/", include("apps.simulations.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )
