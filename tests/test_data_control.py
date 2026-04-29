import json

import pytest

from anbtk import dataControl


def test_get_notebook_paths_resolves_from_nested_directory(initialized_notebook, monkeypatch):
    nested = initialized_notebook / "branch" / "child"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)

    paths = dataControl.get_notebook_paths()

    assert paths is not None
    assert paths.root == initialized_notebook
    assert paths.anbtk == initialized_notebook / ".anbtk"


def test_require_notebook_paths_raises_outside_notebook(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(FileNotFoundError, match="Not inside an initialized Ancestors Notebook."):
        dataControl.require_notebook_paths()


def test_initanb_creates_expected_structure_and_seed_files(initialized_notebook):
    anbtk_dir = initialized_notebook / ".anbtk"

    assert anbtk_dir.is_dir()
    assert (anbtk_dir / "fsgram.anb").is_file()
    assert (anbtk_dir / "anbtk.json").is_file()
    assert (anbtk_dir / "templates" / "anb1.j2").is_file()
    assert (anbtk_dir / "templates" / "anb2.j2").is_file()

    with open(anbtk_dir / "anbtk.json", "r") as handle:
        data = json.load(handle)

    assert data == {"Story": 0, "Biography": 0, "Picture": 0}


def test_relative_to_anbtk_returns_project_relative_path(initialized_notebook, monkeypatch):
    nested = initialized_notebook / "branch"
    nested.mkdir()
    target = nested / "story.dgu"
    target.write_text("---\n---\n")
    monkeypatch.chdir(nested)

    relative = dataControl.relative_to_anbtk(target)

    assert relative == "branch/story.dgu"


def test_data_update_increments_ids_for_known_entities(initialized_notebook, monkeypatch):
    monkeypatch.chdir(initialized_notebook)

    first_story_id = dataControl.dataUpdate("Story", "my-story")
    second_story_id = dataControl.dataUpdate("Story", "my-other-story")
    biography_id = dataControl.dataUpdate("Biography", "alice")

    with open(initialized_notebook / ".anbtk" / "anbtk.json", "r") as handle:
        data = json.load(handle)

    assert first_story_id == "h[1]-my-story"
    assert second_story_id == "h[2]-my-other-story"
    assert biography_id == "b[1]-alice"
    assert data["Story"] == 2
    assert data["Biography"] == 1
