# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests for the sphinx_example_index.identifiers module."""

import pytest

from sphinx_example_index.identifiers import (
    format_title_to_example_id,
    format_title_to_source_ref_id,
    format_example_id_to_source_ref_id,
)


@pytest.mark.parametrize(
    "title, expected",
    [
        ("Title of an example", "title-of-an-example"),
        # test unicode normalization
        ("Title of an éxample", "title-of-an-example"),
    ],
)
def test_format_title_to_example_id(title: str, expected: str) -> None:
    assert expected == format_title_to_example_id(title)


@pytest.mark.parametrize(
    "title, expected",
    [("Title of an example", "example-src-title-of-an-example")],
)
def test_format_title_to_source_ref_id(title: str, expected: str) -> None:
    assert expected == format_title_to_source_ref_id(title)


@pytest.mark.parametrize(
    "example_id, expected",
    [("title-of-an-example", "example-src-title-of-an-example")],
)
def test_format_example_id_to_source_ref_id(
    example_id: str, expected: str
) -> None:
    assert expected == format_example_id_to_source_ref_id(example_id)
