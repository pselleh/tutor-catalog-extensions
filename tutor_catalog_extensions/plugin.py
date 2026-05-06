from tutor import hooks

hooks.Filters.CONFIG_DEFAULTS.add_items([
    (
        "DISCOVERY_EXTRA_PIP_PACKAGES",
        "git+https://github.com/pselleh/catalog-extensions.git@main",
    ),
])

hooks.Filters.ENV_PATCHES.add_item((
    "discovery-production-settings",
    """
INSTALLED_APPS.append("cba_catalog_extensions.apps.CbaCatalogExtensionsConfig")
"""
))
