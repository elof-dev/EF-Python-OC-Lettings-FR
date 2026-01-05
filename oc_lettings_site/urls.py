"""Module de gestion des URLs pour le site oc_lettings_site"""

from django.contrib import admin
from django.urls import include, path
from . import views

# J'ai conservé l'index de base, l'admin et include délègue les URLs aux applications lettings et
# profiles
urlpatterns = [
    path("", views.index, name="index"),
    path("lettings/", include(("lettings.urls", "lettings"), namespace="lettings")),
    path("profiles/", include(("profiles.urls", "profiles"), namespace="profiles")),
    path("admin/", admin.site.urls),
]
