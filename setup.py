from setuptools import setup, find_packages

setup(
    name="tutor-catalog-extensions",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "tutor.plugin.v1": [
            "tutor_catalog_extensions = tutor_catalog_extensions.plugin",
        ],
    },
)
