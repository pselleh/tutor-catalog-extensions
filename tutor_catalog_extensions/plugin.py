from tutor import hooks

# Register Django app
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-settings",
    """
INSTALLED_APPS += ["catalog_extensions"]
"""
))

# Register URLs
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-urls",
    """
from django.urls import include, path

urlpatterns += [
    path("", include("catalog_extensions.urls")),
]
"""
))
