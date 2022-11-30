# The IEC 61400-15-2 EYA DEF

The `eya_def` repo provides a digital format for exchange of information
on wind plant energy yield assessment reporting as defined by the
IEC 61400-15-2 standard. For more information regarding the IEC 61400-15
working group, please see the progress update presentation
[here](https://zenodo.org/record/3952717).

## JSON Schema and examples

The `eya_def` takes the form of a JSON Schema
([iec_61400-15-2_eya_def.schema.json](
json_schema/iec_61400-15-2_eya_def.schema.json)).

Examples of JSON files that implement (comply with) the JSON Schema are
found [here](json_schema/examples).

## Schema diagrams

Visit [Draw.io](https://draw.io) to edit the data tables.

Also see https://www.diagrams.net/blog/single-repository-diagrams for
info about GitHub and draw.io functionality.

  ![Diagram](https://github.com/IEC-61400-15/energy_yield_reporting_DEF/blob/main/SVG_IEC%2061400-15-2%20DEF.drawio.svg)

## Python package

This repo includes the python package `eya_def_tools` for working with
the EYA DEF data model. This package is located [here](python_package)
and has a separate README located [here](python_package/README.md).
