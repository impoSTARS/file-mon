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
python monitor.py
python monitor.py --config /path/to/pwd/config.yaml
```
If the --config option is omitted, the tool will look for a configuration file named `config.yaml` in the current working directory.

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

