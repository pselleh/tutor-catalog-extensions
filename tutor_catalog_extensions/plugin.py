print("🔥 catalog_extensions plugin LOADED")

from tutor import hooks


# ---------------------------------------------------
# 1. Install package into Open edX image
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item((
    "openedx-dockerfile-post-python-requirements",
    """
# Install catalog extensions
COPY ./catalog-extensions /openedx/catalog-extensions
RUN pip install -e /openedx/catalog-extensions
"""
))


# ---------------------------------------------------
# 2. Register Django app
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-common-settings",
    """
if "catalog_extensions" not in INSTALLED_APPS:
    INSTALLED_APPS.append("catalog_extensions")
"""
))


# ---------------------------------------------------
# 3. Register URLs
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item((
    "discovery-root-urlconf",
    """
from django.conf.urls import include, url

urlpatterns += [
    url(r"^api/catalog/", include("catalog_extensions.urls")),
]
"""
))
