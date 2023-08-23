# The IEC 61400-15-2 EYA DEF python toolset
[![Checked with mypy](
http://www.mypy-lang.org/static/mypy_badge.svg)](
http://mypy-lang.org/)
[![Code style: black](
https://img.shields.io/badge/code%20style-black-000000.svg)](
https://github.com/psf/black)
[![Imports: isort](
https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](
https://pycqa.github.io/isort/)
[![pre-commit](
https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](
https://github.com/pre-commit/pre-commit)


The `eya_def_tools` package provides a toolset for working with the
IEC 61400-15-2 EYA Reporting Digital Exchange Format (DEF) in the python
programming language.

## Installation

Installation of the `eya_def_tools` package requires python version 3.11
or higher. It is recommended to install it into a virtual environment,
using for example [virtualenv](https://virtualenv.pypa.io/en/latest/)
or [miniforge](https://github.com/conda-forge/miniforge).

The package can be installed from the git repository as follows. In the
future it is intended to add it on PyPI for installation directly with
`pip` (i.e. without the need to clone the repository).

```bash
# Download the source code from the 'main' branch
git clone -b main https://github.com/IEC-61400-15/eya_def.git

# Activate your virtual environment or conda environment prior to
# installing, e.g. with a virtualenv environment in Windows:
<path_to_virtual_environment>\Scripts\activate
# or with a conda environment:
conda activate <environment_name>

# Navigate to python package directory
cd eya_def
cd eya_def_tools

# Install `eya_def_tools`
pip install .
```

To install in editable mode for development, including the development
dependencies, replace the last command by the following.

```bash
pip install -e .[dev]
```

The `erd` flag can be added to also install dependencies for using the
`erdantic` package to generate entity relationship diagrams (ERDs) from
the pydantic data models. This requires a prior installation of the
`graphviz` software. In case of issues installing the `pygraphviz`
package, using the following options may help.

```bash
pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz==<DESIRED_VERSION>
```

## Documentation

The documentation of the package (including user documentation and API
documentation) is created using [Sphinx](https://www.sphinx-doc.org).
The API documentation is generated automatically from the docstrings
within the source code.

To build the HTML documentation, navigate to the docs directory and
execute the following.

```bash
make html
```

## Testing

The test suite is built using [pytest](https://docs.pytest.org). The
`pytest` package is included as a dependency in the requirements and
is installed automatically (together with other dependencies) upon
installation of `eya_def_tools`.

To run the test suite with coverage reporting, including details on
statements with missing coverage, simply execute the following at the
top-level python package directory.

```bash
pytest --pyargs eya_def_tools --cov=eya_def_tools --cov-report term-missing
```

Contributors are encouraged to write tests to cover new features.

## Type hints and static type checking

Type hints and static type checking are optional in Python, but make
code dramatically more readable and can help identify type issues that
would otherwise trigger errors at runtime. This project enforces the use
of type hints and runs static type checking using the
[mypy](https://mypy.readthedocs.io/en/stable/) tool, which is part of
the `pre-commit` hooks

The `mypy` static type checking can also be run by executing the
following at the root of the repository directory.

```bash
mypy --config-file pyproject.toml
```

The mypy configurations are contained in the
[pyproject.toml file](pyproject.toml).
