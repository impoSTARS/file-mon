# File Monitor

A CLI tool to monitor changes to files. It can watch multiple files and logs any changes to those files. You can specify the files to monitor through a YAML configuration file.

## Installation

```bash
pip install git+https://github.com/impoSTARS/file-mon.git
```
## Usage

### Basic Usage

Monitor files specified in a configuration file:

```bash
filemon 
filemon --add /path/to/file
filemon --config /path/to/pwd/config.yaml
filemon --validate
filemon --remove /path/to/file
sss
as
dossa
some more
```

Add a file:

If the --config option is omitted, the tool will look for a configuration file named `config.yaml` in the current working directory.

## Demo
Here is an example output:
```bash
2023-08-07 11:36:44.289 | INFO     | __main__:start_monitoring:285 - Monitoring started...
2023-08-07 11:36:12.230 | INFO     | __main__:on_modified:108 - change: remote_execution True -> RemoteExecution=False
2023-08-07 11:36:12.231 | INFO     | __main__:on_modified:113 - File /home/umlal/file-mon/README.md was modified by user umlal of group umlal.
```
### Help
```bash
                                                                                            
┌──(venv)─(umlal㉿umlal)-[~/file-mon]
└─$ filemon --add ~/file-mon/README.md -h
usage: filemon [-h] [--config CONFIG] [--add ADD] [--remove REMOVE] [--validate]

File Change Monitor Tool

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the YAML configuration file default:/home/umlal/file-mon/config.yaml
  --add ADD             Add a file to the configuration
  --remove REMOVE, --delete REMOVE
                        Delete a file from the configuration,
  --validate VALIDATE   Validate the configuration(Also checks if the files exist)
```
### Configuration File

The configuration file is a YAML file with the following format:

```yaml
files:
  - /path/to/server.conf
  - /path/to/deployment.yaml
```
Each entry under files is an absolute path to a file you want to monitor on the system.

## Features

    Monitors changes to specified files and logs them.
    Supports absolute paths.
    Automatically creates an empty configuration file if none is provided.
    Logs details about missing files.


## Contribute
To report on bugs or request functionality you can add issues.
To make changes sumbit a PR, make sure to use the same conventions, be desriptive, small commits, add unittests.
### Install Dev
```bash
git clone https://github.com/impoSTARS/file-mon
cd file-mon
pip install -r requirements
pip install -e .
```
### unit tests
we use pytest
```bash
pytest /tests
```