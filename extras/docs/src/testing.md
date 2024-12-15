# Testing Zenplate

## Overview

Zenplate uses `pytest` for testing. The tests are located in the `tests` directory. 
The tests typically reside in one test file per source file, with some exceptions (builtin plugins).

The non-sourcecode resources required for running the tests are in the `tests/fixtures` directory.

In addition to fixtures folder, there are also python source files within the `tests` directory having names ending in `fixtures`.
These source files contain functions and objects that are used in the tests.


## Installing Pre-requisites

To run the tests, you will need to install the pre-requisites. You can do this by running the following command:

```shell
pip install -e .[development]
```

## Running the Tests

```shell
pytest
```

## Running the Linter

```shell
ruff check --fix
```

## Running the Formatter

```shell
ruff format
```

## Running the Type Checker

> Not yet implemented, but will be using `mypy`

[//]: # (```shell)
[//]: # (mypy zenplate)
[//]: # (```)
