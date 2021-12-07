# Advent of Code - Python solutions
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: pylint](https://img.shields.io/badge/%20linter-pylint-%231674b1?style=flat)](https://github.com/PyCQA/pylint)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Pre-commmit: enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)

A place to keep my python solutions to [Advent of Code 2021](https://adventofcode.com/).

Solutions are by no means optimal, but a number of tools have been used to help with clean code and easy use.

# Dependencies

* [Pyenv](https://github.com/pyenv/pyenv) with python >=3.7, for its flexible environment support
* [Poetry](https://python-poetry.org/) for packaging and dependency management
* [Pre-commit](https://pre-commit.com/) to enforce consistency
* [Make](https://www.gnu.org/software/make/) for ease of command line tools

If you want to try out the code but don't want to bother with the above - all you really need is `numpy` and `pandas`!
# Setup (first use)

Set up a poetry environment with pre-commit git hooks installed:

```make env```

To activate your poetry shell to run the code, you can invoke a poetry shell directly

```poetry shell```

Or if you want your typical bash setup in this shell, you can use a `make` command:

```make shell```

To run pre-commit hooks manually:

```make lint```
