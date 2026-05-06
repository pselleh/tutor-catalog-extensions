print("🔥 catalog_extensions plugin LOADED")

from tutor import hooks


# ---------------------------------------------------
# 1. Register Django app
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-common-settings",
    """
if "cba_catalog_extensions" not in INSTALLED_APPS:
    INSTALLED_APPS.append("cba_catalog_extensions")
"""
))


# ---------------------------------------------------
# 2. Register URLs
# ---------------------------------------------------
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


# ---------------------------------------------------
# 3. Install your app into Discovery (CORRECT for Tutor 21)
# ---------------------------------------------------
hooks.Filters.PIP_REQUIREMENTS.add_item((
    "discovery",
    "git+https://github.com/pselleh/catalog-extensions.git"
))
