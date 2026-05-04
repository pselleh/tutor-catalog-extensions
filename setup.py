from setuptools import setup, find_packages

setup(
    name="tutor-catalog-extensions",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "tutor.plugin.v1": [
            "catalog_extensions = tutor_catalog_extensions.plugin",
        ]
    },
)
