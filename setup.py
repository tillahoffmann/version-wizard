from setuptools import find_packages, setup
from version_wizard import from_github_tag


setup(
    name="version-wizard",
    packages=find_packages(),
    version=from_github_tag(),
    extras_require={
        "test": [
            "flake8",
            "pytest",
            "pytest-cov",
        ],
    }
)
