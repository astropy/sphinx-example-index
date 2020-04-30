# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests that build the test-example-index site through the Sphinx CLI
in order to fully run the build-finished events.
"""

import os
import shutil
from typing import TYPE_CHECKING

import pytest
import sphinx
from sphinx.cmd.build import build_main

from tests.utils import Build

if TYPE_CHECKING:
    from _pytest.tmpdir import TempdirFactory
    from sphinx.testing.path import path

sphinx_version = sphinx.version_info[:2]


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


@pytest.mark.skipif(
    sphinx_version <= (1, 7),
    reason=(
        "Example contains download role with external URL that is not "
        "supported by Sphinx 1.7."
    ),
)
def test_example_gallery_build(example_index_build: Build) -> None:
    """Test the overall build status code for the example-index case."""
    assert example_index_build.status == 0
