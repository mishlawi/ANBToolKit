import pytest

from anbtk import dataControl


@pytest.fixture
def initialized_notebook(tmp_path, monkeypatch):
    root = tmp_path / "notebook"
    root.mkdir()
    monkeypatch.chdir(root)
    dataControl.initanb()
    return root
