import argparse
import yaml

from loguru import logger
import sys
import time
import os
import traceback
import pwd
import grp

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    logger.info("Install watchdog : pip install watchdog")

DEFAULT_CONF_NAME = "config.yaml"
PATH_DEF_CONF = os.path.abspath(os.path.relpath(DEFAULT_CONF_NAME, start=os.getcwd()))


class FileChangeHandler(FileSystemEventHandler):
    """
    Class to handle file changes
    """

    def on_modified(self, event):
        if event.is_directory:
            return
        if (file_path := event.src_path) in self.files_to_monitor:
            file_stat = os.stat(file_path)

            # Getting the owner and group by UID and GID
            owner_name = pwd.getpwuid(file_stat.st_uid).pw_name
            group_name = grp.getgrgid(file_stat.st_gid).gr_name

            logger.info(
                f"File {file_path} was modified by user {owner_name} of group {group_name}."
            )
        elif event.src_path == self.config_file:
            logger.info("Configuration file changed. Restarting...")
            # Restart the script
            os.execv(sys.executable, ["python"] + sys.argv)

    def __init__(self, files_to_monitor, config_file):
        self.files_to_monitor = files_to_monitor
        self.config_file = config_file


def create_empty_config():
    """
    Create an empty config file and return its absolute path
    """
    config_path = PATH_DEF_CONF
    with open(config_path, "w") as file:
        yaml.dump({"files": [config_path]}, file)
    logger.warning(f"Created an empty config file at {config_path}")
    return config_path


def add_file_to_config(file_path: str, config_path: str = PATH_DEF_CONF):
    """
    Add a file to the configuration file.
    :param file_path: Absolute path to the file to add
    :param config_path: Path to the YAML configuration file
    """
    config_path = os.path.abspath(config_path)
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        logger.error(f"File {file_path} does not exist.")
        return

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    if "files" not in config:
        config["files"] = []

    if file_path not in config["files"]:
        config["files"].append(file_path)

    with open(config_path, "w") as file:
        yaml.safe_dump(config, file)

    logger.info(f"Added {file_path} to {config_path}.")


def validate_yaml(config_path: str = PATH_DEF_CONF):
    """
    Validate the YAML configuration file.
    :param config_path: Path to the YAML configuration file
    """
    config_path = os.path.abspath(config_path)
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        if "files" not in config or not isinstance(config["files"], list):
            logger.error("Invalid config format. 'files' key must be a list.")
            return False

        for file_path in config["files"]:
            if not os.path.exists(file_path):
                logger.warning(f"File {file_path} does not exist.")

        return True

    except yaml.YAMLError as exc:
        logger.error(f"Error in configuration file: {exc}")
        return False


def remove_file_from_config(file_path: str, config_path: str = PATH_DEF_CONF):
    """
    Remove a file from the configuration file.
    :param file_path: Absolute path to the file to delete
    :param config_path: Path to the YAML configuration file
    """
    config_path = os.path.abspath(config_path)
    file_path = os.path.abspath(file_path)

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    if "files" in config and file_path in config["files"]:
        config["files"].remove(file_path)

        with open(config_path, "w") as file:
            yaml.safe_dump(config, file)

        logger.info(f"Deleted {file_path} from {config_path}.")
    else:
        logger.warning(f"{file_path} not found in {config_path}.")


def prepare_config(args, config_path: str = PATH_DEF_CONF):
    """
    Prepares the config, add/ delete file paths, and validate yaml
    """
    # Create config if one does not exists
    config_path = os.path.abspath(config_path)
    if not os.path.exists(config_path):
        config_path = create_empty_config()
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # validate the config
    validate_yaml(config_path=config_path)

    # add if need
    if args.add is not None:
        add_file_to_config(args.add)

    if args.remove is not None:
        if args is not None:
            remove_file_from_config(args.delete)
        elif args.remove is not None:
            remove_file_from_config(args.delete)

    if args.validate is not None:
        validate_yaml(config_path)
    files_to_monitor = config["files"]
    for file_path in files_to_monitor[:]:
        if not os.path.exists(file_path):
            logger.warning(f"File {file_path} was not found.")
            files_to_monitor.remove(file_path)
    return files_to_monitor


def start_monitoring(files_to_monitor, config_path: str, observer: Observer):
    """
    Main function to start monitoring
    :param config_path: path to the YAML configuration file
    :param observer: Observer object for

    monitoring files
    """

    event_handler = FileChangeHandler(files_to_monitor, config_path)

    # Determine unique directories to monitor
    directories_to_monitor = set(
        os.path.dirname(file_path) for file_path in files_to_monitor
    )

    for directory in directories_to_monitor:
        observer.schedule(event_handler, path=directory, recursive=False)

    try:
        observer.start()

    except FileNotFoundError as e:
        logger.critical(
            f"Config File to monitor was not found, check config: {str(config_path)}"
        )
        # logger.info(event_handler.pathtofile)
        logger.debug(traceback.print_exc())
    logger.info("Monitoring started...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    observer = Observer()
    parser = argparse.ArgumentParser(description="File Change Monitor Tool")
    parser.add_argument(
        "--config",
        required=False,
        default=PATH_DEF_CONF,
        help=f"Path to the YAML configuration file default:{PATH_DEF_CONF}",
    )
    parser.add_argument("--add", help="Add a file to the configuration", default=None)
    parser.add_argument(
        "--remove",
        "--delete",
        help="Delete a file from the configuration,",
        default=None,
    )
    # parser.add_argument("--remove", help="Delete a file from the configuration")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the configuration(Also checks if the files exist)",
    )
    args: Namespace | None = parser.parse_args()

    monitor_files = prepare_config(args=args)
    if monitor_files:
        start_monitoring(monitor_files, args.config, observer)


if __name__ == "__main__":
    main()
