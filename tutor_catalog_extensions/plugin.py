from tutor import hooks

# Register the Django app in Discovery
hooks.Filters.ENV_PATCHES.add_item(
    (
        "discovery-common-settings",
        """
if "catalog_extensions" not in INSTALLED_APPS:
    INSTALLED_APPS.append("catalog_extensions")
""",
    )
)
