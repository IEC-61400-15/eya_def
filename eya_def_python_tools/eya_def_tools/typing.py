"""Type definitions for the EYA DEF data model.

"""

from typing import TypeAlias

NestedAnnotatedFloatDict: TypeAlias = (
    dict[str, float]
    | dict[str, dict[str, float]]
    | dict[str, dict[str, dict[str, float]]]
    | dict[str, dict[str, dict[str, dict[str, float]]]]
)
