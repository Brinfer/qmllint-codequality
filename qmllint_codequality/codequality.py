"""Module providing a collection of class representing a CodeQuality report.

It's mostly TypedDict.
It facilitate dictionary/JSON manipulation, representing a report in CodeQuality format.

The format of a report can be found on the CodeQuality's Github repository:
https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md#data-types
"""

from enum import Enum, unique
from typing import TypedDict


@unique
class Category(str, Enum):
    """Value that can be set in the ``categories`` field of the CodeQuality JSON.

    .. seealso::
        * https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md#categories
    """

    BUG_RISK = "Bug Risk"
    CLARITY = "Clarity"
    COMPATIBILITY = "Compatibility"
    COMPLEXITY = "Complexity"
    DUPLICATION = "Duplication"
    PERFORMANCE = "Performance"
    SECURITY = "Security"
    STYLE = "Style"


@unique
class Severity(str, Enum):
    """Value that can be set in the ``severity`` field of the CodeQuality JSON."""

    INFO = "info"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"
    BLOCKER = "blocker"


class Position(TypedDict, total=True):
    """A CodeQuality position.

    The typical format is as follow:

    ```json
    {
        "lines": <a line number>
        "column": <a column number>
    }
    ```

    Line and column numbers are 1-based. Therefore, a Position of `{ "line": 2, "column": 3 }` represents the
    third character on the second line of the file.
    """

    lines: int
    """The line number of a position.

    Required.
    """

    column: int
    """The column number of a position.

    Required.
    """


class LocationPositionBased(TypedDict, total=False):
    """A CodeQuality location based on a position.

    The typical format is as follow:

    ```json
    {
        "begin": <a position>
        "end": <a position>
    }
    ```

    See Position to have further details about the ``begin`` and ``end`` fields.
    """

    begin: Position
    """Position at which the issue begins.

    Required.

    .. seealso:: Position
    """

    end: Position
    """Position at which the issue end.

    This field is used to represent a range on which the issue takes place.

    Optional.

    .. seealso:: Position
    """


class Location(TypedDict, total=False):
    """A CodeQuality location.

    Different location format are possible, but only one is used and is as follow:

    ```json
    {
        "path": "<path to the file>",
        "position": <a position>
    }
    ```

    See LocationPositionBased to have further details about the ``position`` field.
    """

    path: str
    """All Locations require a path property, which is the file path.

    Required.
    """

    position: LocationPositionBased
    """Positions refer to specific characters within a source file.

    The position is expressed as a line and column coordinates.

    Optional.

    .. seealso:: LocationPositionBased
    """


class Report(TypedDict, total=True):
    """A CodeQuality report.

    The typical format of an element is as follows:

    ```json
    {
        "type": "issus",
        "severity": "<severity of the issus>",
        "check_name": "<issus name>",
        "description": "<description of the issus>",
        "categories": [
            "<category of the issus>"
        ],
        "fingerprint": "<unique hash>",
        "location": <a location>
        }
    },
    ```

    .. note::
        * Not all the possible elements contained in the file are represented. Only those used in this program are

    .. seealso::
        - Category for the different value of the fields ``categories``.
        - Location to have further details about the ``location`` field.
    """

    type: str
    """Must always be 'issue'

    Required.
    """

    check_name: str
    """A unique name representing the static analysis check that emitted this issue.

    Required.
    """

    description: str
    """A string explaining the issue that was detected.

    Descriptions must be a single line of text (no newlines), with no HTML formatting contained within.
    Ideally, descriptions should be fewer than 70 characters long, but this is not a requirement.

    Required.
    """

    categories: list[Category] | Category
    """At least one category indicating the nature of the issue being reported.

    Required.

    .. seealso:: Category
    """

    location: Location
    """A Location object representing the place in the source code where the issue was discovered.

    Locations refer to ranges of a source code file. A Location contains a path and a source range
    (expressed as lines or positions).

    Required.

    .. seealso:: Location
    """

    severity: Severity
    """A Severity string (info, minor, major, critical, or blocker) describing the potential impact
    of the issue found.

    Optional but required by GitLab.
    """

    fingerprint: str
    """A unique, deterministic identifier for the specific issue being reported to allow a user to exclude
    it from future analyses.

    Optional but required by GitLab.
    """
