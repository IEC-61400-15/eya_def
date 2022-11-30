# The IEC 61400-15-2 EYA DEF python toolset
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

The `eya_def_tools` package provides a toolset for working with the
IEC 61400-15-2 EYA Reporting Digital Exchange Format (DEF) in the python
programming language.

## Installation

Installation of the `eya_def_tools` package requires python version 3.10
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
path_to_virtual_environment\Scripts\activate
# or with a conda environment:
conda activate environment_name

# Navigate to python package directory
cd eya_def
cd python_package

# Install `eya_def_tools`
pip install .
```

To install in editable mode for development, including the development
dependencies, replace the last command by the following.

```bash
pip install -e .[dev]
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

To run the test suite, simply execute the following at the top-level
python package directory.

```bash
pytest .
```

Contributors are encouraged to write tests to cover new features.
