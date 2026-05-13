print("🔥 catalog_extensions plugin LOADED")

from tutor import hooks


# ---------------------------------------------------
# Install catalog_extensions into Open edX image
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-dockerfile-post-python-requirements",
        """
COPY ./catalog-extensions /openedx/catalog-extensions

RUN $PIP_COMMAND install -e /openedx/catalog-extensions
""",
    )
)


# ---------------------------------------------------
# Register Django app in Discovery
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item(
    (
        "discovery-common-settings",
        """
if "catalog_extensions" not in INSTALLED_APPS:
    INSTALLED_APPS.append("catalog_extensions")
""",
    )
)


# ---------------------------------------------------
# Register Discovery URLs
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item(
    (
        "discovery-root-urlconf",
        """
from django.conf.urls import include, url

urlpatterns += [
    url(r"^api/catalog/", include("catalog_extensions.urls")),
]
""",
    )
)
