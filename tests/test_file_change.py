import pytest
from src.monitor import FileChangeHandler, start_monitoring
from watchdog.observers import Observer
from loguru import logger
import yaml
import os


def test_file_monitoring(tmp_path):
    # Create temporary files to monitor
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("content")
    file2.write_text("content")

    # Create temporary config.yaml
    config_file = tmp_path / "config.yaml"
    config_content = {"files": [str(file1), str(file2)]}
    config_file.write_text(yaml.dump(config_content))

    # Custom handler to detect file change
    class TestHandler(FileChangeHandler):
        def on_modified(self, event):
            super().on_modified(event)
            if event.src_path == str(file1):
                self.file_modified = True

        def __init__(self, files_to_monitor, config_file):
            super().__init__(files_to_monitor, config_file)
            self.file_modified = False

    observer = Observer()
    event_handler = TestHandler(config_content["files"], str(config_file))
    observer.schedule(event_handler, path=str(tmp_path), recursive=False)
    observer.start()

    # Modify one of the files
    file1.write_text("new content")

    # Wait to allow the observer to detect the change
    observer.join(timeout=2)

    assert event_handler.file_modified, "File modification was not detected"
