print("🔥 catalog_extensions plugin LOADED")

from tutor import hooks


# ---------------------------------------------------
# 1. Register Django app in Discovery settings
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-common-settings",
    """
# Ensure app is only added once
if "cba_catalog_extensions" not in INSTALLED_APPS:
    INSTALLED_APPS.append("cba_catalog_extensions")
"""
))


# ---------------------------------------------------
# 2. Register URLs safely (no duplicates)
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
# 3. Clean old package + install correct app (single step)
# ---------------------------------------------------
hooks.Filters.IMAGES_BUILD.add_item((
    "discovery",
    """
# Remove conflicting legacy package (ignore failure if not present)
RUN pip uninstall -y catalog-extensions || true && \\
    pip install --no-cache-dir git+https://github.com/pselleh/catalog-extensions.git
"""
))
