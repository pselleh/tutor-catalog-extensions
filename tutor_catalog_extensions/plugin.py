print("🔥 catalog_extensions plugin LOADED")

from tutor import hooks

# ✅ Install package in discovery image
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-production-settings",
    """
import subprocess
subprocess.call(["pip", "install", "/openedx/requirements/private.txt"])
"""
))

# ✅ Register Django app
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-production-settings",
    """
INSTALLED_APPS.append("catalog_extensions")
"""
))

# ✅ Add URLs
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-production-settings",
    """
from django.urls import include, path

urlpatterns += [
    path("api/catalog/", include("catalog_extensions.urls")),
]
"""
))
