# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests that build the test-example-index site through the Sphinx CLI
in order to fully run the build-finished events.
"""

import os
import re
import shutil
from typing import TYPE_CHECKING

import pytest
import sphinx
from sphinx.cmd.build import build_main

from tests.utils import (
    Build,
    parse_example_page,
    contains_href,
    contains_external_href,
    contains_linked_img,
)

if TYPE_CHECKING:
    from _pytest.tmpdir import TempdirFactory
    from sphinx.testing.path import path

sphinx_version = sphinx.version_info[:2]

NO_SPHINX_17_MESSAGE = (
    "Example contains download role with external URL that is not "
    "supported by Sphinx 1.7."
)


@pytest.fixture(scope="session")
def example_index_build(
    tmpdir_factory: "TempdirFactory", casesdir: "path"
) -> Build:
    """Test fixture that builds the example-index test case with a
    parallelized build.
    """
    case_dir = str(casesdir / "test-example-index")
    src_dir = str(tmpdir_factory.mktemp("example-index").join("docs"))
    shutil.copytree(case_dir, src_dir)

    argv = ["-j 4", "-W", "-b", "html", src_dir, "_build/html"]

    start_dir = os.path.abspath(".")
    try:
        os.chdir(src_dir)
        status = build_main(argv=argv)
    finally:
        os.chdir(start_dir)
    assert status == 0

    return Build(
        src_dir=src_dir,
        build_dir=os.path.join(src_dir, "_build/html"),
        status=status,
    )


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_example_gallery_build(example_index_build: Build) -> None:
    """Test the overall build status code for the example-index case."""
    assert example_index_build.status == 0


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_api_link(example_index_build: Build) -> None:
    """Test that internal API links work, with the api-link example."""
    tree = parse_example_page(example_index_build.build_dir, "api-link")
    assert contains_href(tree, "../index.html#sphinx_example_index.setup")


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_ref_link(example_index_build: Build) -> None:
    """The ref-link example has an example of a link made with the ref role.
    """
    tree = parse_example_page(example_index_build.build_dir, "ref-link")
    assert contains_href(tree, "../index.html#api")


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_doc_link(example_index_build: Build) -> None:
    """The doc-link example has a doc role for making a link to another page.
    """
    tree = parse_example_page(example_index_build.build_dir, "doc-link")
    assert contains_href(tree, "../page-with-examples.html")


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_intersphinx_ref_link(example_index_build: Build) -> None:
    """The intersphinx-ref-link example has a ref role to the Astropy
    docs with intersphinx
    """
    tree = parse_example_page(
        example_index_build.build_dir, "intersphinx-ref-link"
    )
    assert contains_external_href(
        tree, "https://docs.astropy.org/en/stable/wcs/index.html#astropy-wcs",
    )


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_intersphinx_api_link(example_index_build: Build) -> None:
    """The intersphinx-api-link example has a ref role to the Astropy
    docs with intersphinx.
    """
    tree = parse_example_page(
        example_index_build.build_dir, "intersphinx-api-link"
    )
    expected_href = (
        "https://docs.astropy.org/en/stable/api/astropy.table.Table.html"
        "#astropy.table.Table"
    )
    assert contains_external_href(tree, expected_href)


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_header_reference_target(example_index_build: Build) -> None:
    """The header-reference-target-example example has an example of a ref
    link to a target on a header that's also part of the example content.
    This shows that the link ends up pointing back to the original.
    """
    tree = parse_example_page(
        example_index_build.build_dir, "header-reference-target-example"
    )
    # ref link inside the scope of the example
    assert contains_href(tree, "#section-target")
    # ref link outside the scope of the example
    assert contains_href(tree, "../ref-targets.html#section-2-target")


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_named_equation(example_index_build: Build) -> None:
    """The named-equation example has an example of an equation with a
    label, and a reference to that label.
    This shows that the link points back to the original equation.
    """
    tree = parse_example_page(example_index_build.build_dir, "named-equation")
    assert contains_href(tree, "#equation-euler")


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_example_with_an_image(example_index_build: Build) -> None:
    """A regular image directive with a relative URI to a local image."""
    tree = parse_example_page(
        example_index_build.build_dir, "example-with-an-image"
    )
    assert contains_linked_img(tree, "../_images/astropy_project_logo.svg")


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_example_with_an_external_image(example_index_build: Build) -> None:
    """A regular image directive with an external URI."""
    tree = parse_example_page(
        example_index_build.build_dir, "example-with-an-external-image"
    )
    assert contains_linked_img(
        tree, "https://www.astropy.org/images/astropy_project_logo.svg"
    )


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_example_with_a_figure(example_index_build: Build) -> None:
    """A figure directive with a relative URI to a local image."""
    tree = parse_example_page(
        example_index_build.build_dir, "example-with-a-figure"
    )
    assert contains_linked_img(tree, "../_images/astropy_project_logo.svg")


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_example_with_an_external_figure(example_index_build: Build) -> None:
    """A figure directive with a external image URI."""
    tree = parse_example_page(
        example_index_build.build_dir, "example-with-an-external-figure"
    )
    assert contains_linked_img(
        tree, "https://www.astropy.org/images/astropy_project_logo.svg"
    )


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_matplotlib_plot(example_index_build: Build) -> None:
    """A matplotlib-based plot directive."""
    tree = parse_example_page(example_index_build.build_dir, "matplotlib-plot")
    assert contains_external_href(tree, "../matplotlib-1.py")
    assert contains_external_href(tree, "../matplotlib-1.png")
    assert contains_external_href(tree, "../matplotlib-1.hires.png")
    assert contains_external_href(tree, "../matplotlib-1.pdf")

    img_tag = tree.select(".body img")[0]
    assert img_tag["src"] == "../_images/matplotlib-1.png"


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_file_download_example(example_index_build: Build) -> None:
    """Test the link made by a download directive to a file hosted on the
    site itself.
    """
    tree = parse_example_page(
        example_index_build.build_dir, "file-download-example"
    )
    for tag in tree.select(".body a.reference.download.internal"):
        match = re.match(r"../_downloads/[a-z0-9]+/hello\.py", tag["href"])
        if match is not None:
            return
    assert False  # link was not found


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_absolute_file_download_example(example_index_build: Build) -> None:
    """Test an absolute link to a file hosted on the site, made with a download
    directive.
    """
    tree = parse_example_page(
        example_index_build.build_dir, "absolute-file-download-example"
    )
    for tag in tree.select(".body a.reference.download.internal"):
        match = re.match(
            r"../_downloads/[a-z0-9]+/astropy_project_logo\.svg", tag["href"]
        )
        if match is not None:
            return
    assert False  # link was not found


@pytest.mark.skipif(sphinx_version <= (1, 7), reason=NO_SPHINX_17_MESSAGE)
def test_external_file_download_example(example_index_build: Build) -> None:
    """Test an absolute link to a file hosted on the site, made with a download
    directive.
    """
    tree = parse_example_page(
        example_index_build.build_dir, "external-file-download-example"
    )
    expected_href = (
        "https://raw.githubusercontent.com/astropy/astropy/master/README.rst"
    )
    for tag in tree.select(".body a.reference.download.external"):
        if tag["href"] == expected_href:
            return
    assert False  # link was not found
