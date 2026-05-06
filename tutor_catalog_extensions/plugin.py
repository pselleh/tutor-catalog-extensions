print("🔥 catalog_extensions plugin LOADED")

from tutor import hooks

# 1. Register Django app
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-common-settings",
    """
INSTALLED_APPS.append("cba_catalog_extensions")
"""
))

# 2. Register URLs safely (avoid duplicate injection)
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-root-urlconf",
    """
from django.urls import include, path

if not any("cba_catalog_extensions.urls" in str(p) for p in urlpatterns):
    urlpatterns += [
        path("api/catalog/", include("cba_catalog_extensions.urls")),
    ]
"""
))
