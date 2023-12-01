"""Test the scanning functionality."""

from pathlib import Path

import pytest

from bumpver.scan import scan_file, scan_filetree
from bumpver.tests.mock_file_data import MOCK_FILES, FileDetails


@pytest.mark.parametrize(
    "mock_file",
    [pytest.param(mock_file, id=key) for key, mock_file in MOCK_FILES.items()],
)
def test_file_scan(mock_file: FileDetails, tmp_path: Path) -> None:
    pyproject_path = tmp_path / mock_file.filename
    pyproject_path.write_text(mock_file.content)

    f = scan_file(pyproject_path)

    assert f is not None
    assert f.file_path == pyproject_path
    assert f.instances == mock_file.instances


def test_subdir_file_scan(tmp_path: Path) -> None:
    p = MOCK_FILES["pyproject"]
    i = MOCK_FILES["init"]

    p_path = tmp_path / p.filename
    p_path.write_text(p.content)

    project_path = tmp_path / "project"
    project_path.mkdir()

    i_path = project_path / i.filename
    i_path.write_text(i.content)

    f = list(scan_filetree(tmp_path))

    assert len(f) == 2  # noqa: PLR2004

    assert f[0].file_path == p_path
    assert f[0].instances == p.instances

    assert f[1].file_path == i_path
    assert f[1].instances == i.instances
