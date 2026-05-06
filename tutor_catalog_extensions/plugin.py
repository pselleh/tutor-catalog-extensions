print("🔥 catalog_extensions plugin LOADED")

from tutor import hooks


# ---------------------------------------------------
# 1. Register Django app (FIXED NAME)
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-common-settings",
    """
if "catalog_extensions" not in INSTALLED_APPS:
    INSTALLED_APPS.append("catalog_extensions")
"""
))


# ---------------------------------------------------
# 2. Register URLs (FIXED NAME)
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-root-urlconf",
    """
from django.urls import include, path

if not any("catalog_extensions.urls" in str(p) for p in urlpatterns):
    urlpatterns += [
        path("api/catalog/", include("catalog_extensions.urls")),
    ]
"""
))
