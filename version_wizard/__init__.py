import logging
import os
import re


LOGGER = logging.getLogger(__name__)


def _check_manifest(version_file: str, manifest_file: str = "MANIFEST.in") -> None:
    """
    Check that the manifest file includes the version file.
    """
    with open(manifest_file) as fp:
        if not any(re.match(fr"include\s+{version_file}", line) for line in fp):
            raise RuntimeError(f"manifest file `{manifest_file} does not include `{version_file}; "
                               f"please add `include {version_file}`")


def from_github_tag(default: str = "0.0.0+dev", version_file: str = "VERSION",
                    version_pattern: str = r"\d+\.\d+\.\d+", check_manifest: bool = True,
                    manifest_file: str = "MANIFEST.in") -> str:
    """
    Load the version from the version file if it exists. Otherwise, get the version from a GitHub
    tag reference and write it to the version file.

    Args:
        default: Default version if a github tag reference is not available.
        version_file: File to load the version from or write the version to.
        version_pattern: Pattern of the version to extract from the GitHub tag reference.
        check_manifest: Whether to verify that the `version_file` is included by `manifest_file`.
        manifest_file: File encoding the package manifest.

    Returns:
        The package version.
    """
    if check_manifest:
        _check_manifest(version_file, manifest_file)

    # Load from the file if it exists.
    try:
        with open(version_file) as fp:
            return fp.read().strip()
    except FileNotFoundError:
        LOGGER.info("version file `%s` does not yet exist", version_file)

    # Get the GitHub environment information.
    try:
        ref = os.environ["GITHUB_REF"]
    except KeyError:
        LOGGER.warning("GitHub environment variable `GITHUB_REF` is not set; defaulting to `%s`",
                       default)
        return default

    # Match the version and write it to the file.
    match = re.match(fr"^refs/tags/(?P<version>{version_pattern})$", ref)
    if match:
        version = match.group("version")
        with open(version_file, "w") as fp:
            fp.write(version)
        LOGGER.info("wrote version `%s` to `%s` file", version, version_file)
        return version
    elif re.match(r"^refs/(heads|pull)/", ref):
        LOGGER.info("ref `%s` is not a tag", ref)
    else:
        raise ValueError(f"unexpected reference `{ref}`")
    return default
