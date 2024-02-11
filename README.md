# The IEC 61400-15-2 EYA DEF

The IEC 61400-15-2 Energy Yield Assessment Digital Exchange Format
(EYA DEF) defines a complementary format for energy yield assessment
reporting to the main written report, aimed at facilitating automated
solutions for data exchange, and is published in the form of a JSON
Schema. Whereas the written EYA report provides an effective narrative
for a human reader, the digital exchange format provides the clear
definitions of namespace, structure and format required for computer
systems to exchange energy yield assessment data.

This repo provides all source data files for the EYA DEF, along with
associated material and tools, as well as serving as the platform for
development work.

This README file only briefly covers some key topics for convenient
reference. Full details will be provided at a separate documentation
site, which still needs to be developed.

## Use cases



## The EYA DEF JSON Schema

The latest version of EYA DEF JSON Schema is available here [here](
json_schema/iec_61400-15-2_eya_def.schema.json). The JSON Schema is the
primary definition of the EYA DEF data model.

## Example EYA DEF JSON documents

Examples of JSON document files that implement (comply with) the JSON
Schema are found [here](json_schema/examples).

## Python package

This repo includes the Python package [eya_def_tools](eya_def_tools),
which provides a convenient interface for working with the EYA DEF data
model in a Python environment. It has a separate README file, which is
located [here](eya_def_tools/README.md).

## Schema diagrams

The Python package (see [below](#Python-package)) uses [erdantic](
https://erdantic.drivendata.org/stable/) to generate graphical
representations of the `pydantic` data model. Note that the data types
shown in the diagrams are the Python types defined in the `pydantic`
data model and not the JSON Schema types.

The top levels of the current draft of the data model is illustrated
below.

  ![data_model_top_levels_diagram](diagrams/eya_def_document_top_level.svg)

## Developer guidance

For guidance related to tools and processes for development work, see
the [Python package README](eya_def_tools/README.md). The Python package
forms an integral part of the development workflow.
