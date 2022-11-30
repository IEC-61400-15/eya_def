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

## Pre-commit hooks

The [pre-commit](https://pre-commit.com/) package is used for managing  
git hooks. This is part of the python package development (`dev`)
dependencies and is installed automatically during the `eya_def_tools`
package development installation (when using the `[dev]` option). You
can check it has been installed successfully by executing the following.

```bash
pre-commit --version
```

The project configurations for the git hooks are contained within the
file `.pre-commit-config.yaml` at the root repository directory.

Only lint checks are run on both `git commit` and `git push`. Tests
are (currently) not included.

To install `pre-commit` in your local repository for the 'pre-commit'
and 'pre-push' stages, execute the following from the root of the git
repository in an environment where all dependencies are installed.

```bash
pre-commit install --hook-type pre-commit --hook-type pre-push
```

After installation, `pre-commit` will run automatically on `git commit`
and `git push`. Note that some hooks related to formatting (e.g.
`requirements-txt-fixer` and `trailing-whitespace`) will auto-fix files
but return an error on doing so. In these cases the fixed files need to
be staged again and the commit attempt repeated. It should then pass the
second time.

If you want to run `pre-commit` manually on all files in the repository,
including all the hooks, execute the following command.

```bash
pre-commit run --all-files --hook-stage push
```

The `pre-commit` hook dependencies can be updated by executing the
following.

```bash
pre-commit autoupdate
```
