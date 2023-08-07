import pytest
import os
import yaml
from src.monitor import add_file_to_config, remove_file_from_config, validate_yaml


@pytest.fixture
def config_fixture():
    test_config = "test_config.yaml"
    with open(test_config, "w") as file:
        yaml.safe_dump({"files": []}, file)

    yield test_config

    # Teardown
    os.remove(test_config)


def test_add_file_to_config(config_fixture):
    test_file = "test_file.txt"
    test_file = os.path.abspath(test_file)
    open(test_file, "a").close()  # Create an empty file for testing

    add_file_to_config(test_file, config_fixture)

    with open(config_fixture, "r") as file:
        config = yaml.safe_load(file)

    assert test_file in config["files"]

    os.remove(test_file)  # Cleanup the test file


def test_remove_file_from_config(config_fixture):
    test_file = "test_file_to_remove.txt"
    test_file = os.path.abspath(test_file)
    with open(config_fixture, "a") as file:
        yaml.safe_dump({"files": [test_file]}, file)

    remove_file_from_config(test_file, config_fixture)

    with open(config_fixture, "r") as file:
        config = yaml.safe_load(file)

    assert test_file not in config["files"]


def test_validate_yaml_valid(config_fixture):
    assert validate_yaml(config_fixture) == True


def test_validate_yaml_invalid():
    invalid_config = "invalid_config.yaml"
    with open(invalid_config, "w") as file:
        file.write("not_a_list: 'hello'")

    assert validate_yaml(invalid_config) == False

    os.remove(invalid_config)  # Cleanup
