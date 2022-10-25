from setuptools import find_packages, setup
from version_wizard import from_github_tag


with open("README.rst") as fp:
    long_description = fp.read()
    long_description = long_description.replace(".. automodule::",
                                                ".. code-block::\n\n  ..automodule::")

setup(
    name="version-wizard",
    packages=find_packages(),
    version=from_github_tag(),
    extras_require={
        "doc": [
            "sphinx",
        ],
        "test": [
            "flake8",
            "pytest",
            "pytest-cov",
            "twine",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/tillahoffmann/wizard-version/",
    author="Till Hoffmann",
)
