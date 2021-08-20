from django.contrib import admin
from django.urls import path, include
from django.conf import Settings, settings
from django.conf.urls.static import static

# Tailored for documenting the APi
from rest_framework import permissions
from Api.permissions import IsAuthorOrReadOnly
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Furika Ecommerce API",
        default_version="v1",
        description="Furika Ecommerce API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jmulingwakithome.jmk@gmail.com"),
        license=openapi.License(name="Furika License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("products/", include("Api.urls"), name="store"),
    path("users/", include("Auth.urls"), name="accounts"),
    # for adding auth to the browsable web api
    path("auth/", include("rest_framework.urls")),
    # authentication
    path("auth/", include("dj_rest_auth.urls")),
    # registration specific
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    # Documentation urlpatterns
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
