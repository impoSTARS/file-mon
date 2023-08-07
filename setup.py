from setuptools import setup, find_packages

setup(
    name="filemon",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "watchdog",
        "loguru",
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "file-monitor = src.monitor:main",
            "file-mon = src.monitor:main",
            "filemon = src.monitor:main",
        ],
    },
    author="Sir AppSec",
    author_email="sirappsec@gmail.com",
    description="A CLI tool to monitor file changes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/impoSTARS/file-monitor",
)
