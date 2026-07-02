from tutor import hooks

print("🔥 tutor_catalog_extensions plugin LOADED")

# Register the Django app with Discovery.
hooks.Filters.ENV_PATCHES.add_item(
    (
        "discovery-common-settings",
        """
if "catalog_extensions" not in INSTALLED_APPS:
    INSTALLED_APPS.append("catalog_extensions")
""",
    )
)
