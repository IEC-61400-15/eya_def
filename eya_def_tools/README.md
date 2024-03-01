# The IEC 61400-15-2 EYA DEF Python toolset

The `eya_def_tools` package provides a toolset for working with the
IEC 61400-15-2 EYA Reporting Digital Exchange Format (DEF) in the Python
programming language. It includes a nested `pydantic` data model for the
EYA DEF that is equivalent of the JSON Schema.

This README file only briefly covers some key topics in relation to the
Python package for convenient reference. Full details will be provided
at a separate documentation site, which still needs to be developed. The
README for the EYA DEF repo is located [here](../README.md) and includes
all general information (i.e. all information that is not specific to
the Python package).

## User guidance

The following provides brief guidance for users on how to get started
using the `eya_def_tools` package.

### Installation

Installation of the `eya_def_tools` package requires python version 3.11
or higher. It is recommended to install it into a virtual environment,
using for example [virtualenv](https://virtualenv.pypa.io/en/latest/)
or [miniforge](https://github.com/conda-forge/miniforge).

The package can be installed from the Git repository as follows. In the
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

# Navigate to Python package directory
cd eya_def
cd eya_def_tools

# Install 'eya_def_tools'
pip install .
```

### File I/O

The EYA DEF tools include some utilities for reading from and writing
to data files, which are located under `eya_def_tools.io`.

The code snippet below shows an example of parsing an EYA DEF JSON data
file into an `EyaDefDocument` model instance. If any data in the file is
invalid, the parse operation will fail with an exception including the
details of the validation errors.

```python
from pathlib import Path
from eya_def_tools.io import parser
eya_def_document = parser.parse_file(filepath=Path("C:/path/to/my/eya_def_file.json"))
print(eya_def_document)
```

## Developer guidance

The following provides brief guidance for developers on how to set up a
development environment and use the development tools.

### Development installation

To install `eya_def_tools` in editable mode for development, including
the development dependencies, use the following command.

```bash
pip install -e .[dev]
```

The `erd` flag can be added optionally to also install dependencies for
using the `erdantic` package to generate entity relationship diagrams
(ERDs) from the pydantic data models. This requires a prior installation
of the [Graphviz](https://graphviz.org/) software.

In a Windows environment, you may need to include additional options
when installing `pygraphviz` with `pip`, to specify the locations for
the `graphviz` installation. See the [PyGraphviz documentation](
https://pygraphviz.github.io/documentation/stable/install.html) for more
detail.

### Documentation build

The documentation of the package (including user documentation and API
documentation) is created using [Sphinx](https://www.sphinx-doc.org).
The API documentation is generated automatically from the docstrings
within the source code.

To build the HTML documentation, navigate to the docs directory and
execute the following.

```bash
make html
```

### Testing

The test suite is built using [pytest](https://docs.pytest.org). The
`pytest` package is included as a dependency in the requirements and
is installed automatically (together with other dependencies) upon
installation of `eya_def_tools`.

To run the test suite with coverage reporting, including details on
statements with missing coverage, simply execute the following at the
top-level Python package directory.

```bash
pytest --pyargs eya_def_tools --cov=eya_def_tools --cov-report term-missing
```

Contributors are encouraged to write tests to cover new features.

### Type hints and static type checking

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

### GitHub Actions pipelines

The `eya_def` repo has a GitHub Actions pipeline configured to run
checks on pull requests (PRs) to check file formatting and ensure that
all tests pass.

### Pre-commit hooks

The [pre-commit](https://pre-commit.com/) package is used for managing  
Git hooks. This is part of the Python package development dependencies
and is installed automatically during the `eya_def_tools` package
development installation (when using the `[dev]` option). You can check
it has been installed successfully by executing the following.

```bash
pre-commit --version
```

The project configurations for the Git hooks are contained within the
file `.pre-commit-config.yaml` at the root repository directory.

Lint checks are run on both `git commit` and `git push`. Tests are
not included in the Git hooks.

To install `pre-commit` in your local repository for the 'pre-commit'
and 'pre-push' stages, execute the following from the root of the Git
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
