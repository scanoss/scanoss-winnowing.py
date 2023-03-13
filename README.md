# SCANOSS Winnowing Python Library
The SCANOSS Winnowing python package provides fast implementation of the winnowing algorithm.
This is achieved using a C code implementation to generate the snippet IDs.

[![Local Build/Test](https://github.com/scanoss/scanoss-winnowing.py/actions/workflows/python-local-test.yml/badge.svg)](https://github.com/scanoss/scanoss-winnowing.py/actions/workflows/python-local-test.yml)
[![Publish Python Package - PyPI](https://github.com/scanoss/scanoss-winnowing.py/actions/workflows/python-publish-pypi.yml/badge.svg)](https://github.com/scanoss/scanoss-winnowing.py/actions/workflows/python-publish-pypi.yml)

## Installation
To install (from [pypi.org](https://pypi.org/project/scanoss_winnowing)), please run:
```bash
pip3 install scanoss_winnowing
```

## Usage
The **scanoss_winnowing** package can be used in Python projects/scripts. A good example of how to consume it can be found [here](https://github.com/scanoss/scanoss.py/blob/main/src/scanoss/scanner.py).

The `scanoss-py` package leverages this package. It can be installed using:
```bash
pip3 install scanoss[fast_winnowing]
```

## Development
Before starting with development of this project, please read our [CONTRIBUTING](CONTRIBUTING.md) and [CODE OF CONDUCT](CODE_OF_CONDUCT.md).

## Requirements
Python 3.7 or higher.

The dependencies can be found in the [requirements.txt](requirements.txt) and [requirements-dev.txt](requirements-dev.txt) files.

To install dependencies, run:
```bash
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```

## Package Development
More details on Python packaging/distribution can be found [here](https://packaging.python.org/overview/), [here](https://packaging.python.org/guides/distributing-packages-using-setuptools/), and [here](https://packaging.python.org/guides/using-testpypi/#using-test-pypi).

It is good practice to set up a Virtual Env ([venv](https://docs.python.org/3/library/venv.html)) to isolate and simplify development/testing.
If using PyCharm, please follow [these instructions](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html).

In order to develop/test a Python package, it is necessary to register the package locally. This can be done using the following command:
```bash
pip3 install -e .
```
There is also a [Makefile](Makefile) in the repository, which provide helpers to achieve this:
```bash
make dev_setup
```
## Package Deployment
Packaging the library for deployment is done using [setup](https://docs.python.org/3/distutils/setupscript.html).

### Versioning
The version of the package is defined in the [init](src/scanoss_winnowing/__init__.py) file. Please update this version before packaging/releasing an update.

### Packaging
To package the library, please run:
```bash
make dist
```

## Deployment

### Deployment - GitHub Action
There are a number of [GitHub Actions](https://github.com/scanoss/scanoss-winnowing.py/actions) configured to help with the release of the ***scanoss_winnowing*** package:

* Test Release to TestPyPI - Manually triggered from the GitHub UI
  * [Source](https://github.com/scanoss/scanoss-winnowing.py/actions/workflows/testpypi-src.yml)
  * [Windows](https://github.com/scanoss/scanoss-winnowing.py/actions/workflows/testpypi-win.yml)
  * [Linux](https://github.com/scanoss/scanoss-winnowing.py/actions/workflows/testpypi-linux.yml)
  * [Mac](https://github.com/scanoss/scanoss-winnowing.py/actions/workflows/testpypi-mac.yml)
* Official Release to PyPI - Triggered by pushing a tagged version
  * [Multi-OS & Source](https://github.com/scanoss/scanoss-winnowing.py/actions/workflows/python-publish-pypi.yml)

The test deployments have to be triggered manually, while the official release can also be triggered by pushing a tagged version.

### Deployment - Desktop
There are also local packaging command to aid local development/testing.

These use [twine](https://twine.readthedocs.io/en/latest/) to upload packages to [pypi.org](https://pypi.org).
In order to run twine, a user needs to be registered with both [TestPyPI](https://test.pypi.org) and [PyPI](https://pypi.org).
Details for using TestPyPI can be found [here](https://packaging.python.org/guides/using-testpypi) and PyPI [here](https://packaging.python.org/guides/distributing-packages-using-setuptools/#uploading-your-project-to-pypi).

Once the credentials have been stored in $HOME/.pypirc, the following command can be run:
```bash
make publish_test
```
This will deploy the package to [TestPyPI](https://test.pypi.org/project/scanoss_winnowing). Run some tests to verify everything is ok.

Then deploy to prod:
```bash
make publish
```
This will deploy the package to [PyPI](https://pypi.org/project/scanoss_winnowing).

The package will then be available to install using:
```bash
pip3 install scanoss_winnowing
```

## Bugs/Features
To request features or alert about bugs, please do so [here](https://github.com/scanoss/scanoss-winnowing.py/issues).

## Changelog
Details of major changes to the library can be found in [CHANGELOG.md](CHANGELOG.md).

## Background
Details about the Winnowing algorithm used for scanning can be found [here](WINNOWING.md).
