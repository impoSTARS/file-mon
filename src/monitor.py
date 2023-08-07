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
    config_path = os.path.relpath("config.yaml", start=os.getcwd())
    with open(config_path, "w") as file:
        yaml.dump({"files": ["/path/to/file"]}, file)
    logger.warning(f"Created an empty config file at {config_path}")
    return config_path


def start_monitoring(config_path: str, observer: Observer):
    """
    Main function to start monitoring
    :param config_path: path to the YAML configuration file
    :param observer: Observer object for

    monitoring files
    """
    config_path = os.path.abspath(config_path)
    if not os.path.exists(config_path):
        config_path = create_empty_config()
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    files_to_monitor = config["files"]
    for file_path in files_to_monitor[:]:
        if not os.path.exists(file_path):
            logger.warning(f"File {file_path} was not found.")
            files_to_monitor.remove(file_path)

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
        default="config.yaml",
        help="Path to the YAML configuration file default:config.yaml",
    )
    args = parser.parse_args()
    start_monitoring(args.config, observer)


if __name__ == "__main__":
    main()
