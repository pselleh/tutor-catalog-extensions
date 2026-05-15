print("🔥 tutor_catalog_extensions plugin LOADED")

from tutor import hooks


# ---------------------------------------------------
# Add catalog_extensions package to Discovery build
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item(
    (
        "private.txt",
        """
-e /openedx/catalog-extensions
""",
    )
)


# ---------------------------------------------------
# Copy package into build context
# ---------------------------------------------------
hooks.Filters.MOUNTED_DIRECTORIES.add_item(
    (
        "openedx",
        "/home/cbaadmin/src/catalog-extensions",
        "/openedx/catalog-extensions",
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

# ---------------------------------------------------
# LMS CSRF / cookie fixes
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        """
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys([
    "https://eadvantage.com",
    "https://apps.eadvantage.com",
    "https://studio.eadvantage.com",
    "https://discovery.eadvantage.com",
]))

SESSION_COOKIE_DOMAIN = ".eadvantage.com"

CSRF_COOKIE_DOMAIN = ".eadvantage.com"

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
""",
    )
)

# ---------------------------------------------------
# LMS CORS fixes
# ---------------------------------------------------
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        """
CORS_ORIGIN_WHITELIST = list(dict.fromkeys([
    "https://eadvantage.com",
    "https://apps.eadvantage.com",
    "https://studio.eadvantage.com",
]))
""",
    )
)
