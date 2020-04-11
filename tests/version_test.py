"""Tests for the sphinx_example_index.version module."""

from sphinx_example_index.version import version


def test_version() -> None:
    assert isinstance(version, str)
