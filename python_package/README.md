# IEC 61400-15-2 Reporting Digital Exchange Format (DEF) Python Toolset

The `iec_eya_def_tools` python package provides a toolset for working with
the IEC 61400-15-2 Reporting Digital Exchange Format (DEF).

Note that the package requires an installation of Python version 3.10 or
higher.

## Installation

The package can be installed from the git repository as follows.

```bash
    # Download the source code from the `master` branch
    git clone -b master https://github.com/IEC-61400-15/energy_yield_reporting_DEF.git

    # Activate your virtual environment or conda environment prior to
	# installing, e.g.:
	# <path_to_virtual_environment>\Scripts\activate
    # conda activate <environment_name>
    
    # Navigate to python package directory
    cd energy_yield_reporting_DEF
	cd python_package

    # Install `iec_eya_def_tools`
    pip install .
```

To install in editable mode for development, replace the last command by:
```bash
    # Install `iec_eya_def_tools` in editable mode
    pip install -e .
```
