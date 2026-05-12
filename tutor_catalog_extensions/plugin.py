print("🔥 catalog_extensions plugin LOADED")

from tutor import hooks


# ---------------------------------------------------
# 1. Add local package to openedx image build
# ---------------------------------------------------
hooks.Filters.IMAGES_BUILD.add_item(
    (
        "openedx",
        str("/home/cbaadmin/src/catalog-extensions"),
        "/openedx/catalog-extensions",
    )
)


# ---------------------------------------------------
# 2. Install package requirements
# ---------------------------------------------------
hooks.Filters.OPENEDX_EXTRA_PIP_REQUIREMENTS.add_item(
    "file:///openedx/catalog-extensions"
)


# ---------------------------------------------------
# 3. Register Django app in Discovery
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
# 4. Register Discovery URLs
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
