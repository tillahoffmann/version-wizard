import logging
import os
import pathlib
import pytest
from unittest import mock
from version_wizard import _check_manifest, from_github_tag


def test_get_version_from_file(tmp_path: pathlib.Path) -> None:
    version_file = tmp_path / "MY-VERSION"
    version_file.write_text("test-version")
    assert from_github_tag(check_manifest=False, version_file=version_file) == "test-version"


def test_check_manifest(tmp_path: pathlib.Path) -> None:
    # Check the function directly.
    manifest_file = tmp_path / "SOME-MANIFEST"
    manifest_file.write_text("include MY-VERSION")
    _check_manifest("MY-VERSION", manifest_file)
    with pytest.raises(RuntimeError):
        _check_manifest("OTHER-VERSION", manifest_file)
    # Check by calling `from_github_tag`.
    assert from_github_tag(manifest_file=manifest_file, version_file="MY-VERSION") == "dev"


def test_get_version_from_env(tmp_path: pathlib.Path) -> None:
    version_file = tmp_path / "MY-VERSION"
    with mock.patch.dict(os.environ, {"GITHUB_REF": "refs/tags/1.2.asdf"}):
        assert from_github_tag(version_file=version_file, check_manifest=False,
                               version_pattern=r"\d+\.\d+\.\w+") == "1.2.asdf"
    assert version_file.read_text() == "1.2.asdf"


def test_get_version_from_env_not_a_tag(tmp_path: pathlib.Path, caplog: pytest.LogCaptureFixture) \
        -> None:
    with mock.patch.dict(os.environ, {"GITHUB_REF": "refs/heads/..."}), \
            caplog.at_level(logging.INFO):
        assert from_github_tag(check_manifest=False, version_file=tmp_path / "VERSION") == "dev"
        assert "is not a tag" in caplog.text

    with mock.patch.dict(os.environ, {"GITHUB_REF": "refs/bug/..."}), pytest.raises(ValueError):
        from_github_tag(check_manifest=False, version_file=tmp_path / "VERSION")
