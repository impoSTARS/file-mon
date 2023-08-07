import pytest
import os
from src.monitor import FileChangeHandler


@pytest.fixture
def revision_files(tmp_path):
    last_revision_file = tmp_path / "last_revision.txt"
    last_revision_file.write_text("line1\nline2\nline3\n")

    current_revision_file = tmp_path / "current_revision.txt"
    current_revision_file.write_text("line3\nline2\nline1\n")

    return str(last_revision_file), str(current_revision_file)


def test_compare_revisions(revision_files, tmp_path):
    last_revision, current_revision = revision_files
    temp_dir = tmp_path

    handler = FileChangeHandler(
        files_to_monitor=[],
        config_file="config_file",
        store_temp=True,
        temp_dir=str(temp_dir),
    )

    # Make sure file paths are absolute
    assert os.path.isabs(last_revision)
    assert os.path.isabs(current_revision)

    file_path = "revision.txt"
    # Assuming the file_path is processed internally, you might want to set up how it is mapped to last_revision and current_revision

    changes = handler.compare_revisions(file_path)

    # Assert the detected changes
    assert changes == [("line1", "line3"), ("line3", "line1")]
