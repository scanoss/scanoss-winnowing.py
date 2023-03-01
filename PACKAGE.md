# SCANOSS Winnowing Python Package
The SCANOSS Winnowing python package provides fast implementation of the winnowing algorithm.

## Installation
To install (from [pypi.org](https://pypi.org/project/scanoss_winnowing)), please run:
```bash
pip3 install scanoss_winnowing
```
To upgrade an existing installation please run:
```bash
pip3 install --upgrade scanoss_winnowing
```

### Package Usage
The **scanoss_winnowing** package can be used in Python projects/scripts. A good example of how to consume it can be found [here](https://github.com/scanoss/scanoss.py/blob/main/src/scanoss/scanner.py).

In general the easiest way to consume it is to import the required module as follows:
```python
from scanoss_winnowing.winnowing import Winnowing

def main():
    winnowing = Winnowing()
    filename = 'test-file.c'
    winnowing.wfp_for_file(filename,filename)
    
if __name__ == "__main__":
    main()
```

## Requirements
Python 3.7 or higher.

## Source code
The source for this package can be found [here](https://github.com/scanoss/scanoss-winnowing.py).

## Changelog
Details of each release can be found [here](https://github.com/scanoss/scanoss-winnowing.py/blob/main/CHANGELOG.md).
