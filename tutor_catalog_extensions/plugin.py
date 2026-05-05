print("🔥 catalog_extensions plugin LOADED")

from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item((
    "discovery-production-settings",
    """
INSTALLED_APPS.append("catalog_extensions")
"""
))
